from flask import Flask, render_template, redirect  # , request
# import json
import os
from flask_cors import CORS
from dotenv import load_dotenv
import boto3


load_dotenv()
app = Flask(__name__)
CORS(app)

creds = {
    'AWS_KEY_ID': os.environ.get('AWS_KEY_ID'),
    'AWS_SECRET_KEY': os.environ.get('AWS_SECRET_KEY')
}

dynamodb = boto3.client('dynamodb',
                        aws_access_key_id=creds['AWS_KEY_ID'],
                        aws_secret_access_key=creds['AWS_SECRET_KEY'],
                        region_name='us-west-1')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/bills')
def bills():
    response = dynamodb.scan(
        TableName='Bills',
        Select='ALL_ATTRIBUTES',
        FilterExpression='active = :true',
        ExpressionAttributeValues={':true': {'BOOL': True}}
    )
    response = sorted(response['Items'],
                      key=lambda x: x['latest_major_action_date_unix']['N'],
                      reverse=True)
    return render_template('bills.html',
                           response=response)


@app.route('/lobbying')
def lobbying():
    response = dynamodb.scan(
        TableName='Lobbying_Representations',
        Select='ALL_ATTRIBUTES'
    )
    response = sorted(response['Items'],
                      key=lambda x: x['latest_filing_date_unix']['N'],
                      reverse=True)[:20]

    return render_template('lobbying.html',
                           response=response)


if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=False, host='0.0.0.0')
