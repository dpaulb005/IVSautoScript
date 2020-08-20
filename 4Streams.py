import restful
import json
import boto3
import sys
import smtplib, ssl
import time
client = boto3.client('ivs')
def main(pc_access_key, pc_secret_key,type_stream):
    client = boto3.client('ivs', aws_access_key_id=pc_access_key,aws_secret_access_key = pc_secret_key)
    if command.lower() == 'start':
        start(pc_access_key, pc_secret_key, type_stream,  '10.0.0.197')
        start(pc_access_key, pc_secret_key, type_stream,  '10.0.0.196')
        start(pc_access_key, pc_secret_key, type_stream,  '10.0.0.195')
        start(pc_access_key, pc_secret_key, type_stream, '10.0.0.194')




    elif command.lower() == 'create':
        encoder_data = restful.get_encoders('10.0.0.197')
        status_data = encoder_data['vid_encoders']
        active_data = json.dumps(status_data[0]["status"])
        create(pc_access_key, pc_secret_key, type_stream,  '10.0.0.197')
        create(pc_access_key, pc_secret_key, type_stream,   '10.0.0.196')
        create(pc_access_key, pc_secret_key, type_stream,   '10.0.0.195')
        create(pc_access_key, pc_secret_key, type_stream,  '10.0.0.194')


def create(pc_access_key, pc_secret_key, type_stream,ip_encode):
    systemProp = restful.get_system_properties(ip_encode)
    name = systemProp['device_name']
    name_stream = name
    response = client.create_channel(
        name=name_stream,
        type=type_stream,
        latencyMode='LOW',
        tags={'string': 'string' })
    playback = response['channel']['playbackUrl']
    ingest = response['channel']['ingestEndpoint']
    arn_key = response['streamKey']['arn']
    responseStreamkey = client.get_stream_key(arn=arn_key)
    streamKey = responseStreamkey['streamKey']['value']
    streamUrl = '{"url":"' + 'rtmps://' + ingest + '/app/' + streamKey + '"}'
    data_json = restful.get_out_streams_configs(ip_encode ,out_stream_id=19)
    turnOn = data_json['enable']
    data_json['enable'] = True
    data_json['output_type']['rtmp']['service']['data'] = streamUrl
    data_out = data_json['output_type']['rtmp']['service']['data']
    parsed_data = json.loads(data_out)
    rtmp_loader = parsed_data['url']
    restful.put_out_streams_configs(ip_encode, '19' , data_json )


def start(pc_access_key, pc_secret_key,type_stream,name_stream, ip_encode):
    client = boto3.client('ivs', aws_access_key_id=pc_access_key, aws_secret_access_key=pc_secret_key)
    channel_all = client.list_channels(
        filterByName=name_stream,
        maxResults=50)
    channel_list = channel_all['channels']
    readable_channel = json.dumps(channel_list[0]["arn"])
    channel_info = client.get_channel(
        arn=readable_channel[1:-1])
    ingest_server = channel_info['channel']['ingestEndpoint']
    streamKeyAll = client.list_stream_keys(
        channelArn=readable_channel[1:-1], )
    streamKeyArn = streamKeyAll['streamKeys']
    stream_arn = json.dumps(streamKeyArn[0]["arn"])
    stream_arn = stream_arn[1:-1]
    streamKeyData = client.get_stream_key(
        arn=stream_arn)
    stream_key = streamKeyData['streamKey']['value']
    data_json = restful.get_out_streams_configs(ip_encode, out_stream_id=19)
    turnOn = data_json['enable']
    data_json['enable'] = True
    streamURL = '{"url":"' + 'rtmps://' + ingest_server + '/app/' + stream_key + '"}'
    data_json['output_type']['rtmp']['service']['data'] = streamURL
    data_out = data_json['output_type']['rtmp']['service']['data']
    parsed_data = json.loads(data_out)
    streamURL = parsed_data['url']
    restful.put_out_streams_configs(ip_encode, '19', data_json)
    print('Stream Started')







if __name__ == "__main__":
    if len(sys.argv) <4:
        print("%s:  Error: %s\n" % (sys.argv[0], "Not enough command options given"))
        print("Argument 1 (required): AWS Access Key (e.g. ABCDE1FGHIJKL2MNOPQR)")
        print("Argument 2 (required): AWS Secret Access Key (e.g. aBCdE1fGHijKlMn+OPq2RsTUV3wxy45Zab6c+7D8)")
        print("Argument 3 (required): Type of Stream (e.g. BASIC or STANDARD, defaults to basic if input is not BASIC or STANDARD)")
        print('Argument 4 (required) Command (e.g. Create , Start)')
        print(" ")
        sys.exit(3)
    else:
        pc_access_key = sys.argv[1]
        pc_secret_key = sys.argv[2]
        type_stream = sys.argv[3]
        command = sys.argv[4]

main(pc_access_key, pc_secret_key,type_stream)
