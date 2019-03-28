import pytest

from downloader.downloader import Downloader
from receiver import app


@pytest.fixture()
def monkey_patched_downloader():
    def noop():
        print('noop invoked')

    dl = Downloader('foo', 'bar')
    dl._get_youtube_object = noop
    return dl


def test_should_download(monkey_patched_downloader):
    monkey_patched_downloader._get_youtube_object()
