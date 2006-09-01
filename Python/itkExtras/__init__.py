# new features introduced by itk module
# each new feature use a name in lower case
clrLine = "\033[2K\033E\033[1A"

def auto_progress( progressType = 1 ):
  """Set up auto progress report
  
  progressType:
    1 or True  -> auto progress be used in a terminal
    2          -> simple auto progress (without special characters)
    0 or False -> disable auto progress
  """
  import itkConfig
  
  if progressType == True or progressType == 1 :
    itkConfig.ImportCallback = terminal_import_callback
    itkConfig.ProgressCallback = terminal_progress_callback
    
  elif progressType == 2 :
    itkConfig.ImportCallback = simple_import_callback
    itkConfig.ProgressCallback = simple_progress_callback
    
  elif progressType == False or progressType == 0 :
    itkConfig.ImportCallback = None
    itkConfig.ProgressCallback = None
    
  else:
    raise ValueError("Invalid auto progress type: "+repr(progressType))
  
def terminal_progress_callback(name, p):
  import sys
  print >> sys.stderr, clrLine+"%s: %f" % (name, p),
  if p == 1 :
    print >> sys.stderr, clrLine,
  
def terminal_import_callback(name, p):
  import sys
  print >> sys.stderr, clrLine+"Loading %s..." % name,
  if p == 1 :
    print >> sys.stderr, clrLine,
  
def simple_import_callback(name, p):
  import sys
  print >> sys.stderr, clrLine+"Loading %s..." % name,
  if p == 1 :
    print >> sys.stderr, "done"

def simple_progress_callback(name, p):
  import sys
  print >> sys.stderr, clrLine+"Running %s..." % name,
  if p == 1 :
    print >> sys.stderr, "done"


def force_load():
  """force itk to load all the submodules"""
  import itk
  for k in dir(itk):
    getattr(itk, k)

# Function to print itk object info
import sys
def echo(object, f=sys.stderr) :
   import itk
   ss = itk.StringStream()
   try :
      try:
         object.Print(ss.GetStream())
      except:
         object.Print(ss.GetStream(),Indent.New());
   except:
      print >> f, repr(object)
   else:
      print >> f, ss.GetString()
del sys

# return the size of an imageClass
def size(imageOrFilter) :
  # we don't need the entire output, only its size
  imageOrFilter.UpdateOutputInformation()
  img = image(imageOrFilter)
  return img.GetLargestPossibleRegion().GetSize()
  
# return the pyhsical size of an image
def physical_size(imageOrFilter) :
  from __builtin__ import range # required because range is overladed in this module
  spacing_ = spacing(imageOrFilter)
  size_ = size(imageOrFilter)
  result = []
  for i in range(0, spacing_.Size()):
    result.append( spacing_.GetElement(i) * size_.GetElement(i) )
  return result

# return the spacing of an image
def spacing(imageOrFilter) :
  # we don't need the entire output, only its size
  imageOrFilter.UpdateOutputInformation()
  img = image(imageOrFilter)
  return img.GetSpacing()
  
# return the index of an imageClass
def index(imageOrFilter) :
  # we don't need the entire output, only its size
  imageOrFilter.UpdateOutputInformation()
  img = image(imageOrFilter)
  return img.GetLargestPossibleRegion().GetIndex()
  
# return a structuring elt
def strel(dim, radius=1) :
  import itk
  return itk.FlatStructuringElement[dim].Ball(radius)
  
# return an image
from itkTemplate import image

# return the template of a class and its parameters
def template(cl) :
  from itkTemplate import itkTemplate
  return itkTemplate.__class_to_template__[class_(cl)]
  
# return ctype
def ctype(s) :
  from itkTypes import itkCType
  ret = itkCType.GetCType(" ".join(s.split()))
  if ret == None :
    raise KeyError("Unrecognized C type '%s'" % s)
  return ret
  
# return a class from an instance
def class_(obj) :
  import inspect
  if inspect.isclass(obj) :
    # obj is already a class !
    return obj
  else :
    # First, drop the smart pointer
    try:
      obj = obj.GetPointer()
    except:
      pass
    # try to get the real object if elt is a pointer (ends with Ptr)
    try:
      cls = obj.__dict__[obj.__class__]
    except:
      cls = obj.__class__
    # finally, return the class found
    return cls

# return range
def range(imageOrFilter) :
  import itk
  img = image(imageOrFilter)
  img.UpdateOutputInformation()
  img.Update()
  comp = itk.MinimumMaximumImageCalculator[img].New(Image=img)
  comp.Compute()
  return (comp.GetMinimum(), comp.GetMaximum())

# write an image
def write(imageOrFilter, fileName):
  import itk
  img = image(imageOrFilter)
  img.UpdateOutputInformation()
  writer = itk.ImageFileWriter[img].New(Input=img, FileName=fileName)
  writer.Update()
  
# choose the method to call according to the dimension of the image
def show(input, **kargs) :
    import itk
    img = image(input)
    if img.GetImageDimension() == 3 and "show3D" in dir(itk):
	return itk.show3D(input, **kargs)
    else :
	# print "2D not supported yet, use the 3D viewer."
	return show2D(input, **kargs)
    
class show2D :
  def __init__(self, input) :
    # use the tempfile module to get a non used file name and to put
    # the file at the rignt place
    import tempfile
    self.__tmpFile__ = tempfile.NamedTemporaryFile(suffix='.tif')
    write(input, self.__tmpFile__.name)
    # no run imview
    import os
    os.system("imview %s -fork" % self.__tmpFile__.name)
    #tmpFile.close()


class pipeline:
  """A convenient class to store the reference to the filters of a pipeline
  
  With this class, a method can create a pipeline of several filters and return
  it without losing the references to the filters in this pipeline. The pipeline
  object act almost like a filter (it has a GetOutput() method) and thus can
  be simply integrated in another pipeline.
  """
  def __init__( self, input=None ):
    self.clear()
    self.SetInput( input )

  def connect( self, filter ):
    """Connect a new filter to the pipeline
    
    The output of the first filter will be used as the input of this
    one and the filter passed as parameter will be added to the list
    """
    if self.GetOutput() != None:
      filter.SetInput( self.GetOutput() )
    self.append( filter )

  def append( self, filter ):
    """Add a new filter to the pipeline
    
    The new filter will not be connected. The user must connect it.
    """
    self.filter_list.append( filter )

  def clear( self ):
    """Clear the filter list
    """
    self.filter_list = []

  def GetOutput( self ):
    """Return the output of the pipeline
    
    If another output is needed, use
    pipeline[-1].GetAnotherOutput() instead of this method, or subclass
    pipeline to implement another GetOutput() method
    """
    if len(self) == 0:
      return self.GetInput()
    else :
      return self[-1].GetOutput()

  def SetInput( self, input ):
    """Set the input of the pipeline
    """
    if len(self) != 0:
      self[0].SetInput(input)
    self.input = input

  def GetInput( self ):
    """Get the input of the pipeline
    """
    return self.input
    
  def Update( self ):
    """Update the pipeline
    """
    if len(self) > 0:
      return self[-1].Update()
  
  def UpdateOutputInformation( self ):
    if "UpdateOutputInformation" in dir(self[-1]):
      self[-1].UpdateOutputInformation()
    else:	
      self.Update()
      
  def __getitem__( self, i ):
     return self.filter_list[i]

  def __len__( self ):
     return len(self.filter_list)

# now loads the other modules we may found in the same directory
import os.path, sys
directory = os.path.dirname(__file__)
moduleNames = [name[:-len('.py')] for name in os.listdir(directory) if name.endswith('.py') and name != '__init__.py']
for name in moduleNames:
  # there should be another way - I don't like to much exec -, but the which one ??
  exec "from %s import *" % name
# some cleaning
del directory, os, sys, moduleNames, name
