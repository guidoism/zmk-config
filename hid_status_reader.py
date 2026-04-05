"""
Read keyboard status reports from ZMK raw HID interface.

Requires: pip install hidapi

Report format (first 4 bytes of 32-byte report):
  byte 0: report ID (0x01 = status update)
  byte 1-2: layer state (16-bit bitset, little-endian)
  byte 3: flags (bit 0 = caps_word active)
"""

import hid
import sys
import time

# zmk-raw-hid defaults
USAGE_PAGE = 0xFF60
USAGE = 0x61

LAYER_NAMES = {
    0: "BASE",
    1: "NUM/SYM",
    2: "BRACKETS",
    3: "NAV",
    4: "WINMGMT",
    5: "SPANISH",
    6: "SPECIAL",
    7: "(empty)",
    8: "BOXDRAW",
    9: "FKEYS",
}


def find_device():
    """Find the raw HID device by usage page and usage."""
    for dev in hid.enumerate():
        if dev["usage_page"] == USAGE_PAGE and dev["usage"] == USAGE:
            return dev
    return None


def active_layers(state):
    """Return list of active layer numbers from a bitset."""
    layers = []
    for i in range(16):
        if state & (1 << i):
            layers.append(i)
    return layers


def main():
    print("Searching for ZMK raw HID device...")
    dev_info = find_device()
    if not dev_info:
        print("Device not found. Is the keyboard plugged in?")
        print("\nAvailable HID devices:")
        for d in hid.enumerate():
            if d["usage_page"] > 0xFF00:
                print(f"  {d['manufacturer_string']} {d['product_string']} "
                      f"usage_page=0x{d['usage_page']:04X} usage=0x{d['usage']:04X}")
        sys.exit(1)

    print(f"Found: {dev_info['manufacturer_string']} {dev_info['product_string']}")
    print(f"  Path: {dev_info['path']}")
    print(f"  Usage: 0x{dev_info['usage_page']:04X}/0x{dev_info['usage']:04X}")
    print()

    device = hid.device()
    device.open_path(dev_info["path"])
    device.set_nonblocking(False)

    print("Listening for status reports... (Ctrl+C to quit)\n")

    try:
        while True:
            data = device.read(64, timeout_ms=5000)
            if not data:
                continue

            if data[0] != 0x01:
                print(f"Unknown report ID: 0x{data[0]:02X}, data: {data[:8]}")
                continue

            layer_state = data[1] | (data[2] << 8)
            caps_word = bool(data[3] & 0x01)
            layers = active_layers(layer_state)
            layer_names = [LAYER_NAMES.get(l, f"L{l}") for l in layers]

            status = f"Layers: {' + '.join(layer_names) or 'NONE'}"
            if caps_word:
                status += "  [CAPS WORD]"

            print(f"\r{status:<60}", end="", flush=True)

    except KeyboardInterrupt:
        print("\n\nDone.")
    finally:
        device.close()


if __name__ == "__main__":
    main()
