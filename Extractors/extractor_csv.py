"""extract data from .csv file
"""
from io import StringIO
import numpy as np
import matplotlib.pyplot as plt

def use(filePath, recipe=''):
  """
  Args:
     filePath (string): full path file name
     recipe (string): supplied to guide recipes
                      recipe is / separated hierarchical elements parent->child
  Returns:
    dict: containing image, metaVendor, metaUser, recipe
  """
  # Extractor for fancy instrument
  data = np.loadtxt(filePath, delimiter=',')
  ax1 = plt.subplot(111)
  if recipe.endswith('red'):              #: Draw with red curve
    ax1.plot(data[:,0], data[:,1],'r')
  else:                                   #: Default | blueish curve
    ax1.plot(data[:,0], data[:,1])
  metaUser = {'max':data[:,1].max(), 'min':data[:,1].min()}
  recipe = 'csv'

  #convert axes to svg image
  figfile = StringIO()
  plt.savefig(figfile, format='svg')
  image = figfile.getvalue()

  # return everything
  return {'image':image, 'recipe':recipe, 'metaVendor':{}, 'metaUser':metaUser}

  #other datatypes follow here
  #...
  #final return if nothing successful
  return {}
