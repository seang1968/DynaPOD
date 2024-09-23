from xml_consumer import XMLConsumer
import logging
import sys

def main(config_file):
    # Create an XML consumer to load resources and process actions
    xml_consumer = XMLConsumer(config_file)
    xml_consumer.parse_and_process()

    # Get the logger from the ResourceManager
    logger = xml_consumer.resource_manager.get_resource("LogFile")

    # Demonstrate logging at different levels
    logger.debug("This is a DEBUG message, it will be logged to the file.")
    logger.info("This is an INFO message, it will be logged to both file and console.")
    logger.warning("This is a WARNING message.")
    logger.error("This is an ERROR message.")
    logger.critical("This is a CRITICAL message.")

    # Create enough logs to trigger a log file rollover
    logger.info("Generating a large number of logs to trigger rollover...")
    for i in range(10):
        logger.debug(f"Debug log entry {i}")

    logger.info("Completed log generation. Check the log files for rotation.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <config.xml>")
    else:
        main(sys.argv[1])
