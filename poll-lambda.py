import urllib3
import json
import datetime as dt
import time
import boto3
import os
from decimal import Decimal

PROPUBLICA_API_KEY = os.environ['PROPUBLICA_API_KEY']

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):

    http = urllib3.PoolManager()

    retries = 0
    data = []
    offset = [0, 20, 40, 60, 80]
    url = 'https://api.propublica.org/congress/v1/116/both/bills/introduced.json'

    while len(data) == 0 and retries < 5:
        for x in offset:
            retries += 1

            r = http.request('GET', url+f'?offset={x}', headers={'X-API-Key': f'{PROPUBLICA_API_KEY}'})

            data = json.loads(r.data.decode('utf-8'))
    
            if len(data) == 0:
                print(f"Empty response from ProPublica API after {retries} retries")

            data = data['results'][0]['bills']
            
            insert_data(data)


def insert_data(recList):
    table = dynamodb.Table('Bills')
    for i in range(len(recList)):
        record = recList[i]
        table.put_item(
            Item={
                "bill_id": record['bill_id'],
                "bill_type": record['bill_type'],
                "number": record['number'],
                "title": record['title'],
                "sponsor_title": record['sponsor_title'],
                "sponsor_id": record['sponsor_id'],
                "sponsor_name": record['sponsor_name'],
                "sponsor_state": record['sponsor_state'],
                "sponsor_party": record['sponsor_party'],
                "cosponsors": record['cosponsors'],
                "introduced_date": record['introduced_date'],
                "introduced_date_unix": time_helper(record['introduced_date']),
                "latest_major_action_date": record['latest_major_action_date'],
                "latest_major_action_date_unix": time_helper(record['latest_major_action_date']),
                "latest_major_action": record['latest_major_action'],
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
                "committee_codes": record['committee_codes'],
                "subcommittee_codes": record['subcommittee_codes'],
                "subjects": record['primary_subject'],
                "summary": record['summary'],
                "summary_short": record['summary_short'],
                "congressdotgov_url": record['congressdotgov_url'],
                "entry_timestamp": Decimal(time.time())
            }
        )


def time_helper(timestring):
    try:
        new_time = Decimal(time.mktime(dt.datetime.strptime(timestring, "%Y-%m-%d").timetuple()))
    except:
        new_time = None
    return new_time