"""The motivation for this is that I want a text-based keymap format
that is easy to understand, can be edited quickly, can be used for
displaying what my keyboard's current layer means, and should be
easily transformed into other formats for creating firmware or display
on webpages.
"""

import re, unicodedata, yaml, sys, collections
from pprint import pprint as pp
from more_itertools import split_into, transpose

if len(sys.argv) != 5:
    print(f'Usage: {sys.argv[0]} [drawing|firmware] columns rows thumbs')

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
    #'draw_config': {'n_columns': 2,},
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
    '󰆢': '',
    '󰿦': {'type': 'ghost'},
    '': {'type': 'held'},
}

def split(s):
    return re.findall(r'\n?(.╭─+╮.+?╰─+╯)\w*', s, re.S)

for i, s in enumerate(split(layers)):
    # 1. Split apart into index, name, and list of rows
    lines = s.splitlines()
    top, middle, bottom = lines[0], lines[1:-1], lines[-1]
    column_sizes = list(map(len, re.search(r'(.*╭)(─+)(╮.*)', top).groups()))
    column_sizes[-1] = None # This make sure split_into returns the rest of the string
    # This splits the lines into prefix, body, suffix and then puts
    # the prefixes together, bodies togethers, and suffixes together.
    columns = [list(map(''.join, split_into(s, column_sizes))) for s in middle]
    segments = list(transpose(columns))
    index = ''.join([s.strip(' │') for s in segments[0]])
    name = ''.join([s.strip(' │') for s in segments[2]]) or f'layer_{i}'
    rows = [s.split() for s in segments[1]]

    # 2. Remove rows and columns based on intended keyboard size
    del rows[3] # We've given up on this row of thumb keys, too many keys clanky!
    if columnslen == 5:
        rows = [r[1:-1] for r in rows[:3]] + rows[3:]
    if thumbslen == 3:
        rows = rows[:3] + [rows[3][1:-1]]

    # 3. Replace keys in rows with keycodes or drawing config
    if outtype == 'firmware':
        rows = [[keycodes[k] for k in r] for r in rows]
        maxlen = min(12, max([max(map(len, r)) for r in rows]))
        rows = [[k.center(maxlen) for k in r] for r in rows]
        layer = '\n '.join(map(' '.join, rows))
        print(f"ZMK_LAYER({name},\n {layer})")
    elif outtype == 'drawing':
        #print(yaml.dump(config, default_flow_style=None, sort_keys=False))
        pass

quit()









for i, s in enumerate(split(combos)):
    keys = []
    for j, line in enumerate(s.splitlines()):
        if j == 4: continue
        if m := re.match(r'.*│(.+)│(\w+)\*.*', line):
            name = m.group(2)
            separate = True
            keys.extend(m.group(1).split())
        elif m := re.match(r'.*│(.+)│(\w+).*', line):
            name = m.group(2)
            separate = False
            keys.extend(m.group(1).split())
        elif m := re.match(r'.*│(.+)│.*', line):
            keys.extend(m.group(1).split())
    keys = [k for k, key in enumerate(keys) if key == '']
    config['combos'].append({
        'p': keys,
        'k': name,
        'l': ['BASE'],
        'draw_separate': separate,
        #  align: top
        #  offset: 2
    })

vmid = lambda t: t.split('\n')[1:-1]
def hmid(s):
    if m := re.match(r'[\s\d]│(.+)│([^│]*)', s):
        return (m.group(1).split(), m.group(2))
    
keycodes = dict(k.split('\t') for k in keycodes.splitlines())

#insides = [' '.join([hmid(s) for s in vmid(t)]) for t in splitup]
#for i, layer in enumerate(insides):
#    #codes = ' '.join([keycodes[k] for k in layer.split()])
#    # print(f"ZMK_LAYER(layer_{i}, {codes})")
#    for k in layer.split():
#        print(k, keycodes[k])


# TODO: change
#  - 󰘴f to {t: f, h: CTRL}
#  - arrows to $$phosphor:bold/arrow-fat-up$$
#  - P↑ to

# This is basically just like keycodes.tsv
def drawingcodes(k):
    if k == '󰘴f': return {'t': 'f', 'h': 'CTRL'}
    if k == '󰘴j': return {'t': 'j', 'h': 'CTRL'}
    if k == '󰆢': return ''
    if k == '󰿦': return {'type': 'ghost'}
    if k == '': return {'type': 'held'}
    return k




splitup = re.findall(r'\n?(.╭─+╮.+?╰─+╯)\w*', layers, re.S)


entire_layers = collections.defaultdict(list)
for i, t in enumerate(splitup):
    #print(f'LAYER {i}')
    print(t)
    quit()
    layer = []
    name = f'layer_{i}'
    for j, s in enumerate(vmid(t)):
        middle, newname = hmid(s)
        if outtype == 'drawing':
            middle = [drawingcodes(k) for k in middle]
        elif outtype == 'firmware':
            middle = [keycodes[k] for k in middle]
        if newname:
            name = newname

        if j == 3: continue # we no longer use this row
        if j < 3: # top three rows
            if columns == 6:
                layer.append(middle)
                entire_layers[name].extend(middle)
            elif columns == 5:
                layer.append(middle[1:-1])
                entire_layers[name].extend(middle[1:-1])
        else: # thumbs
            if thumbs == 3:
                middle = middle[1:-1]
            layer.extend(middle)
            entire_layers[name].extend(middle)
    config['layers'][name] = layer

if outtype == 'drawing':
    print(yaml.dump(config, default_flow_style=None, sort_keys=False))
elif outtype == 'firmware':
    for name, layer in entire_layers.items():
        layer = ' '.join(layer)
        print(f"ZMK_LAYER({name}, {layer})")
