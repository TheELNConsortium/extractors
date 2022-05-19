"""extract data from a .png file
"""
import base64
from io import BytesIO
import numpy as np
from PIL import Image

def use(filePath, recipe=''):
  """
  Args:
     filePath (string): full path file name
     recipe (string): supplied to guide recipes
                      recipe is / separated hierarchical elements parent->child
  Returns:
    dict: containing image, metaVendor, metaUser, recipe
  """
  # Extractor
  image = Image.open(filePath)
  metaVendor = image.info
  if recipe.endswith('crop'):                   #: Crop 3/4 of the image
    imgArr = np.array(image)[:,:,0]
    newHeight = int(imgArr.shape[0]/2)
    newWidth  = int(imgArr.shape[1]/2)
    imgArr = imgArr[:newHeight, :newWidth]
    recipe = 'image/png/crop'
  else:                                         #: Default | uncropped
    imgArr = np.array(image)[:,:,0]
    recipe = 'image/png'
  maskBlackPixel = imgArr<128
  metaUser   = {'number black pixel', len(maskBlackPixel[maskBlackPixel]),
                'number all pixel', np.prod(image.size)}

  # convert PIL image to base64
  imageData = Image.fromarray(imgArr).convert('P')
  figfile = BytesIO()
  imageData.save(figfile, format="PNG")
  imageData = base64.b64encode(figfile.getvalue()).decode()
  imageData = "data:image/png;base64," + imageData

  # return everything
  return {'image':imageData, 'recipe':recipe, 'metaVendor':metaVendor, 'metaUser':metaUser}

  #other datatypes could follow here if statements are used
  #...
  #final return if nothing successful
  return {}
