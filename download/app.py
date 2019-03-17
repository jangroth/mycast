import boto3
import validators
import pytube

# Global variables are reused across execution contexts (if available)
from pytube import YouTube

session = boto3.Session()


def _create_response(status_code, text):
    return {
        "statusCode": status_code,
        "body": text
    }


def lambda_handler(event, context):
    try:
        url = event['body']['url']
    except (KeyError, TypeError):
        return _create_response(400, '"url" is required in request body.')
    if not validators.url(url):
        return _create_response(400, 'Invalid "url" in request body.')
    yt = YouTube(url)
    print(yt.streams.filter(only_audio=True).all())
    return _create_response(200, 'Ok')
