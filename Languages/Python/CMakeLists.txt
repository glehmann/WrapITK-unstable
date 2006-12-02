###############################################################################
# configure python
FIND_PACKAGE(PythonLibs)
FIND_PACKAGE(PythonInterp)
MARK_AS_ADVANCED(PYTHON_EXECUTABLE)
INCLUDE_DIRECTORIES(${PYTHON_INCLUDE_PATH})


###############################################################################
# store the current dir, so it can be reused later
SET(WRAP_ITK_PYTHON_SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}" CACHE INTERNAL "python source dir")
SET(WRAP_ITK_PYTHON_BINARY_DIR "${CMAKE_CURRENT_BINARY_DIR}" CACHE INTERNAL "python binary dir")


###############################################################################
# create the python directory in the classindex dir
FILE(MAKE_DIRECTORY ${WRAPPER_MASTER_INDEX_OUTPUT_DIR}/python)


###############################################################################
# Add doxygen support : Experimental
SET(DOXYGEN_MAN_PATH CACHE PATH "Experimental/Python only: Directory in which doxygen-generated man pages for itk classes are or should be placed.")
IF(DOXYGEN_MAN_PATH)
  # Configure the make_doxygen_conf.py script.
  SET(CONFIG_ITK_PATH)
  FOREACH(dir ${ITK_INCLUDE_DIRS})
    SET(CONFIG_ITK_PATH "${CONFIG_ITK_PATH}'${dir}',\n")
  ENDFOREACH(dir)
  SET(CONFIG_WRAP_ITK_DOXYGEN_ROOT "${DOXYGEN_MAN_PATH}")
  SET(CONFIG_ITK_SOURCE_DIR "${ITK_SOURCE_DIR}")
  CONFIGURE_FILE("${CMAKE_CURRENT_SOURCE_DIR}/make_doxygen_config.py.in" 
    "${CMAKE_CURRENT_BINARY_DIR}/make_doxygen_config.py"
    @ONLY IMMEDIATE)
ENDIF(DOXYGEN_MAN_PATH)


###############################################################################
# Configure the path-dependent itkConfig.py

# we specify these directories with relative paths  so that the file can be 
# bundled up into an install conventiently. Python will take care of turning
# the / path separator into \ on windows if needed.

IF(CMAKE_CONFIGURATION_TYPES)
  SET(CONFIG_WRAP_ITK_DATA_ROOT "../../Data")
  SET(CONFIG_WRAP_ITK_TEST_ROOT "../../Testing")
  SET(CONFIG_PYTHON_CONFIGPY_DIR "../Configuration")

  FOREACH(config ${CMAKE_CONFIGURATION_TYPES})
    # SWIG-generated libs and *.py files are sent to ${config} subdir
    # This assumes that LIBRARY_OUTPUT_PATH is WrapITK_BINARY_DIR/bin (bad!)
    # TODO: We need a better way to do this.
    SET(CONFIG_PYTHON_SWIGPY_DIR "../../lib/${config}")
    SET(CONFIG_PYTHON_SWIGLIB_DIR "../../lib/${config}")
    CONFIGURE_FILE("${CMAKE_CURRENT_SOURCE_DIR}/itkConfig.py.in"
                   "${WrapITK_BINARY_DIR}/Python/${config}/itkConfig.py"
                   @ONLY IMMEDIATE)
  ENDFOREACH(config)
ELSE(CMAKE_CONFIGURATION_TYPES)
  SET(CONFIG_WRAP_ITK_DATA_ROOT "../Data")
  SET(CONFIG_WRAP_ITK_TEST_ROOT "../Testing")
  SET(CONFIG_PYTHON_CONFIGPY_DIR "Configuration")

  SET(CONFIG_PYTHON_SWIGPY_DIR "../lib")
  SET(CONFIG_PYTHON_SWIGLIB_DIR "../lib")
  CONFIGURE_FILE("${CMAKE_CURRENT_SOURCE_DIR}/itkConfig.py.in"
                 "${WrapITK_BINARY_DIR}/Python/itkConfig.py"
                 @ONLY IMMEDIATE)
ENDIF(CMAKE_CONFIGURATION_TYPES)

SET(CONFIG_WRAP_ITK_TEST_ROOT "None")
SET(CONFIG_PYTHON_SWIGLIB_DIR "../lib")
SET(CONFIG_PYTHON_SWIGPY_DIR "../lib")
SET(CONFIG_PYTHON_CONFIGPY_DIR "Configuration")
CONFIGURE_FILE("${CMAKE_CURRENT_SOURCE_DIR}/itkConfig.py.in"
               "${WrapITK_BINARY_DIR}/Python/InstallOnly/itkConfig.py"
              @ONLY IMMEDIATE)

WRAP_ITK_INSTALL(/Python "${WrapITK_BINARY_DIR}/Python/InstallOnly/itkConfig.py")


###############################################################################
# Copy python files for out-of-source builds, and set up install of same.

# Create a list of Python files.
# WrapITK/Python/*.py
SET(ITK_PYTHON_FILES
  itk
  itkBase
  itkTemplate
  itkTypes
#  itkExtras/__init__
  itkLazy
  )
# Done listing files.

# Now copy these files if necessary.

IF ("${WrapITK_BINARY_DIR}" MATCHES "^${WrapITK_SOURCE_DIR}$")
  # In source build -- no need to copy Python file. Do need to set up the install.
  FOREACH(file ${ITK_PYTHON_FILES})
    SET(install_tgt "${CMAKE_CURRENT_SOURCE_DIR}/${file}.py")
    SET(WRAP_ITK_PYTHON_INSTALL_FILES ${WRAP_ITK_PYTHON_FILES} "${install_tgt}")
  ENDFOREACH(file)
ELSE ("${WrapITK_BINARY_DIR}" MATCHES "^${WrapITK_SOURCE_DIR}$")
  SET(WRAP_ITK_PYTHON_FILES)
  ADD_CUSTOM_TARGET(copy_python_files ALL)
  FOREACH(file ${ITK_PYTHON_FILES})
    SET(src "${CMAKE_CURRENT_SOURCE_DIR}/${file}.py")
    # recall that WRAP_ITK_BUILD_INTDIR expands to nothing if no config types are set,
    # or to "CMAKE_CONFIG_INTDIR/" if there are such. Likewise, WRAP_ITK_INSTALL_INTDIR
    # expands to ${BUILD_TYPE}/ or nothing.
    SET(copy_tgt "${CMAKE_CURRENT_BINARY_DIR}/${WRAP_ITK_BUILD_INTDIR}${file}.py")
    SET(WRAP_ITK_PYTHON_FILES ${WRAP_ITK_PYTHON_FILES} "${copy_tgt}")
    SET(install_tgt "${CMAKE_CURRENT_BINARY_DIR}/${WRAP_ITK_INSTALL_INTDIR}${file}.py")
    SET(WRAP_ITK_PYTHON_INSTALL_FILES ${WRAP_ITK_PYTHON_INSTALL_FILES} "${install_tgt}")
    
    # create the directory to avoid loosing case on windows
    FILE(MAKE_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/${WRAP_ITK_INSTALL_INTDIR}${path})

    ADD_CUSTOM_COMMAND(SOURCE ${src}
      COMMAND ${CMAKE_COMMAND}
      ARGS -E copy ${src} ${copy_tgt}
      OUTPUTS ${copy_tgt}
      TARGET copy_python_files
      COMMENT "Copying ${file}.py to build dir.")
  ENDFOREACH(file)
  
  # driver command to make the copy happen.
  ADD_CUSTOM_COMMAND(
    SOURCE copy_python_files
    DEPENDS ${WRAP_ITK_PYTHON_FILES}
    TARGET copy_python_files)
ENDIF ("${WrapITK_BINARY_DIR}" MATCHES "^${WrapITK_SOURCE_DIR}$")

# Install the package python files.
WRAP_ITK_INSTALL(/Python ${WRAP_ITK_PYTHON_INSTALL_FILES})


###############################################################################
# Configure and install the custom python .pth files

IF(CMAKE_CONFIGURATION_TYPES)

  FOREACH(config ${CMAKE_CONFIGURATION_TYPES})
    SET(CONFIG_WRAP_ITK_PYTHON_DIR "${CMAKE_CURRENT_BINARY_DIR}/${config}")

    # SWIG-generated libs and *.py files are sent to ${config} subdir
    # This assumes that LIBRARY_OUTPUT_PATH is WrapITK_BINARY_DIR/bin (bad!)
    # TODO: We need a better way to do this.
    CONFIGURE_FILE("${CMAKE_CURRENT_SOURCE_DIR}/WrapITK.pth.in"
                   "${CMAKE_CURRENT_BINARY_DIR}/${config}/WrapITK.pth"
                   @ONLY IMMEDIATE)
  ENDFOREACH(config)
ELSE(CMAKE_CONFIGURATION_TYPES)
  SET(CONFIG_WRAP_ITK_PYTHON_DIR "${CMAKE_CURRENT_BINARY_DIR}")

  CONFIGURE_FILE("${CMAKE_CURRENT_SOURCE_DIR}/WrapITK.pth.in"
                 "${CMAKE_CURRENT_BINARY_DIR}/WrapITK.pth"
                 @ONLY IMMEDIATE)

ENDIF(CMAKE_CONFIGURATION_TYPES)

SET(CONFIG_WRAP_ITK_PYTHON_DIR "${CMAKE_INSTALL_PREFIX}/${WRAP_ITK_INSTALL_PREFIX}/Python")
CONFIGURE_FILE("${CMAKE_CURRENT_SOURCE_DIR}/WrapITK.pth.in"
            "${CMAKE_CURRENT_BINARY_DIR}/InstallOnly/WrapITK.pth"
            @ONLY IMMEDIATE)

IF(PYTHON_EXECUTABLE)
  FILE(WRITE ${CMAKE_CURRENT_BINARY_DIR}/det_spp.py "try:\n  import distutils.sysconfig; print distutils.sysconfig.get_python_lib(1)\nexcept: pass")
  EXEC_PROGRAM("${PYTHON_EXECUTABLE}"
    ARGS "\"${CMAKE_CURRENT_BINARY_DIR}/det_spp.py\""
    OUTPUT_VARIABLE py_spp
  )
ENDIF(PYTHON_EXECUTABLE)

STRING(REGEX REPLACE "\\\\" "/" py_spp_nobackslashes "${py_spp}")
SET(PY_SITE_PACKAGES_PATH "${py_spp_nobackslashes}" CACHE PATH "Python site-packages directory to install a .pth file pointing at WrapITK Python modules.")
MARK_AS_ADVANCED(PY_SITE_PACKAGES_PATH)
IF(PY_SITE_PACKAGES_PATH)
  INSTALL_AT_ABSOLUTE_PATH(install_wrapitk_compatibility "${PY_SITE_PACKAGES_PATH}" "${CMAKE_CURRENT_BINARY_DIR}/InstallOnly/WrapITK.pth")
ENDIF(PY_SITE_PACKAGES_PATH)



# # compile python files
# SET(PYTHON_MODULES "")
# FOREACH(m ${WRAP_ITK_MODULES})
#   SET(PYTHON_MODULES ${PYTHON_MODULES} _${m}Python)
# ENDFOREACH(m)
# 
# ADD_CUSTOM_TARGET(PythonCompile ALL
#   ${PYTHON_EXECUTABLE}
#   ${PY_SITE_PACKAGES_PATH}/../compileall.py -l
#   -d "${CMAKE_INSTALL_PREFIX}/${WRAP_ITK_INSTALL_PREFIX}/lib"
#   ${WrapITK_BINARY_DIR}/lib
#   
#   COMMAND ${PYTHON_EXECUTABLE}
#   ${PY_SITE_PACKAGES_PATH}/../compileall.py -l
#   -d "${CMAKE_INSTALL_PREFIX}/${WRAP_ITK_INSTALL_PREFIX}/Python"
#   ${WrapITK_BINARY_DIR}/Python
#   
#   DEPENDS SwigRuntimePython ${PYTHON_MODULES}
# )


MACRO(END_WRAPPER_LIBRARY_PYTHON)

  SET(cpp_files )

  SET(python_files )

  SET(modules )
  
  # the list of interface this module depends
  SET(module_target_depend )
  FOREACH(dep ${WRAPPER_LIBRARY_DEPENDS})
    SET(module_target_depend ${module_target_depend} ${${dep}_SWIG_FILES})
  ENDFOREACH(dep)

  FOREACH(source ${WRAPPER_LIBRARY_CABLESWIG_INPUTS})
  
    GET_FILENAME_COMPONENT(base_name ${source} NAME_WE)
    STRING(REGEX REPLACE "^wrap_" "" group_name "${base_name}")
    
    # create the swig interface for all the groups in the module
    #
    SET(interface_file "${WRAPPER_MASTER_INDEX_OUTPUT_DIR}/${base_name}.i")
    SET(lib ${group_name}Python)
    SET(python_file "${LIBRARY_OUTPUT_PATH}/${lib}.py")
    SET(cpp_file "${CMAKE_CURRENT_BINARY_DIR}/${base_name}Python.cpp")

    ADD_CUSTOM_COMMAND(
      OUTPUT ${cpp_file} ${python_file}
      COMMAND swig -c++ -python -fcompact -O -features autodoc=1 -Werror -w508 -w312 -w314 -w509 -w302 -w362
      -w389 # operator[], to be suppressed later...
      -w384 -w383 # operator++ ane operator--
      -w361 # operator!
      -w467 # overloaded functions (with typemaps)
#      -l${WRAP_ITK_PYTHON_SOURCE_DIR}/python.i
      -o ${cpp_file}
#      -I${WRAPPER_MASTER_INDEX_OUTPUT_DIR}
      -outdir ${LIBRARY_OUTPUT_PATH}
      ${interface_file}
      WORKING_DIRECTORY ${WRAPPER_MASTER_INDEX_OUTPUT_DIR}/python
      DEPENDS ${interface_file} ${WRAPPER_MASTER_INDEX_OUTPUT_DIR}/python/${base_name}_ext.i ${WRAP_ITK_PYTHON_SOURCE_DIR}/python.i ${module_target_depend}
    )
    ADD_CUSTOM_TARGET(${base_name}SwigPython DEPENDS ${cpp_file})
    
    # add the current interface files to the deps
    SET(module_target_depend ${module_target_depend} ${interface_file})
    
    SET(cpp_files ${cpp_files} ${cpp_file})
    
    SET(modules ${modules} ${lib})

    SET(python_files ${python_files} ${python_file})

    ADD_LIBRARY(${lib} MODULE ${cpp_file})
    SET_TARGET_PROPERTIES(${lib} PROPERTIES PREFIX "_")
    IF(CMAKE_COMPILER_IS_GNUCC)
      SET_TARGET_PROPERTIES(${lib} PROPERTIES COMPILE_FLAGS "-fvisibility=hidden")
    ENDIF(CMAKE_COMPILER_IS_GNUCC)
    TARGET_LINK_LIBRARIES(${lib} ${WRAPPER_LIBRARY_LINK_LIBRARIES} ${PYTHON_LIBRARY})
    
  ENDFOREACH(source)
  
#  ADD_LIBRARY(${WRAPPER_LIBRARY_NAME}Python MODULE ${cpp_files})
#  SET_TARGET_PROPERTIES(${WRAPPER_LIBRARY_NAME}Python PROPERTIES PREFIX "_")
#  TARGET_LINK_LIBRARIES( ${WRAPPER_LIBRARY_NAME}Python
#    ${WRAPPER_LIBRARY_LINK_LIBRARIES} 
#    ${PYTHON_LIBRARY}
#  )

  ADD_CUSTOM_TARGET(${WRAPPER_LIBRARY_NAME}SwigPython DEPENDS ${cpp_files} ${python_files})
  
  ADD_CUSTOM_TARGET(${WRAPPER_LIBRARY_NAME}Python DEPENDS ${modules})


ENDMACRO(END_WRAPPER_LIBRARY_PYTHON)

MACRO(INCLUDE_WRAP_CMAKE_PYTHON module)

  # the default typemaps, exception handler, and includes
  SET(text "%include ${WRAP_ITK_PYTHON_SOURCE_DIR}/python.i\n\n")
  
  # add stream support only in one module, so it doesn't implemented in all the modules
  IF("${module}" STREQUAL "ITKCommonBase")
    SET(text "${text}%include std_iostream.i\n")
    SET(text "${text}%{\n")
    SET(text "${text}using namespace std;  // workaround a bug in swig where basic_string is used without the std:: prefix\n")
    SET(text "${text}%}\n")
    SET(text "${text}%include std_sstream.i\n\n")
  ENDIF("${module}" STREQUAL "ITKCommonBase")

  SET(WRAP_ITK_PYTHON_SWIG_EXT "${text}")

ENDMACRO(INCLUDE_WRAP_CMAKE_PYTHON)

MACRO(END_INCLUDE_WRAP_CMAKE_PYTHON module)
  # MESSAGE("${WRAP_ITK_PYTHON_SWIG_EXT}")
  CONFIGURE_FILE("${WRAP_ITK_PYTHON_SOURCE_DIR}/module_ext.i.in"
    "${WRAPPER_MASTER_INDEX_OUTPUT_DIR}/python/wrap_${module}_ext.i"
    @ONLY IMMEDIATE)
ENDMACRO(END_INCLUDE_WRAP_CMAKE_PYTHON)

MACRO(ADD_SIMPLE_TYPEDEF_PYTHON wrap_class swig_name)
  # split the class name and the template parameters
  IF("${wrap_class}" MATCHES "<.*>")
    STRING(REGEX REPLACE "^([^<]+)< *(.+) *>([^>]*)$" "\\1" cpp_name "${wrap_class}")
    STRING(REGEX REPLACE "^([^<]+)< *(.+) *>([^>]*)$" "\\2" template_params "${wrap_class}")
    STRING(REGEX REPLACE "^([^<]+)< *(.+) *>([^>]*)$" "\\3" ext_def "${wrap_class}")
  ELSE("${wrap_class}" MATCHES "<.*>")
    SET(cpp_name "${wrap_class}")
    SET(template_params NO_TEMPLATE)
    SET(ext_def "")
  ENDIF("${wrap_class}" MATCHES "<.*>")
  STRING(REGEX REPLACE ".*::" "" simple_name "${cpp_name}")
#  MESSAGE("${wrap_class} -- ${swig_name}")
#  MESSAGE("${cpp_name} -- ${template_params} -- ${ext_def}")

  # generate the python files, without taking care of the Superclasses
  IF(NOT "${swig_name}" MATCHES "Superclass")
    # TODO
  ENDIF(NOT "${swig_name}" MATCHES "Superclass")
  
  # and now, generate the typemaps and other customizations
  
  IF("${swig_name}" STREQUAL "itkLightObject")
    SET(text "\n\n")
    SET(text "${text}%extend itkLightObject {\n")
    SET(text "${text}  std::string __str__() {\n")
    SET(text "${text}    itk::OStringStream msg;\n")
    SET(text "${text}    self->Print( msg );\n")
    SET(text "${text}    return msg.str();\n")
    SET(text "${text}  }\n")
    SET(text "${text}}\n")
    SET(text "${text}\n\n")
#    
# A bug in swig currently prevent to use %extend on superclasses of smart pointed classes,
# without redefining the method in the subclasses, so implement the __str__ method in all
# the smart pointed classes (see below)
#    SET(WRAP_ITK_PYTHON_SWIG_EXT "${WRAP_ITK_PYTHON_SWIG_EXT}${text}")
  ENDIF("${swig_name}" STREQUAL "itkLightObject")
  
  IF("${wrap_class}" MATCHES "SmartPointer$")
    STRING(REGEX REPLACE "_Pointer$" "" smart_pointed "${swig_name}")
    ADD_PYTHON_POINTER_TYPEMAP("${smart_pointed}")

    SET(text "\n\n")
    SET(text "${text}%extend ${smart_pointed} {\n")
    SET(text "${text}  std::string __str__() {\n")
    SET(text "${text}    itk::OStringStream msg;\n")
    SET(text "${text}    self->Print( msg );\n")
    SET(text "${text}    return msg.str();\n")
    SET(text "${text}  }\n")
    SET(text "${text}}\n")
    SET(text "${text}\n\n")
#
# can't get it work neither - some protected methods of superclasses
# are exposed in the smart pointer. There must be somthing nasty with
# smart pointers and %extend
#    SET(WRAP_ITK_PYTHON_SWIG_EXT "${WRAP_ITK_PYTHON_SWIG_EXT}${text}")
  ENDIF("${wrap_class}" MATCHES "SmartPointer$")

  IF("${cpp_name}" STREQUAL "itk::Index")
    ADD_PYTHON_SEQ_TYPEMAP("${swig_name}" "${template_params}")
  ENDIF("${cpp_name}" STREQUAL "itk::Index")

  IF("${cpp_name}" STREQUAL "itk::Size")
    ADD_PYTHON_SEQ_TYPEMAP("${swig_name}" "${template_params}")
  ENDIF("${cpp_name}" STREQUAL "itk::Size")

#   IF("${cpp_name}" STREQUAL "itk::RGBPixel")
#     ADD_PYTHON_SEQ_TYPEMAP("${swig_name}" "${template_params}")
#   ENDIF("${cpp_name}" STREQUAL "itk::RGBPixel")

  IF("${cpp_name}" STREQUAL "itk::Offset")
    ADD_PYTHON_SEQ_TYPEMAP("${swig_name}" "${template_params}")
  ENDIF("${cpp_name}" STREQUAL "itk::Offset")

  IF("${cpp_name}" STREQUAL "itk::FixedArray")
    ADD_PYTHON_VEC_TYPEMAP("${swig_name}" "${template_params}")
  ENDIF("${cpp_name}" STREQUAL "itk::FixedArray")

  IF("${cpp_name}" STREQUAL "itk::Vector")
    ADD_PYTHON_VEC_TYPEMAP("${swig_name}" "${template_params}")
  ENDIF("${cpp_name}" STREQUAL "itk::Vector")

  IF("${cpp_name}" STREQUAL "itk::CovariantVector")
    ADD_PYTHON_VEC_TYPEMAP("${swig_name}" "${template_params}")
  ENDIF("${cpp_name}" STREQUAL "itk::CovariantVector")

  IF("${cpp_name}" STREQUAL "itk::Point")
    ADD_PYTHON_VEC_TYPEMAP("${swig_name}" "${template_params}")
  ENDIF("${cpp_name}" STREQUAL "itk::Point")

  IF("${cpp_name}" STREQUAL "itk::ContinuousIndex")
    ADD_PYTHON_VEC_TYPEMAP("${swig_name}" "${template_params}")
  ENDIF("${cpp_name}" STREQUAL "itk::ContinuousIndex")

  IF("${cpp_name}" STREQUAL "itk::Array")
    ADD_PYTHON_VARIABLE_LENGHT_SEQ_TYPEMAP("${swig_name}" "${template_params}")
  ENDIF("${cpp_name}" STREQUAL "itk::Array")
    
  IF("${cpp_name}" STREQUAL "itk::VectorContainer" AND NOT "${swig_name}" MATCHES "Pointer$")
    # add a template definition for the superclass which is not in ITK
    STRING(REGEX REPLACE "^[^,]+, *(.+) *$" "\\1" superclass_template_param "${template_params}")
    STRING(REPLACE "::" "" superclass_template_param "${superclass_template_param}")
    STRING(REPLACE "unsigned" "U" superclass_template_param "${superclass_template_param}")
    STRING(REPLACE "signed" "S" superclass_template_param "${superclass_template_param}")
    STRING(REPLACE "char" "C" superclass_template_param "${superclass_template_param}")
    STRING(REPLACE "short" "S" superclass_template_param "${superclass_template_param}")
    STRING(REPLACE "long" "L" superclass_template_param "${superclass_template_param}")
    STRING(REPLACE "float" "F" superclass_template_param "${superclass_template_param}")
    STRING(REPLACE "double" "D" superclass_template_param "${superclass_template_param}")
    STRING(REPLACE " " "" superclass_template_param "${superclass_template_param}")
    STRING(REPLACE "<" "" superclass_template_param "${superclass_template_param}")
    STRING(REPLACE ">" "" superclass_template_param "${superclass_template_param}")
    STRING(REPLACE "," "" superclass_template_param "${superclass_template_param}")
    SET(WRAP_ITK_PYTHON_SWIG_EXT "${WRAP_ITK_PYTHON_SWIG_EXT}%template(${swig_name}_Superclass) std::vector< ${superclass_template_param} >;\n")
  ENDIF("${cpp_name}" STREQUAL "itk::VectorContainer" AND NOT "${swig_name}" MATCHES "Pointer$")

ENDMACRO(ADD_SIMPLE_TYPEDEF_PYTHON)




MACRO(ADD_PYTHON_SEQ_TYPEMAP swig_name dim)
  SET(text "\n\n")
  SET(text "${text}%typemap(in) ${swig_name}& (${swig_name} itks) {\n")
  SET(text "${text}  if ((SWIG_ConvertPtr($input,(void **)(&$1),$1_descriptor, 0)) == -1) {\n")
  SET(text "${text}    PyErr_Clear();\n")
  SET(text "${text}    if (PySequence_Check($input) && PyObject_Length($input) == ${dim}) {\n")
  SET(text "${text}      for (int i =0; i < ${dim}; i++) {\n")
  SET(text "${text}          PyObject *o = PySequence_GetItem($input,i);\n")
  SET(text "${text}          if (!PyInt_Check(o)) {\n")
  SET(text "${text}            PyErr_SetString(PyExc_ValueError,\"Expecting a sequence of int\");\n")
  SET(text "${text}            return NULL;\n")
  SET(text "${text}          }\n")
  SET(text "${text}          itks[i] = PyInt_AsLong(o);\n")
  SET(text "${text}      }\n")
  SET(text "${text}      $1 = &itks;\n")
  SET(text "${text}    }else if (PyInt_Check($input)) {\n")
  SET(text "${text}      for (int i =0; i < ${dim}; i++) {\n")
  SET(text "${text}          itks[i] = PyInt_AsLong($input);\n")
  SET(text "${text}      }\n")
  SET(text "${text}      $1 = &itks;\n")
  SET(text "${text}    } else {\n")
  SET(text "${text}      SWIG_fail;\n")
  SET(text "${text}    }\n")
  SET(text "${text}  }\n")
  SET(text "${text}}\n")
  SET(text "${text}%typemap(typecheck) ${swig_name}& {\n")
  SET(text "${text}  void *ptr;\n")
  SET(text "${text}  if (SWIG_ConvertPtr($input, &ptr, $1_descriptor, 0) == -1\n")
  SET(text "${text}      && ( !PySequence_Check($input) || PyObject_Length($input) != ${dim} )\n")
  SET(text "${text}      && !PyInt_Check($input) ) {\n")
  SET(text "${text}    _v = 0;\n")
  SET(text "${text}    PyErr_Clear();\n")
  SET(text "${text}  } else {\n")
  SET(text "${text}    _v = 1;\n")
  SET(text "${text}  }\n")
  SET(text "${text}}\n")
  SET(text "${text}%typemap(in) ${swig_name} (${swig_name} itks) {\n")
  SET(text "${text}  ${swig_name} * s;\n")
  SET(text "${text}  if ((SWIG_ConvertPtr($input,(void **)(&s),$descriptor(${swig_name}*), 0)) == -1) {\n")
  SET(text "${text}    PyErr_Clear();\n")
  SET(text "${text}    if (PySequence_Check($input) && PyObject_Length($input) == ${dim}) {\n")
  SET(text "${text}      for (int i =0; i < ${dim}; i++) {\n")
  SET(text "${text}          PyObject *o = PySequence_GetItem($input,i);\n")
  SET(text "${text}          if (!PyInt_Check(o)) {\n")
  SET(text "${text}            PyErr_SetString(PyExc_ValueError,\"Expecting a sequence of int\");\n")
  SET(text "${text}            return NULL;\n")
  SET(text "${text}          }\n")
  SET(text "${text}         itks[i] = PyInt_AsLong(o);\n")
  SET(text "${text}      }\n")
  SET(text "${text}      $1 = itks;\n")
  SET(text "${text}    }else if (PyInt_Check($input)) {\n")
  SET(text "${text}      for (int i =0; i < ${dim}; i++) {\n")
  SET(text "${text}          itks[i] = PyInt_AsLong($input);\n")
  SET(text "${text}      }\n")
  SET(text "${text}      $1 = itks;\n")
  SET(text "${text}    } else {\n")
  SET(text "${text}      SWIG_fail;\n")
  SET(text "${text}    }\n")
  SET(text "${text}  } else if( s != NULL ) {\n")
  SET(text "${text}    $1 = *s;\n")
  SET(text "${text}  } else {\n")
  SET(text "${text}    PyErr_SetString(PyExc_ValueError, \"Value can't be None\");\n")
  SET(text "${text}    SWIG_fail;\n")
  SET(text "${text}  }\n")
  SET(text "${text}}\n")
  SET(text "${text}%typemap(typecheck) ${swig_name} {\n")
  SET(text "${text}  void *ptr;\n")
  SET(text "${text}  if (SWIG_ConvertPtr($input, &ptr, $descriptor(${swig_name}*), 0) == -1\n")
  SET(text "${text}       && ( !PySequence_Check($input) || PyObject_Length($input) != ${dim} )\n")
  SET(text "${text}       && !PyInt_Check($input) ) {\n")
  SET(text "${text}    _v = 0;\n")
  SET(text "${text}    PyErr_Clear();\n")
  SET(text "${text}  } else {\n")
  SET(text "${text}    _v = 1;\n")
  SET(text "${text}  }\n")
  SET(text "${text}}\n")
#  SET(text "${text}%{\n")
#  SET(text "${text}#include <itkMacro.h>")
#  SET(text "${text}%}\n")
  SET(text "${text}%extend ${swig_name} {\n")
  SET(text "${text}  long __getitem__(unsigned long dim) {\n")
  SET(text "${text}    if (dim >= ${dim}) { throw std::out_of_range(\"${swig_name} index out of range.\"); }\n")
  SET(text "${text}    return self->operator[]( dim );\n")
  SET(text "${text}  }\n")
  SET(text "${text}  void __setitem__(unsigned long dim, long int v) {\n")
  SET(text "${text}    if (dim >= ${dim}) { throw std::out_of_range(\"${swig_name} index out of range.\"); }\n")
  SET(text "${text}    self->operator[]( dim ) = v;\n")
  SET(text "${text}  }\n")
  SET(text "${text}  unsigned int __len__() {\n")
  SET(text "${text}    return ${dim};\n")
  SET(text "${text}  }\n")
  SET(text "${text}  std::string __repr__() {\n")
  SET(text "${text}    itk::OStringStream msg;\n")
  SET(text "${text}    msg << \"${swig_name}(\" << *self << \")\";\n")
  SET(text "${text}    return msg.str();\n")
  SET(text "${text}  }\n")
  SET(text "${text}}\n")
  SET(text "${text}\n\n")
  
  SET(WRAP_ITK_PYTHON_SWIG_EXT "${WRAP_ITK_PYTHON_SWIG_EXT}${text}")
ENDMACRO(ADD_PYTHON_SEQ_TYPEMAP)



MACRO(ADD_PYTHON_VEC_TYPEMAP swig_name template_params)
  STRING(REGEX REPLACE "(.*),(.*)" "\\1" type "${template_params}")
  STRING(REGEX REPLACE "(.*),(.*)" "\\2" dim "${template_params}")

  SET(text "\n\n")
  SET(text "${text}%typemap(in) ${swig_name}& (${swig_name} itks) {\n")
  SET(text "${text}  if ((SWIG_ConvertPtr($input,(void **)(&$1),$1_descriptor, 0)) == -1) {\n")
  SET(text "${text}    PyErr_Clear();\n")
  SET(text "${text}    if (PySequence_Check($input) && PyObject_Length($input) == ${dim}) {\n")
  SET(text "${text}      for (int i =0; i < ${dim}; i++) {\n")
  SET(text "${text}          PyObject *o = PySequence_GetItem($input,i);\n")
  SET(text "${text}          if (PyInt_Check(o)) {\n")
  SET(text "${text}            itks[i] = PyInt_AsLong(o);\n")
  SET(text "${text}          } else if (PyFloat_Check(o)) {\n")
  SET(text "${text}            itks[i] = (${type})PyFloat_AsDouble(o);\n")
  SET(text "${text}          } else {\n")
  SET(text "${text}            PyErr_SetString(PyExc_ValueError,\"Expecting a sequence of int or float\");\n")
  SET(text "${text}            return NULL;\n")
  SET(text "${text}          }\n")
  SET(text "${text}      }\n")
  SET(text "${text}      $1 = &itks;\n")
  SET(text "${text}    }else if (PyInt_Check($input)) {\n")
  SET(text "${text}      for (int i =0; i < ${dim}; i++) {\n")
  SET(text "${text}          itks[i] = PyInt_AsLong($input);\n")
  SET(text "${text}      }\n")
  SET(text "${text}      $1 = &itks;\n")
  SET(text "${text}    }else if (PyFloat_Check($input)) {\n")
  SET(text "${text}      for (int i =0; i < ${dim}; i++) {\n")
  SET(text "${text}          itks[i] = (${type})PyFloat_AsDouble($input);\n")
  SET(text "${text}      }\n")
  SET(text "${text}      $1 = &itks;\n")
  SET(text "${text}    } else {\n")
  SET(text "${text}      SWIG_fail;\n")
  SET(text "${text}    }\n")
  SET(text "${text}  }\n")
  SET(text "${text}}\n")
  SET(text "${text}%typemap(typecheck) ${swig_name}& {\n")
  SET(text "${text}  void *ptr;\n")
  SET(text "${text}  if (SWIG_ConvertPtr($input, &ptr, $1_descriptor, 0) == -1\n")
  SET(text "${text}      && ( !PySequence_Check($input) || PyObject_Length($input) != ${dim} )\n")
  SET(text "${text}      && !PyInt_Check($input) && !PyFloat_Check($input) ) {\n")
  SET(text "${text}    _v = 0;\n")
  SET(text "${text}    PyErr_Clear();\n")
  SET(text "${text}  } else {\n")
  SET(text "${text}    _v = 1;\n")
  SET(text "${text}  }\n")
  SET(text "${text}}\n")
  SET(text "${text}%typemap(in) ${swig_name} (${swig_name} itks) {\n")
  SET(text "${text}  ${swig_name} * s;\n")
  SET(text "${text}  if ((SWIG_ConvertPtr($input,(void **)(&s),$descriptor(${swig_name}*), 0)) == -1) {\n")
  SET(text "${text}    PyErr_Clear();\n")
  SET(text "${text}    if (PySequence_Check($input) && PyObject_Length($input) == ${dim}) {\n")
  SET(text "${text}      for (int i =0; i < ${dim}; i++) {\n")
  SET(text "${text}          PyObject *o = PySequence_GetItem($input,i);\n")
  SET(text "${text}          if (PyInt_Check(o)) {\n")
  SET(text "${text}            itks[i] = PyInt_AsLong(o);\n")
  SET(text "${text}          } else if (PyFloat_Check(o)) {\n")
  SET(text "${text}            itks[i] = (${type})PyFloat_AsDouble(o);\n")
  SET(text "${text}          } else {\n")
  SET(text "${text}            PyErr_SetString(PyExc_ValueError,\"Expecting a sequence of int or float\");\n")
  SET(text "${text}            return NULL;\n")
  SET(text "${text}          }\n")
  SET(text "${text}      }\n")
  SET(text "${text}      $1 = itks;\n")
  SET(text "${text}    }else if (PyInt_Check($input)) {\n")
  SET(text "${text}      for (int i =0; i < ${dim}; i++) {\n")
  SET(text "${text}          itks[i] = PyInt_AsLong($input);\n")
  SET(text "${text}      }\n")
  SET(text "${text}      $1 = itks;\n")
  SET(text "${text}    }else if (PyFloat_Check($input)) {\n")
  SET(text "${text}      for (int i =0; i < ${dim}; i++) {\n")
  SET(text "${text}          itks[i] = (${type})PyFloat_AsDouble($input);\n")
  SET(text "${text}      }\n")
  SET(text "${text}      $1 = itks;\n")
  SET(text "${text}    } else {\n")
  SET(text "${text}      SWIG_fail;\n")
  SET(text "${text}    }\n")
  SET(text "${text}  } else if( s != NULL ) {\n")
  SET(text "${text}    $1 = *s;\n")
  SET(text "${text} } else {\n")
  SET(text "${text}   PyErr_SetString(PyExc_ValueError, \"Value can't be None\");\n")
  SET(text "${text}   SWIG_fail;\n")
  SET(text "${text}  }\n")
  SET(text "${text}}\n")
  SET(text "${text}%typemap(typecheck) ${swig_name} {\n")
  SET(text "${text}  void *ptr;\n")
  SET(text "${text}  if (SWIG_ConvertPtr($input, &ptr, $descriptor(${swig_name}*), 0) == -1\n")
  SET(text "${text}       && ( !PySequence_Check($input) || PyObject_Length($input) != ${dim} )\n")
  SET(text "${text}      && !PyInt_Check($input) && !PyFloat_Check($input) ) {\n")
  SET(text "${text}    _v = 0;\n")
  SET(text "${text}    PyErr_Clear();\n")
  SET(text "${text}  } else {\n")
  SET(text "${text}    _v = 1;\n")
  SET(text "${text}  }\n")
  SET(text "${text}}\n")
  SET(text "${text}%extend ${swig_name} {\n")
  SET(text "${text}  ${type} __getitem__(unsigned long dim) {\n")
  SET(text "${text}    if (dim >= ${dim}) { throw std::out_of_range(\"${swig_name} index out of range.\"); }\n")
  SET(text "${text}    return self->operator[]( dim );\n")
  SET(text "${text}  }\n")
  SET(text "${text}  void __setitem__(unsigned long dim, ${type} v) {\n")
  SET(text "${text}    if (dim >= ${dim}) { throw std::out_of_range(\"${swig_name} index out of range.\"); }\n")
  SET(text "${text}    self->operator[]( dim ) = v;\n")
  SET(text "${text}  }\n")
  SET(text "${text}  unsigned int __len__() {\n")
  SET(text "${text}    return ${dim};\n")
  SET(text "${text}  }\n")
  SET(text "${text}  std::string __repr__() {\n")
  SET(text "${text}    itk::OStringStream msg;\n")
  SET(text "${text}    msg << \"${swig_name}(\" << *self << \")\";\n")
  SET(text "${text}    return msg.str();\n")
  SET(text "${text}  }\n")
  SET(text "${text}}\n")
  SET(text "${text}\n\n")
  
  SET(WRAP_ITK_PYTHON_SWIG_EXT "${WRAP_ITK_PYTHON_SWIG_EXT}${text}")
ENDMACRO(ADD_PYTHON_VEC_TYPEMAP)

MACRO(ADD_PYTHON_VARIABLE_LENGHT_SEQ_TYPEMAP type value_type)
  SET(text "\n\n")
  SET(text "${text}%typemap(in) ${type}& (${type} itks) {\n")
  SET(text "${text}  if ((SWIG_ConvertPtr($input,(void **)(&$1),$1_descriptor, 0)) == -1) {\n")
  SET(text "${text}    PyErr_Clear();\n")
  SET(text "${text}    itks = ${type}( PyObject_Length($input) );\n")
  SET(text "${text}    for (int i =0; i < itks.GetSize(); i++) {\n")
  SET(text "${text}      PyObject *o = PySequence_GetItem($input,i);\n")
  SET(text "${text}      if (PyInt_Check(o)) {\n")
  SET(text "${text}        itks[i] = (${value_type})PyInt_AsLong(o);\n")
  SET(text "${text}      } else if (PyFloat_Check(o)) {\n")
  SET(text "${text}        itks[i] = (${value_type})PyFloat_AsDouble(o);\n")
  SET(text "${text}      } else {\n")
  SET(text "${text}        PyErr_SetString(PyExc_ValueError,\"Expecting a sequence of int or float\");\n")
  SET(text "${text}        return NULL;\n")
  SET(text "${text}      }\n")
  SET(text "${text}    }\n")
  SET(text "${text}    $1 = &itks;\n")
  SET(text "${text}  }\n")
  SET(text "${text}}\n")
  SET(text "${text}%typemap(typecheck) ${type}& {\n")
  SET(text "${text}  void *ptr;\n")
  SET(text "${text}  if (SWIG_ConvertPtr($input, &ptr, $1_descriptor, 0) == -1\n")
  SET(text "${text}      && !PySequence_Check($input) ) {\n")
  SET(text "${text}    _v = 0;\n")
  SET(text "${text}    PyErr_Clear();\n")
  SET(text "${text}  } else {\n")
  SET(text "${text}    _v = 1;\n")
  SET(text "${text}  }\n")
  SET(text "${text}}\n")
  SET(text "${text}%typemap(in) ${type} (${type} itks) {\n")
  SET(text "${text}  ${type} * s;\n")
  SET(text "${text}  if ((SWIG_ConvertPtr($input,(void **)(&s),$descriptor(${type}*), 0)) == -1) {\n")
  SET(text "${text}    PyErr_Clear();\n")
  SET(text "${text}    itks = ${type}( PyObject_Length($input) );\n")
  SET(text "${text}    for (int i =0; i < itks.GetSize(); i++) {\n")
  SET(text "${text}      PyObject *o = PySequence_GetItem($input,i);\n")
  SET(text "${text}      if (PyInt_Check(o)) {\n")
  SET(text "${text}        itks[i] = (${value_type})PyInt_AsLong(o);\n")
  SET(text "${text}      } else if (PyFloat_Check(o)) {\n")
  SET(text "${text}        itks[i] = (${value_type})PyFloat_AsDouble(o);\n")
  SET(text "${text}      } else {\n")
  SET(text "${text}        PyErr_SetString(PyExc_ValueError,\"Expecting a sequence of int or float\");\n")
  SET(text "${text}        return NULL;\n")
  SET(text "${text}      }\n")
  SET(text "${text}    }\n")
  SET(text "${text}    $1 = itks;\n")
  SET(text "${text}  }\n")
  SET(text "${text}}\n")
  SET(text "${text}%typemap(typecheck) ${type} {\n")
  SET(text "${text}  void *ptr;\n")
  SET(text "${text}  if (SWIG_ConvertPtr($input, &ptr, $descriptor(${type}*), 0) == -1\n")
  SET(text "${text}      && !PySequence_Check($input) ) {\n")
  SET(text "${text}    _v = 0;\n")
  SET(text "${text}    PyErr_Clear();\n")
  SET(text "${text}  } else {\n")
  SET(text "${text}    _v = 1;\n")
  SET(text "${text}  }\n")
  SET(text "${text}}\n")
  SET(text "${text}%extend ${type} {\n")
  SET(text "${text}  ${value_type} __getitem__(unsigned long dim) {\n")
  SET(text "${text}    if (dim >= self->GetSize()) { throw std::out_of_range(\"${swig_name} index out of range.\"); }\n")
  SET(text "${text}    return self->operator[]( dim );\n")
  SET(text "${text}  }\n")
  SET(text "${text}  void __setitem__(unsigned long dim, ${value_type} v) {\n")
  SET(text "${text}    if (dim >= self->GetSize()) { throw std::out_of_range(\"${swig_name} index out of range.\"); }\n")
  SET(text "${text}    self->operator[]( dim ) = v;\n")
  SET(text "${text}  }\n")
  SET(text "${text}  unsigned int __len__() {\n")
  SET(text "${text}    return self->GetSize();\n")
  SET(text "${text}  }\n")
  SET(text "${text}  std::string __repr__() {\n")
  SET(text "${text}    itk::OStringStream msg;\n")
  SET(text "${text}    msg << \"${swig_name}(\" << *self << \")\";\n")
  SET(text "${text}    return msg.str();\n")
  SET(text "${text}  }\n")
  SET(text "${text}}\n")
  SET(text "${text}\n\n")
  
  SET(WRAP_ITK_PYTHON_SWIG_EXT "${WRAP_ITK_PYTHON_SWIG_EXT}${text}")
ENDMACRO(ADD_PYTHON_VARIABLE_LENGHT_SEQ_TYPEMAP)


MACRO(ADD_PYTHON_POINTER_TYPEMAP template_params)
  SET(text "\n\n")
  SET(text "${text} // Python typemaps for Smart Pointers to ${template_params} class. \n\n")
  SET(text "${text}%typemap(out) ${template_params} * {\n")
  SET(text "${text}  std::string methodName = \"\$symname\";\n")
  SET(text "${text}  if(methodName.find(\"GetPointer\") != -1) {\n")
  SET(text "${text}    // really return a pointer in that case\n")
  SET(text "${text}    \$result = SWIG_NewPointerObj((void *)(\$1), \$1_descriptor, 1);\n")
  SET(text "${text}  } else {\n")
  SET(text "${text}    ${template_params}_Pointer * ptr;\n")
  SET(text "${text}    ptr = new ${template_params}_Pointer(\$1);\n")
  SET(text "${text}    \$result = SWIG_NewPointerObj((void *)(ptr), \$descriptor(${template_params}_Pointer *), 1);\n")
  SET(text "${text}  }\n")
  SET(text "${text}}\n")
  SET(text "${text}%typemap(in) ${template_params} * {\n")
  SET(text "${text}  ${template_params}_Pointer * sptr;\n")
  SET(text "${text}  ${template_params} * ptr;\n")
  SET(text "${text}  // we must test this case first to avoid a segfault if arg is None\n")
  SET(text "${text}  if ((SWIG_ConvertPtr($input,(void **) &ptr, $1_descriptor, SWIG_POINTER_EXCEPTION)) != -1) {\n")
  SET(text "${text}    // we have a simple pointer. Just return it\n")
  SET(text "${text}    $1 = ptr;\n")
  SET(text "${text}  } else if ((SWIG_ConvertPtr($input,(void **) &sptr, $descriptor(${template_params}_Pointer *), SWIG_POINTER_EXCEPTION)) != -1) {\n")
  SET(text "${text}    // it's a SmartPointer. Get the pointer and return it\n")
  SET(text "${text}    $1 = sptr->GetPointer();\n")
  SET(text "${text}  } else {\n")
  SET(text "${text}    // not a pointer nor a SmartPointer... typemap fail !\n")
  SET(text "${text}    SWIG_fail;\n")
  SET(text "${text}  }\n")
  SET(text "${text}  // clean the error before exit\n")
  SET(text "${text}  PyErr_Clear();\n")
  SET(text "${text}}\n")
  SET(text "${text}%typemap(typecheck) ${template_params} * {\n")
  SET(text "${text}  void *ptr;\n")
  SET(text "${text}  if (SWIG_ConvertPtr(\$input, &ptr, \$1_descriptor, 0) == -1\n")
  SET(text "${text}      && SWIG_ConvertPtr(\$input, &ptr, \$descriptor(${template_params}_Pointer *), 0) == -1) {\n")
  SET(text "${text}    _v = 0;\n")
  SET(text "${text}    PyErr_Clear();\n")
  SET(text "${text}  } else {\n")
  SET(text "${text}    _v = 1;\n")
  SET(text "${text}  }\n")
  SET(text "${text}}\n")
  SET(text "${text}\n\n")
  
  SET(WRAP_ITK_PYTHON_SWIG_EXT "${WRAP_ITK_PYTHON_SWIG_EXT}${text}")
ENDMACRO(ADD_PYTHON_POINTER_TYPEMAP)


MACRO(CONFIGURE_PYTHON_CONFIG_FILES outdir)
  # Pull the WRAPPED_CLASSES list apart and use it to create Python-specific
  # support files. This also uses the global WRAPPER_LIBRARY_DEPENDS,
  # and WRAPPER_LIBRARY_NAME variables.
    
    SET(CONFIG_DEPENDS "")
  FOREACH(dep ${WRAPPER_LIBRARY_DEPENDS})
    SET(CONFIG_DEPENDS "${CONFIG_DEPENDS} '${dep}',")
  ENDFOREACH(dep)
  
  # Deal with the WRAPPED_CLASSES strings, which are in the format
  # "simple name # c++ name # swig name # c++ template parameters"    
  # or "simple name # c++ name # swig name # NO_TEMPLATE"
  # We want to change them to the format:
  # "  ('simple name', 'c++ name', 'swig name', 'template params'),\n"
  # or "  ('simple name', 'c++ name', 'swig name'),\n", respectively.
    
  SET(CONFIG_TEMPLATES "")
  FOREACH(wrapped_class ${WRAPPED_CLASSES})
    # first put the internal quotes in place
    STRING(REGEX REPLACE
      " # "
      "', '"
      py_template_def
      "${wrapped_class}")
    # now put the outside parens and quotes, etc. in place
    SET(py_template_def "  ('${py_template_def}'),\n")
    # now strip out the NO_TEMPLATE if there is none
    STRING(REGEX REPLACE
      ", 'NO_TEMPLATE'"
      ""
      py_template_def
      "${py_template_def}")
    SET(CONFIG_TEMPLATES "${CONFIG_TEMPLATES}${py_template_def}")
  ENDFOREACH(wrapped_class)
  
  CONFIGURE_FILE("${WRAP_ITK_CONFIG_DIR}/LanguageSupport/ModuleConfig.py.in"
    "${outdir}/${WRAPPER_LIBRARY_NAME}Config.py"
    @ONLY IMMEDIATE)
  WRAP_ITK_INSTALL("/Python/Configuration" "${outdir}/${WRAPPER_LIBRARY_NAME}Config.py")
ENDMACRO(CONFIGURE_PYTHON_CONFIG_FILES)

MACRO(CONFIGURE_PYTHON_LOADER_FILE outdir)
  # Create the loader file for importing just the current wrapper library. Uses
  # the global WRAPPER_LIBRARY_NAME variable.
  
  SET(CONFIG_LIBRARY_NAME "${WRAPPER_LIBRARY_NAME}")
  CONFIGURE_FILE("${WRAP_ITK_CONFIG_DIR}/LanguageSupport/ModuleLoader.py.in"
    "${outdir}/${WRAPPER_LIBRARY_NAME}.py"
    @ONLY IMMEDIATE)
ENDMACRO(CONFIGURE_PYTHON_LOADER_FILE)

MACRO(CONFIGURE_PYTHON_EXTERNAL_PROJECT_CONFIG outdir)
  # Create a helper file to set some sys.path entries so that external projects
  # can be easily loaded even when not installed. To use, call 'import ProjectConfig'
  # or 'import ProjectConfig-[Debug|Release|...]' if multiple build styles were
  # selected from an IDE. After this module is imported, the external project
  # can be easily imported by 'import ProjectName'.
  # If ProjectConfig was not used, the user would have to manually set sys.path
  # to point to *both* the Python directory in the WrapITK build tree and the
  # directory where the current project's SWIG libraries have been placed.
  
  IF(CMAKE_CONFIGURATION_TYPES)
    FOREACH(config ${CMAKE_CONFIGURATION_TYPES})
      # SWIG-generated libs and *.py files are sent to ${config} subdir
      SET(CONFIG_WRAP_ITK_PYTHON_DIR "${WrapITK_DIR}/Python/${config}")
      SET(CONFIG_PROJECT_PYTHON_DIR "${CMAKE_BINARY_DIR}/Python/${config}")
      SET(CONFIG_PROJECT_OUTPUT_DIR "${LIBRARY_OUTPUT_PATH}/${config}")
      CONFIGURE_FILE("${WRAP_ITK_CONFIG_DIR}/LanguageSupport/ExternalProjectConfig.py.in"
        "${outdir}/ProjectConfig_${config}.py"
        @ONLY IMMEDIATE)
      CONFIGURE_FILE("${WRAP_ITK_CONFIG_DIR}/LanguageSupport/ExternalProjectConfig.pth.in"
        "${outdir}/${config}/${PROJECT_NAME}.pth"
        @ONLY IMMEDIATE)
  ENDFOREACH(config)
  ELSE(CMAKE_CONFIGURATION_TYPES)
    SET(CONFIG_WRAP_ITK_PYTHON_DIR "${WrapITK_DIR}/Python")
    SET(CONFIG_PROJECT_PYTHON_DIR "${CMAKE_BINARY_DIR}/Python")
    SET(CONFIG_PROJECT_OUTPUT_DIR "${LIBRARY_OUTPUT_PATH}")
    CONFIGURE_FILE("${WRAP_ITK_CONFIG_DIR}/LanguageSupport/ExternalProjectConfig.py.in"
      "${outdir}/ProjectConfig.py"
      @ONLY IMMEDIATE)
    CONFIGURE_FILE("${WRAP_ITK_CONFIG_DIR}/LanguageSupport/ExternalProjectConfig.pth.in"
      "${outdir}/${PROJECT_NAME}.pth"
      @ONLY IMMEDIATE)
  ENDIF(CMAKE_CONFIGURATION_TYPES)
ENDMACRO(CONFIGURE_PYTHON_EXTERNAL_PROJECT_CONFIG)


MACRO(PYTHON_SUPPORT_CONFIGURE_FILES)
  # Create the various files to make it easier to use the ITK wrappers, especially
  # with reference to the multitude of templates.
  # Currently, only Python is supported.
  
    CONFIGURE_PYTHON_CONFIG_FILES("${PROJECT_BINARY_DIR}/Python/Configuration")      
    IF(CMAKE_CONFIGURATION_TYPES)
      FOREACH(config ${CMAKE_CONFIGURATION_TYPES})
        CONFIGURE_PYTHON_LOADER_FILE("${PROJECT_BINARY_DIR}/Python/${config}")
      ENDFOREACH(config)
    ELSE(CMAKE_CONFIGURATION_TYPES)
      CONFIGURE_PYTHON_LOADER_FILE("${PROJECT_BINARY_DIR}/Python/")
    ENDIF(CMAKE_CONFIGURATION_TYPES)
    # Just install the files once, regardless of how many different places
    # they were configured into. If there are no configuration types, the 
    # INTDIR variable expands to '', so no harm done.
    WRAP_ITK_INSTALL("/Python" "${PROJECT_BINARY_DIR}/Python/${WRAP_ITK_INSTALL_INTDIR}${WRAPPER_LIBRARY_NAME}.py")
    IF(EXTERNAL_WRAP_ITK_PROJECT)
      # Configure a python file to make it easier to use this external project
      # without first installing it into WrapITK.
      CONFIGURE_PYTHON_EXTERNAL_PROJECT_CONFIG("${PROJECT_BINARY_DIR}/Python/")
    ENDIF(EXTERNAL_WRAP_ITK_PROJECT)
ENDMACRO(PYTHON_SUPPORT_CONFIGURE_FILES)


###############################################################################
# Create the PyUtils library
# SUBDIRS(PyUtils)
SUBDIRS(Tests)
SUBDIRS(itkExtras)


