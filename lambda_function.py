import json
import boto3

def lambda_handler(event, context):
    
    region = event['queryStringParameters']['region']
    instance_tag_value = event['queryStringParameters']['instance']
    instance_ids = []
    
    ec2 = boto3.client('ec2', region_name=region)

    filter = [{
        'Name': 'tag:SmartStart', 
        'Values': [instance_tag_value]
    }]
    
    instances = ec2.describe_instances(Filters=filter)
    for resevation in instances['Reservations']:
        for reservation_instance in resevation['Instances']:
            if reservation_instance['State']['Code'] == 80:
                instance_ids.append(str(reservation_instance['InstanceId']))
                print(instance_ids)
    
    if len(instance_ids) > 0:
        ec2.start_instances(InstanceIds=instance_ids)
        return {
            'statusCode': 200,
            'body': json.dumps('Started instance(s) {} selected with the tag SmartStart={}'.format(instance_ids, instance_tag_value))
        }
    else:
        return {
            'statusCode': 200,
            'body': json.dumps('No stopped instance with the tag SmartStart={}'.format(instance_tag_value))
        }
