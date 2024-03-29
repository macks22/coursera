import oauth2 as oauth
import urllib2 as urllib


# See assignment1.html instructions or README for how to get these credentials
api_key = "oiMXDC9nmsIkKrzX7ldLb6L34"
api_secret = "zGNUERQ8tSKCuvWZdF0r51nSKRljbRLYRcGeKIUQWVijdgdMy4"
access_token_key = "2605830732-5vx8Hd48nAXtbNRa5QXmShKjP8Pr2N6WhVjlZZl"
access_token_secret = "swYp7w04hUSTftnEZhspxKgq1hZH07RMVzbkFBF5jHlOo"

_debug = 0

oauth_token    = oauth.Token(key=access_token_key, secret=access_token_secret)
oauth_consumer = oauth.Consumer(key=api_key, secret=api_secret)

signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

http_handler  = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)


def twitterreq(url, http_method='GET', parameters=None):
    """Construt, sign, and open a twitter request using the hard-coded
    credentials at the global scope.

    """
    req = oauth.Request.from_consumer_and_token(
        oauth_consumer,
        token=oauth_token,
        http_url=url,
        http_method=http_method,
        parameters=parameters if parameters is not None else [])

    req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)
    headers = req.to_header()

    if http_method == "POST":
        encoded_post_data = req.to_postdata()
    else:
        encoded_post_data = None
        url = req.to_url()

    opener = urllib.OpenerDirector()
    opener.add_handler(http_handler)
    opener.add_handler(https_handler)
    response = opener.open(url, encoded_post_data)

    return response


def fetchsamples():
    url = "https://stream.twitter.com/1/statuses/sample.json"
    response = twitterreq(url)
    for line in response:
        print line.strip()


if __name__ == '__main__':
    fetchsamples()
