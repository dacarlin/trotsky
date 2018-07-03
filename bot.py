import os
import time
from slackclient import SlackClient

BOT_NAME = 'trotsky'
TOKEN = os.environ.get('SLACK_TOKEN')

def get_bot_id(bot_name, token):
    slack_client = SlackClient(token)
    api_call = slack_client.api_call('users.list')
    if api_call.get('ok'):
        users = api_call.get('members')
        for user in users:
            if 'name' in user and user.get('name') == bot_name:
                print('Found user ID {} for bot {}'.format(user['id'], bot_name)) 
                return user['id']

BOT_ID = get_bot_id(BOT_NAME, TOKEN) 
slack_client = SlackClient(TOKEN)

def detect_will(token): 
    not_will = "alex brooks trotsky dickbot a.maclay slackbot".split() 
    slack_client = SlackClient(token) 
    api_call = slack_client.api_call('users.list') 
    if api_call.get('ok'): 
        users = api_call.get('members')
        potential_wills = []
        for user in users:
            if user['name'] not in not_will:
                print("Potentiall Will:", user['name']) 
                potential_wills.append(user) 
        #print("Potential Wills:", potential_wills) 
        if len(potential_wills) == 1:
            will = potential_wills[0] 
            print("Detected Will as user {} with ID {}".format(will['name'], will['id'])) 
            return will 

WILL_USER = detect_will(TOKEN) 

def handle_command(message_text, channel, user):
    '''
    Given a message (text) and a channel name, do something
    '''
    
    if user == WILL_USER['id']:
        return

    if user == BOT_ID:
        return  

    WILL_NAME = WILL_USER['name'] 
    if '@will' in message_text:
        response = message_text.replace('@will', '@{}'.format(WILL_NAME)).strip()
        slack_client.api_call('chat.postMessage', channel=channel, text=response, as_user=True) 
    elif 'bye' in message_text.lower():
        response = 'See ya! Wouldn\'t wanna be ya'
        slack_client.api_call('chat.postMessage', channel=channel, text=response, as_user=True) 
        exit()
    else:
        # do nothing 
        pass 

def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output:
                print(output.keys()) 
                print(type(output['user'])) 
                # The bot will be listening to all messages 
                print('Message text: {}'.format(output['text'])) 
                return output['text'], output['channel'], output['user'] 

    # If there is no output: 
    return None, None, None 

if __name__ == '__main__':
    READ_WEBSOCKET_DELAY = 2 
    if slack_client.rtm_connect():
        print('Bot connected and running')
        while True:
            text, channel, user = parse_slack_output(slack_client.rtm_read())
            if text and channel and user:
                handle_command(text, channel, user)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print('Connection failed. Invalid token or bot ID?')
