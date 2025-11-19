import sys, logging
sys.path.insert(0, r'c:\GitHub\Interzen\Interzen.POC\ZenIA\src')
from core.config import config
config.setup_logging()
logger = logging.getLogger('mcp_server.server')
logger.debug('DEBUG TEST - should appear if LOG_LEVEL=DEBUG')
logger.info('INFO TEST - should always appear')
print('CURRENT LOG LEVEL:', logging.getLevelName(logger.getEffectiveLevel()))
