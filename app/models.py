from settings import get
import MySQLdb


class Transaction(object):

    def __init__(self, model):
        self.connection = model.connection

    def __enter__(self):
        self.connection.autocommit(False)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None and exc_val is None and exc_tb is None:
            self.connection.commit()
        else:
            self.connection.rollback()
        self.connection.autocommit(True)


class ClosingCursor(object):

    def __init__(self, connection):
        self.cursor = connection.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.cursor.close()
        except:
            pass


class Model(object):
    FIELDS = {}
    connection = MySQLdb.connect(host=get('DB_HOST'), user=get('DB_USER'),
                                 passwd=get('DB_PASS'), db=get('DB_NAME'))

    def __init__(self, *args, **kwargs):
        for field, spec in self.FIELDS.items():
            value = kwargs.get(field)
            if value is None and not spec['null']:
                raise ValueError("{} is a required field.".format(field))
            setattr(self, field, spec['type'](value))


class User(Model):
    FIELDS = {
        'id': {'type': int, 'null': False}
    }

    def save(self):
        cursor = self.connection.cursor()
        query = "INSERT IGNORE INTO error_scarer_user (id) VALUES ({});".format(self.id)
        cursor.execute(query)


class Log(Model):
    FIELDS = {
        'level': {'type': str, 'null': True},
        'os': {'type': str, 'null': True},
        'message': {'type': str, 'null': True},
        'created_at': {'type': int, 'null': True},
        'device': {'type': str, 'null': True},
        'app_version': {'type': str, 'null': True},
        'page': {'type': str, 'null': True},
        'page_type': {'type': str, 'null': True},
        'buzz_id': {'type': int, 'null': True},
        'buzz': {'type': str, 'null': True},
        'stack': {'type': str, 'null': True}
    }

    def to_json(self):
        return {field: getattr(self, field) for field in self.FIELDS}

    def save(self):
        with ClosingCursor(self.connection) as closing:
            names = []
            values = []
            for field, spec in self.FIELDS.items():
                value = spec['type'](getattr(self, field))
                if value is None:
                    continue
                names.append(str(field))
                if isinstance(value, (str, unicode)):
                    value = '"{}"'.format(value)
                values.append(str(value))
            query = """INSERT INTO error_scarer_log ({}) VALUES ({});""".format(", ".join(names), ", ".join(values))
            closing.cursor.execute(query)
            self.id = closing.cursor.lastrowid

    @classmethod
    def find(cls, user_id=None, buzz_id=None, since=None, until=None):
        if user_id is not None:
            sql = "SELECT {} FROM error_scarer_log LEFT JOIN error_scarer_userlog ON error_scarer_log.id = error_scarer_userlog.log_id LEFT JOIN error_scarer_user ON error_scarer_user.id = error_scarer_userlog.user_id WHERE {}"
        else:
            sql = "SELECT {} FROM error_scarer_log WHERE {}"

        wheres = []

        if since is not None:
            wheres.append("created_at > {}".format(int(since)))
        if until is not None:
            wheres.append("created_at < {}".format(int(until)))
        if buzz_id is not None:
            wheres.append("buzz_id = {}".format(int(buzz_id)))
        if user_id is not None:
            wheres.append("user_id = {}".format(int(user_id)))

        where_clause = " AND ".join(wheres) + ";"

        fields = Log.FIELDS.keys()
        sql = sql.format(", ".join(fields), where_clause)

        with ClosingCursor(Log.connection) as closing:
            closing.cursor.execute(sql)
            for row in closing.cursor.fetchall():
                yield Log(**{field: value for field, value in zip(fields, row)})


class UserLog(Model):
    FIELDS = {
        'user_id': {'type': int, 'null': False},
        'log_id': {'type': int, 'null': False}
    }

    def save(self):
        with ClosingCursor(self.connection) as closing:
            query ="INSERT INTO error_scarer_userlog (user_id, log_id) VALUES ({}, {})", (self.user_id, self.log_id)
            closing.cursor.execute("INSERT INTO error_scarer_userlog (user_id, log_id) VALUES ({}, {});".format(self.user_id, self.log_id))
            self.id = closing.cursor.lastrowid
