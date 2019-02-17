from slacker import Slacker
import yaml
import sys

with open('./data/config.yml') as f:
    config = yaml.safe_load(f)

slack = Slacker(config['config']['slack']['token'])
channel = config['config']['slack']['channel']
icon = config['config']['slack']['icon']

slack.chat.post_message(channel, sys.argv[1], icon_emoji=icon)
