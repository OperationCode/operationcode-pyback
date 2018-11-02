import logging

from gunicorn import glogging


class HealthCheckFilter(logging.Filter):
    def filter(self, record):
        return 'ELB-HealthChecker' not in record.getMessage()


class CustomGunicornLogger(glogging.Logger):
    def setup(self, cfg):
        super().setup(cfg)

        logger = logging.getLogger('gunicorn.access')
        logger.addFilter(HealthCheckFilter())
