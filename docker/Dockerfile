FROM python:3.7-alpine

ADD ./downloader.py /
RUN pip install pytube boto3

CMD [ "python", "./downloader.py" ]