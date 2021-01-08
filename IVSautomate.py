import restful
import json
import boto3
import sys
client = boto3.client('ivs')
def main(pc_access_key, pc_secret_key, type_stream,name_stream,command):
    client = boto3.client('ivs', aws_access_key_id=pc_access_key,
    aws_secret_access_key=pc_secret_key)
    if type_stream == 'STANDARD':
        type_stream = 'STANDARD'
    else:
        type_stream = 'BASIC'
    channel_all = client.list_channels(
        filterByName = name_stream,
        maxResults=50)
    channel_list = channel_all['channels']
    if command.lower() == 'stop'  or command.lower() == 'create'   or command.lower() == 'start'  or command.lower() == 'delete':
        try:
            name_of_channel = json.dumps(channel_list[0]["name"])
            if name_of_channel != '':
                readable_channel = json.dumps(channel_list[0]["arn"])
                if command.lower() == 'delete':
                    response = client.delete_channel(
                        arn=readable_channel[1:-1])
                    print('Channel Deleted')
                    exit()
                if command.lower() == 'stop':
                    data_json = restful.get_out_streams_configs("10.0.0.169", out_stream_id=47)
                    turnOff = data_json['enable']
                    data_json['enable'] = False
                    restful.put_out_streams_configs('10.0.0.169', '47', data_json)
                    print('Stream Stopped')

                    exit()
                if command.lower() == 'start':
                    channel_info = client.get_channel(
                        arn=readable_channel[1:-1])
                    #print(channel_info)
                    ingest_server = channel_info['channel']['ingestEndpoint']
                    #print(ingest_server)
                    streamKeyAll = client.list_stream_keys(
                        channelArn=readable_channel[1:-1],)
                    streamKeyArn = streamKeyAll['streamKeys']
                    #print(streamKeyAll)
                    stream_arn = json.dumps(streamKeyArn[0]["arn"])
                    stream_arn = stream_arn[1:-1]
                    streamKeyData = client.get_stream_key(
                        arn=stream_arn)
                    stream_key = streamKeyData['streamKey']['value']
                    data_json = restful.get_out_streams_configs('ENCODER_IP_HERE', out_stream_id=47)
                    turnOn = data_json['enable']
                    data_json['enable'] = True
                    streamURL = '{"url":"' + 'rtmps://' + ingest_server + '/app/' + stream_key + '"}'
                    data_json['output_type']['rtmp']['service']['data'] = streamURL
                    data_out = data_json['output_type']['rtmp']['service']['data']
                    parsed_data = json.loads(data_out)
                    streamURL = parsed_data['url']
                    restful.put_out_streams_configs('ENCODER_IP_HERE', '47' , data_json )
                if command.lower() == 'create':
                    create(pc_access_key, pc_secret_key, type_stream, name_stream, command)
                    print('Channel Created')
        except IndexError:
            print('Creating channel')
            create(pc_access_key, pc_secret_key, type_stream,name_stream,command)
    else:
        print('Invalid Command')
def create(pc_access_key, pc_secret_key, type_stream,name_stream,command):
    response = client.create_channel(
        name=name_stream,
        type=type_stream,
        latencyMode='NORMAL',
        tags={'string': 'string' })
    playback = response['channel']['playbackUrl']
    ingest = response['channel']['ingestEndpoint']
    arn_key = response['streamKey']['arn']
    responseStreamkey = client.get_stream_key(arn=arn_key)
    streamKey = responseStreamkey['streamKey']['value']
    streamUrl = '{"url":"' + 'rtmps://' + ingest + '/app/' + streamKey + '"}'
    data_json = restful.get_out_streams_configs("ENCODER_IP_HERE" ,out_stream_id=47)
    turnOn = data_json['enable']
    data_json['enable'] = True
    data_json['output_type']['rtmp']['service']['data'] = streamUrl
    data_out = data_json['output_type']['rtmp']['service']['data']
    parsed_data = json.loads(data_out)
    rtmp_loader = parsed_data['url']
    restful.put_out_streams_configs('ENCODER_IP_HERE', '47' , data_json )

if __name__ == "__main__":
    if len(sys.argv) <5:
        print("%s:  Error: %s\n" % (sys.argv[0], "Not enough command options given"))
        print("Argument 1 (required): AWS Access Key (e.g. ABCDE1FGHIJKL2MNOPQR)")
        print("Argument 2 (required): AWS Secret Access Key (e.g. aBCdE1fGHijKlMn+OPq2RsTUV3wxy45Zab6c+7D8)")
        print("Argument 3 (required): Type of Stream (e.g. BASIC or STANDARD, defaults to basic if input is not BASIC or STANDARD)")
        print("Argument 4 (required): Name of Stream (e.g. Name can be anything if name does not exist stream will create automatically)")
        print("Argument 5 (required): Command (e.g. Delete,Stop,Start,Create)")
        print(" ")
        sys.exit(3)
    else:
        pc_access_key = sys.argv[1]
        pc_secret_key = sys.argv[2]
        type_stream = sys.argv[3]
        name_stream = sys.argv[4]
        command = sys.argv[5]

main(pc_access_key, pc_secret_key,type_stream,name_stream,command)
