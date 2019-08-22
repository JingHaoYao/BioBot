import os
import time
import re
import sqlite3
from slackclient import SlackClient
from biobot_db import BioBotDB


# instantiate Slack client
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
biobot_id = None

# constants
RTM_READ_DELAY = 0.2
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"
command_list = [
    "add bio",
    "remove bio",
    "display bio"
]

biobot_db = BioBotDB()

def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            user = event["user"]
            if user_id == biobot_id:
                return message, event["channel"], user
    return None, None, None

def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)
    print (matches.group(1))
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def post_message(channel, text):
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=text
    )

def handle_command(command, channel, user):
    """
        Executes bot command if the command is known
    """
    # Default response is help text for the user
    default_response = "Not sure what you mean <@{}>. Try *help*".format(user)

    # Finds and executes the given command, filling in response
    response = None
    # This is where you start to implement more commands!
    if command.startswith("help"):
        response = "Possible commands are:\n- " + "\n- ".join(command_list)
    elif command.startswith("display bio"):
        slack_id, msg = parse_direct_mention(command.split()[2])
        if slack_id is None:
            response = "Please enter a person to display their bio!"
        else:
            response = biobot_db.select_bio_db(slack_id)
    elif command.startswith("remove bio"):
        biobot_db.delete_bio_db(user)
        response = "Bio deleted!"

    # Sends the response back to the channel
    post_message(
        channel,
        text=response or default_response
    )

if __name__ == "__main__":

    if slack_client.rtm_connect(
        with_team_state=False,
        auto_reconnect=True
    ):
        print("BioBot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        biobot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel, user = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel, user)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")
