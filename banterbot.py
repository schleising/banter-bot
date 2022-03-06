from datetime import datetime, timedelta, time
from pathlib import Path
import random
from typing import Optional
import warnings
import sys
import logging
from zoneinfo import ZoneInfo

from pytz import timezone
from telegram import Bot
from telegram.ext import Updater, JobQueue, CallbackContext

from Footy.Footy import Footy
from Footy.Match import Match
from Footy.TeamData import teamsToWatch, allTeams, supportedTeamMapping
import Footy.BantzStrings as BantzStrings

# Set the chat ID
CHAT_ID = '-701653934'

class BanterBot:
    def __init__(self) -> None:
        # Enable logging
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)

        self.logger = logging.getLogger(__name__)

        try:
            # Get the token from the bot_token.txt file, this is exclued from git, so may not exist
            with open(Path('bot_token.txt'), 'r', encoding='utf8') as secretFile:
                token = secretFile.read()
        except:
            # If bot_token.txt is not available, print some help and exit
            print('No bot_token.txt file found, you need to put your token from BotFather in here')
            sys.exit()

        # Set the teams we're interested in
        teams = [team for team in teamsToWatch]

        # Create a Footy object using the list of teams we're interested in
        self.footy = Footy(teams)

        # Create the Updater and pass it your bot's token.
        # Make sure to set use_context=True to use the new context based callbacks
        # Post version 12 this will no longer be necessary
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
        # Log that we are updating today's matches
        print('Updating matches')

        # Get today's matches for the teams in the list
        self.todaysMatches = self.footy.GetMatches()

        # If the download was successful, print the matches
        if self.todaysMatches is not None:
            # Iterate over the matches
            for match in self.todaysMatches:
                print(match)

                # Set the context to the supported team name if My Team is not playing, otherwise set it to the opposition
                teamContext=match.teamName

                # If the match is in the future
                if (match.matchDate - timedelta(minutes=5)) > datetime.now(ZoneInfo('UTC')):
                    # Add a job to send a message that this should be an easy game 5 minutes before the game starts
                    self.jq.run_once(self.SendEasyGame, match.matchDate - timedelta(minutes=5), context=teamContext)

                # Add a job to check the scores once the game starts
                matchContext = match
                runTime = match.matchDate if match.matchDate > datetime.now(ZoneInfo('UTC')) else 0
                self.jq.run_once(self.SendScoreUpdates, runTime, context=matchContext)

                if (match.matchDate + timedelta(minutes=5)) > datetime.now(ZoneInfo('UTC')):
                    # If this is a home game for one of the teams we're interested in, add the empty seats message
                    if match.homeTeam in supportedTeamMapping:
                        # Add a job to send the empty seats message 5 minutes after the game starts
                        self.jq.run_once(self.SendEmptySeats, match.matchDate + timedelta(minutes=5), context=teamContext)
        else:
            print('Download Failed')

    def SendMessage(self, bot: Bot, chatId: str, message: Optional[str]):
        if message is not None:
            bot.send_message(chat_id=chatId, text=message)
            print(message)
        else:
            print('No Status Change')

    def SendScoreUpdates(self, context: CallbackContext) -> None:
        if context.job is not None and isinstance(context.job.context, Match):
            oldMatchData = context.job.context
            newMatchData: Optional[Match] = self.footy.GetMatch(oldMatchData)

            if newMatchData is not None:
                # Get the dict details of the team we're sending a message about
                teamDict = allTeams[newMatchData.teamName]

                message = None

                # Check if this is the start of the match
                if newMatchData.matchChanges.fullTime:
                    if newMatchData.matchChanges.teamWon:
                        message = BantzStrings.teamWon[random.randint(0, len(BantzStrings.teamWon ) - 1)].format(**teamDict)
                    if newMatchData.matchChanges.teamLost:
                        message = BantzStrings.teamLost[random.randint(0, len(BantzStrings.teamLost ) - 1)].format(**teamDict)
                    if newMatchData.matchChanges.teamDrew:
                        message = BantzStrings.teamDrew[random.randint(0, len(BantzStrings.teamDrew ) - 1)].format(**teamDict)
                else:
                    if newMatchData.matchChanges.firstHalfStarted:
                        message = BantzStrings.teamMatchStarted[random.randint(0, len(BantzStrings.teamMatchStarted ) - 1)].format(**teamDict)
                    # Check for a goal
                    if newMatchData.matchChanges.teamScored:
                        message = BantzStrings.teamScored[random.randint(0, len(BantzStrings.teamScored) - 1)].format(**teamDict)
                    if newMatchData.matchChanges.teamConceded:
                        message = BantzStrings.teamConceded[random.randint(0, len(BantzStrings.teamConceded) - 1)].format(**teamDict)
                    if newMatchData.matchChanges.teamVarAgainst:
                        message = BantzStrings.teamVarAgainst[random.randint(0, len(BantzStrings.teamVarAgainst) - 1)].format(**teamDict)
                    if newMatchData.matchChanges.teamVarFor:
                        message = BantzStrings.teamVarFor[random.randint(0, len(BantzStrings.teamVarFor) - 1)].format(**teamDict)

                    # Add a job to check the scores again in 20 seconds
                    matchContext = newMatchData
                    self.jq.run_once(self.SendScoreUpdates, 20, context=matchContext)

                # If there is a message, add the scoreline
                if message is not None:
                    message = f'{message}\n{newMatchData.GetScoreline()}'

                self.SendMessage(context.bot, CHAT_ID, message)
        else:
            return

    def SendEmptySeats(self, context: CallbackContext) -> None:
        if  context.job is not None and isinstance(context.job.context, str):
            # Get the full team name
            team = context.job.context

            # Get the ground for this tean
            ground = allTeams[team]['ground']

            # Send the message
            context.bot.send_message(chat_id=CHAT_ID, text=f'Plenty of empty seats at {ground}')
            print(f'Plenty of empty seats at {ground}')

    def SendEasyGame(self, context: CallbackContext) -> None:
        if  context.job is not None and isinstance(context.job.context, str):
            # Get the full name for this team
            team = context.job.context

            # Get the shorter name for this team
            teamName = allTeams[team]['name']

            # Send the message
            context.bot.send_message(chat_id=CHAT_ID, text=f'Should be an easy game for {teamName}')
            print(f'Should be an easy game for {teamName}')

    # Log errors
    def error(self, update, context: CallbackContext) -> None:
        self.logger.warning('Update "%s" caused error "%s"', update, context.error)

# Main function
def main() -> None:
    # Filter out a warning from dateparser
    warnings.filterwarnings('ignore', message='The localize method is no longer necessary')

    # Start the banter bot
    BanterBot()

if __name__ == '__main__':
    # Call the main function
    main()
