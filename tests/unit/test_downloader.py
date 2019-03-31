import pytest

from downloader.downloader import Downloader


@pytest.fixture()
def monkey_patched_downloader(mocker):
    dl = Downloader('foo', 'bar')
    dl._get_youtube_object = mocker.MagicMock()
    dl._get_audio_stream = mocker.MagicMock()
    dl._upload_to_s3 = mocker.MagicMock()
    dl._bucket = mocker.MagicMock()
    return dl


def test_should_download(monkey_patched_downloader):
    monkey_patched_downloader.run()

    monkey_patched_downloader._get_youtube_object.assert_called_once()
    monkey_patched_downloader._get_audio_stream.assert_called_once()
    monkey_patched_downloader._upload_to_s3.assert_called_once()
