import os
from lib.settings_helpers import make_settings, main

app_name = os.path.basename(os.path.dirname(__file__))

environment_settings = {
    'dev': {
        'DB_USER': 'error_scarer',
        'DB_PASS': 'error_scarer',
        'DB_NAME': 'error_scarer',
        'DB_HOST': 'localhost',
        'NSQ_CMS_EVENTS_TOPIC': 'basura#ephemeral',
        'NSQ_CMS_EVENTS_CHANNEL': 'error_scarer#ephemeral',
    },
    'stage': {

    },
    'live': {

    }
}

default_settings = {}
get, env = make_settings(app_name, default_settings, environment_settings)

if __name__ == '__main__':
    main(get)
