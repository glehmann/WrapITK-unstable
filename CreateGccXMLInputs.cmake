
SET(WRAPPER_MASTER_INDEX_OUTPUT_DIR "${PROJECT_BINARY_DIR}/ClassIndex")
SET(WRAPPER_SWIG_LIBRARY_OUTPUT_DIR "${PROJECT_BINARY_DIR}/SWIG")

################################################################################
# Macros for writing the global module CableSwig inputs which specify all the
# groups to be bundled together into one module. 
################################################################################

MACRO(WRITE_MODULE_FILES)
#   # Write the wrap_LIBRARY_NAME.cxx file which specifies all the wrapped groups.
#   
#   MESSAGE(STATUS "${WRAPPER_LIBRARY_NAME}: Creating module wrapper files.")
# 
#   
#   SET(group_list "")
#   FOREACH(group_name ${WRAPPER_LIBRARY_GROUPS})
#     SET(group_list "${group_list}    \"${group_name}\",\n")
#   ENDFOREACH(group_name ${group})
#   STRING(REGEX REPLACE ",\n$" "\n" group_list "${group_list}")
# 
#   SET(CONFIG_GROUP_LIST "${group_list}")
#   
#   # Create the cxx file.
#   SET(cxx_file "${WRAPPER_LIBRARY_OUTPUT_DIR}/wrap_${WRAPPER_LIBRARY_NAME}.cxx")
#   CONFIGURE_FILE("${WRAP_ITK_CONFIG_DIR}/wrap_ITK.cxx.in"
#     "${cxx_file}" @ONLY IMMEDIATE)
#   
# 
#   IF(WRAP_ITK_TCL)
#     WRITE_MODULE_FOR_LANGUAGE("Tcl")
#   ENDIF(WRAP_ITK_TCL)
#   IF(WRAP_ITK_PYTHON)
#     WRITE_MODULE_FOR_LANGUAGE("Python")
#   ENDIF(WRAP_ITK_PYTHON)
#   IF(WRAP_ITK_JAVA)
#     WRITE_MODULE_FOR_LANGUAGE("Java")
#   ENDIF(WRAP_ITK_JAVA)
#   IF(WRAP_ITK_PERL)
#     WRITE_MODULE_FOR_LANGUAGE("Perl")
#   ENDIF(WRAP_ITK_PERL)
ENDMACRO(WRITE_MODULE_FILES)

MACRO(WRITE_MODULE_FOR_LANGUAGE language)
#   # Write the language specific CableSwig input which declares which language is
#   # to be used and includes the general module cableswig input.
#   SET(CONFIG_LANGUAGE "${language}")
#   SET(CONFIG_MODULE_NAME ${WRAPPER_LIBRARY_NAME})
#   STRING(TOUPPER ${language} CONFIG_UPPER_LANG)
#   
#   # Create the cxx file.
#   SET(cxx_file "${WRAPPER_LIBRARY_OUTPUT_DIR}/wrap_${WRAPPER_LIBRARY_NAME}${language}.cxx")  
#   CONFIGURE_FILE("${WRAP_ITK_CONFIG_DIR}/wrap_ITKLang.cxx.in"
#     "${cxx_file}" @ONLY IMMEDIATE)
#   
ENDMACRO(WRITE_MODULE_FOR_LANGUAGE)


MACRO(WRAP_INCLUDE_CABLE_SWIG include_file)
  IF("${include_file}" MATCHES "<.*>")
    SET(GCC_XML_INCLUDES "${GCC_XML_INCLUDES}#include ${include_file}\n")
  ELSE("${include_file}" MATCHES "<.*>")
    SET(GCC_XML_INCLUDES "${GCC_XML_INCLUDES}#include \"${include_file}\"\n")
  ENDIF("${include_file}" MATCHES "<.*>")
ENDMACRO(WRAP_INCLUDE_CABLE_SWIG)


MACRO(ADD_SIMPLE_TYPEDEF_CABLE_SWIG wrap_class swig_name)
  SET(GCC_XML_TYPEDEFS "${GCC_XML_TYPEDEFS}      typedef ${wrap_class} ${swig_name};\n")
ENDMACRO(ADD_SIMPLE_TYPEDEF_CABLE_SWIG)


MACRO(INCLUDE_WRAP_CMAKE_CABLE_SWIG module)
  # clear the typedefs and the includes
  SET(GCC_XML_TYPEDEFS )
  SET(GCC_XML_INCLUDES )
  SET(GCC_XML_FORCE_INSTANTIATE )
ENDMACRO(INCLUDE_WRAP_CMAKE_CABLE_SWIG)

MACRO(END_INCLUDE_WRAP_CMAKE_CABLE_SWIG module)
  # write the wrap_*.cxx file
  #
  # Global vars used: WRAPPER_INCLUDE_FILES WRAPPER_MODULE_NAME and WRAPPER_TYPEDEFS
  # Global vars modified: none

#   MESSAGE("${GCC_XML_INCLUDES}${GCC_XML_TYPEDEFS}")

  # Create the cxx file.
  SET(file_name "wrap_${module}.cxx")
  SET(cxx_file "${WRAPPER_LIBRARY_OUTPUT_DIR}/${file_name}")
  SET(CONFIG_WRAPPER_INCLUDES "${GCC_XML_INCLUDES}")
  SET(CONFIG_WRAPPER_MODULE_NAME "${WRAPPER_MODULE_NAME}")
  SET(CONFIG_WRAPPER_TYPEDEFS "${GCC_XML_TYPEDEFS}")
  SET(CONFIG_WRAPPER_FORCE_INSTANTIATE "${GCC_XML_FORCE_INSTANTIATE}")
  CONFIGURE_FILE("${WRAP_ITK_CONFIG_DIR}/wrap_.cxx.in"
    "${cxx_file}" @ONLY IMMEDIATE)
  
  # generate the xml file
  SET(gccxml_inc_file "${WRAPPER_LIBRARY_OUTPUT_DIR}/gcc_xml.inc")
  SET(xml_file "${WRAPPER_LIBRARY_OUTPUT_DIR}/wrap_${module}.xml")
  ADD_CUSTOM_COMMAND(
    OUTPUT ${xml_file}
    COMMAND ${GCCXML}
          -fxml-start=_cable_
          -fxml=${xml_file}
          --gccxml-gcc-options ${gccxml_inc_file}
          -DCSWIG
          -DCABLE_CONFIGURATION
          ${cxx_file}
    DEPENDS ${GCCXML} ${cxx_file} ${gccxml_inc_file}
  )
  ADD_CUSTOM_TARGET(${module}Xml DEPENDS ${xml_file})
  
ENDMACRO(END_INCLUDE_WRAP_CMAKE_CABLE_SWIG)


MACRO(ADD_ONE_TYPEDEF_CABLE_SWIG  wrap_method wrap_class swig_name template_params)
  # insert a blank line to separate the classes
  SET(GCC_XML_TYPEDEFS "${GCC_XML_TYPEDEFS}\n")
  IF("${wrap_method}" MATCHES "FORCE_INSTANTIATE")
    # add a peace of code for type instantiation
    SET(GCC_XML_FORCE_INSTANTIATE "${GCC_XML_FORCE_INSTANTIATE}  sizeof(${swig_name});\n")
  ENDIF("${wrap_method}" MATCHES "FORCE_INSTANTIATE")
ENDMACRO(ADD_ONE_TYPEDEF_CABLE_SWIG)

MACRO(WRAP_LIBRARY_CABLE_SWIG library_name)
  # create the files used to pass the file to include to gccxml
  SET(gccxml_inc_file "${WRAPPER_LIBRARY_OUTPUT_DIR}/gcc_xml.inc")
  SET(CONFIG_GCCXML_INC_CONTENTS)
  GET_DIRECTORY_PROPERTY(include_dir_list INCLUDE_DIRECTORIES)
  FOREACH(dir ${include_dir_list})
    SET(CONFIG_GCCXML_INC_CONTENTS "${CONFIG_GCCXML_INC_CONTENTS}-I${dir}\n")
  ENDFOREACH(dir)
  CONFIGURE_FILE("${WRAP_ITK_CONFIG_DIR}/gcc_xml.inc.in" "${gccxml_inc_file}"
    @ONLY IMMEDIATE)
ENDMACRO(WRAP_LIBRARY_CABLE_SWIG)
