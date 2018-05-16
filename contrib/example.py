from comprasnet import ComprasNet
import logging
import sys
from datetime import datetime

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False
        },
    },
})

comprasnet = ComprasNet()
results = comprasnet.search_auctions_by_date(datetime.strptime(sys.argv[1], '%d/%m/%Y'))
print(results)
