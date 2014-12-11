DEBUG = False
MOTO = u'A very helpful bot. "I know, it\'s 42."'
ADMINS = (u'blurrcat', u'sha')
SLACK_USERNAME = u'debot'
SLACK_ICON = u':poop:'
SLACK_TOKEN = u'slack_token'
EXTRA_PLUGINS_GIT = ''
EXTRA_PLUGINS_GIT_DIR = ''
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'DEBUG' if DEBUG else 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': True
        }
    }
}
