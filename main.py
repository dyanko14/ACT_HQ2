"""--------------------------------------------------------------------------
 Business   | Asesores y Consultores en Tecnología S.A. de C.V.
 Programmer | Dyanko Cisneros Mendoza
 Customer   | Human Quality
 Project    | Meeting Room
 Version    | 0.1 --------------------------------------------------------- """

## CONTROL SCRIPT IMPORT -------------------------------------------------------
from gui import TLP, BTN, BTNPAGE, BTNGROUP, BTNSTATE, LBL, LVL, POPUP, PAGE
from extronlib import event, Version
from extronlib.device import eBUSDevice, ProcessorDevice, UIDevice
from extronlib.interface import (ContactInterface, DigitalIOInterface, \
    EthernetClientInterface, EthernetServerInterfaceEx, FlexIOInterface, \
    IRInterface, RelayInterface, SerialInterface, SWPowerInterface, \
    VolumeInterface)
from extronlib.ui import Button, Knob, Label, Level
from extronlib.system import Clock, MESet, Wait

## MODULE IMPORT ---------------------------------------------------------------
## IP:
import extr_matrix_DXPHD4k_Series_v1_1_1_0            as DeviceA
import extr_other_MediaPort200_v1_1_0_0               as DeviceB
import csco_vtc_SX_Series_TC73_v1_3_0_0               as DeviceC
import biam_dsp_TesiraSeries_v1_5_20_0                as DeviceD
import lutr_lc_CasetaWirelessSmartBridgePro_v1_0_2_0  as DeviceE
## RS-232:
import smfy_controller_RS485_RTS_Transmitter_v1_0_0_0 as DeviceF
## IR/Serial

print(Version())

## PROCESOR DEFINITION ---------------------------------------------------------
IPCP = ProcessorDevice('IPlink')

## IP:
MATRIX = DeviceA.EthernetClass('10.10.10.10', 23, Model='DXP 88 HD 4k')
BRIDGE = DeviceB.EthernetClass('10.10.10.11', 23, Model='MediaPort 200')
CISCO = DeviceC.EthernetClass('10.10.10.12', 23, Model='SX20 TC7.3.X')
BIAMP = DeviceD.EthernetClass('192.168.10.150', 23, Model='TesiraFORTE CI')
LUTRON = DeviceE.EthernetClass('192.168.10.15', 23, Model='Caseta Wireless Smart Bridge Pro')
## RS-232:
SOMFY = DeviceF.SerialClass(IPCP, 'COM1', Baud=9600, Model='RS485 RTS Transmitter')

## INITIALIZATE ----------------------------------------------------------------
def initialize():
    """This is the last function that loads when starting the system """
    ## OPEN CONNECTION SOCKETS
    ## IP
    MATRIX.Connect()
    BRIDGE.Connect()
    CISCO.Connect()
    BIAMP.Connect()
    LUTRON.Connect()
    ## RS-232
    SOMFY.Initialize()

    ## RECURSIVE FUNCTIONS
    update_loop_matrix()
    update_loop_bridge()
    update_loop_cisco()
    update_loop_biamp()

    ## POWER COUNTER VARIABLE
    global PWRCOUNT
    PWRCOUNT = 4 #Color Pwr Button Feedback 4=Too Much Red Button, 3=Red, 2=Slow Red, 1=Gray

    ## DATA INITIALIZE
    ## Cisco Camera PAGE
    CISCO_DATA['PresetMode'] = 'Recall'
    CISCO_DATA['Camera'] = 'Local'
    BTNGROUP['VCPTZ'].SetCurrent(BTN['VCRecall'])
    BTNGROUP['VCCam'].SetCurrent(BTN['VCLocal'])

    ## Cisco Dial PAGE
    global dialerVC           ## To access the Dial String variable in all program
    dialerVC = ''             ## Clean the Dial String Variable
    CISCO_DATA['Dial'] = ''   ## Clean the Dial Data in Dictionary
    LBL['VCDial'].SetText('') ## Clean the Dial Data in GUI

    ## VoIP Dial PAGE
    global dialerVI           ## To access the Dial String variable in all program
    dialerVI = ''             ## Clean the Dial String Variable
    VOIP_DATA['Dial'] = ''    ## Clean the Dial Data in Dictionary
    LBL['Dial'].SetText('')   ## Clean the Dial Data in gui

    ## TOUCH PANEL FUNCTIONS
    TLP.HideAllPopups()
    TLP.ShowPage(PAGE['Index'])
    BTNGROUP['Main'].SetCurrent(None) ##Turn Off all feedback button in GUI Main PAGE
    LBL['CountAll'].SetText('')

    ## NOTIFY TO CONSOLE
    print('System Inicializate')
    pass

## SUBSCRIBE FUNCTIONS ---------------------------------------------------------
def subscribe_matrix():
    """This send Subscribe Commands to Device """
    MATRIX.SubscribeStatus('ConnectionStatus', None, matrix_parsing)
    MATRIX.SubscribeStatus('OutputTieStatus', {'Output':'1', 'Tie Type':'Video'}, matrix_parsing)
    MATRIX.SubscribeStatus('OutputTieStatus', {'Output':'2', 'Tie Type':'Video'}, matrix_parsing)
    MATRIX.SubscribeStatus('OutputTieStatus', {'Output':'3', 'Tie Type':'Video'}, matrix_parsing)
    MATRIX.SubscribeStatus('OutputTieStatus', {'Output':'4', 'Tie Type':'Video'}, matrix_parsing)
    MATRIX.SubscribeStatus('OutputTieStatus', {'Output':'1', 'Tie Type':'Audio'}, matrix_parsing)
    MATRIX.SubscribeStatus('SignalStatus', {'Input' : '1'}, matrix_parsing)
    MATRIX.SubscribeStatus('SignalStatus', {'Input' : '2'}, matrix_parsing)
    MATRIX.SubscribeStatus('SignalStatus', {'Input' : '3'}, matrix_parsing)
    MATRIX.SubscribeStatus('SignalStatus', {'Input' : '4'}, matrix_parsing)
    MATRIX.SubscribeStatus('SignalStatus', {'Input' : '5'}, matrix_parsing)
    MATRIX.SubscribeStatus('SignalStatus', {'Input' : '6'}, matrix_parsing)
    pass

def subscribe_bridge():
    """This send Subscribe Commands to Device """
    BRIDGE.SubscribeStatus('ConnectionStatus', None, bridge_parsing)
    BRIDGE.SubscribeStatus('HDMIInputEDID', None, bridge_parsing)
    BRIDGE.SubscribeStatus('USBHostStatus', None, bridge_parsing)
    BRIDGE.SubscribeStatus('USBTerminalType', None, bridge_parsing)
    BRIDGE.SubscribeStatus('VideoSendStatus', None, bridge_parsing)
    BRIDGE.SubscribeStatus('VideoSignalPresence', None, bridge_parsing)
    pass

def subscribe_cisco():
    """This send Subscribe Commands to Device """
    CISCO.SubscribeStatus('ConnectionStatus', None, cisco_parsing)
    CISCO.SubscribeStatus('CallStatus', {'Call':'1'}, cisco_parsing)
    CISCO.SubscribeStatus('PresentationMode', None, cisco_parsing)
    CISCO.SubscribeStatus('Standby', None, cisco_parsing)
    CISCO.SubscribeStatus('AutoAnswer', None, cisco_parsing)
    CISCO.SubscribeStatus('Volume', None, cisco_parsing)
    pass

def subscribe_biamp():
    """This send Subscribe Commands to Device """
    BIAMP.SubscribeStatus('ConnectionStatus', None, biamp_parsing)
    BIAMP.SubscribeStatus('MuteControl', {'Instance Tag':'lvl_spk', 'Channel':'1'}, biamp_parsing)
    BIAMP.SubscribeStatus('MuteControl', {'Instance Tag':'lvl_vcrx', 'Channel':'1'}, biamp_parsing)
    BIAMP.SubscribeStatus('MuteControl', {'Instance Tag':'mute_mix', 'Channel':'1'}, biamp_parsing)
    BIAMP.SubscribeStatus('LevelControl', {'Instance Tag':'lvl_spk', 'Channel':'1'}, biamp_parsing)
    pass

def subscribe_lutron():
    """This send Subscribe Commands to Device """
    LUTRON.SubscribeStatus('ConnectionStatus', None, lutron_parsing)
    pass

def subscribe_somfy():
    """This send Subscribe Commands to Device """
    SOMFY.SubscribeStatus('ConnectionStatus', None, somfy_parsing)
    pass

## UPDATE FUNCTIONS ------------------------------------------------------------
def update_matrix():
    """This send Update Commands to Device"""
    MATRIX.Update('OutputTieStatus', {'Output':'1', 'Tie Type':'Video'})
    MATRIX.Update('OutputTieStatus', {'Output':'2', 'Tie Type':'Video'})
    MATRIX.Update('OutputTieStatus', {'Output':'3', 'Tie Type':'Video'})
    MATRIX.Update('OutputTieStatus', {'Output':'4', 'Tie Type':'Video'})
    MATRIX.Update('OutputTieStatus', {'Output':'1', 'Tie Type':'Audio'})
    MATRIX.Update('SignalStatus', {'Input' : '1'})
    MATRIX.Update('SignalStatus', {'Input' : '2'})
    MATRIX.Update('SignalStatus', {'Input' : '3'})
    MATRIX.Update('SignalStatus', {'Input' : '4'})
    MATRIX.Update('SignalStatus', {'Input' : '5'})
    MATRIX.Update('SignalStatus', {'Input' : '6'})
    pass

def update_bridge():
    """This send Update Commands to Device"""
    BRIDGE.Update('ConnectionStatus')
    BRIDGE.Update('HDMIInputEDID')
    BRIDGE.Update('USBHostStatus')
    BRIDGE.Update('USBTerminalType')
    BRIDGE.Update('VideoSendStatus')
    BRIDGE.Update('VideoSignalPresence')
    pass

def update_cisco():
    """This send Update Commands to Device"""
    CISCO.Update('CallStatus', {'Call':'1'})
    CISCO.Update('PresentationMode')
    CISCO.Update('Standby')
    CISCO.Update('AutoAnswer')
    CISCO.Update('Volume')
    pass

def update_biamp():
    """This send Update Commands to Device"""
    BIAMP.Update('MuteControl', {'Instance Tag':'lvl_spk', 'Channel':'1'})
    BIAMP.Update('MuteControl', {'Instance Tag':'lvl_vcrx', 'Channel':'1'})
    BIAMP.Update('MuteControl', {'Instance Tag':'mute_mix', 'Channel':'1'})
    BIAMP.Update('LevelControl', {'Instance Tag':'lvl_spk', 'Channel':'1'})
    pass

def update_lutron():
    """This send Update Commands to Device"""
    LUTRON.Update('OutputLevel', {'Integration ID':'2'})
    pass

## DATA PARSING FUNCTIONS ------------------------------------------------------
## These functions receive the data of the devices in real time
## Each function stores the parsed data in dictionaries and activate feedback
## Each function works with the subscription methods of the Python modules
def matrix_parsing(command, value, qualifier):
    """Retrieve the Real Information of the Device """
    if command == 'ConnectionStatus':
        print('Matrix Module Conex status: {}'.format(value))

        if value == 'Connected':
            MATRIX_DATA['ConexModule'] = True
            BTN['LANMatrix'].SetState(1)
        else:
            MATRIX_DATA['ConexModule'] = False
            BTN['LANMatrix'].SetState(0)
            ## Disconnect the IP Socket
            MATRIX.Disconnect()

    elif command == 'OutputTieStatus':
        if qualifier['Output'] == '1': ## Left Display
            if qualifier['Tie Type'] == 'Video':
                if value == '1':
                    BTNGROUP['LCD1_S'].SetCurrent(BTN['LHDMI'])
                elif value == '2':
                    BTNGROUP['LCD1_S'].SetCurrent(BTN['LVGA'])
                elif value == '3':
                    BTNGROUP['LCD1_S'].SetCurrent(BTN['LPTZ'])
                elif value == '4':
                    BTNGROUP['LCD1_S'].SetCurrent(BTN['LShare'])

        elif qualifier['Output'] == '2': ## Right Display
            if qualifier['Tie Type'] == 'Video':
                if value == '1':
                    BTNGROUP['LCD2_S'].SetCurrent(BTN['RHDMI'])
                elif value == '2':
                    BTNGROUP['LCD2_S'].SetCurrent(BTN['RVGA'])
                elif value == '3':
                    BTNGROUP['LCD2_S'].SetCurrent(BTN['RPTZ'])
                elif value == '4':
                    BTNGROUP['LCD2_S'].SetCurrent(BTN['RShare'])

        elif qualifier['Output'] == '3': ## VC Content Input
            if qualifier['Tie Type'] == 'Video':
                if value == '1':
                    BTNGROUP['VCPC_S'].SetCurrent(BTN['VCHDMI'])
                elif value == '2':
                    BTNGROUP['VCPC_S'].SetCurrent(BTN['VCVGA'])
                elif value == '3':
                    BTNGROUP['VCPC_S'].SetCurrent(BTN['VCPTZ'])
                elif value == '4':
                    BTNGROUP['VCPC_S'].SetCurrent(BTN['VCShare'])

        elif qualifier['Output'] == '4': ## Webex Input
            if qualifier['Tie Type'] == 'Video':
                if value == '1':
                    BTNGROUP['Webex'].SetCurrent(BTN['WHDMI'])
                elif value == '2':
                    BTNGROUP['Webex'].SetCurrent(BTN['WVGA'])
                elif value == '3':
                    BTNGROUP['Webex'].SetCurrent(BTN['WPTZ'])
                elif value == '4':
                    BTNGROUP['Webex'].SetCurrent(BTN['WShare'])
                elif value == '5':
                    BTNGROUP['Webex'].SetCurrent(BTN['WCisco1'])
                elif value == '6':
                    BTNGROUP['Webex'].SetCurrent(BTN['WCisco2'])

        elif qualifier['Output'] == '1': ## Audio HDMI Matrix Dembedder
            if qualifier['Tie Type'] == 'Audio':
                if value == '1':
                    BTNGROUP['Audio'].SetCurrent(BTN['XHDMI'])
                elif value == '2':
                    BTNGROUP['Audio'].SetCurrent(BTN['XVGA'])
                elif value == '4':
                    BTNGROUP['Audio'].SetCurrent(BTN['XShare'])

    elif command == 'SignalStatus':
        if qualifier['Input'] == '1':
            if value == 'Signal Detected':
                BTN['Signal1'].SetState(1)
            else:
                BTN['Signal1'].SetState(0)
        elif qualifier['Input'] == '2':
            if value == 'Signal Detected':
                BTN['Signal2'].SetState(1)
            else:
                BTN['Signal2'].SetState(0)
        elif qualifier['Input'] == '3':
            if value == 'Signal Detected':
                BTN['Signal3'].SetState(1)
            else:
                BTN['Signal3'].SetState(0)
        elif qualifier['Input'] == '4':
            if value == 'Signal Detected':
                BTN['Signal4'].SetState(1)
            else:
                BTN['Signal4'].SetState(0)
        elif qualifier['Input'] == '5':
            if value == 'Signal Detected':
                BTN['Signal5'].SetState(1)
            else:
                BTN['Signal5'].SetState(0)
        elif qualifier['Input'] == '6':
            if value == 'Signal Detected':
                BTN['Signal6'].SetState(1)
            else:
                BTN['Signal6'].SetState(0)
    pass

def bridge_parsing(command, value, qualifier):
    """Retrieve the Real Information of the Device """
    if command == 'ConnectionStatus':
        print('Bridge Module Conex status: {}'.format(value))

        if value == 'Connected':
            BRIDGE_DATA['ConexModule'] = True
            BTN['LanBridge'].SetState(1)
        else:
            BRIDGE_DATA['ConexModule'] = False
            BTN['LanBridge'].SetState(0)
            ## Disconnect the IP Socket
            BRIDGE.Disconnect()

    elif command == 'HDMIInputEDID':
        print(value)
        BRIDGE_DATA['InputEDID'] = value

    elif command == 'USBHostStatus':
        print(value)
        BRIDGE_DATA['USBHost'] = value

    elif command == 'USBTerminalType':
        print(value)
        BRIDGE_DATA['USBTerminal'] = value

    elif command == 'VideoSendStatus':
        print(value)
        if value == 'On':
            BRIDGE_DATA['VideoSend'] = True
        else:
            BRIDGE_DATA['VideoSend'] = False

    elif command == 'VideoSignalPresence':
        print(value)
        if value == 'Signal':
            BRIDGE_DATA['VideoSignal'] = True
        else:
            BRIDGE_DATA['VideoSignal'] = False
    pass

def cisco_parsing(command, value, qualifier):
    """Retrieve the Real Information of the Device """
    if command == 'ConnectionStatus':
        print('Cisco Module Conex status: {}'.format(value))

        if value == 'Connected':
            CISCO_DATA['ConexModule'] = True
            BTN['LANCisco'].SetState(1)
        else:
            CISCO_DATA['ConexModule'] = False
            BTN['LANCisco'].SetState(0)
            ## Disconnect the IP Socket
            CISCO.Disconnect()

    elif command == 'CallStatus':
        print(qualifier + value)
        CISCO_DATA['Call'] = value

    elif command == 'PresentationMode':
        print(value)
        CISCO_DATA['Content'] = value

    elif command == 'Standby':
        print(value)
        if value == 'Activate':
            CISCO_DATA['Power'] = True
        else:
            CISCO_DATA['Power'] = False

    elif command == 'AutoAnswer':
        if value == 'On':
            CISCO_DATA['AutoAnswer'] = True
            BTN['VCAutoAn'].SetState(1)
        elif value == 'Off':
            CISCO_DATA['AutoAnswer'] = False
            BTN['VCAutoAn'].SetState(0)

    elif command == 'Volume':
        print(value)
        LVL['VC'].SetLevel(value)    ## Send volume value to Level Bar
        CISCO_DATA['Volume'] = value ## Store volume value in dictionary
    pass

def biamp_parsing(command, value, qualifier):
    """Retrieve the Real Information of the Device """
    if command == 'ConnectionStatus':
        print('Biamp Module Conex status: {}'.format(value))

        if value == 'Connected':
            BIAMP_DATA['ConexModule'] = True
            BTN['LANBiamp'].SetState(1)
        else:
            BIAMP_DATA['ConexModule'] = False
            BTN['LANBiamp'].SetState(0)
            ## Turn Off feedback Buttons
            LVL['Spk'].SetLevel(-100)
            ## Disconnect the IP Socket
            BIAMP.Disconnect()

    elif command == 'MuteControl':
        print(str(qualifier) + ' ' + str(value))

        if qualifier['Instance Tag'] == 'lvl_spk':
            if value == 'On':
                BIAMP_DATA['MuteSpk'] = True
                BTN['XSpk'].SetState(1)
            elif value == 'Off':
                BIAMP_DATA['MuteSpk'] = False
                BTN['XSpk'].SetState(0)

        elif qualifier['Instance Tag'] == 'lvl_vcrx':
            if value == 'On':
                BIAMP_DATA['MuteVCRx'] = True
                BTN['XVC'].SetState(1)
            elif value == 'Off':
                BIAMP_DATA['MuteVCRx'] = False
                BTN['XVC'].SetState(0)

        elif qualifier['Instance Tag'] == 'mute_mix':
            if value == 'On':
                BIAMP_DATA['Mute_Mics'] = True
                BTN['XMics'].SetState(1)
            elif value == 'Off':
                BIAMP_DATA['Mute_Mics'] = False
                BTN['XMics'].SetState(0)

    elif command == 'LevelControl':
        print(str(qualifier) + ' ' + str(value))
        value = int(value)            ## Convert reported volume to Integer
        LVL['Spk'].SetLevel(value)    ## Send volume value to Level Bar
        BIAMP_DATA['lvl_spk'] = value ## Store volume value in dictionary
    pass

def lutron_parsing(command, value, qualifier):
    """Retrieve the Real Information of the Device """
    if command == 'ConnectionStatus':
        print('Lutron Module Conex status: {}'.format(value))

        if value == 'Connected':
            LUTRON_DATA['ConexModule'] = True
            BTN['LANLutron'].SetState(1)
        else:
            LUTRON_DATA['ConexModule'] = False
            BTN['LANLutron'].SetState(0)
            ## Disconnect the IP Socket
            LUTRON.Disconnect()
    pass

def somfy_parsing(command, value, qualifier):
    """Retrieve the Real Information of the Device """
    if command == 'ConnectionStatus':
        print('Somfy Module Conex status: {}'.format(value))

        if value == 'Connected':
            SOMFY_DATA['ConexModule'] = True
            BTN['232Somfy'].SetState(1)
        else:
            SOMFY_DATA['ConexModule'] = False
            BTN['232Somfy'].SetState(0)

    pass
## EVENT FUNCTIONS ----------------------------------------------------------------
## This functions report a 'Online' / 'Offline' status after to send a Connect()
## CAUTION: If you never make a Connect(), the Module never work with Subscriptions
@event(MATRIX, 'Connected')
@event(MATRIX, 'Disconnected')
def matrix_conex_event(interface, state):
    """MATRIX CONNECT() STATUS """
    print('Matrix Conex Event: ' + state)
    if state == 'Connected':
        BTN['LANMatrix'].SetState(1)
        MATRIX_DATA['ConexEvent'] = True
        ## Send & Query Information
        subscribe_matrix()
        update_matrix()
    if state == 'Disconnected':
        BTN['LANMatrix'].SetState(0)
        MATRIX_DATA['ConexEvent'] = False
        trying_matrix()
    pass

@event(BRIDGE, 'Connected')
@event(BRIDGE, 'Disconnected')
def bridge_conex_event(interface, state):
    """BRIDGE CONNECT() STATUS """
    print('Bridge Conex Event: ' + state)
    if state == 'Connected':
        BTN['LanBridge'].SetState(1)
        BRIDGE_DATA['ConexEvent'] = True
        ## Send & Query Information
        subscribe_bridge()
        update_bridge()
    if state == 'Disconnected':
        BTN['LanBridge'].SetState(0)
        BRIDGE_DATA['ConexEvent'] = False
        trying_bridge()
    pass

@event(CISCO, 'Connected')
@event(CISCO, 'Disconnected')
def cisco_conex_event(interface, state):
    """CISCO CONNECT() STATUS """
    print('Cisco Conex Event: ' + state)
    if state == 'Connected':
        BTN['LANCisco'].SetState(1)
        CISCO_DATA['ConexEvent'] = True
        ## Send & Query Information
        subscribe_cisco()
        update_cisco()
    if state == 'Disconnected':
        BTN['LANCisco'].SetState(0)
        CISCO_DATA['ConexEvent'] = False
        trying_cisco()
    pass

@event(BIAMP, 'Connected')
@event(BIAMP, 'Disconnected')
def biamp_conex_event(interface, state):
    """DEVICE CONNECT() STATUS """
    print('Biamp Conex Event: ' + state)
    if state == 'Connected':
        BTN['LANBiamp'].SetState(1)
        BIAMP_DATA['ConexEvent'] = True
        ## Send & Query Information
        subscribe_biamp()
        update_biamp()
    if state == 'Disconnected':
        BTN['LANBiamp'].SetState(0)
        BIAMP_DATA['ConexEvent'] = False
        trying_biamp()
    pass

@event(LUTRON, 'Connected')
@event(LUTRON, 'Disconnected')
def lutron_conex_event(interface, state):
    """DEVICE CONNECT() STATUS """
    print('Lutron Conex Event: ' + state)
    if state == 'Connected':
        BTN['LANLutron'].SetState(1)
        LUTRON_DATA['ConexEvent'] = True
        ## Send & Query Information
        subscribe_lutron()
        update_lutron()
    if state == 'Disconnected':
        BTN['LANLutron'].SetState(0)
        LUTRON_DATA['ConexEvent'] = False
        trying_lutron()
    pass

## RECURSIVE FUNCTIONS ------------------------------------------------------------
## Help´s when the device was Off in the first Connect() method when the code starts
def trying_matrix():
    """Try to make a Connect() to device"""
    if MATRIX_DATA['ConexEvent'] == False:
        print('Tryng to make a Connect() in Matrix')
        MATRIX.Connect(4) ## Have 4 seconds to try to connect
    pass
loop_trying_matrix = Wait(5, trying_matrix)

def trying_bridge():
    """Try to make a Connect() to device"""
    if BRIDGE_DATA['ConexEvent'] == False:
        print('Tryng to make a Connect() in Bridge')
        BRIDGE.Connect(4) ## Have 4 seconds to try to connect
    pass
loop_trying_bridge = Wait(5, trying_bridge)

def trying_cisco():
    """Try to make a Connect() to device"""
    if CISCO_DATA['ConexEvent'] == False:
        print('Tryng to make a Connect() in Cisco')
        CISCO.Connect(4) ## Have 4 seconds to try to connect
    pass
loop_trying_cisco = Wait(5, trying_cisco)

def trying_biamp():
    """Try to make a Connect() to device"""
    if BIAMP_DATA['ConexEvent'] == False:
        print('Tryng to make a Connect() in Biamp')
        BIAMP.Connect(4) ## Have 4 seconds to try to connect
    pass
loop_trying_biamp = Wait(5, trying_biamp)

def trying_lutron():
    """Try to make a Connect() to device"""
    if LUTRON_DATA['ConexEvent'] == False:
        print('Tryng to make a Connect() in Lutron')
        LUTRON.Connect(4) ## Have 4 seconds to try to connect
    pass
loop_trying_lutron = Wait(5, trying_lutron)

## RECURSIVE LOOP FUNCTIONS -----------------------------------------------------------
## This not affect any device
## This return True / False when no response is received from Module
## If in 5 times the data is not reported (connectionCounter = 5) from the Update Command
## Generate 'Connected' / 'Disconnected'

def update_loop_matrix():
    """Continuos Update Commands to produce Module Connected / Disconnected"""
    MATRIX.Update('SignalStatus', {'Input':'1'})
    loop_update_matrix.Restart()
loop_update_matrix = Wait(12, update_loop_matrix)

def update_loop_bridge():
    """Continuos Update Commands to produce Module Connected / Disconnected"""
    BRIDGE.Update('AutoImage')
    loop_update_bridge.Restart()
loop_update_bridge = Wait(12, update_loop_bridge)

def update_loop_cisco():
    """Continuos Update Commands to produce Module Connected / Disconnected"""
    CISCO.Update('AutoAnswer')
    loop_update_cisco.Restart()
loop_update_cisco = Wait(12, update_loop_cisco)

def update_loop_biamp():
    """Continuos Update Commands to produce Module Connected / Disconnected"""
    BIAMP.Update('VerboseMode')
    loop_update_biamp.Restart()
loop_update_biamp = Wait(12, update_loop_biamp)

def update_loop_lutron():
    """Continuos Update Commands to produce Module Connected / Disconnected"""
    LUTRON.Update('OutputLevel', {'Integration ID':'2'})
    loop_update_lutron.Restart()
loop_update_lutron = Wait(12, update_loop_lutron)

## DATA DICTIONARIES -----------------------------------------------------------
## Each dictionary store the real time information of room devices
## IP
MATRIX_DATA = {
    'ConexModule': None,
    'ConexEvent' : None,
}

BRIDGE_DATA = {
    'ConexModule': None,
    'ConexEvent' : None,
    ##
    'InputEDID'  : '',
    'USBHost'    : '',
    'USBTerminal': '',
    'VideoSend'  : None,
    'VideoSignal': None,
}

CISCO_DATA = {
    'ConexModule': None,
    'ConexEvent' : None,
    ##
    'AutoAnswer' : None,
    'CallStatus' : '',
    'Camera'     : '',
    'Dial'       : '',
    'Power'      : None,
    'PresetMode' : '',
    'Volume'     : None,
}

BIAMP_DATA = {
    'ConexModule': None,
    'ConexEvent' : None,
    ##
    'MuteSpk'    : None,
    'MuteVCRx'   : None,
    'Mute_Mics'  : None,
    'lvl_spk'    : None,
}

VOIP_DATA = {
    'Dial' : '',
    'DTMF' : False
}

LUTRON_DATA = {
    'ConexModule': None,
    'ConexEvent' : None,
}

## RS-232
SOMFY_DATA = {
    'ConexModule': None,
    'ConexEvent' : None,
}

## IR-Serial
LCD1_DATA = {
    'Input' : '',
    'Power' : '',
}

LCD2_DATA = {
    'Input' : '',
    'Power' : '',
}
## PAGE USER EVENTS ------------------------------------------------------------
## PAGE Index ------------------------------------------------------------------
@event(BTN['Index'], 'Pressed')
def index_events(button, state):
    """User Actions: Touch Index Page"""
    TLP.ShowPage(PAGE['Main'])
    TLP.ShowPopup(POPUP['Hi'])
    print('Touch Mode: %s' % 'Index')
    pass

## PAGE Main -------------------------------------------------------------------
@event(BTNPAGE['Main'], BTNSTATE['List'])
def main_events(button, state):
    """User Actions: Touch Main Page"""
    if button is BTN['Video'] and state == 'Pressed':
        TLP.ShowPopup(POPUP['Video'])
        LBL['Master'].SetText('Seleccionar Display')
        print('Touch Mode: %s' % 'Video')

    elif button is BTN['VC'] and state == 'Pressed':
        TLP.ShowPopup(POPUP['VC'])
        LBL['Master'].SetText('Control de Videoconferencia')
        print('Touch Mode: %s' % 'VC')

    elif button is BTN['Webex'] and state == 'Pressed':
        TLP.ShowPopup(POPUP['Webex'])
        LBL['Master'].SetText('Control de Webconferencia')
        print('Touch Mode: %s' % 'Webex')

    elif button is BTN['VoIP'] and state == 'Pressed':
        TLP.ShowPopup(POPUP['VoIP'])
        LBL['Master'].SetText('Telefonía IP')
        print('Touch Mode: %s' % 'VoIP')

    elif button is BTN['Lights'] and state == 'Pressed':
        TLP.ShowPopup(POPUP['Lights'])
        LBL['Master'].SetText('Control de Iluminación')
        print('Touch Mode: %s' % 'Lights')

    elif button is BTN['Audio'] and state == 'Pressed':
        ## Query Data from Biamp
        update_biamp()
        TLP.ShowPopup(POPUP['Audio'])
        LBL['Master'].SetText('Control de Audio')
        print('Touch Mode: %s' % 'Audio')

    elif button is BTN['Status'] and state == 'Pressed':
        TLP.ShowPopup(POPUP['Status'])
        LBL['Master'].SetText('Información de Dispositivos')
        print('Touch Mode: %s' % 'Status')

    elif button is BTN['PwrOff'] and state == 'Pressed':
        TLP.ShowPopup(POPUP['Power'])
        LBL['Master'].SetText('¿Deseas Apagar el Sistema?')
        print('Touch Mode: %s' % 'PowerOff')

    ##Turn On the feedbak of last pressed button
    BTNGROUP['Main'].SetCurrent(button)
    pass

## PAGE Video ------------------------------------------------------------------
@event(BTNPAGE['Video'], BTNSTATE['List'])
def video_events(button, state):
    """User Actions: Touch Video Page"""
    if button is BTN['DisplayL'] and state == 'Pressed':
        TLP.ShowPopup(POPUP['LCD1'])
        LBL['Master'].SetText('Control de Pantalla Izquierda')
        print('Video Mode: %s' % 'Display L')

    elif button is BTN['DisplayR'] and state == 'Pressed':
        TLP.ShowPopup(POPUP['LCD2'])
        LBL['Master'].SetText('Control de Pantalla Derecha')
        print('Video Mode: %s' % 'Display R')
    pass

## PAGE Display L --------------------------------------------------------------
@event(BTNPAGE['LCD1'], BTNSTATE['List'])
def display_l_events(button, state):
    """User Actions: Touch LCD-L Page"""
    if button is BTN['LHDMI'] and state == 'Pressed':
        ## HDMI to Display Left - Video
        MATRIX.Set('MatrixTieCommand', None, {'Input':'1', 'Output':'1', 'Tie Type':'Video'})
        print('Button Pressed - LCD L: %s' % 'HDMI')

    elif button is BTN['LVGA'] and state == 'Pressed':
        ## VGA to Display Left - Video
        MATRIX.Set('MatrixTieCommand', None, {'Input':'2', 'Output':'1', 'Tie Type':'Video'})
        print('Button Pressed - LCD L: %s' % 'VGA')

    elif button is BTN['LPTZ'] and state == 'Pressed':
        ## PTZ to Display Left - Video
        MATRIX.Set('MatrixTieCommand', None, {'Input':'3', 'Output':'1', 'Tie Type':'Video'})
        print('Button Pressed - LCD L: %s' % 'PTZ')

    elif button is BTN['LShare'] and state == 'Pressed':
        ## ShareLink to Display Left - Video
        MATRIX.Set('MatrixTieCommand', None, {'Input':'4', 'Output':'1', 'Tie Type':'Video'})
        print('Button Pressed - LCD L: %s' % 'ShareLink')

    elif button is BTN['LPwrOn'] and state == 'Pressed':
        ## The system send the command action directly
        print('Button Pressed - LCD L: %s' % 'PowerOn')

    elif button is BTN['LPwrOff'] and state == 'Pressed':
        ## The system send the command action directly
        print('Button Pressed - LCD L: %s' % 'PowerOff')

    elif button is BTN['LBack'] and state == 'Pressed':
        ## Hide actual POPUP and show the Display Selection POPUP
        TLP.ShowPopup(POPUP['Video'])
        print('Button Pressed - LCD L: %s' % 'Back')
    pass

## PAGE Display R --------------------------------------------------------------
@event(BTNPAGE['LCD2'], BTNSTATE['List'])
def display_r_events(button, state):
    """User Actions: Touch LCD-R Page"""
    if button is BTN['RHDMI'] and state == 'Pressed':
        ## HDMI to Display Right - Video
        MATRIX.Set('MatrixTieCommand', None, {'Input':'1', 'Output':'2', 'Tie Type':'Video'})
        print('Button Pressed - LCD R: %s' % 'HDMI')

    elif button is BTN['RVGA'] and state == 'Pressed':
        ## VGA to Display Right - Video
        MATRIX.Set('MatrixTieCommand', None, {'Input':'2', 'Output':'2', 'Tie Type':'Video'})
        print('Button Pressed - LCD R: %s' % 'VGA')

    elif button is BTN['RPTZ'] and state == 'Pressed':
        ## PTZ to Display Right - Video
        MATRIX.Set('MatrixTieCommand', None, {'Input':'3', 'Output':'2', 'Tie Type':'Video'})
        print('Button Pressed - LCD R: %s' % 'PTZ')

    elif button is BTN['RShare'] and state == 'Pressed':
        ## ShareLink to Display Right - Video
        MATRIX.Set('MatrixTieCommand', None, {'Input':'4', 'Output':'2', 'Tie Type':'Video'})
        print('Button Pressed - LCD R: %s' % 'ShareLink')

    elif button is BTN['RPwrOn'] and state == 'Pressed':
        ## The system send the command action directly
        print('Button Pressed - LCD R: %s' % 'PowerOn')

    elif button is BTN['RPwrOff'] and state == 'Pressed':
        ## The system send the command action directly
        print('Button Pressed - LCD R: %s' % 'PowerOff')

    elif button is BTN['RBack'] and state == 'Pressed':
        ## Hide actual POPUP and show the Display Selection POPUP
        TLP.ShowPopup(POPUP['Video'])
        print('Button Pressed - LCD R: %s' % 'Back')
    pass

## PAGE VC ---------------------------------------------------------------------
@event(BTNPAGE['VCCall'], BTNSTATE['List'])
def vc_call_events(button, state):
    """User Actions: Touch VC Page"""
    if button is BTN['VCCall'] and state == 'Pressed':
        ##--This button dial the number typed on the touch panel (Cisco VC)
        CISCO.Set('Hook', 'Dial', {'Protocol':'H323', 'Number': CISCO_DATA['Dial']})
        print('Button Pressed - VC: %s' % 'Call')

    elif button is BTN['VCHangup'] and state == 'Pressed':
        ##--This button hangs up all active calls (Cisco VC)
        CISCO.Set('Hook', 'Disconnect All', {'Protocol':'H323'})
        print('Button Pressed - VC: %s' % 'Hangup')
    pass

## This function is called when the user press a Dial Button
## This function add or remove data from the panel Dial Number
def dialer_vc(btn_name):
    """User Actions: Touch VC Page"""
    global dialerVC

    if btn_name == 'Delete':         #If the user push 'Delete' button
        dialerVC = dialerVC[:-1]     #Remove the last char of the string
        CISCO_DATA['Dial'] = dialerVC #Asign the string to the data dictionary
        LBL['VCDial'].SetText(dialerVC)  #Send the string to GUI Label

    else:                            #If the user push a [*#0-9] button
        number = str(btn_name[4])    #Extract the valid character of BTN name
        dialerVC += number           #Append the last char to the string
        CISCO_DATA['Dial'] = dialerVC #Asign the string to the data dictionary
        LBL['VCDial'].SetText(dialerVC)  #Send the string to GUI Label
    pass

@event(BTNPAGE['VCDial'], BTNSTATE['List'])
def vc_dial_events(button, state):
    """User Actions: Touch VC Page"""
    ## All the VC Dial Buttons pressed come in button variable
    if state == 'Pressed' or state == 'Repeated':
        print('Button Pressed - VC: %s' % button.Name)
        dialer_vc(button.Name) #Recall a validation function
        button.SetState(1)
    else:
        button.SetState(0)
    pass

@event(BTNPAGE['VCOpt'], BTNSTATE['List'])
def vc_opt_events(button, state):
    """User Actions: Touch VC Page"""

    ## VC Options: Content Control
    if button is BTN['VCEnviar'] and state == 'Pressed':
        TLP.ShowPopup(POPUP['VC_PC'])
        BTN['VCEnviar'].SetState(1)
        print('Button Pressed - VC: %s' % 'Content')
    else:
        BTN['VCEnviar'].SetState(0)

    ## VC Options: Camera Control
    if button is BTN['VCCamara'] and state == 'Pressed':
        TLP.ShowPopup(POPUP['VC_Cam'])
        BTN['VCCamara'].SetState(1)
        print('Button Pressed - VC: %s' % 'Camera')
    else:
        BTN['VCCamara'].SetState(0)

    ## VC Options: AutoAnswer
    if button is BTN['VCAutoAn'] and state == 'Pressed':
        #
        if CISCO_DATA['AutoAnswer'] == True:
            CISCO.Set('AutoAnswer', 'Off')

        elif CISCO_DATA['AutoAnswer'] == False:
            CISCO.Set('AutoAnswer', 'On')
        print('Button Pressed - VC: %s' % 'AutoAnswer')
    pass

## PAGE VC Content -------------------------------------------------------------
@event(BTNPAGE['VCPC'], BTNSTATE['List'])
def vc_cam_content_sources(button, state):
    """User Actions: Touch VC Content Page"""

    if button is BTN['VCHDMI'] and state == 'Pressed':
        ## HDMI to Cisco Computer Input - Video
        MATRIX.Set('MatrixTieCommand', None, {'Input':'1', 'Output':'3', 'Tie Type':'Video'})
        print('Button Pressed - VC Share: %s' % 'HDMI')

    elif button is BTN['VCVGA'] and state == 'Pressed':
        ## VGA to Cisco Computer Input - Video
        MATRIX.Set('MatrixTieCommand', None, {'Input':'2', 'Output':'3', 'Tie Type':'Video'})
        print('Button Pressed - VC Share: %s' % 'VGA')

    elif button is BTN['VCPTZ'] and state == 'Pressed':
        ## PTZ to Cisco Computer Input - Video
        MATRIX.Set('MatrixTieCommand', None, {'Input':'3', 'Output':'3', 'Tie Type':'Video'})
        print('Button Pressed - VC Share: %s' % 'PTZ')

    elif button is BTN['VCShare'] and state == 'Pressed':
        ## ShareLink to Cisco Computer Input - Video
        MATRIX.Set('MatrixTieCommand', None, {'Input':'4', 'Output':'3', 'Tie Type':'Video'})
        print('Button Pressed - VC Share: %s' % 'ClickShare')

    elif button is BTN['VCBack2'] and state == 'Pressed':
        ## Hide VC Content POPUP and Show the main VC POPUP
        TLP.ShowPopup(POPUP['VC'])
        print('Button Pressed - VC Share: %s' % 'Back')

    elif button is BTN['VCSend'] and state == 'Pressed':
        ## Play - Share graphics presentation
        CISCO.Set('Presentation', '1')
        print('Button Pressed - VC Share: %s' % 'Send')

    elif button is BTN['VCStop'] and state == 'Pressed':
        ## Stop - Sharing graphics
        CISCO.Set('Presentation', 'Stop')
        print('Button Pressed - VC Share: %s' % 'Stop')
    pass

## PAGE VC Camera --------------------------------------------------------------
@event(BTNPAGE['VCCam'], BTNSTATE['List'])
def vc_nav_events(button, state):
    """User Actions: Touch VC Camera Page"""
    if button is BTN['VCUp']:
        if state == 'Pressed' or state == 'Repeated':
            if CISCO_DATA['Camera'] == 'Local':
                CISCO.Set('CameraTiltSX20', 'Up', {'Speed':7})
                print('Cam Local - Cisco: %s' % 'Cam Up')
            elif CISCO_DATA['Camera'] == 'Remote':
                CISCO.Set('FarEndCameraPan/Tilt', 'Up')
                print('Cam Remota - Cisco: %s' % 'Cam Up')
        #--
        elif state == 'Released':
            if CISCO_DATA['Camera'] == 'Local':
                CISCO.Set('CameraTiltSX20', 'Stop', {'Speed':7})
                print('Cam Local - Cisco: %s' % 'Cam Stop')
            elif CISCO_DATA['Camera'] == 'Remote':
                CISCO.Set('FarEndCameraPan/Tilt', 'Stop')
                print('Cam Remota - Cisco: %s' % 'Cam Stop')
    #--
    elif button is BTN['VCLeft']:
        if state == 'Pressed' or state == 'Repeated':
            if CISCO_DATA['Camera'] == 'Local':
                CISCO.Set('CameraPanSX20', 'Left', {'Speed':7})
                print('Cam Local - Cisco: %s' % 'Cam Left')
            elif CISCO_DATA['Camera'] == 'Remote':
                CISCO.Set('FarEndCameraPan/Tilt', 'Left')
                print('Cam Remota - Cisco: %s' % 'Cam Left')
        #--
        elif state == 'Released':
            if CISCO_DATA['Camera'] == 'Local':
                CISCO.Set('CameraPanSX20', 'Stop', {'Speed':7})
                print('Cam Local - Cisco: %s' % 'Cam Stop')
            elif CISCO_DATA['Camera'] == 'Remote':
                CISCO.Set('FarEndCameraPan/Tilt', 'Stop')
                print('Cam Remota - Cisco: %s' % 'Cam Stop')
    #--
    elif button is BTN['VCDown']:
        if state == 'Pressed' or state == 'Repeated':
            if CISCO_DATA['Camera'] == 'Local':
                CISCO.Set('CameraTiltSX20', 'Down', {'Speed':7})
                print('Cam Local - Cisco: %s' % 'Cam Down')
            elif CISCO_DATA['Camera'] == 'Remote':
                CISCO.Set('FarEndCameraPan/Tilt', 'Down')
                print('Cam Remota - Cisco: %s' % 'Cam Down')
        #--
        elif state == 'Released':
            if CISCO_DATA['Camera'] == 'Local':
                CISCO.Set('CameraTiltSX20', 'Stop', {'Speed':7})
                print('Cam Local - Cisco: %s' % 'Cam Stop')
            elif CISCO_DATA['Camera'] == 'Remote':
                CISCO.Set('FarEndCameraPan/Tilt', 'Stop')
                print('Cam Remota - Cisco: %s' % 'Cam Stop')
    #--
    elif button is BTN['VCRight']:
        if state == 'Pressed' or state == 'Repeated':
            if CISCO_DATA['Camera'] == 'Local':
                CISCO.Set('CameraPanSX20', 'Right', {'Speed':7})
                print('Cam Local - Cisco: %s' % 'Cam Right')
            elif CISCO_DATA['Camera'] == 'Remote':
                CISCO.Set('FarEndCameraPan/Tilt', 'Right')
                print('Cam Remota - Cisco: %s' % 'Cam Right')
        #--
        elif state == 'Released':
            if CISCO_DATA['Camera'] == 'Local':
                CISCO.Set('CameraPanSX20', 'Stop', {'Speed':7})
                print('Cam Local - Cisco: %s' % 'Cam Stop')
            elif CISCO_DATA['Camera'] == 'Remote':
                CISCO.Set('FarEndCameraPan/Tilt', 'Stop')
                print('Cam Remota - Cisco: %s' % 'Cam Stop')
    #--
    elif button is BTN['VCZoom1']: #+
        if state == 'Pressed' or state == 'Repeated':
            if CISCO_DATA['Camera'] == 'Local':
                CISCO.Set('CameraZoomSX20', 'In', {'Speed':7})
                print('Cam Local - Cisco: %s' % 'Cam Zoom+')
            elif CISCO_DATA['Camera'] == 'Remote':
                CISCO.Set('FarEndCameraZoom', 'In')
                print('Cam Remota - Cisco: %s' % 'Cam Zoom+')
            BTN['VCZoom1'].SetState(1)
        #--
        elif state == 'Released':
            if CISCO_DATA['Camera'] == 'Local':
                CISCO.Set('CameraZoomSX20', 'Stop', {'Speed':7})
                print('Cam Local - Cisco: %s' % 'Cam Stop')
            elif CISCO_DATA['Camera'] == 'Remote':
                CISCO.Set('FarEndCameraZoom', 'Stop')
                print('Cam Remota - Cisco: %s' % 'Cam Stop')
            BTN['VCZoom1'].SetState(0)
    #--
    elif button is BTN['VCZoom2']: #-
        if state == 'Pressed' or state == 'Repeated':
            if CISCO_DATA['Camera'] == 'Local':
                CISCO.Set('CameraZoomSX20', 'Out', {'Speed':7})
                print('Cam Local - Cisco: %s' % 'Cam Zoom-')
            elif CISCO_DATA['Camera'] == 'Remote':
                CISCO.Set('FarEndCameraZoom', 'Out')
                print('Cam Remota - Cisco: %s' % 'Cam Zoom-')
            BTN['VCZoom2'].SetState(1)
        #--
        elif state == 'Released':
            if CISCO_DATA['Camera'] == 'Local':
                CISCO.Set('CameraZoomSX20', 'Stop', {'Speed':7})
                print('Cam Local - Cisco: %s' % 'Cam Stop')
            elif CISCO_DATA['Camera'] == 'Remote':
                CISCO.Set('FarEndCameraZoom', 'Stop')
                print('Cam Remota - Cisco: %s' % 'Cam Stop')
            BTN['VCZoom2'].SetState(0)
    #--
    if button is BTN['VCLocal'] and state == 'Pressed':
        CISCO_DATA['Camera'] = 'Local'
        BTNGROUP['VCCam'].SetCurrent(BTN['VCLocal'])
        print('Button Pressed - Cisco: %s' % 'Cam Local')
    #--
    elif button is BTN['VCRemote'] and state == 'Pressed':
        CISCO_DATA['Camera'] = 'Remote'
        BTNGROUP['VCCam'].SetCurrent(BTN['VCRemote'])
        print('Button Pressed - Cisco: %s' % 'Cam Remote')
    pass


@event(BTNPAGE['VCPre'], BTNSTATE['List'])
def vc_cam_events(button, state):
    """User Actions: Touch VC Camera Page"""
    if button is BTN['VCP1'] and state == 'Pressed':
        if CISCO_DATA['Camera'] == 'Local':
            if CISCO_DATA['PresetMode'] == 'Recall':
                CISCO.Set('CameraPresetPositionRecallSX20', '1')
                print('Recall Local Preset Cisco: %s' % '1')
            elif CISCO_DATA['PresetMode'] == 'Save':
                CISCO.Set('CameraPresetSaveSX20', '1')
                print('Save Local Preset Cisco: %s' % '1')
        #--
        elif CISCO_DATA['Camera'] == 'Remote':
            if CISCO_DATA['PresetMode'] == 'Recall':
                CISCO.Set('FarEndCameraPresetRecall', '1')
                print('Recall Remote Preset Cisco: %s' % '1')
            elif CISCO_DATA['PresetMode'] == 'Save':
                CISCO.Set('FarEndCameraPresetSave', '1')
                print('Save Remote Preset Cisco: %s' % '1')
    #--
    elif button is BTN['VCP2'] and state == 'Pressed':
        if CISCO_DATA['Camera'] == 'Local':
            if CISCO_DATA['PresetMode'] == 'Recall':
                CISCO.Set('CameraPresetPositionRecallSX20', '2')
                print('Recall Local Preset Cisco: %s' % '2')
            elif CISCO_DATA['PresetMode'] == 'Save':
                CISCO.Set('CameraPresetSaveSX20', '2')
                print('Save Local Preset Cisco: %s' % '2')
        #--
        elif CISCO_DATA['Camera'] == 'Remote':
            if CISCO_DATA['PresetMode'] == 'Recall':
                CISCO.Set('FarEndCameraPresetRecall', '2')
                print('Recall Remote Preset Cisco: %s' % '2')
            elif CISCO_DATA['PresetMode'] == 'Save':
                CISCO.Set('FarEndCameraPresetSave', '2')
                print('Save Remote Preset Cisco: %s' % '2')
    #--
    elif button is BTN['VCP3'] and state == 'Pressed':
        if CISCO_DATA['Camera'] == 'Local':
            if CISCO_DATA['PresetMode'] == 'Recall':
                CISCO.Set('CameraPresetPositionRecallSX20', '3')
                print('Recall Local Preset Cisco: %s' % '3')
            elif CISCO_DATA['PresetMode'] == 'Save':
                CISCO.Set('CameraPresetSaveSX20', '3')
                print('Save Local Preset Cisco: %s' % '3')
        #--
        elif CISCO_DATA['Camera'] == 'Remote':
            if CISCO_DATA['PresetMode'] == 'Recall':
                CISCO.Set('FarEndCameraPresetRecall', '3')
                print('Recall Remote Preset Cisco: %s' % '3')
            elif CISCO_DATA['PresetMode'] == 'Save':
                CISCO.Set('FarEndCameraPresetSave', '3')
                print('Save Remote Preset Cisco: %s' % '3')
    #--
    elif button is BTN['VCP4'] and state == 'Pressed':
        if CISCO_DATA['Camera'] == 'Local':
            if CISCO_DATA['PresetMode'] == 'Recall':
                CISCO.Set('CameraPresetPositionRecallSX20', '4')
                print('Recall Local Preset Cisco: %s' % '4')
            elif CISCO_DATA['PresetMode'] == 'Save':
                CISCO.Set('CameraPresetSaveSX20', '4')
                print('Save Local Preset Cisco: %s' % '4')
        #--
        elif CISCO_DATA['Camera'] == 'Remote':
            if CISCO_DATA['PresetMode'] == 'Recall':
                CISCO.Set('FarEndCameraPresetRecall', '4')
                print('Recall Remote Preset Cisco: %s' % '4')
            elif CISCO_DATA['PresetMode'] == 'Save':
                CISCO.Set('FarEndCameraPresetSave', '4')
                print('Save Remote Preset Cisco: %s' % '4')
    #--
    elif button is BTN['VCP5'] and state == 'Pressed':
        if CISCO_DATA['Camera'] == 'Local':
            if CISCO_DATA['PresetMode'] == 'Recall':
                CISCO.Set('CameraPresetPositionRecallSX20', '5')
                print('Recall Local Preset Cisco: %s' % '5')
            elif CISCO_DATA['PresetMode'] == 'Save':
                CISCO.Set('CameraPresetSaveSX20', '5')
                print('Save Local Preset Cisco: %s' % '5')
        #--
        elif CISCO_DATA['Camera'] == 'Remote':
            if CISCO_DATA['PresetMode'] == 'Recall':
                CISCO.Set('FarEndCameraPresetRecall', '5')
                print('Recall Remote Preset Cisco: %s' % '5')
            elif CISCO_DATA['PresetMode'] == 'Save':
                CISCO.Set('FarEndCameraPresetSave', '5')
                print('Save Remote Preset Cisco: %s' % '5')
    #--
    elif button is BTN['VCRecall'] and state == 'Pressed':
        CISCO_DATA['PresetMode'] = 'Recall'
        BTNGROUP['VCPTZ'].SetCurrent(BTN['VCRecall'])
        print('Button Pressed - Cisco: %s' % 'Recall')
    #--
    elif button is BTN['VCSave'] and state == 'Pressed':
        CISCO_DATA['PresetMode'] = 'Save'
        BTNGROUP['VCPTZ'].SetCurrent(BTN['VCSave'])
        print('Button Pressed - Cisco: %s' % 'Save')
    pass

## PAGE Webex ------------------------------------------------------------------
@event(BTNPAGE['Webex'], BTNSTATE['List'])
def webex_events(button, state):
    """User Actions: Touch Webex Page"""
    if button is BTN['WHDMI'] and state == 'Pressed':
        ## HDMI to MediaPort200 Input - Video
        MATRIX.Set('MatrixTieCommand', None, {'Input':'1', 'Output':'5', 'Tie Type':'Video'})
        print('Button Pressed - Webex: %s' % 'HDMI')

    elif button is BTN['WVGA'] and state == 'Pressed':
        ## VGA to MediaPort200 Input - Video
        MATRIX.Set('MatrixTieCommand', None, {'Input':'2', 'Output':'5', 'Tie Type':'Video'})
        print('Button Pressed - Webex: %s' % 'VGA')

    elif button is BTN['WPTZ'] and state == 'Pressed':
        ## PTZ to MediaPort200 Input - Video
        MATRIX.Set('MatrixTieCommand', None, {'Input':'3', 'Output':'5', 'Tie Type':'Video'})
        print('Button Pressed - Webex: %s' % 'PTZ')

    elif button is BTN['WShare'] and state == 'Pressed':
        ## ShareLink to MediaPort200 Input - Video
        MATRIX.Set('MatrixTieCommand', None, {'Input':'4', 'Output':'5', 'Tie Type':'Video'})
        print('Button Pressed - Webex: %s' % 'ShareLink')

    elif button is BTN['WCisco1'] and state == 'Pressed':
        ## Cisco 1 to MediaPort200 Input - Video
        MATRIX.Set('MatrixTieCommand', None, {'Input':'5', 'Output':'5', 'Tie Type':'Video'})
        print('Button Pressed - Webex: %s' % 'Cisco 1')

    elif button is BTN['WCisco2'] and state == 'Pressed':
        ## Cisco 2 to MediaPort200 Input - Video
        MATRIX.Set('MatrixTieCommand', None, {'Input':'6', 'Output':'5', 'Tie Type':'Video'})
        print('Button Pressed - Webex: %s' % 'Cisco 2')
    pass

## PAGE VoIP -------------------------------------------------------------------
@event(BTNPAGE['TelCall'], BTNSTATE['List'])
def vi_call_events(button, state):
    """User Actions: Touch VoIP Page"""
    if button is BTN['Call'] and state == 'Pressed':
        ##--This button dial the number typed on the touch panel (Biamp VoIP)
        BIAMP.Set('VoIPHook', 'Dial',
                  {'Instance Tag':'Dialer', 'Line':'1', 'Call Appearance':'1', \
                    'Number':VOIP_DATA['Dial']})
        print('Button Pressed - VoIP: %s' % 'Call')
    #--
    elif button is BTN['Hangup'] and state == 'Pressed':
        ##--This button hangs up all active calls (Biamp VoIP)
        BIAMP.Set('VoIPHook', 'End',
                  {'Instance Tag':'Dialer', 'Line':'1', 'Call Appearance':'1'})
        print('Button Pressed - VoIP: %s' % 'Hangup')
    pass

## This function is called when the user press a Dial Button
## This function add or remove data from the panel Dial Number
def dialer_voip(btn_name):
    """User Actions: Touch VoIP Page"""
    global dialerVI

    if btn_name == 'Delete':         #If the user push 'Delete' button
        dialerVI = dialerVI[:-1]     #Remove the last char of the string
        VOIP_DATA['Dial'] = dialerVI #Asign the string to the data dictionary
        LBL['Dial'].SetText(dialerVI)    #Send the string to GUI Label

    else:                                #If the user push a [*#0-9] button
        number = str(btn_name[4])        #Extract the valid character of BTN name
        if VOIP_DATA['DTMF'] == False:   #If the DTMF is off
            dialerVI += number           #Append the last char to the string
            VOIP_DATA['Dial'] = dialerVI #Asign the string to the data dictionary
            LBL['Dial'].SetText(dialerVI)    #Send the string to GUI Label
        elif VOIP_DATA['DTMF'] == True:  #If DTMF is On
            BIAMP.Set('DTMF', number, {'Instance Tag':'Dialer', 'Line':'1'})
    pass

@event(BTNPAGE['TelDial'], BTNSTATE['List'])
def vi_dial_events(button, state):
    """User Actions: Touch VoIP Page"""
    ## All the VoIP Dial Buttons pressed come in button variable
    if state == 'Pressed' or state == 'Repeated':
        print('Button Pressed - VoIP: %s' % button.Name)
        dialer_voip(button.Name) #Recall a validation function
        button.SetState(1)
    else:
        button.SetState(0)
    pass

@event(BTNPAGE['TelOpt'], BTNSTATE['List'])
def vi_opt_events(button, state):
    """User Actions: Touch VoIP Page"""
    ## VoIP Redial Control
    if button is BTN['Redial'] and state == 'Pressed':
        BIAMP.Set('VoIPHook', 'Redial', {'Instance Tag':'Dialer', \
                  'Line':'1', 'Call Appearance':'1'})
        print('Button Pressed - VoIP: %s' % 'Redial')

    ## VoIP DTMF Control
    elif button is BTN['DTMF'] and state == 'Pressed':
        if VOIP_DATA['DTMF'] == False:
            VOIP_DATA['DTMF'] = True
            BTN['DTMF'].SetState(1)
            print('Button Pressed - VoIP: %s' % 'DTMF On')
        #--
        elif VOIP_DATA['DTMF'] == True:
            VOIP_DATA['DTMF'] = False
            BTN['DTMF'].SetState(0)
            print('Button Pressed - VoIP: %s' % 'DTMF Off')
        print('Button Pressed - VoIP: %s' % 'DTMF')

    ## Hold / Resume Control
    elif button is BTN['Hold'] and state == 'Pressed':
        print('Button Pressed - VoIP: %s' % 'Hold/Resume')
    pass

## PAGE Audio ------------------------------------------------------------------
@event(BTNPAGE['Audio1'], BTNSTATE['List'])
def audio_source_events(button, state):
    """User Actions: Touch Audio Page"""

    if button is BTN['XHDMI'] and state == 'Pressed':
        ## HDMI to HDMI Audio Dembedder Input - Audio
        MATRIX.Set('MatrixTieCommand', None, {'Input':'1', 'Output':'1', 'Tie Type':'Audio'})
        print('Button Pressed - Audio: %s' % 'HDMI')

    elif button is BTN['XVGA'] and state == 'Pressed':
         ## VGA to HDMI Audio Dembedder Input - Audio
        MATRIX.Set('MatrixTieCommand', None, {'Input':'2', 'Output':'1', 'Tie Type':'Audio'})
        print('Button Pressed - Audio: %s' % 'VGA')

    elif button is BTN['XShare'] and state == 'Pressed':
         ## ShareLink to HDMI Audio Dembedder Input - Audio
        MATRIX.Set('MatrixTieCommand', None, {'Input':'4', 'Output':'1', 'Tie Type':'Audio'})
        print('Button Pressed - Audio: %s' % 'ShareLink')
    pass

@event(BTNPAGE['Audio2'], BTNSTATE['List'])
def audio_vol_events(button, state):
    """User Actions: Touch Audio Page"""

    ## Data of current Biamp Block Gain
    global CURRENTLVL1
    global CURRENTLVL2
    CURRENTLVL1 = BIAMP_DATA['lvl_spk']
    CURRENTLVL2 = CISCO_DATA['Volume']

    ## Audio Speaker: Vol -
    if button is BTN['XSpkLess']:
        if state == 'Pressed' or state == 'Repeated':
            CURRENTLVL1 -= 5 ## Decrease 5 dB
            if CURRENTLVL1 < -100:
                print('Biamp Minimun gain')
            else:
                BIAMP.Set('LevelControl', CURRENTLVL1, {'Instance Tag':'lvl_spk', 'Channel':'1'})
                LVL['Spk'].SetLevel(CURRENTLVL1)
            BTN['XSpkLess'].SetState(1)
        else:
            BTN['XSpkLess'].SetState(0)
        print('Button Pressed - Audio: %s' % 'Spk-')

    ## Audio Speaker: Vol +
    elif button is BTN['XSpkPlus']:
        if state == 'Pressed' or state == 'Repeated':
            CURRENTLVL1 += 5 ## Increase 5 dB
            if CURRENTLVL1 > 12:
                print('Biamp Maximun gain')
            else:
                BIAMP.Set('LevelControl', CURRENTLVL1, {'Instance Tag':'lvl_spk', 'Channel':'1'})
                LVL['Spk'].SetLevel(CURRENTLVL1)
            BTN['XSpkPlus'].SetState(1)
        else:
            BTN['XSpkPlus'].SetState(0)
        print('Button Pressed - Audio: %s' % 'Spk+')

    ## Audio VC Remote: Vol -
    if button is BTN['XVCLess']:
        if state == 'Pressed' or state == 'Repeated':
            CURRENTLVL2 -= 5 ## Decrease 5 dB
            if CURRENTLVL2 < 0:
                print('VC Minimun gain')
            else:
                CISCO.Set('Volume', CURRENTLVL2)
                LVL['VC'].SetLevel(CURRENTLVL2)
            BTN['XVCLess'].SetState(1)
        else:
            BTN['XVCLess'].SetState(0)
        print('Button Pressed - Audio: %s' % 'VC-')

    ## Audio VC Remote: Vol +
    if button is BTN['XVCPlus']:
        if state == 'Pressed' or state == 'Repeated':
            CURRENTLVL2 += 5 ## Increase 5 dB
            if CURRENTLVL2 < 0:
                print('VC Maximun gain')
            else:
                CISCO.Set('Volume', CURRENTLVL2)
                LVL['VC'].SetLevel(CURRENTLVL2)
            BTN['XVCPlus'].SetState(1)
        else:
            BTN['XVCPlus'].SetState(0)
        print('Button Pressed - Audio: %s' % 'VC+')
    pass

@event(BTNPAGE['Audio3'], BTNSTATE['List'])
def audio_mute_events(button, state):
    """User Actions: Touch Audio Page"""

    ## Mute Speaker Audio Control
    if button is BTN['XSpk'] and state == 'Pressed':
        if BIAMP_DATA['MuteSpk'] == True:
            BIAMP.Set('MuteControl', 'Off', {'Instance Tag':'lvl_spk', 'Channel':'1'})
        elif BIAMP_DATA['MuteSpk'] == False:
            BIAMP.Set('MuteControl', 'On', {'Instance Tag':'lvl_spk', 'Channel':'1'})
        print('Button Pressed - Audio: %s' % 'Mute Spk')

    ## Mute VC Remote Audio Control
    elif button is BTN['XVC'] and state == 'Pressed':
        if BIAMP_DATA['MuteVCRx'] == True:
            BIAMP.Set('MuteControl', 'Off', {'Instance Tag':'lvl_vcrx', 'Channel':'1'})
        elif BIAMP_DATA['MuteVCRx'] == False:
            BIAMP.Set('MuteControl', 'On', {'Instance Tag':'lvl_vcrx', 'Channel':'1'})
        print('Button Pressed - Audio: %s' % 'Mute VC')

    ## Mute All Mics Audio Control
    elif button is BTN['XMics'] and state == 'Pressed':
        if BIAMP_DATA['Mute_Mics'] == True:
            BIAMP.Set('MuteControl', 'Off', {'Instance Tag':'mute_mix', 'Channel':'1'})
        elif BIAMP_DATA['Mute_Mics'] == False:
            BIAMP.Set('MuteControl', 'On', {'Instance Tag':'mute_mix', 'Channel':'1'})
        print('Button Pressed - Audio: %s' % 'Mute Mics')
    pass

## Lights PAGE -----------------------------------------------------------------
@event(BTNPAGE['Lights'], BTNSTATE['List'])
def lights_events(button, state):
    """User Actions: Touch Lights Page"""

    if button is BTN['Escene1'] and state == 'Pressed':
        ## All Lights Off
        LUTRON.Set('4ButtonPicoControls', 'Press', {'Integration ID':'2', 'Button':'4'})
        print('Button Pressed - Lights: %s' % 'Escene 1')

    elif button is BTN['Escene2'] and state == 'Pressed':
        ## Black soft Lights
        LUTRON.Set('4ButtonPicoControls', 'Press', {'Integration ID':'2', 'Button':'3/Lower'})
        print('Button Pressed - Lights: %s' % 'Escene 2')

    elif button is BTN['Escene3'] and state == 'Pressed':
        ## White soft Lights
        LUTRON.Set('4ButtonPicoControls', 'Press', {'Integration ID':'2', 'Button':'2/Raise'})
        print('Button Pressed - Lights: %s' % 'Escene 3')

    elif button is BTN['Escene4'] and state == 'Pressed':
        ## All Lights On
        LUTRON.Set('4ButtonPicoControls', 'Press', {'Integration ID':'2', 'Button':'1'})
        print('Button Pressed - Lights: %s' % 'Escene 4')

    ## Mutually Exclusive
    BTNGROUP['Lights'].SetCurrent(button)
    pass

## Blinds PAGE -----------------------------------------------------------------
@event(BTNPAGE['Blinds'], BTNSTATE['List'])
def lights_events(button, state):
    """User Actions: Touch Blinds Page"""

    if button is BTN['BlindsUp'] and state == 'Pressed' or state == 'Repeated':
        ## Blinds Up
        #SOMFY.Set('Tilt', 'Up', {'Channel':'1', 'Amplitude':1})
        BTNGROUP['Blinds'].SetCurrent(button)
        print('Button Pressed - Lights: %s' % 'Blinds Up')

    elif button is BTN['BlindsSt'] and state == 'Pressed':
        ## Blinds Stop
        #SOMFY.Set('Position', 'Stop', {'Channel':'1'})
        BTNGROUP['Blinds'].SetCurrent(button)
        print('Button Pressed - Lights: %s' % 'Blinds Stop')

    elif button is BTN['BlindsDw'] and state == 'Pressed' or state == 'Repeated':
        ## Blinds Down
        #SOMFY.Set('Tilt', 'Down', {'Channel':'1', 'Amplitude':1})
        BTNGROUP['Blinds'].SetCurrent(button)
        print('Button Pressed - Lights: %s' % 'Blinds Down')
    
    ## Mutually Exclusive
    BTNGROUP['Blinds'].SetCurrent(button)
    pass

## Status PAGE -----------------------------------------------------------------

## Power PAGE ------------------------------------------------------------------
@event(BTN['PowerAll'], BTNSTATE['List'])
def power_events(button, state):
    """User Actions: Touch PowerOff Page"""

    global PWRCOUNT
    ## If the user press the Power Button:
    ## Only Turn On the first state of button - Does not do any action
    if state == 'Pressed':
        BTN['PowerAll'].SetState(4)
        print('Button Pressed: %s' % 'PowerAll')

    ## If the user holds down the button:
    ## A variable is Decremented from 4 to 0 seconds
    ## In each new value, Turn On each visual state of the Power Button
    ## Whne the value is equal to 0, ShutDown all devices in the System
    elif state == 'Repeated':
        PWRCOUNT = PWRCOUNT - 1
        BTN['PowerAll'].SetState(PWRCOUNT)
        LBL['CountAll'].SetText(str(PWRCOUNT))
        print('Button Repeated: %s' % 'PowerAll')
        ## SHUTDOWN ALL DEVICES
        if PWRCOUNT == 0:
            TLP.ShowPage(PAGE['Index'])

    ## If the user release the Button:
    ## Clean the counter power data in GUI and delete the visual feedback
    elif state == 'Released':
        PWRCOUNT = 4
        BTN['PowerAll'].SetState(0)
        LBL['CountAll'].SetText('')
        print('Button Released: %s' % 'PowerAll')
    pass

## End Events Definitions-------------------------------------------------------
initialize()
