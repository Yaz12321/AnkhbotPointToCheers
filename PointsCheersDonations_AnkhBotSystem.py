#---------------------------------------
#	Import Libraries
#---------------------------------------
import clr, sys, json, os, codecs
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")
from ast import literal_eval

#---------------------------------------
#	[Required]	Script Information
#---------------------------------------
ScriptName = "Points_to_Cheers_Donations"
Website = ""
Creator = "Yaz12321"
Version = "1.0"
Description = "Give points to cheers and donations"

settingsFile = os.path.join(os.path.dirname(__file__), "settings.json")

#---------------------------------------
#   Version Information
#---------------------------------------

# Version:

# > 1.0 < 
    # Official Release

class Settings:
    # Tries to load settings from file if given 
    # The 'default' variable names need to match UI_Config
    def __init__(self, settingsFile = None):
        if settingsFile is not None and os.path.isfile(settingsFile):
            with codecs.open(settingsFile, encoding='utf-8-sig',mode='r') as f:
                self.__dict__ = json.load(f, encoding='utf-8-sig') 
        else: #set variables if no settings file
            self.bitratio = 10
            self.donationratio = 10
            
    # Reload settings on save through UI
    def ReloadSettings(self, data):
        self.__dict__ = json.loads(data, encoding='utf-8-sig')
        return

    # Save settings to files (json and js)
    def SaveSettings(self, settingsFile):
        with codecs.open(settingsFile,  encoding='utf-8-sig',mode='w+') as f:
            json.dump(self.__dict__, f, encoding='utf-8-sig')
        with codecs.open(settingsFile.replace("json", "js"), encoding='utf-8-sig',mode='w+') as f:
            f.write("var settings = {0};".format(json.dumps(self.__dict__, encoding='utf-8-sig')))
        return


#---------------------------------------
# Initialize Data on Load
#---------------------------------------
def Init():
    # Globals
    global MySettings

    # Load in saved settings
    MySettings = Settings(settingsFile)

    # End of Init
    return

#---------------------------------------
# Reload Settings on Save
#---------------------------------------
def ReloadSettings(jsonData):
    # Globals
    global MySettings

    # Reload saved settings
    MySettings.ReloadSettings(jsonData)

    # End of ReloadSettings
    return

def Execute(data):
    
    #Parent.SendTwitchMessage(data.RawData)
    if "PRIVMSG" in data.RawData:
        splitted = data.RawData.split("PRIVMSG")
        if "bits" in splitted[0]:
            splitted2 = splitted[0].split(";")
            for i in splitted2:
                if "bits" in i:
                    value = i.replace("bits=","")
                    points = int(float(value)*float(MySettings.bitratio/100))
                    success = Parent.AddPoints(data.User,points)
                    #Parent.SendTwitchMessage("Success?: {} {}".format(success,points))
                    

        if "amount" in splitted[0]:
            splitted2 = splitted[0].split(";")
            for i in splitted2:
                if "amount" in i:
                    value = i.replace("amount=","")
                    points = int(float(value)*MySettings.donationratio)
                    success = Parent.AddPoints(data.User,points)
                    #Parent.SendTwitchMessage("Success?: {} {}".format(success,points))    

    return

def Tick():
    return

def UpdateSettings():
    with open(m_ConfigFile) as ConfigFile:
        MySettings.__dict__ = json.load(ConfigFile)
    return
