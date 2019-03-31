import logging
import os

import boto3
from pytube import YouTube

logging.basicConfig(
    format='%(asctime)s %(name)-25s %(levelname)-8s %(message)s',
    level=logging.INFO)
log = logging.getLogger()
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
        youtube = YouTube(self.url)
        youtube.register_on_progress_callback(self._on_progress)
        return youtube

    def _get_audio_stream(self, youtube):
        stream = youtube.streams.filter(only_audio=True, mime_type="audio/mp4").order_by('abr').desc().first()
        self._total_size = stream.filesize
        return stream

    def _on_progress(self, stream, chunk, file_handle, bytes_remaining):
        percent_done = 100 - round(bytes_remaining / self._total_size * 100)
        if abs(percent_done - self._progress_percent) > 10:
            log.info('{}% done...'.format(percent_done))
            self._progress_percent = percent_done

    def _upload_to_s3(self, file_name):
        log.info('Uploading "{}" into bucket "{}"'.format(file_name, self.bucket_name))
        self._bucket.upload_file(file_name, 'streams/{}'.format(file_name))

    def _download_audio(self):
        log.info('Requesting download from {}...'.format(self.url))
        youtube = self._get_youtube_object()
        stream = self._get_audio_stream(youtube)
        log.info('Starting download of "{}"...'.format(youtube.title))
        downloaded_file = stream.download()
        log.info('Starting upload into bucket "{}"'.format(self.bucket_name))
        self._upload_to_s3(downloaded_file)
        log.info('Done')

    def run(self):
        self._download_audio()


if __name__ == '__main__':
    url = os.getenv('URL', 'https://www.youtube.com/watch?v=4bJ0dvAl98k')
    bucket_name = os.getenv('BUCKET_NAME', 'mycast-streams')
    Downloader(url=url, bucket_name=bucket_name).run()
