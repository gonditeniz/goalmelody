#!/usr/bin/python

import logging
from teamscore import TeamScore
from audiovisual import Audiovisual 
from motion import Motion 
import argparse
import time

OFF_TIME = 15

def _parse_args():
    parser = argparse.ArgumentParser(description='Play a sound when your team scores a goal. Display a color depending on you team result.')
    parser.add_argument('-t', '--team', dest='team', action='store',
                       help='Name of the team', type=str, required=True)
    parser.add_argument('-c', '--check-time', dest='time', action='store',
                       help='Time interval for checking results in seconds', type=int, required=True)
    parser.add_argument('-j', '--json', dest='json', action='store', default=None,
                       help='Local json for checking results', type=str)

    args = parser.parse_args()
    return args

def main():
    args = _parse_args()

    logging.basicConfig(level=logging.DEBUG)    
    
    team_score = TeamScore(args.team, args.json)
    audiovisual = Audiovisual()
    motion = Motion()

    while(True):
        if motion.presence():
            if team_score.new_goal():
                audiovisual.set_melody(Audiovisual.MELODY) 
                time.sleep(OFF_TIME)
                audiovisual.set_melody(Audiovisual.SILENCE) 

            team_result = team_score.result()
            if  team_result == TeamScore.RESULT_WIN:
                audiovisual.set_color(Audiovisual.GREEN) 
            elif team_result == TeamScore.RESULT_DRAW:
                audiovisual.set_color(Audiovisual.YELLOW) 
            else:
                audiovisual.set_color(Audiovisual.RED) 
        else:
            audiovisual.set_color(Audiovisual.WHITE) 
            
        time.sleep(args.time-OFF_TIME)
            

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logging.info('Thanks for using GoalMelody')
        exit(0)
