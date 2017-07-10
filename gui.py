""" --------------------------------------------------------------------------
 Business   | Asesores y Consultores en Tecnología S.A. de C.V.
 Programmer | Dyanko Cisneros Mendoza
 Customer   | Human Quality
 Project    | Meeting Room
 Version    | 0.1 --------------------------------------------------------- """

## CONTROL SCRIPT IMPORT -------------------------------------------------------
from extronlib.device import UIDevice
from extronlib.ui import Button, Label, Level
from extronlib.system import MESet

# UI Device
TLP = UIDevice('TouchPanel')

# UI Buttons
BTN = {
    ## Index
    'Index'     : Button(TLP, 1),
    ## Main
    'Video'     : Button(TLP, 2),
    'VC'        : Button(TLP, 3),
    'Webex'     : Button(TLP, 4),
    'VoIP'      : Button(TLP, 5),
    'Lights'    : Button(TLP, 6),
    'Audio'     : Button(TLP, 7),
    'Status'    : Button(TLP, 8),
    'PwrOff'    : Button(TLP, 9),
    ## Video
    'DisplayL'  : Button(TLP, 11),
    'DisplayR'  : Button(TLP, 12),
    ## Display L
    'LHDMI'     : Button(TLP, 21),
    'LVGA'      : Button(TLP, 22),
    'LPTZ'      : Button(TLP, 23),
    'LShare'    : Button(TLP, 24),
    'LPwrOn'    : Button(TLP, 25),
    'LPwrOff'   : Button(TLP, 26),
    'LBack'     : Button(TLP, 27),
    ## Display R
    'RHDMI'     : Button(TLP, 31),
    'RVGA'      : Button(TLP, 32),
    'RPTZ'      : Button(TLP, 33),
    'RShare'    : Button(TLP, 34),
    'RPwrOn'    : Button(TLP, 35),
    'RPwrOff'   : Button(TLP, 36),
    'RBack'     : Button(TLP, 37),
    ## Webex
    'WHDMI'     : Button(TLP, 61),
    'WVGA'      : Button(TLP, 62),
    'WPTZ'      : Button(TLP, 63),
    'WShare'    : Button(TLP, 64),
    'WCisco1'   : Button(TLP, 65),
    'WCisco2'   : Button(TLP, 66),
    ## Lights & Blinds
    'Escene1'   : Button(TLP, 71),
    'Escene2'   : Button(TLP, 72),
    'Escene3'   : Button(TLP, 73),
    'Escene4'   : Button(TLP, 74),
    'BlindsUp'  : Button(TLP, 75, repeatTime=0.1),
    'BlindsSt'  : Button(TLP, 76),
    'BlindsDw'  : Button(TLP, 77, repeatTime=0.1),
    ## VoIP Dial
    'Call'      : Button(TLP, 91),
    'Hangup'    : Button(TLP, 92),
    ## VoIP Numbers
    'Dial0'     : Button(TLP, 100),
    'Dial1'     : Button(TLP, 101),
    'Dial2'     : Button(TLP, 102),
    'Dial3'     : Button(TLP, 103),
    'Dial4'     : Button(TLP, 104),
    'Dial5'     : Button(TLP, 105),
    'Dial6'     : Button(TLP, 106),
    'Dial7'     : Button(TLP, 107),
    'Dial8'     : Button(TLP, 108),
    'Dial9'     : Button(TLP, 109),
    'DialA'     : Button(TLP, 110),
    'DialG'     : Button(TLP, 111),
    'Delete'    : Button(TLP, 115, repeatTime=0.1),
    ## VoIP Options
    'Redial'    : Button(TLP, 112),
    'DTMF'      : Button(TLP, 113),
    'Hold'      : Button(TLP, 114),
    ## VC Dial
    'VCCall'    : Button(TLP, 131),
    'VCHangup'  : Button(TLP, 132),
    ## VC Numbers
    'VCDial0'   : Button(TLP, 140),
    'VCDial1'   : Button(TLP, 141),
    'VCDial2'   : Button(TLP, 142),
    'VCDial3'   : Button(TLP, 143),
    'VCDial4'   : Button(TLP, 144),
    'VCDial5'   : Button(TLP, 145),
    'VCDial6'   : Button(TLP, 146),
    'VCDial7'   : Button(TLP, 147),
    'VCDial8'   : Button(TLP, 148),
    'VCDial9'   : Button(TLP, 149),
    'VCDialA'   : Button(TLP, 150),
    'VCDialG'   : Button(TLP, 151),
    'VCDelete'  : Button(TLP, 155, repeatTime=0.1),
    ## VC Options
    'VCEnviar'  : Button(TLP, 152),
    'VCCamara'  : Button(TLP, 153),
    'VCAutoAn'  : Button(TLP, 154),
    ## VC Content Sources
    'VCHDMI'    : Button(TLP, 181),
    'VCVGA'     : Button(TLP, 182),
    'VCPTZ'     : Button(TLP, 183),
    'VCShare'   : Button(TLP, 184),
    ## VC Content Sharing
    'VCBack2'   : Button(TLP, 185),
    'VCSend'    : Button(TLP, 186),
    'VCStop'    : Button(TLP, 187),
    ## VC Camera Presets
    'VCP1'      : Button(TLP, 161),
    'VCP2'      : Button(TLP, 162),
    'VCP3'      : Button(TLP, 163),
    'VCP4'      : Button(TLP, 164),
    'VCP5'      : Button(TLP, 165),
    'VCRecall'  : Button(TLP, 166),
    'VCSave'    : Button(TLP, 167),
    ## VC Camera Zoom
    'VCZoom1'   : Button(TLP, 168, repeatTime=0.1),
    'VCZoom2'   : Button(TLP, 169, repeatTime=0.1),
    ## VC Camera Movement
    'VCUp'      : Button(TLP, 170, repeatTime=0.1),
    'VCLeft'    : Button(TLP, 171, repeatTime=0.1),
    'VCDown'    : Button(TLP, 172, repeatTime=0.1),
    'VCRight'   : Button(TLP, 173, repeatTime=0.1),
    ## VC Camera Selection
    'VCLocal'   : Button(TLP, 174),
    'VCRemote'  : Button(TLP, 175),
    ## Audio Sources
    'XHDMI'     : Button(TLP, 188),
    'XVGA'      : Button(TLP, 189),
    'XShare'    : Button(TLP, 190),
    ## Audio Gain
    'XSpkLess'  : Button(TLP, 191, repeatTime=0.1),
    'XSpkPlus'  : Button(TLP, 192, repeatTime=0.1),
    'XVCLess'   : Button(TLP, 193, repeatTime=0.1),
    'XVCPlus'   : Button(TLP, 194, repeatTime=0.1),

    ## Audio Mute
    'XSpk'      : Button(TLP, 197),
    'XVC'       : Button(TLP, 198),
    'XMics'     : Button(TLP, 199),
    ## Status
    'LANMatrix' : Button(TLP, 211),
    'LanBridge' : Button(TLP, 212),
    'LANCisco'  : Button(TLP, 213),
    'LANBiamp'  : Button(TLP, 214),
    'LANLutron' : Button(TLP, 215),
    '232Somfy'  : Button(TLP, 216),
    ## Signal Led
    'Signal1'   : Button(TLP, 221),
    'Signal2'   : Button(TLP, 222),
    'Signal3'   : Button(TLP, 223),
    'Signal4'   : Button(TLP, 224),
    'Signal5'   : Button(TLP, 225),
    'Signal6'   : Button(TLP, 226),
    ## Power
    'PowerAll'  : Button(TLP, 250, repeatTime=1),
}

# UI Page Buttons
BTNPAGE = {
    'Main'   : [BTN['Video'], BTN['VC'], BTN['Webex'], BTN['Lights'],
                BTN['VoIP'], BTN['Audio'], BTN['Status'], BTN['PwrOff']],

    'Video'  : [BTN['DisplayL'], BTN['DisplayR']],

    'LCD1'   : [BTN['LHDMI'], BTN['LVGA'], BTN['LPTZ'], BTN['LShare'],
                BTN['LPwrOn'], BTN['LPwrOff'], BTN['LBack']],

    'LCD1_S' : [BTN['LHDMI'], BTN['LVGA'], BTN['LPTZ'], BTN['LShare']],

    'LCD2'   : [BTN['RHDMI'], BTN['RVGA'], BTN['RPTZ'], BTN['RShare'],
                BTN['RPwrOn'], BTN['RPwrOff'], BTN['RBack']],

    'LCD2_S' : [BTN['RHDMI'], BTN['RVGA'], BTN['RPTZ'], BTN['RShare']],

    'VCCall' : [BTN['VCCall'], BTN['VCHangup']],

    'VCDial' : [BTN['VCDial0'], BTN['VCDial1'], BTN['VCDial2'], BTN['VCDial3'],
                BTN['VCDial4'], BTN['VCDial5'], BTN['VCDial6'], BTN['VCDial7'],
                BTN['VCDial8'], BTN['VCDial9'], BTN['VCDialA'], BTN['VCDialG'],
                BTN['VCDelete']],

    'VCOpt'  : [BTN['VCEnviar'], BTN['VCCamara'], BTN['VCAutoAn']],

    'VCPC'   : [BTN['VCHDMI'], BTN['VCVGA'], BTN['VCPTZ'], BTN['VCShare'],
                BTN['VCBack2'], BTN['VCSend'], BTN['VCStop']],

    'VCPC_S' : [BTN['VCHDMI'], BTN['VCVGA'], BTN['VCPTZ'], BTN['VCShare']],

    'VCCam'  : [BTN['VCUp'], BTN['VCLeft'], BTN['VCDown'], BTN['VCRight'],
                BTN['VCZoom1'], BTN['VCZoom2'], BTN['VCLocal'], BTN['VCRemote']],

    'VCPre'  : [BTN['VCP1'], BTN['VCP2'], BTN['VCP3'], BTN['VCP4'],
                BTN['VCP5'], BTN['VCRecall'], BTN['VCSave']],

    'Webex'  : [BTN['WHDMI'], BTN['WVGA'], BTN['WPTZ'], BTN['WShare'],
                BTN['WCisco1'], BTN['WCisco2']],

    'TelCall': [BTN['Call'], BTN['Hangup']],

    'TelDial': [BTN['Dial0'], BTN['Dial1'], BTN['Dial2'], BTN['Dial3'],
                BTN['Dial4'], BTN['Dial5'], BTN['Dial6'], BTN['Dial7'],
                BTN['Dial8'], BTN['Dial9'], BTN['DialA'], BTN['DialG'],
                BTN['Delete']],

    'TelOpt' : [BTN['Redial'], BTN['DTMF'], BTN['Hold']],

    'Lights' : [BTN['Escene1'], BTN['Escene2'], BTN['Escene3'], BTN['Escene4']],

    'Blinds' : [BTN['BlindsUp'], BTN['BlindsSt'], BTN['BlindsDw']],

    'Audio1' : [BTN['XHDMI'], BTN['XVGA'], BTN['XShare']],

    'Audio2' : [BTN['XSpkLess'], BTN['XSpkPlus'], BTN['XVCLess'], BTN['XVCPlus']],

    'Audio3' : [BTN['XSpk'], BTN['XVC'], BTN['XMics']],
}

# UI Group Page Buttons
BTNGROUP = {
    'Main' : MESet(BTNPAGE['Main']),

    'VCCam' : MESet([BTN['VCLocal'], BTN['VCRemote']]),

    'VCPTZ' : MESet([BTN['VCRecall'], BTN['VCSave']]),

    'LCD1_S' : MESet(BTNPAGE['LCD1_S']),

    'LCD2_S' : MESet(BTNPAGE['LCD2_S']),

    'VCPC_S' : MESet(BTNPAGE['VCPC_S']),

    'Webex' : MESet(BTNPAGE['Webex']),

    'Lights': MESet(BTNPAGE['Lights']),

    'Blinds': MESet(BTNPAGE['Blinds']),

    'Audio' : MESet(BTNPAGE['Audio1']),
}

# UI Button states
BTNSTATE = {
    'List' : ['Pressed', 'Released', 'Held', 'Repeated', 'Tapped'],
}

# UI Labels
LBL = {
    'Master'  : Label(TLP, 300),
    'Dial'    : Label(TLP, 116),
    'VCDial'  : Label(TLP, 156),
    'PwrAll'  : Label(TLP, 251),
    'CountAll': Label(TLP, 252),
}

# UI Levels
LVL = {
    'Spk' : Level(TLP, 195),
    'VC'  : Level(TLP, 196),
}
LVL['Spk'].SetRange(-100, 12, 1)

# UI Device Popups
POPUP = {
    'Video'  : 'Video',
    'LCD1'   : 'Display_L',
    'LCD2'   : 'Display_R',
    'VC'     : 'VC',
    'VC_PC'  : 'VC_Content',
    'VC_Cam' : 'VC_Cam',
    'Webex'  : 'Webex',
    'VoIP'   : 'VoIP',
    'Lights' : 'Lights',
    'Audio'  : 'Audio',
    'Status' : 'Status',
    'Power'  : 'x_PowerOff',
    'Hi'     : 'x_Welcome',
}

# UI Device Pages
PAGE = {
    'Index' : 'Index',
    'Main'  : 'Main',
}
