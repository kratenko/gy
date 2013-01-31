import logging
log = None

def includeme(config):
    global log
    log = logging.getLogger(__name__)
    log.info('including package')

