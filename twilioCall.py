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
    _from = "+17079883108"
    _to = "+17072196111"
    #_to = "+447506225616"
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
        str1 = "My name is Noora and I will be helping you through the airport.  At this hour, I can predict it will take you around 38 minutes to exit the airport.  If you have any questions, just ask me via SMS which are btw free of charge ."
        str2 = ""
        return str1 + str2

    def buildBaggageMessage(self):
        str1 = "I just wanted to let you know that if somebody is waiting for you at arrivals, you can send 'notify (phone number)', and I will keep them up to date with your progress."
        str2 = ""
        return str1 + str2

    def buildFarewell(self):
        str1 = "All checked in baggage has been taken off the plane and will be arriving at conveyer belt 12 in approximately 25 minutes. After picking it up please proceed through customs to the arrival hall."
        return str1

    def to(self):
        return self._to

    def src(self):
        return self._from





class NooraComms:

    _clientAccess = ""
    _devAccess = ""
    _dest = ''
    _src = ''
    def __init__(self,config,dest , src):
        self._clientAccess = config.getClientAccessAPIAI()
        self._devAccess = config.getDevAccessAPIAI()
        self._dest = dest
        self._src = src

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
            print responseDict['result']
            if responseDict['result']['action'] == 'initiateCall' :
                placeHelpCall(config , self._dest , self._src)
        else:
            response_message = "Something went Terrible wrong with my brain, Bear with me !! "
        print response_message

        return response_message

    def processEvents(self , event):
        print signal




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
def runOnce(config , dst , src):
    account_sid = config.getAccountSid()
    auth_token  = config.getAuthToken()
    client = TwilioRestClient(account_sid, auth_token)


    Mbuilder = MessageBuilder(dst , src)
    m1 = client.messages.create(to=Mbuilder.to(), from_=Mbuilder.src(),body=Mbuilder.Body)
    print "Sent Body"
    #time.sleep(5)
    wait()

    m2 = client.messages.create(to=Mbuilder.to(), from_=Mbuilder.src(),body=Mbuilder.buildWelcomeMessage())
    print "Sent Welcome message"
    #time.sleep(5)
    wait()


    m4 = client.messages.create( to = Mbuilder.to() , from_ = Mbuilder.src() , body = Mbuilder.buildFarewell() );
    print "Sent Bags message"
    wait()

    m3 = client.messages.create( to = Mbuilder.to() , from_ = Mbuilder.src(), body = Mbuilder.buildBaggageMessage())
    print " Sent Notify Message"

@run_once
def placeIntroCall(config , dest , src):
    client = TwilioRestClient(config.getAccountSid(), config.getAuthToken())
    call = client.calls.create(url="https://dl.dropboxusercontent.com/u/1864833/firstCall.xml",
    #to="+40734203494",
    to =dest,
    from_ = src)


def placeHelpCall(config , dest , src):
    client = TwilioRestClient(config.getAccountSid(), config.getAuthToken())
    call = client.calls.create(url="https://dl.dropboxusercontent.com/u/1864833/helpCall.xml",
    #to="+40734203494",
    to =dest,
    from_ = src)


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


if __name__ == "__main__":
    config = ParseTwilioConfig.Parser("sagarProd.config")
    dest_ = "+17072196111"
    src_ = "+17079883108"
    config.parseConfig()

    NooraEngine = NooraComms(config , dest_ , src_ )
    #placeIntroCall(config , dest_ , src_)
    wait()
    #runOnce(config , dest_ , src _)
    app.run(debug=False)



