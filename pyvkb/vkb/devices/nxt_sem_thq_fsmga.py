from vkb import led
from .base import VKBDevice


# TODO: refactor this into something more elegant. This was just kinda add things as you thought of 'em kinda dev


class NXT_SEM_THQ_FSMGA(VKBDevice):
    PRODUCT_ID = 0x2234

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

    ALL_LEDS = [
        LED_THQ_MD, 
        LED_SEM_A1,
        LED_SEM_A2,
        LED_SEM_B1,
        LED_SEM_B2,
        LED_SEM_B3,
        LED_SEM_GL,
        LED_SEM_GF,
        LED_SEM_GR,
        LED_FSM_L1,
        LED_FSM_L2,
        LED_FSM_L3,
        LED_FSM_L4,
        LED_FSM_R1,
        LED_FSM_R2,
        LED_FSM_R3,
        LED_FSM_R4,
        LED_FSM_AP,
        LED_FSM_FD,
        LED_FSM_YD,
        LED_FSM_VS,
    ]

    @property
    def led_top(self):
        return self.get_led(self.LED_TOP)

    @led_top.setter
    def led_top(self, color1):
        self.set_led(
            self.LED_TOP,
            color1=color1,
            color_mode=led.ColorMode.COLOR1,
            led_mode=led.LEDMode.CONSTANT,
        )

    @property
    def led_base(self):
        return self.get_led(self.LED_BASE)

    @led_base.setter
    def led_base(self, color):
        vc = led.hex_color_to_vkb_color(color)
        self.set_led(
            self.LED_BASE,
            color1=color,
            color_mode=led.ColorMode.COLOR1,
            led_mode=led.LEDMode.CONSTANT,
        )

    @property
    def led_pov(self):
        return self.get_led(self.LED_POV)

    @led_pov.setter
    def led_pov(self, color1):
        self.set_led(
            self.LED_POV,
            color1=color1,
            color_mode=led.ColorMode.COLOR1,
            led_mode=led.LEDMode.CONSTANT,
        )
