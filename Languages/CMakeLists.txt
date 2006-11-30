




# the macro in charge of dispatching to the language specific macros

MACRO(WRAP_CLASS_ALL_LANGUAGES)
ENDMACRO(WRAP_CLASS_ALL_LANGUAGES)

MACRO(WRAP_NON_TEMPLATE_CLASS_ALL_LANGUAGES class)
ENDMACRO(WRAP_NON_TEMPLATE_CLASS_ALL_LANGUAGES class)

MACRO(END_WRAP_CLASS_ALL_LANGUAGES)
ENDMACRO(END_WRAP_CLASS_ALL_LANGUAGES)

MACRO(ADD_SIMPLE_TYPEDEF_ALL_LANGUAGES wrap_class swig_name)
ENDMACRO(ADD_SIMPLE_TYPEDEF_ALL_LANGUAGES wrap_class swig_name)

MACRO(END_WRAPPER_LIBRARY_ALL_LANGUAGES)
  END_WRAPPER_LIBRARY_PYTHON()
ENDMACRO(END_WRAPPER_LIBRARY_ALL_LANGUAGES)









################################################################################
# Macros to collect information about wrapped types and module dependencies
# so that support files for given languages can be created to automatically
# load the modules in the right order and provide support for looking up
# templated types.
# Currently only Python support is implemented.
################################################################################


MACRO(LANGUAGE_SUPPORT_INITIALIZE)
  # Re-set the WRAPPED_CLASSES variable used to collect class and template data.
  # This variable holds a list of strings of the one of two forms:
  #
  # "simple name # c++ name # swig name # c++ template parameters"
  # where 'simple name' is the name the class should have in the wrapped code
  # (e.g. drop the itk), 'c++ name' is the name of the templated class in c++ 
  # (not including the template parameters!), 'swig name' is the name of this
  # particular template instantiation in the swig wrappers (e.g. itkImageF2),
  # and 'c++ template parameters' are the raw text between the template angle
  # brackets (e.g. the ... in itk::Image<...>) for this template instantiation.
  #
  # or "simple name # c++ name # swig name # NO_TEMPLATE"
  # where simple name is the same as above, 'c++ name' is the name of the class
  # in c++, and 'swig name' is the name of the class in the swig wrappers.
  # 
  # Also re-set the WRAPPER_TYPEMAPS variable, which holds the text of SWIG
  # typemaps generated for smart pointers wrapped in this library.

  SET(WRAPPED_CLASSES)
  SET(WRAPPER_TYPEMAPS)
ENDMACRO(LANGUAGE_SUPPORT_INITIALIZE)


MACRO(LANGUAGE_SUPPORT_CONFIGURE_FILES)
  # Create the various files to make it easier to use the ITK wrappers, especially
  # with reference to the multitude of templates.
  # Currently, only Python is supported.
  
  MESSAGE(STATUS "${WRAPPER_LIBRARY_NAME}: Creating language support files.")

  CONFIGURE_TYPEMAPS("${WRAPPER_SWIG_LIBRARY_OUTPUT_DIR}")
  
  IF(WRAP_ITK_PYTHON AND WRAPPER_LIBRARY_PYTHON)
    PYTHON_SUPPORT_CONFIGURE_FILES()
  ENDIF(WRAP_ITK_PYTHON AND WRAPPER_LIBRARY_PYTHON)

  IF(WRAP_ITK_TCL AND WRAPPER_LIBRARY_TCL)
    TCL_SUPPORT_CONFIGURE_FILES()
  ENDIF(WRAP_ITK_TCL AND WRAPPER_LIBRARY_TCL)

  IF(WRAP_ITK_JAVA AND WRAPPER_LIBRARY_JAVA)
    JAVA_SUPPORT_CONFIGURE_FILES()
  ENDIF(WRAP_ITK_JAVA AND WRAPPER_LIBRARY_JAVA)

ENDMACRO(LANGUAGE_SUPPORT_CONFIGURE_FILES)


MACRO(LANGUAGE_SUPPORT_ADD_CLASS simple_name cpp_name swig_name template_parameters)
  # Add the template definitions to the WRAPPED_CLASSES list,
  # where 'simple_name' is the name the class should have in the wrapped code
  # (e.g. drop the itk), 'cpp_name' is the name of the templated class in c++ 
  # (not including the template parameters!), 'swig_name' is the name of this
  # particular template instantiation in the swig wrappers (e.g. itkImageF2)
  # or just the base name if this isn't a templated class,  and
  # 'template_params' are the raw text between the template angle brackets
  # (e.g. the ... in itk::Image<...>) for this template instantiation.
  # Leave template params empty (e.g. "") for non-template classes.
  #
  # We use this data to create our string of the form
  # "simple name # c++ name # swig name # c++ template parameters"
  # or "simple name # c++ name # swig name # NO_TEMPLATE"
  # as required above.

  # the var passed in parameters of the macro can't be modified, so use a different name
  IF("${template_parameters}" STREQUAL "")
    SET(template_params "NO_TEMPLATE")
  ELSE("${template_parameters}" STREQUAL "")
    SET(template_params "${template_parameters}")
  ENDIF("${template_parameters}" STREQUAL "")

  SET(WRAPPED_CLASSES ${WRAPPED_CLASSES} "${simple_name} # ${cpp_name} # ${swig_name} # ${template_params}")
#  ADD_TYPEMAP("${simple_name}" "${cpp_name}" "${swig_name}" "${template_params}")
ENDMACRO(LANGUAGE_SUPPORT_ADD_CLASS)


MACRO(ADD_TYPEMAP simple_name cpp_name swig_name template_params)
  IF(WRAP_ITK_PYTHON AND WRAPPER_LIBRARY_PYTHON)
    ADD_PYTHON_TYPEMAP("${simple_name}" "${cpp_name}" "${swig_name}" "${template_params}")
  ENDIF(WRAP_ITK_PYTHON AND WRAPPER_LIBRARY_PYTHON)

  IF(WRAP_ITK_TCL AND WRAPPER_LIBRARY_TCL)
    ADD_TCL_TYPEMAP("${simple_name}" "${cpp_name}" "${swig_name}" "${template_params}")
  ENDIF(WRAP_ITK_TCL AND WRAPPER_LIBRARY_TCL)

  IF(WRAP_ITK_JAVA AND WRAPPER_LIBRARY_JAVA)
    ADD_JAVA_TYPEMAP("${simple_name}" "${cpp_name}" "${swig_name}" "${template_params}")
  ENDIF(WRAP_ITK_JAVA AND WRAPPER_LIBRARY_JAVA)
ENDMACRO(ADD_TYPEMAP)





MACRO(CONFIGURE_TYPEMAPS outdir)
  SET(CONFIG_TYPEMAP_TEXT "${WRAPPER_TYPEMAPS}")
  CONFIGURE_FILE("${WRAP_ITK_CONFIG_DIR}/typemaps.swg.in"
    "${outdir}/${WRAPPER_LIBRARY_NAME}.swg"
    @ONLY IMMEDIATE)
   WRAP_ITK_INSTALL("/SWIG" "${outdir}/${WRAPPER_LIBRARY_NAME}.swg")
ENDMACRO(CONFIGURE_TYPEMAPS)









# build the languages list

SET(WRAP_ITK_LANGUAGES )
FILE(GLOB local_files *)
FOREACH(f ${local_files})
  FILE(RELATIVE_PATH lang "${CMAKE_CURRENT_SOURCE_DIR}" "${f}")
  IF(NOT ${lang} MATCHES "CVS")
    STRING(TOUPPER "${lang}" lang_upper)
    
    # add the language to the options
    OPTION(WRAP_ITK_${lang_upper} "Build swig ${lang} wrapper support." OFF)
    
    # add the language to the list, if the user have turn it on, and include
    # the subdirectory
    IF(WRAP_ITK_${lang_upper})
      SET(WRAP_ITK_LANGUAGES ${WRAP_ITK_LANGUAGES} "${lang}")
      ADD_SUBDIRECTORY("${lang}")
      GET_DIRECTORY_PROPERTY(inc DIRECTORY "${lang}" INCLUDE_DIRECTORIES)
      INCLUDE_DIRECTORIES(${inc})
    ENDIF(WRAP_ITK_${lang_upper})
  ENDIF(NOT ${lang} MATCHES "CVS")
ENDFOREACH(f)

MESSAGE("${WRAP_ITK_LANGUAGES}")


#IF(IS_DIRECTORY)

#OPTION(WRAP_ITK_PYTHON "Build cswig Python wrapper support." OFF)


