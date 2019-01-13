import stomp
import json
import logging
import os

mqhost = os.environ['MQHOST']
mqport = os.environ['MQPORT']
mq_user = os.environ['MQUSER']
mq_passwd = os.environ['MQPASS']
conn: stomp.Connection = None
logger: logging.Logger = None


def init_logger():
    global logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)


def connect_mq():
    global conn
    conn = stomp.Connection([(mqhost, mqport)], use_ssl=True)
    conn.start()
    conn.connect(mq_user, mq_passwd, wait=True)
    # conn.set_listener('', MyListener())


def extract_emails(event):
    mails = list()
    for record in event.get('Records'):
        rcvd_email = record.get('ses').get('mail')
        headers = rcvd_email.get('commonHeaders')
        mail_msg = dict()
        mail_msg.update(date=headers.get('date'), from_addr=headers.get('from'), subject=headers.get('subject'))
        mail_msg.update(to=headers.get('to'))
        mails.append(mail_msg)
    return mails


def handle_mail(event, context):
    global conn
    if not logger:
        init_logger()
    try:
        logger.info(f'Function {context.fuction_name} with id {context.aws_request_id} is invoked.')
        if not conn:
            connect_mq()
        mails = extract_emails(event)
        conn.send(body=json.dumps(mails), destination='/queue/mails', content_type='application/json')
    except Exception as ex:
        logger.error(f'Something went wrong: {str(ex)}')

