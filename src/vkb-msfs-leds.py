import logging
from SimConnect import *
from SimConnect.Enum import *
from SimConnect.RequestList import Request
from time import sleep

from vkb.devices import find_all_vkb
from vkb import led

vkb_inst = find_all_vkb()[1]

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)
LOGGER.info("START")

sm = SimConnect()
aq = AircraftRequests(sm)
ae = AircraftEvents(sm)

### BEGIN THQ_SEM_FSM

LED_THQ_MD = 0

LED_SEM_A1 = 10
LED_SEM_A2 = 11
LED_SEM_B1 = 12
LED_SEM_B2 = 13
LED_SEM_B3 = 14

LED_SEM_GL = 15
LED_SEM_GF = 16
LED_SEM_GR = 17

LED_FSM_L1 = 18
LED_FSM_L2 = 19
LED_FSM_L3 = 20
LED_FSM_L4 = 21
LED_FSM_R1 = 22
LED_FSM_R2 = 23
LED_FSM_R3 = 24
LED_FSM_R4 = 25

LED_FSM_AP = 26
LED_FSM_FD = 27
LED_FSM_YD = 28
LED_FSM_VS = 29

### END THQ_SEM_FSM

################################
# Simvar reference enum
################################

################################################################################
# Enum                  # Value             # Usage         # Description

# @group "Default SimVar"
# @{

# Autopilot Status
# @val 0.0: Disabled
# @val 1.0: Enabled
SIMVAR_S_AP_EN          = 100
SIMVAR_S_AP_FD          = 101
SIMVAR_S_AP_YD          = 102

# Landing Gear
# @val 0.0: Retracted
# @val 1.0: Extended
SIMVAR_S_GEAR_L         = 310
SIMVAR_S_GEAR_C         = 311
SIMVAR_S_GEAR_R         = 312

# Parking Brake
# @val 0.0: Disabled
# @val 1.0: Enabled
SIMVAR_S_PBRAKE         = 315

# Autopilot Vertical Modes
SIMVAR_S_AP_PIT         = 120                                # Not used
SIMVAR_S_AP_ALT         = 121               # ALT=[G]
SIMVAR_S_AP_LVL         = 122               # LVL=[G]
SIMVAR_S_AP_FLC         = 123               # FLC=[G]
SIMVAR_S_AP_GS          = 124               #               # Buggy?

# Autopilot Horizontal Modes
SIMVAR_S_AP_ROL         = 150               #               # Not used
SIMVAR_S_AP_HDG         = 151               # HDG=[G]
SIMVAR_S_AP_VS          = 152               # VS =[G]
SIMVAR_S_AP_NAV         = 153               # NAV_ON        # NAV Enabled, can be either locked or armed.
SIMVAR_S_AP_LOC         = 154               # NAV_ON

# @}
# endgroup "Default SimVar"

# @group "WTAP LVar"
# @{

# Autopilot WT1000 Present
# @val 0.0: No
# @val 1.0: Yes
SIMVAR_WTAP_WT1000      = 1001              #               # Enables WTAP logic

# Vnav State
# @val 0.0: Disabled
# @val 1.0: Enabled_Inactive                # VNV_OFF
# @val 2.0: Enabled_Active                  # VNV_ON
SIMVAR_WTAP_VNV         = 1120

# Vnav Path Mode
# @val 0.0: None
# @val 1.0: Path_Armed                      # VNV={Y}
# @val 2.0: Path_Active                     # VNV={G}
# @val 3.0: Path_Invalid
SIMVAR_WTAP_VNV_PATH    = 1121

# Approach Guidance Mode
# @val 0.0: None                            # APR_OFF
# @val 1.0: GS_Armed (ILS)                  # APR=[Y]
# @val 2.0: GS_Active(ILS)                  # APR=[G]
# @val 3.0: GP_Armed (RNAV)                 # APR=[Y]
# @val 4.0: GP_Active(RNAV)                 # APR=[G]
SIMVAR_WTAP_GP_Mode     = 1122

# Lnav Is Tracking
# @val 0.0: Lnav_Not_Tracking               # NAV={Y}
# @val 1.0: Lnav_Is_Tracking                # NAV={G}
SIMVAR_WTAP_NAV_TRK     = 1150

# @}
# endgroup "WTAP LVar"

# @group "SF50 LVar"
# @{

# SF50 Auto Throttle
# @var ???: AT_OFF
# @var ???: AT_FMS
# @var 3.0: AT_MAN
SIMVAR_SF50_AT_STATUS   = 2000              

# @}
# endgroup "SF50 LVar"






################################################################################

################################
# Simvar reference map
################################

SC_SimvarRefMap = {
    ######## AutoPilot Master ########
    SIMVAR_S_AP_EN   :   aq.find('AUTOPILOT_MASTER'),                        #                                       #
    SIMVAR_S_AP_FD   :   aq.find('AUTOPILOT_FLIGHT_DIRECTOR_ACTIVE'),        #
    SIMVAR_S_AP_YD   :   aq.find('AUTOPILOT_YAW_DAMPER'),                    #
    
    ######## Landing Gear ########
    SIMVAR_S_GEAR_L  :   aq.find('GEAR_LEFT_POSITION'),                      #
    SIMVAR_S_GEAR_C  :   aq.find('GEAR_CENTER_POSITION'),                    #
    SIMVAR_S_GEAR_R  :   aq.find('GEAR_RIGHT_POSITION'),                     #
    
    SIMVAR_S_PBRAKE  :   aq.find('BRAKE_PARKING_POSITION'),                  #
    
    ######## Autopilot Function ########
    SIMVAR_S_AP_LVL  :   aq.find('AUTOPILOT_WING_LEVELER'),
    SIMVAR_S_AP_PIT  :   aq.find('AUTOPILOT_PITCH_HOLD'),
    SIMVAR_S_AP_ROL  :   aq.find('AUTOPILOT_ATTITUDE_HOLD'),
    SIMVAR_S_AP_HDG  :   aq.find('AUTOPILOT_HEADING_LOCK'),
    SIMVAR_S_AP_VS   :   aq.find('AUTOPILOT_VERTICAL_HOLD'),
    SIMVAR_S_AP_FLC  :   aq.find('AUTOPILOT_FLIGHT_LEVEL_CHANGE'),
    SIMVAR_S_AP_ALT  :   aq.find('AUTOPILOT_ALTITUDE_LOCK'),
    SIMVAR_S_AP_NAV  :   aq.find('AUTOPILOT_NAV1_LOCK'),
    SIMVAR_S_AP_LOC  :   aq.find('AUTOPILOT_APPROACH_HOLD'),
    SIMVAR_S_AP_GS   :   aq.find('AUTOPILOT_GLIDESLOPE_HOLD'),
    SIMVAR_WTAP_WT1000 : Request((b'L:WT1000_AP_G1000_INSTALLED', b'Bool'),
        sm, _dec = "WT1000 Is Present", _settable=False),
    SIMVAR_WTAP_VNV  :   Request((b'L:WTAP_Vnav_State', b'Number'),
        sm, _dec = "WTAP VNAV State", _settable=False),
    SIMVAR_WTAP_GP_Mode  :   Request((b'L:WTAP_GP_Approach_Mode', b'Number'),
        sm, _dec = "WTAP VNAV GP Status", _settable=False),
    SIMVAR_WTAP_NAV_TRK: Request((b'L:WTAP_LNav_Is_Tracking', b'Bool'),
        sm, _dec = "WTAP VNAV State", _settable=False),
    SIMVAR_WTAP_VNV_PATH: Request((b'L:WTAP_Vnav_Path_Mode', b'Number'),
        sm, _dec = "WTAP VNAV Path Mode", _settable=False),
    SIMVAR_SF50_AT_STATUS: Request((b'L:SF50_Autothrottle_Status', b'Number'),
        sm, _dec = "SF50 AT Status", _settable=False),    
}

################################
# Simvar data update every cycle
################################
SC_SimvarData = {}

################################
# VKB LED reference map
################################
VKB_LedRefMap = {
    LED_FSM_AP: [SIMVAR_S_AP_EN],                                               # AP
    LED_FSM_FD: [SIMVAR_S_AP_FD],                                               # FD
    LED_FSM_YD: [SIMVAR_S_AP_YD],                                               # YD
    LED_FSM_VS: [SIMVAR_S_AP_VS],                                               # VS
    LED_FSM_L1: [SIMVAR_S_AP_HDG],                                              # HDG
    LED_FSM_L2: [],
    LED_FSM_L3: [SIMVAR_S_AP_NAV, SIMVAR_S_AP_LOC, SIMVAR_S_AP_ROL, SIMVAR_S_AP_HDG,             # NAV / LOC
        SIMVAR_WTAP_WT1000, SIMVAR_WTAP_NAV_TRK],
    LED_FSM_L4: [                                                               # APR / GS
        SIMVAR_WTAP_WT1000, SIMVAR_WTAP_GP_Mode],
    LED_FSM_R1: [SIMVAR_S_AP_ALT, SIMVAR_S_AP_VS, SIMVAR_S_AP_FLC],             # ALT
    LED_FSM_R2: [SIMVAR_S_AP_LVL],                                              # LVL
    LED_FSM_R3: [                                                               # VNV, testing
        SIMVAR_WTAP_WT1000, SIMVAR_WTAP_VNV, SIMVAR_WTAP_VNV_PATH], 
    LED_FSM_R4: [SIMVAR_S_AP_FLC],                                              # FLC / IAS
    LED_SEM_GL: [SIMVAR_S_GEAR_L, SIMVAR_S_PBRAKE],
    LED_SEM_GF: [SIMVAR_S_GEAR_C, SIMVAR_S_PBRAKE],
    LED_SEM_GR: [SIMVAR_S_GEAR_R, SIMVAR_S_PBRAKE], 
}


################################
# VKB LED status data, generate by logic
################################
VKB_LedCfgData = []

################################
# VKB LED update data, update every cycle
################################
VKB_LedStatus = {}

################################
# VKB LED initial config
# Disable all LEDs and record status
################################
for led_key, led_ref in VKB_LedRefMap.items() :
    if   0 != len(led_ref) :
        led_cfg = led.LEDConfig(led_key, led.ColorMode.COLOR1, led.LEDMode.OFF, '#000', '#000')
        VKB_LedCfgData.append(led_cfg)
        VKB_LedStatus[led_key] = led_cfg
vkb_inst.update_leds(VKB_LedCfgData)


sleep(1)

################################
# Auto handle VKB LED update logic
################################
def VKB_UpdateLedCfgData( led_cfg ) :
    if VKB_LedStatus[led_cfg.led] != led_cfg :
        VKB_LedCfgData.append(led_cfg)
        VKB_LedStatus[led_cfg.led] = led_cfg

################################
# Main loop begin
################################
while not sm.quit :
    
    # Clear cfg data
    VKB_LedCfgData = []
    
    # update simvars from MSFS
    for sc_key, sc_ref in SC_SimvarRefMap.items() :
        if   None != sc_ref :
            SC_SimvarData[sc_key] = sc_ref.get()
        else:
            print("[E] Simvar key={}, ref={} not found !".format(sc_key, sc_ref))
            SC_SimvarData[sc_key] = 0.0
    
    #print(aq.find('AVIONICS_MASTER_SWITCH').get())
    #ELECTRICAL_MASTER_BATTERY
    #print(aq.find('AVIONICS_MASTER_SWITCH').get())
    
    ################################
    # Only enable LEDs w/ avionics power
    ################################
    if   1.0 == aq.find('AVIONICS_MASTER_SWITCH').get():
        # enable led control
        #print("flush")
        
        for led_key, led_ref in VKB_LedRefMap.items() :
            
            # LED control disabled:
            if   0 == len(led_ref) :
                None
             
            ################################
            # LED control custom logic:
            ################################
            
            # Landing Gear
            elif (LED_SEM_GL <= led_key) & (LED_SEM_GR >= led_key) :
                if   0.0 == SC_SimvarData[led_ref[0]] : # gear is up
                    VKB_UpdateLedCfgData(led.LEDConfig(led_key, led.ColorMode.COLOR2, led.LEDMode.CONSTANT, '#000', '#fff'))
                elif (1.0 == SC_SimvarData[led_ref[0]]) & (0.0 == SC_SimvarData[led_ref[1]]) : # gear is down, parking brake off
                    VKB_UpdateLedCfgData(led.LEDConfig(led_key, led.ColorMode.COLOR1, led.LEDMode.CONSTANT, '#777', '#000'))
                elif (1.0 == SC_SimvarData[led_ref[0]]) & (1.0 == SC_SimvarData[led_ref[1]]) : # gear is down, parking brake on
                    VKB_UpdateLedCfgData(led.LEDConfig(led_key, led.ColorMode.COLOR1_p_2, led.LEDMode.CONSTANT, '#444', '#fff'))
                else : # gear in transit
                    VKB_UpdateLedCfgData(led.LEDConfig(led_key, led.ColorMode.COLOR1_p_2, led.LEDMode.FAST_BLINK, '#444', '#fff'))

            # NAV
            elif LED_FSM_L3 == led_key :
                #print("NAV")
                #print(SC_SimvarData[led_ref[0]])
                #print(SC_SimvarData[led_ref[1]])
                #print(SC_SimvarData[led_ref[2]])
                #print(SC_SimvarData[led_ref[3]])
                #print(SC_SimvarData[led_ref[4]])
                #print(SC_SimvarData[led_ref[5]])

                if ((1.0 == SC_SimvarData[led_ref[4]]) & (1.0 == SC_SimvarData[led_ref[5]])) : # WTAP: Lnav_Is_Tracking, [G]
                    VKB_UpdateLedCfgData(led.LEDConfig(led_key, led.ColorMode.COLOR1, led.LEDMode.CONSTANT, '#777', '#000'))
                    print("WT_LNAV")
                elif ((1.0 == SC_SimvarData[led_ref[0]]) | (1.0 == SC_SimvarData[led_ref[1]])) : # NAV enabled.
                    if ((1.0 == SC_SimvarData[led_ref[2]]) | (1.0 == SC_SimvarData[led_ref[3]])) : # NAV armed, [Y]
                        VKB_UpdateLedCfgData(led.LEDConfig(led_key, led.ColorMode.COLOR1_p_2, led.LEDMode.CONSTANT, '#444', '#fff'))
                    else : # NAV Locked [G]
                        VKB_UpdateLedCfgData(led.LEDConfig(led_key, led.ColorMode.COLOR1, led.LEDMode.CONSTANT, '#777', '#000'))
                else : # NAV disabled, [X]
                    VKB_UpdateLedCfgData(led.LEDConfig(led_key, led.ColorMode.COLOR1, led.LEDMode.OFF, '#000', '#000'))

            # APR
            elif LED_FSM_L4 == led_key :
                #print("APR")
                #print(SC_SimvarData[led_ref[0]])
                #print(SC_SimvarData[led_ref[1]])
                #print(SC_SimvarData[led_ref[2]])
                #print(SC_SimvarData[led_ref[3]])
                
                if (1.0 == SC_SimvarData[led_ref[0]]) : # WTAP is present
                    if ((1.0 == SC_SimvarData[led_ref[1]]) | (3.0 == SC_SimvarData[led_ref[1]])) : # WTAP: Armed, [Y]
                        VKB_UpdateLedCfgData(led.LEDConfig(led_key, led.ColorMode.COLOR1_p_2, led.LEDMode.CONSTANT, '#444', '#fff'))
                    elif ((2.0 == SC_SimvarData[led_ref[1]]) | (4.0 == SC_SimvarData[led_ref[1]])) : # WTAP: Locked, [G]
                        VKB_UpdateLedCfgData(led.LEDConfig(led_key, led.ColorMode.COLOR1, led.LEDMode.CONSTANT, '#777', '#000'))
                    else : # WTAP: OFF, [X]
                        VKB_UpdateLedCfgData(led.LEDConfig(led_key, led.ColorMode.COLOR1, led.LEDMode.OFF, '#000', '#000'))

                #if  1.0 == SC_SimvarData[led_ref[1]] : # GS enabled.
                #    if   1.0 == SC_SimvarData[led_ref[2]] : # GS armed.
                #        VKB_UpdateLedCfgData(led.LEDConfig(led_key, led.ColorMode.COLOR1_p_2, led_l4_mode, '#444', '#fff'))
                #    elif 1.0 == SC_SimvarData[led_ref[3]] : # GS captured.
                #        VKB_UpdateLedCfgData(led.LEDConfig(led_key, led.ColorMode.COLOR1, led_l4_mode, '#777', '#000'))
                else : # Fallback to default, GS disabled.
                    VKB_UpdateLedCfgData(led.LEDConfig(led_key, led.ColorMode.COLOR1, led.LEDMode.OFF, '#000', '#000')) 
                
            # ALT
            elif LED_FSM_R1 == led_key:
                #print("ALT")
                #print(SC_SimvarData[led_ref[0]])
                #print(SC_SimvarData[led_ref[1]])
                #print(SC_SimvarData[led_ref[2]])
                #print(SC_SimvarData[led_ref[3]])
                
                if 1.0 == SC_SimvarData[led_ref[0]] : # ALT captured.
                    VKB_UpdateLedCfgData(led.LEDConfig(led_key, led.ColorMode.COLOR1, led.LEDMode.CONSTANT, '#777', '#000'))
                elif (1.0 == SC_SimvarData[led_ref[1]]) | (1.0 == SC_SimvarData[led_ref[2]]) : # ALT armed, temporarily solution.
                    VKB_UpdateLedCfgData(led.LEDConfig(led_key, led.ColorMode.COLOR1_p_2, led.LEDMode.CONSTANT, '#444', '#fff'))
                else : # ALT disabled.
                    VKB_UpdateLedCfgData(led.LEDConfig(led_key, led.ColorMode.COLOR1, led.LEDMode.OFF, '#000', '#000'))
            
            # VNV
            # TODO: Test this!!!
            elif LED_FSM_R1 == LED_FSM_R3 :
                if (1.0 == SC_SimvarData[led_ref[0]]) : # WTAP is present
                    if (2.0 == SC_SimvarData[led_ref[1]]) : # WTAP: VNV Active
                        if (1.0 == SC_SimvarData[led_ref[2]]) : # WTAP: VNV Armed, [Y]
                            VKB_UpdateLedCfgData(led.LEDConfig(led_key, led.ColorMode.COLOR1_p_2, led.LEDMode.CONSTANT, '#444', '#fff'))
                        elif (2.0 == SC_SimvarData[led_ref[2]]) : # WTAP: VNV Locked, [G]
                            VKB_UpdateLedCfgData(led.LEDConfig(led_key, led.ColorMode.COLOR1, led.LEDMode.CONSTANT, '#777', '#000'))
                    else : # WTAP: VNV Disabled, [X]
                        VKB_UpdateLedCfgData(led.LEDConfig(led_key, led.ColorMode.COLOR1, led.LEDMode.OFF, '#000', '#000'))
                else : # Fallback to default, VNV disabled, [X]
                    VKB_UpdateLedCfgData(led.LEDConfig(led_key, led.ColorMode.COLOR1, led.LEDMode.OFF, '#000', '#000')) 
                
                
            # LED control direct map:
            elif 1 == len(led_ref) :
                if   0.0 == SC_SimvarData[led_ref[0]]: # Disabled.
                    VKB_UpdateLedCfgData(led.LEDConfig(led_key, led.ColorMode.COLOR1, led.LEDMode.OFF, '#000', '#000'))
                else : # Enabled.
                    VKB_UpdateLedCfgData(led.LEDConfig(led_key, led.ColorMode.COLOR1, led.LEDMode.CONSTANT, '#777', '#000'))

    ################################
    # Disable all LEDs w/o avionics power
    ################################ 
    else:
        for led_key, led_ref in VKB_LedRefMap.items():
            if   0 != len(led_ref):
                VKB_UpdateLedCfgData(led.LEDConfig(led_key, led.ColorMode.COLOR1, led.LEDMode.OFF, '#000', '#000'))
    
    ################################
    # Finally write all changes to device
    ################################ 
    if VKB_LedCfgData:
        vkb_inst.update_leds(VKB_LedCfgData)
        
        # Clear cfg data (again)
        VKB_LedCfgData = []

    # sleep(0.2)
