import yaml, re
from pprint import pprint as pp
y = yaml.load(open('pretty/draw.yaml'), Loader=yaml.Loader)
layers = {}
for k in y['layers'].keys():
    if m := re.match(r'(\d+)_layer', k):
        i = m.group(1)
        print(i)
        d = { 'layers': {i: y['layers'][k] } }
        open(f'pretty/draw.{i}.yaml', 'w').write(yaml.dump(d, Dumper=yaml.Dumper))
    else:
        raise ValueError("Can't parse layers in yaml")
