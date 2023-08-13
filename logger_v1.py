import logging

logging.basicConfig(
    format='%(name)s - %(levelname)s - %(message)s',level=logging.INFO
)
logger = logging.getLogger("RecycleTracker")
logger.setLevel(logging.DEBUG)