# happinessTwilio
Twilio happiness hack repo

This orchestrates twilio and API.ai integration and some lower level logic

Usage:

* Get a Twilio account and a Api.AI account and list the 4 tokens :  AccountSid (Twilio) , AuthToken ( Twilio)
    ,ClientAccessToken (API.ai) , DevAccessToken (API.ai) as show in the sample .config file.

* Install dependencies using pip as listed in requirements (pip install requirements.txt)

* Download ngrok for proper http tunneling for inbound messages. (https://www.twilio.com/blog/2013/10/test-your-webhooks-locally-with-ngrok.html)

* Run the twilioCall code.
