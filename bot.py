import os
import time
from slackclient import SlackClient

BOT_NAME = 'trotsky'

def get_bot_id(bot_name):
    slack_client = SlackClient(os.environ.get('SLACK_TOKEN'))
    api_call = slack_client.api_call("users.list")
    if api_call.get('ok'):
        users = api_call.get('members')
        for user in users:
            if 'name' in user and user.get('name') == bot_name:
                return user['id']

BOT_ID = get_bot_id(BOT_NAME)
TOKEN = os.environ.get('SLACK_TOKEN')

slack_client = SlackClient(TOKEN)

def handle_command(command, channel):
    '''
    This code only gets called if the bot 'chooses' to respond
    based on the criteria in `parse_slack_output`
    
    command     Original text of the message with the @bot removed 
    channel     The ID (not name) of the channel the message was posted in
    '''

    # do the processing steps for the original message. 
    # Translate? Dyslexize? Something 

    response = command # for now, just say this exact same thing back to us 
    slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)

def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            # Here, we basically control when the bot will respond. 
            if output and 'text' in output:
                # If there is output and it has a text field:
                if BOT_NAME in output['text']:
                    tmp = '@{}'.format(BOT_NAME) 
                    text_without_bot_name = output['text'].split(tmp)[1].strip()
                    # If we choose to respond, we return a tuple: the text of what was said
                    # to get us to respond, and the channel the message was posted in 
                    return text_without_bot_name, output['channel'] 

    # If there is no output: 
    return None, None

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("Bot connected and running")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid token or bot ID?")
