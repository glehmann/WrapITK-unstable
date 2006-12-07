#!/usr/bin/env python

import pygccxml, sys, re, cStringIO
from optparse import OptionParser

optionParser = OptionParser()
optionParser.add_option("--idx", action="append", dest="idx", default=[], metavar="FILE", help="idx file to be used.")
optionParser.add_option("--mdx", action="append", dest="mdx", default=[], metavar="FILE", help="master idx file to be used.")
optionParser.add_option("--include", action="append", dest="includes", default=[], metavar="FILE", help="File to be included in the generated interface file.")
optionParser.add_option("--take-includes", action="append", dest="take_includes", default=[], metavar="FILE", help="File which contains the include to take, and include in the generated interface file.")
optionParser.add_option("--swig-include", action="append", dest="swig_includes", default=[], metavar="FILE", help="File to be included by swig (%include) in the generated interface file.")
optionParser.add_option("--import", action="append", dest="imports", default=[], metavar="FILE", help="File to be imported in the generated interface file.")
optionParser.add_option("-w", "--disable-warning", action="append", dest="warnings", default=[], metavar="WARNING", help="Warning to be disabled.")
optionParser.add_option("-W", "--warning-error", action="store_true", dest="warningError", help="Treat warnings as errors.")
options, args = optionParser.parse_args()

# the output file
if args[1] == '-':
  outputFile = sys.stdout
else :
  outputFile = cStringIO.StringIO()

# a dict to let us use the alias name instead of the full c++ name. Without
# that, in many cases, swig don't know that's the same type
aliases = {}


error = False

def warn( id, msg ):
  global error
  if str(id) not in options.warnings:
    if options.warningError:
      print >> sys.stderr, "Error(%s): %s" % (str(id), msg)
      error = True
    else:
      print >> sys.stderr, "Warning(%s): %s" % (str(id), msg)



notWrapped = [
  "itk::SmartPointerForwardReference",
  "itk::LibHandle",
  "itk::CreateObjectFunctionBase",
  "itk::NeighborhoodAllocator",
  "itk::ImageRegion", # to avoid wrapping all the region for all the dims
  "itk::ImportImageContainer",
  "itk::DefaultPixelAccessor",
  "itk::NeighborhoodAccessorFunctor",
  "itk::DefaultVectorPixelAccessor",
  "itk::VectorImageNeighborhoodAccessorFunctor",
  "itk::ConstNeighborhoodIterator",
  "itk::Neighborhood",
  "itk::VectorContainer",
  "itk::MapContainer",
  "itk::ThreadFunctionType",
  "itk::ThreadProcessIDType",
]


def renameTypesInSTL( s ):
  if s.startswith( "std::" ) and pygccxml.declarations.templates.is_instantiation(s):
    args = []
    for arg in pygccxml.declarations.templates.args(s):
      t, d = typeAndDecorators( arg );
      if aliases.has_key( t ):
        args.append( aliases[t] + d )
      else:
        args.append( renameTypesInSTL( t ) + d )
    return pygccxml.declarations.templates.join( pygccxml.declarations.templates.name(s), args ) + typeAndDecorators( s )[1]
  return s
  

def removeStdAllocator( s ):
  if pygccxml.declarations.templates.is_instantiation(s):
    args = []
    for arg in pygccxml.declarations.templates.args(s):
      if not arg.startswith("std::allocator"):
        t, d = typeAndDecorators( arg );
        args.append( removeStdAllocator( t ) + d )
    return pygccxml.declarations.templates.join( pygccxml.declarations.templates.name(s), args ) + typeAndDecorators( s )[1]
  return s
  

def typeAndDecorators( s ):
  end = ""
  s = s.strip()
  ends = [" ", "*", "&", "const"]
  needToContinue = True
  while needToContinue:
    needToContinue = False
    for e in ends:
      if s.endswith( e ):
        end = e + end
        s = s[:-len(e)]
        needToContinue = True
  return (s, end)
 

def get_alias( decl_string ):
  s = str(decl_string)
  
  # drop the :: prefix - it make swig produce invalid code
  if s.startswith("::"):
    s = s[2:]
  
  # normalize string
  s = normalize( s )
  
  # workaround a bug - or is it a feature ? - somewhere
  s = s.replace("complex float", "std::complex<float>")
  s = s.replace("complex double", "std::complex<double>")
  s = s.replace("complex long double", "std::complex<long double>")
  
  (s, end) = typeAndDecorators( s )

  if aliases.has_key( s ):
#    print >> sys.stderr, s, end, "        ", aliases[s]
    return aliases[s] + end
  
  else:
    # replace the types defined in this type, to support std::vector<itkDataObject> for example
    s = renameTypesInSTL( s )
    
    # drop the allocator part of the type, because it is not supported by the %template directive with some languages (like tcl)
    s = removeStdAllocator( s )
    
    # rename basic_string to std::string to make name shorter
    s = s.replace("std::basic_string< char, std::char_traits< char > >", "std::string")
    
    if "<" in s:
      short_result = s[:s.find("<")]
    else:
      short_result = s
    if s.startswith( "itk::") and not s[:s.rfind("::")] in aliases and not short_result in notWrapped:
      warn( 4, "ITK type not wrapped, or currently not known: %s" % s )
    
    return s + end
    

def load_idx(file_name):
  f = file(file_name)
  for l in f:
    (full_name, alias, module) = re.findall(r'{(.*)} {(.*)} {(.*)}', l)[0]
    # workaround lack of :: prefix in idx files
    # TODO: would it be better to remove the :: prefix in the output of pygccxml ?
    # full_name = "::"+full_name
    # normalize some basic type names
    full_name = normalize( full_name )
    # TODO: add a warning if the type is defined several times
    aliases[ full_name ] = alias
    # declare the typedef
    print >> outputFile, "typedef %s %s;" % (full_name, alias)
  f.close()


def normalize(name):
  name = name.replace("short unsigned int", "unsigned short")
  name = name.replace("long unsigned int", "unsigned long")
  name = name.replace("short int", "short")
  name = name.replace("long int", "long")
  name = name.replace("unsigned int", "unsigned")
  # normalize spaces
  name = " ".join(name.replace(',', ', ').split())
  return name 


def generate( typedef, access ):
  # iterate over the constructors
  for constructor in typedef.type.declaration.constructors(): #recursive=False) :
    if constructor.access_type == access:
      # iterate over the arguments
      args = []
      for arg in constructor.arguments:
        s = "%s %s" % (get_alias(arg.type.decl_string), arg.name)
        # append the default value if it exists
        if arg.default_value:
          s += " = %s" % arg.default_value
        # and add the string to the arg list
        args.append( s )
      print >> outputFile, "    %s(%s);" % (typedef.name, ", ".join( args) )
  
  # iterate over the methods
  for method in typedef.type.declaration.member_functions(): #allow_empty=True, recursive=False):
    generate_method( typedef, method )
    
  # and the operators
  for method in typedef.type.declaration.member_operators(): #allow_empty=True, recursive=False):
    generate_method( typedef, method )
    
  # iterate over enumerations
  if access == "public":
    for enum in typedef.type.declaration.enums():
      if enum.name != "":
        content = [" %s = %i" % (key, value) for key, value in enum.values]
        print >> outputFile, "    enum %s { %s };" % ( enum.name, ", ".join( content ) )
  
  # TODO: ivars, typedefs, ...
    
    
def generate_method( typedef, method ):
  # avoid the apply method for the class vnl_c_vector: the signature is quite strange
  # a currently confuse swig :-/
  if method.access_type == access :
  
    if "(" in method.return_type.decl_string :
      warn( 1, "ignoring method not supported by swig '%s::%s'." % (typedef.name, method.name) )
      return
      
    if ( (typedef.name.startswith('vnl_') and method.name in ["as_ref"]) 
         or (typedef.name.startswith('itk') and method.name in ["rBegin", "rEnd", "GetSpacingCallback", "GetOriginCallback"]) ) :
      warn( 3, "ignoring black listed method '%s::%s'." % (typedef.name, method.name) )
      return
      
    # iterate over the arguments
    args = []
    for arg in method.arguments:
      s = "%s %s" % (get_alias(arg.type.decl_string), arg.name)
      if "(" in s:
        warn( 1, "ignoring method not supported by swig '%s::%s'." % (typedef.name, method.name) )
        return
      # append the default value if it exists
      if arg.default_value:
        s += " = %s" % arg.default_value
      # and add the string to the arg list
      args.append( s )
      
    # find the method decorators
    static = ""
    const = ""
    if method.has_static:
      static = "static "
    if method.has_const:
      const = " const"
    if method.virtuality != "not virtual":
      static += "virtual "
    if method.virtuality == "pure virtual":
      const += " = 0"
      
    print >> outputFile, "    %s%s %s(%s)%s;" % (static, get_alias(method.return_type.decl_string), method.name, ", ".join( args), const )



# init the pygccxml stuff
pygccxml.declarations.scopedef_t.RECURSIVE_DEFAULT = False
pygccxml.declarations.scopedef_t.ALLOW_EMPTY_MDECL_WRAPPER = True
# pass a fake gccxml path: it is not used here, but is required by
# pygccxml
pygccxml_config = pygccxml.parser.config.config_t("gccxml")
# create a reader
pygccxml_reader = pygccxml.parser.source_reader.source_reader_t(pygccxml_config)
# and read a xml file
res = pygccxml_reader.read_xml_file(args[0])

global_ns = pygccxml.declarations.get_global_namespace( res )
cable_ns = global_ns.namespace('_cable_')
wrappers_ns = cable_ns.namespace('wrappers')
# pygccxml.declarations.print_declarations( global_ns )



# and begin to write the output
print >> outputFile, "// This file is automatically generated."
print >> outputFile, "// Do not modify this file manually."
print >> outputFile
print >> outputFile

# first, define the module
# [1:-1] is there to drop the quotes
for lang in ["CHICKEN", "CSHARP", "GUILE", "JAVA", "LUA", "MODULA3", "MZSCHEME", "OCAML", "PERL", "PERL5", "PHP", "PHP4", "PHP5", "PIKE", "PYTHON", "R", "RUBY", "SEXP", "TCL", "XML"]:
  print >> outputFile, "#ifdef SWIG%s" % lang
  print >> outputFile, "%%module %s%s" % ( cable_ns.variable('group').value[1:-1], lang.title() )
  print >> outputFile, "#endif"
print >> outputFile

# add the includes
# use a set to avoid putting many times the same include
s = set()
print >> outputFile, "%{"
# the include files passed in option
for f in options.includes:
  i = "#include <%s>" % f
  if not i in s:
    print >> outputFile, i
    s.add( i )
# and the includes files from other files
for file_name in options.take_includes:
  f = file( file_name )
  for l in f :
    if l.startswith( '#include' ):
      i = " ".join(l.strip().split())
      if not i in s:
        print >> outputFile, i
        s.add( i )
  f.close()
print >> outputFile, "%}"
print >> outputFile
print >> outputFile

# load the aliases files
print >> outputFile, "%{"
# the idx files passed in option
for f in options.idx:
  load_idx(f)
# and the idx files in the mdx ones
for file_name in options.mdx:
  f = file( file_name )
  for l in f :
    # exclude the lines which are starting with % - that's not the idx files
    if not l.startswith( '%' ) and not l.isspace():
      load_idx(l.strip())
  f.close()
# iterate over all the typedefs in the _cable_::wrappers namespace
# to fill the alias dict
for typedef in wrappers_ns.typedefs(): #allow_empty=True):
  s = str(typedef.type.decl_string)
  # drop the :: prefix - it make swig produce invalid code
  if s.startswith("::"):
    s = s[2:]
  if not aliases.has_key( s ) :
    warn(2, "%s (%s) should be already defined in the idx files." % (s, typedef.name) )
    aliases[s] = typedef.name
    # declare the typedef
    print >> outputFile, "typedef %s %s;" % (s, typedef.name)
  
print >> outputFile, "%}"
print >> outputFile
print >> outputFile

# add the imports
for f in options.imports:
  print >> outputFile, "%%import %s" % f
print >> outputFile
print >> outputFile

# add the swig includes
for f in options.swig_includes:
  print >> outputFile, "%%include %s" % f
print >> outputFile
print >> outputFile


# iterate over all the typedefs in the _cable_::wrappers namespace
# to generate the .i file
for typedef in reversed(list(wrappers_ns.typedefs())):
  
  # declare the typedef
  # print >> outputFile, "%{"
  # print >> outputFile, "typedef %s %s;" % (typedef.type.decl_string, typedef.name)
  # print >> outputFile, "%}"
  # print >> outputFile

  # begin a new class
  super_classes = []
  for super_class in typedef.type.declaration.bases:
    super_classes.append( "%s %s" % ( super_class.access, get_alias(super_class.related_class.decl_string) ) )
  s = ""
  if super_classes:
    s = " : " + ", ".join( super_classes )
  print >> outputFile, "class %s%s {" % ( typedef.name, s )
  
  for access in ['public', 'protected', 'private']:
    print >> outputFile, "  %s:" % access
    generate( typedef, access )
    
  # add the destructor in private section if it is not public
  if not pygccxml.declarations.type_traits.has_public_destructor( typedef.type.declaration ) :
    print >> outputFile, "    ~%s();" % typedef.name
  
  # finally, close the class
  print >> outputFile, "};"
  print >> outputFile
  print >> outputFile


if error:
  sys.exit(1)
  
# finally, really write the output
if args[1] != '-':
  f = file(args[1], "w")
  f.write( outputFile.getvalue() )

