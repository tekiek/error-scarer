import cgi
import json
import logging

import tornado.httpclient
import tornado.web


class BaseHandler(tornado.web.RequestHandler):
    http = tornado.httpclient.AsyncHTTPClient()
    http_sync = tornado.httpclient.HTTPClient()

    @property
    def client_ip(self):
        return self.request.headers.get('X-Forwarded-For') or self.request.remote_ip

    def write_error(self, status_code, **kwargs):
        try:
            err_cls, err, traceback = kwargs['exc_info']
        except KeyError:
            logging.error('NO_EXCEPTION_FOR_ERROR: %r %r', status_code, kwargs)
            return self.api_response('INTERNAL_ERROR', 500)

        if issubclass(err_cls, tornado.web.HTTPError):
            if err.log_message and err.log_message.startswith('Missing argument '):
                msg = 'MISSING_ARG_%s' % (err.log_message.split()[-1].upper())
                return self.api_response(msg, code=err.status_code)
            msg = err.log_message or 'INTERNAL_ERROR'
            return self.api_response(msg, err.status_code)

        # Tornado itself logs unhandled exceptions w/ traceback, so we don't
        # need to do any extra logging in this case.
        return self.api_response('INTERNAL_ERROR', 500)

    def api_response(self, data, code=200):
        self.set_status(code)
        self.set_header('Content-Type', 'application/json')
        if not 200 <= code < 300:
            data = {'message': data}
        if not isinstance(data, basestring):
            data = json.dumps(data)
        self.finish(data)

    @property
    def json_body(self):
        if not hasattr(self, '_json_body'):
            content_type, _ = cgi.parse_header(self.request.headers['Content-Type'])
            if content_type != 'application/json':
                raise tornado.web.HTTPError(400, 'INVALID_CONTENT_TYPE')

            try:
                input_data = json.loads(self.request.body)
            except ValueError:
                input_data = None

            if not isinstance(input_data, dict):
                logging.error('invalid JSON: %r', self.request.body)
                raise tornado.web.HTTPError(400, 'INVALID_JSON')

            self._json_body = input_data
        return self._json_body


class MissingHandler(BaseHandler):
    def handle_request(self):
        raise tornado.web.HTTPError(404, 'NOT_FOUND')

    get = post = put = delete = head = options = handle_request
