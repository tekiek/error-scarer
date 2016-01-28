import os
from lib.settings_helpers import make_settings, main

app_name = os.path.basename(os.path.dirname(__file__))

environment_settings = {
    'dev': {
        'REDIS_HOST': 'localhost',
        'REDIS_PORT': 6379,
        'NSQ_CMS_EVENTS_TOPIC': 'hive_artifact_events',
        'NSQ_CMS_EVENTS_CHANNEL': 'qr_cms_events_to_pensieve#ephemeral',
        'TAG_ENDPOINT': "https://pensieve-dev.buzzfeed.com/artifacts/tags/",
        'HIVE_API_URL': 'https://hive-api-stage.buzzfeed.com'
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
