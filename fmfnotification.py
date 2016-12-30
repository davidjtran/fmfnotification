import praw
from twilio.rest import TwilioRestClient
import time
from accounts import *
import traceback

reddit = praw.Reddit('bot1')
subreddit = reddit.subreddit("frugalmalefashion")

checked = []

#checks for most recent post
def fmfNotification():
    while True:
        for submission in subreddit.new(limit = 1):
            subID = submission.id
            if subID not in checked:
                checked.append(subID)
                link = "https://www.reddit.com/" + submission.permalink
                title = submission.title
                postInfo = title + "\n" + link
                if (len(postInfo) >= 160):
                    postInfo = title
                    sendText(postInfo)
                else:
                    sendText(postInfo)

#twilio sms
def sendText(postInfo):
    account = twilioAccountID
    token = twilioAccountToken
    client = TwilioRestClient(account, token)
    message = client.sms.messages.create(to=myNumber,
                                     from_=twilioNumber,
                                     body=postInfo)

# #constantly updating in case servers are down
def secondary():
    try:
        while True:
            fmfNotification()
    except:
        traceback.print_exc()
        print('Resuming in 30sec...')
        time.sleep(30)

secondary()
