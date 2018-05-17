from comprasnet import SearchAuctions, ComprasNetApi
import logging.config
import sys
from datetime import date

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

sa = SearchAuctions(day=date(day=11, month=5, year=2018))
sa.search()

print(sa.total_pages)
print(sa.current_page)
for result in sa.results:
    print(result)
    print(sa.current_page)


# comprasnet_api = ComprasNetApi()
# print(comprasnet_api.get_licitacoes_uasgs())