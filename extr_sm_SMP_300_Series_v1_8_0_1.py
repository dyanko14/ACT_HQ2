from extronlib.interface import SerialInterface, EthernetClientInterface
import re
from extronlib.system import Wait, ProgramLog

class DeviceClass:

    def __init__(self):

        self.Unidirectional = 'False'
        self.connectionCounter = 15
        self.DefaultResponseTimeout = 0.3
        self._compile_list = {}
        self.Subscription = {}
        self.ReceiveData = self.__ReceiveData
        self._ReceiveBuffer = b''
        self.counter = 0
        self.connectionFlag = True
        self.initializationChk = True
        self.Debug = False
        self.Models = {
            'SMP 351 3G-SDI': self.SMP351_3GSDI,
            'SMP 352 3G-SDI': self.SMP351_3GSDI,
            'SMP 351': self.SMP351_Base,
            'SMP 352': self.SMP351_Base,
        }

        self.devicePassword = None

        self.Commands = {
            'ConnectionStatus': {'Status': {}},
            'ActiveLayoutPreset': {'Status': {}},
            'Alarm': {'Parameters': ['Alarm Number'], 'Status': {}},
            'AlarmSeverity': {'Parameters': ['Alarm Number'], 'Status': {}},
            'AspectRatio': {'Parameters': ['Input'], 'Status': {}},
            'AudioBitrate': {'Status': {}},
            'AudioInputGain': {'Parameters': ['Type'], 'Status': {}},
            'AudioLevel': {'Parameters': ['L/R'], 'Status': {}},
            'AudioMuteInput': {'Parameters': ['Type', 'Channel', 'L/R'], 'Status': {}},
            'AudioMuteOutput': {'Parameters': ['L/R'], 'Status': {}},
            'AudioOutputGain': {'Parameters': ['Type'], 'Status': {}},
            'AutoImage': {'Parameters': ['Channel'], 'Status': {}},
            'BitrateControl': {'Parameters': ['Stream'], 'Status': {}},
            'ChapterMarker': {'Status': {}},
            'CPUUsage': {'Status': {}},
            'CurrentRecordingDuration': {'Status': {}},
            'EDID': {'Parameters': ['Input'], 'Status': {}},
            'Encoder': {'Status': {}},
            'ExecutiveMode': {'Status': {}},
            'FileDestination': {'Parameters': ['Drive'], 'Status': {}},
            'FTPUploadDestination': {'Status': {}},
            'GOPLength': {'Status': {}},
            'HDCPStatus': {'Parameters': ['Input'], 'Status': {}},
            'Input3Format': {'Status': {}},
            'InputA': {'Status': {}},
            'InputB': {'Status': {}},
            'InputStatus': {'Status': {}},
            'Metadata': {'Parameters': ['String'], 'Status': {}},
            'MetadataStatus': {'Parameters': ['Type'], 'Status': {}},
            'RecallLayoutPreset': {'Parameters': ['Inputs'], 'Status': {}},
            'RecallEncoderPreset': {'Parameters': ['Stream'], 'Status': {}},
            'RecallUserPreset': {'Parameters': ['Channel'], 'Status': {}},
            'Record': {'Status': {}},
            'RecordControl': {'Status': {}},
            'RecordDestination': {'Status': {}},
            'RecordDualControl': {'Status': {}},
            'RecordExtend': {'Status': {}},
            'RecordingMode': {'Status': {}},
            'RecordingVideoFrameRate': {'Status': {}},
            'RecordResolution': {'Status': {}},
            'RemainingFreeDiskSpace': {'Parameters':['Drive','Unit'], 'Status': {}},
            'RemainingRecordingTime': {'Parameters': ['Drive'], 'Status': {}},
            'StreamControl': {'Parameters': ['Stream'], 'Status': {}},
            'SwapWindows': {'Status': {}},
            'ThumbnailSize': {'Status': {}},
            'VideoBitrate': {'Parameters': ['Stream'], 'Status': {}},
            'VideoMute': {'Parameters': ['Channel'], 'Status': {}},
        }

        self.VerboseDisabled = True
        self.PasswdPromptCount = 0
        self.Authenticated = 'Not Needed'

        if self.Unidirectional == 'False':
            self.AddMatchString(re.compile(b'[78]Rpr(0[1-9]|1[0-6])\r\n'), self.__MatchActiveLayoutPreset, None)
            self.AddMatchString(re.compile(b'Inf39(?:\*\<name\:(video_loss|hdcp_video|audio_loss|disk_space|disk_error|record_halt|temperature\.internal|cpu_usage|ntp\.sync|usb\.front\.overcurrent|usb\.rear\.overcurrent|usb\.keyboard\.overcurrent|usb\.mouse\.overcurrent|auth_failures|sched_server)\,level\:(warning|critical|info|emergency)\>)+\r\n'), self.__MatchAlarm, None)
            self.AddMatchString(re.compile(b'Inf39\*(None active)\r\n'), self.__MatchAlarm, "No Alarm")
            self.AddMatchString(re.compile(b'Aspr0(1|2|3|4|5)\*0(1|2|3)\r\n'), self.__MatchAspectRatio, None)
            self.AddMatchString(re.compile(b'BitrA1\*(080|096|128|192|256|320)\r\n'), self.__MatchAudioBitrate, None)
            self.AddMatchString(re.compile(b'DsG(40000|40001|40002|40003|40004|40005|40005|40006|40007)\*(\-?\d{1,3})\r\n'), self.__MatchAudioInputGain, None)
            self.AddMatchString(re.compile(b'DsG(60000|60001)\*(\-?\d{1,3})\r\n'), self.__MatchAudioOutputGain, None)
            self.AddMatchString(re.compile(b'Inf34\*(-?\d{1,4})\*(-?\d{1,4})\r\n'), self.__MatchAudioLevel, None)
            self.AddMatchString(re.compile(b'DsM4000(0|1|2|3|4|5|6|7)\*(0|1)\r\n'), self.__MatchAudioMuteInput, None)
            self.AddMatchString(re.compile(b'DsM6000(0|1)\*(0|1)\r\n'), self.__MatchAudioMuteOutput, None)
            self.AddMatchString(re.compile(b'Brct(1|2|3)\*(0|1|2)\r\n'), self.__MatchBitrateControl, None)
            self.AddMatchString(re.compile(b'Inf11\*(\d{1,3})\r\n'), self.__MatchCPUUsage, None)
            self.AddMatchString(re.compile(b'Inf35\*(\d{1,2})\:(\d{1,2})\:(\d{1,2})\r\n'), self.__MatchCurrentRecordingDuration, None)
            self.AddMatchString(re.compile(b'EdidA(01|02|04)\*(\d{2})\r\n'), self.__MatchEDID, None)
            self.AddMatchString(re.compile(b'Encm1\*(1|0)\r\n'), self.__MatchEncoder, None)
            self.AddMatchString(re.compile(b'Exe(0|1|2|3)\r\n'), self.__MatchExecutiveMode, None)
            self.AddMatchString(re.compile(b'Inf\*<.*?>\*<.*?>\*<(internal|usbfront|usbrear|auto|N/A).*?(?:\*?(internal|usbfront|usbrear|N/A|\*))?.*?>\*(?:<([0-9]*)(\*[0-9]*)?(\*N/A)?>\*<.*?>\*<.*?>|<\d*\:\d*\:\d*>\*<\d*\:\d*\:\d*>)?\r\n'), self.__MatchFileDestination, None)
            self.AddMatchString(re.compile(b'Inf38\*(None|.*ftp|.*?,cifs)\r\n'), self.__MatchFTPUploadDestination, None)
            self.AddMatchString(re.compile(b'Gopl1\*(\d{1,2})\r\n'), self.__MatchGOPLength, None)
            self.AddMatchString(re.compile(b'HdcpI(01|02|04)\*(0|1|2)\r\n'), self.__MatchHDCPStatus, None)
            self.AddMatchString(re.compile(b'Typ03\*(01|02|03)\r\n'), self.__MatchInput3Format, None)
            self.AddMatchString(re.compile(b'Inf32\*ChA(1|2)\*ChB(3|4|5)\r\n'), self.__MatchInputStatus, 'Update')
            self.AddMatchString(re.compile(b'In0(1|2|3|4|5)\*0(1|2)\r\n'), self.__MatchInputStatus, 'Set')
            self.AddMatchString(re.compile(b'RcdrY(0|1|2)\r\n'), self.__MatchRecord, None)
            self.AddMatchString(re.compile(b'RcdrX1\*(?P<value>0|1|2)\r\n'), self.__MatchRecordControl, None)
            self.AddMatchString(re.compile(b'RcdrD(00|01|02|03|12|13)\r\n'), self.__MatchRecordDestination, None)
            self.AddMatchString(re.compile(b'RcdrX2\*(0|1)\r\n'), self.__MatchRecordDualControl, None)
            self.AddMatchString(re.compile(b'Smod1\*(2|1)\r\n'), self.__MatchRecordingMode, None)
            self.AddMatchString(re.compile(b'Vfrm1\*(1|2|3|4|5|6|7|8)\r\n'), self.__MatchRecordingVideoFrameRate, None)
            self.AddMatchString(re.compile(b'Vres1\*(0|1|2|3|4|5|6|99)\r\n'), self.__MatchRecordResolution, None)
            self.AddMatchString(re.compile(b'Inf36\*(?:internal|usbfront|usbrear)?.*? (\d+)\:(\d{1,2})\:(\d{1,2})(?:\*(?:internal|usbfront|usbrear|).*? (\d+)\:(\d{1,2})\:(\d{1,2}))?\r\n'), self.__MatchRemainingRecordingTime, None)
            self.AddMatchString(re.compile(b'Strc(?P<type>1|2|3)\*(?P<value>0|1)\r\n'), self.__MatchStreamControl, None)
            self.AddMatchString(re.compile(b'RcdrT0(0|1)\r\n'), self.__MatchThumbnailSize, None)
            self.AddMatchString(re.compile(b'BitrV(1|2|3)\*(\d{3,5})\r\n'), self.__MatchVideoBitrate, None)
            self.AddMatchString(re.compile(b'Vmt0(1|2)\*(00|01)\r\n'), self.__MatchVideoMute, None)

            self.findCondition = re.compile(b'\*\<name\:(video_loss|hdcp_video|audio_loss|disk_space|disk_error|record_halt|temperature\.internal|cpu_usage|ntp\.sync|usb\.front\.overcurrent|usb\.rear\.overcurrent|usb\.keyboard\.overcurrent|usb\.mouse\.overcurrent|auth_failures|sched_server)\,level\:(warning|critical|info|emergency)\>')

            self.AddMatchString(re.compile(b'E(\d+)\r\n'), self.__MatchErrors, None)
            self.AddMatchString(re.compile(b'Vrb3\r\n'), self.__MatchVerboseMode, None)

            if 'Serial' != self.ConnectionType:
                self.AddMatchString(re.compile(b'Password:'), self.__MatchPassword, None)
                self.AddMatchString(re.compile(b'Login Administrator\r\n'), self.__MatchLoginAdmin, None)
                self.AddMatchString(re.compile(b'Login User\r\n'), self.__MatchLoginUser, None)

        self.MetadataStatusRegex = re.compile('RcdrM(1?[0-9]\*(?P<value>.*))?\r\n')

    def __MatchPassword(self, match, tag):
        self.PasswdPromptCount += 1
        if self.PasswdPromptCount > 1:
            print('Log in failed. Please supply proper Admin password')
        else:
            if self.devicePassword:
                self.Send(self.devicePassword + '\r\n')
            else:
                self.MissingCredentialsLog('Password')
        self.Authenticated = 'None'

    def __MatchLoginAdmin(self, match, tag):
        self.Authenticated = 'Admin'
        self.PasswdPromptCount = 0

    def __MatchLoginUser(self, match, tag):
        self.Authenticated = 'User'
        self.PasswdPromptCount = 0
        print('Logged in as User. May have limited functionality.')

    def __MatchVerboseMode(self, match, qualifier):
        self.OnConnected()
        self.VerboseDisabled = False

    def __MatchActiveLayoutPreset(self, match, tag):
        ValueStateValues = {
            '01': '1',
            '02': '2',
            '03': '3',
            '04': '4',
            '05': '5',
            '06': '6',
            '07': '7',
            '08': '8',
            '09': '9',
            '10': '10',
            '11': '11',
            '12': '12',
            '13': '13',
            '14': '14',
            '15': '15',
            '16': '16'
        }

        value = ValueStateValues[match.group(1).decode()]
        self.WriteStatus('ActiveLayoutPreset', value, None)

    def UpdateAlarm(self, value, qualifier):
        AlarmCmdString = '39i'
        self.__UpdateHelper('Alarm', AlarmCmdString, value, qualifier)

    def __MatchAlarm(self, match, tag):

        LevelStates = {
            'warning': 'Warning',
            'critical': 'Critical',
            'info': 'Info',
            'emergency': 'Emergency'
        }

        ValueStateValues = {
            'video_loss': 'Video Loss',
            'audio_loss': 'Audio Loss',
            'disk_space': 'Disk Space',
            'record_halt': 'Halt Recording',
            'ntp.sync': 'NTP Sync',
            'auth_failures': 'Authentication Failures',
            'disk_error': 'Disk Error',
            'temperature.internal': 'Internal Temperature',
            'hdcp_video': 'HDCP',
            'cpu_usage': 'CPU Usage',
            'usb.front.overcurrent': 'USB Front Overcurrent',
            'usb.rear.overcurrent': 'USB Rear Overcurrent',
            'usb.keyboard.overcurrent': 'USB Keyboard Overcurrent',
            'usb.mouse.overcurrent': 'USB Mouse Overcurrent',
            'sched_server': 'Schedule Server'
        }

        if tag == 'No Alarm':
            for x in range(0, 12):
                qualifier = {'Alarm Number': str(x + 1)}
                self.WriteStatus('Alarm', 'None Active', qualifier)
                self.WriteStatus('AlarmSeverity', 'Cleared', qualifier)
        else:
            alarmList = re.findall(self.findCondition, match.group(0))

            for enum, x in enumerate(alarmList):
                qualifier = {'Alarm Number': str(enum + 1)}
                self.WriteStatus('Alarm', ValueStateValues[x[0].decode()], qualifier)
                self.WriteStatus('AlarmSeverity', LevelStates[x[1].decode()], qualifier)

            for x in range(len(alarmList), 12):
                qualifier = {'Alarm Number': str(x + 1)}
                self.WriteStatus('Alarm', 'None Active', qualifier)
                self.WriteStatus('AlarmSeverity', 'Cleared', qualifier)

    def UpdateAlarmSeverity(self, value, qualifier):
        self.UpdateAlarm(value, qualifier)

    def SetAspectRatio(self, value, qualifier):

        InputStates = {
            '1': '1',
            '2': '2',
            '3': '3',
            '4': '4',
            '5': '5',
        }

        ValueStateValues = {
            'Fill': '1',
            'Follow': '2',
            'Fit': '3'
        }

        AspectRatioCmdString = 'w{0}*{1}ASPR\r'.format(InputStates[qualifier['Input']], ValueStateValues[value])
        self.__SetHelper('AspectRatio', AspectRatioCmdString, value, qualifier)

    def UpdateAspectRatio(self, value, qualifier):

        InputStates = {
            '1': '1',
            '2': '2',
            '3': '3',
            '4': '4',
            '5': '5',
        }
        AspectRatioCmdString = 'w{0}ASPR\r'.format(InputStates[qualifier['Input']])
        self.__UpdateHelper('AspectRatio', AspectRatioCmdString, value, qualifier)

    def __MatchAspectRatio(self, match, tag):

        ValueStateValues = {
            '1': 'Fill',
            '2': 'Follow',
            '3': 'Fit'
        }

        value = ValueStateValues[match.group(2).decode()]
        self.WriteStatus('AspectRatio', value, {'Input': match.group(1).decode()})

    def SetAudioBitrate(self, value, qualifier):

        ValueStateValues = {
            '80': '80',
            '96': '96',
            '128': '128',
            '192': '192',
            '256': '256',
            '320': '320'
        }

        AudioBitrateCmdString = 'wA1*{0}BITR\r'.format(ValueStateValues[value])
        self.__SetHelper('AudioBitrate', AudioBitrateCmdString, value, qualifier)

    def UpdateAudioBitrate(self, value, qualifier):

        AudioBitrateCmdString = 'wA1BITR\r'
        self.__UpdateHelper('AudioBitrate', AudioBitrateCmdString, value, qualifier)

    def __MatchAudioBitrate(self, match, tag):

        ValueStateValues = {
            '080': '80',
            '096': '96',
            '128': '128',
            '192': '192',
            '256': '256',
            '320': '320'
        }

        value = ValueStateValues[match.group(1).decode()]
        self.WriteStatus('AudioBitrate', value, None)

    def SetAudioInputGain(self, value, qualifier):

        TypeStates = {
            'Audio Channel A (L)': '40000',
            'Audio Channel A (R)': '40001',
            'Digital Channel A (L)': '40002',
            'Digital Channel A (R)': '40003',
            'Audio Channel B (L)': '40004',
            'Audio Channel B (R)': '40005',
            'Digital Channel B (L)': '40006',
            'Digital Channel B (R)': '40007'
        }

        ValueConstraints = {
            'Min': -18,
            'Max': 24
        }

        if ValueConstraints['Min'] <= value <= ValueConstraints['Max']:
            AudioInputGainCmdString = 'wG{0}*{1}AU\r'.format(TypeStates[qualifier['Type']], value * 10)
            self.__SetHelper('AudioInputGain', AudioInputGainCmdString, value, qualifier)
        else:
            print('Invalid Command for SetAudioInputGain')

    def UpdateAudioInputGain(self, value, qualifier):

        TypeStates = {
            'Audio Channel A (L)': '40000',
            'Audio Channel A (R)': '40001',
            'Digital Channel A (L)': '40002',
            'Digital Channel A (R)': '40003',
            'Audio Channel B (L)': '40004',
            'Audio Channel B (R)': '40005',
            'Digital Channel B (L)': '40006',
            'Digital Channel B (R)': '40007'
        }

        AudioInputGainCmdString = 'wG{0}AU\r'.format(TypeStates[qualifier['Type']])
        self.__UpdateHelper('AudioInputGain', AudioInputGainCmdString, value, qualifier)

    def __MatchAudioInputGain(self, match, tag):

        TypeStates = {
            '40000': 'Audio Channel A (L)',
            '40001': 'Audio Channel A (R)',
            '40002': 'Digital Channel A (L)',
            '40003': 'Digital Channel A (R)',
            '40004': 'Audio Channel B (L)',
            '40005': 'Audio Channel B (R)',
            '40006': 'Digital Channel B (L)',
            '40007': 'Digital Channel B (R)',
        }

        value = int(int(match.group(2).decode()) / 10)
        self.WriteStatus('AudioInputGain', value, {'Type': TypeStates[match.group(1).decode()]})

    def UpdateAudioLevel(self, value, qualifier):

        AudioLevelCmdString = '34i'
        self.__UpdateHelper('AudioLevel', AudioLevelCmdString, value, qualifier)

    def __MatchAudioLevel(self, match, tag):

        Left = int(match.group(1).decode()) / 10
        Right = int(match.group(2).decode()) / 10
        self.WriteStatus('AudioLevel', Left, {'L/R': 'Left'})
        self.WriteStatus('AudioLevel', Right, {'L/R': 'Right'})

    def SetAudioMuteInput(self, value, qualifier):

        TypeStates = {
            'Audio': 0,
            'Digital': 2
        }

        ChannelStates = {
            'A': 0,
            'B': 4
        }

        LRStates = {
            'Left': 0,
            'Right': 1
        }

        ValueStateValues = {
            'On': '1',
            'Off': '0'
        }

        Shift = ChannelStates[qualifier['Channel']] + TypeStates[qualifier['Type']] + LRStates[qualifier['L/R']]

        AudioMuteInputCmdString = 'wM4000{0}*{1}AU\r'.format(Shift, ValueStateValues[value])
        self.__SetHelper('AudioMuteInput', AudioMuteInputCmdString, value, qualifier)

    def UpdateAudioMuteInput(self, value, qualifier):

        TypeStates = {
            'Audio': 0,
            'Digital': 2
        }

        ChannelStates = {
            'A': 0,
            'B': 4
        }

        LRStates = {
            'Left': 0,
            'Right': 1
        }

        Shift = ChannelStates[qualifier['Channel']] + TypeStates[qualifier['Type']] + LRStates[qualifier['L/R']]

        AudioMuteInputCmdString = 'wM4000{0}AU\r'.format(Shift)
        self.__UpdateHelper('AudioMuteInput', AudioMuteInputCmdString, value, qualifier)

    def __MatchAudioMuteInput(self, match, tag):

        Left = [0, 2, 4, 6]
        Digital = [2, 3, 6, 7]

        State = {
            '1': 'On',
            '0': 'Off'
        }

        if 0 <= int(match.group(1).decode()) <= 3:
            Channel = 'A'
        elif 4 <= int(match.group(1).decode()) <= 7:
            Channel = 'B'

        if int(match.group(1).decode()) in Digital:
            Type = 'Digital'
        else:
            Type = 'Audio'

        if int(match.group(1).decode()) in Left:
            LR = 'Left'
        else:
            LR = 'Right'

        qualifier = {'Channel': Channel, 'Type': Type, 'L/R': LR}

        value = State[match.group(2).decode()]
        self.WriteStatus('AudioMuteInput', value, qualifier)

    def SetAudioMuteOutput(self, value, qualifier):

        LRStates = {
            'Left': '0',
            'Right': '1'
        }

        ValueStateValues = {
            'On': '1',
            'Off': '0'
        }

        AudioMuteOutputCmdString = 'wM6000{0}*{1}AU\r'.format(LRStates[qualifier['L/R']], ValueStateValues[value])
        self.__SetHelper('AudioMuteOutput', AudioMuteOutputCmdString, value, qualifier)

    def UpdateAudioMuteOutput(self, value, qualifier):

        LRStates = {
            'Left': '0',
            'Right': '1'
        }
        AudioMuteOutputCmdString = 'wM6000{0}AU\r'.format(LRStates[qualifier['L/R']])
        self.__UpdateHelper('AudioMuteOutput', AudioMuteOutputCmdString, value, qualifier)

    def __MatchAudioMuteOutput(self, match, tag):

        LRStates = {
            '0': 'Left',
            '1': 'Right'
        }

        ValueStateValues = {
            '1': 'On',
            '0': 'Off'
        }

        qualifier = {'L/R': LRStates[match.group(1).decode()]}
        value = ValueStateValues[match.group(2).decode()]
        self.WriteStatus('AudioMuteOutput', value, qualifier)

    def SetAudioOutputGain(self, value, qualifier):

        TypeStates = {
            'Output (L)': '60000',
            'Output (R)': '60001'
        }

        ValueConstraints = {
            'Min': -100,
            'Max': 0
        }

        if ValueConstraints['Min'] <= value <= ValueConstraints['Max']:
            AudioOutputGainCmdString = 'wG{0}*{1}AU\r'.format(TypeStates[qualifier['Type']], value * 10)
            self.__SetHelper('AudioOutputGain', AudioOutputGainCmdString, value, qualifier)
        else:
            print('Invalid Command for SetAudioOutputGain')

    def UpdateAudioOutputGain(self, value, qualifier):

        TypeStates = {
            'Output (L)': '60000',
            'Output (R)': '60001'
        }

        AudioOutputGainCmdString = 'wG{0}AU\r'.format(TypeStates[qualifier['Type']])
        self.__UpdateHelper('AudioOutputGain', AudioOutputGainCmdString, value, qualifier)

    def __MatchAudioOutputGain(self, match, tag):

        TypeStates = {
            '60000': 'Output (L)',
            '60001': 'Output (R)'
        }

        value = int(match.group(2).decode()) / 10
        self.WriteStatus('AudioOutputGain', value, {'Type': TypeStates[match.group(1).decode()]})

    def SetAutoImage(self, value, qualifier):

        State = {
            'A': '1',
            'B': '2',
        }
        Channel = qualifier['Channel']
        CmdString = '{0}A\r'.format(State[Channel])
        self.__SetHelper('AutoImage', CmdString, value, qualifier)

    def SetBitrateControl(self, value, qualifier):

        InputState = {
            'Archive A': '1',
            'Archive B': '2',
            'Confidence A': '3'
        }

        ValueStateValues = {
            'VBR': '0',
            'CVBR': '1',
            'CBR': '2'
        }

        BitrateControlCmdString = 'w{0}*{1}BRCT\r'.format(InputState[qualifier['Stream']], ValueStateValues[value])
        self.__SetHelper('BitrateControl', BitrateControlCmdString, value, qualifier)

    def UpdateBitrateControl(self, value, qualifier):

        InputState = {
            'Archive A': '1',
            'Archive B': '2',
            'Confidence A': '3'
        }

        BitrateControlCmdString = 'w{0}BRCT\r'.format(InputState[qualifier['Stream']])
        self.__UpdateHelper('BitrateControl', BitrateControlCmdString, value, qualifier)

    def __MatchBitrateControl(self, match, tag):

        InputState = {
            '1': 'Archive A',
            '2': 'Archive B',
            '3': 'Confidence A'
        }

        ValueStateValues = {
            '0': 'VBR',
            '1': 'CVBR',
            '2': 'CBR'
        }

        value = ValueStateValues[match.group(2).decode()]
        self.WriteStatus('BitrateControl', value, {'Stream': InputState[match.group(1).decode()]})

    def SetChapterMarker(self, value, qualifier):

        CmdString = 'wBRCDR\r'
        self.__SetHelper('ChapterMarker', CmdString, value, qualifier)

    def UpdateCPUUsage(self, value, qualifier):

        CPUUsageCmdString = '11i'
        self.__UpdateHelper('CPUUsage', CPUUsageCmdString, value, qualifier)

    def __MatchCPUUsage(self, match, tag):

        value = int(match.group(1).decode())
        self.WriteStatus('CPUUsage', value, None)

    def UpdateCurrentRecordingDuration(self, value, qualifier):

        CmdString = '35i'
        self.__UpdateHelper('CurrentRecordingDuration', CmdString, value, qualifier)

    def __MatchCurrentRecordingDuration(self, match, tag):

        value = match.group(1).decode() + ':' + match.group(2).decode() + ':' + match.group(3).decode()
        self.WriteStatus('CurrentRecordingDuration', value, None)

    def SetEDID(self, value, qualifier):

        InputStates = {
            '1': '1',
            '2': '2',
            '4': '4',
        }

        ValueStateValues = {
            '800x600 60HZ PC DVI': '1',
            '1024x768 60HZ PC DVI': '2',
            '1280x720 60HZ PC DVI': '3',
            '1280x768 60HZ PC DVI': '4',
            '1280x800 60HZ PC DVI': '5',
            '1280x1024 60HZ PC DVI': '6',
            '1360x768 60HZ PC DVI': '7',
            '1366x768 60HZ PC DVI': '8',
            '1400x1050 60HZ PC DVI': '9',
            '1440x900 60HZ PC DVI': '10',
            '1600x900 60HZ PC DVI': '11',
            '1600x1200 60HZ PC DVI': '12',
            '1680x1050 60HZ PC DVI': '13',
            '1920x1080 60HZ PC DVI': '14',
            '1920x1200 60HZ PC DVI': '15',
            '2048x1080 60HZ PC DVI': '16',
            '800x600 60HZ PC HDMI': '17',
            '1024x768 60HZ PC HDMI': '18',
            '1280x768 60HZ PC HDMI': '19',
            '1280x800 60HZ PC HDMI': '20',
            '1280x1024 60HZ PC HDMI': '21',
            '1360x768 60HZ PC HDMI': '22',
            '1366x768 60HZ PC HDMI': '23',
            '1400x1050 60HZ PC HDMI': '24',
            '1440x900 60HZ PC HDMI': '25',
            '1600x900 60HZ PC HDMI': '26',
            '1600x1200 60HZ PC HDMI': '27',
            '1680x1050 60HZ PC HDMI': '28',
            '1920x1200 60HZ PC HDMI': '29',
            '2048x1080 60HZ PC HDMI': '30',
            '480p 60HZ HDTV HDMI': '31',
            '576p 50HZ HDTV HDMI': '32',
            '720p 50HZ HDTV HDMI': '33',
            '720p 60HZ HDTV HDMI': '34',
            '1080i 50HZ HDTV HDMI': '35',
            '1080i 60HZ HDTV HDMI': '36',
            '1080p 50/25HZ HDTV HDMI': '37',
            '1080p 50HZ HDTV HDMI': '38',
            '1080p 60/24HZ HDTV HDMI': '39',
            '1080p 60HZ HDTV HDMI': '40',
            'Output 1': '41',
            'User Loaded Slot 1': '42',
            'User Loaded Slot 2': '43',
            'User Loaded Slot 3': '44'
        }

        EDIDCmdString = 'wA{0}*{1}EDID\r'.format(InputStates[qualifier['Input']], ValueStateValues[value])
        self.__SetHelper('EDID', EDIDCmdString, value, qualifier)

    def UpdateEDID(self, value, qualifier):

        InputStates = {
            '1': '1',
            '2': '2',
            '4': '4',
        }

        EDIDCmdString = 'wA{0}EDID\r'.format(InputStates[qualifier['Input']])
        self.__UpdateHelper('EDID', EDIDCmdString, value, qualifier)

    def __MatchEDID(self, match, tag):

        InputStates = {
            '01': '1',
            '02': '2',
            '04': '4',
        }

        ValueStateValues = {
            '01': '800x600 60HZ PC DVI',
            '02': '1024x768 60HZ PC DVI',
            '03': '1280x720 60HZ PC DVI',
            '04': '1280x768 60HZ PC DVI',
            '05': '1280x800 60HZ PC DVI',
            '06': '1280x1024 60HZ PC DVI',
            '07': '1360x768 60HZ PC DVI',
            '08': '1366x768 60HZ PC DVI',
            '09': '1400x1050 60HZ PC DVI',
            '10': '1440x900 60HZ PC DVI',
            '11': '1600x900 60HZ PC DVI',
            '12': '1600x1200 60HZ PC DVI',
            '13': '1680x1050 60HZ PC DVI',
            '14': '1920x1080 60HZ PC DVI',
            '15': '1920x1200 60HZ PC DVI',
            '16': '2048x1080 60HZ PC DVI',
            '17': '800x600 60HZ PC HDMI',
            '18': '1024x768 60HZ PC HDMI',
            '19': '1280x768 60HZ PC HDMI',
            '20': '1280x800 60HZ PC HDMI',
            '21': '1280x1024 60HZ PC HDMI',
            '22': '1360x768 60HZ PC HDMI',
            '23': '1366x768 60HZ PC HDMI',
            '24': '1400x1050 60HZ PC HDMI',
            '25': '1440x900 60HZ PC HDMI',
            '26': '1600x900 60HZ PC HDMI',
            '27': '1600x1200 60HZ PC HDMI',
            '28': '1680x1050 60HZ PC HDMI',
            '29': '1920x1200 60HZ PC HDMI',
            '30': '2048x1080 60HZ PC HDMI',
            '31': '480p 60HZ HDTV HDMI',
            '32': '576p 50HZ HDTV HDMI',
            '33': '720p 50HZ HDTV HDMI',
            '34': '720p 60HZ HDTV HDMI',
            '35': '1080i 50HZ HDTV HDMI',
            '36': '1080i 60HZ HDTV HDMI',
            '37': '1080p 50/25HZ HDTV HDMI',
            '38': '1080p 50HZ HDTV HDMI',
            '39': '1080p 60/24HZ HDTV HDMI',
            '40': '1080p 60HZ HDTV HDMI',
            '41': 'Output 1',
            '42': 'User Loaded Slot 1',
            '43': 'User Loaded Slot 2',
            '44': 'User Loaded Slot 3'
        }

        value = ValueStateValues[match.group(2).decode()]
        self.WriteStatus('EDID', value, {'Input': InputStates[match.group(1).decode()]})

    def SetEncoder(self, value, qualifier):

        ValueStateValues = {
            'Composite': '0',
            'Dual': '1'
        }

        EncoderCmdString = 'w1*{0}ENCM\r'.format(ValueStateValues[value])
        self.__SetHelper('Encoder', EncoderCmdString, value, qualifier)

    def UpdateEncoder(self, value, qualifier):

        EncoderCmdString = 'w1ENCM\r'
        self.__UpdateHelper('Encoder', EncoderCmdString, value, qualifier)

    def __MatchEncoder(self, match, tag):

        ValueStateValues = {
            '0': 'Composite',
            '1': 'Dual'
        }

        value = ValueStateValues[match.group(1).decode()]
        self.WriteStatus('Encoder', value, None)

    def SetExecutiveMode(self, value, qualifier):

        ValueStateValues = {
            'Off': '0',
            'Complete Lock Out': '1',
            'Menu Lock Out': '2',
            'Recording Control Only': '3'
        }

        ExecutiveModeCmdString = '{0}X'.format(ValueStateValues[value])
        self.__SetHelper('ExecutiveMode', ExecutiveModeCmdString, value, qualifier)

    def UpdateExecutiveMode(self, value, qualifier):

        ExecutiveModeCmdString = 'X'
        self.__UpdateHelper('ExecutiveMode', ExecutiveModeCmdString, value, qualifier)

    def __MatchExecutiveMode(self, match, tag):

        ValueStateValues = {
            '0': 'Off',
            '1': 'Complete Lock Out',
            '2': 'Menu Lock Out',
            '3': 'Recording Control Only'
        }

        value = ValueStateValues[match.group(1).decode()]
        self.WriteStatus('ExecutiveMode', value, None)

    def UpdateFileDestination(self, value, qualifier):
        FileDestinationCmdString = 'i'
        self.__UpdateHelper('FileDestination', FileDestinationCmdString, value, qualifier)

    def __MatchFileDestination(self, match, tag):

        ValueStateValues = {
            'N/A': 'NA',
            'internal': 'Internal',
            'usbfront': 'Front USB',
            'usbrear': 'Rear USB',
            'auto': 'Auto',
            '*': 'Drive not inserted while USB is set as Destination',
            '': 'Drive not inserted while USB is set as Destination'
        }

        value = ValueStateValues[match.group(1).decode()]
        self.WriteStatus('FileDestination', value, {'Drive': 'Primary'})

        if value == 'Auto':
            self.WriteStatus('RemainingFreeDiskSpace', 0.00, {'Drive': 'Primary', 'Unit': 'MB'})
            self.WriteStatus('RemainingFreeDiskSpace', 0.00, {'Drive': 'Primary', 'Unit': 'GB'})
            self.WriteStatus('FileDestination', 'NA', {'Drive': 'Secondary'})
            self.WriteStatus('RemainingFreeDiskSpace', 0.00, {'Drive': 'Secondary', 'Unit': 'MB'})
            self.WriteStatus('RemainingFreeDiskSpace', 0.00, {'Drive': 'Secondary', 'Unit': 'GB'})
        else:
            if value != 'NA' and value != 'Drive not inserted while USB is set as Destination':

                self.WriteStatus('RemainingFreeDiskSpace', round(int(match.group(3).decode()) / 1024, 2), {'Drive': 'Primary', 'Unit': 'MB'})
                self.WriteStatus('RemainingFreeDiskSpace', round(int(match.group(3).decode()) / (1024 * 1024), 2), {'Drive': 'Primary', 'Unit': 'GB'})
            else:
                self.WriteStatus('RemainingFreeDiskSpace', 0.00, {'Drive' : 'Primary', 'Unit': 'MB'})

            if match.group(2) is not None:
                value2 = ValueStateValues[match.group(2).decode()]
                self.WriteStatus('FileDestination', value2, {'Drive': 'Secondary'})
                if match.group(4) is not None:
                    self.WriteStatus('RemainingFreeDiskSpace', round(int(match.group(4).decode().replace('*', '')) / 1024, 2),{'Drive': 'Secondary', 'Unit': 'MB'})
                    self.WriteStatus('RemainingFreeDiskSpace', round(int(match.group(4).decode().replace('*', '')) / (1024 * 1024), 2),{'Drive': 'Secondary', 'Unit': 'GB'})
                elif match.group(5) is not None:
                    self.WriteStatus('RemainingFreeDiskSpace', 0.00, {'Drive': 'Secondary', 'Unit': 'MB'})
                    self.WriteStatus('RemainingFreeDiskSpace', 0.00, {'Drive': 'Secondary', 'Unit': 'GB'})

            else:
                self.WriteStatus('RemainingFreeDiskSpace', 0.00, {'Drive': 'Secondary', 'Unit': 'MB'})
                self.WriteStatus('RemainingFreeDiskSpace', 0.00, {'Drive': 'Secondary', 'Unit': 'GB'})
                self.WriteStatus('FileDestination', 'NA', {'Drive': 'Secondary'})

    def UpdateFTPUploadDestination(self, value, qualifier):

        FTPUploadDestinationCmdString = '38i'
        self.__UpdateHelper('FTPUploadDestination', FTPUploadDestinationCmdString, value, qualifier)

    def __MatchFTPUploadDestination(self, match, tag):

        value = match.group(1).decode()
        self.WriteStatus('FTPUploadDestination', value, None)

    def SetGOPLength(self, value, qualifier):

        ValueConstraints = {
            'Min': 1,
            'Max': 30
        }

        if ValueConstraints['Min'] <= value <= ValueConstraints['Max']:
            GOPLengthCmdString = 'w1*{0}GOPL\r'.format(value)
            self.__SetHelper('GOPLength', GOPLengthCmdString, value, qualifier)
        else:
            print('Invalid Command for SetGOPLength')

    def UpdateGOPLength(self, value, qualifier):

        GOPLengthCmdString = 'w1GOPL\r'
        self.__UpdateHelper('GOPLength', GOPLengthCmdString, value, qualifier)

    def __MatchGOPLength(self, match, tag):

        value = int(match.group(1).decode())
        self.WriteStatus('GOPLength', value, None)

    def UpdateHDCPStatus(self, value, qualifier):

        if qualifier['Input'] in ('1', '2', '4'):
            HDCPStatusCmdString = 'wI{0}HDCP\r'.format(qualifier['Input'])
            self.__UpdateHelper('HDCPStatus', HDCPStatusCmdString, value, qualifier)
        else:
            print('Invalid Command for UpdateHDCPStatus')

    def __MatchHDCPStatus(self, match, tag):

        InputStates = {
            '01': '1',
            '02': '2',
            '04': '4'
        }

        ValueStateValues = {
            '0': 'No Source Detected',
            '1': 'HDCP Detected',
            '2': 'No HDCP'
        }

        qualifier = {'Input': InputStates[match.group(1).decode()]}
        value = ValueStateValues[match.group(2).decode()]
        self.WriteStatus('HDCPStatus', value, qualifier)

    def SetInput3Format(self, value, qualifier):

        ValueStateValues = {
            'YUVp/HDTV': '1',
            'YUVi': '2',
            'Composite': '3'
        }

        Input3FormatCmdString = '3*{0}\\'.format(ValueStateValues[value])
        self.__SetHelper('Input3Format', Input3FormatCmdString, value, qualifier)

    def UpdateInput3Format(self, value, qualifier):

        Input3FormatCmdString = '3\\'
        self.__UpdateHelper('Input3Format', Input3FormatCmdString, value, qualifier)

    def __MatchInput3Format(self, match, tag):

        ValueStateValues = {
            '01': 'YUVp/HDTV',
            '02': 'YUVi',
            '03': 'Composite'
        }

        value = ValueStateValues[match.group(1).decode()]
        self.WriteStatus('Input3Format', value, None)

    def SetInputA(self, value, qualifier):

        State = {
            '1': '1',
            '2': '2',
        }
        CmdString = '{0}*1!\r'.format(State[value])
        self.__SetHelper('InputA', CmdString, value, qualifier)

    def UpdateInputA(self, value, qualifier):
        CmdString = '32I'
        self.__UpdateHelper('InputA', CmdString, value, qualifier)

    def SetInputB(self, value, qualifier):

        CmdString = '{0}*2!\r'.format(self.InputBState[value])
        self.__SetHelper('InputB', CmdString, value, qualifier)

    def UpdateInputB(self, value, qualifier):
        CmdString = '32I'
        self.__UpdateHelper('InputB', CmdString, value, qualifier)

    def __MatchInputStatus(self, match, tag):

        InputAState = {
            '1': '1',
            '2': '2',
        }

        if tag == 'Set':
            if match.group(2).decode() == '1':
                self.WriteStatus('InputA', InputAState[str(match.group(1).decode())], None)
            elif match.group(2).decode() == '2':
                self.WriteStatus('InputB', self.InputBState[str(match.group(1).decode())], None)
        elif tag == 'Update':
            self.WriteStatus('InputA', InputAState[str(match.group(1).decode())], None)
            self.WriteStatus('InputB', self.InputBState[str(match.group(2).decode())], None)

    def SetMetadata(self, value, qualifier):

        TypeStateValues = {
            'Contributor': '0',
            'Coverage': '1',
            'Creator': '2',
            'Date': '3',
            'Description': '4',
            'Format': '5',
            'Identifier': '6',
            'Language': '7',
            'Publisher': '8',
            'Relation': '9',
            'Rights': '10',
            'Source': '11',
            'Subject': '12',
            'Title': '13',
            'Type': '14',
            'System Name': '15',
            'Course': '16',
        }

        MetaString = qualifier['String']
        if MetaString == '':
            MetadataCmdString = 'wM{0}RCDR\r'.format(TypeStateValues[value])
        else:
            MetadataCmdString = 'wM{0}*{1}RCDR\r'.format(TypeStateValues[value], MetaString)

        self.__SetHelper('Metadata', MetadataCmdString, value, qualifier)

    def UpdateMetadataStatus(self, value, qualifier):

        TypeStateValues = {
            'Contributor': '0',
            'Coverage': '1',
            'Creator': '2',
            'Date': '3',
            'Description': '4',
            'Format': '5',
            'Identifier': '6',
            'Language': '7',
            'Publisher': '8',
            'Relation': '9',
            'Rights': '10',
            'Source': '11',
            'Subject': '12',
            'Title': '13',
            'Type': '14',
            'System Name': '15',
            'Course': '16',
            'Location': '17'
        }

        MetadataStatusCmdString = 'wM{0}RCDR\r'.format(TypeStateValues[qualifier['Type']])
        res = self.__UpdateSyncHelper('MetadataStatus', MetadataStatusCmdString, value, qualifier)
        if res:
            values = re.search(self.MetadataStatusRegex, res)
            try:
                if values.group(1):
                    self.WriteStatus('MetadataStatus', values.group('value'), qualifier)
                else:
                    self.WriteStatus('MetadataStatus', 'No Information', qualifier)
            except AttributeError:
                print('Invalid/unexpected response for UpdateMetadataStatus')

    def SetRecallLayoutPreset(self, value, qualifier):

        InputState = {
            'With Inputs': '7',
            'Without Inputs': '8',
        }

        inputTest = qualifier['Inputs']
        if inputTest in InputState:
            if 1 <= int(value) <= 16:
                CmdString = '{0}*{1}.'.format(InputState[inputTest], value)
                self.__SetHelper('RecallLayoutPreset', CmdString, value, qualifier)
            else:
                print('Invalid Command for SetRecallLayoutPreset')
        else:
            print('Invalid Command for SetRecallLayoutPreset')

    def SetRecallEncoderPreset(self, value, qualifier):

        TypeStates = {
            'Archive A': '1',
            'Archive B': '2',
            'Confidence A': '3'
        }

        if 1 <= int(value) <= 32:
            CmdString = '4*{0}*{1}.'.format(TypeStates[qualifier['Stream']], value)
            self.__SetHelper('RecallEncoderPreset', CmdString, value, qualifier)
        else:
            print('Invalid Command for SetRecallEncoderPreset')

    def SetRecallUserPreset(self, value, qualifier):

        ChannelState = {
            'A': '1',
            'B': '2',
        }

        Channel = qualifier['Channel']
        if Channel in ChannelState:
            if 1 <= int(value) <= 16:
                CmdString = '1*{0}*{1}.'.format(ChannelState[Channel], value)
                self.__SetHelper('RecallUserPreset', CmdString, value, qualifier)
            else:
                print('Invalid Command for SetRecallUserPreset')
        else:
            print('Invalid Command for SetRecallUserPreset')

    def SetRecord(self, value, qualifier):

        State = {
            'Start': '1',
            'Stop': '0',
            'Pause': '2'
        }
        CmdString = 'wY{0}RCDR\r'.format(State[value])
        self.__SetHelper('Record', CmdString, value, qualifier)

    def UpdateRecord(self, value, qualifier):

        CmdString = 'wYRCDR\r'
        self.__UpdateHelper('Record', CmdString, value, qualifier)

    def __MatchRecord(self, match, tag):

        State = {
            '1': 'Start',
            '0': 'Stop',
            '2': 'Pause'
        }
        value = State[match.group(1).decode()]
        self.WriteStatus('Record', value, None)

    def SetRecordExtend(self, value, qualifier):

        if 1 <= int(value) <= 60:
            CmdString = 'wE{0}RCDR\r'.format(str(value))
            self.__SetHelper('RecordExtend', CmdString, value, qualifier)
        else:
            print('Invalid Command for SetRecordExtend')

    def SetRecordControl(self, value, qualifier):

        ValueStateValues = {
            'Enable': '1',
            'Disable': '0',
            'Enable Dual': '2'
        }

        RecordControlCmdString = 'wX1*{0}RCDR\r'.format(ValueStateValues[value])
        self.__SetHelper('RecordControl', RecordControlCmdString, value, qualifier)

    def UpdateRecordControl(self, value, qualifier):

        RecordControlCmdString = 'wX1RCDR\r'
        self.__UpdateHelper('RecordControl', RecordControlCmdString, value, qualifier)

    def __MatchRecordControl(self, match, tag):

        ValueStateValues = {
            '1': 'Enable',
            '0': 'Disable',
            '2': 'Enable Dual'
        }

        value = ValueStateValues[match.group('value').decode()]
        self.WriteStatus('RecordControl', value, None)

    def SetRecordDestination(self, value, qualifier):

        ValueStateValues = {
            'Auto': '0',
            'Internal': '1',
            'USB (Front)': '2',
            'USB (Rear)': '3',
            'Internal + USB Front': '12',
            'Internal + USB Rear': '13',
        }

        RecordDestinationCmdString = 'wD{0}RCDR\r'.format(ValueStateValues[value])
        self.__SetHelper('RecordDestination', RecordDestinationCmdString, value, qualifier)

    def UpdateRecordDestination(self, value, qualifier):

        RecordDestinationCmdString = 'wDRCDR\r'
        self.__UpdateHelper('RecordDestination', RecordDestinationCmdString, value, qualifier)

    def __MatchRecordDestination(self, match, tag):

        ValueStateValues = {
            '00': 'Auto',
            '01': 'Internal',
            '02': 'USB (Front)',
            '03': 'USB (Rear)',
            '12': 'Internal + USB Front',
            '13': 'Internal + USB Rear'
        }

        value = ValueStateValues[match.group(1).decode()]
        self.WriteStatus('RecordDestination', value, None)

    def SetRecordDualControl(self, value, qualifier):

        ValueStateValues = {
            'On': '1',
            'Off': '0'
        }

        RecordDualControlCmdString = 'wX2*{0}RCDR\r'.format(ValueStateValues[value])
        self.__SetHelper('RecordDualControl', RecordDualControlCmdString, value, qualifier)

    def UpdateRecordDualControl(self, value, qualifier):

        RecordDualControlCmdString = 'wX2RCDR\r'
        self.__UpdateHelper('RecordDualControl', RecordDualControlCmdString, value, qualifier)

    def __MatchRecordDualControl(self, match, tag):

        ValueStateValues = {
            '1': 'On',
            '0': 'Off'
        }

        value = ValueStateValues[match.group(1).decode()]
        self.WriteStatus('RecordDualControl', value, None)

    def SetRecordingMode(self, value, qualifier):

        ValueStateValues = {
            'Audio and Video': '1',
            'Video Only': '2'
        }

        RecordingModeCmdString = 'w1*{0}SMOD\r'.format(ValueStateValues[value])
        self.__SetHelper('RecordingMode', RecordingModeCmdString, value, qualifier)

    def UpdateRecordingMode(self, value, qualifier):

        RecordingModeCmdString = 'w1SMOD\r'
        self.__UpdateHelper('RecordingMode', RecordingModeCmdString, value, qualifier)

    def __MatchRecordingMode(self, match, tag):

        ValueStateValues = {
            '1': 'Audio and Video',
            '2': 'Video Only'
        }

        value = ValueStateValues[match.group(1).decode()]
        self.WriteStatus('RecordingMode', value, None)

    def SetRecordingVideoFrameRate(self, value, qualifier):

        State = {
            '30 fps': '1',
            '25 fps': '2',
            '24 fps': '3',
            '15 fps': '4',
            '12.5 fps': '5',
            '12 fps': '6',
            '10 fps': '7',
            '5 fps': '8',
        }
        CmdString = 'w1*{0}VFRM\r'.format(State[value])
        self.__SetHelper('RecordingVideoFrameRate', CmdString, value, qualifier)

    def UpdateRecordingVideoFrameRate(self, value, qualifier):

        CmdString = 'w1VFRM\r'
        self.__UpdateHelper('RecordingVideoFrameRate', CmdString, value, qualifier)

    def __MatchRecordingVideoFrameRate(self, match, tag):

        State = {
            '1': '30 fps',
            '2': '25 fps',
            '3': '24 fps',
            '4': '15 fps',
            '5': '12.5 fps',
            '6': '12 fps',
            '7': '10 fps',
            '8': '5 fps',
        }
        value = State[match.group(1).decode()]
        self.WriteStatus('RecordingVideoFrameRate', value, None)

    def SetRecordResolution(self, value, qualifier):

        ValueStateValues = {
            '480p': '1',
            '720p': '2',
            '1080p': '3',
            '512x288': '4',
            '1024x768': '5',
            '1280x1024': '6',
            'Custom': '99'
        }

        RecordResolutionCmdString = 'w1*{0}VRES\r'.format(ValueStateValues[value])
        self.__SetHelper('RecordResolution', RecordResolutionCmdString, value, qualifier)

    def UpdateRecordResolution(self, value, qualifier):

        RecordResolutionCmdString = 'w1VRES\r'
        self.__UpdateHelper('RecordResolution', RecordResolutionCmdString, value, qualifier)

    def __MatchRecordResolution(self, match, tag):

        ValueStateValues = {
            '1': '480p',
            '2': '720p',
            '3': '1080p',
            '4': '512x288',
            '5': '1024x768',
            '6': '1280x1024',
            '99': 'Custom'
        }

        value = ValueStateValues[match.group(1).decode()]
        self.WriteStatus('RecordResolution', value, None)

    def UpdateRemainingFreeDiskSpace(self, value, qualifier):
        self.UpdateFileDestination(value, qualifier)

    def UpdateRemainingRecordingTime(self, value, qualifier):
        CmdString = '36i'
        self.__UpdateHelper('RemainingRecordingTime', CmdString, value, qualifier)

    def __MatchRemainingRecordingTime(self, match, tag):

        value = match.group(1).decode() + ':' + match.group(2).decode() + ':' + match.group(3).decode()
        self.WriteStatus('RemainingRecordingTime', value, {'Drive': 'Primary'})
        if match.group(4) is not None:
            value2 = match.group(4).decode() + ':' + match.group(5).decode() + ':' + match.group(6).decode()
            self.WriteStatus('RemainingRecordingTime', value2, {'Drive': 'Secondary'})
        else:
            self.WriteStatus('RemainingRecordingTime', '00:00:00', {'Drive': 'Secondary'})

    def SetStreamControl(self, value, qualifier):

        TypeStates = {
            'Archive A': '1',
            'Archive B': '2',
            'Confidence A': '3'
        }

        ValueStateValues = {
            'Enable': '1',
            'Disable': '0'
        }

        StreamControlCmdString = 'w{0}*{1}STRC\r'.format(TypeStates[qualifier['Stream']], ValueStateValues[value])
        self.__SetHelper('StreamControl', StreamControlCmdString, value, qualifier)

    def UpdateStreamControl(self, value, qualifier):

        TypeStates = {
            'Archive A': '1',
            'Archive B': '2',
            'Confidence A': '3'
        }

        StreamControlCmdString = 'w{0}STRC\r'.format(TypeStates[qualifier['Stream']])
        self.__UpdateHelper('StreamControl', StreamControlCmdString, value, qualifier)

    def __MatchStreamControl(self, match, tag):

        TypeStates = {
            '1': 'Archive A',
            '2': 'Archive B',
            '3': 'Confidence A'
        }

        ValueStateValues = {
            '1': 'Enable',
            '0': 'Disable'
        }

        qualifier = {'Stream': TypeStates[match.group('type').decode()]}
        value = ValueStateValues[match.group('value').decode()]
        self.WriteStatus('StreamControl', value, qualifier)

    def SetSwapWindows(self, value, qualifier):

        CmdString = '%'
        self.__SetHelper('SwapWindows', CmdString, value, qualifier)

    def SetThumbnailSize(self, value, qualifier):

        ValueStateValues = {
            'Default': '0',
            'Archived Resolution': '1'
        }

        ThumbnailSizeCmdString = 'wT{0}RCDR\r'.format(ValueStateValues[value])
        self.__SetHelper('ThumbnailSize', ThumbnailSizeCmdString, value, qualifier)

    def UpdateThumbnailSize(self, value, qualifier):

        ThumbnailSizeCmdString = 'wTRCDR\r'
        self.__UpdateHelper('ThumbnailSize', ThumbnailSizeCmdString, value, qualifier)

    def __MatchThumbnailSize(self, match, tag):

        ValueStateValues = {
            '0': 'Default',
            '1': 'Archived Resolution'
        }

        value = ValueStateValues[match.group(1).decode()]
        self.WriteStatus('ThumbnailSize', value, None)

    def SetVideoBitrate(self, value, qualifier):

        InputState = {
            'Archive A': '1',
            'Archive B': '2',
            'Confidence A': '3'
        }

        ValueConstraints = {
            'Min': 200,
            'Max': 10000
        }

        if ValueConstraints['Min'] <= value <= ValueConstraints['Max']:
            VideoBitrateCmdString = 'wV{0}*{1}BITR\r'.format(InputState[qualifier['Stream']], value)
            self.__SetHelper('VideoBitrate', VideoBitrateCmdString, value, qualifier)
        else:
            print('Invalid Command for SetVideoBitrate')

    def UpdateVideoBitrate(self, value, qualifier):

        InputState = {
            'Archive A': '1',
            'Archive B': '2',
            'Confidence A': '3'
        }

        VideoBitrateCmdString = 'wV{0}BITR\r'.format(InputState[qualifier['Stream']])
        self.__UpdateHelper('VideoBitrate', VideoBitrateCmdString, value, qualifier)

    def __MatchVideoBitrate(self, match, tag):
        InputState = {
            '1': 'Archive A',
            '2': 'Archive B',
            '3': 'Confidence A'
        }

        value = int(match.group(2).decode())
        self.WriteStatus('VideoBitrate', value, {'Stream': InputState[match.group(1).decode()]})

    def SetVideoMute(self, value, qualifier):

        Channel = {
            'A': '1',
            'B': '2',
        }

        State = {
            'On': '1',
            'Off': '0',
        }
        CmdString = '{0}*{1}B'.format(Channel[qualifier['Channel']], State[value])
        self.__SetHelper('VideoMute', CmdString, value, qualifier)

    def UpdateVideoMute(self, value, qualifier):

        Channel = {
            'A': '1',
            'B': '2',
        }
        CmdString = '{0}B'.format(Channel[qualifier['Channel']])
        self.__UpdateHelper('VideoMute', CmdString, value, qualifier)

    def __MatchVideoMute(self, match, tag):

        State = {
            '00': 'Off',
            '01': 'On',
        }

        Channel = {
            '1': 'A',
            '2': 'B',
        }
        self.WriteStatus('VideoMute', State[match.group(2).decode()], {'Channel': Channel[match.group(1).decode()]})

    def __SetHelper(self, command, commandstring, value, qualifier):
        self.Debug = True
        if self.VerboseDisabled:
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

        self.counter += 1
        if self.counter > self.connectionCounter and self.connectionFlag:
            self.OnDisconnected()

        if self.Authenticated in ['User', 'Admin', 'Not Needed']:
            if self.Unidirectional == 'True':
                print('Inappropriate Command ', command)
            else:
                if self.VerboseDisabled:
                    @Wait(1)
                    def SendVerbose():
                        self.Send('w3cv\r\n')
                        if command == 'MetadataStatus':
                            return self.__UpdateSyncHelper(command, commandstring, value, qualifier)
                        else:
                            self.Send(commandstring)
                elif command == 'MetadataStatus':
                    return self.__UpdateSyncHelper(command, commandstring, value, qualifier)
                else:
                    self.Send(commandstring)
        else:
            print('Inappropriate Command ', command)

    def __UpdateSyncHelper(self, command, commandstring, value, qualifier):
        if self.Unidirectional == 'True':
            print('Inappropriate Command')
            return ''
        else:
            res = self.SendAndWait(commandstring, self.DefaultResponseTimeout, deliTag=b'\r\n').decode()
            if not res:
                return ''
            elif res[0] == 'E':
                self.__MatchErrors(res, 'Sync')
                return ''
            else:
                return res

    def __MatchErrors(self, match, qualifier):

        DEVICE_ERROR_CODES = {
            '01': 'Invalid input number (too large)',
            '10': 'Invalid command',
            '11': 'Invalid preset number',
            '12': 'Invalid port number',
            '13': 'Invalid parameter',
            '14': 'Command not available for this configuration',
            '17': 'System timed out',
            '22': 'Busy',
            '24': 'Privilege violation',
            '25': 'Device not present',
            '26': 'Maximum number of connections exceeded',
            '27': 'Invalid event number',
            '28': 'Bad filename or file not found',
            '30': 'Hardware failure (followed by a colon [:] and a descriptor number)',
            '31': 'Attempt to break port pass-through when it has not been set',
            '32': 'Incorrect V-chip password'
        }

        if qualifier:
            value = match[1:-2]
        else:
            value = match.group(1).decode()

        if value in DEVICE_ERROR_CODES:
            print(DEVICE_ERROR_CODES[value])
        else:
            print('Unrecognized error code: ' + match.group(0).decode())

    def OnConnected(self):
        self.connectionFlag = True
        self.WriteStatus('ConnectionStatus', 'Connected')
        self.counter = 0

    def OnDisconnected(self):
        self.WriteStatus('ConnectionStatus', 'Disconnected')
        self.connectionFlag = False

        if 'Serial' not in self.ConnectionType:
            self.Authenticated = 'Not Needed'
            self.PasswdPromptCount = 0
        self.VerboseDisabled = True

    def SMP351_Base(self):
        self.InputBState = {
            '3': '3',
            '4': '4',
            }

    def SMP351_3GSDI(self):
        self.InputBState = {
            '3': '3',
            '4': '4',
            '5': '5'
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
