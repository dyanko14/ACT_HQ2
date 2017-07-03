from extronlib.interface import SerialInterface, EthernetClientInterface
import re
from extronlib.system import Wait, ProgramLog


class DeviceClass:

    def __init__(self):

        self.Unidirectional = 'False'
        self.connectionCounter = 5
        self.DefaultResponseTimeout = 0.3
        self._compile_list = {}
        self.Subscription = {}
        self.ReceiveData = self.__ReceiveData
        self._ReceiveBuffer = b''
        self.counter = 0
        self.connectionFlag = True
        self.initializationChk = True
        self.Debug = False
        self.Models = {}

        self.Commands = {
            'ConnectionStatus': {'Status': {}},
            'AspectRatio': {'Status': {}},
            'AudioMute': {'Parameters': ['Group'], 'Status': {}},
            'AutoImage': {'Status': {}},
            'AutoMemory': {'Status': {}},
            'ExecutiveMode': {'Status': {}},
            'Freeze': {'Status': {}},
            'DigitalInputMode': {'Parameters': ['Input'], 'Status': {}},
            'DigitalInputStatus': {'Parameters': ['Input'], 'Status': {}},
            'DigitalOutputMode': {'Parameters': ['Output'], 'Status': {}},
            'HDCPAuthentication': {'Status': {}},
            'HDCPMode': {'Status': {}},
            'HDCPNotification': {'Status': {}},
            'HDMIInputEDID': {'Status': {}},
            'HDMILoopFormat': {'Status': {}},
            'OverscanMode': {'Status': {}},
            'Preset': {'Parameters': ['Preset'], 'Status': {}},
            'ScreenSaverMode': {'Status': {}},
            'ScreenSaverStatus': {'Status': {}},
            'USBHostStatus': {'Status': {}},
            'USBStreamingFormat': {'Status': {}},
            'USBTerminalType': {'Status': {}},
            'VideoMute': {'Parameters': ['Output'], 'Status': {}},
            'VideoSendStatus': {'Status': {}},
            'VideoSignalPresence': {'Status': {}},
            'Volume': {'Parameters': ['Group'], 'Status': {}}
        }
        self.devicePassword = 'extron'
        self.VerboseEnabled = True
        self.PasswdPromptCount = 0
        self.Authenticated = 'Not Needed'


        if self.Unidirectional == 'False':
            self.AddMatchString(re.compile(b'Aspr1\*(1|2)\r\n'), self.__MatchAspectRatio, None)
            self.AddMatchString(re.compile(b'GrpmD(2|4|6|8|10)\*(1|0)\r\n'), self.__MatchAudioMute, None)
            self.AddMatchString(re.compile(b'Amem1\*(0|1)\r\n'), self.__MatchAutoMemory, None)
            self.AddMatchString(re.compile(b'Exe(0|1)\r\n'), self.__MatchExecutiveMode, None)
            self.AddMatchString(re.compile(b'Frz(0|1)\r\n'), self.__MatchFreeze, None)
            self.AddMatchString(re.compile(b'Gpit(1|2)\*(10|[0-9])\r\n'), self.__MatchDigitalInputMode, None)
            self.AddMatchString(re.compile(b'Gpi(1|2)\*(0|1)\r\n'), self.__MatchDigitalInputStatus, None)
            self.AddMatchString(re.compile(b'Gpot(1|2)\*([0-5])\r\n'), self.__MatchDigitalOutputMode, None)
            self.AddMatchString(re.compile(b'HdcpE1\*(0|1)\r\n'), self.__MatchHDCPAuthentication, None)
            self.AddMatchString(re.compile(b'HdcpS([0-4])\r\n'), self.__MatchHDCPMode, None)
            self.AddMatchString(re.compile(b'HdcpN(0|1)\r\n'), self.__MatchHDCPNotification, None)
            self.AddMatchString(re.compile(b'EdidA1\*([1-5][0-9])\r\n'), self.__MatchHDMIInputEDID, None)
            self.AddMatchString(re.compile(b'Vtpo2\*([0-7])\r\n'), self.__MatchHDMILoopFormat, None)
            self.AddMatchString(re.compile(b'Oscn1\*(0|1|2)\r\n'), self.__MatchOverscanMode, None)
            self.AddMatchString(re.compile(b'SsavM(0|1|2)\r\n'), self.__MatchScreenSaverMode, None)
            self.AddMatchString(re.compile(b'SsavS(0|1)\r\n'), self.__MatchScreenSaverStatus, None)
            self.AddMatchString(re.compile(b'Host(0|1|2) VSend(0|1) CommOut[0|1] CommIn[0|1] pcPlaybackIn[0|1] USBStd[0-3]\r\n'), self.__MatchUSBHostStatus, None)
            self.AddMatchString(re.compile(b'Otyp1\*(1|2)\r\n'), self.__MatchUSBStreamingFormat, None)
            self.AddMatchString(re.compile(b'UsbcC(1|2)\r\n'), self.__MatchUSBTerminalType, None)
            self.AddMatchString(re.compile(b'Vmt(0|1|2) (0|1|2)\r\n'), self.__MatchVideoMute, None)
            self.AddMatchString(re.compile(b'In00 (0|1)\r\n'), self.__MatchVideoSignalPresence, None)
            self.AddMatchString(re.compile(b'GrpmD(1|3|5|7|9)\*(0|-[0-9]{1,4})\r\n'), self.__MatchVolume, None)
            self.AddMatchString(re.compile(b'Vrb3\r\n'), self.__MatchVerboseMode, None)

            self.AddMatchString(re.compile(b'E(\d+)\r\n'), self.__MatchError, None)

            self.AddMatchString(re.compile(b'Password:'), self.__MatchPassword, None)

            self.AddMatchString(re.compile(b'Login Administrator\r\n'), self.__MatchLoginAdmin, None)

            self.AddMatchString(re.compile(b'Login User\r\n'), self.__MatchLoginUser, None)


    def SetPassword(self, value, qualifier):
        if self.devicePassword is not None:
            self.Send('{0}\r\n'.format(self.devicePassword))
        else:
            self.MissingCredentialsLog('Password')


    def __MatchPassword(self, match, tag):
        self.PasswdPromptCount += 1
        if self.PasswdPromptCount > 2:
            print('Log in failed. Please supply proper Admin password')
            self.Authenticated = 'None'
        else:
            self.SetPassword(None,None)

    def __MatchLoginAdmin(self, match, tag):

        self.Authenticated = 'Admin'
        self.PasswdPromptCount = 0

    def __MatchLoginUser(self, match, tag):

        self.Authenticated = 'User'
        self.PasswdPromptCount = 0
        print('Logged in as User. May have limited functionality.')

    def SetVerbose(self, value, qualifier):
        self.Send('w3cv\r\n')

    def __MatchVerboseMode(self, match, qualifier):
        self.OnConnected()
        self.VerboseEnabled = False

    def SetAspectRatio(self, value, qualifier):

        ValueStateValues = {
            'Fill': 'w1*1ASPR\r',
            'Follow': 'w1*2ASPR\r'
        }

        AspectRatioCmdString = ValueStateValues[value]
        self.__SetHelper('AspectRatio', AspectRatioCmdString, value, qualifier)

    def UpdateAspectRatio(self, value, qualifier):

        AspectRatioCmdString = 'w1ASPR\r'
        self.__UpdateHelper('AspectRatio', AspectRatioCmdString, value, qualifier)

    def __MatchAspectRatio(self, match, tag):

        ValueStateValues = {
            '1': 'Fill',
            '2': 'Follow'
        }

        value = ValueStateValues[match.group(1).decode()]
        self.WriteStatus('AspectRatio', value, None)

    def SetAudioMute(self, value, qualifier):

        GroupStates = {
            'Program': '2',
            'Mic to Far End': '4',
            'Program to Far End': '6',
            'Far End to Ref': '8',
            'Mic to Aux': '10'
        }

        ValueStateValues = {
            'On': 1,
            'Off': 0
        }

        AudioMuteCmdString = 'wD{0}*{1}GRPM\r'.format(GroupStates[qualifier['Group']], ValueStateValues[value])
        self.__SetHelper('AudioMute', AudioMuteCmdString, value, qualifier)

    def UpdateAudioMute(self, value, qualifier):

        GroupStates = {
            'Program': '2',
            'Mic to Far End': '4',
            'Program to Far End': '6',
            'Far End to Ref': '8',
            'Mic to Aux': '10'
        }

        AudioMuteCmdString = 'wD{0}GRPM\r'.format(GroupStates[qualifier['Group']])
        self.__UpdateHelper('AudioMute', AudioMuteCmdString, value, qualifier)

    def __MatchAudioMute(self, match, tag):

        GroupStates = {
            '2': 'Program',
            '4': 'Mic to Far End',
            '6': 'Program to Far End',
            '8': 'Far End to Ref',
            '10': 'Mic to Aux'
        }

        ValueStateValues = {
            '1': 'On',
            '0': 'Off'
        }

        qualifier = {}
        qualifier['Group'] = GroupStates[match.group(1).decode()]
        value = ValueStateValues[match.group(2).decode()]
        self.WriteStatus('AudioMute', value, qualifier)

    def SetAutoImage(self, value, qualifier):

        ValueStateValues = {
            'Execute': 'A',
            'Execute and Fill': '1*A',
            'Execute and Follow': '2*A'
        }

        AutoImageCmdString = ValueStateValues[value]
        self.__SetHelper('AutoImage', AutoImageCmdString, value, qualifier)

    def SetAutoMemory(self, value, qualifier):

        ValueStateValues = {
            'On': 'w1*1AMEM\r',
            'Off': 'w1*0AMEM\r'
        }

        AutoMemoryCmdString = ValueStateValues[value]
        self.__SetHelper('AutoMemory', AutoMemoryCmdString, value, qualifier)

    def UpdateAutoMemory(self, value, qualifier):

        AutoMemoryCmdString = 'w1AMEM\r'
        self.__UpdateHelper('AutoMemory', AutoMemoryCmdString, value, qualifier)

    def __MatchAutoMemory(self, match, tag):

        ValueStateValues = {
            '1': 'On',
            '0': 'Off'
        }

        value = ValueStateValues[match.group(1).decode()]
        self.WriteStatus('AutoMemory', value, None)

    def SetExecutiveMode(self, value, qualifier):

        ValueStateValues = {
            'On': '1X',
            'Off': '0X'
        }

        ExecutiveModeCmdString = ValueStateValues[value]
        self.__SetHelper('ExecutiveMode', ExecutiveModeCmdString, value, qualifier)

    def UpdateExecutiveMode(self, value, qualifier):

        ExecutiveModeCmdString = 'X'
        self.__UpdateHelper('ExecutiveMode', ExecutiveModeCmdString, value, qualifier)

    def __MatchExecutiveMode(self, match, tag):

        ValueStateValues = {
            '1': 'On',
            '0': 'Off'
        }

        value = ValueStateValues[match.group(1).decode()]
        self.WriteStatus('ExecutiveMode', value, None)

    def SetFreeze(self, value, qualifier):

        ValueStateValues = {
            'On': '1F',
            'Off': '0F'
        }

        FreezeCmdString = ValueStateValues[value]
        self.__SetHelper('Freeze', FreezeCmdString, value, qualifier)

    def UpdateFreeze(self, value, qualifier):

        FreezeCmdString = 'F'
        self.__UpdateHelper('Freeze', FreezeCmdString, value, qualifier)

    def __MatchFreeze(self, match, tag):

        ValueStateValues = {
            '1': 'On',
            '0': 'Off'
        }

        value = ValueStateValues[match.group(1).decode()]
        self.WriteStatus('Freeze', value, None)

    def SetDigitalInputMode(self, value, qualifier):

        ValueStateValues = {
            'Default Off': '0',
            'Push to Mute': '1',
            'Push to Talk': '2',
            'Mic Mute 1': '3',
            'Mic Mute 2': '4',
            'Mic Mute 3': '5',
            'Mic Mute 4': '6',
            'Inc Group Master 1': '7',
            'Dec Group Master 1': '8',
            'Preset Toggle 1': '9',
            'Preset Toggle 2': '10'
        }

        InputValues = {
            '1': '1',
            '2': '2'
        }

        DigitalInputModeCmdString = 'w{0}*{1}GPIT\r'.format(InputValues[qualifier['Input']], ValueStateValues[value])
        self.__SetHelper('DigitalInputMode', DigitalInputModeCmdString, value, qualifier)

    def UpdateDigitalInputMode(self, value, qualifier):

        DigitalInputModeCmdString = 'w{0}GPIT\r'.format(qualifier['Input'])
        self.__UpdateHelper('DigitalInputMode', DigitalInputModeCmdString, value, qualifier)

    def __MatchDigitalInputMode(self, match, tag):

        InputStates = {
            '1': '1',
            '2': '2'
        }

        ValueStateValues = {
            '0': 'Default Off',
            '1': 'Push to Mute',
            '2': 'Push to Talk',
            '3': 'Mic Mute 1',
            '4': 'Mic Mute 2',
            '5': 'Mic Mute 3',
            '6': 'Mic Mute 4',
            '7': 'Inc Group Master 1',
            '8': 'Dec Group Master 1',
            '9': 'Preset Toggle 1',
            '10': 'Preset Toggle 2'
        }

        qualifier = {}
        qualifier['Input'] = InputStates[match.group(1).decode()]
        value = ValueStateValues[match.group(2).decode()]
        self.WriteStatus('DigitalInputMode', value, qualifier)

    def UpdateDigitalInputStatus(self, value, qualifier):

        InputValues = {
            '1': '1',
            '2': '2'
        }

        DigitalInputStatusCmdString = 'w{0}GPI\r'.format(InputValues[qualifier['Input']])
        self.__UpdateHelper('DigitalInputStatus', DigitalInputStatusCmdString, value, qualifier)

    def __MatchDigitalInputStatus(self, match, tag):

        InputStates = {
            '1': '1',
            '2': '2'
        }

        ValueStateValues = {
            '1': 'High',
            '0': 'Low'
        }

        qualifier = {}
        qualifier['Input'] = InputStates[match.group(1).decode()]
        value = ValueStateValues[match.group(2).decode()]
        self.WriteStatus('DigitalInputStatus', value, qualifier)

    def SetDigitalOutputMode(self, value, qualifier):

        OutputStates = {
            '1': '1',
            '2': '2'
        }

        ValueStateValues = {
            'Output High': '0',
            'Output Low': '1',
            'Follow Mute': '2',
            'Follow Mute Inverted': '3',
            'Blink, Follow Input 1': '4',
            'Blink, Follow Input 2': '5'
        }

        DigitalOutputModeCmdString = 'w{0}*{1}GPOT\r'.format(qualifier['Output'], ValueStateValues[value])
        self.__SetHelper('DigitalOutputMode', DigitalOutputModeCmdString, value, qualifier)

    def UpdateDigitalOutputMode(self, value, qualifier):

        DigitalOutputModeCmdString = 'w{0}GPOT\r'.format(qualifier['Output'])
        self.__UpdateHelper('DigitalOutputMode', DigitalOutputModeCmdString, value, qualifier)

    def __MatchDigitalOutputMode(self, match, tag):

        OutputStates = {
            '1': '1',
            '2': '2'
        }

        ValueStateValues = {
            '0': 'Output High',
            '1': 'Output Low',
            '2': 'Follow Mute',
            '3': 'Follow Mute Inverted',
            '4': 'Blink, Follow Input 1',
            '5': 'Blink, Follow Input 2'
        }

        qualifier = {}
        qualifier['Output'] = OutputStates[match.group(1).decode()]
        value = ValueStateValues[match.group(2).decode()]
        self.WriteStatus('DigitalOutputMode', value, qualifier)

    def SetHDCPAuthentication(self, value, qualifier):

        ValueStateValues = {
            'On': 'wE1*1HDCP\r',
            'Off': 'wE1*0HDCP\r'
        }

        HDCPAuthenticationCmdString = ValueStateValues[value]
        self.__SetHelper('HDCPAuthentication', HDCPAuthenticationCmdString, value, qualifier)

    def UpdateHDCPAuthentication(self, value, qualifier):

        HDCPAuthenticationCmdString = 'wE1HDCP\r'
        self.__UpdateHelper('HDCPAuthentication', HDCPAuthenticationCmdString, value, qualifier)

    def __MatchHDCPAuthentication(self, match, tag):

        ValueStateValues = {
            '1': 'On',
            '0': 'Off'
        }

        value = ValueStateValues[match.group(1).decode()]
        self.WriteStatus('HDCPAuthentication', value, None)

    def SetHDCPMode(self, value, qualifier):

        ValueStateValues = {
            'Mode 1': 'wS0HDCP\r',
            'Mode 2': 'wS1HDCP\r',
            'Mode 3': 'wS2HDCP\r',
            'Mode 4': 'wS3HDCP\r'
        }

        HDCPModeCmdString = ValueStateValues[value]
        self.__SetHelper('HDCPMode', HDCPModeCmdString, value, qualifier)

    def UpdateHDCPMode(self, value, qualifier):

        HDCPModeCmdString = 'wSHDCP\r'
        self.__UpdateHelper('HDCPMode', HDCPModeCmdString, value, qualifier)

    def __MatchHDCPMode(self, match, tag):

        ValueStateValues = {
            '0': 'Mode 1',
            '1': 'Mode 2',
            '2': 'Mode 3',
            '3': 'Mode 4'
        }

        value = ValueStateValues[match.group(1).decode()]
        self.WriteStatus('HDCPMode', value, None)

    def SetHDCPNotification(self, value, qualifier):

        ValueStateValues = {
            'On': 'wN1HDCP\r',
            'Off': 'wN0HDCP\r'
        }

        HDCPNotificationCmdString = ValueStateValues[value]
        self.__SetHelper('HDCPNotification', HDCPNotificationCmdString, value, qualifier)

    def UpdateHDCPNotification(self, value, qualifier):

        HDCPNotificationCmdString = 'wNHDCP\r'
        self.__UpdateHelper('HDCPNotification', HDCPNotificationCmdString, value, qualifier)

    def __MatchHDCPNotification(self, match, tag):

        ValueStateValues = {
            '1': 'On',
            '0': 'Off'
        }

        value = ValueStateValues[match.group(1).decode()]
        self.WriteStatus('HDCPNotification', value, None)

    def SetHDMIInputEDID(self, value, qualifier):

        ValueStateValues = {
            '640x480 60Hz': '10', '800x600 60Hz': '11', '1024x768 60Hz': '12',
            '1280x768 60Hz': '13', '1280x800 60Hz': '14', '1280x1024 60Hz': '15',
            '1360x768 60Hz': '16', '1366x768 60Hz': '17', '1440x900 60Hz': '18',
            '1400x1050 60Hz': '19', '1600x900 60Hz': '20', '1680x1050 60Hz': '21',
            '1600x1200 60Hz': '22', '1920x1200 60Hz': '23', '480p 59.94Hz': '24',
            '480p 60Hz': '25', '576p 50Hz': '26', '720p 23.98Hz': '27',
            '720p 24Hz': '28', '720p 25Hz': '29', '720p 29.97Hz': '30',
            '720p 30Hz': '31', '720p 50Hz': '32', '720p 59.94Hz': '33',
            '720p 60Hz': '34', '1080i 50Hz': '35', '1080i 59.94Hz': '36',
            '1080i 60Hz': '37', '1080p 23.98Hz': '38', '1080p 24Hz': '39',
            '1080p 25Hz': '40', '1080p 29.97Hz': '41', '1080p 30Hz': '42',
            '1080p 50Hz': '43', '1080p 59.94Hz': '44', '1080p 60Hz': '45',
            '2048x1080 23.98Hz': '46', '2048x1080 24Hz': '47', '2048x1080 25Hz': '48',
            '2048x1080 29.97Hz': '49', '2048x1080 30Hz': '50', '2048x1080 50Hz': '51',
            '2048x1080 59.94Hz': '52', '2048x1080 60Hz': '53'
        }

        HDMIInputEDIDCmdString = 'wA1*{0}EDID\r'.format(ValueStateValues[value])
        self.__SetHelper('HDMIInputEDID', HDMIInputEDIDCmdString, value, qualifier)

    def UpdateHDMIInputEDID(self, value, qualifier):

        HDMIInputEDIDCmdString = 'wA1EDID\r'
        self.__UpdateHelper('HDMIInputEDID', HDMIInputEDIDCmdString, value, qualifier)

    def __MatchHDMIInputEDID(self, match, tag):

        ValueStateValues = {
            '10': '640x480 60Hz', '11': '800x600 60Hz', '12': '1024x768 60Hz',
            '13': '1280x768 60Hz', '14': '1280x800 60Hz', '15': '1280x1024 60Hz',
            '16': '1360x768 60Hz', '17': '1366x768 60Hz', '18': '1440x900 60Hz',
            '19': '1400x1050 60Hz', '20': '1600x900 60Hz', '21': '1680x1050 60Hz',
            '22': '1600x1200 60Hz', '23': '1920x1200 60Hz', '24': '480p 59.94Hz',
            '25': '480p 60Hz', '26': '576p 50Hz', '27': '720p 23.98Hz',
            '28': '720p 24Hz', '29': '720p 25Hz', '30': '720p 29.97Hz',
            '31': '720p 30Hz', '32': '720p 50Hz', '33': '720p 59.94Hz',
            '34': '720p 60Hz', '35': '1080i 50Hz', '36': '1080i 59.94Hz',
            '37': '1080i 60Hz', '38': '1080p 23.98Hz', '39': '1080p 24Hz',
            '40': '1080p 25Hz', '41': '1080p 29.97Hz', '42': '1080p 30Hz',
            '43': '1080p 50Hz', '44': '1080p 59.94Hz', '45': '1080p 60Hz',
            '46': '2048x1080 23.98Hz', '47': '2048x1080 24Hz', '48': '2048x1080 25Hz',
            '49': '2048x1080 29.97Hz', '50': '2048x1080 30Hz', '51': '2048x1080 50Hz',
            '52': '2048x1080 59.94Hz', '53': '2048x1080 60Hz'
        }

        value = ValueStateValues[match.group(1).decode()]
        self.WriteStatus('HDMIInputEDID', value, None)

    def SetHDMILoopFormat(self, value, qualifier):

        ValueStateValues = {
            'Auto': '0',
            'DVI RGB 444': '1',
            'RGB 444 Full': '2',
            'RGB 444 Limited': '3',
            'YUV 444 Full': '4',
            'YUV 444 Limited': '5',
            'YUV 422 Full': '6',
            'YUV 422 Limited': '7'
        }

        HDMILoopFormatCmdString = 'w2*{0}VTPO\r'.format(ValueStateValues[value])
        self.__SetHelper('HDMILoopFormat', HDMILoopFormatCmdString, value, qualifier)

    def UpdateHDMILoopFormat(self, value, qualifier):

        HDMILoopFormatCmdString = 'w2VTPO\r'
        self.__UpdateHelper('HDMILoopFormat', HDMILoopFormatCmdString, value, qualifier)

    def __MatchHDMILoopFormat(self, match, tag):

        ValueStateValues = {
            '0': 'Auto',
            '1': 'DVI RGB 444',
            '2': 'RGB 444 Full',
            '3': 'RGB 444 Limited',
            '4': 'YUV 444 Full',
            '5': 'YUV 444 Limited',
            '6': 'YUV 422 Full',
            '7': 'YUV 422 Limited'
        }

        value = ValueStateValues[match.group(1).decode()]
        self.WriteStatus('HDMILoopFormat', value, None)

    def SetOverscanMode(self, value, qualifier):

        ValueStateValues = {
            '0%': 'w1*0OSCN\r',
            '2.5%': 'w1*1OSCN\r',
            '5%': 'w1*2OSCN\r'
        }

        OverscanModeCmdString = ValueStateValues[value]
        self.__SetHelper('OverscanMode', OverscanModeCmdString, value, qualifier)

    def UpdateOverscanMode(self, value, qualifier):

        OverscanModeCmdString = 'w1OSCN\r'
        self.__UpdateHelper('OverscanMode', OverscanModeCmdString, value, qualifier)

    def __MatchOverscanMode(self, match, tag):

        ValueStateValues = {
            '0': '0%',
            '1': '2.5%',
            '2': '5%'
        }

        value = ValueStateValues[match.group(1).decode()]
        self.WriteStatus('OverscanMode', value, None)

    def SetPreset(self, value, qualifier):

        PresetStates = {
            '1': '1',
            '2': '2',
            '3': '3',
            '4': '4',
            '5': '5',
            '6': '6',
            '7': '7',
            '8': '8',
            '9': '9',
            '10': '10',
            '11': '11',
            '12': '12',
            '13': '13',
            '14': '14',
            '15': '15',
            '16': '16'
        }

        ValueStateValues = {
            'Save': ',',
            'Recall': '.'
        }

        if value == 'Delete':
            PresetCmdString = 'wX2*{0:03d}PRST\r'.format(int(qualifier['Preset']))
        else:
            PresetCmdString = '2*{0:03d}{1}'.format(int(qualifier['Preset']), ValueStateValues[value])
        self.__SetHelper('Preset', PresetCmdString, value, qualifier)

    def SetScreenSaverMode(self, value, qualifier):

        ValueStateValues = {
            'Extron Logo': '0',
            'User Logo': '1',
            'Blue Screen or Bug': '2'
        }

        ScreenSaverModeCmdString = 'wM{0}SSAV\r'.format(ValueStateValues[value])
        self.__SetHelper('ScreenSaverMode', ScreenSaverModeCmdString, value, qualifier)

    def UpdateScreenSaverMode(self, value, qualifier):

        ScreenSaverModeCmdString = 'wMSSAV\r'
        self.__UpdateHelper('ScreenSaverMode', ScreenSaverModeCmdString, value, qualifier)

    def __MatchScreenSaverMode(self, match, tag):

        ValueStateValues = {
            '0': 'Extron Logo',
            '1': 'User Logo',
            '2': 'Blue Screen or Bug'
        }

        value = ValueStateValues[match.group(1).decode()]
        self.WriteStatus('ScreenSaverMode', value, None)

    def UpdateScreenSaverStatus(self, value, qualifier):

        ScreenSaverStatusCmdString = 'wSSSAV\r'
        self.__UpdateHelper('ScreenSaverStatus', ScreenSaverStatusCmdString, value, qualifier)

    def __MatchScreenSaverStatus(self, match, tag):

        ValueStateValues = {
            '1': 'On',
            '0': 'Off'
        }

        value = ValueStateValues[match.group(1).decode()]
        self.WriteStatus('ScreenSaverStatus', value, None)

    def UpdateVideoSendStatus(self, value, qualifier):
        self.UpdateUSBHostStatus(value, qualifier)

    def UpdateUSBHostStatus(self, value, qualifier):

        USBHostStatusCmdString = '35I\r'
        self.__UpdateHelper('USBHostStatus', USBHostStatusCmdString, value, qualifier)

    def __MatchUSBHostStatus(self, match, tag):

        UsbStateValues = {
            '0': 'Not Present',
            '1': 'Present',
            '2': 'Suspended'
        }

        VideoSendStateValues = {
            '1': 'On',
            '0': 'Off'
        }

        value = UsbStateValues[match.group(1).decode()]
        self.WriteStatus('USBHostStatus', value, None)

        value = VideoSendStateValues[match.group(2).decode()]
        self.WriteStatus('VideoSendStatus', value, None)

    def SetUSBStreamingFormat(self, value, qualifier):

        ValueStateValues = {
            'MJPEG 422 Full': '1',
            'MJPEG 420 Full': '2'
        }

        USBStreamingFormatCmdString = 'w1*{0}OTYP\r'.format(ValueStateValues[value])
        self.__SetHelper('USBStreamingFormat', USBStreamingFormatCmdString, value, qualifier)

    def UpdateUSBStreamingFormat(self, value, qualifier):

        USBStreamingFormatCmdString = 'w1OTYP\r'
        self.__UpdateHelper('USBStreamingFormat', USBStreamingFormatCmdString, value, qualifier)

    def __MatchUSBStreamingFormat(self, match, tag):

        ValueStateValues = {
            '1': 'MJPEG 422 Full',
            '2': 'MJPEG 420 Full'
        }

        value = ValueStateValues[match.group(1).decode()]
        self.WriteStatus('USBStreamingFormat', value, None)

    def SetUSBTerminalType(self, value, qualifier):

        ValueStateValues = {
            'Default': '1',
            'Echo Cancelling Speakerphone': '2'
        }

        USBTerminalTypeCmdString = 'wC{0}USBC\r'.format(ValueStateValues[value])
        self.__SetHelper('USBTerminalType', USBTerminalTypeCmdString, value, qualifier)

    def UpdateUSBTerminalType(self, value, qualifier):

        USBTerminalTypeCmdString = 'wCUSBC\r'
        self.__UpdateHelper('USBTerminalType', USBTerminalTypeCmdString, value, qualifier)

    def __MatchUSBTerminalType(self, match, tag):

        ValueStateValues = {
            '1': 'Default',
            '2': 'Echo Cancelling Speakerphone'
        }

        value = ValueStateValues[match.group(1).decode()]
        self.WriteStatus('USBTerminalType', value, None)

    def SetVideoMute(self, value, qualifier):

        OutputStates = {
            'USB': '1',
            'HDMI Loop': '2'
        }

        ValueStateValues = {
            'Mute Video to Black': '1B',
            'Mute Sync and Video': '2B',
            'Unmute Video/Sync': '0B'
        }

        if (OutputStates[qualifier['Output']] == '1') & (ValueStateValues[value] == '2B'):
            print('Invalid Command for SetVideoMute')
        else:
            VideoMuteCmdString = '{0}*{1}'.format(OutputStates[qualifier['Output']], ValueStateValues[value])
            self.__SetHelper('VideoMute', VideoMuteCmdString, value, qualifier)

    def UpdateVideoMute(self, value, qualifier):

        VideoMuteCmdString = 'B'
        self.__UpdateHelper('VideoMute', VideoMuteCmdString, value, qualifier)

    def __MatchVideoMute(self, match, tag):

        OutputStates = {
            '1': 'USB',
            '2': 'HDMI Loop'
        }

        ValueStateValues = {
            '1': 'Mute Video to Black',
            '2': 'Mute Sync and Video',
            '0': 'Unmute Video/Sync'
        }

        qualifier = {}
        qualifier2 = {}
        qualifier = {'Output': 'USB'}
        qualifier2 = {'Output': 'HDMI Loop'}
        value = ValueStateValues[match.group(1).decode()]
        value2 = ValueStateValues[match.group(2).decode()]
        self.WriteStatus('VideoMute', value, qualifier)
        self.WriteStatus('VideoMute', value2, qualifier2)

    def UpdateVideoSignalPresence(self, value, qualifier):

        VideoSignalPresenceCmdString = 'w0LS\r'
        self.__UpdateHelper('VideoSignalPresence', VideoSignalPresenceCmdString, value, qualifier)

    def __MatchVideoSignalPresence(self, match, tag):

        ValueStateValues = {
            '1': 'Signal',
            '0': 'No Signal'
        }

        value = ValueStateValues[match.group(1).decode()]
        self.WriteStatus('VideoSignalPresence', value, None)

    def SetVolume(self, value, qualifier):

        GroupStates = {
            'Program': '1',
            'Mic to Far End': '3',
            'Program to Far End': '5',
            'Far End to Ref': '7',
            'Mic to Aux': '9'
        }

        ValueConstraints = {
            'Min': -100,
            'Max': 0
        }

        if ValueConstraints['Min'] <= value <= ValueConstraints['Max']:
            VolumeCmdString = 'wD{0}*{1}GRPM\r'.format(GroupStates[qualifier['Group']], int(value * 10))
            self.__SetHelper('Volume', VolumeCmdString, value, qualifier)
        else:
            print('Invalid Command for SetVolume')

    def UpdateVolume(self, value, qualifier):

        GroupStates = {
            'Program': '1',
            'Mic to Far End': '3',
            'Program to Far End': '5',
            'Far End to Ref': '7',
            'Mic to Aux': '9'
        }

        VolumeCmdString = 'wD{0}GRPM\r'.format(GroupStates[qualifier['Group']])
        self.__UpdateHelper('Volume', VolumeCmdString, value, qualifier)

    def __MatchVolume(self, match, tag):

        GroupStates = {
            '1': 'Program',
            '3': 'Mic to Far End',
            '5': 'Program to Far End',
            '7': 'Far End to Ref',
            '9': 'Mic to Aux'
        }

        qualifier = {}
        qualifier['Group'] = GroupStates[match.group(1).decode()]
        value = int(match.group(2).decode()) / 10
        self.WriteStatus('Volume', value, qualifier)

    def __SetHelper(self, command, commandstring, value, qualifier):
        self.Debug = True
        if self.VerboseEnabled:
            @Wait(1)
            def SendVerbose():
                self.Send('w3cv\r\n')
                self.Send(commandstring)
        else:
            self.Send(commandstring)

    def __UpdateHelper(self, command, commandstring, value, qualifier):
        
        if self.initializationChk:
            self.OnConnected()
            self.initializationChk = False

        self.counter = self.counter + 1
        if self.counter > self.connectionCounter and self.connectionFlag:
            self.OnDisconnected()

        if self.Authenticated in ['User', 'Admin', 'Not Needed']:
            if self.Unidirectional == 'True':
                print('Inappropriate Command ', command)
            else:
                if self.VerboseEnabled:
                    @Wait(1)
                    def SendVerbose():
                        self.Send('w3cv\r\n')
                        self.Send(commandstring)
                else:
                    self.Send(commandstring)
        else:
            print('Inappropriate Command ', command)

    def __MatchError(self, match, tag):

        DEVICE_ERROR_CODES = {
            '01': 'Invalid Input Number',
            '10': 'Invalid Command',
            '11': 'Invalid Preset Number',
            '12': 'Invalid port or output number',
            '13': 'Invalid Parameter',
            '14': 'Illegal Command for this Configuration',
            '17': 'Invalid Command for this Signal Type',
            '22': 'Busy',
            '24': 'Privilege Violation',
            '25': 'Device Not Present',
            '26': 'Maximum Number of Connections Exceeded',
            '28': 'Bad Filename/File Not Found',
            '33': 'Bad File Type or Size'
        }

        value = match.group(1).decode()
        if value in DEVICE_ERROR_CODES:
            print(DEVICE_ERROR_CODES[value])
        else:
            self.Error(['Unrecognize error code: ' + match.group(0).decode()])

    def OnConnected(self):
        self.connectionFlag = True
        self.WriteStatus('ConnectionStatus', 'Connected')
        self.counter = 0


    def OnDisconnected(self):
        self.WriteStatus('ConnectionStatus', 'Disconnected')
        self.connectionFlag = False
        self.Authenticated = 'Not Needed'
        self.PasswdPromptCount = 0
        self.VerboseEnabled = False

    ######################################################
    # RECOMMENDED not to modify the code below this point
    ######################################################
    # Send Control Commands
    def Set(self, command, value, qualifier=None):
        method = 'Set%s' % command
        if hasattr(self, method) and callable(getattr(self, method)):
            getattr(self, method)(value, qualifier)
        else:
            print(command, 'does not support Set.')
    # Send Update Commands

    def Update(self, command, qualifier=None):
        method = 'Update%s' % command
        if hasattr(self, method) and callable(getattr(self, method)):
            getattr(self, method)(None, qualifier)
        else:
            print(command, 'does not support Update.')

    # This method is to tie an specific command with a parameter to a call back method
    # when its value is updated. It sets how often the command will be query, if the command
    # have the update method.
    # If the command doesn't have the update feature then that command is only used for feedback
    def SubscribeStatus(self, command, qualifier, callback):
        Command = self.Commands.get(command)
        if Command:
            if command not in self.Subscription:
                self.Subscription[command] = {'method': {}}

            Subscribe = self.Subscription[command]
            Method = Subscribe['method']

            if qualifier:
                for Parameter in Command['Parameters']:
                    try:
                        Method = Method[qualifier[Parameter]]
                    except:
                        if Parameter in qualifier:
                            Method[qualifier[Parameter]] = {}
                            Method = Method[qualifier[Parameter]]
                        else:
                            return

            Method['callback'] = callback
            Method['qualifier'] = qualifier
        else:
            print(command, 'does not exist in the module')

    # This method is to check the command with new status have a callback method then trigger the callback
    def NewStatus(self, command, value, qualifier):
        if command in self.Subscription:
            Subscribe = self.Subscription[command]
            Method = Subscribe['method']
            Command = self.Commands[command]
            if qualifier:
                for Parameter in Command['Parameters']:
                    try:
                        Method = Method[qualifier[Parameter]]
                    except:
                        break
            if 'callback' in Method and Method['callback']:
                Method['callback'](command, value, qualifier)

    # Save new status to the command
    def WriteStatus(self, command, value, qualifier=None):
        self.counter = 0
        if not self.connectionFlag:
            self.OnConnected()
        Command = self.Commands[command]
        Status = Command['Status']
        if qualifier:
            for Parameter in Command['Parameters']:
                try:
                    Status = Status[qualifier[Parameter]]
                except KeyError:
                    if Parameter in qualifier:
                        Status[qualifier[Parameter]] = {}
                        Status = Status[qualifier[Parameter]]
                    else:
                        return
        try:
            #if Status['Live'] != value:
            #    Status['Live'] = value
            self.NewStatus(command, value, qualifier)
        except:
            Status['Live'] = value
            self.NewStatus(command, value, qualifier)

    # Read the value from a command.
    def ReadStatus(self, command, qualifier=None):
        Command = self.Commands[command]
        Status = Command['Status']
        if qualifier:
            for Parameter in Command['Parameters']:
                try:
                    Status = Status[qualifier[Parameter]]
                except KeyError:
                    return None
        try:
            return Status['Live']
        except:
            return None

    def __ReceiveData(self, interface, data):
        # handling incoming unsolicited data
        self._ReceiveBuffer += data
        # check incoming data if it matched any expected data from device module
        if self.CheckMatchedString() and len(self._ReceiveBuffer) > 10000:
            self._ReceiveBuffer = b''

    # Add regular expression so that it can be check on incoming data from device.
    def AddMatchString(self, regex_string, callback, arg):
        if regex_string not in self._compile_list:
            self._compile_list[regex_string] = {'callback': callback, 'para': arg}

    # Check incoming unsolicited data to see if it was matched with device expectancy.
    def CheckMatchedString(self):
        for regexString in self._compile_list:
            while True:
                result = re.search(regexString, self._ReceiveBuffer)
                if result:
                    self._compile_list[regexString]['callback'](result, self._compile_list[regexString]['para'])
                    self._ReceiveBuffer = self._ReceiveBuffer.replace(result.group(0), b'')
                else:
                    break
        return True


class SerialClass(SerialInterface, DeviceClass):

    def __init__(self, Host, Port, Baud=9600, Data=8, Parity='None', Stop=1, FlowControl='Off', CharDelay=0, Model=None):
        SerialInterface.__init__(self, Host, Port, Baud, Data, Parity, Stop, FlowControl, CharDelay)
        self.ConnectionType = 'Serial'
        DeviceClass.__init__(self)
        # Check if Model belongs to a subclass
        if len(self.Models) > 0:
            if Model not in self.Models:
                print('Model mismatch')
            else:
                self.Models[Model]()


class EthernetClass(EthernetClientInterface, DeviceClass):

    def __init__(self, Hostname, IPPort, Protocol='TCP', ServicePort=0, Model=None):
        EthernetClientInterface.__init__(self, Hostname, IPPort, Protocol, ServicePort)
        self.ConnectionType = 'Ethernet'
        DeviceClass.__init__(self)
        # Check if Model belongs to a subclass
        if len(self.Models) > 0:
            if Model not in self.Models:
                print('Model mismatch')
            else:
                self.Models[Model]()
