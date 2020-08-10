import time
import restful
import json
import boto3
import sys
import ast

with open('test.json', "r") as data:
     dictionary = ast.literal_eval(data.read())
print(dictionary[0])

client = boto3.client('ivs', aws_access_key_id ='AKIAUJ3D6TYQNACGXDPK' , aws_secret_access_key = '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')
name_stream = input('Channel Name:')
channel_all = client.list_channels(
        filterByName = name_stream,
        maxResults=50)
channel_list = channel_all['channels']
readable_channel = json.dumps(channel_list[0]["arn"])
time.sleep(12)
response = client.put_metadata(
        channelArn=readable_channel[1:-1],
        metadata=dictionary[0],
time.sleep(12)
response = client.put_metadata(
        channelArn=readable_channel[1:-1],
        metadata=dictionary[1],
time.sleep(12)
response = client.put_metadata(
        channelArn=readable_channel[1:-1],
        metadata=dictionary[2],
time.sleep(12)
response = client.put_metadata(
        channelArn=readable_channel[1:-1],
        metadata=dictionary[3],
response = client.put_metadata(
        channelArn=readable_channel[1:-1],
        metadata=dictionary[4],
time.sleep(12)
