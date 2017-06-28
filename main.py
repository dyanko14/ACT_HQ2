## -------------------------------------------------------------------------- ##
## Business   | Asesores y Consultores en Tecnología S.A. de C.V. ----------- ##
## Programmer | Dyanko Cisneros Mendoza
## Customer   | Human Quality
## Project    | Meeting Room
## Version    | 0.1 --------------------------------------------------------- ##

## CONTROL SCRIPT IMPORT -------------------------------------------------------
from extronlib import event, Version
from extronlib.device import eBUSDevice, ProcessorDevice, UIDevice
from extronlib.interface import (ContactInterface, DigitalIOInterface,
    EthernetClientInterface, EthernetServerInterfaceEx, FlexIOInterface,
    IRInterface, RelayInterface, SerialInterface, SWPowerInterface,
    VolumeInterface)
from extronlib.ui import Button, Knob, Label, Level
from extronlib.system import Clock, MESet, Wait

print(Version())
from gui import TLP, Btn, Btn_Page, Btn_Group, Btn_State, Lbl, Lvl, Popup, Page


## PROCESOR DEFINITION ---------------------------------------------------------
IPCP = ProcessorDevice('IPlink')

## MODULE IMPORT ---------------------------------------------------------------
## Ethernet:
import extr_matrix_DXPHD4k_Series_v1_1_1_0            as DeviceA
import extr_other_MediaPort200_v1_1_0_0               as DeviceB
import csco_vtc_SX_Series_TC73_v1_3_0_0               as DeviceC
import biam_dsp_TesiraSeries_v1_5_20_0                as DeviceD
## RS-232:
import smfy_controller_RS485_RTS_Transmitter_v1_0_0_0 as DeviceE

## Ethernet:
Matrix = DeviceA.EthernetClass('10.10.10.10', 23, Model='DXP 88 HD 4k')
Bridge = DeviceB.EthernetClass('10.10.10.11', 23, Model='MediaPort 200')
Cisco  = DeviceC.EthernetClass('10.10.10.12', 23, Model='SX20 TC7.3.X')
Biamp  = DeviceD.EthernetClass('192.168.10.150', 23, Model='TesiraFORTE CI')
## RS-232:
Somfy  = DeviceE.SerialClass(IPCP, 'COM1', Baud=9600, Model='RS485 RTS Transmitter')

## INITIALIZATE ----------------------------------------------------------------
## This is the last function that loads when starting the system
def Initialize():
    ## Opening a new Connection Thread to all devices
    Matrix.Connect()
    Bridge.Connect()
    Cisco.Connect()
    Biamp.Connect()

    ## Power Page Counter Variable
    global intPwrCount
    intPwrCount = 4 #Color Pwr Button Feedback 4=Too Much Red Button, 3=Red, 2=Slow Red, 1=Gray
    
    ## Subscribe Functions
    SubscribeBiamp()

    ## Update Functions
    UpdateBiamp()

    ## Recursive Functions
    UpdateLoop()

    ## Initialization of data and variables-----------
    ## Initialization in Cisco Camera Page
    Cisco_Data['PresetMode'] = 'Recall'
    Cisco_Data['Camera'] = 'Local'
    Btn_Group['VCPTZ'].SetCurrent(Btn['VCRecall'])
    Btn_Group['VCCam'].SetCurrent(Btn['VCLocal'])
    
    ## Initialization in Cisco Dial Page
    global dialerVC           ## To access the Dial String variable in all program
    dialerVC = ''             ## Clean the Dial String Variable
    Cisco_Data['Dial'] = ''   ## Clean the Dial Data in Dictionary
    Lbl['VCDial'].SetText('') ## Clean the Dial Data in GUI
    
    ## Initialization in VoIP Dial Page
    global dialerVI           ## To access the Dial String variable in all program
    dialerVI = ''             ## Clean the Dial String Variable
    Voip_Data['Dial'] = ''    ## Clean the Dial Data in Dictionary
    Lbl['Dial'].SetText('')   ## Clean the Dial Data in gui
   
    ## TouchPanel Functions
    TLP.HideAllPopups()
    TLP.ShowPage(Page['Index'])
    Btn_Group['Main'].SetCurrent(None) ##Turn Off all feedback button in GUI Main Page
    Lbl['CountAll'].SetText('')
    
    ## Notify to Console
    print('System Inicializate')
    pass

## SUBSCRIBE FUNCTIONS ---------------------------------------------------------
def SubscribeBiamp():
    Biamp.SubscribeStatus('ConnectionStatus',None, Biamp_Parsing)
    Biamp.SubscribeStatus('MuteControl',{'Instance Tag':'lvl_spk','Channel':'1'},Biamp_Parsing)
    Biamp.SubscribeStatus('MuteControl',{'Instance Tag':'lvl_vcrx','Channel':'1'},Biamp_Parsing)
    Biamp.SubscribeStatus('MuteControl',{'Instance Tag':'mute_mix','Channel':'1'},Biamp_Parsing)
    Biamp.SubscribeStatus('LevelControl',{'Instance Tag':'lvl_spk','Channel':'1'},Biamp_Parsing)
    pass

## UPDATE FUNCTIONS ------------------------------------------------------------
def UpdateBiamp():
    Biamp.Update('MuteControl',{'Instance Tag':'lvl_spk','Channel':'1'})
    Biamp.Update('MuteControl',{'Instance Tag':'lvl_vcrx','Channel':'1'})
    Biamp.Update('MuteControl',{'Instance Tag':'mute_mix','Channel':'1'})
    Biamp.Update('LevelControl',{'Instance Tag':'lvl_spk','Channel':'1'})
    pass

## DATA PARSING FUNCTIONS ------------------------------------------------------
## These functions receive the data of the devices in real time
## Each function stores the parsed data in dictionaries and activate feedback
## Each function works with the subscription methods of the Python modules
# Please declare Matrix Data Function below

# Please declare AV Bridge Data Function below
'''def Cisco_Parsing(command,value,qualifier):
    ##
    if command == 'CallStatus':
        Cisco_Data['Call'] = value
    ##
    elif command == 'PresentationMode':
        Cisco_Data['Content'] = value
    ##
    elif command == 'AutoAnswer':
        if value == 'On':
            Cisco_Data['AutoAnswer'] = 'On'
            BtnVCAutoAn.SetState(1)
        elif value == 'Off':
            Cisco_Data['AutoAnswer'] = 'Off'
            BtnVCAutoAn.SetState(0)
    pass'''

def Biamp_Parsing(command,value,qualifier):
    ##
    if command == 'ConnectionStatus':
        print('Biamp Module connection status {}'.format(value))

        if value == 'Connected':
            Biamp_Data['ConexModule'] = True
            Btn['LANBiamp'].SetState(1)
        
        elif value == 'Disconnected':
            Biamp_Data['ConexModule'] = False
            Btn['LANBiamp'].SetState(0)
    ##
    elif command == 'MuteControl':
        print(str(qualifier) + ' ' + str(value))

        if qualifier['Instance Tag'] == 'lvl_spk':
            if value == 'On':
                Biamp_Data['Mute_Spk'] = 'On'
                Btn['XSpk'].SetState(1)
            elif value == 'Off':
                Biamp_Data['Mute_Spk'] = 'Off'
                Btn['XSpk'].SetState(0)
        ##
        elif qualifier['Instance Tag'] == 'lvl_vcrx':
            if value == 'On':
                Biamp_Data['Mute_VCRx'] = 'On'
                Btn['XVC'].SetState(1)
            elif value == 'Off':
                Biamp_Data['Mute_VCRx'] = 'Off'
                Btn['XVC'].SetState(0)
        ##
        elif qualifier['Instance Tag'] == 'mute_mix':
            if value == 'On':
                Biamp_Data['Mute_Mics'] = 'On'
                Btn['XMics'].SetState(1)
            elif value == 'Off':
                Biamp_Data['Mute_Mics'] = 'Off'
                Btn['XMics'].SetState(0)
    ##
    elif command == 'LevelControl':
        Level(TLP, 195).SetLevel(int(value))
        print(str(qualifier) + ' ' + str(value))        
        Biamp_Data['Lvl_Spk'] = value
    pass

## RECURSIVE FUNCTIONS -----------------------------------------------------------
## This functions report a 'Online' / 'Offline' status after to send the Connect() Method
## CAUTION: If you never make a Connect(), the Extron Module never will work with Subscriptions
@event(Biamp, 'Connected')
@event(Biamp, 'Disconnected')
def BiampConnectionHandler(interface, state):
    print('Biamp Conex Event: ' + state)
    if state == 'Connected':
        Btn['LANBiamp'].SetState(1)
        Biamp_Data['ConexEvent'] = True
    if state == 'Disconnected':
        Btn['LANBiamp'].SetState(0)
        Biamp_Data['ConexEvent'] = False
        Trying()
    pass

## This functions try to make a Connect() 
## Help´s when the device was Off in the first Connect() method when the code starts
def Trying():
    if Biamp_Data['ConexEvent'] == False:
        print('Tryng to make a Connect() in Biamp')
        Biamp.Connect()
        LoopTrying.Restart()
    pass
LoopTrying = Wait(5, Trying) ## Invoke a validate function every 5s

def UpdateLoop():
    # This not affect any device
    # This return True / False when no response is received from Module
    # If in 5 times the data is not reported (connectionCounter = 5) from the Update Command
    # Generate 'Connected' / 'Disconnected'
    Biamp.Update('VerboseMode')
    loopUpdate.Restart()
loopUpdate = Wait(12, UpdateLoop) # Invoke a query function each 12s

## DATA DICTIONARIES -----------------------------------------------------------
## Each dictionary store the real time information of room devices
## Data dictionaries - IP Devices
Matrix_Data = {
    'Conex' : '',
    'Input' : '',
    'Output': '',
    'Type'  : '',
}

Bridge_Data = {
    'Conex' : '',
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
    'ConexModule': None,
    'ConexEvent' : None,
    'Mute_Spk'  : '',
    'Mute_VCRx' : '',
    'Mute_Mics' : '',
    'Lvl_Spk'   : None,
}

Voip_Data = {
    'Dial' : '',
    'DTMF' : False
}

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
## PAGE USER EVENTS ------------------------------------------------------------
## Page Index ------------------------------------------------------------------
@event(Btn['Index'],'Pressed')
def IndexEvents(button, state):
    TLP.ShowPage(Page['Main'])
    TLP.ShowPopup(Popup['Hi'])
    print('Touch Mode: %s' % 'Index')
    pass

## Page Main -------------------------------------------------------------------
@event(Btn_Page['Main'], Btn_State['List'])
def MainEvents(button, state):

    if button is Btn['Video'] and state == 'Pressed':
        TLP.ShowPopup(Popup['Video'])
        Lbl['Master'].SetText('Seleccionar Display')
        print('Touch Mode: %s' % 'Video')

    elif button is Btn['VC'] and state == 'Pressed':
        TLP.ShowPopup(Popup['VC'])
        Lbl['Master'].SetText('Control de Videoconferencia')
        print('Touch Mode: %s' % 'VC')

    elif button is Btn['Webex'] and state == 'Pressed':
        TLP.ShowPopup(Popup['Webex'])
        Lbl['Master'].SetText('Control de Webconferencia')
        print('Touch Mode: %s' % 'Webex')

    elif button is Btn['Rec'] and state == 'Pressed':
        Lbl['Master'].SetText('Control de Grabación')
        print('Touch Mode: %s' % 'Recording')

    elif button is Btn['VoIP'] and state == 'Pressed':
        TLP.ShowPopup(Popup['VoIP'])
        Lbl['Master'].SetText('Telefonía IP')
        print('Touch Mode: %s' % 'VoIP')

    elif button is Btn['Audio'] and state == 'Pressed':
        ## Query Data from Biamp
        UpdateBiamp()
        TLP.ShowPopup(Popup['Audio'])
        Lbl['Master'].SetText('Control de Audio')
        print('Touch Mode: %s' % 'Audio')

    elif button is Btn['Status'] and state == 'Pressed':
        TLP.ShowPopup(Popup['Status'])
        Lbl['Master'].SetText('Información de Dispositivos')
        print('Touch Mode: %s' % 'Status')

    elif button is Btn['PwrOff'] and state == 'Pressed':
        TLP.ShowPopup(Popup['Power'])
        Lbl['Master'].SetText('¿Deseas Apagar el Sistema?')
        print('Touch Mode: %s' % 'PowerOff')

    ##Turn On the feedbak of last pressed button
    Btn_Group['Main'].SetCurrent(button)
    pass

## Page Video ------------------------------------------------------------------
@event(Btn_Page['Video'], Btn_State['List'])
def VideoEvents(button, state):
    
    if button is Btn['DisplayL'] and state == 'Pressed':
        TLP.ShowPopup(Popup['LCD1'])
        Lbl['Master'].SetText('Control de Pantalla Izquierda')
        print('Video Mode: %s' % 'Display L')
    
    elif button is Btn['DisplayR'] and state == 'Pressed':
        TLP.ShowPopup(Popup['LCD2'])
        Lbl['Master'].SetText('Control de Pantalla Derecha')
        print('Video Mode: %s' % 'Display R')
    pass

## Page Display L --------------------------------------------------------------
@event(Btn_Page['LCD1'], Btn_State['List'])
def DisplayLEvents(button, state):
    if button is Btn['LHDMI'] and state == 'Pressed':
        ## HDMI to Display Left - Video
        Matrix.Set('MatrixTieCommand', None,{'Input':'1','Output':'1','Tie Type':'Video'})
        print('Button Pressed - LCD L: %s' % 'HDMI')
    
    elif button is Btn['LVGA'] and state == 'Pressed':
        ## VGA to Display Left - Video
        Matrix.Set('MatrixTieCommand', None, {'Input':'2','Output':'1','Tie Type':'Video'})
        print('Button Pressed - LCD L: %s' % 'VGA')
    
    elif button is Btn['LPTZ'] and state == 'Pressed':
        ## PTZ to Display Left - Video
        Matrix.Set('MatrixTieCommand', None, {'Input':'3','Output':'1','Tie Type':'Video'})
        print('Button Pressed - LCD L: %s' % 'PTZ')
    
    elif button is Btn['LShare'] and state == 'Pressed':
        ## ShareLink to Display Left - Video
        Matrix.Set('MatrixTieCommand', None, {'Input':'4','Output':'1','Tie Type':'Video'})
        print('Button Pressed - LCD L: %s' % 'ShareLink')
    
    elif button is Btn['LPwrOn'] and state == 'Pressed':
        ## The system send the command action directly
        print('Button Pressed - LCD L: %s' % 'PowerOn')
    
    elif button is Btn['LPwrOff'] and state == 'Pressed':
        ## The system send the command action directly
        print('Button Pressed - LCD L: %s' % 'PowerOff')
    
    elif button is Btn['LBack'] and state == 'Pressed':
        ## Hide actual popup and show the Display Selection Popup
        TLP.ShowPopup(Popup['Video'])
        print('Button Pressed - LCD L: %s' % 'Back')
    pass

## Page Display R --------------------------------------------------------------
@event(Btn_Page['LCD2'], Btn_State['List'])
def DisplayLEvents(button, state):
    if button is Btn['RHDMI'] and state == 'Pressed':
        ## HDMI to Display Right - Video
        Matrix.Set('MatrixTieCommand', None,{'Input':'1','Output':'2','Tie Type':'Video'})
        print('Button Pressed - LCD R: %s' % 'HDMI')
    
    elif button is Btn['RVGA'] and state == 'Pressed':
        ## VGA to Display Right - Video
        Matrix.Set('MatrixTieCommand', None, {'Input':'2','Output':'2','Tie Type':'Video'})
        print('Button Pressed - LCD R: %s' % 'VGA')
    
    elif button is Btn['RPTZ'] and state == 'Pressed':
        ## PTZ to Display Right - Video
        Matrix.Set('MatrixTieCommand', None, {'Input':'3','Output':'2','Tie Type':'Video'})
        print('Button Pressed - LCD R: %s' % 'PTZ')
    
    elif button is Btn['RShare'] and state == 'Pressed':
        ## ShareLink to Display Right - Video
        Matrix.Set('MatrixTieCommand', None, {'Input':'4','Output':'2','Tie Type':'Video'})
        print('Button Pressed - LCD R: %s' % 'ShareLink')
    
    elif button is Btn['RPwrOn'] and state == 'Pressed':
        ## The system send the command action directly
        print('Button Pressed - LCD R: %s' % 'PowerOn')
    
    elif button is Btn['RPwrOff'] and state == 'Pressed':
        ## The system send the command action directly
        print('Button Pressed - LCD R: %s' % 'PowerOff')
    
    elif button is Btn['RBack'] and state == 'Pressed':
        ## Hide actual popup and show the Display Selection Popup
        TLP.ShowPopup(Popup['Video'])
        print('Button Pressed - LCD R: %s' % 'Back')
    pass

## Page VC ---------------------------------------------------------------------
@event(Btn_Page['VCCall'], Btn_State['List'])
def VCCallEvents(button, state):
    
    if button is Btn['VCCall'] and state == 'Pressed':
        ##--This button dial the number typed on the touch panel (Cisco VC)
        Cisco.Set('Hook','Dial',{'Protocol':'H323','Number': Cisco_Data['Dial']})
        print('Button Pressed - VC: %s' % 'Call')
   
    elif button is Btn['VCHangup'] and state == 'Pressed':
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
        Lbl['VCDial'].SetText(dialerVC)  #Send the string to GUI Label
    #--
    else:                            #If the user push a [*#0-9] button
        Number = str(btn_name[4])    #Extract the valid character of btn name
        dialerVC += Number           #Append the last char to the string
        Cisco_Data['Dial'] = dialerVC #Asign the string to the data dictionary
        Lbl['VCDial'].SetText(dialerVC)  #Send the string to GUI Label
    pass

@event(Btn_Page['VCDial'], Btn_State['List'])
def VCDialEvents(button, state):
    ## All the VC Dial Buttons pressed come in button variable
    if state == 'Pressed' or state == 'Repeated':
        print('Button Pressed - VC: %s' % button.Name)
        DialerVC(button.Name) #Recall a validation function
        button.SetState(1)
    else:
        button.SetState(0)
    pass

@event(Btn_Page['VCOpt'], Btn_State['List'])
def VCOptEvents(button, state):
    
    ## VC Options: Content Control
    if button is Btn['VCEnviar'] and state == 'Pressed':
        TLP.ShowPopup(Popup['VC_PC'])
        Btn['VCEnviar'].SetState(1)
        print('Button Pressed - VC: %s' % 'Content')
    else:
        Btn['VCEnviar'].SetState(0)
    
    ## VC Options: Camera Control
    if button is Btn['VCCamara'] and state == 'Pressed':
        TLP.ShowPopup(Popup['VC_Cam'])
        Btn['VCCamara'].SetState(1)
        print('Button Pressed - VC: %s' % 'Camera')
    else:
        Btn['VCCamara'].SetState(0)
    
    ## VC Options: AutoAnswer
    if button is Btn['VCAutoAn'] and state == 'Pressed':
        if Cisco_Data['AutoAnswer'] == 'On':
            Cisco.Set('AutoAnswer','Off')
        elif Cisco_Data['AutoAnswer'] == 'Off':
            Cisco.Set('AutoAnswer','On')
        print('Button Pressed - VC: %s' % 'AutoAnswer')
    pass

## Page VC Content -------------------------------------------------------------
@event(Btn_Page['VCPC'], Btn_State['List'])
def VCCamEvents(button, state):
    
    if button is Btn['VCHDMI'] and state == 'Pressed':
        ## HDMI to Cisco Computer Input - Video
        Matrix.Set('MatrixTieCommand', None, {'Input':'1','Output':'3','Tie Type':'Video'})
        print('Button Pressed - VC Share: %s' % 'HDMI')
    
    elif button is Btn['VCVGA'] and state == 'Pressed':
        ## VGA to Cisco Computer Input - Video
        Matrix.Set('MatrixTieCommand', None, {'Input':'2','Output':'3','Tie Type':'Video'})
        print('Button Pressed - VC Share: %s' % 'VGA')
    
    elif button is Btn['VCPTZ'] and state == 'Pressed':
        ## PTZ to Cisco Computer Input - Video
        Matrix.Set('MatrixTieCommand', None, {'Input':'3','Output':'3','Tie Type':'Video'})
        print('Button Pressed - VC Share: %s' % 'PTZ')
    
    elif button is Btn['VCShare'] and state == 'Pressed':
        ## ShareLink to Cisco Computer Input - Video
        Matrix.Set('MatrixTieCommand', None, {'Input':'4','Output':'3','Tie Type':'Video'})
        print('Button Pressed - VC Share: %s' % 'ClickShare')
    
    elif button is Btn['VCBack2'] and state == 'Pressed':
        ## Hide VC Content Popup and Show the main VC Popup
        TLP.ShowPopup(Popup['VC'])
        print('Button Pressed - VC Share: %s' % 'Back')
    
    elif button is Btn['VCSend'] and state == 'Pressed':
        ## Play - Share graphics presentation
        Cisco.Set('Presentation','1')
        print('Button Pressed - VC Share: %s' % 'Send')
    
    elif button is Btn['VCStop'] and state == 'Pressed':
        ## Stop - Sharing graphics
        Cisco.Set('Presentation','Stop')
        print('Button Pressed - VC Share: %s' % 'Stop')
    pass

## Page VC Camera --------------------------------------------------------------
@event(Btn_Page['VCCam'], Btn_State['List'])
def VCNavEvents(button, state):
    #--
    if button is Btn['VCUp']:
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
    elif button is Btn['VCLeft']:
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
    elif button is Btn['VCDown']:
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
    elif button is Btn['VCRight']:
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
    elif button is Btn['VCZoom1']: #+
        if state == 'Pressed' or state == 'Repeated':
            if Cisco_Data['Camera'] == 'Local':
                Cisco.Set('CameraZoomSX20','In',{'Speed':7})
                print('Cam Local - Cisco: %s' % 'Cam Zoom+')
            elif Cisco_Data['Camera'] == 'Remote':
                Cisco.Set('FarEndCameraZoom','In')
                print('Cam Remota - Cisco: %s' % 'Cam Zoom+')
            Btn['VCZoom1'].SetState(1)
        #--
        elif state == 'Released':
            if Cisco_Data['Camera'] == 'Local':
                Cisco.Set('CameraZoomSX20','Stop',{'Speed':7})
                print('Cam Local - Cisco: %s' % 'Cam Stop')
            elif Cisco_Data['Camera'] == 'Remote':
                Cisco.Set('FarEndCameraZoom','Stop')
                print('Cam Remota - Cisco: %s' % 'Cam Stop')
            Btn['VCZoom1'].SetState(0)
    #--
    elif button is Btn['VCZoom2']: #-
        if state == 'Pressed' or state == 'Repeated':
            if Cisco_Data['Camera'] == 'Local':
                Cisco.Set('CameraZoomSX20','Out',{'Speed':7})
                print('Cam Local - Cisco: %s' % 'Cam Zoom-')
            elif Cisco_Data['Camera'] == 'Remote':
                Cisco.Set('FarEndCameraZoom','Out')
                print('Cam Remota - Cisco: %s' % 'Cam Zoom-')
            Btn['VCZoom2'].SetState(1)
        #--
        elif state == 'Released':
            if Cisco_Data['Camera'] == 'Local':
                Cisco.Set('CameraZoomSX20','Stop',{'Speed':7})
                print('Cam Local - Cisco: %s' % 'Cam Stop')
            elif Cisco_Data['Camera'] == 'Remote':
                Cisco.Set('FarEndCameraZoom','Stop')
                print('Cam Remota - Cisco: %s' % 'Cam Stop')
            Btn['VCZoom2'].SetState(0)
    #--
    if button is Btn['VCLocal'] and state == 'Pressed':
        Cisco_Data['Camera'] = 'Local'
        Btn_Group['VCCam'].SetCurrent(Btn['VCLocal'])
        print('Button Pressed - Cisco: %s' % 'Cam Local')
    #--
    elif button is Btn['VCRemote'] and state == 'Pressed':
        Cisco_Data['Camera'] = 'Remote'
        Btn_Group['VCCam'].SetCurrent(Btn['VCRemote'])
        print('Button Pressed - Cisco: %s' % 'Cam Remote')
    pass


@event(Btn_Page['VCPre'], Btn_State['List'])
def VCCamEvents(button, state):
    #--
    if button is Btn['VCP1'] and state == 'Pressed':
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
    elif button is Btn['VCP2'] and state == 'Pressed':
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
    elif button is Btn['VCP3'] and state == 'Pressed':
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
    elif button is Btn['VCP4'] and state == 'Pressed':
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
    elif button is Btn['VCP5'] and state == 'Pressed':
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
    elif button is Btn['VCRecall'] and state == 'Pressed':
        Cisco_Data['PresetMode'] = 'Recall'
        Btn_Group['VCPTZ'].SetCurrent(Btn['VCRecall'])
        print('Button Pressed - Cisco: %s' % 'Recall')
    #--
    elif button is Btn['VCSave'] and state == 'Pressed':
        Cisco_Data['PresetMode'] = 'Save'
        Btn_Group['VCPTZ'].SetCurrent(Btn['VCSave'])
        print('Button Pressed - Cisco: %s' % 'Save')
    pass

## Page Webex ------------------------------------------------------------------
@event(Btn_Page['Webex'], Btn_State['List'])
def WebexEvents(button, state):
    
    if button is Btn['WHDMI'] and state == 'Pressed':
        ## HDMI to MediaPort200 Input - Video
        Matrix.Set('MatrixTieCommand', None, {'Input':'1','Output':'5','Tie Type':'Video'})
        print('Button Pressed - Webex: %s' % 'HDMI')
    
    elif button is Btn['WVGA'] and state == 'Pressed':
        ## VGA to MediaPort200 Input - Video
        Matrix.Set('MatrixTieCommand', None, {'Input':'2','Output':'5','Tie Type':'Video'})
        print('Button Pressed - Webex: %s' % 'VGA')
    
    elif button is Btn['WPTZ'] and state == 'Pressed':
        ## PTZ to MediaPort200 Input - Video
        Matrix.Set('MatrixTieCommand', None, {'Input':'3','Output':'5','Tie Type':'Video'})
        print('Button Pressed - Webex: %s' % 'PTZ')
    
    elif button is Btn['WShare'] and state == 'Pressed':
        ## ShareLink to MediaPort200 Input - Video
        Matrix.Set('MatrixTieCommand', None, {'Input':'4','Output':'5','Tie Type':'Video'})
        print('Button Pressed - Webex: %s' % 'ShareLink')
    
    elif button is Btn['WCisco1'] and state == 'Pressed':
        ## Cisco 1 to MediaPort200 Input - Video
        Matrix.Set('MatrixTieCommand', None, {'Input':'5','Output':'5','Tie Type':'Video'})
        print('Button Pressed - Webex: %s' % 'Cisco 1')
    
    elif button is Btn['WCisco2'] and state == 'Pressed':
        ## Cisco 2 to MediaPort200 Input - Video
        Matrix.Set('MatrixTieCommand', None, {'Input':'6','Output':'5','Tie Type':'Video'})
        print('Button Pressed - Webex: %s' % 'Cisco 2')
    pass

## Page VoIP -------------------------------------------------------------------
@event(Btn_Page['TelCall'], Btn_State['List'])
def VICallEvents(button, state):
    if button is Btn['Call'] and state == 'Pressed':
        ##--This button dial the number typed on the touch panel (Biamp VoIP)
        Biamp.Set('VoIPHook','Dial',
                  {'Instance Tag':'Dialer','Line':'1','Call Appearance':'1',
                    'Number':Voip_Data['Dial']})
        print('Button Pressed - VoIP: %s' % 'Call')
    #--
    elif button is Btn['Hangup'] and state == 'Pressed':
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
        Lbl['Dial'].SetText(dialerVI)    #Send the string to GUI Label
    #--
    else:                                #If the user push a [*#0-9] button
        Number = str(btn_name[4])        #Extract the valid character of btn name
        if Voip_Data['DTMF'] == False:   #If the DTMF is off
            dialerVI += Number           #Append the last char to the string
            Voip_Data['Dial'] = dialerVI #Asign the string to the data dictionary
            Lbl['Dial'].SetText(dialerVI)    #Send the string to GUI Label
        elif Voip_Data['DTMF'] == True:  #If DTMF is On
            Biamp.Set('DTMF',Number,{'Instance Tag':'Dialer','Line':'1'})
    pass

@event(Btn_Page['TelDial'], Btn_State['List'])
def VIDialEvents(button, state):
    ## All the VoIP Dial Buttons pressed come in button variable
    if state == 'Pressed' or state == 'Repeated':
        print('Button Pressed - VoIP: %s' % button.Name)
        DialerVoIP(button.Name) #Recall a validation function
        button.SetState(1)
    else:
        button.SetState(0)
    pass

@event(Btn_Page['TelOpt'], Btn_State['List'])
def VIOptEvents(button, state):
    
    ## VoIP Redial Control
    if button is Btn['Redial'] and state == 'Pressed':
        Biamp.Set('VoIPHook','Redial',{'Instance Tag':'Dialer','Line':'1','Call Appearance':'1'})
        print('Button Pressed - VoIP: %s' % 'Redial')
    
    ## VoIP DTMF Control
    elif button is Btn['DTMF'] and state == 'Pressed':
        if Voip_Data['DTMF'] == False:
            Voip_Data['DTMF'] = True
            Btn['DTMF'].SetState(1)
            print('Button Pressed - VoIP: %s' % 'DTMF On')
        #--
        elif Voip_Data['DTMF'] == True:
            Voip_Data['DTMF'] = False
            Btn['DTMF'].SetState(0)
            print('Button Pressed - VoIP: %s' % 'DTMF Off')
        print('Button Pressed - VoIP: %s' % 'DTMF')
    
    ## Hold / Resume Control
    elif button is Btn['Hold'] and state == 'Pressed':
        print('Button Pressed - VoIP: %s' % 'Hold/Resume')
    pass

## Page Audio ------------------------------------------------------------------
@event(Btn_Page['Audio1'], Btn_State['List'])
def AudioSourceEvents(button, state):
    
    if button is Btn['XHDMI'] and state == 'Pressed':
        ## HDMI to HDMI Audio Dembedder Input - Audio
        Matrix.Set('MatrixTieCommand', None, {'Input':'1','Output':'1','Tie Type':'Audio'})
        print('Button Pressed - Audio: %s' % 'HDMI')
    
    elif button is Btn['XVGA'] and state == 'Pressed':
         ## VGA to HDMI Audio Dembedder Input - Audio
        Matrix.Set('MatrixTieCommand', None, {'Input':'2','Output':'1','Tie Type':'Audio'})
        print('Button Pressed - Audio: %s' % 'VGA')
    
    elif button is Btn['XShare'] and state == 'Pressed':
         ## ShareLink to HDMI Audio Dembedder Input - Audio
        Matrix.Set('MatrixTieCommand', None, {'Input':'4','Output':'1','Tie Type':'Audio'})
        print('Button Pressed - Audio: %s' % 'ShareLink')
    pass

@event(Btn_Page['Audio2'], Btn_State['List'])
def AudioVolEvents(button, state):
    ## Data of current Biamp Block Gain
    global currentlvl
    currentlvl = Biamp_Data['Lvl_Spk']

    ## Audio Speaker Control - Vol -
    if button is Btn['XSpkLess']:
        if state == 'Pressed' or state == 'Repeated':
            Btn['XSpkLess'].SetState(1)
        else:
            Btn['XSpkLess'].SetState(0)
        print('Button Pressed - Audio: %s' % 'Spk-')
    
    ## Audio Speaker Control - Vol +
    elif button is Btn['XSpkPlus']:
        if state == 'Pressed' or state == 'Repeated':
            Btn['XSpkPlus'].SetState(1)
        else:
            Btn['XSpkPlus'].SetState(0)
        print('Button Pressed - Audio: %s' % 'Spk+')
    
    ## Audio VC Remote Control - Vol -
    elif button is Btn['XVCLess'] and state == 'Pressed':
        print('Button Pressed - Audio: %s' % 'VC-')
    elif button is Btn['XVCLess'] and state == 'Repeated':
        print('Button Repeated - Audio: %s' % 'VC-')
    
    ## Audio VC Remote Control - Vol +
    elif button is Btn['XVCPlus'] and state == 'Pressed':
        print('Button Pressed - Audio: %s' % 'VC+')
    elif button is Btn['XVCPlus'] and state == 'Repeated':
        print('Button Repeated - Audio: %s' % 'VC+')
    pass

@event(Btn_Page['Audio3'], Btn_State['List'])
def AudioMuteEvents(button, state):
    
    ## Mute Speaker Audio Control
    if button is Btn['XSpk'] and state == 'Pressed':
        if Biamp_Data['Mute_Spk'] == 'On':
            Biamp.Set('MuteControl','Off',{'Instance Tag':'lvl_spk','Channel':'1'})
        elif Biamp_Data['Mute_Spk'] == 'Off':
            Biamp.Set('MuteControl','On',{'Instance Tag':'lvl_spk','Channel':'1'})
        print('Button Pressed - Audio: %s' % 'Mute Spk')
    
    ## Mute VC Remote Audio Control
    elif button is Btn['XVC'] and state == 'Pressed':
        if Biamp_Data['Mute_VCRx'] == 'On':
            Biamp.Set('MuteControl','Off',{'Instance Tag':'lvl_vcrx','Channel':'1'})
        elif Biamp_Data['Mute_VCRx'] == 'Off':
            Biamp.Set('MuteControl','On',{'Instance Tag':'lvl_vcrx','Channel':'1'})
        print('Button Pressed - Audio: %s' % 'Mute VC')
    
    ## Mute All Mics Audio Control
    elif button is Btn['XMics'] and state == 'Pressed':
        if Biamp_Data['Mute_Mics'] == 'On':
            Biamp.Set('MuteControl','Off',{'Instance Tag':'mute_mix','Channel':'1'})
        elif Biamp_Data['Mute_Mics'] == 'Off':
            Biamp.Set('MuteControl','On',{'Instance Tag':'mute_mix','Channel':'1'})
        print('Button Pressed - Audio: %s' % 'Mute Mics')
    pass

## Status Page -----------------------------------------------------------------

## Power Page ------------------------------------------------------------------
@event(Btn['PowerAll'], Btn_State['List'])
def PowerEvents(button, state):   
    global intintPwrCount
    ## If the user press the Power Button:
    ## Only Turn On the first state of button - Does not do any action
    if state == 'Pressed':
        Btn['PowerAll'].SetState(1)
        print('Button Pressed: %s' % 'PowerAll')
    ## If the user holds down the button:
    ## A variable is incremented up to 4 seconds
    ## In each new value, Turn On each visual state of the Power Button
    ## Whne the value is equal to 4, ShutDown all devices in the System
    elif state == 'Repeated':
        intintPwrCount = intintPwrCount - 1
        Btn['PowerAll'].SetState(intintPwrCount)
        Lbl['CountAll'].SetText(str(intintPwrCount))
        print('Button Repeated: %s' % 'PowerAll')
        ## Shutdown routine
        if intintPwrCount == 0:
            TLP.ShowPage(Page['Index'])
    ## If the user release the Button:
    ## Clean the counter power data in GUI and delete the visual feedback
    elif state == 'Released':
        intintPwrCount = 4
        Btn['PowerAll'].SetState(0)
        Lbl['CountAll'].SetText('')
        print('Button Released: %s' % 'PowerAll')
    pass

## End Events Definitions-------------------------------------------------------
Initialize()