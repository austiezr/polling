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
    url = 'https://api.propublica.org/congress/v1/lobbying/latest.json'

    while len(data) == 0 and retries < 5:
        for x in offset:
            retries += 1

            r = http.request('GET', url + f'?offset={x}',
                             headers={'X-API-Key': f'{PROPUBLICA_API_KEY}'})

            data = json.loads(r.data.decode('utf-8'))

            if len(data) == 0:
                print(
                    f"Empty response from ProPublica API after {retries} retries")

            data = data['results'][0]['lobbying_representations']

            insert_data(data)


def insert_data(recList):
    table = dynamodb.Table('Lobbying_Representations')
    for i in range(len(recList)):
        record = recList[i]
        table.put_item(
            Item={
                "representation_id": int(record['id']),
                "client": record['lobbying_client']['name'],
                "registrant": record['lobbying_registrant']['name'],
                "issues": record['specific_issues'],
                "lobbyists": [x['name'] for x in record['lobbyists']],
                "latest_filing_date": record['latest_filing']['filing_date'],
                "latest_filing_date_unix": time_helper(
                    record['latest_filing']['filing_date']),
                "latest_filing_report_year": record['latest_filing'][
                    'report_year'],
                "latest_filing_report_year_unix": time_helper(
                    record['latest_filing']['report_year']),
                "latest_filing_report_type": record['latest_filing'][
                    'report_type'],
                "latest_filing_pdf": record['latest_filing']['pdf_url'],
                "inhouse": record['inhouse'],
                "signed_date": record['signed_date'],
                "signed_date_unix": time_helper(record['signed_date']),
                "effective_date": record['effective_date'],
                "effective_date_unix": time_helper(record['effective_date']),
                "entry_timestamp": Decimal(time.time())
            }
        )


def time_helper(timestring):
    try:
        new_time = Decimal(time.mktime(
            dt.datetime.strptime(timestring, "%Y-%m-%d").timetuple()))
    except:
        new_time = None
    return new_time