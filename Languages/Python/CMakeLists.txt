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
                   "${WRAP_ITK_PYTHON_BINARY_DIR}/${config}/itkConfig.py"
                   @ONLY IMMEDIATE)
  ENDFOREACH(config)
ELSE(CMAKE_CONFIGURATION_TYPES)
  SET(CONFIG_WRAP_ITK_DATA_ROOT "../Data")
  SET(CONFIG_WRAP_ITK_TEST_ROOT "../Testing")
  SET(CONFIG_PYTHON_CONFIGPY_DIR "Configuration")

  SET(CONFIG_PYTHON_SWIGPY_DIR "../lib")
  SET(CONFIG_PYTHON_SWIGLIB_DIR "../lib")
  CONFIGURE_FILE("${CMAKE_CURRENT_SOURCE_DIR}/itkConfig.py.in"
                 "${WRAP_ITK_PYTHON_BINARY_DIR}/itkConfig.py"
                 @ONLY IMMEDIATE)
ENDIF(CMAKE_CONFIGURATION_TYPES)

SET(CONFIG_WRAP_ITK_TEST_ROOT "None")
SET(CONFIG_PYTHON_SWIGLIB_DIR "../lib")
SET(CONFIG_PYTHON_SWIGPY_DIR "../lib")
SET(CONFIG_PYTHON_CONFIGPY_DIR "Configuration")
CONFIGURE_FILE("${CMAKE_CURRENT_SOURCE_DIR}/itkConfig.py.in"
               "${WRAP_ITK_PYTHON_BINARY_DIR}/InstallOnly/itkConfig.py"
              @ONLY IMMEDIATE)

WRAP_ITK_INSTALL(/Python "${WRAP_ITK_PYTHON_BINARY_DIR}/InstallOnly/itkConfig.py")


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


MACRO(WRAP_LIBRARY_PYTHON library_name)
  SET(WRAP_ITK_PYTHON_CONFIGURATION_TEMPLATES "")
  SET(WRAP_ITK_PYTHON_LIBRARY_MODULE "")
ENDMACRO(WRAP_LIBRARY_PYTHON)


MACRO(END_WRAP_LIBRARY_PYTHON)

  SET(cpp_files )

  SET(python_files )

  SET(modules )
  
  # the list of interface this module depends and build the deps for the python configuration file
  SET(module_target_depend )
  SET(WRAP_ITK_PYTHON_CONFIGURATION_DEPENDS "")
  FOREACH(dep ${WRAPPER_LIBRARY_DEPENDS})
    SET(module_target_depend ${module_target_depend} ${${dep}_SWIG_FILES})
    SET(WRAP_ITK_PYTHON_CONFIGURATION_DEPENDS "${WRAP_ITK_PYTHON_CONFIGURATION_DEPENDS} '${dep}',")  
  ENDFOREACH(dep)
  
  # create the python config file
  CONFIGURE_FILE("${WRAP_ITK_PYTHON_SOURCE_DIR}/ModuleConfig.py.in"
    "${WRAP_ITK_PYTHON_BINARY_DIR}/Configuration/${WRAPPER_LIBRARY_NAME}Config.py"
    @ONLY IMMEDIATE)
    
  # create the lib module python file
  SET(WRAP_ITK_FILE_CONTENT "${WRAP_ITK_PYTHON_LIBRARY_MODULE}")
  CONFIGURE_FILE("${WrapITK_SOURCE_DIR}/ConfigurationInputs/empty.in"
    "${WRAP_ITK_PYTHON_BINARY_DIR}/${WRAPPER_LIBRARY_NAME}Python.py"
    @ONLY IMMEDIATE)

  # create the advanced lib module python file
  SET(CONFIG_LIBRARY_NAME "${WRAPPER_LIBRARY_NAME}")
  CONFIGURE_FILE("${WRAP_ITK_PYTHON_SOURCE_DIR}/ModuleLoader.py.in"
    "${WRAP_ITK_PYTHON_BINARY_DIR}/${WRAPPER_LIBRARY_NAME}.py"
    @ONLY IMMEDIATE)

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
    TARGET_LINK_LIBRARIES(${lib} ${WRAPPER_LIBRARY_LINK_LIBRARIES} ${PYTHON_LIBRARY})
    
# gcc visibility can't be used without getting errors when passing objects
# from one module to an other
#
#    IF(CMAKE_COMPILER_IS_GNUCC)
#      SET_TARGET_PROPERTIES(${lib} PROPERTIES COMPILE_FLAGS "-fvisibility=hidden")
#    ENDIF(CMAKE_COMPILER_IS_GNUCC)
    
  ENDFOREACH(source)
  
#  ADD_LIBRARY(${WRAPPER_LIBRARY_NAME}Python MODULE ${cpp_files})
#  SET_TARGET_PROPERTIES(${WRAPPER_LIBRARY_NAME}Python PROPERTIES PREFIX "_")
#  TARGET_LINK_LIBRARIES( ${WRAPPER_LIBRARY_NAME}Python
#    ${WRAPPER_LIBRARY_LINK_LIBRARIES} 
#    ${PYTHON_LIBRARY}
#  )

  ADD_CUSTOM_TARGET(${WRAPPER_LIBRARY_NAME}SwigPython DEPENDS ${cpp_files} ${python_files})
  
  ADD_CUSTOM_TARGET(${WRAPPER_LIBRARY_NAME}Python DEPENDS ${modules})

ENDMACRO(END_WRAP_LIBRARY_PYTHON)


MACRO(ADD_ONE_TYPEDEF_PYTHON wrap_method wrap_class swig_name template_params)
  # ('simple name', 'c++ name', 'swig name', 'template params')
  STRING(REGEX REPLACE "(.*::)" "" base_name "${wrap_class}")
  
  ADD_PYTHON_CONFIG_TEMPLATE("${base_name}" "${wrap_class}" "${swig_name}" "${template_params}")
  IF("${wrap_method}" MATCHES "POINTER")
    IF("${template_params}" STREQUAL "")
      ADD_PYTHON_CONFIG_TEMPLATE("SmartPointer" "itk::SmartPointer" "${swig_name}_Pointer" "${wrap_class}")
    ELSE("${template_params}" STREQUAL "")
      ADD_PYTHON_CONFIG_TEMPLATE("SmartPointer" "itk::SmartPointer" "${swig_name}_Pointer" "${wrap_class}< ${template_params} >")
    ENDIF("${template_params}" STREQUAL "")
  ENDIF("${wrap_method}" MATCHES "POINTER")
  
  # std::complex and vcl_complex are the same classes, but python don't know that
  IF("${wrap_class}" STREQUAL "vcl_complex")
    ADD_PYTHON_CONFIG_TEMPLATE("complex" "std::complex" "${swig_name}" "${template_params}")
  ENDIF("${wrap_class}" STREQUAL "vcl_complex")

ENDMACRO(ADD_ONE_TYPEDEF_PYTHON)


MACRO(ADD_PYTHON_CONFIG_TEMPLATE base_name wrap_class swig_name template_params)

  IF("${template_params}" STREQUAL "")
    SET(WRAP_ITK_PYTHON_CONFIGURATION_TEMPLATES "${WRAP_ITK_PYTHON_CONFIGURATION_TEMPLATES}  ('${base_name}', '${wrap_class}', '${swig_name}'),\n")
  ELSE("${template_params}" STREQUAL "")
    SET(WRAP_ITK_PYTHON_CONFIGURATION_TEMPLATES "${WRAP_ITK_PYTHON_CONFIGURATION_TEMPLATES}  ('${base_name}', '${wrap_class}', '${swig_name}', '${template_params}'),\n")
  ENDIF("${template_params}" STREQUAL "")
    
ENDMACRO(ADD_PYTHON_CONFIG_TEMPLATE)


MACRO(INCLUDE_WRAP_CMAKE_PYTHON module)

  SET(text "")
  
  # add stream support only in one module, so it doesn't implemented in all the modules
  IF("${module}" STREQUAL "ITKCommonBase")
    SET(text "${text}%include std_iostream.i\n")
    SET(text "${text}%include std_sstream.i\n\n")
    SET(text "${text}%include <std_vector.i>\n")
    SET(text "${text}%include <std_map.i>\n")
    SET(text "${text}%include <std_list.i>\n\n")

    # add the vars defined by including std_iostream and std_stream to the python config
    ADD_PYTHON_CONFIG_TEMPLATE("PySwigIterator" "PySwigIterator" "PySwigIterator" "")
    ADD_PYTHON_CONFIG_TEMPLATE("cerr" "std::cerr" "cerr" "")
    ADD_PYTHON_CONFIG_TEMPLATE("cin" "std::cin" "cin" "")
    ADD_PYTHON_CONFIG_TEMPLATE("clog" "std::clog" "clog" "")
    ADD_PYTHON_CONFIG_TEMPLATE("cout" "std::cout" "cout" "")
    ADD_PYTHON_CONFIG_TEMPLATE("cvar" "std::cvar" "cvar" "")
    ADD_PYTHON_CONFIG_TEMPLATE("endl" "std::endl" "endl" "")
    ADD_PYTHON_CONFIG_TEMPLATE("ends" "std::ends" "ends" "")
    ADD_PYTHON_CONFIG_TEMPLATE("flush" "std::flush" "flush" "")
    ADD_PYTHON_CONFIG_TEMPLATE("ios" "std::ios" "ios" "")
    ADD_PYTHON_CONFIG_TEMPLATE("ios_base" "std::ios_base" "ios_base" "")
    ADD_PYTHON_CONFIG_TEMPLATE("ios_base_sync_with_stdio" "std::ios_base_sync_with_stdio" "ios_base_sync_with_stdio" "")
    ADD_PYTHON_CONFIG_TEMPLATE("ios_base_xalloc" "std::ios_base_xalloc" "ios_base_xalloc" "")
    ADD_PYTHON_CONFIG_TEMPLATE("iostream" "std::iostream" "iostream" "")
    ADD_PYTHON_CONFIG_TEMPLATE("istream" "std::istream" "istream" "")
    ADD_PYTHON_CONFIG_TEMPLATE("istringstream" "std::istringstream" "istringstream" "")
    ADD_PYTHON_CONFIG_TEMPLATE("ostream" "std::ostream" "ostream" "")
    ADD_PYTHON_CONFIG_TEMPLATE("ostringstream" "std::ostringstream" "ostringstream" "")
    ADD_PYTHON_CONFIG_TEMPLATE("streambuf" "std::streambuf" "streambuf" "")
    ADD_PYTHON_CONFIG_TEMPLATE("string" "std::string" "string" "")
    ADD_PYTHON_CONFIG_TEMPLATE("stringstream" "std::stringstream" "stringstream" "")

    # include std_strin.i here instead of python.i to workaround a bug when std_string.i
    # is included before std_sstream.i (bug #1607576)
    SET(text "${text}%include std_string.i\n\n")
    
    SET(text "${text}%template(vectorString) std::vector< std::string >;\n")
    ADD_PYTHON_CONFIG_TEMPLATE("vector" "std::vector" "vectorString" "std::string")

    SET(text "${text}%template(listString) std::list< std::string >;\n\n")
    ADD_PYTHON_CONFIG_TEMPLATE("list" "std::list" "listString" "std::string")

  ENDIF("${module}" STREQUAL "ITKCommonBase")

  IF("${module}" STREQUAL "itkVectorContainer")
    FOREACH(t B UC US UL SC SS SL F D)
      SET(text "${text}%template(vector${t}) std::vector< ${ITKT_${t}} >;\n")
      ADD_PYTHON_CONFIG_TEMPLATE("vector" "std::vector" "vector${t}" "${ITKT_${t}}")
    ENDFOREACH(t)
  ENDIF("${module}" STREQUAL "itkVectorContainer")

  IF("${module}" STREQUAL "itkMapContainer")
    SET(text "${text}%template(mapULD) std::map< unsigned long, double >;\n")
    ADD_PYTHON_CONFIG_TEMPLATE("map" "std::map" "mapULD" "unsigned long, double")
  ENDIF("${module}" STREQUAL "itkMapContainer")

  SET(text "${text}\n\n")

  # the default typemaps, exception handler, and includes
  SET(text "${text}%include ${WRAP_ITK_PYTHON_SOURCE_DIR}/python.i\n\n")
  
  SET(WRAP_ITK_PYTHON_SWIG_EXT "${text}")
  
  # register the module for the lib module
  SET(WRAP_ITK_PYTHON_LIBRARY_MODULE "${WRAP_ITK_PYTHON_LIBRARY_MODULE}from ${module}Python import *\n")

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
# the smart pointed classes (see below) (bug #1607365)
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
    IF("${superclass_template_param}" MATCHES "::")
      SET(param "${superclass_template_param}")
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
      ADD_PYTHON_CONFIG_TEMPLATE("vector" "std::vector" "${swig_name}_Superclass" "${param}")
    ENDIF("${superclass_template_param}" MATCHES "::")
  ENDIF("${cpp_name}" STREQUAL "itk::VectorContainer" AND NOT "${swig_name}" MATCHES "Pointer$")

  IF("${cpp_name}" STREQUAL "itk::MapContainer" AND NOT "${swig_name}" MATCHES "Pointer$")
    # add a template definition for the superclass which is not in ITK
    STRING(REGEX REPLACE "^[^,]+, *(.+) *$" "\\1" superclass_template_param "${template_params}")
    IF("${superclass_template_param}" MATCHES "::")
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
      SET(WRAP_ITK_PYTHON_SWIG_EXT "${WRAP_ITK_PYTHON_SWIG_EXT}%template(${swig_name}_Superclass) std::map< unsigned long, ${superclass_template_param}, std::less< unsigned long > >;\n")
    ENDIF("${superclass_template_param}" MATCHES "::")
  ENDIF("${cpp_name}" STREQUAL "itk::MapContainer" AND NOT "${swig_name}" MATCHES "Pointer$")

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
  SET(text "${text}    if (dim >= self->GetSize()) { throw std::out_of_range(\"${type} index out of range.\"); }\n")
  SET(text "${text}    return self->operator[]( dim );\n")
  SET(text "${text}  }\n")
  SET(text "${text}  void __setitem__(unsigned long dim, ${value_type} v) {\n")
  SET(text "${text}    if (dim >= self->GetSize()) { throw std::out_of_range(\"${type} index out of range.\"); }\n")
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


