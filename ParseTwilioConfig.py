import ConfigParser
import io

class Parser:
    _account_sid = ""
    _auth_token = ""
    _configFilePath = ""
    _maxTweets="100"
    configParser = ConfigParser.RawConfigParser()

    def __init__(self, filepath):
        self._configFilePath = filepath
        print 'Using File : ', filepath

        try:
            self.configParser.readfp(open(filepath, 'r'))
        except:
            print 'Invalid cofig file path, Cannot open', filepath

    def parseConfig(self):
        try:
            self._auth_token =  self.configParser.get('User_Twilio_Config','AuthToken')
            self._account_sid = self.configParser.get('User_Twilio_Config','AccountSid')
        except:
            print 'Invalid configuration'


    def getAuthToken(self):
        return self._auth_token

    def getAccountSid(self):
        return self._account_sid


