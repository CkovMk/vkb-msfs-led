import pyglet.input

import pywinusb.hid

from SimConnect import *
from SimConnect.Enum import *
from SimConnect.RequestList import Request
from SimConnect.Attributes import SimConnectDll

#VENDOR_ID = 0x231D
#
#LED_CONFIG_COUNT = 12
#LED_REPORT_ID = 0x59
#LED_REPORT_LEN = 129
#LED_SET_OP_CODE = bytes.fromhex("59a50a")
#
#device_list = pyglet.input.get_devices()
#
#print(device_list)
#
#for _ in device_list:
#    print(_)
#    print(_.get_guid())
#    
#    
#hid_device_list = pywinusb.hid.HidDeviceFilter(vendor_id=VENDOR_ID).get_devices()
#
#print(hid_device_list)
#
#hid_device = hid_device_list[0]
#
#print(hid_device.device_path)
#
#hid_device.open()
#
#led_report = [
#    _ for _ in hid_device.find_feature_reports() if _.report_id == LED_REPORT_ID
#][0]
#
#print(led_report)

sm = SimConnect()

#sm.dll.AddToDataDefinition(
#	sm.hSimConnect, 0x10201, b"L:IS_MENU_ACTIVE", b'Bool',
#    SIMCONNECT_DATATYPE.SIMCONNECT_DATATYPE_FLOAT64, 0.5, 0
#)
#
#sm.dll.AddToDataDefinition(
#	sm.hSimConnect, 0x10202, b"L:WTAP_Vnav_State", b'Bool',
#    SIMCONNECT_DATATYPE.SIMCONNECT_DATATYPE_FLOAT64, 0.5, 0
#)

key = ["True if autopilot vertical hold applied", b'AUTOPILOT VERTICAL HOLD', b'Bool', 'N']
req = Request((key[1], key[2]), sm, _dec = key[0], _settable=False)
print(req)
print(req.get())

key = ["True if menu is active", b'L:IS_MENU_ACTIVE', b'Bool', 'N']
req = Request((key[1], key[2]), sm, _dec = key[0], _settable=False)
print(req)
print(req.get())

key = ["True Vnav enabled", b'L:WTAP_Vnav_State', b'Bool', 'N']
req = Request((key[1], key[2]), sm, _dec = key[0], _settable=False)
print(req)
print(req.get())

req = Request((b'L:WTAP_GP_Approach_Mode', b'Bool'), sm, _dec = "Garmin VNAV GP Status", _settable=False)
print(req)
print(req.get())
