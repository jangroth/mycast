import logging
import os

import boto3
from pytube import YouTube

root = logging.getLogger()
logging.basicConfig(
    format='%(asctime)s %(name)-25s %(levelname)-8s %(message)s',
    level=logging.INFO)
logger = logging.getLogger()
logging.getLogger('boto3').setLevel(logging.ERROR)
logging.getLogger('botocore').setLevel(logging.ERROR)

boto3.setup_default_session(profile_name='jan')


class Downloader:
    def __init__(self, url, bucket_name):
        self.url = url
        self.bucket_name = bucket_name
        self._total_size = 0
        self._progress_percent = 0
        self._bucket = boto3.resource('s3').Bucket(bucket_name)

    def _get_youtube_object(self):
        return YouTube(self.url)

    def _on_progress(self, stream, chunk, file_handle, bytes_remaining):
        percent_done = 100 - round(bytes_remaining / self._total_size * 100)
        if abs(percent_done - self._progress_percent) > 10:
            logging.info('{}% done...'.format(percent_done))
            self._progress_percent = percent_done

    def _upload_to_s3(self, stream, file_handle):
        logger.info('Download complete.')
        file_name = os.path.basename(file_handle.name).replace(' ', '')
        logger.info('Uploading "{}" into bucket "{}"'.format(file_name, self.bucket_name))
        self._bucket.upload_file(file_handle.name, 'streams/{}'.format(file_name))

    def _download_audio(self):
        logging.info('Requesting download from {}...'.format(self.url))
        youtube = YouTube(self.url)
        youtube.register_on_progress_callback(self._on_progress)
        youtube.register_on_complete_callback(self._upload_to_s3)
        stream = youtube \
            .streams \
            .filter(only_audio=True, mime_type="audio/mp4") \
            .order_by('abr') \
            .desc() \
            .first()
        self._total_size = stream.filesize
        logging.info('Starting download "{}"...'.format(youtube.title))
        stream.download()

    def run(self):
        self._download_audio()


if __name__ == '__main__':
    url = os.getenv('URL', 'https://www.youtube.com/watch?v=4bJ0dvAl98k')
    bucket_name = os.getenv('BUCKET_NAME', 'mycast-streams')
    Downloader(url=url, bucket_name=bucket_name).run()
