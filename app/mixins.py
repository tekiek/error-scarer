from statsd import StatsClient
import tornado

import settings

statsd = StatsClient(prefix='error_scarer_api')


class QueryArgumentsMixin(object):
    def get_int_query_argument(self, name, default=1, min_value=1, max_value=None):
        '''Get a querystring argument under the given name, parse it to an integer
        and validate it is at least and/or at most some value.'''
        error_msg = 'INVALID_{}'.format(name.upper())
        arg = self.get_query_argument(name, default=default)
        if not isinstance(arg, int) and not arg.isdigit():
            raise tornado.web.HTTPError(400, error_msg)
        arg = int(arg)
        if min_value is not None and arg < min_value:
            raise tornado.web.HTTPError(400, error_msg)
        if max_value is not None and arg > max_value:
            raise tornado.web.HTTPError(400, error_msg)
        return arg
