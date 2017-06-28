## -------------------------------------------------------------------------- ##
## Business   | Asesores y Consultores en Tecnología S.A. de C.V. ----------- ##
## Programmer | Dyanko Cisneros Mendoza
## Customer   | Human Quality
## Project    | Meeting Room
## Version    | 0.1 --------------------------------------------------------- ##

## CONTROL SCRIPT IMPORT -------------------------------------------------------
from extronlib.device import UIDevice
from extronlib.ui import Button, Label, Level
from extronlib.system import MESet

# UI Device
TLP = UIDevice('TouchPanel')

# UI Buttons
Btn = {
    ## Index
    'Index'   : Button(TLP, 1),
    ## Main
    'Video'     : Button(TLP, 2),
    'VC'        : Button(TLP, 3),
    'Webex'     : Button(TLP, 4),
    'Rec'       : Button(TLP, 5),
    'VoIP'      : Button(TLP, 6),
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
    'Delete'    : Button(TLP, 115, repeatTime = 0.1),
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
    'VCDelete'  : Button(TLP, 155, repeatTime = 0.1),
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
    'VCZoom1'   : Button(TLP, 168, repeatTime = 0.1),
    'VCZoom2'   : Button(TLP, 169, repeatTime = 0.1),
    ## VC Camera Movement
    'VCUp'      : Button(TLP, 170, repeatTime = 0.1),
    'VCLeft'    : Button(TLP, 171, repeatTime = 0.1),
    'VCDown'    : Button(TLP, 172, repeatTime = 0.1),
    'VCRight'   : Button(TLP, 173, repeatTime = 0.1),
    ## VC Camera Selection
    'VCLocal'   : Button(TLP, 174),
    'VCRemote'  : Button(TLP, 175),
    ## Audio Sources
    'XHDMI'     : Button(TLP, 188),
    'XVGA'      : Button(TLP, 189),
    'XShare'    : Button(TLP, 190),
    ## Audio Gain
    'XSpkLess'  : Button(TLP, 191, repeatTime = 0.1),
    'XSpkPlus'  : Button(TLP, 192, repeatTime = 0.1),
    'XVCLess'   : Button(TLP, 193, repeatTime = 0.1),
    'XVCPlus'   : Button(TLP, 194, repeatTime = 0.1),

    ## Audio Mute
    'XSpk'      : Button(TLP, 197),
    'XVC'       : Button(TLP, 198),
    'XMics'     : Button(TLP, 199),
    ## Status
    '232LCD1'   : Button(TLP, 211),
    '232LCD2'   : Button(TLP, 212),
    'LANMatrix' : Button(TLP, 213),
    'LANBiamp'  : Button(TLP, 214),
    '232PTZ'    : Button(TLP, 215),
    '232Cisco'  : Button(TLP, 216),
    'LANRec'    : Button(TLP, 217),
    'LanVaddio' : Button(TLP, 221),

    ## Power
    'PowerAll'  : Button(TLP, 250, repeatTime = 1),
}

# UI Page Buttons
Btn_Page = {
    'Main'   : [Btn['Video'], Btn['VC'], Btn['Webex'], Btn['Rec'],
                Btn['VoIP'], Btn['Audio'], Btn['Status'], Btn['PwrOff']],
    
    'Video'  : [Btn['DisplayL'], Btn['DisplayR']],

    'LCD1'   : [Btn['LHDMI'], Btn['LVGA'], Btn['LPTZ'], Btn['LShare'],
                Btn['LPwrOn'], Btn['LPwrOff'], Btn['LBack']],
    
    'LCD2'   : [Btn['RHDMI'], Btn['RVGA'], Btn['RPTZ'], Btn['RShare'],
                Btn['RPwrOn'], Btn['RPwrOff'], Btn['RBack']],

    'VCCall' : [Btn['VCCall'], Btn['VCHangup']],

    'VCDial' : [Btn['VCDial0'], Btn['VCDial1'], Btn['VCDial2'], Btn['VCDial3'],
                Btn['VCDial4'], Btn['VCDial5'], Btn['VCDial6'], Btn['VCDial7'],
                Btn['VCDial8'], Btn['VCDial9'], Btn['VCDialA'], Btn['VCDialG'],
                Btn['VCDelete']],

    'VCOpt'  : [Btn['VCEnviar'], Btn['VCCamara'], Btn['VCAutoAn']],

    'VCPC'   : [Btn['VCHDMI'], Btn['VCVGA'], Btn['VCPTZ'], Btn['VCShare'],
                Btn['VCBack2'], Btn['VCSend'], Btn['VCStop']],

    'VCCam'  : [Btn['VCUp'], Btn['VCLeft'], Btn['VCDown'], Btn['VCRight'],
                Btn['VCZoom1'], Btn['VCZoom2'], Btn['VCLocal'], Btn['VCRemote']],

    'VCPre'  : [Btn['VCP1'], Btn['VCP2'], Btn['VCP3'], Btn['VCP4'],
                Btn['VCP5'], Btn['VCRecall'], Btn['VCSave']],

    'Webex'  : [Btn['WHDMI'], Btn['WVGA'], Btn['WPTZ'], Btn['WShare'],
                Btn['WCisco1'], Btn['WCisco2']],
    
    'TelCall': [Btn['Call'], Btn['Hangup']],

    'TelDial': [Btn['Dial0'], Btn['Dial1'], Btn['Dial2'], Btn['Dial3'],
                Btn['Dial4'], Btn['Dial5'], Btn['Dial6'], Btn['Dial7'],
                Btn['Dial8'], Btn['Dial9'], Btn['DialA'], Btn['DialG'],
                Btn['Delete']],

    'TelOpt' : [Btn['Redial'], Btn['DTMF'], Btn['Hold']],
    
    'Audio1' : [Btn['XHDMI'], Btn['XVGA'], Btn['XShare']],

    'Audio2' : [Btn['XSpkLess'], Btn['XSpkPlus'], Btn['XVCLess'], Btn['XVCPlus']],

    'Audio3' : [Btn['XSpk'], Btn['XVC'], Btn['XMics']],
}

# UI Group Page Buttons
Btn_Group = {
    'Main' : MESet(Btn_Page['Main']),
    
    'VCCam': MESet([Btn['VCLocal'], Btn['VCRemote']]),

    'VCPTZ': MESet([Btn['VCRecall'], Btn['VCSave']]),
}

# UI Button states
Btn_State = {
    'List' : ['Pressed', 'Released', 'Held', 'Repeated', 'Tapped'],
}

# UI Labels
Lbl = {
    'Master'  : Label(TLP, 300),
    'Dial'    : Label(TLP, 116),
    'VCDial'  : Label(TLP, 156),
    'Rec1'    : Label(TLP, 218),
    'Rec2'    : Label(TLP, 219),
    'Rec3'    : Label(TLP, 220),
    'Vaddio1' : Label(TLP, 222),
    'Vaddio2' : Label(TLP, 223),
    'Vaddio3' : Label(TLP, 224),
    'PwrAll'  : Label(TLP, 251),
    'CountAll': Label(TLP, 252),
}

# UI Levels
Lvl = {
    'Spk' : Level(TLP, 195),
    'VC'  : Level(TLP, 196),
}

# UI Popups
Popup = {
    'Video'  : 'Video',
    'LCD1'   : 'Display_L',
    'LCD2'   : 'Display_R',
    'VC'     : 'VC',
    'VC_PC'  : 'VC_Content',
    'VC_Cam' : 'VC_Cam',
    'Webex'  : 'Webex',
    'VoIP'   : 'VoIP',
    'Audio'  : 'Audio',
    'Status' : 'Status',
    'Power'  : 'x_PowerOff',
    'Hi'     : 'x_Welcome',
}

# UI Pages
Page = {
    'Index' : 'Index',
    'Main'  : 'Main'
}