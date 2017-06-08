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
## Begin User Import -----------------------------------------------------------
import extr_matrix_DXPHD4k_Series_v1_1_1_0 as MatrixLAN
import extr_sm_SMP_300_Series_v1_8_0_1 as SMP351LAN
import csco_vtc_SX_Series_TC73_v1_3_0_0 as CiscoLAN
#--
Matrix = MatrixLAN.EthernetClass('10.10.10.50', 23, Model='DXP 44 HD 4k')
SMP351 = SMP351LAN.EthernetClass('10.10.10.51', 23, Model='SMP 351')
Cisco  = CiscoLAN.EthernetClass('10.10.10.52', 23, Model='SX20 TC7.3.X')
## End User Import -------------------------------------------------------------
##
## Begin Device Definition -----------------------------------------------------

## End Device Definition -------------------------------------------------------
##
## Begin Device/Processor Definition -------------------------------------------
IPCP = ProcessorDevice('IPlink')
## End Device/Processor Definition ---------------------------------------------
##
## Begin Device/User Interface Definition --------------------------------------
TLP = UIDevice('TouchPanel')
## End Device/User Interface Definition ----------------------------------------
##
## Begin Communication Interface Definition ------------------------------------
## Index
BtnIndex     = Button(TLP, 1)
## Main
BtnVideo     = Button(TLP, 2)
BtnVC        = Button(TLP, 3)
BtnWebex     = Button(TLP, 4)
BtnRec       = Button(TLP, 5)
BtnVoIP      = Button(TLP, 6)
BtnAudio     = Button(TLP, 7)
BtnStatus    = Button(TLP, 8)
BtnPwrOff    = Button(TLP, 9)
LblMode      = Label(TLP, 300)
## Video
BtnDisplayL  = Button(TLP, 11)
BtnDisplayR  = Button(TLP, 12)
BtnPTZ       = Button(TLP, 13)
## Display L
BtnLHDMI     = Button(TLP, 21)
BtnLVGA      = Button(TLP, 22)
BtnLPTZ      = Button(TLP, 23)
BtnLShare    = Button(TLP, 24)
BtnLPwrOn    = Button(TLP, 25)
BtnLPwrOff   = Button(TLP, 26)
BtnLBack     = Button(TLP, 27)
## Display R
BtnRHDMI     = Button(TLP, 31)
BtnRVGA      = Button(TLP, 32)
BtnRPTZ      = Button(TLP, 33)
BtnRShare    = Button(TLP, 34)
BtnRPwrOn    = Button(TLP, 35)
BtnRPwrOff   = Button(TLP, 36)
BtnRBack     = Button(TLP, 37)
## PTZ
BtnP1        = Button(TLP, 41)
BtnP2        = Button(TLP, 42)
BtnP3        = Button(TLP, 43)
BtnP4        = Button(TLP, 44)
BtnP5        = Button(TLP, 45)
BtnRecall    = Button(TLP, 46)
BtnSave      = Button(TLP, 47)
##
BtnZoom1     = Button(TLP, 48, repeatTime = 0.1)
BtnZoom2     = Button(TLP, 49, repeatTime = 0.1)
##
BtnPTZUp     = Button(TLP, 50, repeatTime = 0.1)
BtnPTZLeft   = Button(TLP, 51, repeatTime = 0.1)
BtnPTZDown   = Button(TLP, 52, repeatTime = 0.1)
BtnPTZRight  = Button(TLP, 53, repeatTime = 0.1)
##
BtnPTZPwr    = Button(TLP, 54)
## Webex
BtnWHDMI     = Button(TLP, 61)
BtnWVGA      = Button(TLP, 62)
BtnWPTZ      = Button(TLP, 63)
BtnWShare    = Button(TLP, 64)
BtnWCisco1   = Button(TLP, 65)
BtnWCisco2   = Button(TLP, 66)
## REC
Btn4HDMI     = Button(TLP, 71)
Btn4VGA      = Button(TLP, 72)
Btn4PTZ      = Button(TLP, 73)
Btn4Share    = Button(TLP, 74)
Btn4Cisco1   = Button(TLP, 75)
Btn4Cisco2   = Button(TLP, 76)
##
Btn4Mic      = Button(TLP, 77)
Btn4VC       = Button(TLP, 78)
Btn4VoIP     = Button(TLP, 79)
Btn4PC       = Button(TLP, 80)
##
BtnPause     = Button(TLP, 81)
BtnREC       = Button(TLP, 82)
BtnStop      = Button(TLP, 83)
LblRes       = Label(TLP, 84)
BtnRecAV     = Button(TLP, 85)
BtnRecV      = Button(TLP, 86)
LblElapsed   = Label(TLP, 87)
## VoIP
BtnCall      = Button(TLP, 91)
BtnHangup    = Button(TLP, 92)
##
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
## 
BtnRedial    = Button(TLP, 112)
BtnDTMF      = Button(TLP, 113)
BtnHold      = Button(TLP, 114)
BtnDelete    = Button(TLP, 115)
LblDial      = Label(TLP, 116)
## VC
BtnVCCall    = Button(TLP, 131)
BtnVCHangup  = Button(TLP, 132)
##
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
## 
BtnVCEnviar  = Button(TLP, 152)
BtnVCCamara  = Button(TLP, 153)
BtnVCAutoAn  = Button(TLP, 154)
BtnVCDelete  = Button(TLP, 155, repeatTime = 0.1)
LblVCDial    = Label(TLP, 156)
## VC - Content
BtnVCHDMI    = Button(TLP, 181)
BtnVCVGA     = Button(TLP, 182)
BtnVCPTZ     = Button(TLP, 183)
BtnVCShare   = Button(TLP, 184)
##
BtnVCBack2   = Button(TLP, 185)
BtnVCSend    = Button(TLP, 186)
BtnVCStop    = Button(TLP, 187)
## VC - Camera
BtnVCP1      = Button(TLP, 161)
BtnVCP2      = Button(TLP, 162)
BtnVCP3      = Button(TLP, 163)
BtnVCP4      = Button(TLP, 164)
BtnVCP5      = Button(TLP, 165)
BtnVCRecall  = Button(TLP, 166)
BtnVCSave  = Button(TLP, 167)
##
BtnVCZoom1   = Button(TLP, 168, repeatTime = 0.1)
BtnVCZoom2   = Button(TLP, 169, repeatTime = 0.1)
##
BtnVCUp      = Button(TLP, 170, repeatTime = 0.1)
BtnVCLeft    = Button(TLP, 171, repeatTime = 0.1)
BtnVCDown    = Button(TLP, 172, repeatTime = 0.1)
BtnVCRight   = Button(TLP, 173, repeatTime = 0.1)
##
BtnVCLocal   = Button(TLP, 174)
BtnVCRemote  = Button(TLP, 175)
## Audio
BtnXHDMI     = Button(TLP, 188)
BtnXVGA      = Button(TLP, 189)
BtnXShare    = Button(TLP, 190)
##
BtnXSpkLess  = Button(TLP, 191, repeatTime = 0.1)
BtnXSpkPlus  = Button(TLP, 192, repeatTime = 0.1)
BtnXVCLess   = Button(TLP, 193, repeatTime = 0.1)
BtnXVCPlus   = Button(TLP, 194, repeatTime = 0.1)
LevelSpk     = Level(TLP, 195)
LevelVC      = Level(TLP, 196)
##
BtnXSpk      = Button(TLP, 197)
BtnXVC       = Button(TLP, 198)
BtnXMics     = Button(TLP, 199)
## Status
Btn232LCD1   = Button(TLP, 211)
Btn232LCD2   = Button(TLP, 212)
BtnLANMatrix = Button(TLP, 213)
BtnLANTesira = Button(TLP, 214)
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
## Power
BtnPowerAll  = Button(TLP, 250, holdTime = 3)
LblPowerAll  = Label(TLP, 251)

## Group Main
PageMain   = [BtnVideo, BtnVC, BtnWebex, BtnRec, BtnVoIP, 
              BtnAudio, BtnStatus, BtnPwrOff]
GroupMain  = MESet(PageMain)
## Group Video
PageVideo   = [BtnDisplayL, BtnDisplayR, BtnPTZ]
## Group Display L
PageLCD1    = [BtnLHDMI, BtnLVGA, BtnLPTZ, BtnLShare, BtnLPwrOn, 
               BtnLPwrOff, BtnLBack]
## Group Display R
PageLCD2    = [BtnRHDMI, BtnRVGA, BtnRPTZ, BtnRShare, BtnRPwrOn,
               BtnRPwrOff, BtnRBack]
## Group PTZ
PagePTZNav  = [BtnPTZUp, BtnPTZLeft, BtnPTZDown, BtnPTZRight,
               BtnZoom1, BtnZoom2, BtnPTZPwr]
PagePTZPst  = [BtnP1, BtnP2, BtnP3, BtnP4, BtnP5, BtnRecall, BtnSave]
GroupPTZ    = MESet([BtnRecall, BtnSave])
## Group VC
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
## Group Webex
PageWebex   = [BtnWHDMI, BtnWVGA, BtnWPTZ, BtnWShare, BtnWCisco1, BtnWCisco2]
## Group REC
PageRecV    = [Btn4HDMI, Btn4VGA, Btn4PTZ, Btn4Share, Btn4Cisco1, Btn4Cisco2]
PageRecA    = [Btn4Mic, Btn4VC, Btn4VoIP, Btn4PC]
PageRecNav  = [BtnPause, BtnREC, BtnStop]
## Group VoIP
PageTelCall = [BtnCall, BtnHangup]
PageTelDial = [BtnDial0, BtnDial1, BtnDial2, BtnDial3, BtnDial4, BtnDial5,
               BtnDial6, BtnDial7, BtnDial8, BtnDial9, BtnDialA, BtnDialG]
PageTelOpt  = [BtnRedial, BtnDTMF, BtnHold, BtnDelete]
## Group Audio
PageAudio1  = [BtnXHDMI, BtnXVGA, BtnXShare]
PageAudio2  = [BtnXSpkLess, BtnXSpkPlus, BtnXVCLess, BtnXVCPlus]
PageAudio3  = [BtnXSpk, BtnXVC, BtnXMics]
##
ButtonEventList = ['Pressed', 'Released', 'Held', 'Repeated', 'Tapped']
## End Communication Interface Definition --------------------------------------

def Initialize():
    #--
    global PTZ_Status
    global VC_Status
    VC_Status['Preset_Mode'] = 'Recall'    
    VC_Status['Camera'] = 'Local'
    GroupVCPTZ.SetCurrent(BtnVCRecall)
    GroupVCCam.SetCurrent(BtnVCLocal)
    #
    GroupMain.SetCurrent(None)
    #--
    global dialerVC
    dialerVC = []
    VC_Status['Dial'] = ''
    LblVCDial.SetText('')
    #--
    TLP.HideAllPopups()
    TLP.ShowPage('Index')
    #--
    print('System Inicializate')
    pass

## Data Dictionaries -----------------------------------------------------------
PTZ_Status = {
    'Preset_Mode' : '',
    'Power'       : '',
}
VC_Status = {
    'Dial'        : '',
    'Preset_Mode' : '',
    'Camera'      : '',
    'Power'       : '',
}
## Event Definitions -----------------------------------------------------------
@event(BtnIndex,'Pressed')
def IndexEvents(button, state):
    TLP.ShowPage('Main')
    TLP.ShowPopup('x_Welcome')
    print('Touch Mode: %s' % 'Index')
    pass
## Page Main -------------------------------------------------------------------
@event(PageMain, ButtonEventList)
def MainEvents(button, state):
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
    GroupMain.SetCurrent(button)
    pass
    
## Page Video ------------------------------------------------------------------
@event(PageVideo, ButtonEventList)
def VideoEvents(button, state):
    if button is BtnDisplayL and state == 'Pressed':
        TLP.ShowPopup('Display_L')
        LblMode.SetText('Control de Pantalla Izquierda')
        print('Video Mode: %s' % 'Display L')
    elif button is BtnDisplayR and state == 'Pressed':
        TLP.ShowPopup('Display_R')
        LblMode.SetText('Control de Pantalla Derecha')
        print('Video Mode: %s' % 'Display R')
    elif button is BtnPTZ and state == 'Pressed':
        TLP.ShowPopup('PTZ')
        LblMode.SetText('Control de Cámara PTZ')
        print('Video Mode: %s' % 'PTZ')
    pass
    
## Page Display L --------------------------------------------------------------
@event(PageLCD1, ButtonEventList)
def DisplayLEvents(button, state):
    if button is BtnLHDMI and state == 'Pressed':
        Matrix.Set('MatrixTieCommand', None, {'Input':'1','Output':'1','Tie Type':'Video'})
        print('Button Pressed - LCD L: %s' % 'HDMI')
    elif button is BtnLVGA and state == 'Pressed':
        Matrix.Set('MatrixTieCommand', None, {'Input':'2','Output':'1','Tie Type':'Video'})
        print('Button Pressed - LCD L: %s' % 'VGA')
    elif button is BtnLPTZ and state == 'Pressed':
        Matrix.Set('MatrixTieCommand', None, {'Input':'3','Output':'1','Tie Type':'Video'})
        print('Button Pressed - LCD L: %s' % 'PTZ')
    elif button is BtnLShare and state == 'Pressed':
        Matrix.Set('MatrixTieCommand', None, {'Input':'4','Output':'1','Tie Type':'Video'})
        print('Button Pressed - LCD L: %s' % 'ShareLink')
    elif button is BtnLPwrOn and state == 'Pressed':
        print('Button Pressed - LCD L: %s' % 'PowerOn')
    elif button is BtnLPwrOff and state == 'Pressed':
        print('Button Pressed - LCD L: %s' % 'PowerOff')
    elif button is BtnLBack and state == 'Pressed':
        TLP.ShowPopup('Video')
        print('Button Pressed - LCD L: %s' % 'Back')
    pass
## Page Display R --------------------------------------------------------------
@event(PageLCD2, ButtonEventList)
def DisplayREvents(button, state):
    if button is BtnRHDMI and state == 'Pressed':
        Matrix.Set('MatrixTieCommand', None, {'Input':'1','Output':'2','Tie Type':'Video'})
        print('Button Pressed - LCD R: %s' % 'HDMI')
    elif button is BtnRVGA and state == 'Pressed':
        Matrix.Set('MatrixTieCommand', None, {'Input':'2','Output':'2','Tie Type':'Video'})
        print('Button Pressed - LCD R: %s' % 'VGA')
    elif button is BtnRPTZ and state == 'Pressed':
        Matrix.Set('MatrixTieCommand', None, {'Input':'3','Output':'2','Tie Type':'Video'})
        print('Button Pressed - LCD R: %s' % 'PTZ')
    elif button is BtnRShare and state == 'Pressed':
        Matrix.Set('MatrixTieCommand', None, {'Input':'4','Output':'2','Tie Type':'Video'})
        print('Button Pressed - LCD R: %s' % 'ShareLink')
    elif button is BtnRPwrOn and state == 'Pressed':
        print('Button Pressed - LCD R: %s' % 'PowerOn')
    elif button is BtnRPwrOff and state == 'Pressed':
        print('Button Pressed - LCD R: %s' % 'PowerOff')
    elif button is BtnRBack and state == 'Pressed':
        TLP.ShowPopup('Video')
        print('Button Pressed - LCD R: %s' % 'Back')
    pass
## Page PTZ --------------------------------------------------------------------
@event(PagePTZPst, ButtonEventList)
def PZTEvents(button, state):
    #--
    if button is BtnP1 and state == 'Pressed':
        if PTZ_Status['Preset_Mode'] == 'Recall':
            print('Recall Preset - PTZ: %s' % '1')
        elif PTZ_Status['Preset_Mode'] == 'Save':
            print('Save Preset - PTZ: %s' % '1')
    #--
    elif button is BtnP2 and state == 'Pressed':
        if PTZ_Status['Preset_Mode'] == 'Recall':
            print('Recall Preset - PTZ: %s' % '2')
        elif PTZ_Status['Preset_Mode'] == 'Save':
            print('Save Preset - PTZ: %s' % '2')
    #--
    elif button is BtnP3 and state == 'Pressed':
        if PTZ_Status['Preset_Mode'] == 'Recall':
            print('Recall Preset - PTZ: %s' % '3')
        elif PTZ_Status['Preset_Mode'] == 'Save':
            print('Save Preset - PTZ: %s' % '3')
    #--
    elif button is BtnP4 and state == 'Pressed':
        if PTZ_Status['Preset_Mode'] == 'Recall':
            print('Recall Preset - PTZ: %s' % '4')
        elif PTZ_Status['Preset_Mode'] == 'Save':
            print('Save Preset - PTZ: %s' % '4')
    #--    
    elif button is BtnP5 and state == 'Pressed':
        if PTZ_Status['Preset_Mode'] == 'Recall':
            print('Recall Preset - PTZ: %s' % '5')
        elif PTZ_Status['Preset_Mode'] == 'Save':
            print('Save Preset - PTZ: %s' % '5')
    #--
    elif button is BtnRecall and state == 'Pressed':
        PTZ_Status['Preset_Mode'] = 'Recall'
        GroupPTZ.SetCurrent(BtnRecall)
        print('Button Pressed - PTZ: %s' % 'Recall')
    #--
    elif button is BtnSave and state == 'Pressed':
        PTZ_Status['Preset_Mode'] = 'Save'
        GroupPTZ.SetCurrent(BtnSave)
        print('Button Pressed - PTZ: %s' % 'Save')
    pass

@event(PagePTZNav, ButtonEventList)
def PTZEvents2(button, state):
    #--
    if button is BtnPTZUp and state == 'Pressed':
        print('Button Pressed - PTZ: %s' % 'Up')
    elif button is BtnPTZUp and state == 'Repeated':
        print('Button Repeated - PTZ: %s' % 'Up')
    elif button is BtnPTZUp and state == 'Released':
        print('Button Relased - PTZ: %s' % 'Up - Stop')
    #--
    elif button is BtnPTZLeft and state == 'Pressed':
        print('Button Pressed - PTZ: %s' % 'Left')
    elif button is BtnPTZLeft and state == 'Repeated':
        print('Button Repeated - PTZ: %s' % 'Left')
    elif button is BtnPTZLeft and state == 'Released':
        print('Button Relased - PTZ: %s' % 'Left - Stop')
    #--
    elif button is BtnPTZDown and state == 'Pressed':
        print('Button Pressed - PTZ: %s' % 'Down')
    elif button is BtnPTZDown and state == 'Repeated':
        print('Button Repeated - PTZ: %s' % 'Down')
    elif button is BtnPTZDown and state == 'Released':
        print('Button Relased - PTZ: %s' % 'Down - Stop')
    #--
    elif button is BtnPTZRight and state == 'Pressed':
        print('Button Pressed - PTZ: %s' % 'Right')
    elif button is BtnPTZRight and state == 'Repeated':
        print('Button Repeated - PTZ: %s' % 'Right')
    elif button is BtnPTZRight and state == 'Released':
        print('Button Relased - PTZ: %s' % 'Right - Stop')
    #--
    elif button is BtnZoom1 and state == 'Pressed':
        print('Button Pressed - PTZ: %s' % 'Zoom+')
    elif button is BtnZoom1 and state == 'Repeated':
        print('Button Repeated - PTZ: %s' % 'Zoom+')
    elif button is BtnZoom1 and state == 'Released':
        print('Button Relased - PTZ: %s' % 'Zoom+ - Stop')
    #--
    elif button is BtnZoom2 and state == 'Pressed':
        print('Button Pressed - PTZ: %s' % 'Zoom-')
    elif button is BtnZoom2 and state == 'Repeated':
        print('Button Repeated - PTZ: %s' % 'Zoom-')
    elif button is BtnZoom2 and state == 'Released':
        print('Button Relased - PTZ: %s' % 'Zoom- - Stop')
    #--
    elif button is BtnPTZPwr and state == 'Pressed':
        print('Button Pressed - PTZ: %s' % 'Power')
        if PTZ_Status['Power'] == 'On':
            print('Power PTZ: %s' % 'Power Off')
        if PTZ_Status['Power'] == 'Off':
            print('Power PTZ: %s' % 'Power On')
    pass
## Page VC ---------------------------------------------------------------------
@event(PageVCCall, ButtonEventList)
def VCCallEvents(button, state):
    if button is BtnVCCall and state == 'Pressed':
        Cisco.Set('Hook','Dial',{'Protocol':'H323','Number': VC_Status['Dial']})
        print('Button Pressed - VC: %s' % 'Call')
    elif button is BtnVCHangup and state == 'Pressed':
        Cisco.Set('Hook','Disconnect All',{'Protocol':'H323'})
        print('Button Pressed - VC: %s' % 'Hangup')
    pass

def DialerVC(btn_name):
    def CleanDialer():            #Function for clean the added/removed data
        Clean = "".join(dialerVC) #Convert the list to a string
        LblVCDial.SetText(Clean)  #Show the cleaned data into the GUI Label
        VC_Status['Dial'] = Clean #Asign the final data to the data dictionaire
        print(VC_Status['Dial'])  #Notifiy to console
    #--
    if btn_name == 'Delete':      #If the user push 'Delete' button
        if len(dialerVC) <= 0:    #If the Dialer is Null
            print('Null VC Dial') #Notify to console
        else:                     #If the Dialer have any data
            dialerVC.pop()        #Remove the last character
            CleanDialer()         #Recall a clean data function
    else:                         #If the user push a [*#0-9] button
        Number = str(btn_name[4]) #Extract the valid character of btn name
        dialerVC.append(Number)   #Append this valid character
        CleanDialer()             #Recall a clean data function
    pass

@event(PageVCDial, ButtonEventList)
def VCDialEvents(button, state):
    if state == 'Pressed':
        print('Button Pressed - VC: %s' % button.Name)
        DialerVC(button.Name) #Recall a validation function
        button.SetState(1)
    if state == 'Repeated':
        print('Button Repeat  - VC: %s' % button.Name)
        DialerVC(button.Name) #Recall a validation function
        button.SetState(1)
    else:
        button.SetState(0)
    pass

@event(PageVCOpt, ButtonEventList)
def VCOptEvents(button, state):
    if button is BtnVCEnviar and state == 'Pressed':
        TLP.ShowPopup('VC_Content')
        print('Button Pressed - VC: %s' % 'Content')
    elif button is BtnVCCamara and state == 'Pressed':
        TLP.ShowPopup('VC_Cam')
        print('Button Pressed - VC: %s' % 'Camera')
    elif button is BtnVCAutoAn and state == 'Pressed':
        Cisco.Set('AutoAnswer','On')
        print('Button Pressed - VC: %s' % 'AutoAnswer')
    pass
## Page VC Content -------------------------------------------------------------
@event(PageVCShare, ButtonEventList)
def VCCamEvents(button, state):
    if button is BtnVCHDMI and state == 'Pressed':
        Matrix.Set('MatrixTieCommand', None, {'Input':'1','Output':'3','Tie Type':'Video'})
        print('Button Pressed - VC Share: %s' % 'HDMI')
    elif button is BtnVCVGA and state == 'Pressed':
        Matrix.Set('MatrixTieCommand', None, {'Input':'2','Output':'3','Tie Type':'Video'})
        print('Button Pressed - VC Share: %s' % 'VGA')
    elif button is BtnVCPTZ and state == 'Pressed':
        Matrix.Set('MatrixTieCommand', None, {'Input':'3','Output':'3','Tie Type':'Video'})
        print('Button Pressed - VC Share: %s' % 'PTZ')
    elif button is BtnVCShare and state == 'Pressed':
        Matrix.Set('MatrixTieCommand', None, {'Input':'4','Output':'3','Tie Type':'Video'})
        print('Button Pressed - VC Share: %s' % 'ClickShare')
    elif button is BtnVCBack2 and state == 'Pressed':
        TLP.ShowPopup('VC')
        print('Button Pressed - VC Share: %s' % 'Back')
    elif button is BtnVCSend and state == 'Pressed':
        Cisco.Set('Presentation','1') #Share Grahpics
        print('Button Pressed - VC Share: %s' % 'Send')
    elif button is BtnVCStop and state == 'Pressed':
        Cisco.Set('Presentation','Stop')
        print('Button Pressed - VC Share: %s' % 'Stop')
    pass
## Page VC Camera --------------------------------------------------------------
@event(PageVCCamN,ButtonEventList)
def VCNavEvents(button, state):
    #--
    if button is BtnVCUp:
        if state == 'Pressed' or state == 'Repeated':
            if VC_Status['Camera'] == 'Local':
                print('Cam Local - Cisco: %s' % 'Cam Up')
            elif VC_Status['Camera'] == 'Remote':
                print('Cam Remota - Cisco: %s' % 'Cam Up')
        elif state == 'Released':
            if VC_Status['Camera'] == 'Local':
                print('Cam Local - Cisco: %s' % 'Cam Stop')
            elif VC_Status['Camera'] == 'Remote':
                print('Cam Remota - Cisco: %s' % 'Cam Stop')
    #--
    elif button is BtnVCLeft:
        if state == 'Pressed' or state == 'Repeated':
            if VC_Status['Camera'] == 'Local':
                print('Cam Local - Cisco: %s' % 'Cam Left')
            elif VC_Status['Camera'] == 'Remote':
                print('Cam Remota - Cisco: %s' % 'Cam Left')
        elif state == 'Released':
            if VC_Status['Camera'] == 'Local':
                print('Cam Local - Cisco: %s' % 'Cam Stop')
            elif VC_Status['Camera'] == 'Remote':
                print('Cam Remota - Cisco: %s' % 'Cam Stop')
    #--
    elif button is BtnVCDown:
        if state == 'Pressed' or state == 'Repeated':
            if VC_Status['Camera'] == 'Local':
                print('Cam Local - Cisco: %s' % 'Cam Down')
            elif VC_Status['Camera'] == 'Remote':
                print('Cam Remota - Cisco: %s' % 'Cam Down')
        elif state == 'Released':
            if VC_Status['Camera'] == 'Local':
                print('Cam Local - Cisco: %s' % 'Cam Stop')
            elif VC_Status['Camera'] == 'Remote':
                print('Cam Remota - Cisco: %s' % 'Cam Stop')
    #--
    elif button is BtnVCRight:
        if state == 'Pressed' or state == 'Repeated':
            if VC_Status['Camera'] == 'Local':
                print('Cam Local - Cisco: %s' % 'Cam Right')
            elif VC_Status['Camera'] == 'Remote':
                print('Cam Remota - Cisco: %s' % 'Cam Right')
        elif state == 'Released':
            if VC_Status['Camera'] == 'Local':
                print('Cam Local - Cisco: %s' % 'Cam Stop')
            elif VC_Status['Camera'] == 'Remote':
                print('Cam Remota - Cisco: %s' % 'Cam Stop')
    #--
    elif button is BtnVCZoom1:
        if state == 'Pressed' or state == 'Repeated':
            if VC_Status['Camera'] == 'Local':
                print('Cam Local - Cisco: %s' % 'Cam Zoom+')
            elif VC_Status['Camera'] == 'Remote':
                print('Cam Remota - Cisco: %s' % 'Cam Zoom+')
        elif state == 'Released':
            if VC_Status['Camera'] == 'Local':
                print('Cam Local - Cisco: %s' % 'Cam Stop')
            elif VC_Status['Camera'] == 'Remote':
                print('Cam Remota - Cisco: %s' % 'Cam Stop')
    #--
    elif button is BtnVCZoom2:
        if state == 'Pressed' or state == 'Repeated':
            if VC_Status['Camera'] == 'Local':
                print('Cam Local - Cisco: %s' % 'Cam Zoom-')
            elif VC_Status['Camera'] == 'Remote':
                print('Cam Remota - Cisco: %s' % 'Cam Zoom-')
        elif state == 'Released':
            if VC_Status['Camera'] == 'Local':
                print('Cam Local - Cisco: %s' % 'Cam Stop')
            elif VC_Status['Camera'] == 'Remote':
                print('Cam Remota - Cisco: %s' % 'Cam Stop')
    #--
    if button is BtnVCLocal and state == 'Pressed':
        VC_Status['Camera'] = 'Local'
        GroupVCCam.SetCurrent(BtnVCLocal)
        print('Button Pressed - Cisco: %s' % 'Cam Local')
    #--
    elif button is BtnVCRemote and state == 'Pressed':
        VC_Status['Camera'] = 'Remote'
        GroupVCCam.SetCurrent(BtnVCRemote)
        print('Button Pressed - Cisco: %s' % 'Cam Remote')
    pass

@event(PageVCCamP, ButtonEventList)
def VCCamEvents(button, state):
    #--
    if button is BtnVCP1 and state == 'Pressed':
        if VC_Status['Camera'] == 'Local':
            if VC_Status['Preset_Mode'] == 'Recall':
                print('Recall Local Preset Cisco: %s' % '1')
            elif VC_Status['Preset_Mode'] == 'Save':
                print('Save Local Preset Cisco: %s' % '1')
        elif VC_Status['Camera'] == 'Remote':
            if VC_Status['Preset_Mode'] == 'Recall':
                print('Recall Remote Preset Cisco: %s' % '1')
            elif VC_Status['Preset_Mode'] == 'Save':
                print('Save Remote Preset Cisco: %s' % '1')
    #--
    elif button is BtnVCP2 and state == 'Pressed':
        if VC_Status['Camera'] == 'Local':
            if VC_Status['Preset_Mode'] == 'Recall':
                print('Recall Local Preset Cisco: %s' % '2')
            elif VC_Status['Preset_Mode'] == 'Save':
                print('Save Local Preset Cisco: %s' % '2')
        elif VC_Status['Camera'] == 'Remote':
            if VC_Status['Preset_Mode'] == 'Recall':
                print('Recall Remote Preset Cisco: %s' % '2')
            elif VC_Status['Preset_Mode'] == 'Save':
                print('Save Remote Preset Cisco: %s' % '2')
    #--
    elif button is BtnVCP3 and state == 'Pressed':
        if VC_Status['Camera'] == 'Local':
            if VC_Status['Preset_Mode'] == 'Recall':
                print('Recall Local Preset Cisco: %s' % '3')
            elif VC_Status['Preset_Mode'] == 'Save':
                print('Save Local Preset Cisco: %s' % '3')
        elif VC_Status['Camera'] == 'Remote':
            if VC_Status['Preset_Mode'] == 'Recall':
                print('Recall Remote Preset Cisco: %s' % '3')
            elif VC_Status['Preset_Mode'] == 'Save':
                print('Save Remote Preset Cisco: %s' % '3')
    #--
    elif button is BtnVCP4 and state == 'Pressed':
        if VC_Status['Camera'] == 'Local':
            if VC_Status['Preset_Mode'] == 'Recall':
                print('Recall Local Preset Cisco: %s' % '4')
            elif VC_Status['Preset_Mode'] == 'Save':
                print('Save Local Preset Cisco: %s' % '4')
        elif VC_Status['Camera'] == 'Remote':
            if VC_Status['Preset_Mode'] == 'Recall':
                print('Recall Remote Preset Cisco: %s' % '4')
            elif VC_Status['Preset_Mode'] == 'Save':
                print('Save Remote Preset Cisco: %s' % '4')
    #--
    elif button is BtnVCP5 and state == 'Pressed':
        if VC_Status['Camera'] == 'Local':
            if VC_Status['Preset_Mode'] == 'Recall':
                print('Recall Local Preset Cisco: %s' % '5')
            elif VC_Status['Preset_Mode'] == 'Save':
                print('Save Local Preset Cisco: %s' % '5')
        elif VC_Status['Camera'] == 'Remote':
            if VC_Status['Preset_Mode'] == 'Recall':
                print('Recall Remote Preset Cisco: %s' % '5')
            elif VC_Status['Preset_Mode'] == 'Save':
                print('Save Remote Preset Cisco: %s' % '5')
    #--
    elif button is BtnVCRecall and state == 'Pressed':
        VC_Status['Preset_Mode'] = 'Recall'
        GroupVCPTZ.SetCurrent(BtnVCRecall)
        print('Button Pressed - Cisco: %s' % 'Recall')
    #--
    elif button is BtnVCSave and state == 'Pressed':
        VC_Status['Preset_Mode'] = 'Save'
        GroupVCPTZ.SetCurrent(BtnVCSave)
        print('Button Pressed - Cisco: %s' % 'Save')
    pass
## Page Webex ------------------------------------------------------------------
@event(PageWebex, ButtonEventList)
def WebexEvents(button, state):
    if button is BtnWHDMI and state == 'Pressed':
        Matrix.Set('MatrixTieCommand', None, {'Input':'1','Output':'5','Tie Type':'Video'})
        print('Button Pressed - Webex: %s' % 'HDMI')
    elif button is BtnWVGA and state == 'Pressed':
        Matrix.Set('MatrixTieCommand', None, {'Input':'2','Output':'5','Tie Type':'Video'})
        print('Button Pressed - Webex: %s' % 'VGA')
    elif button is BtnWPTZ and state == 'Pressed':
        Matrix.Set('MatrixTieCommand', None, {'Input':'3','Output':'5','Tie Type':'Video'})
        print('Button Pressed - Webex: %s' % 'PTZ')
    elif button is BtnWShare and state == 'Pressed':
        Matrix.Set('MatrixTieCommand', None, {'Input':'4','Output':'5','Tie Type':'Video'})
        print('Button Pressed - Webex: %s' % 'ShareLink')
    elif button is BtnWCisco1 and state == 'Pressed':
        Matrix.Set('MatrixTieCommand', None, {'Input':'5','Output':'5','Tie Type':'Video'})
        print('Button Pressed - Webex: %s' % 'Cisco 1')
    elif button is BtnWCisco2 and state == 'Pressed':
        Matrix.Set('MatrixTieCommand', None, {'Input':'6','Output':'5','Tie Type':'Video'})
        print('Button Pressed - Webex: %s' % 'Cisco 2')
    pass
## Page Recording --------------------------------------------------------------
@event(PageRecV, ButtonEventList)
def RecEventsV(button, state):
    if button is Btn4HDMI and state == 'Pressed':
        Matrix.Set('MatrixTieCommand', None, {'Input':'1','Output':'4','Tie Type':'Video'})
        print('Button Pressed - REC: %s' % 'HDMI')
    elif button is Btn4VGA and state == 'Pressed':
        Matrix.Set('MatrixTieCommand', None, {'Input':'2','Output':'4','Tie Type':'Video'})
        print('Button Pressed - REC: %s' % 'VGA')
    elif button is Btn4PTZ and state == 'Pressed':
        Matrix.Set('MatrixTieCommand', None, {'Input':'3','Output':'4','Tie Type':'Video'})
        print('Button Pressed - REC: %s' % 'PTZ')
    elif button is Btn4Share and state == 'Pressed':
        Matrix.Set('MatrixTieCommand', None, {'Input':'4','Output':'4','Tie Type':'Video'})
        print('Button Pressed - REC: %s' % 'ShareLink')
    elif button is Btn4Cisco1 and state == 'Pressed':
        Matrix.Set('MatrixTieCommand', None, {'Input':'5','Output':'4','Tie Type':'Video'})
        print('Button Pressed - REC: %s' % 'Cisco 1')
    elif button is Btn4Cisco2 and state == 'Pressed':
        Matrix.Set('MatrixTieCommand', None, {'Input':'6','Output':'4','Tie Type':'Video'})
        print('Button Pressed - REC: %s' % 'Cisco 2')
    pass

@event(PageRecA, ButtonEventList)
def RecEventsA(button, state):
    if button is Btn4Mic and state == 'Pressed':
        print('Button Pressed - REC: %s' % 'Mics')
    elif button is Btn4VC and state == 'Pressed':
        print('Button Pressed - REC: %s' % 'VC')
    elif button is Btn4VoIP and state == 'Pressed':
        print('Button Pressed - REC: %s' % 'VoIP')
    elif button is Btn4PC and state == 'Pressed': 
        print('Button Pressed - REC: %s' % 'PC')
    pass

@event(PageRecNav, ButtonEventList)
def RecEventsNav(button, state):
    if button is BtnPause and state == 'Pressed':
        SMP351.Set('Record','Pause')
        print('Button Pressed - REC: %s' % 'Pause')
    elif button is BtnREC and state == 'Pressed':
        SMP351.Set('Record','Start')
        print('Button Pressed - REC: %s' % 'Rec')
    elif button is BtnStop and state == 'Pressed':
        SMP351.Set('Record','Stop')
        print('Button Pressed - REC: %s' % 'Stop')
    pass
## Page VoIP -------------------------------------------------------------------
@event(PageTelCall, ButtonEventList)
def VCCallEvents(button, state):
    if button is BtnCall and state == 'Pressed':
        print('Button Pressed - VoIP: %s' % 'Call')
    elif button is BtnHangup and state == 'Pressed':
        print('Button Pressed - VoIP: %s' % 'Hangup')
    pass

@event(PageTelDial, ButtonEventList)
def VCDialEvents(button, state):
    if button is BtnDial0 and state == 'Pressed':
        print('Button Pressed - VoIP: %s' % 'Dial 0')
    elif button is BtnDial1 and state == 'Pressed':
        print('Button Pressed - VoIP: %s' % 'Dial 1')
    elif button is BtnDial2 and state == 'Pressed':
        print('Button Pressed - VoIP: %s' % 'Dial 2')
    elif button is BtnDial3 and state == 'Pressed':
        print('Button Pressed - VoIP: %s' % 'Dial 3')
    elif button is BtnDial4 and state == 'Pressed':
        print('Button Pressed - VoIP: %s' % 'Dial 4')
    elif button is BtnDial5 and state == 'Pressed':
        print('Button Pressed - VoIP: %s' % 'Dial 5')
    elif button is BtnDial6 and state == 'Pressed':
        print('Button Pressed - VoIP: %s' % 'Dial 6')
    elif button is BtnDial7 and state == 'Pressed':
        print('Button Pressed - VoIP: %s' % 'Dial 7')
    elif button is BtnDial8 and state == 'Pressed':
        print('Button Pressed - VoIP: %s' % 'Dial 8')
    elif button is BtnDial9 and state == 'Pressed':
        print('Button Pressed - VoIP: %s' % 'Dial 9')
    elif button is BtnDialA and state == 'Pressed':
        print('Button Pressed - VoIP: %s' % 'Dial *')
    elif button is BtnDialG and state == 'Pressed':
        print('Button Pressed - VoIP: %s' % 'Dial #')
    pass

@event(PageTelOpt, ButtonEventList)
def VCOptEvents(button, state):
    if button is BtnRedial and state == 'Pressed':
        print('Button Pressed - VoIP: %s' % 'Redial')
    elif button is BtnDTMF and state == 'Pressed':
        print('Button Pressed - VoIP: %s' % 'DTMF')
    elif button is BtnHold and state == 'Pressed':
        print('Button Pressed - VoIP: %s' % 'Hold/Resume')
    #--
    elif button is BtnDelete and state == 'Pressed':
        print('Button Pressed - VoIP: %s' % 'Delete')
    elif button is BtnDelete and state == 'Repeated':
        print('Button Repeated - VoIP: %s' % 'Delete')
    pass
## Page Audio ------------------------------------------------------------------
@event(PageAudio1, ButtonEventList)
def AudioSourceEvents(button, state):
    if button is BtnXHDMI and state == 'Pressed':
        Matrix.Set('MatrixTieCommand', None, {'Input':'1','Output':'1','Tie Type':'Audio'})
        print('Button Pressed - Audio: %s' % 'HDMI')
    elif button is BtnXVGA and state == 'Pressed':
        Matrix.Set('MatrixTieCommand', None, {'Input':'2','Output':'1','Tie Type':'Audio'})
        print('Button Pressed - Audio: %s' % 'VGA')
    elif button is BtnXShare and state == 'Pressed':
        Matrix.Set('MatrixTieCommand', None, {'Input':'4','Output':'1','Tie Type':'Audio'})
        print('Button Pressed - Audio: %s' % 'ShareLink')
    pass
    
@event(PageAudio2, ButtonEventList)
def AudioVolEvents(button, state):
    if button is BtnXSpkLess and state == 'Pressed':
        print('Button Pressed - Audio: %s' % 'Spk-')
    elif button is BtnXSpkLess and state == 'Repeated':
        print('Button Repeated - Audio: %s' % 'Spk-')
    #--
    elif button is BtnXSpkPlus and state == 'Pressed':
        print('Button Pressed - Audio: %s' % 'Spk+')
    elif button is BtnXSpkPlus and state == 'Repeated':
        print('Button Repeated - Audio: %s' % 'Spk+')
    #--
    elif button is BtnXVCLess and state == 'Pressed':
        print('Button Pressed - Audio: %s' % 'VC-')
    elif button is BtnXVCLess and state == 'Repeated':
        print('Button Repeated - Audio: %s' % 'VC-')
    #--
    elif button is BtnXVCPlus and state == 'Pressed':
        print('Button Pressed - Audio: %s' % 'VC+')
    elif button is BtnXVCPlus and state == 'Repeated':
        print('Button Repeated - Audio: %s' % 'VC+')
    pass
    
@event(PageAudio3, ButtonEventList)
def AudioMuteEvents(button, state):
    if button is BtnXSpk and state == 'Pressed':
        print('Button Pressed - Audio: %s' % 'Mute Spk')
    elif button is BtnXVC and state == 'Pressed':
        print('Button Pressed - Audio: %s' % 'Mute VC')
    elif button is BtnXMics and state == 'Pressed':
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

