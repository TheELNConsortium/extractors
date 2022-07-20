#!/usr/bin/python3
import base64
import sys
import importlib
import argparse
from pathlib import Path
from io import BytesIO
from PIL import Image
import cairosvg
import matplotlib.pyplot as plt
import matplotlib.axes as mpaxes

argparser = argparse.ArgumentParser(usage='testExtractor.py  path/to/file.png [-r recipe] [-d directory]')
argparser.add_argument('filePath', help='file path')
argparser.add_argument('-r','--recipe', help='extraction recipe', default='')
argparser.add_argument('-d','--directory', help='path to directory with extractors; default "Extractors"',\
                       default='Extractors')
args = argparser.parse_args()

#test if usage clear
filePath = Path(args.filePath)
print('Info: test file',args.filePath)
print('      plot type',args.recipe)
if not filePath.exists():
  print('      File does not exist!')

#load corresponding file
extension = filePath.suffix[1:]
pyFile = 'extractor_'+extension+'.py'
pyPath = Path.home()/args.directory[2:] if args.directory.startswith('~/') else Path(args.directory)
sys.path.append(str(pyPath))
if (pyPath/pyFile).exists():
    module  = importlib.import_module(pyFile[:-3])
    content = module.use(filePath, args.recipe)

    #verify image is of correct type
    if 'image' not in content:
        print('**Error: image not produced by extractor')
        sys.exit()
    if isinstance(content['image'],Image.Image):
        content['image'].show()
        print('**Warning: image is a PIL image: not a base64 string')
        print('Encode image via the following: pay attention to jpg/png which is encoded twice\n```')
        print('from io import BytesIO')
        print('figfile = BytesIO()')
        print('image.save(figfile, format="PNG")')
        print('imageData = base64.b64encode(figfile.getvalue()).decode()')
        print('image = "data:image/jpg;base64," + imageData')
        print('```')
    elif isinstance(content['image'], mpaxes._subplots.Axes):
        plt.show()
        print('**Warning: image is a matplotlib axis: not a svg string')
        print('  figfile = StringIO()')
        print('plt.savefig(figfile, format="svg")')
        print('image = figfile.getvalue()')

    #verify image visually
    elif isinstance(content['image'], str):
        if content['image'].startswith('data:image/'):
            #png or jpg encoded base64
            extension = content['image'][11:14]
            i = base64.b64decode(content['image'][22:])
        else:
            #svg data
            i = cairosvg.svg2png(bytestring=content['image'].encode())
        i = BytesIO(i)
        i = Image.open(i)
        i.show()
        del content['image']
    else:
        print("**ERROR, UNKNOWN IMAGE TYPE RETURNED", type(content['image']))

    print('Identified metadata',content)
