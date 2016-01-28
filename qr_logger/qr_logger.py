import os
import nsq
import sys
import json
import urllib
import logging

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

import tornado
import tornado.httpclient

from settings import get

NSQ_CMS_EVENTS_TOPIC = get('NSQ_CMS_EVENTS_TOPIC')
NSQ_CMS_EVENTS_CHANNEL = get('NSQ_CMS_EVENTS_CHANNEL')
TAG_ENDPOINT = get('TAG_ENDPOINT')

"""
Static variables
"""
MESSAGE_TIMEOUT = 60

"""
Global Data Structures
"""
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
client = tornado.httpclient.AsyncHTTPClient(max_clients=20)


def get_handle_response(msg):
    def handle_response(resp):
        if resp.error:
            logger.error("API Error: {}".format(resp.error))
            msg.requeue()
        else:
            msg.finish()
    return handle_response


def handle_message(msg):
    data = json.loads(msg.body)
    if data['source'] != 'error-scarer':
        return True

    msg.enable_async()

    request = tornado.httpclient.HTTPRequest(
        url="/logs",
        method='POST',
        body=urllib.urlencode(msg.body),
        connect_timeout=5.,
        request_timeout=int(MESSAGE_TIMEOUT * 0.5)
    )

    client.fetch(request,
                 callback=get_handle_response(msg),
                 raise_error=True)


if __name__ == '__main__':
    tornado.options.define('lookupd_http_addresses', default='127.0.0.1:4161', multiple=True)
    tornado.options.parse_command_line()

    nsq.Reader(topic=NSQ_CMS_EVENTS_TOPIC,
               channel=NSQ_CMS_EVENTS_CHANNEL,
               lookupd_http_addresses=tornado.options.options.lookupd_http_addresses.split(','),
               message_handler=handle_message,
               max_in_flight=20,
               msg_timeout=MESSAGE_TIMEOUT)
    nsq.run()
