SILENT = 0; WARN = 1; ERROR = 2
DebugLevel = WARN

def LoadModule(name, namespace):
  """This function causes a SWIG module to be loaded into memory after its dependencies
  are satisfied. Information about the templates defined therein is looked up from 
  a config file, and PyTemplate instances for each are created, or added to if the
  instance already exists in the 'namespace' dictionary.
  The 'namespace' parameter is updated with these PyTemplate instances. The raw
  classes loaded from the named module's SWIG interface are placed in the 'swig'
  sub-module within the namespace. This sub-module is created if needed."""
  import sys, imp, itkPyTemplate
  
  module = SatisfyDependenciesAndLoad(name)
  swig = namespace.setdefault('swig', imp.new_module('swig'))
  for k, v in module.__dict__.items():
    if not k.startswith('__'): setattr(swig, k, v)
  
  data = module_data[name]
  if data:
    for template in data.templates:
      pyTemplateName, swigTemplateName, templateParams, mangledName = template
      templateContainer = namespace.setdefault(pyTemplateName, itkPyTemplate.itkPyTemplate(swigTemplateName))
      if isinstance(templateContainer, itkPyTemplate.itkPyTemplate):
        try: templateContainer.__set__(templateParams, getattr(module, mangledName))
        except Exception, e: DebugPrintError("%s not found in module %s because of exception:\n %s" %(mangledName, name, e))
      else:
        DebugPrintError("Cannot update template information for %s because there is a non itkPyTemplate instance with that name." %pyTemplateName)

def SatisfyDependenciesAndLoad(name):
  """Recursively satisfy the dependencies of named module and load that module.
  Dependencies are looked up from the auto-generated configuration files."""
  import sys
  
  # SWIG-generated modules have Python appended
  moduleName = "%sPython" %name
  # bail out if it's already loaded.
  if moduleName in sys.modules: return sys.modules[moduleName]
  data = module_data[name]
  if data:
    for dep in data.depends:
      SatisfyDependenciesAndLoad(dep)
  return LoadSWIGLibrary(moduleName)

def LoadSWIGLibrary(moduleName):
  """Do all the work to set up the environment so that a SWIG-generated library
  can be properly loaded. This invloves setting paths, etc., defined in itkConfig."""
  import sys, imp, itkConfig
  
  # To share symbols across extension modules, we must set
  #     sys.setdlopenflags(dl.RTLD_NOW|dl.RTLD_GLOBAL)
  #
  # Since RTLD_NOW==0x002 and RTLD_GLOBAL==0x100 very commonly
  # we will just guess that the proper flags are 0x102 when there
  # is no dl module.

  # Save the current dlopen flags and set the ones we need.
  try:
    import dl
    newflags = dl.RTLD_NOW|dl.RTLD_GLOBAL
  except:
    newflags = 0x102  # No dl module, so guess (see above).
  try:
    oldflags = sys.getdlopenflags()
    sys.setdlopenflags(newflags)
  except:
    oldflags = None
  
  # set the path so that the imported module can load swig-generated shared  
  # libraries or other swig-generated scripts.
  sys.path.insert(1, itkConfig.swig_lib)
  sys.path.insert(1, itkConfig.swig_py)
  
  # find and load the module
  try:
    fp = None # needed in case next line raises exception, so that finally block works
    fp, pathname, description = imp.find_module(moduleName, [itkConfig.swig_py,])
    return imp.load_module(moduleName, fp, pathname, description)
  finally:
    # Since we may exit via an exception, close fp explicitly.
    if fp: fp.close()
    # and restore environment to normalcy
    sys.path.remove(itkConfig.swig_lib)
    sys.path.remove(itkConfig.swig_py)
    if oldflags and hasattr(sys, 'setdlopenflags'):
      # try to avoid raising an exception, because if we do, the import exception
      # that might have occured above in the try block won't get reported.
      try: sys.setdlopenflags(oldflags)
      except: pass

class ModuleData(dict):
  """A dictionary that knows how to look up module configuration data from the
  auto-generated configuration files. The location of these files is specified in
  itkConfig."""
  
  def __getitem__(self, key):
    import os, itkConfig
    try:
      return dict.__getitem__(self, key)
    except KeyError:
      # search order for keyConfig.py: 
      # (1) itkConfig.config_py directory
      # (2) __file__/Configuration
      # (3) ./Configuration
      # (4) .
      data = self.__find_file(key, [itkConfig.config_py, 
        os.path.join(__file__, 'Configuration'), 'Configuration', '.'])
      if data:
        return data
      else:
        DebugPrintError("Could not find configuration data for module %s." %key)
        
  def __find_file(self, module, paths):
    import os
    configFile = "%sConfig.py" %module
    for path in paths:
      try: listing = os.listdir(path)
      except: continue
      if configFile in listing:
        result = self.AttributeDict() # so we can write 'result.depends, etc., instead of result['depends']'
        execfile(os.path.join(path, configFile), result)
        self[file] = result
        return result
    return None
  
  class AttributeDict(dict):
    """A dictionary that can be accessed with __getattribute__, so that d[key] or
    d.key both return the value for that key."""    
    def __getattribute__(self, key):
      try:
        return self[key]
      except:
        return dict.__getattribute__(self, key)

def DebugPrintError(error):
  import sys
  if DebugLevel == WARN:
    print >> sys.stderr, error
  elif DebugLevel == ERROR:
    raise RuntimeError(error)


module_data = ModuleData()