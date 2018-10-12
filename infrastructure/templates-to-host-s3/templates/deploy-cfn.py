import sys
import boto3

cloudformation = boto3.client('cloudformation', region_name=sys.argv[6])

def create_stack(service_name, test_account, production_account,template_bucket, infra_template_bucket):

    with open('02.infra-per-microservice.yaml', 'r') as content_file:
        content = content_file.read()
        cloudformation.create_stack(
            StackName=service_name + "-test-resources",
            TemplateBody=content,
            Capabilities = ["CAPABILITY_NAMED_IAM"],
            Parameters=[{
                "ParameterKey": "ServiceName",
                "ParameterValue": service_name
                },
                {
                    "ParameterKey": "TestAccount",
                    "ParameterValue": test_account
                },
                {
                    "ParameterKey": "ProductionAccount",
                    "ParameterValue": production_account
                },
                {
                    "ParameterKey": "TemplateBucket",
                    "ParameterValue": template_bucket
                }
                ,
                {
                    "ParameterKey": "InfrastructureTemplateBucket",
                    "ParameterValue": infra_template_bucket
                }
            ]
        )
        cloudformation.get_waiter('stack_create_complete').wait(StackName=service_name + "-test-resources")

def deploy_cfn():
    if len(sys.argv) == 0:
        return
    service_name = sys.argv[1]
    test_account = sys.argv[2]
    production_account = sys.argv[3]
    template_bucket = sys.argv[4]
    infra_template_bucket = sys.argv[5]
    print(service_name)
    try:
        response = cloudformation.describe_stacks( StackName=service_name + "-test-resources")
        if (response["Stacks"] or len(response["Stacks"][0]["StackId"]) > 0):
            print("stack already exists")
            return
        else:
            create_stack(service_name, test_account, production_account,template_bucket, infra_template_bucket)
    except Exception as e:
        print(e)
        create_stack(service_name, test_account, production_account, template_bucket, infra_template_bucket)

if __name__ == '__main__':
    deploy_cfn()
