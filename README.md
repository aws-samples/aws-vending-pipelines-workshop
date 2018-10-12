# AWS Vending Pipelines Workshop

Sample code for "Empowering developers in highly compliant environments" workshop

The workshop shows how developers can be vended pipelines to release their serverless and container based applications. It offers a self-service mechanism increasing agility while still allowing governance and control

This code should not be used as is for production workloads but rather as guidance for how to automate pipeline vending to strike a balance between agility and control

## License Summary

This sample code is made available under a modified MIT license. See the LICENSE file.

## Pre-requisites

* Two AWS Accounts to act as "Non-Prod" and "Prod" environments. Ideally there should be separate accounts for Tooling and Service Catalog Products but they are merged into Non-Prod here for simplicity
* Permissions to create DevOps resources (EC2, Lambda, API Gateway, Code* services, Cloudformation, KMS...etc.) in both accounts

## Release Process

This is the release process followed for this workshop. For more information check "Teams" section in this whitepaper: https://d1.awsstatic.com/whitepapers/DevOps/practicing-continuous-integration-continuous-delivery-on-AWS.pdf

![Release Process](/images/release-process.png)

## Setup

### A. Create infrastructre and required roles (CENTRAL IT / OPS/ PARTNER)

![Infrastructure](/images/01.infra.png)

1. [Non-Prod] Create an S3 Bucket in same region you intend to run application in. This bucket will be referred to later as "Template Bucket". Copy all contents of "infrastructure/templates-to-host-s3" under S3 prefix "templates" in the "Template Bucket". Also zip all the contents of folder "templates" under "infrastructure/templates-to-host-s3"  as templates.zip and copy into the root of the bucket. The final structure should look like follows:

![Templates](/images/bucket-templates.png)
![Bucket root](/images/bucket-root.png)

2. [Non-Prod, Prod] Create VPC and ECS Cluster resources using "infrastructure/cluster.yaml" templates. Leverage CloudFormation StackSets for that task.
3. [Non-Prod, Prod] Using output values from previous templates, replace values of ssm parameters in "infrastructure/non-prod/ssm-params.yml" and run it along with "infrastructure/prod/prod-ssm-params.yml" in the corresponding account
4. [Non-Prod] Create resources, IAM roles and policies required to run pipelines in Non-Prod account using infrastructure/non-prod/admin-resources.yml
5. [Prod] Create IAM roles and policies required to deploy services into Prod account using infrastructure/prod/prod-admin-resources.yml. Pass ServiceName as "admin-resources"
6. [Non-Prod] Allow Prod roles access to Artifact Bucket using bucket policy defined in infrastructure/non-prod/admin-bucket-policy.yml

### B. Create an AWS Service Catalog Portfolio of approved release Products (TOOLING DEVELOPER)

![Tooling](/images/02.tooling.png)

1. [SC Account: Could be Non-Prod for simplicity] Create Service Catalog Portfolio "App Services" adding a product using template in infrastructure/sc account/sc-microservice-ecs.yml. Create another portfolio "Team Services" and add a product using template infrastructure/sc account/sc-team-non-prod-permissions.yaml. Create a Lanuch Constraint to allow products be launched with an IAM role having enough permissions to manage all resources used in this workshop. This role will be trusted to be used with Service Catalog only as it will have admin permissions. For more information on Creating SC Products amd Portfolios check https://docs.aws.amazon.com/servicecatalog/latest/adminguide/getstarted.html
2. [Non-Prod] Give developer teams access to "App Services" portfolio and give team leaders access to "Team Services" portfolio

### C. Create mircroservice team permissions (APP LEADER)

![Team permissions](/images/03.team-permissions.png)

Repeat for every microservice

1. [NonProd] Login with AppLeader role that typically should have ServiceCatalogEndUserFullPermissions policy attached. This is a person who assigns permissions to a team at the start of a new project to launch their required pipelines
2. [Non-Prod] Navigate through "Team Services" portfolio and launch team permissions product passing:
   * Microservice name: This acts as a prefix giving the app team access to all resources starting with that prefix. Accordingly, teams should always create CodeCommit repos and pass service name params starting with that prefix. In this sample code, the microservice name used is "tasks"
   * Team role name: Name of the IAM role assigned to the microservice team and typically should have been done using an Identity Federation system. For more information on identity federation on AWS check https://aws.amazon.com/identity/federation/

### D1. Deploy Microservice - ECS (DEVELOPERS)

![Vend Pipeline](/images/04.vend-pipeline.png)

Repeat for every microservice

1. [NonProd] Login with team role that perimssions were attached to in section C
2. [Non-Prod] Go to service catalog console and navigate through "Team Services" portfolio and launch product "ECS Microservice" passing:
    * ServiceName: Name of the CodeCommit repo to be created in next step. Must start with prefix assigned to team. Check step C2
    * InfraBucket: Bucket with infrastructure for application like a CloudFormation template to create a dynamodb table for example.
    * InfraBucketArchive: Name and prefix of Zip file containing infrastructure CFN templates for application. A sample can be found under "application/sample infrastructure"
3. [Non-Prod] Create CodeCommit repo in same region and note the name of your code. For example, tasks

### D2. Deploy Microservice - Serverless (DEVELOPERS)

Repeat for every microservice

1. [Non-Prod] You can use same code repo as above if serverless SAM template is on root folder of that repo
2. [Non-Prod] Run 'Serverless Microservice' Service Catalog product passing:
    * ServiceName: Name of the CodeCommit repo

### E. Commit Microservice code (DEVELOPERS)

![Commit Code](/images/05.commit-code.png)

Repeat for every microservice

1. [Non-Prod] Push microservice code into CodeCommit repo using git client. This pushed code typically includes application code and buildspec file for building and running tests. In case of serverless, it includes a template.yaml file on the root level. Infrastructure templates must have a main.yaml template which can have as many nested templates. It also must have on root level "test-stack-configuration.json" and "prod-stack-configuration.json" template configuration files for test and prod environments respectively. A sample infrastructure set can be found under "application/sample infrastructure". For more information on template configuration files check https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/continuous-delivery-codepipeline-basic-walkthrough.html

***