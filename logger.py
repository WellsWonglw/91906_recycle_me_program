import logging

# Configure the logging format and level
logging.basicConfig(
    format='%(name)s - %(levelname)s - %(message)s',level=logging.INFO
)
# Create a logger instance named "RecycleME"
logger = logging.getLogger("RecycleME")
# Set the logging level to DEBUG
logger.setLevel(logging.DEBUG)