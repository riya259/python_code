import boto3
client = boto3.client('ec2')
dynamodb = boto3.resource('dynamodb')
def vpc_creation(input_cidr,vpc_name):
    response = client.create_vpc(
        CidrBlock=input_cidr,
        TagSpecifications=[{
            'ResourceType': 'vpc',
            'Tags': [{'Key': 'Name', 'Value': vpc_name},]
        },]
    )
    for i in response:
        vpc_id = response[i].get(u'VpcId')
        print(f"vpc_id = {vpc_id}")
def dynamodb_creation(input_cidr,vpc_name,table_name):
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'vpc_name',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'vpc_cidr',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'vpc_name',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'vpc_cidr',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    # Wait until the table exists.
    table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
    table.put_item(
        Item={
            'vpc_name': vpc_name,
            'vpc_cidr': input_cidr,
            'status': 'Created'
            }
        )

vpc_creation('10.0.0.0/16','vpc-test')
dynamodb_creation('10.0.0.0/16','vpc-test','riya')
