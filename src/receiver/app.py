import logging
import tempfile

import validators
from pytube import YouTube

# Global variables are reused across execution contexts (if available)

logging.basicConfig(
    format='%(asctime)s %(name)-25s %(levelname)-8s %(message)s',
    level=logging.INFO)
logging.getLogger('boto3').setLevel(logging.ERROR)
logging.getLogger('botocore').setLevel(logging.ERROR)
LOG = logging.getLogger()


class YoutubeToS3:
    def __init__(self, url, bucket_name):
        self.url = url
        self.bucket_name = bucket_name
        self.base_dir = tempfile.mkdtemp()

    def run(self):
        streams = YouTube(self.url).streams
        streams.filter(only_audio=True)
        pass


class ProcessingError(Exception):
    def __init__(self, http_return_code, message):
        self.http_return_code = http_return_code
        self.message = message


def _get_url(event):
    try:
        url = event['body']['url']
    except (KeyError, TypeError):
        raise ProcessingError(400, '"url" is required in request body.')
    if not validators.url(url):
        raise ProcessingError(400, 'Invalid "url" in request body.')
    return url


def _create_response(status_code, text):
    return {
        "statusCode": status_code,
        "body": text
    }


def _get_bucket_name():
    return 'TODO'


def lambda_handler(event, context):
    LOG.info('Entering handler')
    try:
        url = _get_url(event)
        bucket_name = _get_bucket_name()
    except ProcessingError as p:
        LOG.warning('Exiting with status {} - {}'.format(p.http_return_code, p.message))
        return _create_response(p.http_return_code, p.message)

    YoutubeToS3(url=url, bucket_name=bucket_name).run()
    # yt = YouTube(url)
    # print(yt.streams.filter(only_audio=True).all())
    return _create_response(200, 'ok')
