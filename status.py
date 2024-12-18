import json, subprocess, serial, re, rich, rich.console, os, sys, time
from copy import copy
from pprint import pprint as pp
from more_itertools import chunked
updated = os.stat('status-layout.txt').st_mtime

POSITIONS = """
 ╭────────────────────────────────────────────────────────────────╮
 │                                                    │
 │     a    s    d    f                j    k    l    :       │
 │                                                    │
 │                                                            │
 │               󰆢    󰆢                󰆢    󰆢                 │
 ╰────────────────────────────────────────────────────────────────╯
"""


def load_layers():
    layers = list(chunked(open('status-layout.txt').read().split('\n'), 7))
    layers = ['\n'.join([s[:67] for s in l]) for l in layers]
    layers = [re.sub(r'([│╰╯─╭╮]+)', r'[bold turquoise2]\1[/]', layer) for layer in layers]
    layers = [re.sub(r'([󰆢])', r'[dim]\1[/]', layer) for layer in layers]
    return layers

layers = load_layers()

modifiers = {
    'shift': {
        ' ([abcdefghijklmnopqrstuvwxyz]) ': lambda m: f' {m.group(1).upper()} ',
    },
    'command': {
    },
    'control': {},
    'option': {},
}

# Cool colors:
#    [cyan]
#    [bold cyan]
#    [bold magenta1]
#    [bold green1]
#    [bold turquoise2]
#    [turquoise2]

def msb(n):
    "What is the most significant bit set (also, what is the highest layer set)"
    if not n:
        return 0
    i = 0
    while n:
        n = n >> 1
        i += 1
    return i - 1

p = subprocess.run(['/Users/guido/miniforge3/bin/discotool', 'json'], capture_output=True)
devs = json.loads(p.stdout)
#path = [d['ports'][0]['dev'] for d in devs if '23C7B91420F266DF' == d['serial_num']][0]
path = [d['ports'][0]['dev'] for d in devs if 'DF6114B5C3791031' == d['serial_num']][0]
ser = serial.Serial(path)
con = rich.console.Console(highlight=False)
if len(sys.argv) > 1 and sys.argv[1] == '-v':
    while s := ser.readline():
        print(s.decode().strip())
        
con.show_cursor(False)
layer = ''
shortcuts = {
#    'C-:    ': 'avy-goto-char',
#    'C-h m  ': 'describe-mode',
#    'C-h k  ': 'describe-key',
#    'C-h i  ': 'info',
#    'C-h l  ': 'view-lossage',
#    'C-x C-x': 'exchange-point-and-mark',
#    'C-c ←  ': 'winner-undo',
#    'M-o    ': 'other-window',
#    'C-c M-o': 'comint-clear-buffer',
}

# TODO: OSError when restarted this, we know this is going to happen when
#       we press the bootloader combo so maybe we should ancticipate this
#       and check until it's working.
#
#       It would also be cool if the script would watch for the download
#       Unzip it and copy it over.
while True:
    try:
        while s := ser.readline():
            # zmk: set_layer_state: layer_changed: layer 3 state 0
            # GUIDO: layer 4, new state set: 16
            if m := re.search(r'GUIDO: layer (\d+), new state set: (\d+)', s.decode()):
                state = int(m.group(2))
                n = msb(state)
                layer = layers[n]
                con.clear()
                con.print(layer)
                con.print('\n'.join((f'{k}  {v}' for k, v in shortcuts.items())))
        
                if os.stat('status-layout.txt').st_mtime > updated:
                    updated = os.stat('status-layout.txt').st_mtime
                    layers = load_layers()
        
            if m := re.search(r'GUIDO: Modifiers set to 0x(\d\d)', s.decode()):
                mods = int(m.group(1), 16)
        
                modified = copy(layer)
                modline = []
                
                if mods & 0x01:
                    modifiers['control']
                    modline.append('Control')
                if mods &0x02:
                    for a, b in modifiers['shift'].items():
                        modified = re.sub(a, b, modified)
                    modline.append('Shift')
                if mods & 0x04:
                    modifiers['option']
                    modline.append('Option')
                if mods & 0x08:
                    modifiers['command']
                    modline.append('Command')
                if mods & 0x10:
                    modifiers['control']
                    modline.append('Control')
                if mods &0x20:
                    modifiers['shift']
                    modline.append('Shift')
                if mods & 0x40:
                    modifiers['option']
                    modline.append('Option')
                if mods & 0x80:
                    modifiers['command']
                    modline.append('Command')
                con.clear()
                con.print(modified)
                if modline:
                    con.print(' '.join(modline), justify="center")
                else:
                    con.print('---', justify="center")
            #else:
            #    con.print('---', justify="center")
    except serial.serialutil.SerialException as e:
        print('Shutting down because keyboard was unplugged...')
        ser = None
        while not ser:
            try:
                ser = serial.Serial(path)
            except serial.serialutil.SerialException as e:
                time.sleep(1)
    except Exception as e:
        print('Shutting down...')
        print(type(e), e)
        
con.show_cursor(True)
