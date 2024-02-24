import pyglet.input

import pywinusb.hid

VENDOR_ID = 0x231D

LED_CONFIG_COUNT = 12
LED_REPORT_ID = 0x59
LED_REPORT_LEN = 129
LED_SET_OP_CODE = bytes.fromhex("59a50a")

device_list = pyglet.input.get_devices()

print(device_list)

for _ in device_list:
    print(_)
    print(_.get_guid())
    
    
hid_device_list = pywinusb.hid.HidDeviceFilter(vendor_id=VENDOR_ID).get_devices()

print(hid_device_list)

hid_device = hid_device_list[0]

print(hid_device.device_path)

hid_device.open()

led_report = [
    _ for _ in hid_device.find_feature_reports() if _.report_id == LED_REPORT_ID
][0]

print(led_report)

