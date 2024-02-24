import sys
import pywinusb.hid as hid

from vkb.devices.defs import VKB_DEVICES, VENDOR_ID


def find_all_vkb():
    """ Returns all VKB devices connected to the system sorted by GUID """
    # cheat with device_path as "guid" and get rid of pyglet & dinput.

    devices = []
    for hiddev in hid.HidDeviceFilter(vendor_id=VENDOR_ID).get_devices():
        devcls = VKB_DEVICES.get(hiddev.product_id)
        if devcls is not None:
            devices.append(
                devcls(
                    hiddev,
                    guid=hiddev.device_path,
                )
            )
    return sorted(devices, key=lambda d: d.guid)
