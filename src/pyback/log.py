import logging


class HealthCheckFilter(logging.Filter):
    def filter(self, record):
        return 'ELB-HealthChecker/2.0' not in record
