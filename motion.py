import urllib
import httplib
import json
import logging

class Motion(object):

    SERVER = 's2.tts01.net'        
    ACCESS_TOKEN = "CHANGE-ME"
    RESOURCE_PATH_MOTION = '/Api/v1/000285/Motion/'

    
    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)

    def _get_request(self, resource_path, params):
        self._logger.info('Sending get request')
        connection = httplib.HTTPConnection(self.SERVER)        
        connection.request('GET', resource_path + '?' + urllib.urlencode(params))
        response = connection.getresponse()        
        return response

    def presence(self):
        self._logger.info('Checking presence')
        parameters = {}   
        parameters['oauth_consumer_key'] = self.ACCESS_TOKEN       
        response = self._get_request(self.RESOURCE_PATH_MOTION, parameters)
        response_json = json.loads(response.read())
        
        index = response_json["objects"][0]["id"]
        value = response_json["objects"][0]["value"]
        presence = value.startswith('1')
        self._logger.info('Presence value: {0}'.format(presence))

        return presence

