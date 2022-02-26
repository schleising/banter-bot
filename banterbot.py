from datetime import datetime, timedelta, time
from pathlib import Path
from typing import Optional
import warnings
import sys
import logging
from zoneinfo import ZoneInfo

from pytz import timezone
from telegram.ext import Updater, JobQueue, CallbackContext

from Footy.Footy import Footy
from Footy.Match import Match

# Set the chat ID
CHAT_ID = '-701653934'

# Map team names and stadiums
teamMapping = {
    'Tottenham Hotspur FC': {
        'name': 'Tottenham',
        'ground': 'Tottenham Hotspur Sainsburys Arena',
    },
    'Chelsea FC': {
        'name': 'Chelsea',
        'ground': 'Stamford Bridge',
    },
    'Liverpool FC': {
        'name': 'Liverpool',
        'ground': 'Anfield',
    },
    'Manchester City FC': {
        'name': 'Man City',
        'ground': 'the Etihad'
    }
}

class BanterBot:
    def __init__(self) -> None:
        # Enable logging
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)

        self.logger = logging.getLogger(__name__)

        # Create the Updater and pass it your bot's token.
        # Make sure to set use_context=True to use the new context based callbacks
        # Post version 12 this will no longer be necessary
        try:
            # Get the token from the bot_token.txt file, this is exclued from git, so may not exist
            with open(Path('bot_token.txt'), 'r', encoding='utf8') as secretFile:
                token = secretFile.read()
        except:
            # If bot_token.txt is not available, print some help and exit
            print('No bot_token.txt file found, you need to put your token from BotFather in here')
            sys.exit()

        # Set the teams we're interested in
        self.teams = [team for team in teamMapping]

        # Create a Footy object using the list of teams we're interested in
        self.footy = Footy(self.teams)

        # Create the updater
        self.updater = Updater(token, use_context=True)

        # Get the dispatcher to register handlers
        self.dp = self.updater.dispatcher

        # Get the job queue
        self.jq: JobQueue = self.updater.job_queue

        # Add a job which gets todays matches once a day at 1am
        matchUpdateTime = time(1, 0, tzinfo=timezone('UTC'))
        nowTime = datetime.now(tz=ZoneInfo('UTC')).timetz()
        self.jq.run_daily(self.MatchUpdateHandler, matchUpdateTime)

        # Call Get Matches if this is started after the update time
        if nowTime > matchUpdateTime:
            self.GetMatches()

        # Add the error handler to log errors
        self.dp.add_error_handler(self.error)

        # Start the bot polling
        self.updater.start_polling()

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        self.updater.idle()

    def MatchUpdateHandler(self, context: CallbackContext) -> None:
        # Call get matches, this allows the function to be called directly
        self.GetMatches()

    def GetMatches(self) -> None:
        # Get today's matches for the teams in the list
        self.todaysMatches = self.footy.GetTodaysMatches()

        # If the download was successful, print the matches
        if self.todaysMatches is not None:
            # Iterate over the matches
            for match in self.todaysMatches:
                print(match)

                # Set the context to the team name
                teamContext=match.homeTeam if match.homeTeam in self.teams else match.awayTeam

                # If the match is in the future
                if match.matchDate > datetime.now(ZoneInfo('UTC')):
                    # Add a job to send a message that this should be n easy game
                    self.jq.run_once(self.SendEasyGame, match.matchDate - timedelta(minutes=5), context=teamContext)

                # Add a job to check the scores once the game starts
                matchContext = match
                runTime = match.matchDate if match.matchDate > datetime.now(ZoneInfo('UTC')) else 0
                self.jq.run_once(self.SendScoreUpdates, runTime, context=matchContext)

                # If this is a home game for one of the teams we're interested in, add the empty seats message
                if match.homeTeam in self.teams:
                    # Add a job to send the empty seats message
                    self.jq.run_once(self.SendEmptySeats, match.matchDate + timedelta(minutes=5), context=teamContext)
        else:
            print('Download Failed')

    def SendScoreUpdates(self, context: CallbackContext):
        if context.job is not None:
            oldMatchData: Match = context.job.context
            newMatchData: Optional[Match] = self.footy.GetMatch(oldMatchData.id)

            if newMatchData is not None:
                if oldMatchData.homeScore != newMatchData.homeScore or oldMatchData.awayScore != newMatchData.awayScore:
                    context.bot.send_message(chat_id=CHAT_ID, text=f'{newMatchData}')

                if newMatchData.status != 'FINISHED':
                    # Add a job to check the scores once the game starts
                    matchContext = newMatchData
                    self.jq.run_once(self.SendScoreUpdates, 60, context=matchContext)
                elif oldMatchData.status != 'FINISHED':
                    # Send the final score
                    context.bot.send_message(chat_id=CHAT_ID, text=f'{newMatchData}')
        else:
            return

    def SendEmptySeats(self, context: CallbackContext) -> None:
        # Get the full team name
        team = context.job.context if context.job is not None else 'FATAL ERROR !!!'

        # Get the ground for this tean
        ground = teamMapping[team]['ground']

        # Send the message
        context.bot.send_message(chat_id=CHAT_ID, text=f'Plenty of empty seats at {ground}')

    def SendEasyGame(self, context: CallbackContext) -> None:
        # Get the full name for this team
        team = context.job.context if context.job is not None else 'FATAL ERROR !!!'

        # Get the shorter name for this team
        teamName = teamMapping[team]['name']

        # Send the message
        context.bot.send_message(chat_id=CHAT_ID, text=f'Should be an easy game for {teamName}')

    # Log errors
    def error(self, update, context):
        self.logger.warning('Update "%s" caused error "%s"', update, context.error)

# Main function
def main():
    # Filter out a warning from dateparser
    warnings.filterwarnings('ignore', message='The localize method is no longer necessary')

    # Start the banter bot
    BanterBot()

if __name__ == '__main__':
    # Call the main function
    main()
