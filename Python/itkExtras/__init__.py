# new features introduced by itk module
# each new feature use a name in lower case

def auto_progress( b ):
  import itkTemplate
  itkTemplate.auto_progress = b
  
  import itkConfig
  if b :
    def loadingCallback(name, p):
      import sys
      clrLine = "\033[2000D\033[K"
      print >> sys.stderr, clrLine+"Loading %s..." % name,
      if p == 1 :
        print >> sys.stderr, clrLine,
    
    itkConfig.ImportCallback = loadingCallback
  else:
    itkConfig.ImportCallback = None
  

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
  st = itk.BinaryBallStructuringElement[itk.B, dim]()
  st.SetRadius(radius)
  # call the boring CreateStructuringElement() method
  st.CreateStructuringElement()
  return st
  
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
    img = image(input)
    if img.GetImageDimension() == 3:
	return show3D(input, **kargs)
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

# display scalar images in volume
class show3D :
  def __init__(self, input=None, MinOpacity=0.0, MaxOpacity=0.1) :
    import qt
    import vtk
    from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
    self.__MinOpacity__ = MinOpacity
    self.__MaxOpacity__ = MaxOpacity
    # every QT app needs an app
    self.__app__ = qt.QApplication(['itkviewer'])
    # create the widget
    self.__widget__ = QVTKRenderWindowInteractor()
    self.__ren__ = vtk.vtkRenderer()
    self.__widget__.GetRenderWindow().AddRenderer(self.__ren__)
    self.__itkvtkConverter__ = None
    self.__volumeMapper__ = vtk.vtkVolumeTextureMapper2D()
    self.__volume__ = vtk.vtkVolume()
    self.__volumeProperty__ = vtk.vtkVolumeProperty()
    self.__volume__.SetMapper(self.__volumeMapper__)
    self.__volume__.SetProperty(self.__volumeProperty__)
    self.__ren__.AddVolume(self.__volume__)
    self.__outline__ = None
    self.__outlineMapper__ = None
    self.__outlineActor__ = None
    self.AdaptColorAndOpacity(0, 255)
    if input :
      self.SetInput(input)
      self.AdaptColorAndOpacity()
      
  def Render(self):
    self.__ren__.Render()
    
  def GetWidget(self) :
    return self.__widget__
  
  def GetRenderer(self) :
    return self.__ren__
  
  def GetConverter(self) :
    return self.__itkvtkConverter__
  
  def GetVolumeMapper(self) :
    return self.__volumeMapper__
  
  def GetVolume(self) :
    return self.__volume__
  
  def GetVolumeProperty(self) :
    return self.__volumeProperty__
  
  def Show(self) :
    self.__widget__.show()
    
  def Hide(self) :
    self.__widget__.hide()
    
  def SetInput(self, input) :
    from __builtin__ import range # required because range is overladed in this module
    img = image(input)
    self.__input__ = img
    if img :
      # Update to try to avoid to exit if a c++ exception is throwed
      # sadely, it will not prevent the program to exit later...
      # a real fix would be to wrap c++ exception in vtk
      img.UpdateOutputInformation()
      img.Update()
      import itk
      # flip the image to get the same representation than the vtk one
      self.__flipper__ = itk.FlipImageFilter[img].New(Input=img)
      axes = self.__flipper__.GetFlipAxes()
      axes.SetElement(1, True)
      self.__flipper__.SetFlipAxes(axes)
      # change the spacing while still keeping the ratio to workaround vtk bug
      # when spacing is very small
      spacing_ = spacing(img)
      normSpacing = []
      for i in range(0, spacing_.Size()):
        normSpacing.append( spacing_.GetElement(i) / spacing_.GetElement(0) )
      self.__changeInfo__ = itk.ChangeInformationImageFilter[img].New(self.__flipper__, OutputSpacing=normSpacing, ChangeSpacing=True)
      # now really convert the data
      self.__itkvtkConverter__ = itk.ImageToVTKImageFilter[img].New(self.__changeInfo__)
      self.__volumeMapper__.SetInput(self.__itkvtkConverter__.GetOutput())
      # needed to avoid warnings
      # self.__itkvtkConverter__.GetOutput() must be callable
      import vtk
      if not self.__outline__ :
	  self.__outline__ = vtk.vtkOutlineFilter()
	  self.__outline__.SetInput(self.__itkvtkConverter__.GetOutput())
	  self.__outlineMapper__ = vtk.vtkPolyDataMapper()
	  self.__outlineMapper__.SetInput(self.__outline__.GetOutput())
	  self.__outlineActor__ = vtk.vtkActor()
	  self.__outlineActor__.SetMapper(self.__outlineMapper__)
	  self.__ren__.AddActor(self.__outlineActor__)
      else :
	  self.__outline__.SetInput(self.__itkvtkConverter__.GetOutput())

    self.Render()
    
  def GetInput(self):
    return self.__input__
  
  def AdaptColorAndOpacity(self, minVal=None, maxVal=None):
    if minVal == None or maxVal == None :
      m, M = self.GetRange()
      if minVal == None :
        minVal = m
      if maxVal == None :
        maxVal = M
    self.AdaptOpacity(minVal, maxVal)
    self.AdaptColor(minVal, maxVal)
    
  def AdaptOpacity(self, minVal=None, maxVal=None) :
    import vtk
    if minVal == None or maxVal == None :
      m, M = self.GetRange()
      if minVal == None :
        minVal = m
      if maxVal == None :
        maxVal = M
    opacityTransferFunction = vtk.vtkPiecewiseFunction()
    opacityTransferFunction.AddPoint(minVal, self.__MinOpacity__)
    opacityTransferFunction.AddPoint(maxVal, self.__MaxOpacity__)
    self.__volumeProperty__.SetScalarOpacity(opacityTransferFunction)
    
  def AdaptColor(self, minVal=None, maxVal=None):
    import vtk
    if minVal == None or maxVal == None :
      m, M = self.GetRange()
      if minVal == None :
        minVal = m
      if maxVal == None :
        maxVal = M
    colorTransferFunction = vtk.vtkColorTransferFunction()
    colorTransferFunction.AddHSVPoint(minVal, 0.0, 0.0, 0.0)
    colorTransferFunction.AddHSVPoint((maxVal-minVal)*0.25, 0.66, 1.0, 1.0)
    colorTransferFunction.AddHSVPoint((maxVal-minVal)*0.5,  0.44, 1.0, 1.0)
    colorTransferFunction.AddHSVPoint((maxVal-minVal)*0.75, 0.22, 1.0, 1.0)
    colorTransferFunction.AddHSVPoint(maxVal,               0.0,  1.0, 1.0)
    self.__volumeProperty__.SetColor(colorTransferFunction)
    self.Render()
    
  def GetRange(self) :
    conv = self.GetConverter()
    conv.Update()
    return conv.GetOutput().GetScalarRange()
  
  def GetMaxOpacity(self) :
    return self.__MaxOpacity__
  
  def GetMinOpacity(self) :
    return self.__MinOpacity__
  
  def SetMaxOpacity(self, val) :
    self.__MaxOpacity__ = val
    self.AdaptColorAndOpacity()
    
  def SetMinOpacity(self, val) :
    self.__MinOpacity__ = val
    self.AdaptColorAndOpacity()


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
