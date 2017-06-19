## -------------------------------------------------------------------------- ##
## Empresa     | Asesores y Consultores en Tecnología S.A. de C.V. ---------- ##
## Programador | Dyanko Cisneros Mendoza
## Cliente     | Human Quality
## Proyecto    | Sala de Juntas
## Versión     | 0.1 -------------------------------------------------------- ##

## Begin ControlScript Import --------------------------------------------------
from extronlib import event, Version
from extronlib.device import eBUSDevice, ProcessorDevice, UIDevice
from extronlib.interface import (ContactInterface, DigitalIOInterface,
    EthernetClientInterface, EthernetServerInterfaceEx, FlexIOInterface,
    IRInterface, RelayInterface, SerialInterface, SWPowerInterface,
    VolumeInterface)
from extronlib.ui import Button, Knob, Label, Level
from extronlib.system import Clock, MESet, Wait

print(Version())

## End ControlScript Import ----------------------------------------------------
##
## Begin Device/Processor Definition -------------------------------------------
IPCP = ProcessorDevice('IPlink')
## End Device/Processor Definition ---------------------------------------------
##
## Begin Device/User Interface Definition --------------------------------------
TLP = UIDevice('TouchPanel')
## End Device/User Interface Definition ----------------------------------------
##
## Begin User Import -----------------------------------------------------------
## Instances of Python Extron modules------------------
## IP-controlled Modules declared:
import extr_matrix_DXPHD4k_Series_v1_1_1_0            as DeviceA
import extr_other_MediaPort200_v1_1_0_0               as DeviceB
import extr_sm_SMP_300_Series_v1_8_0_1                as DeviceC
import csco_vtc_SX_Series_TC73_v1_3_0_0               as DeviceD
import biam_dsp_TesiraSeries_v1_5_19_0                as DeviceE
## Serial-controlled Modules declared:
import smfy_controller_RS485_RTS_Transmitter_v1_0_0_0 as DeviceF
import shrp_display_PN_E603_E703_v1_0_2_0             as DeviceG
import shrp_display_PN_E603_E703_v1_0_2_0_            as DeviceH

## IP-controlled Devices declared:
Matrix   = DeviceA.EthernetClass('10.10.10.10', 23, Model='DXP 88 HD 4k')
Bridge   = DeviceB.EthernetClass('10.10.10.11', 23, Model='MediaPort 200')
Recorder = DeviceC.EthernetClass('10.10.10.12', 23, Model='SMP 351')
Cisco    = DeviceD.EthernetClass('10.10.10.13', 23, Model='SX20 TC7.3.X')
Biamp    = DeviceE.EthernetClass('10.10.10.14', 23, Model='TesiraFORTE CI')
## Serial-controlled Devices declared:
Somfy    = DeviceF.SerialClass(IPCP, 'COM1', Baud=9600, Model='RS485 RTS Transmitter')
##
## End User Import -------------------------------------------------------------
## Begin Communication Interface Definition ------------------------------------
## Instantiating ID GUI Buttons to variable names
## Page Index
BtnIndex     = Button(TLP, 1)
## Page Main
BtnVideo     = Button(TLP, 2)
BtnVC        = Button(TLP, 3)
BtnWebex     = Button(TLP, 4)
BtnRec       = Button(TLP, 5)
BtnVoIP      = Button(TLP, 6)
BtnAudio     = Button(TLP, 7)
BtnStatus    = Button(TLP, 8)
BtnPwrOff    = Button(TLP, 9)
LblMode      = Label(TLP, 300)
## Page Video
BtnDisplayL  = Button(TLP, 11)
BtnDisplayR  = Button(TLP, 12)
## Page Display L
BtnLHDMI     = Button(TLP, 21)
BtnLVGA      = Button(TLP, 22)
BtnLPTZ      = Button(TLP, 23)
BtnLShare    = Button(TLP, 24)
BtnLPwrOn    = Button(TLP, 25)
BtnLPwrOff   = Button(TLP, 26)
BtnLBack     = Button(TLP, 27)
## Page Display R
BtnRHDMI     = Button(TLP, 31)
BtnRVGA      = Button(TLP, 32)
BtnRPTZ      = Button(TLP, 33)
BtnRShare    = Button(TLP, 34)
BtnRPwrOn    = Button(TLP, 35)
BtnRPwrOff   = Button(TLP, 36)
BtnRBack     = Button(TLP, 37)
## Page Webex
BtnWHDMI     = Button(TLP, 61)
BtnWVGA      = Button(TLP, 62)
BtnWPTZ      = Button(TLP, 63)
BtnWShare    = Button(TLP, 64)
BtnWCisco1   = Button(TLP, 65)
BtnWCisco2   = Button(TLP, 66)
## Page Recording - Sources Control
Btn4HDMI     = Button(TLP, 71)
Btn4VGA      = Button(TLP, 72)
Btn4PTZ      = Button(TLP, 73)
Btn4Share    = Button(TLP, 74)
Btn4Cisco1   = Button(TLP, 75)
Btn4Cisco2   = Button(TLP, 76)
## Page Recording - Mute Control
Btn4Mic      = Button(TLP, 77)
Btn4VC       = Button(TLP, 78)
Btn4VoIP     = Button(TLP, 79)
Btn4PC       = Button(TLP, 80)
## Page Recording - Record Control
BtnPause     = Button(TLP, 81)
BtnREC       = Button(TLP, 82)
BtnStop      = Button(TLP, 83)
LblRes       = Label(TLP, 84)
BtnRecAV     = Button(TLP, 85)
BtnRecV      = Button(TLP, 86)
LblElapsed   = Label(TLP, 87)
## Page VoIP - Dial Control
BtnCall      = Button(TLP, 91)
BtnHangup    = Button(TLP, 92)
## Page VoIP - Numbers Control
BtnDial0     = Button(TLP, 100)
BtnDial1     = Button(TLP, 101)
BtnDial2     = Button(TLP, 102)
BtnDial3     = Button(TLP, 103)
BtnDial4     = Button(TLP, 104)
BtnDial5     = Button(TLP, 105)
BtnDial6     = Button(TLP, 106)
BtnDial7     = Button(TLP, 107)
BtnDial8     = Button(TLP, 108)
BtnDial9     = Button(TLP, 109)
BtnDialA     = Button(TLP, 110)
BtnDialG     = Button(TLP, 111)
## Page VoIP - Options Control
BtnRedial    = Button(TLP, 112)
BtnDTMF      = Button(TLP, 113)
BtnHold      = Button(TLP, 114)
BtnDelete    = Button(TLP, 115, repeatTime = 0.1)
LblDial      = Label(TLP, 116)
## Page VC - Dial Control
BtnVCCall    = Button(TLP, 131)
BtnVCHangup  = Button(TLP, 132)
## Page VC - Numbers Control
BtnVCDial0   = Button(TLP, 140)
BtnVCDial1   = Button(TLP, 141)
BtnVCDial2   = Button(TLP, 142)
BtnVCDial3   = Button(TLP, 143)
BtnVCDial4   = Button(TLP, 144)
BtnVCDial5   = Button(TLP, 145)
BtnVCDial6   = Button(TLP, 146)
BtnVCDial7   = Button(TLP, 147)
BtnVCDial8   = Button(TLP, 148)
BtnVCDial9   = Button(TLP, 149)
BtnVCDialA   = Button(TLP, 150)
BtnVCDialG   = Button(TLP, 151)
## Page VC - Options Control
BtnVCEnviar  = Button(TLP, 152)
BtnVCCamara  = Button(TLP, 153)
BtnVCAutoAn  = Button(TLP, 154)
BtnVCDelete  = Button(TLP, 155, repeatTime = 0.1)
LblVCDial    = Label(TLP, 156)
## Page VC - Content Sources Control
BtnVCHDMI    = Button(TLP, 181)
BtnVCVGA     = Button(TLP, 182)
BtnVCPTZ     = Button(TLP, 183)
BtnVCShare   = Button(TLP, 184)
## Page VC - Content Sharing Control
BtnVCBack2   = Button(TLP, 185)
BtnVCSend    = Button(TLP, 186)
BtnVCStop    = Button(TLP, 187)
## Page VC - Camera Presets Control
BtnVCP1      = Button(TLP, 161)
BtnVCP2      = Button(TLP, 162)
BtnVCP3      = Button(TLP, 163)
BtnVCP4      = Button(TLP, 164)
BtnVCP5      = Button(TLP, 165)
BtnVCRecall  = Button(TLP, 166)
BtnVCSave    = Button(TLP, 167)
## Page VC - Camera Zoom Control
BtnVCZoom1   = Button(TLP, 168, repeatTime = 0.1)
BtnVCZoom2   = Button(TLP, 169, repeatTime = 0.1)
## Page VC - Camera Movement Control
BtnVCUp      = Button(TLP, 170, repeatTime = 0.1)
BtnVCLeft    = Button(TLP, 171, repeatTime = 0.1)
BtnVCDown    = Button(TLP, 172, repeatTime = 0.1)
BtnVCRight   = Button(TLP, 173, repeatTime = 0.1)
## Page VC - Camera Selection Control
BtnVCLocal   = Button(TLP, 174)
BtnVCRemote  = Button(TLP, 175)
## Page Audio - Sources Control
BtnXHDMI     = Button(TLP, 188)
BtnXVGA      = Button(TLP, 189)
BtnXShare    = Button(TLP, 190)
## Page Audio - Gain Control
BtnXSpkLess  = Button(TLP, 191, repeatTime = 0.1)
BtnXSpkPlus  = Button(TLP, 192, repeatTime = 0.1)
BtnXVCLess   = Button(TLP, 193, repeatTime = 0.1)
BtnXVCPlus   = Button(TLP, 194, repeatTime = 0.1)
LevelSpk     = Level(TLP, 195)
LevelSpk.SetRange(-100, 12, 1)
LevelVC      = Level(TLP, 196)
## Page Audio - Mute Control
BtnXSpk      = Button(TLP, 197)
BtnXVC       = Button(TLP, 198)
BtnXMics     = Button(TLP, 199)
## Page Status
Btn232LCD1   = Button(TLP, 211)
Btn232LCD2   = Button(TLP, 212)
BtnLANMatrix = Button(TLP, 213)
BtnLANBiamp = Button(TLP, 214)
Btn232PTZ    = Button(TLP, 215)
Btn232Cisco  = Button(TLP, 216)
BtnLANRec    = Button(TLP, 217)
RecLabel1    = Label(TLP, 218)
RecLabel2    = Label(TLP, 219)
RecLabel3    = Label(TLP, 220)
BtnLanVaddio = Button(TLP, 221)
Lbl1Vaddio   = Label(TLP, 222)
Lbl2Vaddio   = Label(TLP, 223)
Lbl3Vaddio   = Label(TLP, 224)
## Page Power
BtnPowerAll  = Button(TLP, 250, holdTime = 3)
LblPowerAll  = Label(TLP, 251)

## Button Grouping -------------------------------------------------------------
## Group Page Main
PageMain   = [BtnVideo, BtnVC, BtnWebex, BtnRec, BtnVoIP, 
              BtnAudio, BtnStatus, BtnPwrOff]
GroupMain  = MESet(PageMain)
## Group Popup Video
PageVideo   = [BtnDisplayL, BtnDisplayR]
## Group Popup Display L
PageLCD1    = [BtnLHDMI, BtnLVGA, BtnLPTZ, BtnLShare, BtnLPwrOn, 
               BtnLPwrOff, BtnLBack]
## Group Popup Display R
PageLCD2    = [BtnRHDMI, BtnRVGA, BtnRPTZ, BtnRShare, BtnRPwrOn,
               BtnRPwrOff, BtnRBack]
## Group Popup VC
PageVCCall  = [BtnVCCall, BtnVCHangup]
PageVCDial  = [BtnVCDial0, BtnVCDial1, BtnVCDial2, BtnVCDial3, BtnVCDial4,
               BtnVCDial5, BtnVCDial6, BtnVCDial7, BtnVCDial8, BtnVCDial9,
               BtnVCDialA, BtnVCDialG, BtnVCDelete]
PageVCOpt   = [BtnVCEnviar, BtnVCCamara, BtnVCAutoAn]
PageVCShare = [BtnVCHDMI, BtnVCVGA, BtnVCPTZ, BtnVCShare, BtnVCBack2,
               BtnVCSend, BtnVCStop]
PageVCCamN  = [BtnVCZoom1, BtnVCZoom2, BtnVCUp, BtnVCLeft, BtnVCDown,
               BtnVCRight, BtnVCLocal, BtnVCRemote]
PageVCCamP  = [BtnVCP1, BtnVCP2, BtnVCP3, BtnVCP4, BtnVCP5,
               BtnVCRecall, BtnVCSave]
GroupVCPTZ  = MESet([BtnVCRecall, BtnVCSave])
GroupVCCam  = MESet([BtnVCLocal, BtnVCRemote])
## Group Popup Webex
PageWebex   = [BtnWHDMI, BtnWVGA, BtnWPTZ, BtnWShare, BtnWCisco1, BtnWCisco2]
## Group Popup REC
PageRecV    = [Btn4HDMI, Btn4VGA, Btn4PTZ, Btn4Share, Btn4Cisco1, Btn4Cisco2]
PageRecA    = [Btn4Mic, Btn4VC, Btn4VoIP, Btn4PC]
PageRecNav  = [BtnPause, BtnREC, BtnStop]
GroupRec    = MESet(PageRecNav)
## Group Popup VoIP
PageTelCall = [BtnCall, BtnHangup]
PageTelDial = [BtnDial0, BtnDial1, BtnDial2, BtnDial3, BtnDial4, BtnDial5,
               BtnDial6, BtnDial7, BtnDial8, BtnDial9,
               BtnDialA, BtnDialG, BtnDelete]
PageTelOpt  = [BtnRedial, BtnDTMF, BtnHold]
## Group Popup Audio
PageAudio1  = [BtnXHDMI, BtnXVGA, BtnXShare]
PageAudio2  = [BtnXSpkLess, BtnXSpkPlus, BtnXVCLess, BtnXVCPlus]
PageAudio3  = [BtnXSpk, BtnXVC, BtnXMics]
## Group Button State List
ButtonEventList = ['Pressed', 'Released', 'Held', 'Repeated', 'Tapped']
## End Communication Interface Definition --------------------------------------

# This is the last function that loads when starting the system-----------------
def Initialize():
    ## Opening a new Connection Thread to all devices
    Biamp.Connect()

    ## Initialization of data and variables-----------
    ## Initialization in Cisco Camera Page
    Cisco_Data['PresetMode'] = 'Recall'
    Cisco_Data['Camera'] = 'Local'
    GroupVCPTZ.SetCurrent(BtnVCRecall)
    GroupVCCam.SetCurrent(BtnVCLocal)
    
    ## Initialization in Cisco Dial Page
    global dialerVC         ## To access the Dial String variable in all program
    dialerVC = ''           ## Clean the Dial String Variable
    Cisco_Data['Dial'] = '' ## Clean the Dial Data in Dictionary
    LblVCDial.SetText('')   ## Clean the Dial Data in GUI
    
    ## Initialization in VoIP Dial Page
    global dialerVI         ## To access the Dial String variable in all program
    dialerVI = ''           ## Clean the Dial String Variable
    Voip_Data['Dial'] = ''  ## Clean the Dial Data in Dictionary
    LblDial.SetText('')     ## Clean the Dial Data in gui
   
    ## Subscribe Data Parsing of all devices
    ## Matrix Subscribe Commands
    
    ## AV Bridge Subscribe Commands
    
    ## Recorder Subscribe Commands
    Recorder.SubscribeStatus('Record',None,Recorder_Parsing)
    Recorder.SubscribeStatus('RecordDestination',None,Recorder_Parsing)
    Recorder.SubscribeStatus('RecordResolution',None,Recorder_Parsing)
    Recorder.SubscribeStatus('RecordingMode',None,Recorder_Parsing)
    ## Cisco Subscribe Commands
    Cisco.SubscribeStatus('CallStatus',{'Call':'1'},Cisco_Parsing)
    Cisco.SubscribeStatus('PresentationMode',None,Cisco_Parsing)
    ## Biamp Subscribe Commands
    Biamp.SubscribeStatus('ConnectionStatus',None, Biamp_Parsing)
    Biamp.SubscribeStatus('MuteControl',{'Instance Tag':'lvl_spk','Channel':'1'},Biamp_Parsing)
    Biamp.SubscribeStatus('MuteControl',{'Instance Tag':'lvl_vcrx','Channel':'1'},Biamp_Parsing)
    Biamp.SubscribeStatus('MuteControl',{'Instance Tag':'mute_mix','Channel':'1'},Biamp_Parsing)
    Biamp.SubscribeStatus('LevelControl',{'Instance Tag':'lvl_spk','Channel':'1'},Biamp_Parsing)
    ## Somfy Subscribe Commands
    
    ## TouchPanel Functions
    TLP.HideAllPopups()
    TLP.ShowPage('Index')
    GroupMain.SetCurrent(None) ##Turn Off all feedback button in GUI Main Page
    
    ## Notify to Console
    print('System Inicializate')
    pass

## Data Parsing Functions ------------------------------------------------------
## These functions receive the data of the devices in real time
## Each function stores the parsed data in dictionaries and activate feedback
## Each function works with the subscription methods of the Python modules

## Data Parsing Functions - IP Controlled Devices ------------------------------
# Please declare Matrix Data Function below

# Please declare AV Bridge Data Function below

def Recorder_Parsing(command,value,qualifier):
    #--
    if command == 'Record':
        Recorder_Data['Record'] = value
        if value == 'Start':
            print(Recorder_Data['Record'])
            GroupRec.SetCurrent(BtnREC)
        elif value == 'Stop':
            print(Recorder_Data['Record'])
            GroupRec.SetCurrent(BtnStop)
        elif value == 'Pause':
            print(Recorder_Data['Record'])
            GroupRec.SetCurrent(BtnPause)
    #--
    elif command == 'RecordDestination':
        Recorder_Data['Destination'] = value
        print(Recorder_Data['Destination'])
    #--
    elif command == 'RecordResolution':
        LblRes.SetText(value)
        print(value)
    #--
    elif command == 'RecordingMode':
        if value == 'Audio and Video':
            BtnRecAV.SetState(1)
            BtnRecV.SetState(0)
        elif value == 'Video Only':
            BtnRecAV.SetState(0)
            BtnRecV.SetState(1)
    pass

def Cisco_Parsing(command,value,qualifier):
    #--
    if command == 'CallStatus':
        Cisco_Data['Call'] = value
    #--
    elif command == 'PresentationMode':
        Cisco_Data['Content'] = value
    #--
    elif command == 'AutoAnswer':
        if value == 'On':
            Cisco_Data['AutoAnswer'] = 'On'
            BtnVCAutoAn.SetState(1)
        elif value == 'Off':
            Cisco_Data['AutoAnswer'] = 'Off'
            BtnVCAutoAn.SetState(0)
    pass

def Biamp_Parsing(command,value,qualifier):
    #--
    if command == 'ConnectionStatus':
        if value == 'Connected':
            Biamp_Data['Conex'] = 'Connected'
            BtnLANBiamp.SetState(1)
        elif value == 'Disconnected':
            Biamp_Data['Conex'] = 'Disconnected'
            BtnLANBiamp.SetState(0)
    #--
    elif command == 'MuteControl':
        if qualifier['Instance Tag'] == 'lvl_spk':
            if value == 'On':
                Biamp_Data['Mute_Spk'] = 'On'
                BtnXSpk.SetState(1)
            elif value == 'Off':
                Biamp_Data['Mute_Spk'] = 'Off'
                BtnXSpk.SetState(0)
        #--
        elif qualifier['Instance Tag'] == 'lvl_vcrx':
            if value == 'On':
                Biamp_Data['Mute_VCRx'] = 'On'
                BtnXVC.SetState(1)
            elif value == 'Off':
                Biamp_Data['Mute_VCRx'] = 'Off'
                BtnXVC.SetState(0)
        #--
        elif qualifier['Instance Tag'] == 'mute_mix':
            if value == 'On':
                Biamp_Data['Mute_Mics'] = 'On'
                BtnXMics.SetState(1)
            elif value == 'Off':
                Biamp_Data['Mute_Mics'] = 'Off'
                BtnXMics.SetState(0)
    #--
    elif command == 'LevelControl':
        LevelSpk.SetLevel(value)
        Biamp_Data['Lvl_Spk'] = value
        print(value)
    pass

## Data Parsing Functions - Serial Controlled Devices --------------------------

## Data dictionaries -----------------------------------------------------------
## Each dictionary store the real time information of room devices
## Data dictionaries - IP Controlled Devices -----------------------------------
Matrix_Data = {
    'Conex' : '',
    'Input' : '',
    'Output': '',
    'Type'  : '',
}

Bridge_Data = {
    'Conex' : '',
}

Recorder_Data = {
    'Destination' : '',
    'Mode'        : '',
    'Record'      : '',
    'Resolution'  : '',
}

Cisco_Data = {
    'AutoAnswer' : '',
    'CallStatus' : '',
    'Camera'     : '',
    'Conex'      : '',
    'Dial'       : '',
    'Power'      : '',
    'PresetMode' : '',
}

Biamp_Data = {
    'Conex'     : '',
    'Mute_Spk'  : '',
    'Mute_VCRx' : '',
    'Mute_Mics' : '',
    'Lvl_Spk'   : None,
}

Voip_Data = {
    'Dial' : '',
    'DTMF' : False
}
## Data dictionaries - Serial Controlled Devices -------------------------------
Somfy_Data = {
    'Conex' : '',
}

LCD1_Data = {
    'Input' : '',
    'Power' : '',
}
LCD2_Data = {
    'Input' : '',
    'Power' : '',
}
## Event Definitions -----------------------------------------------------------
## This section define all actions that a user triggers through the buttons ----
## Page Index ------------------------------------------------------------------
@event(BtnIndex,'Pressed')
def IndexEvents(button, state):
    TLP.ShowPage('Main')
    TLP.ShowPopup('x_Welcome')
    print('Touch Mode: %s' % 'Index')
    pass

## Page Main -------------------------------------------------------------------
@event(PageMain, ButtonEventList)
def MainEvents(button, state):
    #--
    if button is BtnVideo and state == 'Pressed':
        TLP.ShowPopup('Video')
        LblMode.SetText('Selección de Video')
        print('Touch Mode: %s' % 'Video')
    #--
    elif button is BtnVC and state == 'Pressed':
        TLP.ShowPopup('VC')
        LblMode.SetText('Control de Videoconferencia')
        print('Touch Mode: %s' % 'VC')
    #--
    elif button is BtnWebex and state == 'Pressed':
        TLP.ShowPopup('Webex')
        LblMode.SetText('Control de Webconferencia')
        print('Touch Mode: %s' % 'Webex')
    #--
    elif button is BtnRec and state == 'Pressed':
        TLP.ShowPopup('Recording')
        LblMode.SetText('Control de Grabación')
        SMP351.Set('RecordingMode','Audio and Video')
        print('Touch Mode: %s' % 'Recording')
    #--
    elif button is BtnVoIP and state == 'Pressed':
        TLP.ShowPopup('VoIP')
        LblMode.SetText('Telefonía IP')
        print('Touch Mode: %s' % 'VoIP')
    #--
    elif button is BtnAudio and state == 'Pressed':
        ## If the data dictionary are null, then run the Audio queries
        if Biamp_Data['Mute_Spk'] == '':
            Biamp.Update('MuteControl',{'Instance Tag':'lvl_spk','Channel':'1'})
        elif Biamp_Data['Mute_VCRx'] == '':
            Biamp.Update('MuteControl',{'Instance Tag':'lvl_vcrx','Channel':'1'})
        elif Biamp_Data['Mute_Mics'] == '':
            Biamp.Update('MuteControl',{'Instance Tag':'mute_mix','Channel':'1'})
        elif Biamp_Data['Lvl_Spk'] == None:
            Biamp.Update('LevelControl',{'Instance Tag':'lvl_spk','Channel':'1'})
        #--
        TLP.ShowPopup('Audio')
        LblMode.SetText('Control de Audio')
        print('Touch Mode: %s' % 'Audio')
    #--
    elif button is BtnStatus and state == 'Pressed':
        TLP.ShowPopup('Status')
        LblMode.SetText('Información de Dispositivos')
        print('Touch Mode: %s' % 'Status')
    #--
    elif button is BtnPwrOff and state == 'Pressed':
        TLP.ShowPopup('x_PowerOff')
        LblMode.SetText('¿Deseas Apagar el Sistema?')
        print('Touch Mode: %s' % 'PowerOff')
    #--
    ##Turn On the feedbak of last pressed button
    GroupMain.SetCurrent(button)
    pass
    
## Page Video ------------------------------------------------------------------
@event(PageVideo, ButtonEventList)
def VideoEvents(button, state):
    if button is BtnDisplayL and state == 'Pressed':
        ## Open the Video Sources available for Left Display in GUI
        TLP.ShowPopup('Display_L')
        LblMode.SetText('Control de Pantalla Izquierda')
        print('Video Mode: %s' % 'Display L')
    elif button is BtnDisplayR and state == 'Pressed':
        ## Open the Video Sources available for Right Display in GUI
        TLP.ShowPopup('Display_R')
        LblMode.SetText('Control de Pantalla Derecha')
        print('Video Mode: %s' % 'Display R')
    pass
    
## Page Display L --------------------------------------------------------------
@event(PageLCD1, ButtonEventList)
def DisplayLEvents(button, state):
    if button is BtnLHDMI and state == 'Pressed':
        ## HDMI to Display Left - Video
        Matrix.Set('MatrixTieCommand', None,{'Input':'1','Output':'1','Tie Type':'Video'})
        print('Button Pressed - LCD L: %s' % 'HDMI')
    elif button is BtnLVGA and state == 'Pressed':
        ## VGA to Display Left - Video
        Matrix.Set('MatrixTieCommand', None, {'Input':'2','Output':'1','Tie Type':'Video'})
        print('Button Pressed - LCD L: %s' % 'VGA')
    elif button is BtnLPTZ and state == 'Pressed':
        ## PTZ to Display Left - Video
        Matrix.Set('MatrixTieCommand', None, {'Input':'3','Output':'1','Tie Type':'Video'})
        print('Button Pressed - LCD L: %s' % 'PTZ')
    elif button is BtnLShare and state == 'Pressed':
        ## ShareLink to Display Left - Video
        Matrix.Set('MatrixTieCommand', None, {'Input':'4','Output':'1','Tie Type':'Video'})
        print('Button Pressed - LCD L: %s' % 'ShareLink')
    elif button is BtnLPwrOn and state == 'Pressed':
        ## The system send the command action directly
        LCD1.Set('Power','On')
        print('Button Pressed - LCD L: %s' % 'PowerOn')
    elif button is BtnLPwrOff and state == 'Pressed':
        ## The system send the command action directly
        LCD1.Set('Power','Off')
        print('Button Pressed - LCD L: %s' % 'PowerOff')
    elif button is BtnLBack and state == 'Pressed':
        ## Hide actual popup and show the Display Selection Popup
        TLP.ShowPopup('Video')
        print('Button Pressed - LCD L: %s' % 'Back')
    pass

## Page Display R --------------------------------------------------------------
@event(PageLCD2, ButtonEventList)
def DisplayREvents(button, state):
    if button is BtnRHDMI and state == 'Pressed':
        ## HDMI to Display Right - Video
        Matrix.Set('MatrixTieCommand', None, {'Input':'1','Output':'2','Tie Type':'Video'})
        print('Button Pressed - LCD R: %s' % 'HDMI')
    elif button is BtnRVGA and state == 'Pressed':
        ## VGA to Display Right - Video
        Matrix.Set('MatrixTieCommand', None, {'Input':'2','Output':'2','Tie Type':'Video'})
        print('Button Pressed - LCD R: %s' % 'VGA')
    elif button is BtnRPTZ and state == 'Pressed':
        ## PTZ to Display Right - Video
        Matrix.Set('MatrixTieCommand', None, {'Input':'3','Output':'2','Tie Type':'Video'})
        print('Button Pressed - LCD R: %s' % 'PTZ')
    elif button is BtnRShare and state == 'Pressed':
        ## ShareLink to Display Right - Video
        Matrix.Set('MatrixTieCommand', None, {'Input':'4','Output':'2','Tie Type':'Video'})
        print('Button Pressed - LCD R: %s' % 'ShareLink')
    elif button is BtnRPwrOn and state == 'Pressed':
        ## The system send the command action directly
        LCD2.Set('Power','On')
        print('Button Pressed - LCD R: %s' % 'PowerOn')
    elif button is BtnRPwrOff and state == 'Pressed':
        ## The system send the command action directly
        LCD2.Set('Power','Off')
        print('Button Pressed - LCD R: %s' % 'PowerOff')
    elif button is BtnRBack and state == 'Pressed':
        ## Hide actual popup and show the Display Selection Popup
        TLP.ShowPopup('Video')
        print('Button Pressed - LCD R: %s' % 'Back')
    pass

## Page VC ---------------------------------------------------------------------
@event(PageVCCall, ButtonEventList)
def VCCallEvents(button, state):
    if button is BtnVCCall and state == 'Pressed':
        ##--This button dial the number typed on the touch panel (Cisco VC)
        Cisco.Set('Hook','Dial',{'Protocol':'H323','Number': Cisco_Data['Dial']})
        print('Button Pressed - VC: %s' % 'Call')
    elif button is BtnVCHangup and state == 'Pressed':
        ##--This button hangs up all active calls (Cisco VC)
        Cisco.Set('Hook','Disconnect All',{'Protocol':'H323'})
        print('Button Pressed - VC: %s' % 'Hangup')
    pass

## This function is called when the user press a Dial Button
## This function add or remove data from the panel Dial Number
def DialerVC(btn_name):
    global dialerVC
    #--    
    if btn_name == 'Delete':         #If the user push 'Delete' button
        dialerVC = dialerVC[:-1]     #Remove the last char of the string
        Cisco_Data['Dial'] = dialerVC #Asign the string to the data dictionary
        LblVCDial.SetText(dialerVC)  #Send the string to GUI Label
    #--
    else:                            #If the user push a [*#0-9] button
        Number = str(btn_name[4])    #Extract the valid character of btn name
        dialerVC += Number           #Append the last char to the string
        Cisco_Data['Dial'] = dialerVC #Asign the string to the data dictionary
        LblVCDial.SetText(dialerVC)  #Send the string to GUI Label
    pass

@event(PageVCDial, ButtonEventList)
def VCDialEvents(button, state):
    ## All the VC Dial Buttons pressed come in button variable
    if state == 'Pressed' or state == 'Repeated':
        print('Button Pressed - VC: %s' % button.Name)
        DialerVC(button.Name) #Recall a validation function
        button.SetState(1)
    else:
        button.SetState(0)
    pass

@event(PageVCOpt, ButtonEventList)
def VCOptEvents(button, state):
    ## VC Options: Content Control
    if button is BtnVCEnviar and state == 'Pressed':
        TLP.ShowPopup('VC_Content')
        BtnVCEnviar.SetState(1)
        print('Button Pressed - VC: %s' % 'Content')
    else:
        BtnVCEnviar.SetState(0)
    ## VC Options: Camera Control
    if button is BtnVCCamara and state == 'Pressed':
        TLP.ShowPopup('VC_Cam')
        BtnVCCamara.SetState(1)
        print('Button Pressed - VC: %s' % 'Camera')
    else:
        BtnVCCamara.SetState(0)
    ## VC Options: AutoAnswer
    if button is BtnVCAutoAn and state == 'Pressed':
        if Cisco_Data['AutoAnswer'] == 'On':
            Cisco.Set('AutoAnswer','Off')
        elif Cisco_Data['AutoAnswer'] == 'Off':
            Cisco.Set('AutoAnswer','On')
        print('Button Pressed - VC: %s' % 'AutoAnswer')
    pass

## Page VC Content -------------------------------------------------------------
@event(PageVCShare, ButtonEventList)
def VCCamEvents(button, state):
    if button is BtnVCHDMI and state == 'Pressed':
        ## HDMI to Cisco Computer Input - Video
        Matrix.Set('MatrixTieCommand', None, {'Input':'1','Output':'3','Tie Type':'Video'})
        print('Button Pressed - VC Share: %s' % 'HDMI')
    elif button is BtnVCVGA and state == 'Pressed':
        ## VGA to Cisco Computer Input - Video
        Matrix.Set('MatrixTieCommand', None, {'Input':'2','Output':'3','Tie Type':'Video'})
        print('Button Pressed - VC Share: %s' % 'VGA')
    elif button is BtnVCPTZ and state == 'Pressed':
        ## PTZ to Cisco Computer Input - Video
        Matrix.Set('MatrixTieCommand', None, {'Input':'3','Output':'3','Tie Type':'Video'})
        print('Button Pressed - VC Share: %s' % 'PTZ')
    elif button is BtnVCShare and state == 'Pressed':
        ## ShareLink to Cisco Computer Input - Video
        Matrix.Set('MatrixTieCommand', None, {'Input':'4','Output':'3','Tie Type':'Video'})
        print('Button Pressed - VC Share: %s' % 'ClickShare')
    elif button is BtnVCBack2 and state == 'Pressed':
        ## Hide VC Content Popup and Show the main VC Popup
        TLP.ShowPopup('VC')
        print('Button Pressed - VC Share: %s' % 'Back')
    elif button is BtnVCSend and state == 'Pressed':
        ## Play - Share graphics presentation
        Cisco.Set('Presentation','1')
        print('Button Pressed - VC Share: %s' % 'Send')
    elif button is BtnVCStop and state == 'Pressed':
        ## Stop - Sharing graphics
        Cisco.Set('Presentation','Stop')
        print('Button Pressed - VC Share: %s' % 'Stop')
    pass

## Page VC Camera --------------------------------------------------------------
@event(PageVCCamN,ButtonEventList)
def VCNavEvents(button, state):
    #--
    if button is BtnVCUp:
        if state == 'Pressed' or state == 'Repeated':
            if Cisco_Data['Camera'] == 'Local':
                Cisco.Set('CameraTiltSX20','Up',{'Speed':7})
                print('Cam Local - Cisco: %s' % 'Cam Up')
            elif Cisco_Data['Camera'] == 'Remote':
                Cisco.Set('FarEndCameraPan/Tilt','Up')
                print('Cam Remota - Cisco: %s' % 'Cam Up')
        #--
        elif state == 'Released':
            if Cisco_Data['Camera'] == 'Local':
                Cisco.Set('CameraTiltSX20','Stop',{'Speed':7})
                print('Cam Local - Cisco: %s' % 'Cam Stop')
            elif Cisco_Data['Camera'] == 'Remote':
                Cisco.Set('FarEndCameraPan/Tilt','Stop')
                print('Cam Remota - Cisco: %s' % 'Cam Stop')
    #--
    elif button is BtnVCLeft:
        if state == 'Pressed' or state == 'Repeated':
            if Cisco_Data['Camera'] == 'Local':
                Cisco.Set('CameraPanSX20','Left',{'Speed':7})
                print('Cam Local - Cisco: %s' % 'Cam Left')
            elif Cisco_Data['Camera'] == 'Remote':
                Cisco.Set('FarEndCameraPan/Tilt','Left')
                print('Cam Remota - Cisco: %s' % 'Cam Left')
        #--
        elif state == 'Released':
            if Cisco_Data['Camera'] == 'Local':
                Cisco.Set('CameraPanSX20','Stop',{'Speed':7})
                print('Cam Local - Cisco: %s' % 'Cam Stop')
            elif Cisco_Data['Camera'] == 'Remote':
                Cisco.Set('FarEndCameraPan/Tilt','Stop')
                print('Cam Remota - Cisco: %s' % 'Cam Stop')
    #--
    elif button is BtnVCDown:
        if state == 'Pressed' or state == 'Repeated':
            if Cisco_Data['Camera'] == 'Local':
                Cisco.Set('CameraTiltSX20','Down',{'Speed':7})
                print('Cam Local - Cisco: %s' % 'Cam Down')
            elif Cisco_Data['Camera'] == 'Remote':
                Cisco.Set('FarEndCameraPan/Tilt','Down')
                print('Cam Remota - Cisco: %s' % 'Cam Down')
        #--
        elif state == 'Released':
            if Cisco_Data['Camera'] == 'Local':
                Cisco.Set('CameraTiltSX20','Stop',{'Speed':7})
                print('Cam Local - Cisco: %s' % 'Cam Stop')
            elif Cisco_Data['Camera'] == 'Remote':
                Cisco.Set('FarEndCameraPan/Tilt','Stop')
                print('Cam Remota - Cisco: %s' % 'Cam Stop')
    #--
    elif button is BtnVCRight:
        if state == 'Pressed' or state == 'Repeated':
            if Cisco_Data['Camera'] == 'Local':
                Cisco.Set('CameraPanSX20','Right',{'Speed':7})
                print('Cam Local - Cisco: %s' % 'Cam Right')
            elif Cisco_Data['Camera'] == 'Remote':
                Cisco.Set('FarEndCameraPan/Tilt','Right')
                print('Cam Remota - Cisco: %s' % 'Cam Right')
        #--
        elif state == 'Released':
            if Cisco_Data['Camera'] == 'Local':
                Cisco.Set('CameraPanSX20','Stop',{'Speed':7})
                print('Cam Local - Cisco: %s' % 'Cam Stop')
            elif Cisco_Data['Camera'] == 'Remote':
                Cisco.Set('FarEndCameraPan/Tilt','Stop')
                print('Cam Remota - Cisco: %s' % 'Cam Stop')
    #--
    elif button is BtnVCZoom1: #+
        if state == 'Pressed' or state == 'Repeated':
            if Cisco_Data['Camera'] == 'Local':
                Cisco.Set('CameraZoomSX20','In',{'Speed':7})
                print('Cam Local - Cisco: %s' % 'Cam Zoom+')
            elif Cisco_Data['Camera'] == 'Remote':
                Cisco.Set('FarEndCameraZoom','In')
                print('Cam Remota - Cisco: %s' % 'Cam Zoom+')
            BtnVCZoom1.SetState(1)
        #--
        elif state == 'Released':
            if Cisco_Data['Camera'] == 'Local':
                Cisco.Set('CameraZoomSX20','Stop',{'Speed':7})
                print('Cam Local - Cisco: %s' % 'Cam Stop')
            elif Cisco_Data['Camera'] == 'Remote':
                Cisco.Set('FarEndCameraZoom','Stop')
                print('Cam Remota - Cisco: %s' % 'Cam Stop')
            BtnVCZoom1.SetState(0)
    #--
    elif button is BtnVCZoom2: #-
        if state == 'Pressed' or state == 'Repeated':
            if Cisco_Data['Camera'] == 'Local':
                Cisco.Set('CameraZoomSX20','Out',{'Speed':7})
                print('Cam Local - Cisco: %s' % 'Cam Zoom-')
            elif Cisco_Data['Camera'] == 'Remote':
                Cisco.Set('FarEndCameraZoom','Out')
                print('Cam Remota - Cisco: %s' % 'Cam Zoom-')
            BtnVCZoom2.SetState(1)
        #--
        elif state == 'Released':
            if Cisco_Data['Camera'] == 'Local':
                Cisco.Set('CameraZoomSX20','Stop',{'Speed':7})
                print('Cam Local - Cisco: %s' % 'Cam Stop')
            elif Cisco_Data['Camera'] == 'Remote':
                Cisco.Set('FarEndCameraZoom','Stop')
                print('Cam Remota - Cisco: %s' % 'Cam Stop')
            BtnVCZoom2.SetState(0)
    #--
    if button is BtnVCLocal and state == 'Pressed':
        Cisco_Data['Camera'] = 'Local'
        GroupVCCam.SetCurrent(BtnVCLocal)
        print('Button Pressed - Cisco: %s' % 'Cam Local')
    #--
    elif button is BtnVCRemote and state == 'Pressed':
        Cisco_Data['Camera'] = 'Remote'
        GroupVCCam.SetCurrent(BtnVCRemote)
        print('Button Pressed - Cisco: %s' % 'Cam Remote')
    pass

@event(PageVCCamP, ButtonEventList)
def VCCamEvents(button, state):
    #--
    if button is BtnVCP1 and state == 'Pressed':
        if Cisco_Data['Camera'] == 'Local':
            if Cisco_Data['PresetMode'] == 'Recall':
                Cisco.Set('CameraPresetPositionRecallSX20','1')
                print('Recall Local Preset Cisco: %s' % '1')
            elif Cisco_Data['PresetMode'] == 'Save':
                Cisco.Set('CameraPresetSaveSX20','1')
                print('Save Local Preset Cisco: %s' % '1')
        #--
        elif Cisco_Data['Camera'] == 'Remote':
            if Cisco_Data['PresetMode'] == 'Recall':
                Cisco.Set('FarEndCameraPresetRecall','1')
                print('Recall Remote Preset Cisco: %s' % '1')
            elif Cisco_Data['PresetMode'] == 'Save':
                Cisco.Set('FarEndCameraPresetSave','1')
                print('Save Remote Preset Cisco: %s' % '1')
    #--
    elif button is BtnVCP2 and state == 'Pressed':
        if Cisco_Data['Camera'] == 'Local':
            if Cisco_Data['PresetMode'] == 'Recall':
                Cisco.Set('CameraPresetPositionRecallSX20','2')
                print('Recall Local Preset Cisco: %s' % '2')
            elif Cisco_Data['PresetMode'] == 'Save':
                Cisco.Set('CameraPresetSaveSX20','2')
                print('Save Local Preset Cisco: %s' % '2')
        #--
        elif Cisco_Data['Camera'] == 'Remote':
            if Cisco_Data['PresetMode'] == 'Recall':
                Cisco.Set('FarEndCameraPresetRecall','2')
                print('Recall Remote Preset Cisco: %s' % '2')
            elif Cisco_Data['PresetMode'] == 'Save':
                Cisco.Set('FarEndCameraPresetSave','2')
                print('Save Remote Preset Cisco: %s' % '2')
    #--
    elif button is BtnVCP3 and state == 'Pressed':
        if Cisco_Data['Camera'] == 'Local':
            if Cisco_Data['PresetMode'] == 'Recall':
                Cisco.Set('CameraPresetPositionRecallSX20','3')
                print('Recall Local Preset Cisco: %s' % '3')
            elif Cisco_Data['PresetMode'] == 'Save':
                Cisco.Set('CameraPresetSaveSX20','3')
                print('Save Local Preset Cisco: %s' % '3')
        #--
        elif Cisco_Data['Camera'] == 'Remote':
            if Cisco_Data['PresetMode'] == 'Recall':
                Cisco.Set('FarEndCameraPresetRecall','3')
                print('Recall Remote Preset Cisco: %s' % '3')
            elif Cisco_Data['PresetMode'] == 'Save':
                Cisco.Set('FarEndCameraPresetSave','3')
                print('Save Remote Preset Cisco: %s' % '3')
    #--
    elif button is BtnVCP4 and state == 'Pressed':
        if Cisco_Data['Camera'] == 'Local':
            if Cisco_Data['PresetMode'] == 'Recall':
                Cisco.Set('CameraPresetPositionRecallSX20','4')
                print('Recall Local Preset Cisco: %s' % '4')
            elif Cisco_Data['PresetMode'] == 'Save':
                Cisco.Set('CameraPresetSaveSX20','4')
                print('Save Local Preset Cisco: %s' % '4')
        #--
        elif Cisco_Data['Camera'] == 'Remote':
            if Cisco_Data['PresetMode'] == 'Recall':
                Cisco.Set('FarEndCameraPresetRecall','4')
                print('Recall Remote Preset Cisco: %s' % '4')
            elif Cisco_Data['PresetMode'] == 'Save':
                Cisco.Set('FarEndCameraPresetSave','4')
                print('Save Remote Preset Cisco: %s' % '4')
    #--
    elif button is BtnVCP5 and state == 'Pressed':
        if Cisco_Data['Camera'] == 'Local':
            if Cisco_Data['PresetMode'] == 'Recall':
                Cisco.Set('CameraPresetPositionRecallSX20','5')
                print('Recall Local Preset Cisco: %s' % '5')
            elif Cisco_Data['PresetMode'] == 'Save':
                Cisco.Set('CameraPresetSaveSX20','5')
                print('Save Local Preset Cisco: %s' % '5')
        #--
        elif Cisco_Data['Camera'] == 'Remote':
            if Cisco_Data['PresetMode'] == 'Recall':
                Cisco.Set('FarEndCameraPresetRecall','5')
                print('Recall Remote Preset Cisco: %s' % '5')
            elif Cisco_Data['PresetMode'] == 'Save':
                Cisco.Set('FarEndCameraPresetSave','5')
                print('Save Remote Preset Cisco: %s' % '5')
    #--
    elif button is BtnVCRecall and state == 'Pressed':
        Cisco_Data['PresetMode'] = 'Recall'
        GroupVCPTZ.SetCurrent(BtnVCRecall)
        print('Button Pressed - Cisco: %s' % 'Recall')
    #--
    elif button is BtnVCSave and state == 'Pressed':
        Cisco_Data['PresetMode'] = 'Save'
        GroupVCPTZ.SetCurrent(BtnVCSave)
        print('Button Pressed - Cisco: %s' % 'Save')
    pass

## Page Webex ------------------------------------------------------------------
@event(PageWebex, ButtonEventList)
def WebexEvents(button, state):
    if button is BtnWHDMI and state == 'Pressed':
        ## HDMI to MediaPort200 Input - Video
        Matrix.Set('MatrixTieCommand', None, {'Input':'1','Output':'5','Tie Type':'Video'})
        print('Button Pressed - Webex: %s' % 'HDMI')
    elif button is BtnWVGA and state == 'Pressed':
        ## VGA to MediaPort200 Input - Video
        Matrix.Set('MatrixTieCommand', None, {'Input':'2','Output':'5','Tie Type':'Video'})
        print('Button Pressed - Webex: %s' % 'VGA')
    elif button is BtnWPTZ and state == 'Pressed':
        ## PTZ to MediaPort200 Input - Video
        Matrix.Set('MatrixTieCommand', None, {'Input':'3','Output':'5','Tie Type':'Video'})
        print('Button Pressed - Webex: %s' % 'PTZ')
    elif button is BtnWShare and state == 'Pressed':
        ## ShareLink to MediaPort200 Input - Video
        Matrix.Set('MatrixTieCommand', None, {'Input':'4','Output':'5','Tie Type':'Video'})
        print('Button Pressed - Webex: %s' % 'ShareLink')
    elif button is BtnWCisco1 and state == 'Pressed':
        ## Cisco 1 to MediaPort200 Input - Video
        Matrix.Set('MatrixTieCommand', None, {'Input':'5','Output':'5','Tie Type':'Video'})
        print('Button Pressed - Webex: %s' % 'Cisco 1')
    elif button is BtnWCisco2 and state == 'Pressed':
        ## Cisco 2 to MediaPort200 Input - Video
        Matrix.Set('MatrixTieCommand', None, {'Input':'6','Output':'5','Tie Type':'Video'})
        print('Button Pressed - Webex: %s' % 'Cisco 2')
    pass

## Page Recording --------------------------------------------------------------
@event(PageRecV, ButtonEventList)
def RecEventsV(button, state):
    if button is Btn4HDMI and state == 'Pressed':
        ## HDMI to SMP351 Input - Video
        Matrix.Set('MatrixTieCommand', None, {'Input':'1','Output':'4','Tie Type':'Video'})
        print('Button Pressed - REC: %s' % 'HDMI')
    elif button is Btn4VGA and state == 'Pressed':
        ## VGA to SMP351 Input - Video
        Matrix.Set('MatrixTieCommand', None, {'Input':'2','Output':'4','Tie Type':'Video'})
        print('Button Pressed - REC: %s' % 'VGA')
    elif button is Btn4PTZ and state == 'Pressed':
        ## PTZ to SMP351 Input - Video
        Matrix.Set('MatrixTieCommand', None, {'Input':'3','Output':'4','Tie Type':'Video'})
        print('Button Pressed - REC: %s' % 'PTZ')
    elif button is Btn4Share and state == 'Pressed':
        ## ShareLink to SMP351 Input - Video
        Matrix.Set('MatrixTieCommand', None, {'Input':'4','Output':'4','Tie Type':'Video'})
        print('Button Pressed - REC: %s' % 'ShareLink')
    elif button is Btn4Cisco1 and state == 'Pressed':
        ## Cisco Out 1 to SMP351 Input - Video
        Matrix.Set('MatrixTieCommand', None, {'Input':'5','Output':'4','Tie Type':'Video'})
        print('Button Pressed - REC: %s' % 'Cisco 1')
    elif button is Btn4Cisco2 and state == 'Pressed':
        ## Cisco Out 2 to SMP351 Input - Video
        Matrix.Set('MatrixTieCommand', None, {'Input':'6','Output':'4','Tie Type':'Video'})
        print('Button Pressed - REC: %s' % 'Cisco 2')
    pass

@event(PageRecA, ButtonEventList)
def RecEventsA(button, state):
    ## Enable / Disable - Mic Audio Recording
    if button is Btn4Mic and state == 'Pressed':
        print('Button Pressed - REC: %s' % 'Mics')
    ## Enable / Disable - VC Audio Recording
    elif button is Btn4VC and state == 'Pressed':
        print('Button Pressed - REC: %s' % 'VC')
    ## Enable / Disable - VoIP Audio Recording
    elif button is Btn4VoIP and state == 'Pressed':
        print('Button Pressed - REC: %s' % 'VoIP')
    ## Enable / Disable - PC Audio Recording
    elif button is Btn4PC and state == 'Pressed': 
        print('Button Pressed - REC: %s' % 'PC')
    pass

@event(PageRecNav, ButtonEventList)
def RecEventsNav(button, state):
    if button is BtnPause and state == 'Pressed':
        ## Pause the Recording
        SMP351.Set('Record','Pause')
        print('Button Pressed - REC: %s' % 'Pause')
    elif button is BtnREC and state == 'Pressed':
        ## Start to Record
        SMP351.Set('Record','Start')
        print('Button Pressed - REC: %s' % 'Rec')
    elif button is BtnStop and state == 'Pressed':
        ## Stop the Recording
        SMP351.Set('Record','Stop')
        print('Button Pressed - REC: %s' % 'Stop')
    pass

## Page VoIP -------------------------------------------------------------------
@event(PageTelCall, ButtonEventList)
def VICallEvents(button, state):
    if button is BtnCall and state == 'Pressed':
        ##--This button dial the number typed on the touch panel (Biamp VoIP)
        Biamp.Set('VoIPHook','Dial',
                  {'Instance Tag':'Dialer','Line':'1','Call Appearance':'1',
                    'Number':Voip_Data['Dial']})
        print('Button Pressed - VoIP: %s' % 'Call')
    #--
    elif button is BtnHangup and state == 'Pressed':
        ##--This button hangs up all active calls (Biamp VoIP)
        Biamp.Set('VoIPHook','End',
                  {'Instance Tag':'Dialer','Line':'1','Call Appearance':'1'})
        print('Button Pressed - VoIP: %s' % 'Hangup')
    pass

## This function is called when the user press a Dial Button
## This function add or remove data from the panel Dial Number
def DialerVoIP(btn_name):
    global dialerVI
    #--
    if btn_name == 'Delete':         #If the user push 'Delete' button
        dialerVI = dialerVI[:-1]     #Remove the last char of the string
        Voip_Data['Dial'] = dialerVI #Asign the string to the data dictionary
        LblDial.SetText(dialerVI)    #Send the string to GUI Label
    #--
    else:                                #If the user push a [*#0-9] button
        Number = str(btn_name[4])        #Extract the valid character of btn name
        if Voip_Data['DTMF'] == False:   #If the DTMF is off
            dialerVI += Number           #Append the last char to the string
            Voip_Data['Dial'] = dialerVI #Asign the string to the data dictionary
            LblDial.SetText(dialerVI)    #Send the string to GUI Label
        elif Voip_Data['DTMF'] == True:  #If DTMF is On
            Biamp.Set('DTMF',Number,{'Instance Tag':'Dialer','Line':'1'})
    pass

@event(PageTelDial, ButtonEventList)
def VIDialEvents(button, state):
    ## All the VoIP Dial Buttons pressed come in button variable
    if state == 'Pressed' or state == 'Repeated':
        print('Button Pressed - VoIP: %s' % button.Name)
        DialerVoIP(button.Name) #Recall a validation function
        button.SetState(1)
    else:
        button.SetState(0)
    pass

@event(PageTelOpt, ButtonEventList)
def VIOptEvents(button, state):
    ## VoIP Redial Control
    if button is BtnRedial and state == 'Pressed':
        Biamp.Set('VoIPHook','Redial',{'Instance Tag':'Dialer','Line':'1','Call Appearance':'1'})
        print('Button Pressed - VoIP: %s' % 'Redial')
    ## VoIP DTMF Control
    elif button is BtnDTMF and state == 'Pressed':
        if Voip_Data['DTMF'] == False:
            Voip_Data['DTMF'] = True
            BtnDTMF.SetState(1)
            print('Button Pressed - VoIP: %s' % 'DTMF On')
        #--
        elif Voip_Data['DTMF'] == True:
            Voip_Data['DTMF'] = False
            BtnDTMF.SetState(0)
            print('Button Pressed - VoIP: %s' % 'DTMF Off')
        print('Button Pressed - VoIP: %s' % 'DTMF')
    ## Hold / Resume Control
    elif button is BtnHold and state == 'Pressed':
        print('Button Pressed - VoIP: %s' % 'Hold/Resume')
    pass

## Page Audio ------------------------------------------------------------------
@event(PageAudio1, ButtonEventList)
def AudioSourceEvents(button, state):
    if button is BtnXHDMI and state == 'Pressed':
        ## HDMI to HDMI Audio Dembedder Input - Audio
        Matrix.Set('MatrixTieCommand', None, {'Input':'1','Output':'1','Tie Type':'Audio'})
        print('Button Pressed - Audio: %s' % 'HDMI')
    elif button is BtnXVGA and state == 'Pressed':
         ## VGA to HDMI Audio Dembedder Input - Audio
        Matrix.Set('MatrixTieCommand', None, {'Input':'2','Output':'1','Tie Type':'Audio'})
        print('Button Pressed - Audio: %s' % 'VGA')
    elif button is BtnXShare and state == 'Pressed':
         ## ShareLink to HDMI Audio Dembedder Input - Audio
        Matrix.Set('MatrixTieCommand', None, {'Input':'4','Output':'1','Tie Type':'Audio'})
        print('Button Pressed - Audio: %s' % 'ShareLink')
    pass

@event(PageAudio2, ButtonEventList)
def AudioVolEvents(button, state):
    ## Data of current Biamp Block Gain
    global currentlvl
    currentlvl = Biamp_Data['Lvl_Spk']    
    ## Audio Speaker Control - Vol -
    if button is BtnXSpkLess:    
        if state == 'Pressed' or state == 'Repeated':
            BtnXSpkLess.SetState(1)
            currentlvl -= 5
            #--
            if currentlvl >= -100:
                Biamp.Set('LevelControl',currentlvl,{'Instance Tag':'lvl_spk','Channel':'1'})
                LevelSpk.SetLevel(currentlvl)
                print('Audio: %s' % 'Spk-')
            else:
                print('Audio: %s' % 'Spk- Full')
        else:
            BtnXSpkLess.SetState(0)
    ## Audio Speaker Control - Vol +
    elif button is BtnXSpkPlus:
        if state == 'Pressed' or state == 'Repeated':
            BtnXSpkPlus.SetState(1)
            currentlvl += 5
            #--
            if currentlvl < 12:
                Biamp.Set('LevelControl',currentlvl,{'Instance Tag':'lvl_spk','Channel':'1'})
                LevelSpk.SetLevel(currentlvl)
                print('Audio: %s' % 'Spk+')
            else:
                print('Audio: %s' % 'Spk+ Full')
        else:
            BtnXSpkPlus.SetState(0)
    ## Audio VC Remote Control - Vol -
    elif button is BtnXVCLess and state == 'Pressed':
        print('Button Pressed - Audio: %s' % 'VC-')
    elif button is BtnXVCLess and state == 'Repeated':
        print('Button Repeated - Audio: %s' % 'VC-')
    ## Audio VC Remote Control - Vol +
    elif button is BtnXVCPlus and state == 'Pressed':
        print('Button Pressed - Audio: %s' % 'VC+')
    elif button is BtnXVCPlus and state == 'Repeated':
        print('Button Repeated - Audio: %s' % 'VC+')
    pass

@event(PageAudio3, ButtonEventList)
def AudioMuteEvents(button, state):
    ## Mute Speaker Audio Control
    if button is BtnXSpk and state == 'Pressed':
        print('Mute Spk Dictionary: ' + Biamp_Data['Mute_Spk'])
        if Biamp_Data['Mute_Spk'] == 'On':
            Biamp.Set('MuteControl','Off',{'Instance Tag':'lvl_spk','Channel':'1'})
        elif Biamp_Data['Mute_Spk'] == 'Off':
            Biamp.Set('MuteControl','On',{'Instance Tag':'lvl_spk','Channel':'1'})
        print('Button Pressed - Audio: %s' % 'Mute Spk')
    ## Mute VC Remote Audio Control
    elif button is BtnXVC and state == 'Pressed':
        print('Mute VC.Rx Dictionary: ' + Biamp_Data['Mute_VCRx'])
        if Biamp_Data['Mute_VCRx'] == 'On':
            Biamp.Set('MuteControl','Off',{'Instance Tag':'lvl_vcrx','Channel':'1'})
        elif Biamp_Data['Mute_VCRx'] == 'Off':
            Biamp.Set('MuteControl','On',{'Instance Tag':'lvl_vcrx','Channel':'1'})
        print('Button Pressed - Audio: %s' % 'Mute VC')
    ## Mute All Mics Audio Control
    elif button is BtnXMics and state == 'Pressed':
        print('Mute Mix Dictionary: ' + Biamp_Data['Mute_Mics'])
        if Biamp_Data['Mute_Mics'] == 'On':
            Biamp.Set('MuteControl','Off',{'Instance Tag':'mute_mix','Channel':'1'})
        elif Biamp_Data['Mute_Mics'] == 'Off':
            Biamp.Set('MuteControl','On',{'Instance Tag':'mute_mix','Channel':'1'})
        print('Button Pressed - Audio: %s' % 'Mute Mics')
    pass

## Page Status -----------------------------------------------------------------

## Page PowerOff ---------------------------------------------------------------
@event(BtnPowerAll, ButtonEventList)
def PowerEvents(button, state):
    if state == 'Pressed':
        print('Button Pressed: %s' % 'PowerAll')
    elif state == 'Held':
        print('Button Held: %s' % 'PowerAll')
    pass

## End Events Definitions-------------------------------------------------------

Initialize()