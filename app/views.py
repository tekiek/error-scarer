import time
import logging

import tornado
from base import BaseHandler
from mixins import QueryArgumentsMixin

import app.models


logger = logging.getLogger(__name__)


class AppHandler(BaseHandler, QueryArgumentsMixin):

    @tornado.gen.coroutine
    def get(self, artifact_id):
        self.api_response({'endpoint': 'base/'})


class LogHandler(AppHandler):

    @tornado.gen.coroutine
    def get(self):
        """
        :param int since: The unix timestamp for the starting time from which to search for errors.
        :param int until: The unix timestamp for the ending time from which to search for errors.
        :returns: Logs between the times specified.
        """
        since = self.get_argument('since', default=time.time() - 24 * 60 * 60)
        until = self.get_argument('until', default=time.time())
        buzz_id = self.get_argument('buzz_id', default=None)
        user_id = self.get_argument('user_id', default=None)
        message = self.get_argument('message', default=None)

        logs = app.models.Log.find(since=since, until=until,
                                   buzz_id=buzz_id, user_id=user_id)

        if message is not None:
            self.api_response({"logs": [log.to_json() for log in logs if message in log.message]})
        else:
            self.api_response({"logs": [log.to_json() for log in logs]})


    @tornado.gen.coroutine
    def post(self):
        try:
            app_version = self.get_argument('app_version', default=None)
            buzz = self.get_argument('buzz', default=None)
            buzz_id = self.get_argument('buzz_id', default=None)
            created_at = self.get_argument('date_happened', default=None)
            device = self.get_argument('device', default=None)
            message = self.get_argument('message', default=None)
            os = self.get_argument('os', default=None)
            page = self.get_argument('page', default=None)
            level = self.get_argument('type', default=None)
            user_id = self.get_argument('user_id', default=None)

            with app.models.Transaction(app.models.User):
                user = app.models.User(id=user_id)
                log = app.models.Log(level=level, os=os, message=message,
                                     created_at=created_at, device=device,
                                     app_version=app_version, page=page,
                                     page_type=page, buzz_id=buzz_id,
                                     buzz=buzz)

                user.save()
                log.save()

                userlog = app.models.UserLog(user_id=user.id, log_id=log.id)
                userlog.save()

                self.api_response({'status': 'OK', 'user_id': user.id, 'log_id': log.id, 'userlog_id': userlog.id})
        except Exception, e:
            logger.exception(e)
            self.api_response({'status': 'ERROR',
                               'message': str(e)})



class UserLogHandler(AppHandler):

    @tornado.gen.coroutine
    def get(self, artifact_id):
        """
        :param int user_id: The id for the user who is logging.
        :returns: Logs associated with the user account.
        """
        self.api_response({'endpoint': 'users/{id}/logs'})
