import urllib
import httplib
import json
import logging

class Audiovisual(object):

    SERVER = 's2.tts01.net'        
    ACCESS_TOKEN = "CHANGE-ME"
    RESOURCE_PATH_AUDIO = '/Api/v1/000285/AudioVisual/'
    RESOURCE_PATH_COLOR = '/Api/v1/000285/RGB/RGB/'

    RED = '1,0,0'
    YELLOW = '1,1,0'
    GREEN = '0,1,0'
    WHITE = '1,1,1'
    MELODY = '3:1:1000:2E.N:2E.N:2C.D:S.D'
    SILENCE = '1:1:1000:S.N'
    
    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)

    def _get_request(self, resource_path, params):
        self._logger.info('Sending get request')
        connection = httplib.HTTPConnection(self.SERVER)        
        connection.request('GET', resource_path + '?' + urllib.urlencode(params))
        response = connection.getresponse()        
        return response

    def _put_request(self, resource_path, params, headers):
        self._logger.info('Sending put request')
        connection = httplib.HTTPConnection(self.SERVER)        
        connection.request('PUT', resource_path, json.dumps(params), headers=headers)
        response = connection.getresponse()        
        if "20" in str(response.status):
            return True
        else:
            return False

    def set_color(self, color):
        parameters = {}   
        parameters['oauth_consumer_key'] = self.ACCESS_TOKEN       
        response = self._get_request(self.RESOURCE_PATH_COLOR, parameters)
        response_json = json.loads(response.read())
        
        index = response_json["objects"][0]["id"]
        value = response_json["objects"][0]["value"]
        self._logger.info('Previous color is {0}'.format(value))

        parameters['value'] = color
        headers = {'Authorization': "OAuth %s" % self.ACCESS_TOKEN,  
                   'Content-Type': "application/json",                  
                  }

        self._logger.info('Setting color to {0}'.format(color))
        return self._put_request(self.RESOURCE_PATH_COLOR + str(index), parameters, headers)
        
    def set_melody(self, melody):
        parameters = {}   
        parameters['oauth_consumer_key'] = self.ACCESS_TOKEN       
        response = self._get_request(self.RESOURCE_PATH_AUDIO, parameters)
        response_json = json.loads(response.read())
        
        index = response_json["objects"][0]["id"]
        value = response_json["objects"][0]["value"]
        self._logger.info('Previous melody: {0}'.format(value))

        parameters['value'] = melody
        headers = {'Authorization': "OAuth %s" % self.ACCESS_TOKEN,  
                   'Content-Type': "application/json",                  
                  }

        self._logger.info('Setting melody to: {0}'.format(melody))
        return self._put_request(self.RESOURCE_PATH_AUDIO + str(index), parameters, headers)
