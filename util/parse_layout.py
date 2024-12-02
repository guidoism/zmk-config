"""The motivation for this is that I want a text-based keymap format
that is easy to understand, can be edited quickly, can be used for
displaying what my keyboard's current layer means, and should be
easily transformed into other formats for creating firmware or display
on webpages.
"""

import re, unicodedata, yaml, sys, collections
from pprint import pprint as pp
from itertools import chain
from more_itertools import split_into, transpose, flatten, divide

if len(sys.argv) != 5:
    print(f'Usage: {sys.argv[0]} [drawing|firmware|status] columns rows thumbs')

outtype = sys.argv[1]
columnslen, rowslen, thumbslen = map(int, sys.argv[2:])

assert columnslen in {5, 6}
assert rowslen    in {3}
assert thumbslen  in {3, 4}

config = {
    'layout': {
        'ortho_layout': {
            'split': True,
            'columns': columnslen,
            'rows': rowslen,
            'thumbs': thumbslen,
        },
    },
    'draw_config': {
        'n_columns': 2,
        'append_colon_to_layer_header': False,
    },
    'layers': {
    },
    'combos': [
    ],
}

layers = open('layout.txt').read()
combos = open('combos.txt').read()

keycodes = dict(k.strip().split('\t') for k in open('keycodes.tsv'))
drawingcodes = {
    '󰘴f': {'t': 'f', 'h': 'CTRL'},
    '󰘴j': {'t': 'j', 'h': 'CTRL'},
    '󰘶󱁐': {'t': '$$mdi:keyboard-space$$', 'h': 'SHIFT'},
    '󰆢': '',
    '󰿦': {'type': 'ghost'},
    '': {'type': 'held'},
    'L←': '$$mdi:chevron-double-left$$',
    'L→': '$$mdi:chevron-double-right$$',
    'P↑': 'PGUP',
    'P↓': 'PGDN',
}

# │ESC   󰆢    󰆢   ¶←   ¶→    󰆢       ESC  P↑    ↑   P↓    󰆢    󰆢   │
# │ 󰆢    󰆢    󰆢   W←   W→    󰆢       BS    ←    ↓    →    󰞷    󰆢   │


def split(s):
    return re.findall(r'\n?(.╭─+╮.+?╰─+╯)\w*', s, re.S)

def extract_middle(s):
    "Split apart into index, name, and list of rows"
    lines = s.splitlines()
    top, middle, bottom = lines[0], lines[1:-1], lines[-1]
    column_sizes = list(map(len, re.search(r'(.*╭)(─+)(╮.*)', top).groups()))
    column_sizes[-1] = None # This make sure split_into returns the rest of the string
    # This splits the lines into prefix, body, suffix and then puts
    # the prefixes together, bodies togethers, and suffixes together.
    columns = [list(map(''.join, split_into(s, column_sizes))) for s in middle]
    segments = list(transpose(columns)) # transpose is awesome!
    index = ''.join([s.strip(' │') for s in segments[0]])
    name = ''.join([s.strip(' │') for s in segments[2]]) or f'layer_{i}'
    rows = [s.split() for s in segments[1]]
    return index, name, rows

def whittle_down(rows):
    "Remove rows and columns based on intended keyboard size"
    del rows[3] # We've given up on this row of thumb keys, too many keys clanky!
    if columnslen == 5:
        rows = [r[1:-1] for r in rows[:3]] + rows[3:]
    if thumbslen == 3:
        rows = rows[:3] + [rows[3][:3] + rows[3][-3:]]
    return rows

for i, s in enumerate(split(combos)):
    index, name, rows = extract_middle(s)
    rows = whittle_down(rows)
    name, separate, action = re.match(r'(\w+)(\*?)\((.+)\)', name).groups()
    layer = 'ALL'
    keysdown = [i for i, k in enumerate(flatten(rows)) if k == '']
    if outtype == 'firmware':
        keysdown = ' '.join(map(str, keysdown))
        print(f"ZMK_COMBO({name.lower()}_combo, {action}, {keysdown}, {layer}, 50)")
    elif outtype == 'drawing':
        d = {
            'p': keysdown,
            'k': name,
            'l': ['BASE'],
            'draw_separate': bool(separate),
        }
        config['combos'].append(d)

for i, s in enumerate(split(layers)):
    index, name, rows = extract_middle(s)
    rows = whittle_down(rows)
    if outtype == 'firmware':
        rows = [[keycodes[k] for k in r] for r in rows]
        maxlen = min(15, max([max(map(len, r)) for r in rows]))
        rows = [[k.ljust(maxlen) for k in r] for r in rows]
        layer = '\n '.join(map(' '.join, rows))
        print(f"ZMK_LAYER({name},\n {layer})")
    elif outtype == 'drawing':
        config['layers'][name] = [[drawingcodes.get(k, k) for k in r] for r in rows]
    elif outtype == 'status':
        rows.insert(3, [])
        width = columnslen * 2 * 5
        print(' ╭' + '─' * (width+5) + '╮')
        for j, row in enumerate(rows):
            prefix = f'{i}│' if j == 2 else ' │'
            middle = (''.join([k.center(5) for k in row])).center(width)
            left, right = divide(2, middle)
            middle = ''.join(chain(left, ' '*5, right))
            print(prefix + middle + '│')
        print(' ╰' + '─' * (width+5) + '╯')

if outtype == 'drawing':
    print(yaml.dump(config, default_flow_style=None, sort_keys=False))




