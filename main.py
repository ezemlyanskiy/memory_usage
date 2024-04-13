import logging
import time
from logging.handlers import RotatingFileHandler

import psutil
import requests

ENDPOINT = 'https://example.com/'
RETRY_PERIOD = 60


def check_memory_usage(session):
    memory = psutil.virtual_memory()

    if memory.percent > 90:
        try:
            response = session.post(
                ENDPOINT, json={'message': 'High memory usage alarm!'}
            )
            response.raise_for_status()
            logging.info('Alarm was sent successfully')
        except requests.exceptions.HTTPError as errh:
            raise errh
        except requests.exceptions.ConnectionError as conerr:
            raise conerr
        except requests.exceptions.RequestException as errex:
            raise errex


def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format=(
            '[{asctime}] #{levelname:8} {filename} '
            '{lineno} - {name} - {message}'
        ),
        style='{',
        handlers=[
            RotatingFileHandler('main.log', maxBytes=50000000, backupCount=5),
        ],
    )


def main():
    setup_logging()
    logging.info('Started...')

    with requests.session() as session:
        while True:
            try:
                check_memory_usage(session)
            except KeyboardInterrupt:
                logging.info('Stopped...')
                return
            except Exception as error:
                logging.error(error)
            finally:
                time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    main()
