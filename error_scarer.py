#!/usr/bin/env python
import logging
import os

import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpserver

import app.ping
import app.views

import settings  # noqa (imported for side effects)


APP_ROOT = os.path.abspath(os.path.dirname(__file__))


class Application(tornado.web.Application):

    def __init__(self):
        debug = tornado.options.options.environment == 'dev'
        if debug:
            logging.getLogger().setLevel(logging.DEBUG)
            logging.debug('debug logging enabled')

        app_settings = {
            'debug': debug,
        }

        handlers = [
            (r'^/ping$', app.ping.PingHandler),

            (r'^/users/([0-9]*)/logs$', app.views.UserLogHandler),
            (r'^/logs$', app.views.LogHandler),
        ]

        super(Application, self).__init__(handlers, **app_settings)


if __name__ == '__main__':
    tornado.options.define('port', help='listen on port', type=int)
    tornado.options.parse_command_line()
    assert tornado.options.options.port, '--port is required'

    name = os.path.basename(APP_ROOT)
    port = tornado.options.options.port
    address = '0.0.0.0'
    logging.info('starting %s on %s:%d', name, address, port)

    http_server = tornado.httpserver.HTTPServer(
        request_callback=Application(), xheaders=True)
    http_server.listen(port, address=address)

    tornado.ioloop.IOLoop.instance().start()
