import urllib3
import json
import datetime as dt
import time
import boto3
import os
from decimal import Decimal
import xmltodict

PROPUBLICA_API_KEY = os.environ['PROPUBLICA_API_KEY']

dynamodb = boto3.client('dynamodb')


def lambda_handler(event, context):

    http = urllib3.PoolManager()

    bills = extract_data()
    print(bills)

    url = 'https://api.propublica.org/congress/v1/'

    for x in bills:
        data = []
        retries = 0

        congress = x[-3:]
        bill_slug = x[:-4]

        while len(data) == 0 and retries < 5:
            retries += 1

            r = http.request('GET', url+f'{congress}/bills/{bill_slug}',
                             headers={'X-API-Key': f'{PROPUBLICA_API_KEY}'})

            try:
                data = json.loads(r.data.decode('utf-8'))
                data = data['results'][0]

            except json.decoder.JSONDecodeError:
                data = xmltodict.parse(r.data.decode('utf-8'))
                data = json.dumps(data)
                data = json.loads(data)['result_set']['results']

            if len(data) == 0:
                print(f"Empty response from ProPublica API after {retries} retries")

            insert_data(data)


def extract_data():

    bills = []

    response = dynamodb.scan(
        TableName='Bills',
        Select='SPECIFIC_ATTRIBUTES',
        ProjectionExpression='bill_id',
        FilterExpression='active = :true',
        ExpressionAttributeValues={':true': {'BOOL': True}}
    )

    bills.extend([x['bill_id']['S'] for x in response['Items']])

    incomplete = 'LastEvaluatedKey' in response.keys()
    if incomplete is True:
        while incomplete is True:
            response = dynamodb.scan(
                TableName='Bills',
                Select='SPECIFIC_ATTRIBUTES',
                ProjectionExpression='bill_id',
                ExclusiveStartKey=response['LastEvaluatedKey']['bill_id'],
                FilterExpression='active = :true',
                ExpressionAttributeValues={':true': {'BOOL': True}}
                )
            bills.extend([x['bill_id']['S'] for x in response['Items']])
            incomplete = 'LastEvaluatedKey' in response.keys()

    return bills


def insert_data(record):
    table = boto3.resource('dynamodb')
    table = table.Table('Bills')
    table.put_item(
        Item={
            "bill_id": record['bill_slug']+'-116',
            "bill_type": record['bill_type'],
            "number": record['number'],
            "title": record['title'],
            "sponsor_title": record['sponsor_title'],
            "sponsor_id": record['sponsor_id'],
            "sponsor_name": record['sponsor'],
            "sponsor_state": record['sponsor_state'],
            "sponsor_party": record['sponsor_party'],
            "cosponsors": record['cosponsors'],
            "cosponsors_by_party": record['cosponsors_by_party'],
            "introduced_date": record['introduced_date'],
            "introduced_date_unix": time_helper(record['introduced_date']),
            "latest_major_action_date": record['latest_major_action_date'],
            "latest_major_action_date_unix": time_helper(record['latest_major_action_date']),
            "latest_major_action": record['latest_major_action'],
            "actions": record['actions'],
            "active": record['active'],
            "house_passage": record['house_passage'],
            "house_passage_unix": time_helper(record['house_passage']),
            "senate_passage": record['senate_passage'],
            "senate_passage_unix": time_helper(record['senate_passage']),
            "last_vote": record['last_vote'],
            "last_vote_unix": time_helper(record['last_vote']),
            "enacted": record['enacted'],
            "enacted_unix": time_helper(record['enacted']),
            "vetoed": record['vetoed'],
            "vetoed_unix": time_helper(record['vetoed']),
            "committees": record['committees'],
            "committee_codes": record['committee_codes'],
            "subcommittee_codes": record['subcommittee_codes'],
            "subjects": record['primary_subject'],
            "summary": record['summary'],
            "summary_short": record['summary_short'],
            "congressdotgov_url": record['congressdotgov_url'],
            "versions": record['versions'],
            "presidential_statements": record['presidential_statements'],
            "votes": record['votes'],
            "entry_timestamp": Decimal(time.time())
        }
    )


def time_helper(timestring):
    try:
        new_time = Decimal(time.mktime(dt.datetime.strptime(timestring, "%Y-%m-%d").timetuple()))
    except:
        new_time = None
    return new_time