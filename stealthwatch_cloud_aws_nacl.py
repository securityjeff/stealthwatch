import json

import boto3
import urllib3

# Replace these items with the values from the appropriate SWC web portal
CUSTOMER = 'customer'
API_USER = 'customer@domain.com'
API_KEY = 'abc123_insert_key'

# Other alert types could be added here
ALERT_TYPES = {
    'Excessive Access Attempts (External)',
}

# Prepare the headers for requests to the Observable API
OBSERVATIONS_ENDPOINT = (
    'https://{}.obsrvbl.com/api/v3/observations/all/'.format(CUSTOMER)
)
REQUEST_HEADERS = {
    'Authorization': 'ApiKey {}:{}'.format(API_USER, API_KEY),
    'Accept': 'application/json'
}

REMOTE_IP_FIELDS = {'remote_ip', 'connected_ip', 'external_ip'}


# Retrieves observation details for a particular alert
def get_obs_data(alert_id):
    http = urllib3.PoolManager()
    url = OBSERVATIONS_ENDPOINT + '?alert={}'.format(alert_id)
    response = http.request(
        'GET',
        url,
        headers=REQUEST_HEADERS
    )
    return json.loads(response.data)['objects']


def lambda_handler(event, context):
    ec2_client = boto3.client('ec2')

    alert_json = event['Records'][0]['Sns']['Message']
    alert_data = json.loads(alert_json)

    # React to known alert types only
    alert_type = alert_data['type']
    print('Alert type is {}'.format(alert_data['type']))
    if alert_type not in ALERT_TYPES:
        print('Unrecognized alert type, exiting')
        return

    # Extract remote IPs from observations
    alert_id = int(alert_data['id'])
    remote_ips = set()
    for obs_data in get_obs_data(alert_id):
        for field in REMOTE_IP_FIELDS:
            if field in obs_data:
                remote_ips.add(obs_data[field])

    # Look up the source's VPC
    source_name = alert_data['source_name']
    instance_response = ec2_client.describe_instances(
        Filters=[{'Name': 'instance-id', 'Values': [source_name]}]
    )
    try:
        vpc_id = instance_response['Reservations'][0]['Instances'][0]['VpcId']
    except (IndexError, KeyError):
        print('Could not find instance {}'.format(source_name))
        return

    # Find the VPC's ACL
    acl_response = ec2_client.describe_network_acls(
        Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}]
    )
    try:
        acl_id = acl_response['NetworkAcls'][0]['NetworkAclId']
    except (IndexError, KeyError):
        print('Could not find ACL info for {}'.format(vpc_id))
    entries = acl_response['NetworkAcls'][0]['Entries']
    min_rule = min(e['RuleNumber'] for e in entries)
    print(repr(entries))
    already_blocked = {e['CidrBlock'] for e in entries if 'CidrBlock' in e}

    cidrs_to_block = {'{}/32'.format(x) for x in remote_ips}
    cidrs_to_block -= already_blocked

    # Create new rules
    for i, cidr_block in enumerate(cidrs_to_block, 1):
        rule_number = min_rule - i
        if rule_number <= 0:
            print('Out of space for rules')
            break
        print('Creating: {}. DENY {}'.format(rule_number, cidr_block))
        create_response = ec2_client.create_network_acl_entry(
            #  DryRun=True,  # Comment out DryRun to make this happen for real
            NetworkAclId=acl_id,
            RuleNumber=rule_number,
            Protocol='-1',
            RuleAction='deny',
            Egress=False,
            CidrBlock=cidr_block,
        )
        print(create_response)
