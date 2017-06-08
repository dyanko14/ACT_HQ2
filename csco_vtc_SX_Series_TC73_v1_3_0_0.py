from extronlib.interface import SerialInterface, EthernetClientInterface
from re import compile, findall, search
from extronlib.system import Wait, ProgramLog


class DeviceClass:
    def __init__(self):

        self.Unidirectional = 'False'
        self.connectionCounter = 15
        self.DefaultResponseTimeout = 0.3
        self._Compile_List = {}
        self.Subscription = {}
        self.ReceiveData = self.__ReceiveData
        self._ReceiveBuffer = b''
        self.counter = 0
        self.connectionFlag = True
        self.initializationChk = True

        self.deviceUsername = 'admin'
        self.devicePassword = 'TANDBERG'
        self._CallHistoryOccurrenceType = 'Time'
        self._NumberofPhonebookSearch = 5
        self._NumberofPhonebookFolderSearch = 5
        self._NumberofCallHistory = 5
        self._NumberOfContactsPerSearch = 50
        self._NumberOfFoldersPerSearch = 50

        self.Models = {
            'SX20 TC7.3.X': self.csco_12_2083_SX20,
            'SX80 TC7.3.X': self.csco_12_2083_SX80,
        }

        self.Commands = {
            'ConnectionStatus': {'Status': {}},
            'AssignLocalOutput': {'Parameters': ['Layout ID', 'Output ID'], 'Status': {}},
            'AutoAnswer': {'Status': {}},
            'AudioVolumeMute': {'Status': {}},
            'CallSetupMode': {'Status': {}},
            'CallHistoryRefresh': {'Status': {}},
            'CallHistory': {'Parameters': ['Button', 'Detail Type'], 'Status': {}},
            'CallHistoryNavigation': {'Status': {}},
            'CallHistorySelect': {'Parameters': ['Button'], 'Status': {}},
            'CallStatus': {'Parameters': ['Call'], 'Status': {}},
            'CallStatusType': {'Parameters': ['Call'], 'Status': {}},
            'CameraFocus': {'Parameters': ['Camera'], 'Status': {}},
            'CameraPan': {'Parameters': ['Camera', 'Speed'], 'Status': {}},
            'CameraPresetPositionRecall': {'Parameters': ['Camera'], 'Status': {}},
            'CameraPresetRecall': {'Status': {}},
            'CameraPresetSave': {'Parameters': ['Camera'], 'Status': {}},
            'CameraPresetSaveSX20': {'Status': {}},
            'CameraPresetPositionRecallSX20': {'Status': {}},
            'CameraTilt': {'Parameters': ['Camera', 'Speed'], 'Status': {}},
            'CameraZoom': {'Parameters': ['Camera', 'Speed'], 'Status': {}},
            'CameraFocusSX20': {'Status': {}},
            'CameraPanSX20': {'Parameters': ['Speed'], 'Status': {}},
            'CameraTiltSX20': {'Parameters': ['Speed'], 'Status': {}},
            'CameraZoomSX20': {'Parameters': ['Speed'], 'Status': {}},
            'CloseMenu': {'Status': {}},
            'DisplayMode': {'Status': {}},
            'DisplayName': {'Parameters': ['Call'], 'Status': {}},
            'DoNotDisturb': {'Status': {}},
            'FarEndControl': {'Status': {}},
            'FarEndCameraPanTilt': {'Status': {}},
            'FarEndCameraPresetRecall': {'Status': {}},
            'FarEndCameraPresetSave': {'Status': {}},
            'FarEndCameraSource': {'Status': {}},
            'FarEndCameraZoom': {'Status': {}},
            'FirmwareVersion': {'Status': {}},
            'Hook': {'Parameters': ['Protocol', 'Number'], 'Status': {}},
            'InputSX20': {'Status': {}},
            'InputSX80': {'Status': {}},
            'InputLineLevel': {'Parameters': ['Input'], 'Status': {}},
            'InputMicLevel': {'Parameters': ['Input'], 'Status': {}},
            'InputMute': {'Parameters': ['Input'], 'Status': {}},
            'IREmulation': {'Status': {}},
            'Layout': {'Parameters': ['Layout ID'], 'Status': {}},
            'LayoutSet': {'Parameters': ['Target'], 'Status': {}},
            'MicrophonesMute': {'Status': {}},
            'OutputLevel': {'Parameters': ['Output'], 'Status': {}},
            'AudioOutput': {'Parameters': ['Output'], 'Status': {}},
            'PhonebookFolderIDNavigation': {'Status': {}},
            'PhonebookFolderIDSearchResult': {'Parameters': ['Button'], 'Status': {}},
            'PhonebookFolderIDSearchSet': {'Status': {}},
            'PhonebookFolderIDUpdate': {'Parameters': ['Phonebook Type'], 'Status': {}},
            'PhonebookNavigation': {'Parameters': ['Contact', 'FolderID', 'Phonebook Type', 'Phonebook Tag'],
                                    'Status': {}},
            'PhonebookSearch': {'Parameters': ['Phonebook Type'], 'Status': {}},
            'PhonebookSearchResult': {'Parameters': ['Button'], 'Status': {}},
            'PhonebookSearchSet': {'Status': {}},
            'PhonebookUpdate': {'Parameters': ['Contact', 'FolderID', 'Phonebook Type', 'Phonebook Tag'], 'Status': {}},
            'PictureInPicture': {'Status': {}},
            'Presentation': {'Status': {}},
            'PresentationMode': {'Status': {}},
            'PresentationSendingMode': {'Status': {}},
            'PresetRecall': {'Status': {}},
            'PresetSave': {'Status': {}},
            'Reboot': {'Status': {}},
            'RemoteNumber': {'Parameters': ['Call'], 'Status': {}},
            'SelfViewDefaultFullscreenMode': {'Status': {}},
            'SelfView': {'Status': {}},
            'SelfViewPosition': {'Status': {}},
            'SIPRegistrationStatus': {'Status': {}},
            'SleepTimer': {'Status': {}},
            'Standby': {'Status': {}},
            'Volume': {'Status': {}},
            'H323AliasE164Command': {'Status': {}},
            'H323AliasIDCommand': {'Status': {}},
            'H323AliasIDStatus': {'Status': {}},
            'H323GatekeeperAddressCommand': {'Status': {}},
            'H323GatekeeperStatus': {'Status': {}},
            'H323ProfileAuthenticationLoginNameCommand': {'Status': {}},
            'H323ProfileAuthenticationPasswordCommand': {'Status': {}},
            'H323GatekeeperAddress': {'Status': {}},
            'IPv4AddressCommand': {'Status': {}},
            'IPv4GatewayCommand': {'Status': {}},
            'IPv4SubnetMaskCommand': {'Status': {}},
            'DNSDomainName': {'Status': {}},
            'DNSDomainNameCommand': {'Status': {}},
            'DNSServerAddressCommand': {'Status': {}},
            'DNSServerAddress': {'Parameters': ['Server'], 'Status': {}},
            'GatewayAddress': {'Status': {}},
            'MACAddress': {'Status': {}},
            'NetworkAssignment': {'Status': {}},
            'IPAddress': {'Status': {}},
            'SubnetMask': {'Status': {}},
            'DTMF': {'Status': {}},
            'SpeakerTrackControl': {'Status': {}},
            'SpeakerTrackMode': {'Status': {}},
            'CameraSerialNumberRefresh': {'Status': {}},
            'SNCameraPresetSave': {'Parameters': ['Serial Number'], 'Status': {}},
            'SNCameraFocus': {'Parameters': ['Serial Number'], 'Status': {}},
            'SNCameraPan': {'Parameters': ['Serial Number', 'Speed'], 'Status': {}},
            'SNCameraTilt': {'Parameters': ['Serial Number', 'Speed'], 'Status': {}},
            'SNCameraZoom': {'Parameters': ['Serial Number', 'Speed'], 'Status': {}},
            'DefaultCallRate': {'Status': {}},
            'MaxReceiveCallRate': {'Status': {}},
            'MaxTotalReceiveCallRate': {'Status': {}},
            'MaxTotalTransmitCallRate': {'Status': {}},
            'MaxTransmitCallRate': {'Status': {}},
        }

        self.CallStatusRegEx = compile('\*s Call \d+ Status: (\w+)\r\n')
        self.CallStatusTypeRegEx = compile(
            '\*s Call \d+ CallType: (Video|Audio|AudioCanEscalate|ForwardAllCall|Unknown)\r\n')
        self.CSDisplayNameRegEx = compile('\*s Call \d+ DisplayName: "(.*)"\r\n')
        self.RemoteNumberRegEx = compile('\*s Call \d+ RemoteNumber: "(.*)"\r\n')

        self.CallIDRegEx = compile('\*s Call (\d+) Status: \w+\r\n')
        self.__LastCallStatus = 0
        self.__CallID = []

        self.DictIDList = {}
        self.SerialNumberID = compile('\*s Camera ([0-9]) SerialNumber: "(.+)"\r\n')
        self.SerialNumberIDList = []

        self.__UpdateTimer = 0
        self.MinLabel = 1
        self.MaxLabel = 0
        self.DirNameRegEx = compile('\*r ResultSet Contact (\d+) Name: "(.+)"\r\n')
        self.DirNumberRegEx = compile('\*r ResultSet Contact (\d+) ContactMethod 1 Number: "(.+)"')
        self.Offset = 0
        self.newList = {}
        self.folderList = {}

        self.FolderMin = 1
        self.FolderLimit = 0
        self.FolderNameRegEx = compile('\*r ResultSet Folder (\d+) Name: "(.+)"\r\n')
        self.FolderIDRegEx = compile('\*r ResultSet Folder (\d+) FolderId: "(.+)"')

        self.PrevCallHist = ''
        self.StartCallHist = 1
        self.CHDisplayNameRegEx = compile('Entry (\d+) DisplayName: "([^"]*)"\r\n')
        self.CallBackNumberRegEx = compile('Entry (\d+) CallbackNumber: "([^"]*)"\r\n')
        if self._CallHistoryOccurrenceType == 'Time':
            self.LastOccurrenceTimeRegEx = compile('Entry (\d+) LastOccurrenceStartTime: "([^"]*)"\r\n')
            self.OccurrenceCountRegEx = compile('Entry (\d+) OccurrenceCount: (\d+)\r\n')
        else:
            self.LastOccurrenceTimeRegEx = compile('Entry (\d+) StartTime: "([^"]*)"\r\n')
            self.OccurrenceCountRegEx = compile('Entry (\d+) Count: (\d+)\r\n')
        self.OccurrenceTypeRegEx = compile('Entry (\d+) OccurrenceType: (\w*)\r\n')
        self.AdvanceCallHist = True

        self.AddMatchString(compile(b'xstatus call\r\n\*\* end\r\n'), self.__MatchCallStatusIdle, None)
        self.AddMatchString(compile(b'\*s Call (\d+) Status: [\s\S]+\*\* end\r\n'), self.__MatchCallStatus, None)
        self.AddMatchString(compile(b'\*c xConfiguration Conference 1 AutoAnswer Mode: (Off|On)\r\n'),
                            self.__MatchAutoAnswer, None)
        self.AddMatchString(compile(b'\*s Audio VolumeMute: (Off|On)\r\n'), self.__MatchAudioVolumeMute, None)
        self.AddMatchString(compile(b'\*r CallHistoryRecentsResult [\s\S]+\*\* end\r\n'), self.__MatchCallHistory, None)
        self.AddMatchString(compile(b'\*c xConfiguration Video Monitors: (\w+)\r\n'), self.__MatchDisplayMode, None)
        self.AddMatchString(compile(b'\*s Conference DoNotDisturb: (Inactive|Active)\r\n'), self.__MatchDoNotDisturb,
                            None)
        self.AddMatchString(compile(b'\*c xConfiguration Conference 1 FarEndControl Mode: (Off|On)\r\n'),
                            self.__MatchFarEndControl, None)
        self.AddMatchString(compile(b'\*s SystemUnit Software Version: "([\w\.]+)"\r\n'), self.__MatchFirmwareVersion,
                            None)
        self.AddMatchString(compile(b'\*c xConfiguration Video MainVideoSource: ([1-5])\r\n'), self.__MatchInputSX20,
                            None)
        self.AddMatchString(compile(b'\*s Video Input MainVideoSource: ([1-5])\r\n'), self.__MatchInputSX80, None)
        self.AddMatchString(compile(b'\*c xConfiguration Audio Input (Line \d) Level: (\d+)\r\n'),
                            self.__MatchInputLineLevel, None)
        self.AddMatchString(compile(b'\*c xConfiguration Audio Input (Microphone \d) Level: (\d+)\r\n'),
                            self.__MatchInputMicLevel, None)
        self.AddMatchString(compile(b'\*c xConfiguration Audio Input ((Microphone|Line) \d) Mode: (On|Off)\r\n'),
                            self.__MatchInputMute, None)
        self.AddMatchString(compile(b'\*s Audio Microphones Mute: (Off|On)\r\n'), self.__MatchMicrophonesMute, None)
        self.AddMatchString(compile(b'\*c xConfiguration Audio Output (Line \d|HDMI \d) Level: (-{0,1}\d+)\r\n'),
                            self.__MatchOutputLevel, None)
        self.AddMatchString(compile(b'\*c xConfiguration Audio Output (Line \d|HDMI \d) Mode: (On|Off)\r\n'),
                            self.__MatchAudioOutput, None)
        self.AddMatchString(compile(b'\*c xConfiguration Video SelfviewDefault FullscreenMode: (Off|On|Current)\r\n'),
                            self.__MatchSelfViewDefaultFullscreenMode, None)
        self.AddMatchString(compile(b'\*s Video Selfview Mode: (On|Off)\r\n'), self.__MatchSelfView, None)
        self.AddMatchString(compile(b'\*s Video Selfview PIPPosition: (Upper|Center|Lower)(Left|Center|Right)\r\n'),
                            self.__MatchSelfViewPosition, None)
        self.AddMatchString(compile(
            b'\*s SIP Profile 1 Registration 1 Status: (Deregister|Failed|Inactive|Registered|Registering)\r\n'),
            self.__MatchSIPRegistrationStatus, None)
        self.AddMatchString(compile(b'\*s Standby Active: (On|Off)\r\n'), self.__MatchStandby, None)
        self.AddMatchString(compile(b'\*s Conference Presentation LocalSource: ([0-5])\r\n'), self.__MatchPresentation,
                            None)
        self.AddMatchString(compile(b'\*s Audio Volume: (\d+)\r\n'), self.__MatchVolume, None)
        self.AddMatchString(compile(b'\*s Conference Presentation Mode: (Sending|Receiving|Off)\r\n'),
                            self.__MatchPresentationMode, None)
        self.AddMatchString(compile(b'\*s Conference Presentation LocalSendingMode: (Off|LocalRemote|LocalOnly)\r\n'),
                            self.__MatchPresentationSendingMode, None)
        self.AddMatchString(compile(b'\*s Network 1 DNS Domain Name: "(.*)"'), self.__MatchDNSDomainName, None)
        self.AddMatchString(compile(b'\*s Network 1 IPv4 DNS Server ([1-3]) Address: "([0-9.]{7,15})"\r\n'),
                            self.__MatchDNSServerAddress, None)
        self.AddMatchString(compile(b'\*s Network 1 IPv4 Gateway: "([0-9.]{7,15})"\r\n'), self.__MatchGatewayAddress,
                            None)
        self.AddMatchString(compile(b'\*s Gatekeeper Address: "([0-9.]{7,15})"\r\n'), self.__MatchH323GatekeeperAddress,
                            None)
        self.AddMatchString(compile(b'\*c xConfiguration H323 Profile 1 H323Alias ID: "([\w\W]+)"\r\n'),
                            self.__MatchH323AliasIDStatus, None)
        self.AddMatchString(compile(
            b'\*s H323 Gatekeeper Status: (Required|Discovering|Discovered|Authenticating|Authenticated|Registering|Registered|Inactive|Rejected)\r\n'),
            self.__MatchH323GatekeeperStatus, None)
        self.AddMatchString(compile(b'\*s Network 1 IPv4 Address: "([0-9.]{7,15})"\r\n'), self.__MatchIPAddress, None)
        self.AddMatchString(compile(b'\*c xConfiguration Network 1 IPv4 Assignment: (DHCP|Static)\r\n\*\* end\r\n'),
                            self.__MatchNetworkAssignment, None)
        self.AddMatchString(compile(b'\*s Network 1 IPv4 SubnetMask: "([0-9.]{7,15})"\r\n'), self.__MatchSubnetMask,
                            None)
        self.AddMatchString(compile(b'\*s Network 1 Ethernet MacAddress: "([:0-9A-Z]{17})"\r\n\*\* end\r\n'),
                            self.__MatchMACAddress, None)
        self.AddMatchString(compile(b'\*s Cameras SpeakerTrack Status: (Active|Inactive)\r\n\*\* end\r\n'),
                            self.__MatchSpeakerTrackControl, None)
        self.AddMatchString(compile(
            b'xstatus camera SerialNumber\r\n(\*s Camera ([0-7]) SerialNumber: "(.*)"\r\n){7}\*\* end\r\n\r\nOK'),
            self.__MatchSerianNumberCameraID, None)
        self.AddMatchString(compile(b'\*c xConfiguration Conference 1 DefaultCall Rate: ([0-9]{2,4})\r\n'),
                            self.__MatchDefaultCallRate, None)
        self.AddMatchString(compile(b'\*c xConfiguration Conference 1 MaxReceiveCallRate: ([0-9]{2,4})\r\n'),
                            self.__MatchMaxReceiveCallRate, None)
        self.AddMatchString(compile(b'\*c xConfiguration Conference 1 MaxTotalReceiveCallRate: ([0-9]{2,5})\r\n'),
                            self.__MatchMaxTotalReceiveCallRate, None)
        self.AddMatchString(compile(b'\*c xConfiguration Conference 1 MaxTotalTransmitCallRate: ([0-9]{2,5})\r\n'),
                            self.__MatchMaxTotalTransmitCallRate, None)
        self.AddMatchString(compile(b'\*c xConfiguration Conference 1 MaxTransmitCallRate: ([0-9]{2,4})\r\n'),
                            self.__MatchMaxTransmitCallRate, None)
        self.AddMatchString(compile(b'login:'), self.__MatchLogin, None)
        self.AddMatchString(compile(b'Password:'), self.__MatchPassword, None)
        self.AddMatchString(compile(b'Login incorrect\r\n'), self.__MatchError, None)
        self.AddMatchString(compile(b'\xFF\xFD\x18\xFF\xFD\x20\xFF\xFD\x23\xFF\xFD\x27'), self.__MatchAuthentication,
                            None)

    @property
    def CallHistoryOccurrenceType(self):
        return self._CallHistoryOccurrenceType

    @CallHistoryOccurrenceType.setter
    def CallHistoryOccurrenceType(self, value):
        self._CallHistoryOccurrenceType = value

    @property
    def NumberofPhonebookSearch(self):
        return self._NumberofPhonebookSearch

    @NumberofPhonebookSearch.setter
    def NumberofPhonebookSearch(self, value):
        self._NumberofPhonebookSearch = value

    @property
    def NumberofCallHistory(self):
        return self._NumberofCallHistory

    @NumberofCallHistory.setter
    def NumberofCallHistory(self, value):
        self._NumberofCallHistory = value

    @property
    def NumberofPhonebookFolderSearch(self):
        return self._NumberofPhonebookFolderSearch

    @NumberofPhonebookFolderSearch.setter
    def NumberofPhonebookFolderSearch(self, value):
        self._NumberofPhonebookFolderSearch = value

    def __MatchAuthentication(self, match, tag):
        print('Matched Handshake')
        self.Send(
            b'\xFF\xFB\x18\xFF\xFB\x1F\xFF\xFC\x20\xFF\xFC\x23\xFF\xFB\x27\xFF\xFA\x1F\x00\x50\x00\x19\xFF\xF0\xFF\xFA\x27\x00\xFF\xF0\xFF\xFA\x18\x00\x41\x4E\x53\x49\xFF\xF0\xFF\xFD\x03\xFF\xFB\x01\xFF\xFE\x05\xFF\xFC\x21')

    def __MatchLogin(self, match, qualifier):
        self.Send(self.deviceUsername + '\r\n')
        if self.deviceUsername is not None:
            self.Send('{0}\r\n'.format(self.deviceUsername))
        else:
            self.MissingCredentialsLog('Username')

    def __MatchPassword(self, match, qualifier):
        print('Match Password')
        if self.devicePassword is not None:
            self.Send('{0}\r\n'.format(self.devicePassword))
        else:
            self.MissingCredentialsLog('Password')

    def __MatchSerianNumberCameraID(self, match, tag):
        res = match.group(0).decode()
        TupleIDlist = findall(self.SerialNumberID, res)
        if TupleIDlist:
            IDlist = dict(TupleIDlist)
            self.DictIDList = {v: k for k, v in IDlist.items()}

    def SetAssignLocalOutput(self, value, qualifier):
        layout = qualifier['Layout ID']
        output = qualifier['Output ID']
        if 1 <= layout <= 2147483647 and 0 <= output <= 65534:
            self.__SetHelper('AssignLocalOutput',
                             'xCommand Video Layout AssignLocalOutput OutputId:{0} LayoutId:{1}\r'.format(output,
                                                                                                          layout),
                             value, qualifier)
        else:
            print('Invalid Command')

    def SetAutoAnswer(self, value, qualifier):
        if value in ['On', 'Off']:
            self.__SetHelper('AutoAnswer', 'xConfiguration Conference 1 AutoAnswer Mode: {0}\r'.format(value), value,
                             qualifier)
        else:
            print('Invalid Command')

    def UpdateAutoAnswer(self, value, qualifier):
        self.__UpdateHelper('AutoAnswer', 'xConfiguration Conference 1 AutoAnswer Mode\r', qualifier)

    def __MatchAutoAnswer(self, match, tag):
        self.WriteStatus('AutoAnswer', match.group(1).decode(), None)

    def SetAudioVolumeMute(self, value, qualifier):

        valueStates = {
            'On': 'Mute',
            'Off': 'UnMute',
        }

        if value in ['On', 'Off']:
            self.__SetHelper('AudioVolumeMute', 'xCommand Audio Volume {0}\r'.format(valueStates[value]), value,
                             qualifier)
        else:
            print('Invalid Command for SetAudioVolumeMute')

    def UpdateAudioVolumeMute(self, value, qualifier):
        self.__UpdateHelper('AudioVolumeMute', 'xStatus Audio VolumeMute\r', qualifier)

    def __MatchAudioVolumeMute(self, match, tag):
        self.WriteStatus('AudioVolumeMute', match.group(1).decode(), None)

    def SetCallSetupMode(self, value, qualifier):

        ValueStateValues = {
            'Gatekeeper': 'Gatekeeper',
            'Direct': 'Direct'
        }

        CallSetupModeCmdString = 'xConfiguration H323 Profile 1 CallSetup Mode: {0}\r'.format(ValueStateValues[value])
        self.__SetHelper('CallSetupMode', CallSetupModeCmdString, value, qualifier)

    def SetCallHistoryRefresh(self, value, qualifier):
        self.__UpdateCallHistoryHelper(value, qualifier)

    def __UpdateCallHistoryHelper(self, value, qualifier):
        CallHistoryCmdString = 'xCommand CallHistory Recents Filter: All Offset: {0} Limit: {1} Order: Occurrence{2}\r'.format(
            self.StartCallHist - 1, self._NumberofCallHistory, self._CallHistoryOccurrenceType)
        self.Send(CallHistoryCmdString)

    def __MatchCallHistory(self, match, tag):
        res = match.group(0).decode()
        if self.PrevCallHist != res:
            self.PrevCallHist = res
            self.AdvanceCallHist = True
            DisplayNameList = dict(findall(self.CHDisplayNameRegEx, res))
            CallBackNumberList = dict(findall(self.CallBackNumberRegEx, res))
            LastOccurrenceTimeList = dict(findall(self.LastOccurrenceTimeRegEx, res))
            OccurrenceTypeList = dict(findall(self.OccurrenceTypeRegEx, res))
            OccurrenceCountList = dict(findall(self.OccurrenceCountRegEx, res))

            for button in range(1, self._NumberofCallHistory + 1):
                index = str(button - 1)

                if index in DisplayNameList:
                    self.WriteStatus('CallHistory', DisplayNameList[index],
                                     {'Button': str(button), 'Detail Type': 'Display Name'})
                    self.WriteStatus('CallHistory', CallBackNumberList[index],
                                     {'Button': str(button), 'Detail Type': 'Callback Number'})
                    self.WriteStatus('CallHistory', LastOccurrenceTimeList[index],
                                     {'Button': str(button), 'Detail Type': 'Last Occurrence Time'})
                    self.WriteStatus('CallHistory', OccurrenceTypeList[index],
                                     {'Button': str(button), 'Detail Type': 'Occurrence Type'})
                    self.WriteStatus('CallHistory', OccurrenceCountList[index],
                                     {'Button': str(button), 'Detail Type': 'Occurrence Count'})
                else:
                    self.WriteStatus('CallHistory', ' ', {'Button': str(button), 'Detail Type': 'Display Name'})
                    self.WriteStatus('CallHistory', ' ', {'Button': str(button), 'Detail Type': 'Callback Number'})
                    self.WriteStatus('CallHistory', ' ', {'Button': str(button), 'Detail Type': 'Last Occurrence Time'})
                    self.WriteStatus('CallHistory', ' ', {'Button': str(button), 'Detail Type': 'Occurrence Type'})
                    self.WriteStatus('CallHistory', ' ', {'Button': str(button), 'Detail Type': 'Occurrence Count'})
                    self.AdvanceCallHist = False

    def SetCallHistoryNavigation(self, value, qualifier):
        if value in ['Up', 'Down', 'Page Up', 'Page Down']:
            if 'Page' in value:
                NumberOfAdvance = self._NumberofCallHistory
            else:
                NumberOfAdvance = 1

            if 'Down' in value and self.AdvanceCallHist:
                self.StartCallHist += NumberOfAdvance
            elif 'Up' in value:
                self.StartCallHist -= NumberOfAdvance

            if self.StartCallHist < 1:
                self.StartCallHist = 1

            self.__UpdateCallHistoryHelper(value, qualifier)
        else:
            print('Invalid Command')

    def SetCallHistorySelect(self, value, qualifier):
        ButtonStates = {str(a): str(a) for a in range(1, 21)}
        number = self.ReadStatus('CallHistory',
                                 {'Button': ButtonStates[qualifier['Button']], 'Detail Type': 'Callback Number'})
        if number:
            self.Send('xCommand Dial Number:"{0}"\r'.format(number))

    def UpdateCallStatus(self, value, qualifier):
        self.__UpdateHelper('CallStatus', 'xstatus call\r', qualifier)

    def __MatchCallStatusIdle(self, match, tag):
        for index in range(1, 6):
            self.WriteStatus('CallStatus', 'Idle', {'Call': str(index)}, 'Live')
            self.WriteStatus('DisplayName', '', {'Call': str(index)}, 'Live')
            self.WriteStatus('RemoteNumber', '', {'Call': str(index)}, 'Live')
            self.WriteStatus('CallStatusType', 'Unknown', {'Call': str(index)}, 'Live')

    def __MatchCallStatus(self, match, tag):
        res = match.group(0).decode()
        self.__CallID = findall(self.CallIDRegEx, res)

        callList = findall(self.CallStatusRegEx, res)
        callValue = {
            'Idle': 'Idle',
            'Dialling': 'Dialing',
            'Ringing': 'Ringing',
            'Connecting': 'Connecting',
            'Connected': 'Connected',
            'Disconnecting': 'Disconnecting',
            'OnHold': 'On Hold',
            'EarlyMedia': 'Early Media',
            'Preserved': 'Preserved',
            'RemotePreserved': 'Remote Preserved',
        }

        DisplayNameList = findall(self.CSDisplayNameRegEx, res)
        RemoteNumberList = findall(self.RemoteNumberRegEx, res)
        CallStatusTypeList = findall(self.CallStatusTypeRegEx, res)

        for index in range(1, len(callList) + 1):
            self.WriteStatus('CallStatus', callValue[callList[index - 1]], {'Call': str(index)})
            self.WriteStatus('DisplayName', DisplayNameList[index - 1], {'Call': str(index)})
            self.WriteStatus('RemoteNumber', RemoteNumberList[index - 1], {'Call': str(index)})
            self.WriteStatus('CallStatusType', CallStatusTypeList[index - 1], {'Call': str(index)})
        else:
            index += 1
            while index <= 5:
                self.WriteStatus('CallStatus', 'Idle', {'Call': str(index)})
                self.WriteStatus('DisplayName', '', {'Call': str(index)})
                self.WriteStatus('RemoteNumber', '', {'Call': str(index)})
                self.WriteStatus('CallStatusType', 'Unknown', {'Call': str(index)})
                index += 1

    def UpdateCallStatusType(self, value, qualifier):
        self.UpdateCallStatus(value, qualifier)

    def SetCameraFocus(self, value, qualifier):
        camID = qualifier['Camera']
        if 1 <= int(camID) <= 7:
            if value in ['Far', 'Near', 'Stop']:
                self.__SetHelper('CameraFocus', 'xCommand Camera Ramp CameraId:{0} Focus:{1}\r'.format(camID, value),
                                 value, qualifier)
            elif value is 'Auto':
                self.__SetHelper('CameraFocus', 'xCommand Camera TriggerAutoFocus CameraId:{0}\r'.format(camID), value,
                                 qualifier)
            else:
                print('Invalid Command')
        else:
            print('Invalid Command')

    def SetCameraPan(self, value, qualifier):
        camID = qualifier['Camera']
        camSpeed = qualifier['Speed']
        if 1 <= int(camID) <= 7 and 1 <= int(camSpeed) <= 15:
            if value in ['Left', 'Right', 'Stop']:
                self.__SetHelper('CameraPan',
                                 'xCommand Camera Ramp CameraId:{0} Pan:{1} PanSpeed:{2}\r'.format(camID, value,
                                                                                                   camSpeed), value,
                                 qualifier)
            else:
                print('Invalid Command')
        else:
            print('Invalid Command')

    def SetCameraPresetPositionRecall(self, value, qualifier):
        camID = qualifier['Camera']
        if 1 <= int(camID) <= 7 and 0 < int(value) <= 15:
            self.__SetHelper('CameraPresetPositionRecall',
                             'xCommand Camera PositionActivateFromPreset CameraId:{0} PresetId:{1}\r'.format(camID,
                                                                                                             value),
                             value, qualifier)
        else:
            print('Invalid Command')

    def SetCameraPresetRecall(self, value, qualifier):
        if 0 < int(value) < 36:
            self.__SetHelper('CameraPresetRecall', 'xCommand Camera Preset Activate PresetId: {0}\r'.format(value),
                             value, qualifier)
        else:
            print('Invalid Command')

    def SetCameraPresetSave(self, value, qualifier):
        camID = qualifier['Camera']
        if 1 <= int(camID) <= 7:
            if 0 < int(value) < 36:
                self.__SetHelper('CameraPresetSave',
                                 'xCommand Camera Preset Store PresetId: {0} CameraId: {1}\r'.format(value, camID),
                                 value, qualifier)
            else:
                print('Invalid Command')
        else:
            print('Invalid Command')

    def SetCameraPresetPositionRecallSX20(self, value, qualifier):
        if 0 < int(value) < 15:
            self.__SetHelper('CameraPresetPositionRecall',
                             'xCommand Camera PositionActivateFromPreset CameraId:1 PresetId:{0}\r'.format(value),
                             value, qualifier)
        else:
            print('Invalid Command')

    def SetCameraPresetSaveSX20(self, value, qualifier):
        if 0 < int(value) < 36:
            self.__SetHelper('CameraPresetSave',
                             'xCommand Camera Preset Store PresetId: {0} CameraId: 1\r'.format(value), value, qualifier)
        else:
            print('Invalid Command')

    def SetCameraTilt(self, value, qualifier):
        camID = qualifier['Camera']
        camSpeed = qualifier['Speed']
        if 1 <= int(camID) <= 7 and 1 <= int(camSpeed) <= 15:
            if value in ['Up', 'Down', 'Stop']:
                self.__SetHelper('CameraTilt',
                                 'xCommand Camera Ramp CameraId:{0} Tilt:{1} TiltSpeed:{2}\r'.format(camID, value,
                                                                                                     camSpeed), value,
                                 qualifier)
            else:
                print('Invalid Command')
        else:
            print('Invalid Command')

    def SetCameraZoom(self, value, qualifier):
        camID = qualifier['Camera']
        camSpeed = qualifier['Speed']
        if 1 <= int(camID) <= 7 and 1 <= int(camSpeed) <= 15:
            if value in ['In', 'Out', 'Stop']:
                self.__SetHelper('CameraZoom',
                                 'xCommand Camera Ramp CameraId:{0} Zoom:{1} ZoomSpeed:{2}\r'.format(camID, value,
                                                                                                     camSpeed), value,
                                 qualifier)
            else:
                print('Invalid Command')
        else:
            print('Invalid Command')

    def SetCameraFocusSX20(self, value, qualifier):
        if value in ['Far', 'Near', 'Stop']:
            self.__SetHelper('CameraFocusSX20', 'xCommand Camera Ramp CameraId:1 Focus:{0}\r'.format(value), value,
                             qualifier)
        elif value is 'Auto':
            self.__SetHelper('CameraFocusSX20', 'xCommand Camera TriggerAutoFocus CameraId:1\r', value, qualifier)
        else:
            print('Invalid Command')

    def SetCameraPanSX20(self, value, qualifier):
        camSpeed = qualifier['Speed']
        if 1 <= int(camSpeed) <= 15:
            if value in ['Left', 'Right', 'Stop']:
                self.__SetHelper('CameraPanSX20',
                                 'xCommand Camera Ramp CameraId:1 Pan:{0} PanSpeed:{1}\r'.format(value, camSpeed),
                                 value, qualifier)
            else:
                print('Invalid Command')
        else:
            print('Invalid Command')

    def SetCameraTiltSX20(self, value, qualifier):
        camSpeed = qualifier['Speed']
        if 1 <= int(camSpeed) <= 15:
            if value in ['Up', 'Down', 'Stop']:
                self.__SetHelper('CameraTiltSX20',
                                 'xCommand Camera Ramp CameraId:1 Tilt:{0} TiltSpeed:{1}\r'.format(value, camSpeed),
                                 value, qualifier)
            else:
                print('Invalid Command')
        else:
            print('Invalid Command')

    def SetCameraZoomSX20(self, value, qualifier):
        camSpeed = qualifier['Speed']
        if 1 <= int(camSpeed) <= 15:
            if value in ['In', 'Out', 'Stop']:
                self.__SetHelper('CameraZoomSX20',
                                 'xCommand Camera Ramp CameraId:1 Zoom:{0} ZoomSpeed:{1}\r'.format(value, camSpeed),
                                 value, qualifier)
            else:
                print('Invalid Command')
        else:
            print('Invalid Command')

    def SetCloseMenu(self, value, qualifier):
        CloseMenuCmdString = 'xCommand UserInterface OSD Close Element: Menu\r'
        self.__SetHelper('CloseMenu', CloseMenuCmdString, value, qualifier)

    def SetDisplayMode(self, value, qualifier):
        if self.DisplayModeStates[value]:
            self.__SetHelper('DisplayMode', 'xConfiguration Video Monitors: {0}\r'.format(
                self.DisplayModeStates[value].replace(' ', '')), value, qualifier)
        else:
            print('Invalid Command')

    def UpdateDisplayMode(self, value, qualifier):
        self.__UpdateHelper('DisplayMode', 'xConfiguration Video Monitors\r', qualifier)

    def __MatchDisplayMode(self, match, tag):
        value = match.group(1).decode()
        value = value if value in ['Dual', 'Single', 'Triple', 'Auto'] else 'Dual Presentation Only'
        self.WriteStatus('DisplayMode', value, None)

    def SetDoNotDisturb(self, value, qualifier):
        if value in ['Active', 'Inactive']:
            cmd = 'Activate' if value == 'Active' else 'Deactivate'
            self.__SetHelper('DoNotDisturb', 'xCommand Conference DoNotDisturb {0}\r'.format(cmd), value, qualifier)
        else:
            print('Invalid Command')

    def UpdateDoNotDisturb(self, value, qualifier):
        self.__UpdateHelper('DoNotDisturb', 'xStatus Conference 1 DoNotDisturb\r', qualifier)

    def __MatchDoNotDisturb(self, match, tag):
        value = {'Active': 'Active', 'Inactive': 'Inactive'}
        self.WriteStatus('DoNotDisturb', value[match.group(1).decode()], None)

    def UpdateDNSDomainName(self, value, qualifier):
        DNSDomainNameCmdString = 'xStatus Network DNS Domain Name\r'
        self.__UpdateHelper('DNSDomainName', DNSDomainNameCmdString, qualifier)

    def __MatchDNSDomainName(self, match, tag):
        value = match.group(1).decode()
        self.WriteStatus('DNSDomainName', value, None)

    def SetDNSDomainNameCommand(self, value, qualifier):
        if value:
            CommandString = 'xConfiguration Network 1 DNS Domain Name: {0}\r'.format(value)
            self.__SetHelper('DNSDomainNameCommand', CommandString, value, qualifier)
        else:
            print('Invalid Command')

    def SetDNSServerAddressCommand(self, value, qualifier):
        if value:
            CommandString = 'xConfiguration Network 1 DNS Server 1 Address: {0}\r'.format(value)
            self.__SetHelper('DNSServerAddressCommand', CommandString, value, qualifier)
        else:
            print('Invalid Command')

    def SetFarEndControl(self, value, qualifier):
        if value in ['On', 'Off']:
            self.__SetHelper('FarEndControl', 'xConfiguration Conference 1 FarEndControl Mode: {0}\r'.format(value),
                             value, qualifier)
        else:
            print('Invalid Command')

    def UpdateFarEndControl(self, value, qualifier):
        self.__UpdateHelper('FarEndControl', 'xConfiguration Conference 1 FarEndControl Mode\r', qualifier)

    def __MatchFarEndControl(self, match, tag):
        self.WriteStatus('FarEndControl', match.group(1).decode(), None)

    def SetFarEndCameraPanTilt(self, value, qualifier):
        if value in ['Left', 'Right', 'Up', 'Down']:
            self.__SetHelper('FarEndCameraPanTilt', 'xCommand FarEndControl Camera Move Value:{0}\r'.format(value),
                             value, qualifier)
        elif value == 'Stop':
            self.__SetHelper('FarEndCameraPanTilt', 'xCommand FarEndControl Camera Stop\r', value, qualifier)
        else:
            print('Invalid Command')

    def SetFarEndCameraPresetRecall(self, value, qualifier):
        if 0 < int(value) < 16:
            self.__SetHelper('FarEndCameraPresetRecall',
                             'xCommand FarEndControl Preset Activate PresetId:{0}\r'.format(value), value, qualifier)
        else:
            print('Invalid Command')

    def SetFarEndCameraPresetSave(self, value, qualifier):
        if 0 < int(value) < 16:
            self.__SetHelper('FarEndCameraPresetSave',
                             'xCommand FarEndControl Preset Store PresetId:{0}\r'.format(value), value, qualifier)
        else:
            print('Invalid Command')

    def SetFarEndCameraSource(self, value, qualifier):
        if 0 <= int(value) < 16:
            self.__SetHelper('FarEndCameraSource', 'xCommand FarEndControl Source Select SourceId:{0}\r'.format(value),
                             value, qualifier)
        else:
            print('Invalid Command')

    def SetFarEndCameraZoom(self, value, qualifier):
        if value in ['In', 'Out']:
            self.__SetHelper('FarEndCameraZoom', 'xCommand FarEndControl Camera Move Value:Zoom{0}\r'.format(value),
                             value, qualifier)
        elif value == 'Stop':
            self.__SetHelper('FarEndCameraZoom', 'xCommand FarEndControl Camera Stop\r', value, qualifier)
        else:
            print('Invalid Command')

    def SetH323AliasE164Command(self, value, qualifier):
        if value:
            CommandString = 'xConfiguration H323 Profile 1 H323Alias E164: {0}\r'.format(value)
            self.__SetHelper('H323AliasE164Command', CommandString, value, qualifier)
        else:
            print('Invalid Command')

    def SetH323AliasIDCommand(self, value, qualifier):
        if value:
            CommandString = 'xConfiguration H323 Profile 1 H323Alias ID: {0}\r'.format(value)
            self.__SetHelper('H323AliasIDCommand', CommandString, value, qualifier)
        else:
            print('Invalid Command')

    def UpdateH323AliasIDStatus(self, value, qualifier):
        CommandString = 'xConfiguration H323 Profile 1 H323Alias ID\r'
        self.__UpdateHelper('H323AliasIDStatus', CommandString, qualifier)

    def __MatchH323AliasIDStatus(self, match, tag):
        value = match.group(1).decode()
        self.WriteStatus('H323AliasIDStatus', value, None)

    def UpdateH323GatekeeperAddress(self, value, qualifier):
        H323GatekeeperAddressCmdString = 'xStatus H323 Gatekeeper Address\r'
        self.__UpdateHelper('H323GatekeeperAddress', H323GatekeeperAddressCmdString, qualifier)

    def __MatchH323GatekeeperAddress(self, match, tag):
        value = match.group(1).decode()
        self.WriteStatus('H323GatekeeperAddress', value, None)

    def SetH323GatekeeperAddressCommand(self, value, qualifier):
        if value:
            CommandString = 'xConfiguration H323 Profile 1 Gatekeeper Address: {0}\r'.format(value)
            self.__SetHelper('H323GatekeeperAddressCommand', CommandString, value, qualifier)
        else:
            print('Invalid Command')

    def UpdateH323GatekeeperStatus(self, value, qualifier):
        H323GatekeeperStatusCmdString = 'xStatus H323 Gatekeeper Status\r'
        self.__UpdateHelper('H323GatekeeperStatus', H323GatekeeperStatusCmdString, qualifier)

    def __MatchH323GatekeeperStatus(self, match, tag):
        ValueStateValues = {
            'Required': 'Required',
            'Discovering': 'Discovering',
            'Discovered': 'Discovered',
            'Authenticating': 'Authenticating',
            'Authenticated': 'Authenticated',
            'Registering': 'Registering',
            'Registered': 'Registered',
            'Inactive': 'Inactive',
            'Rejected': 'Rejected'
        }

        value = ValueStateValues[match.group(1).decode()]
        self.WriteStatus('H323GatekeeperStatus', value, None)

    def SetH323ProfileAuthenticationLoginNameCommand(self, value, qualifier):
        if value:
            CommandString = 'xConfiguration H323 Profile 1 Authentication LoginName: {0}\r'.format(value)
            self.__SetHelper('H323ProfileAuthenticationLoginNameCommand', CommandString, value, qualifier)
        else:
            print('Invalid Command')

    def SetH323ProfileAuthenticationPasswordCommand(self, value, qualifier):
        if value:
            CommandString = 'xConfiguration H323 Profile 1 Authentication Password: {0}\r'.format(value)
            self.__SetHelper('H323ProfileAuthenticationPasswordCommand', CommandString, value, qualifier)
        else:
            print('Invalid Command')

    def SetHook(self, value, qualifier):
        Protocol_Values = {
            'H320': 'h320',
            'H323': 'h323',
            'SIP': 'sip',
            'Auto': 'Auto',
        }

        protocol = qualifier['Protocol']

        if value in ['Disconnect All', 'Accept', 'Reject', 'Hold All']:
            self.__SetHelper('Hook', 'xCommand Call {0}\r'.format(value.replace(' ', '')), value, qualifier)
        elif 'Resume' in value or 'Disconnect' in value or 'Hold' in value or 'Join' in value:
            val = value.split(' ')
            cmd = val[0]
            index = int(val[1]) - 1
            try:
                self.__SetHelper('Hook', 'xCommand Call {0} CallId: {1}\r'.format(cmd, self.__CallID[index]), value,
                                 qualifier)
            except IndexError:
                print('Invalid Command')
        elif value is 'Dial':
            number = qualifier['Number']
            if number:
                if protocol == 'Auto':
                    self.__SetHelper('Hook', 'xCommand Dial Number:"{0}"\r'.format(number), value, qualifier)
                else:
                    self.__SetHelper('Hook', 'xCommand Dial Number:"{0}" Protocol:{1}\r'.format(number, Protocol_Values[
                        protocol]), value, qualifier)
        else:
            print('Invalid Command')

    def UpdateFirmwareVersion(self, value, qualifier):
        FirmwareVersionCmdString = 'xStatus SystemUnit Software Version\r'
        self.__UpdateHelper('FirmwareVersion', FirmwareVersionCmdString, qualifier)

    def __MatchFirmwareVersion(self, match, tag):
        value = match.group(1).decode()
        self.WriteStatus('FirmwareVersion', value, None)

    def SetInputSX20(self, value, qualifier):
        InputStates = {
            '1': '1',
            '2': '2',
        }

        if InputStates[value]:
            self.__SetHelper('InputSX20', 'xConfiguration Video MainVideoSource: {0}\r'.format(InputStates[value]),
                             value, qualifier)
        else:
            print('Invalid Command')

    def UpdateInputSX20(self, value, qualifier):
        self.__UpdateHelper('InputSX20', 'xConfiguration Video MainVideoSource\r', qualifier)

    def __MatchInputSX20(self, match, tag):
        self.WriteStatus('InputSX20', match.group(1).decode(), None)

    def SetInputSX80(self, value, qualifier):
        InputStates = {
            '1': '1',
            '2': '2',
            '3': '3',
            '4': '4',
            '5': '5',
        }
        if InputStates[value]:
            self.__SetHelper('InputSX80',
                             'xCommand Video Input SetMainVideoSource ConnectorId: {0}\r'.format(InputStates[value]),
                             value, qualifier)
        else:
            print('Invalid Command')

    def UpdateInputSX80(self, value, qualifier):
        self.__UpdateHelper('InputSX80', 'xStatus Video Input MainVideoSource\r', qualifier)

    def __MatchInputSX80(self, match, tag):
        self.WriteStatus('InputSX80', match.group(1).decode(), None)

    def SetInputLineLevel(self, value, qualifier):
        input_ = self.LineStates[qualifier['Input']]
        if input_ and 0 <= value <= 24:
            self.__SetHelper('InputLineLevel', 'xConfiguration Audio Input {0} Level:{1}\r'.format(input_, value),
                             value, qualifier)
        else:
            print('Invalid Command')

    def UpdateInputLineLevel(self, value, qualifier):
        input_ = self.LineStates[qualifier['Input']]
        if input_:
            self.__UpdateHelper('InputLineLevel', 'xConfiguration Audio Input {0} Level\r'.format(input_), qualifier)
        else:
            print('Invalid Command')

    def __MatchInputLineLevel(self, match, tag):
        input_ = match.group(1).decode()
        value = int(match.group(2))
        self.WriteStatus('InputLineLevel', value, {'Input': input_})

    def SetInputMicLevel(self, value, qualifier):
        input_ = self.MicStates[qualifier['Input']]
        if input_ and 0 <= value <= 70:
            self.__SetHelper('InputMicLevel', 'xConfiguration Audio Input {0} Level:{1}\r'.format(input_, value), value,
                             qualifier)
        else:
            print('Invalid Command')

    def UpdateInputMicLevel(self, value, qualifier):
        input_ = self.MicStates[qualifier['Input']]
        if input_:
            self.__UpdateHelper('InputMicLevel', 'xConfiguration Audio Input {0} Level\r'.format(input_), qualifier)
        else:
            print('Invalid Command')

    def __MatchInputMicLevel(self, match, tag):
        input_ = match.group(1).decode()
        value = int(match.group(2))
        self.WriteStatus('InputMicLevel', value, {'Input': input_})

    def SetInputMute(self, value, qualifier):
        stateValue = {
            'On': 'On',
            'Off': 'Off',
        }

        input_ = self.InputMuteStates[qualifier['Input']]
        if input_:
            self.__SetHelper('InputMute', 'xConfiguration Audio Input {0} Mode:{1}\r'.format(input_, stateValue[value]),
                             value, qualifier)
        else:
            print('Invalid Command')

    def UpdateInputMute(self, value, qualifier):
        input_ = self.InputMuteStates[qualifier['Input']]
        if input_:
            self.__UpdateHelper('InputMute', 'xConfiguration Audio Input {0} Mode\r'.format(input_), qualifier)
        else:
            print('Invalid Command')

    def __MatchInputMute(self, match, tag):

        input_ = match.group(1).decode()
        self.WriteStatus('InputMute', match.group(3).decode(), {'Input': input_})

    def SetIPv4AddressCommand(self, value, qualifier):
        if value:
            CommandString = 'xConfiguration Network 1 IPv4 Address: {0}\r'.format(value)
            self.__SetHelper('IPv4AddressCommand', CommandString, value, qualifier)
        else:
            print('Invalid Command')

    def SetIPv4GatewayCommand(self, value, qualifier):
        if value:
            CommandString = 'xConfiguration Network 1 IPv4 Gateway: {0}\r'.format(value)
            self.__SetHelper('IPv4GatewayCommand', CommandString, value, qualifier)
        else:
            print('Invalid Command')

    def SetIPv4SubnetMaskCommand(self, value, qualifier):
        if value:
            CommandString = 'xConfiguration Network 1 IPv4 SubnetMask: {0}\r'.format(value)
            self.__SetHelper('IPv4SubnetMaskCommand', CommandString, value, qualifier)
        else:
            print('Invalid Command')

    def SetIREmulation(self, value, qualifier):

        cmdVal = {
            'Delete': 'C',
            'Mute Mic': 'MuteMic',
            'Aux': 'SrcAux',
            'Camera': 'SrcCamera',
            'Doc Camera': 'SrcDocCam',
            'PC': 'SrcPc',
            'VCR': 'SrcVcr',
            '#': 'Square',
            '*': 'Star',
            'Volume Down': 'VolumeDown',
            'Volume Up': 'VolumeUp',
            'Zoom In': 'ZoomIn',
            'Zoom Out': 'ZoomOut',
        }
        if value in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'Call', 'Disconnect', 'F1', 'F2', 'F3', 'F4',
                     'F5',
                     'Grab', 'Home', 'Layout', 'Mute', 'Ok', 'Phonebook', 'Presentation', 'Selfview',
                     'Up', 'Down', 'Left', 'Right', ]:
            self.__SetHelper('IREmulation', 'xCommand Key Click Key:{0}\r'.format(value), value, qualifier)
        elif value in cmdVal:
            self.__SetHelper('IREmulation', 'xCommand Key Click Key:{0}\r'.format(cmdVal[value]), value, qualifier)
        else:
            print('Invalid Command')

    def SetLayout(self, value, qualifier):
        id_ = qualifier[self.Commands['Layout']['Parameters'][0]]
        if 1 <= id_ <= 65535:
            if value in ['Add', 'Remove']:
                self.__SetHelper('Layout', 'xCommand Video Layout {0} LayoutId: {1}\r'.format(value, id_), value,
                                 qualifier)
            elif value in ['Remove All', 'Reset']:
                self.__SetHelper('Layout', 'xCommand Video Layout {0}\r'.format(value.replace(' ', '')), value,
                                 qualifier)
            else:
                print('Invalid Command')
        else:
            print('Invalid Command')

    def SetLayoutSet(self, value, qualifier):
        targetStates = {
            'Local': 'Local',
            'Remote': 'Remote'
        }

        target = targetStates[qualifier['Target']]
        if target and value in ['Auto', 'Custom', 'Equal', 'Fullscreen', 'Overlay', 'Presentation Large Speaker',
                                'Presentation Small Speaker', 'Prominent', 'Single']:
            self.__SetHelper('LayoutSet',
                             'xCommand Video PictureLayoutSet Target: {0} LayoutFamily: {1}\r'.format(target,
                                                                                                      value.replace(' ',
                                                                                                                    '')),
                             value, qualifier)
        elif target and value == 'Speaker Full':
            self.__SetHelper('LayoutSet',
                             'xCommand Video PictureLayoutSet Target: {0} LayoutFamily: Speaker_Full\r'.format(target),
                             value, qualifier)
        else:
            print('Invalid Command')

    def SetMicrophonesMute(self, value, qualifier):
        cmdVal = {
            'On': 'Mute',
            'Off': 'UnMute',
        }
        self.__SetHelper('MicrophonesMute', 'xCommand Audio Microphones {0}\r'.format(cmdVal[value]), value, qualifier)

    def UpdateMicrophonesMute(self, value, qualifier):
        self.__UpdateHelper('MicrophonesMute', 'xStatus Audio Microphones\r', qualifier)

    def __MatchMicrophonesMute(self, match, tag):
        self.WriteStatus('MicrophonesMute', match.group(1).decode(), None)

    def SetOutputLevel(self, value, qualifier):
        Output = self.AudioOutputStates[qualifier['Output']]
        if Output and -24 <= value <= 0:
            self.__SetHelper('OutputLevel', 'xConfiguration Audio Output {0} Level:{1}\r'.format(Output, value), value,
                             qualifier)
        else:
            print('Invalid Command')

    def UpdateOutputLevel(self, value, qualifier):
        Output = self.AudioOutputStates[qualifier['Output']]
        if Output:
            self.__UpdateHelper('OutputLevel', 'xConfiguration Audio Output {0} Level\r'.format(Output), qualifier)
        else:
            print('Invalid Command')

    def __MatchOutputLevel(self, match, tag):
        Output = match.group(1).decode()
        value = int(match.group(2))
        self.WriteStatus('OutputLevel', value, {'Output': Output})

    def SetAudioOutput(self, value, qualifier):
        Output = self.AudioOutputStates[qualifier['Output']]
        if Output and value in ['On', 'Off']:
            self.__SetHelper('AudioOutput', 'xConfiguration Audio Output {0} Mode:{1}\r'.format(Output, value), value,
                             qualifier)
        else:
            print('Invalid Command')

    def UpdateAudioOutput(self, value, qualifier):
        Output = qualifier[self.Commands['AudioOutput']['Parameters'][0]]
        self.__UpdateHelper('AudioOutput', 'xConfiguration Audio Output {0} Mode\r'.format(Output), qualifier)

    def __MatchAudioOutput(self, match, tag):
        Output = match.group(1).decode()
        self.WriteStatus('AudioOutput', match.group(2).decode(), {'Output': Output})

    def SetPhonebookSearchSet(self, value, qualifier):
        if 1 <= value <= self._NumberofPhonebookSearch:
            number = self.ReadStatus('PhonebookSearchResult', {'Button': int(value)})
            if number and number != '***End of list***':
                number = number[number.find(' : ') + 3:]
                commandstring = 'xCommand Dial Number:"{0}"\r'.format(number)
                self.Send(commandstring)

    def SetPhonebookFolderIDNavigation(self, value, qualifier):
        if self.FolderLimit != 0:
            if value in ['Up', 'Down', 'Page Up', 'Page Down']:
                if 'Page' in value:
                    NumberOfAdvance = self._NumberofPhonebookFolderSearch
                else:
                    NumberOfAdvance = 1

                if 'Down' in value and self.FolderMin <= len(self.folderList):
                    self.FolderMin += NumberOfAdvance
                    self.FolderLimit += NumberOfAdvance
                elif 'Up' in value:
                    self.FolderMin -= NumberOfAdvance
                    self.FolderLimit -= NumberOfAdvance

                if self.FolderMin < 1:
                    self.FolderMin = 1

                if self.FolderLimit < self._NumberofPhonebookFolderSearch:
                    self.FolderLimit = self._NumberofPhonebookFolderSearch

            button = 1
            for i in range(self.FolderMin, self.FolderLimit + 1):
                if str(i) in self.folderList:
                    self.WriteStatus('PhonebookFolderIDSearchResult', '{0}'.format(self.folderList[str(i)]['Name']),
                                     {'Button': button})
                    button += 1

            if button <= self._NumberofPhonebookFolderSearch:
                self.WriteStatus('PhonebookFolderIDSearchResult', '***End of list***', {'Button': button})
                button += 1
                for i in range(button, int(self._NumberofPhonebookFolderSearch) + 1):
                    self.WriteStatus('PhonebookFolderIDSearchResult', '', {'Button': i})
            else:
                print('Invalid Command')

    def SetPhonebookNavigation(self, value, qualifier):
        if self.MaxLabel != 0:
            if value in ['Up', 'Down', 'Page Up', 'Page Down']:
                if 'Page' in value:
                    NumberOfAdvance = self._NumberofPhonebookSearch
                else:
                    NumberOfAdvance = 1

                if 'Down' in value and self.MinLabel <= len(self.newList):
                    self.MinLabel += NumberOfAdvance
                    self.MaxLabel += NumberOfAdvance
                elif 'Up' in value:
                    self.MinLabel -= NumberOfAdvance
                    self.MaxLabel -= NumberOfAdvance

                if self.MinLabel < 1:
                    if self.Offset != 0:
                        self.SetPhonebookUpdate('Previous Search', qualifier)
                        self.MinLabel = len(self.newList) - (self._NumberofPhonebookSearch - 1)
                        self.MaxLabel = len(self.newList)
                    else:
                        self.MinLabel = 1

                if self.MaxLabel < self._NumberofPhonebookSearch:
                    self.MaxLabel = self._NumberofPhonebookSearch

                if self.MaxLabel > len(self.newList) and len(self.newList) == self._NumberOfContactsPerSearch:
                    self.SetPhonebookUpdate('Next Search', qualifier)

                self.SetPhonebookWriteHandler(value, qualifier)
        else:
            print('Invalid Command')

    def SetPhonebookFolderIDSearchSet(self, value, qualifier):
        if self.folderList:
            folderName = self.ReadStatus('PhonebookFolderIDSearchResult', {'Button': value})
            if folderName != '***End of list***':
                self.FolderIDNumber = [v['ID'] for v in self.folderList.values() if v['Name'] == folderName][0]
        else:
            print('Invalid Command for SetPhonebookFolderIDSearchSet')

    def SetPhonebookFolderIDUpdate(self, value, qualifier):
        phonebookValue = qualifier['Phonebook Type']
        self.FolderMin = 1
        self.FolderLimit = self._NumberofPhonebookFolderSearch
        if phonebookValue:
            cmdStr = 'xCommand Phonebook Search PhonebookType:{0} ContactType: Folder Offset: 0 Limit: {1}\r'.format(
                phonebookValue, self._NumberOfFoldersPerSearch)
            res = self.SendAndWait(cmdStr, 10, deliTag=b'** end')
            if res:
                res = res.decode()
                self.folderList = {}
                folderName = findall(self.FolderNameRegEx, res)
                folderID = findall(self.FolderIDRegEx, res)

                for i, name in folderName:
                    self.folderList[i] = {'Name': name}

                for i, id_ in folderID:
                    if i in self.folderList:
                        self.folderList[i]['ID'] = id_
                    else:
                        self.folderList[i] = {'ID': id_}

                button = 1
                for i in range(1, self._NumberofPhonebookFolderSearch + 1):
                    if str(i) in self.folderList:
                        self.WriteStatus('PhonebookFolderIDSearchResult', '{0}'.format(self.folderList[str(i)]['Name']),
                                         {'Button': int(i)})
                        button += 1

                if button <= self._NumberofPhonebookFolderSearch:
                    self.WriteStatus('PhonebookFolderIDSearchResult', '***End of list***', {'Button': button})
                    button += 1
                    for i in range(button, int(self._NumberofPhonebookFolderSearch) + 1):
                        self.WriteStatus('PhonebookFolderIDSearchResult', '', {'Button': i})
        else:
            print('Invalid Command')

    def SetPhonebookUpdate(self, value, qualifier):
        if value == 'Refresh':
            self.Offset = 0
            self.MinLabel = 1
            self.MaxLabel = self._NumberofPhonebookSearch
        elif value == 'Next Search' and len(self.newList) == self._NumberOfContactsPerSearch:
            self.MinLabel = 1
            self.MaxLabel = 5
            self.Offset += self._NumberOfContactsPerSearch
        elif value == 'Previous Search':
            self.Offset -= self._NumberOfContactsPerSearch

        if self.Offset < 0:
            self.MinLabel = 1
            self.MaxLabel = self._NumberofPhonebookSearch
            self.Offset = 0

        self.WriteStatus('PhonebookSearchResult', '***Loading Contacts***', {'Button': 1})
        for i in range(2, int(self._NumberofPhonebookSearch) + 1):
            self.WriteStatus('PhonebookSearchResult', '...', {'Button': i})

        self.SetPhonebookUpdateHandler(value, qualifier)

    def SetPhonebookUpdateHandler(self, value, qualifier):
        phonebookType = qualifier['Phonebook Type']
        contact = qualifier['Contact']
        folderID = qualifier['FolderID']
        tag = qualifier['Phonebook Tag']
        if phonebookType in ['Corporate', 'Local']:
            if contact:
                contact = 'SearchString: "{0}" '.format(contact)
            else:
                contact = ''

            if folderID:
                fldID = 'FolderID:"{0}" '.format(folderID)
            else:
                fldID = ''

            if tag in ['Favorite', 'Untagged']:
                pbTag = ' Tag:{0}'.format(tag)
            else:
                pbTag = ''

            cmdStr = 'xCommand Phonebook Search PhonebookType:{0} {1}SearchField: Name ContactType: Contact {2} Offset: {3} Limit: {5}{4}\r'.format(
                phonebookType, contact, fldID, self.Offset, pbTag, self._NumberOfContactsPerSearch)
            res = self.SendAndWait(cmdStr, 15, deliTag='** end')
            if res:
                res = res.decode()
                self.newList = {}
                nameList = findall(self.DirNameRegEx, res)
                numberList = findall(self.DirNumberRegEx, res)

                for i, name in nameList:
                    self.newList[i] = {'Name': name}

                for i, number in numberList:
                    if i in self.newList:
                        self.newList[i]['Number'] = number
                    else:
                        self.newList[i] = {'Number': number}

                self.SetPhonebookWriteHandler(value, qualifier)
        else:
            print('Invalid Command')

    def SetPhonebookWriteHandler(self, value, qualifier):
        button = 1
        for i in range(self.MinLabel, self.MaxLabel + 1):
            if str(i) in self.newList:
                self.WriteStatus('PhonebookSearchResult',
                                 '{0} : {1}'.format(self.newList[str(i)]['Name'], self.newList[str(i)]['Number']),
                                 {'Button': button})
                button += 1

        if button <= self._NumberofPhonebookSearch:
            self.WriteStatus('PhonebookSearchResult', '***End of list***', {'Button': button})
            button += 1
            for i in range(button, int(self._NumberofPhonebookSearch) + 1):
                self.WriteStatus('PhonebookSearchResult', '', {'Button': i})

    def SetPictureInPicture(self, value, qualifier):
        if value in ['On', 'Off']:
            self.__SetHelper('PictureInPicture', 'xCommand CamCtrlPip Mode:{0}\r'.format(value), value, qualifier)
        else:
            print('Invalid Command')

    def SetPresentation(self, value, qualifier):
        if self.PresentationStates[value]:
            if value == 'Stop':
                cmd = 'xCommand Presentation Stop\r'
            else:
                cmd = 'xCommand Presentation Start PresentationSource: {0}\r'.format(self.PresentationStates[value])

            if cmd:
                self.__SetHelper('Presentation', cmd, value, qualifier)
            else:
                print('Invalid Command')
        else:
            print('Invalid Command')

    def UpdatePresentation(self, value, qualifier):
        self.__UpdateHelper('Presentation', 'xStatus Conference Presentation LocalSource\r', qualifier)

    def __MatchPresentation(self, match, tag):
        value = match.group(1).decode()
        value = 'Stop' if value == '0' else value
        self.WriteStatus('Presentation', value, None)

    def UpdatePresentationMode(self, value, qualifier):
        PresentationModeCmdString = 'xStatus Conference Presentation Mode\r'
        self.__UpdateHelper('PresentationMode', PresentationModeCmdString, qualifier)

    def __MatchPresentationMode(self, match, tag):
        value = match.group(1).decode()
        self.WriteStatus('PresentationMode', value, None)

    def SetPresentationSendingMode(self, value, qualifier):
        ValueStateValues = {
            'Local and Remote': 'xCommand Presentation Start SendingMode: LocalRemote\r',
            'Local Only': 'xCommand Presentation Start SendingMode: LocalOnly\r'
        }

        PresentationSendingModeCmdString = ValueStateValues[value]
        self.__SetHelper('PresentationSendingMode', PresentationSendingModeCmdString, value, qualifier)

    def UpdatePresentationSendingMode(self, value, qualifier):
        PresentationSendingModeCmdString = 'xStatus Conference Presentation LocalSendingMode\r'
        self.__UpdateHelper('PresentationSendingMode', PresentationSendingModeCmdString, qualifier)

    def __MatchPresentationSendingMode(self, match, tag):
        ValueStateValues = {
            'LocalRemote': 'Local and Remote',
            'LocalOnly': 'Local Only',
            'Off': 'Off',
        }

        value = ValueStateValues[match.group(1).decode()]
        self.WriteStatus('PresentationSendingMode', value, None)

    def SetPresetRecall(self, value, qualifier):
        ValueStateValues = {
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
            '15': '15'
        }

        PresetRecallCmdString = 'xCommand Preset Activate PresetId:{0}\r'.format(ValueStateValues[value])
        self.__SetHelper('PresetRecall', PresetRecallCmdString, value, qualifier)

    def SetPresetSave(self, value, qualifier):
        ValueStateValues = {
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
            '15': '15'
        }

        PresetSaveCmdString = 'xCommand Preset Store PresetId:{0} Type:All\r'.format(ValueStateValues[value])
        self.__SetHelper('PresetSave', PresetSaveCmdString, value, qualifier)

    def SetReboot(self, value, qualifier):
        self.__SetHelper('Reboot', 'xCommand Boot\r', value, qualifier)

    def SetSelfViewDefaultFullscreenMode(self, value, qualifier):
        ValueStateValues = {
            'On': 'On',
            'Off': 'Off',
            'Current': 'Current'
        }

        SelfViewDefaultFullscreenModeCmdString = 'xConfiguration Video SelfviewDefault FullscreenMode:{0}\r'.format(
            ValueStateValues[value])
        self.__SetHelper('SelfViewDefaultFullscreenMode', SelfViewDefaultFullscreenModeCmdString, value, qualifier)

    def UpdateSelfViewDefaultFullscreenMode(self, value, qualifier):
        SelfViewDefaultFullscreenModeCmdString = 'xConfiguration Video SelfviewDefault FullscreenMode\r'
        self.__UpdateHelper('SelfViewDefaultFullscreenMode', SelfViewDefaultFullscreenModeCmdString, qualifier)

    def __MatchSelfViewDefaultFullscreenMode(self, match, tag):
        ValueStateValues = {
            'On': 'On',
            'Off': 'Off',
            'Current': 'Current'
        }

        value = ValueStateValues[match.group(1).decode()]
        self.WriteStatus('SelfViewDefaultFullscreenMode', value, None)

    def SetSelfView(self, value, qualifier):
        if value in ['On', 'Off']:
            self.__SetHelper('SelfView', 'xCommand Video Selfview Set Mode:{0}\r'.format(value), value, qualifier)
        else:
            print('Invalid Command')

    def UpdateSelfView(self, value, qualifier):
        self.__UpdateHelper('SelfView', 'xStatus Video Selfview Mode\r', qualifier)

    def __MatchSelfView(self, match, tag):
        self.WriteStatus('SelfView', match.group(1).decode(), None)

    def SetSelfViewPosition(self, value, qualifier):
        if value in ['Upper Left', 'Upper Center', 'Upper Right', 'Center Left', 'Center Right', 'Lower Left',
                     'Lower Right']:
            self.__SetHelper('SelfViewPosition',
                             'xCommand Video Selfview Set PIPPosition:{0}\r'.format(value.replace(' ', '')), value,
                             qualifier)
        else:
            print('Invalid Command')

    def UpdateSelfViewPosition(self, value, qualifier):
        self.__UpdateHelper('SelfViewPosition', 'xStatus Video Selfview PIPPosition\r', qualifier)

    def __MatchSelfViewPosition(self, match, tag):
        value = match.group(1).decode() + ' ' + match.group(2).decode()
        self.WriteStatus('SelfViewPosition', value, None)

    def UpdateSIPRegistrationStatus(self, value, qualifier):
        SIPRegistrationStatusCmdString = 'xStatus SIP Profile 1 Registration 1 Status\r'
        self.__UpdateHelper('SIPRegistrationStatus', SIPRegistrationStatusCmdString, qualifier)

    def __MatchSIPRegistrationStatus(self, match, tag):
        ValueStateValues = {
            'Deregister': 'Deregistering',
            'Failed': 'Failed',
            'Inactive': 'Inactive',
            'Registered': 'Registered',
            'Registering': 'Registering'
        }

        value = ValueStateValues[match.group(1).decode()]
        self.WriteStatus('SIPRegistrationStatus', value, None)

    def SetCameraSerialNumberRefresh(self, value, qualifier):
        self.__SetHelper('CameraSerialNumberRefresh', 'xstatus camera SerialNumber\r', value, qualifier)

    def SetSNCameraPresetSave(self, value, qualifier):
        camID = qualifier['Serial Number']
        if camID in self.DictIDList:
            if 0 < int(value) < 36:
                self.__SetHelper('SNCameraPresetSave',
                                 'xCommand Camera Preset Store PresetId: {0} CameraId: {1}\r'.format(value,
                                                                                                     self.DictIDList[
                                                                                                         camID]), value,
                                 qualifier)
            else:
                print('Invalid Command')
        else:
            print('Invalid Command')

    def SetSNCameraFocus(self, value, qualifier):
        camID = qualifier['Serial Number']
        if camID in self.DictIDList:
            if value in ['Far', 'Near', 'Stop']:
                self.__SetHelper('SNCameraFocus',
                                 'xCommand Camera Ramp CameraId:{0} Focus:{1}\r'.format(self.DictIDList[camID], value),
                                 value, qualifier)
            elif value is 'Auto':
                self.__SetHelper('SNCameraFocus',
                                 'xCommand Camera TriggerAutoFocus CameraId:{0}\r'.format(self.DictIDList[camID]),
                                 value, qualifier)
            else:
                print('Invalid Command')
        else:
            print('Invalid Command')

    def SetSNCameraPan(self, value, qualifier):
        camID = qualifier['Serial Number']
        camSpeed = qualifier['Speed']
        if camID in self.DictIDList:
            if value in ['Left', 'Right', 'Stop']:
                self.__SetHelper('SNCameraPan', 'xCommand Camera Ramp CameraId:{0} Pan:{1} PanSpeed:{2}\r'.format(
                    self.DictIDList[camID], value, camSpeed), value, qualifier)
            else:
                print('Invalid Command')
        else:
            print('Invalid Command')

    def SetSNCameraTilt(self, value, qualifier):
        camID = qualifier['Serial Number']
        camSpeed = qualifier['Speed']
        if camID in self.DictIDList:
            if value in ['Up', 'Down', 'Stop']:
                self.__SetHelper('SNCameraTilt', 'xCommand Camera Ramp CameraId:{0} Tilt:{1} TiltSpeed:{2}\r'.format(
                    self.DictIDList[camID], value, camSpeed), value, qualifier)
            else:
                print('Invalid Command')
        else:
            print('Invalid Command')

    def SetSNCameraZoom(self, value, qualifier):
        camID = qualifier['Serial Number']
        camSpeed = qualifier['Speed']
        if camID in self.DictIDList:
            if value in ['In', 'Out', 'Stop']:
                self.__SetHelper('SNCameraZoom', 'xCommand Camera Ramp CameraId:{0} Zoom:{1} ZoomSpeed:{2}\r'.format(
                    self.DictIDList[camID], value, camSpeed), value, qualifier)
            else:
                print('Invalid Command')
        else:
            print('Invalid Command')

    def SetSleepTimer(self, value, qualifier):
        if 0 < value < 481:
            self.__SetHelper('SleepTimer', 'xCommand Standby ResetTimer Delay:{0}\r'.format(value), value, qualifier)
        else:
            print('Invalid Command')

    def SetStandby(self, value, qualifier):
        self.__SetHelper('Standby', 'xCommand Standby {0}\r'.format(value), value, qualifier)

    def UpdateStandby(self, value, qualifier):
        self.__UpdateHelper('Standby', 'xStatus Standby\r', qualifier)

    def __MatchStandby(self, match, tag):
        cmdVal = {
            b'Off': 'Deactivate',
            b'On': 'Activate',
        }
        self.WriteStatus('Standby', cmdVal[match.group(1)], None)

    def SetVolume(self, value, qualifier):
        if 0 <= value <= 100:
            self.__SetHelper('Volume', 'xcommand audio volume set level:{0}\r'.format(value), value, qualifier)
        else:
            print('Invalid Command')

    def UpdateVolume(self, value, qualifier):
        self.__UpdateHelper('Volume', 'xstatus audio volume\r', qualifier)

    def __MatchVolume(self, match, tag):
        self.WriteStatus('Volume', int(match.group(1)), None)

    def UpdateDisplayName(self, value, qualifier):
        self.UpdateCallStatus(value, qualifier)

    def UpdateDNSServerAddress(self, value, qualifier):
        ServerStates = {
            '1': '1',
            '2': '2',
            '3': '3'
        }

        DNSServerAddressCmdString = 'xStatus Network 1 IPv4 DNS Server {0} Address\r'.format(
            ServerStates[qualifier['Server']])
        self.__UpdateHelper('DNSServerAddress', DNSServerAddressCmdString, qualifier)

    def __MatchDNSServerAddress(self, match, tag):
        ServerStates = {
            '1': '1',
            '2': '2',
            '3': '3'
        }

        qualifier = {}
        qualifier['Server'] = ServerStates[match.group(1).decode()]
        value = match.group(2).decode()
        self.WriteStatus('DNSServerAddress', value, qualifier)

    def SetDTMF(self, value, qualifier):
        ValueStateValues = {
            '0': '0',
            '1': '1',
            '2': '2',
            '3': '3',
            '4': '4',
            '5': '5',
            '6': '6',
            '7': '7',
            '8': '8',
            '9': '9',
            '*': '*',
            '#': '#'
        }

        DTMFCommandCmdString = 'xCommand DTMFSend DTMFString:{0}\r'.format(ValueStateValues[value])
        self.__SetHelper('DTMFCommand', DTMFCommandCmdString, value, qualifier)

    def UpdateGatewayAddress(self, value, qualifier):
        GatewayAddressCmdString = 'xStatus Network 1 IPv4 Gateway\r'
        self.__UpdateHelper('GatewayAddress', GatewayAddressCmdString, qualifier)

    def __MatchGatewayAddress(self, match, tag):
        value = match.group(1).decode()
        self.WriteStatus('GatewayAddress', value, None)

    def UpdateIPAddress(self, value, qualifier):
        IPAddressCmdString = 'xStatus Network 1 IPv4 Address\r'
        self.__UpdateHelper('IPAddress', IPAddressCmdString, qualifier)

    def __MatchIPAddress(self, match, tag):
        value = match.group(1).decode()
        self.WriteStatus('IPAddress', value, None)

    def UpdateMACAddress(self, value, qualifier):
        MACAddressCmdString = 'xStatus Network 1 Ethernet MacAddress\r'
        self.__UpdateHelper('MACAddress', MACAddressCmdString, qualifier)

    def __MatchMACAddress(self, match, tag):
        value = match.group(1).decode()
        self.WriteStatus('MACAddress', value, None)

    def UpdateNetworkAssignment(self, value, qualifier):
        NetworkAssignmentCmdString = 'xConfiguration Network 1 IPv4 Assignment\r'
        self.__UpdateHelper('NetworkAssignment', NetworkAssignmentCmdString, qualifier)

    def __MatchNetworkAssignment(self, match, tag):
        ValueStateValues = {
            'Static': 'Static',
            'DHCP': 'DHCP'
        }

        value = ValueStateValues[match.group(1).decode()]
        self.WriteStatus('NetworkAssignment', value, None)

    def UpdateRemoteNumber(self, value, qualifier):
        self.UpdateCallStatus(value, qualifier)

    def SetSpeakerTrackControl(self, value, qualifier):
        ValueStateValues = {
            'On': 'Activate',
            'Off': 'Deactivate'
        }

        SpeakerTrackControlCmdString = 'xCommand Cameras SpeakerTrack {0}\r'.format(ValueStateValues[value])
        self.__SetHelper('SpeakerTrackControl', SpeakerTrackControlCmdString, value, qualifier)

    def UpdateSpeakerTrackControl(self, value, qualifier):
        SpeakerTrackControlCmdString = 'xStatus Cameras SpeakerTrack Status\r'
        self.__UpdateHelper('SpeakerTrackControl', SpeakerTrackControlCmdString, qualifier)

    def __MatchSpeakerTrackControl(self, match, tag):
        ValueStateValues = {
            'Active': 'On',
            'Inactive': 'Off'
        }

        value = ValueStateValues[match.group(1).decode()]
        self.WriteStatus('SpeakerTrackControl', value, None)

    def SetSpeakerTrackMode(self, value, qualifier):
        ValueStateValues = {
            'Auto': 'Auto',
            'Off': 'Off'
        }

        SpeakerTrackModeCmdString = 'xConfiguration Cameras SpeakerTrack Mode: {0}\r'.format(ValueStateValues[value])
        self.__SetHelper('SpeakerTrackMode', SpeakerTrackModeCmdString, value, qualifier)

    def UpdateSubnetMask(self, value, qualifier):
        SubnetMaskCmdString = 'xStatus Network 1 IPv4 SubnetMask\r'
        self.__UpdateHelper('SubnetMask', SubnetMaskCmdString, qualifier)

    def __MatchSubnetMask(self, match, tag):
        value = match.group(1).decode()
        self.WriteStatus('SubnetMask', value, None)

    def SetDefaultCallRate(self, value, qualifier):
        ValueConstraints = {
            'Min': 64,
            'Max': 6000
        }

        if ValueConstraints['Min'] <= value <= ValueConstraints['Max']:
            DefaultCallRateCmdString = 'xConfiguration Conference 1 DefaultCall Rate: {0}\r'.format(value)
            self.__SetHelper('DefaultCallRate', DefaultCallRateCmdString, value, qualifier)
        else:
            print('Invalid Command')

    def UpdateDefaultCallRate(self, value, qualifier):
        self.__UpdateHelper('DefaultCallRate', 'xConfiguration Conference 1 DefaultCall Rate\r', qualifier)

    def __MatchDefaultCallRate(self, match, tag):
        self.WriteStatus('DefaultCallRate', int(match.group(1)), None)

    def SetMaxReceiveCallRate(self, value, qualifier):
        ValueConstraints = {
            'Min': 64,
            'Max': 6000
        }

        if ValueConstraints['Min'] <= value <= ValueConstraints['Max']:
            MaxReceiveCallRateCmdString = 'xConfiguration Conference 1 MaxReceiveCallRate: {0}\r'.format(value)
            self.__SetHelper('MaxReceiveCallRate', MaxReceiveCallRateCmdString, value, qualifier)
        else:
            print('Invalid Command')

    def UpdateMaxReceiveCallRate(self, value, qualifier):
        self.__UpdateHelper('MaxReceiveCallRate', 'xConfiguration Conference 1 MaxReceiveCallRate\r', qualifier)

    def __MatchMaxReceiveCallRate(self, match, tag):
        self.WriteStatus('MaxReceiveCallRate', int(match.group(1)), None)

    def SetMaxTotalReceiveCallRate(self, value, qualifier):
        ValueConstraints = {
            'Min': 64,
            'Max': 10000
        }

        if ValueConstraints['Min'] <= value <= ValueConstraints['Max']:
            MaxTotalReceiveCallRateCmdString = 'xConfiguration Conference 1 MaxTotalReceiveCallRate: {0}\r'.format(
                value)
            self.__SetHelper('MaxTotalReceiveCallRate', MaxTotalReceiveCallRateCmdString, value, qualifier)
        else:
            print('Invalid Command')

    def UpdateMaxTotalReceiveCallRate(self, value, qualifier):
        self.__UpdateHelper('MaxTotalReceiveCallRate', 'xConfiguration Conference 1 MaxTotalReceiveCallRate\r',
                            qualifier)

    def __MatchMaxTotalReceiveCallRate(self, match, tag):
        self.WriteStatus('MaxTotalReceiveCallRate', int(match.group(1)), None)

    def SetMaxTotalTransmitCallRate(self, value, qualifier):
        ValueConstraints = {
            'Min': 64,
            'Max': 10000
        }

        if ValueConstraints['Min'] <= value <= ValueConstraints['Max']:
            MaxTotalTransmitCallRateCmdString = 'xConfiguration Conference 1 MaxTotalTransmitCallRate: {0}\r'.format(
                value)
            self.__SetHelper('MaxTotalTransmitCallRate', MaxTotalTransmitCallRateCmdString, value, qualifier)
        else:
            print('Invalid Command')

    def UpdateMaxTotalTransmitCallRate(self, value, qualifier):
        self.__UpdateHelper('MaxTotalTransmitCallRate', 'xConfiguration Conference 1 MaxTotalTransmitCallRate\r',
                            qualifier)

    def __MatchMaxTotalTransmitCallRate(self, match, tag):
        self.WriteStatus('MaxTotalTransmitCallRate', int(match.group(1)), None)

    def SetMaxTransmitCallRate(self, value, qualifier):
        ValueConstraints = {
            'Min': 64,
            'Max': 6000
        }

        if ValueConstraints['Min'] <= value <= ValueConstraints['Max']:
            MaxTransmitCallRateCmdString = 'xConfiguration Conference 1 MaxTransmitCallRate: {0}\r'.format(value)
            self.__SetHelper('MaxTransmitCallRate', MaxTransmitCallRateCmdString, value, qualifier)
        else:
            print('Invalid Command')

    def UpdateMaxTransmitCallRate(self, value, qualifier):
        self.__UpdateHelper('MaxTransmitCallRate', 'xConfiguration Conference 1 MaxTransmitCallRate\r', qualifier)

    def __MatchMaxTransmitCallRate(self, match, tag):
        self.WriteStatus('MaxTransmitCallRate', int(match.group(1)), None)

    def __SetHelper(self, command, commandstring, value, qualifier):
        self.Send(commandstring)

    def __UpdateHelper(self, command, commandstring, qualifier):
        if self.initializationChk:
            self.OnConnected()
            self.initializationChk = False

        self.counter = self.counter + 1
        if self.counter > self.connectionCounter and self.connectionFlag:
            self.OnDisconnected()

        self.Send(commandstring)

    def __MatchError(self, match, tag):
        print(match.group(0).decode())

    def OnConnected(self):
        self.connectionFlag = True
        self.WriteStatus('ConnectionStatus', 'Connected')
        self.counter = 0

    def OnDisconnected(self):
        self.WriteStatus('ConnectionStatus', 'Disconnected')
        self.connectionFlag = False

    def csco_12_2083_SX20(self):
        self.DisplayModeStates = {
            'Dual': 'Dual',
            'Single': 'Single',
            'Dual Presentation Only': 'Dual Presentation Only',
            'Auto': 'Auto'
        }

        self.InputMuteStates = {
            'Microphone 1': 'Microphone 1',
            'Microphone 2': 'Microphone 2',
        }

        self.MicStates = {
            'Microphone 1': 'Microphone 1',
            'Microphone 2': 'Microphone 2',
        }

        self.PresentationStates = {
            '1': '1',
            '2': '2',
            'Stop': 'Stop',
        }

    def csco_12_2083_SX80(self):
        self.DisplayModeStates = {
            'Dual': 'Dual',
            'Single': 'Single',
            'Dual Presentation Only': 'Dual Presentation Only',
            'Triple': 'Triple',
            'Auto': 'Auto',
        }

        self.AudioOutputStates = {
            'Line 1': 'Line 1',
            'Line 2': 'Line 2',
            'Line 3': 'Line 3',
            'Line 4': 'Line 4',
            'Line 5': 'Line 5',
            'Line 6': 'Line 6',
            'HDMI 1': 'HDMI 1',
            'HDMI 2': 'HDMI 2',

        }

        self.LineStates = {
            'Line 1': 'Line 1',
            'Line 2': 'Line 2',
            'Line 3': 'Line 3',
            'Line 4': 'Line 4',
        }

        self.MicStates = {
            'Microphone 1': 'Microphone 1',
            'Microphone 2': 'Microphone 2',
            'Microphone 3': 'Microphone 3',
            'Microphone 4': 'Microphone 4',
            'Microphone 5': 'Microphone 5',
            'Microphone 6': 'Microphone 6',
            'Microphone 7': 'Microphone 7',
            'Microphone 8': 'Microphone 8',
        }

        self.InputMuteStates = {
            'Microphone 1': 'Microphone 1',
            'Microphone 2': 'Microphone 2',
            'Microphone 3': 'Microphone 3',
            'Microphone 4': 'Microphone 4',
            'Microphone 5': 'Microphone 5',
            'Microphone 6': 'Microphone 6',
            'Microphone 7': 'Microphone 7',
            'Microphone 8': 'Microphone 8',
            'Line 1': 'Line 1',
            'Line 2': 'Line 2',
            'Line 3': 'Line 3',
            'Line 4': 'Line 4',
        }

        self.PresentationStates = {
            '1': '1',
            '2': '2',
            '3': '3',
            '4': '4',
            '5': '5',
            'Stop': 'Stop',
        }

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
            if Status['Live'] != value:
                Status['Live'] = value
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
        if self.CheckMatchedString() and len(self._ReceiveBuffer) > 50000:
            self._ReceiveBuffer = b''

    # Add regular expression so that it can be check on incoming data from device.
    def AddMatchString(self, regex_string, callback, arg):
        if regex_string not in self._Compile_List:
            self._Compile_List[regex_string] = {'callback': callback, 'para': arg}

    # Check incoming unsolicited data to see if it was matched with device expectancy. 
    def CheckMatchedString(self):
        for regexString in self._Compile_List:
            while True:
                result = search(regexString, self._ReceiveBuffer)
                if result:
                    self._Compile_List[regexString]['callback'](result, self._Compile_List[regexString]['para'])
                    self._ReceiveBuffer = self._ReceiveBuffer.replace(result.group(0), b'')
                else:
                    break
        return True

    def MissingCredentialsLog(self, credential_type):
        if isinstance(self, EthernetClientInterface):
            port_info = 'IP Address: {0}:{1}'.format(self.IPAddress, self.IPPort)
        elif isinstance(self, SerialInterface):
            port_info = 'Host Alias: {0}\r\nPort: {1}'.format(self.Host.DeviceAlias, self.Port)
        else:
            return
        ProgramLog("{0} module received a request from the device for a {1}, "
                   "but device{1} was not provided.\n Please provide a device{1} "
                   "and attempt again.\n Ex: dvInterface.device{1} = '{1}'\n Please "
                   "review the communication sheet.\n {2}"
                   .format(__name__, credential_type, port_info), 'warning')


class SerialClass(SerialInterface, DeviceClass):
    def __init__(self, Host, Port, Baud=9600, Data=8, Parity='None', Stop=1, FlowControl='Off', CharDelay=0,
                 Model=None):
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


class SerialOverEthernetClass(EthernetClientInterface, DeviceClass):
    def __init__(self, Hostname, IPPort, Protocol='TCP', ServicePort=0, Model=None):
        EthernetClientInterface.__init__(self, Hostname, IPPort, Protocol, ServicePort)
        self.ConnectionType = 'Serial'
        DeviceClass.__init__(self)
        # Check if Model belongs to a subclass       
        if len(self.Models) > 0:
            if Model not in self.Models:
                print('Model mismatch')
            else:
                self.Models[Model]()