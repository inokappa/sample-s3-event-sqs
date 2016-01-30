'''
## Special Thanks

reference : https://code.google.com/p/kjk/source/browse/trunk/scripts/test_parse_s3_log.py
reference : http://qiita.com/marcy-terui/items/6dbf2969bc69fd3d6c13
reference : http://qiita.com/ikawaha/items/c654f746cfe76b888a27
'''

from __future__ import print_function
import re
import os
import logging
import sys
import json
import ast
import datetime
from datetime import datetime as dt
import time
import pytz
import urllib
import boto3
from boto3.session import Session

session = Session(
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)

sqs = session.resource('sqs')
s3 = session.client('s3')

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

def parse_s3_log_line(line):
    match = s3_line_logpat.match(line.strip())
    result = [match.group(1+n) for n in range(17)]
    return result

def dump_parsed_s3_line(parsed):
    log = {}
    for (name, val) in zip(s3_names, parsed):
        if name == 'datetime':
            val = datetime.datetime.strptime(val.split(' ')[0], '%d/%b/%Y:%H:%M:%S').replace(tzinfo=pytz.utc)
            val = val.isoformat()
        log.update(ast.literal_eval('{"%s": "%s"}' % (name, val)))
    return json.dumps(log)

def recive_event_message():
    queue = sqs.get_queue_by_name(QueueName=os.getenv('SQS_QUEUE_NAME'))
    for message in queue.receive_messages(MessageAttributeNames=['*']):
       body = message.body
       message.delete()
       return json.loads(body)

def main():
    while 1:
        logging.info("Start polling...")
        time.sleep(60) 
        event = recive_event_message()
        if event == None:
            logging.info("Event does not exists...")
            continue
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key']).decode('utf8')
        print(bucket)
        print(key)
        #try:
        #    logging.info('Getting object {} from bucket {}.'.format(key, bucket))
        #    response = s3.get_object(Bucket=bucket, Key=key)
        #    print(response)
        #except Exception as e:
        #    print(e)
        #    logging.error('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        #    raise e

if __name__ == "__main__":
    main()
