# Download the Python helper library from twilio.com/docs/python/install
from twilio.rest import TwilioRestClient

# Your Account Sid and Auth Token from twilio.com/user/account
config = ParseTwilioConfig.Parser("sagar.config")
config.parseConfig()
account_sid = config.getAccountSid
auth_token  = config.get
client = TwilioRestClient(account_sid, auth_token)

call = client.calls.create(url="http://demo.twilio.com/docs/voice.xml", to="+40734203494", from_="+17079883108 ")
print(call.sid)
