import os


class Downloader:
    def __init__(self, url, bucket_name):
        self.url = url
        self.bucket_name = bucket_name

    def run(self):
        print('Hello world - {} {}'.format(self.url, self.bucket_name))


if __name__ == '__main__':
    url = os.getenv('URL')
    bucket_name = os.getenv('BUCKET_NAME')
    Downloader(url=url, bucket_name=bucket_name).run()
