import restful
import json
import boto3
import sys
import smtplib, ssl
import time
def email(old_status, active_data,ip_encode,passwordGmail):
    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    sender_email = ""
    receiver_email = ""
    password = passwordGmail
    message = """\
    Subject: Stream has changed status's

    Your stream with the ip of """ + ip_encode + """ has changed from """ + old_status + ''' to ''' + active_data

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

old_status = '"STARTING"'
def main(old_status,ip_encode,passwordGmail):
    while True:
        encoder_data = restful.get_encoders(ip_encode)
        status_data = encoder_data['vid_encoders']
        active_data = json.dumps(status_data[0]["status"])
        print(active_data)
        if active_data != old_status:
            email(old_status, active_data,ip_encode,passwordGmail)
            old_status = active_data
        time.sleep(10)
if __name__ == "__main__":
    if len(sys.argv) <2:
        print("%s:  Error: %s\n" % (sys.argv[0], "Not enough command options given"))
        print("Argument 1 (required): IP of stream")
        print('Argument 2 (required): Password of gmail account')
    else:
        ip_encode = sys.argv[1]
        passwordGmail = sys.argv[2]
main('"STARTING"', ip_encode,passwordGmail)
