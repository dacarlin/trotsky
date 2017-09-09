import os 
from slackclient import SlackClient 

# this code from https://www.fullstackpython.com/blog/build-first-slack-bot-python.html

BOT_NAME = 'tell'
slack_client = SlackClient(os.environ.get('SLACK_TOKEN'))

if __name__ == '__main__':
    api_call = slack_client.api_call("users.list")
    if api_call.get('ok'):
        
        users = api_call.get('members')
        for user in users: 
            if 'name' in user and user.get('name') == BOT_NAME:
                print("Bot ID for {} is {}".format(user['name'], user['id'])) 


