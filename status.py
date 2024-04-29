import json, subprocess, serial, re, rich, rich.console, os
from copy import copy
updated = os.stat('layout.txt').st_mtime
from pprint import pprint as pp
from more_itertools import chunked
layers = list(chunked(open('layout.txt').read().split('\n'), 7))
layers = ['\n'.join(l) for l in layers]
layers = [re.sub(r'([│╰╯─╭╮]+)', r'[bold turquoise2]\1[/]', layer) for layer in layers]
layers = [re.sub(r'([󰆢])', r'[dim]\1[/]', layer) for layer in layers]

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
path = [d['ports'][0]['dev'] for d in devs if '23C7B91420F266DF' == d['serial_num']][0]
ser = serial.Serial(path)
con = rich.console.Console(highlight=False)
con.show_cursor(False)
layer = ''
shortcuts = {
    'C-:    ': 'avy-goto-char',
    'C-h m  ': 'describe-mode',
    'C-h k  ': 'describe-key',
    'C-h i  ': 'info',
    'C-h l  ': 'view-lossage',
    'C-x C-x': 'exchange-point-and-mark',
    'C-c ←  ': 'winner-undo',
    'M-o    ': 'other-window',
    'C-c M-o': 'comint-clear-buffer',
}

while s := ser.readline():
    # zmk: set_layer_state: layer_changed: layer 3 state 0
    # GUIDO: layer 4, new state set: 16
    if m := re.search(r'GUIDO: layer (\d+), new state set: (\d+)', s.decode()):
        state = int(m.group(2))
        n = msb(state)
        layer = layers[n]
        con.clear()
        con.print(layer)

        if os.stat('layout.txt').st_mtime > updated:
            updated = os.stat('layout.txt').st_mtime
            layers = json.load(open('layout.txt'))

    if m := re.search(r'GUIDO: Modifiers set to 0x(\d\d)', s.decode()):
        mods = int(m.group(1), 16)

        modified = copy(layer)
        modline = []
        
        if mods & 0x01:
            modifiers['control']
            modline.append('^')
        if mods &0x02:
            for a, b in modifiers['shift'].items():
                modified = re.sub(a, b, modified)
            modline.append('⇧')
        if mods & 0x04:
            modifiers['option']
            modline.append('⌥')
        if mods & 0x08:
            modifiers['command']
            modline.append('⌘')
        if mods & 0x10:
            modifiers['control']
            modline.append('^')
        if mods &0x20:
            modifiers['shift']
            modline.append('⇧')
        if mods & 0x40:
            modifiers['option']
            modline.append('⌥')
        if mods & 0x80:
            modifiers['command']
            modline.append('⌘')
        con.clear()
        con.print(modified)
        if modline:
            con.print(''.join(modline), justify="center")
        else:
            con.print('---', justify="center")
    else:
        con.print('---', justify="center")

    con.print('\n'.join((f'{k}  {v}' for k, v in shortcuts.items())))
