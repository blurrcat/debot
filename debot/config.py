DEBUG = False
DEBOT_MOTO = u'A very helpful bot. "I know, it\'s 42."'
DEBOT_ADMINS = (u'blurrcat', u'sha')
SLACK_USERNAME = u'debot'
SLACK_ICON = u':poop:'
REQUIRED_CONFIG = (u'SLACK_TOKEN',)
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
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': True
        }
    }
}
