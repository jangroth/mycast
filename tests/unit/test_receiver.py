import pytest

from receiver import app


@pytest.fixture()
def event_template():
    """ Generates API GW Event"""

    return {
        "body": {"test": "body"},
        "resource": "/{proxy+}",
        "requestContext": {
            "resourceId": "123456",
            "apiId": "1234567890",
            "resourcePath": "/{proxy+}",
            "httpMethod": "POST",
            "requestId": "c6af9ac6-7b61-11e6-9a41-93e8deadbeef",
            "accountId": "123456789012",
            "identity": {
                "apiKey": "",
                "userArn": "",
                "cognitoAuthenticationType": "",
                "caller": "",
                "userAgent": "Custom User Agent String",
                "user": "",
                "cognitoIdentityPoolId": "",
                "cognitoIdentityId": "",
                "cognitoAuthenticationProvider": "",
                "sourceIp": "127.0.0.1",
                "accountId": ""
            },
            "stage": "prod"
        },
        "queryStringParameters": {
            "foo": "bar"
        },
        "headers": {
            "Via":
                "1.1 08f323deadbeefa7af34d5feb414ce27.cloudfront.net (CloudFront)",
            "Accept-Language":
                "en-US,en;q=0.8",
            "CloudFront-Is-Desktop-Viewer":
                "true",
            "CloudFront-Is-SmartTV-Viewer":
                "false",
            "CloudFront-Is-Mobile-Viewer":
                "false",
            "X-Forwarded-For":
                "127.0.0.1, 127.0.0.2",
            "CloudFront-Viewer-Country":
                "US",
            "Accept":
                "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Upgrade-Insecure-Requests":
                "1",
            "X-Forwarded-Port":
                "443",
            "Host":
                "1234567890.execute-api.us-east-1.amazonaws.com",
            "X-Forwarded-Proto":
                "https",
            "X-Amz-Cf-Id":
                "aaaaaaaaaae3VYQb9jd-nvCd-de396Uhbp027Y2JvkCPNLmGJHqlaA==",
            "CloudFront-Is-Tablet-Viewer":
                "false",
            "Cache-Control":
                "max-age=0",
            "User-Agent":
                "Custom User Agent String",
            "CloudFront-Forwarded-Proto":
                "https",
            "Accept-Encoding":
                "gzip, deflate, sdch"
        },
        "pathParameters": {
            "proxy": "/examplepath"
        },
        "httpMethod": "POST",
        "stageVariables": {
            "baz": "qux"
        },
        "path": "/examplepath"
    }


@pytest.fixture()
def event_empty():
    return {}


@pytest.fixture()
def event_invalid_url(event_template):
    event_template.update({
        "body": {"url": "haus"}
    })
    return event_template


@pytest.fixture()
def event_valid_url(event_template):
    event_template.update({
        "body": {"url": "https://www.youtube.com/watch?v=9bZkp7q19f0"}
    })
    return event_template


def test_should_return_200_on_valid_request(event_valid_url):
    ret = app.lambda_handler(event_valid_url, "")
    assert ret['statusCode'] == 200


def test_should_return_400_on_empty_request(event_empty):
    ret = app.lambda_handler(event_empty, "")
    assert ret['statusCode'] == 400


def test_should_return_400_if_no_url_in_body(event_template):
    ret = app.lambda_handler(event_template, "")
    assert ret['statusCode'] == 400


def test_should_return_400_if_invalid_url_in_body(event_invalid_url):
    ret = app.lambda_handler(event_invalid_url, "")
    assert ret['statusCode'] == 400
