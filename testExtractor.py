#!/usr/bin/python3
import base64, os, sys, importlib
from io import BytesIO
from PIL import Image
import cairosvg
import matplotlib.pyplot as plt
import matplotlib.axes as mpaxes

#test if usage clear
if len(sys.argv)==1 or sys.argv[1]=='help':
  print("Usage:\n  testExtractor.py  path/to/file.png plotType\nwhere plotType is optional.")
  print("Examples:")
  print('te')
  sys.exit()
filePath = sys.argv[1]
plotType = sys.argv[2] if len(sys.argv)>2 else ''
print('Info: test file',filePath)
print('Info: plot type',plotType,'\n')

#load corresponding file
sys.path.append('Extractors')
extension = os.path.splitext(filePath)[1][1:]
pyFile = 'extractor_'+extension+'.py'
if os.path.exists('Extractors'+os.sep+pyFile):
  module  = importlib.import_module(pyFile[:-3])
  content = module.use(filePath, plotType)

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
