# Download the Python helper library from twilio.com/docs/python/install
from twilio.rest import TwilioRestClient
import ParseTwilioConfig
import time
import os
import json
from flask import Flask, request, redirect
from twilio import twiml
import twilio

try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai


class MessageBuilder:
    _from = "+17079883108 "
    _to = "+17072196111"
    Body = "Welcome to Dubai, This is a cost free Message.."

    def __init__(self , t=None , f=None):
        if t != None:
            self._to = t
        if f != None:
            self._from = f

    def buildTransitMessage(self):
        str1 = "You have landed on Terminal 1, your connecting fligt is on terminal 2 and it will take you 15 minutes to reach there"
        str2 = "Further information about the gates would be delivered cost free when you reach there"
        return str1 + str2

    def buildWelcomeMessage(self):
        str1 = "Currently the approximate immigration time is 35 minutes "
        str2 = "Information about baggage would be delivered once you reach immigration"
        return str1 + str2

    def buildBaggageMessage(self):
        str1 = "Your bags are on Carousal 5"
        str2 = "The turn around time is nominal and you should get your bags in approximately 10 minutes"
        return str1 + str2

    def buildFarewell(self):
        str1 = "I hope your transit/experience with DXB was pleasent. We look forward to serve you again. Enjoy DubHI!!"
        return str1

    def to(self):
        return self._to

    def src(self):
        return self._from





class NooraComms:

    _clientAccess = ""
    _devAccess = ""
    def __init__(self,config):
        self._clientAccess = config.getClientAccessAPIAI()
        self._devAccess = config.getDevAccessAPIAI()

    def sendQuery(self, text):
        response_message = ""
        ai = apiai.ApiAI(self._clientAccess)
        request = ai.text_request()
        request.lang = 'en'  # optional, default value equal 'en'
        request.session_id = "<SESSION ID, UNIQUE FOR EACH USER>"
        request.query = text
        response = request.getresponse()
        responseDict = json.loads (response.read())
        if responseDict['status']['code'] == 200:
            response_message = responseDict['result']['fulfillment']['speech']
        else:
            response_message = "Something went Terrible wrong with my brain, Bear with me !! "
        print response_message

        return response_message




def wait():
    os.system('read -s -n 1 -p "Press any key to continue..."')


def run_once(f):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)
    wrapper.has_run = False
    return wrapper


@run_once
def runOnce(config):
    account_sid = config.getAccountSid()
    auth_token  = config.getAuthToken()
    client = TwilioRestClient(account_sid, auth_token)


    Mbuilder = MessageBuilder()
    m1 = client.messages.create(to=Mbuilder.to(), from_=Mbuilder.src(),body=Mbuilder.Body)
    print "Sent Body"
    #time.sleep(5)
    wait()

    m2 = client.messages.create(to=Mbuilder.to(), from_=Mbuilder.src(),body=Mbuilder.buildWelcomeMessage())
    print "Sent Welcome message"
    #time.sleep(5)
    wait()

    m3 = client.messages.create( to = Mbuilder.to() , from_ = Mbuilder.src(), body = Mbuilder.buildBaggageMessage())
    print " Sent baggage message"
    #time.sleep(5)
    wait()

    m4 = client.messages.create( to = Mbuilder.to() , from_ = Mbuilder.src() , body = Mbuilder.buildFarewell() );
    print "Sent farewell"

@run_once
def placeIntroCall(config):
    client = TwilioRestClient(config.getAccountSid(), config.getAuthToken())
    call = client.calls.create(url="https://dl.dropboxusercontent.com/u/1864833/firstCall.xml",
    #to="+17072196111",
    to ="+46729994117",
    from_ = "+17079883108")


app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
    """Respond to incoming calls with a simple text message."""

    resp = twilio.twiml.Response()
    inbound_message = request.form.get('Body')
    print "recieved : " + inbound_message
    # response_message = "I don't understand what you meant...need more code!"
    # if inbound_message != "Hello":
    #     resp.message(response_message)
    # else:
    #     resp.message("Hello to you too")
    response_message = NooraEngine.sendQuery(inbound_message)
    resp.message(response_message)

    return str(resp)

# @app.route("/twilio", methods=['POST'])
# def inbound_sms():
#     twiml_response = twiml.Response()
#     inbound_message = request.forms.get("Body")
#     response_message = "I don't understand what you meant...need more code!"
#     # we can use the incoming message text in a condition statement
#     if inbound_message == "Hello":
#         response_message = "Well, hello right back at ya!"
#     twiml_response.message(response_message)
#     # we return back the mimetype because Twilio needs an XML response
#     response.content_type = "application/xml"
#     return str(twiml_response)


if __name__ == "__main__":
    config = ParseTwilioConfig.Parser("sagarProd.config")
    config.parseConfig()

    NooraEngine = NooraComms(config)
    placeIntroCall(config)
    wait()
    #runOnce(config)
    app.run(debug=False)



