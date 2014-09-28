import urllib
import httplib
import json
import logging

class TeamScore(object):
    
    SERVER = 'football-api.com'
    API_URL = '/api/?Action=today&APIKey=CHANGE-ME&comp_id=1204'

    RESULT_WIN = 1
    RESULT_DRAW = 0
    RESULT_LOSE = -1

    def __init__(self, football_team_name, json=None):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._team_name = football_team_name
        self._match_json = json
        self._team_score = self._get_team_score()
        self._logger.info('Initial score {0}'.format(self._team_score))
        
    def new_goal(self):
        self._logger.info('Checking new goal')
        team_score = self._get_team_score()
        if team_score != self._team_score:
            self._logger.info('New goal is different')
            self._team_score = team_score
            return True

        self._logger.info('New goal is equal')
        return False

    def result(self):
        self._logger.info('Checking new result')
        return self._get_team_result()

    def _get_live_scores(self):
        self._logger.info('Getting live scores')
        connection = httplib.HTTPConnection(self.SERVER)        
        connection.request('GET', self.API_URL)
        live_scores = connection.getresponse()
        live_scores_json = json.loads(live_scores.read())

        return live_scores_json 

    def _get_team_match(self, live_scores_json):
        self._logger.info('Getting team match')
        matches = live_scores_json['matches']
        for match in matches:
            if match['match_localteam_name'] == self._team_name or match['match_visitorteam_name'] == self._team_name:
                return match

    def _get_team_score(self):
        self._logger.info('Getting team score')
        if self._match_json:
            with open(self._match_json, 'r') as f:
                match_json = json.load(f)
        else:
            live_scores_json = self._get_live_scores()
            match_json = self._get_team_match(live_scores_json)

        if match_json['match_localteam_name'] == self._team_name:
            return match_json['match_localteam_score']
        else:
            return match_json['match_visitorteam_score']

    def _check_local(self, match_json):
        self._logger.info('Checking if team is local')
        if match_json['match_localteam_name'] == self._team_name:
            return True
        return False

    def _get_team_result(self):
        self._logger.info('Getting team result')
        if self._match_json:
            with open(self._match_json, 'r') as f:
                match_json = json.load(f)
        else:
            live_scores_json = self._get_live_scores()
            match_json = self._get_team_match(live_scores_json)

        if match_json['match_localteam_score'] == match_json['match_visitorteam_score']:
            return self.RESULT_DRAW
        else:
            if self._check_local(match_json):
               if match_json['match_localteam_score'] > match_json['match_visitorteam_score']:
                    return self.RESULT_WIN
               else:
                    return self.RESULT_LOSE
            else:
               if match_json['match_localteam_score'] > match_json['match_visitorteam_score']:
                    return self.RESULT_LOSE
               else:
                    return self.RESULT_WIN
