import re, unicodedata, yaml, sys
from pprint import pprint as pp

if len(sys.argv) != 4:
    print(f'Usage: {sys.argv[0]} columns rows thumbs')
columns, rows, thumbs = map(int, sys.argv[1:])

config = {
'layout': {
  'ortho_layout': {
      'split': True,
      'columns': columns,
      'rows': rows,
      'thumbs': thumbs,
  },
},
#'draw_config': {'n_columns': 2,},
'layers': {
},
'combos': [
],
}


split_layers = lambda s: re.findall(r'\n?.╭─+╮(.+?)╰─+╯\w*', s, re.S)

combos = open('combos.txt').read()
splitup = split_layers(combos)
for i, s in enumerate(splitup):
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
    #print(name, keys)
    config['combos'].append({
        'p': keys,
        'k': name,
        'l': ['BASE'],
        'draw_separate': separate,
    })

lines = open('layout.txt').read()
keycodes = open('keycodes.tsv').read()

splitup = re.findall(r'\n?(.╭─+╮.+?╰─+╯)\w*', lines, re.S)
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

def replace(k):
    if k == '󰘴f': return {'t': 'f', 'h': 'CTRL'}
    if k == '󰘴j': return {'t': 'j', 'h': 'CTRL'}
    if k == '󰆢': return ''
    if k == '󰿦': return ''
    if k == '': return {'type': 'held'} # held
    return k

for i, t in enumerate(splitup):
    #print(f'LAYER {i}')
    layer = []
    name = f'layer_{i}'
    for j, s in enumerate(vmid(t)):
        middle, newname = hmid(s)
        middle = [replace(k) for k in middle]
        if newname:
            name = newname
        if j == 3: continue # we no longer use this row
        if j < 3: # top three rows
            if columns == 6:
                layer.append(middle)
                #print(i, len(middle))
            elif columns == 5:
                layer.append(middle[1:-1])
        else: # thumbs
            layer.extend(middle)
    config['layers'][name] = layer
print(yaml.dump(config, default_flow_style=None, sort_keys=False))
