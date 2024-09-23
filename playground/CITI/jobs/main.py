from xml_consumer import XMLConsumer

def main(config_file):
    xml_consumer = XMLConsumer(config_file)
    xml_consumer.parse_and_process()
    pass

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python main.py <config.xml>")
    else:
        main(sys.argv[1])