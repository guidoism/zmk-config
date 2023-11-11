import yaml, re
from pprint import pprint as pp
y = yaml.load(open('pretty/draw.yaml'), Loader=yaml.Loader)

change = {
    '0_layer': '$$mdi:numeric-0-circle$$',
    '1_layer': '$$mdi:numeric-1-circle$$',
    '2_layer': '$$mdi:numeric-2-circle$$',
    '3_layer': '$$mdi:numeric-3-circle$$',
    '4_layer': '$$mdi:numeric-4-circle$$',
    '5_layer': '$$mdi:numeric-5-circle$$',
    '6_layer': '$$mdi:numeric-6-circle$$',
    '7_layer': '$$mdi:numeric-7-circle$$',
    '8_layer': '$$mdi:numeric-8-circle$$',
}

layers = {}
for k in y['layers'].keys():
    if m := re.match(r'(\d+)_layer', k):
        i = m.group(1)
        print(i)
        d = { 'layers': {i: [[change.get(str(key), key) for key in row] for row in y['layers'][k]] } }
        open(f'pretty/draw.{i}.yaml', 'w').write(yaml.dump(d, Dumper=yaml.Dumper))
    else:
        raise ValueError("Can't parse layers in yaml")
