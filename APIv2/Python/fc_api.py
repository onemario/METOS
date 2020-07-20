import requests
from requests.auth import AuthBase
from Crypto.Hash import HMAC
from Crypto.Hash import SHA256
from datetime import datetime
from dateutil import tz


class AuthHmacMetos(AuthBase):
    """Creates HMAC authorization header for Metos REST service POST request."""
    def __init__(self, apiRoute, publicKey, privateKey, method):
        self._publicKey = publicKey
        self._privateKey = privateKey
        self._method = method
        self._apiRoute = apiRoute

    def __call__(self, request):
        dateStamp = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')#'Mon, 23 Jul 2018 13:24:09 GMT'#
        request.headers['Date'] = dateStamp
        msg = (self._method + self._apiRoute + dateStamp + self._publicKey).encode(encoding='utf-8')
        h = HMAC.new(self._privateKey.encode(encoding='utf-8'), msg, SHA256)
        signature = h.hexdigest()
        authorizationStr = 'hmac ' + self._publicKey + ':' + signature
        request.headers['Authorization'] = authorizationStr
        #print('HMAC header decrypted: {}'.format(msg)
        #print('Accept: {}'.format(request.headers['Accept']))
        #print('Authorization: {}'.format(request.headers['Authorization']))
        #print('Date: {}'.format(request.headers['Date']))    
        return request

class FcApi:
    """Sets API endpoint URL for GET and POST requests."""
    def __init__(self, apiUri, publicKey, privateKey):
        self._apiUri = apiUri
        self._publicKey = publicKey
        self._privateKey = privateKey

    def __checkStatus(self, response, auth, route):
        response.close()
        print(" > {} {}".format(auth._method, self._apiUri + route))
        if response.status_code != 200:
            print(" > {} {}".format(response.status_code, response.reason))

    def get(self, route):
        pure_route = route.split('?', 1)[0] #remove parameters from the route for signature calculation
        auth = AuthHmacMetos(pure_route, self._publicKey, self._privateKey, 'GET')
        response = requests.get(self._apiUri + route, headers={'Accept': 'application/json'}, auth=auth)
        response.close()
        self.__checkStatus(response, auth, route)
        return response

    def post(self, route, payload):
        auth = AuthHmacMetos(route, self._publicKey, self._privateKey, 'POST')
        response = requests.post(self._apiUri + route, data=payload, headers={'Accept': 'application/json'}, auth=auth)
        response.close()
        self.__checkStatus(response, auth, route)
        return response

    def put(self, route, payload):
        auth = AuthHmacMetos(route, self._publicKey, self._privateKey, 'PUT')
        response = requests.put(self._apiUri + route, data=payload, headers={'Accept': 'application/json'}, auth=auth)
        response.close()
        self.__checkStatus(response, auth, route)
        return response

    def getEpochs(self, timestamp, station_timezone=None):
        """
        Convert given datetime to UNIX epochs in local station timezone

        timestamp        -- e.g. datetime(2018, 10, 10, 0, 0, 0)
        station_timezone -- e.g. tz.tzlocal()
        """
        if station_timezone is None:
            station_timezone = tz.tzlocal()
        # conversion to POSIX seconds
        t0 = datetime(1970, 1, 1).replace(tzinfo=station_timezone)
        return int((timestamp.replace(tzinfo=station_timezone) - t0).total_seconds())
