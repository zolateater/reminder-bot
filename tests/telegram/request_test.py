from src.telegram.request import RequestBuilder

# RequestBuilder tests #
def test_request_builder():
    rq = RequestBuilder("TestToken")
    request = rq.build("testMethod", RequestBuilder.HTTP_GET, {})
    assert request.uri == "https://api.telegram.org/botTestToken/testMethod"
