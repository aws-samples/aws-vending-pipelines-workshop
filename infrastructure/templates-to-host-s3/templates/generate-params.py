import json

params = {}
def generate_params():
    with open('/tmp/cfn-output.json') as json_data:
        outputs = json.load(json_data)
        for output in outputs:
            params[output['OutputKey']] = output['OutputValue']
    with open('/tmp/cfn-output.json', 'w') as outfile:
        json.dump(params, outfile)

if __name__ == '__main__':
    generate_params()
