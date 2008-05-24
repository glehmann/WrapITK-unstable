
MACRO(WRAP_LIBRARY_SWIG_INTERFACE library_name)
  # store the content of the mdx file
  SET(SWIG_INTERFACE_MDX_CONTENT )
  # store the content of the .i file for the module - a set of import of all the .i files generated for the module
  SET(SWIG_INTERFACE_MODULE_CONTENT )
  # store the content of the .includes files - a set of #includes for that module
  SET(SWIG_INTERFACE_INCLUDES_CONTENT )
  # the list of .idx files generated for the module
  SET(SWIG_INTERFACE_IDX_FILES )
  # build a list of modules to create the ignerator custom command in 
  # END_WRAP_LIBRARY_SWIG_INTERFACE
  SET(SWIG_INTERFACE_MODULES )
  # typedefs for swig
  SET(SWIG_INTERFACE_TYPEDEFS )
ENDMACRO(WRAP_LIBRARY_SWIG_INTERFACE)

MACRO(END_WRAP_LIBRARY_SWIG_INTERFACE)

  # the list of .i files generated for the module
  SET(SWIG_INTERFACE_FILES )

  FOREACH(module ${SWIG_INTERFACE_MODULES})
    # create the swig interface
    SET(interface_file "${WRAPPER_MASTER_INDEX_OUTPUT_DIR}/wrap_${module}.i")
    SET(xml_file "${WRAPPER_LIBRARY_OUTPUT_DIR}/wrap_${module}.xml")
    SET(includes_file "${WRAPPER_MASTER_INDEX_OUTPUT_DIR}/${WRAPPER_LIBRARY_NAME}.includes")
    # prepare the options
    SET(opts )
    FOREACH(dep ${WRAPPER_LIBRARY_DEPENDS})
      SET(opts ${opts} --mdx "${WRAPPER_MASTER_INDEX_OUTPUT_DIR}/${dep}.mdx")
      SET(opts ${opts} --take-includes "${WRAPPER_MASTER_INDEX_OUTPUT_DIR}/${dep}.includes")
      SET(opts ${opts} --import "${dep}.i")
    ENDFOREACH(dep)
    # import the interface files previously defined instead of importing all the files defined
    # in the module to avoid many warnings when running swig
    FOREACH(i ${SWIG_INTERFACE_FILES})
      GET_FILENAME_COMPONENT(bi "${i}" NAME)
      SET(opts ${opts} --import "${bi}")
    ENDFOREACH(i)
  
  # MESSAGE("${opts}")
  
    # configure the test driver, to set the python path to the pygccxml dir
  #   FIND_PROGRAM(ITK_TEST_DRIVER itkTestDriver)
  #   SET(PYTHON_PYGCCXML_DRIVER "${ITK_TEST_DRIVER}"
  #     --add-before-env PYTHONPATH "${WRAP_ITK_CMAKE_DIR}/pygccxml-0.8.2/"
  #     "${PYTHON_EXECUTABLE}"
  #   )
  
    # prepare dependencies
    SET(DEPS )
    FOREACH(dep ${WRAPPER_LIBRARY_DEPENDS})
      SET(DEPS ${DEPS} ${${dep}IdxFiles} ${${dep}SwigFiles})
      # be sure that the module is selected by the user
      IF(NOT "${WRAP_ITK_MODULES}" MATCHES "(^|;)${dep}(;|$)")
        MESSAGE(SEND_ERROR "${dep} is required by ${WRAPPER_LIBRARY_NAME} module. Please set WRAP_${dep} to ON, or WRAP_${WRAPPER_LIBRARY_NAME} to OFF.")
      ENDIF(NOT "${WRAP_ITK_MODULES}" MATCHES "(^|;)${dep}(;|$)")
    ENDFOREACH(dep)
  
    ADD_CUSTOM_COMMAND(
      OUTPUT ${interface_file}
      COMMAND ${PYTHON_EXECUTABLE} ${CMAKE_BINARY_DIR}/igenerator.py
        ${opts}
        --mdx ${mdx_file}
        --take-includes ${includes_file}
  #       --import ${module_interface_file}
        --swig-include wrap_${module}_ext.i
        -w1 -w3 -w51 -w52 -w53 -w54 #--warning-error
        # --verbose
        ${xml_file}
        ${interface_file}
      DEPENDS ${DEPS} ${xml_file} ${includes_file} ${CMAKE_BINARY_DIR}/igenerator.py ${SWIG_INTERFACE_IDX_FILES} ${SWIG_INTERFACE_FILES}
    )
  #   ADD_CUSTOM_TARGET(${module}Swig DEPENDS ${interface_file})
  #   ADD_DEPENDENCIES(${module}Swig ${WRAPPER_LIBRARY_NAME}Idx)
  #   ADD_DEPENDENCIES(${WRAPPER_LIBRARY_NAME}Swig ${module}Swig)
  
    SET(SWIG_INTERFACE_FILES ${SWIG_INTERFACE_FILES} ${interface_file})
  ENDFOREACH(module)


  # the mdx file
  SET(mdx_file "${WRAPPER_MASTER_INDEX_OUTPUT_DIR}/${WRAPPER_LIBRARY_NAME}.mdx")
  SET(CONFIG_INDEX_FILE_CONTENT "${SWIG_INTERFACE_MDX_CONTENT}")
  CONFIGURE_FILE("${WRAP_ITK_CONFIG_DIR}/Master.mdx.in" "${mdx_file}"
     @ONLY IMMEDIATE )

  SET(module_interface_file "${WRAPPER_MASTER_INDEX_OUTPUT_DIR}/${WRAPPER_LIBRARY_NAME}.i")
  SET(module_interface_ext_file "${WRAPPER_MASTER_INDEX_OUTPUT_DIR}/${WRAPPER_LIBRARY_NAME}_ext.i")
  SET(deps_imports )
  SET(deps_includes )
  FOREACH(dep ${WRAPPER_LIBRARY_DEPENDS})
    SET(deps_imports "${deps_imports}%import ${dep}.i\n")
    SET(deps_includes "${deps_includes}#include \"${dep}.includes\"\n")
  ENDFOREACH(dep)
  SET(SWIG_INTERFACE_INCLUDES "${deps_includes}#include \"${WRAPPER_LIBRARY_NAME}.includes\"")
  SET(CONFIG_MODULE_INTERFACE_CONTENT "${deps_imports}${SWIG_INTERFACE_MODULE_CONTENT}")  
  CONFIGURE_FILE("${WRAP_ITK_CONFIG_DIR}/module.i.in" "${module_interface_file}"
    @ONLY IMMEDIATE )
  SET(WRAP_ITK_FILE_CONTENT )
  CONFIGURE_FILE("${WRAP_ITK_CONFIG_DIR}/empty.in" "${module_interface_ext_file}"
    @ONLY IMMEDIATE )
  
  # create the file which store all the includes
  SET(includes_file "${WRAPPER_MASTER_INDEX_OUTPUT_DIR}/${WRAPPER_LIBRARY_NAME}.includes")
  CONFIGURE_FILE("${WRAP_ITK_CONFIG_DIR}/module.includes.in"
     ${includes_file}
     @ONLY IMMEDIATE )

#   ADD_CUSTOM_TARGET(${WRAPPER_LIBRARY_NAME}Idx DEPENDS ${SWIG_INTERFACE_IDX_FILES})
  SET(${WRAPPER_LIBRARY_NAME}IdxFiles ${SWIG_INTERFACE_IDX_FILES} CACHE INTERNAL "Internal ${WRAPPER_LIBRARY_NAME}Idx file list.")

  ADD_CUSTOM_TARGET(${WRAPPER_LIBRARY_NAME}Swig DEPENDS ${SWIG_INTERFACE_FILES})
  SET(${WRAPPER_LIBRARY_NAME}SwigFiles ${SWIG_INTERFACE_FILES} CACHE INTERNAL "Internal ${WRAPPER_LIBRARY_NAME}Swig file list.")
  FOREACH(dep ${WRAPPER_LIBRARY_DEPENDS})
    ADD_DEPENDENCIES(${WRAPPER_LIBRARY_NAME}Swig ${dep}Swig) # ${dep}Idx
  ENDFOREACH(dep)

ENDMACRO(END_WRAP_LIBRARY_SWIG_INTERFACE)


MACRO(WRAP_INCLUDE_SWIG_INTERFACE include_file)
  # TODO: don't include the same file several times
  IF("${include_file}" MATCHES "<.*>")
    SET(SWIG_INTERFACE_INCLUDES_CONTENT "${SWIG_INTERFACE_INCLUDES_CONTENT}#include ${include_file}\n")
  ELSE("${include_file}" MATCHES "<.*>")
    SET(SWIG_INTERFACE_INCLUDES_CONTENT "${SWIG_INTERFACE_INCLUDES_CONTENT}#include \"${include_file}\"\n")
  ENDIF("${include_file}" MATCHES "<.*>")
ENDMACRO(WRAP_INCLUDE_SWIG_INTERFACE)


MACRO(INCLUDE_WRAP_CMAKE_SWIG_INTERFACE module)
ENDMACRO(INCLUDE_WRAP_CMAKE_SWIG_INTERFACE)

MACRO(END_INCLUDE_WRAP_CMAKE_SWIG_INTERFACE module)
  # variables used:
  # WRAPPER_LIBRARY_NAME
  # WRAPPER_LIBRARY_OUTPUT_DIR
  # WRAPPER_LIBRARY_CABLESWIG_INPUTS
  # WRAPPER_LIBRARY_DEPENDS
  # WRAPPER_MASTER_INDEX_OUTPUT_DIR
  # MODULE_INCLUDES
  
     
  # the master idx file
  SET(mdx_file "${WRAPPER_MASTER_INDEX_OUTPUT_DIR}/${WRAPPER_LIBRARY_NAME}.mdx")
  
  # generate the idx file for all the groups of the module
  SET(idx_file "${WRAPPER_LIBRARY_OUTPUT_DIR}/wrap_${module}.idx")
  ADD_CUSTOM_COMMAND(
    OUTPUT ${idx_file}
    COMMAND ${CABLE_INDEX}
          ${xml_file} ${idx_file}
    DEPENDS ${CABLE_INDEX} ${xml_file}
  )
#   ADD_CUSTOM_TARGET(${module}Idx DEPENDS ${idx_file})

  # store the path of the idx file to store it in the mdx file
  SET(SWIG_INTERFACE_MDX_CONTENT "${SWIG_INTERFACE_MDX_CONTENT}${idx_file}\n")
  SET(SWIG_INTERFACE_IDX_FILES ${SWIG_INTERFACE_IDX_FILES} ${idx_file})
  
  SET(SWIG_INTERFACE_MODULE_CONTENT "${SWIG_INTERFACE_MODULE_CONTENT}%import wrap_${module}.i\n")

  SET(SWIG_INTERFACE_MODULES ${SWIG_INTERFACE_MODULES} ${module})

  SET(interface_ext_file "${WRAPPER_MASTER_INDEX_OUTPUT_DIR}/wrap_${module}_ext.i")
  SET(WRAP_ITK_FILE_CONTENT )
  CONFIGURE_FILE("${WRAP_ITK_CONFIG_DIR}/empty.in" "${interface_ext_file}"
    @ONLY IMMEDIATE )

ENDMACRO(END_INCLUDE_WRAP_CMAKE_SWIG_INTERFACE)


MACRO(ADD_ONE_TYPEDEF_SWIG_INTERFACE wrap_method wrap_class swig_name)
  # Add one  typedef to WRAPPER_TYPEDEFS
  # 'wrap_method' is the one of the valid WRAPPER_WRAP_METHODS from WRAP_CLASS,
  # 'wrap_class' is the fully-qualified C++ name of the class
  # 'swig_name' is what the swigged class should be called
  # The optional last argument is the template parameters that should go between 
  # the < > brackets in the C++ template definition.
  # Only pass 3 parameters to wrap a non-templated class
  #
  # Global vars used: none
  # Global vars modified: WRAPPER_TYPEDEFS
  
  # get the base C++ class name (no namespaces) from wrap_class:
  STRING(REGEX REPLACE "(.*::)" "" base_name "${wrap_class}")

  SET(wrap_pointer 0)
  SET(template_parameters "${ARGV3}")
  IF(template_parameters)
    SET(full_class_name "${wrap_class}< ${template_parameters} >")
  ELSE(template_parameters)
    SET(full_class_name "${wrap_class}")
  ENDIF(template_parameters)
  
  # ADD_ONE_TYPEDEF_ALL_LANGUAGES("${wrap_method}" "${wrap_class}" "${swig_name}" "${ARGV3}")
  
  # Add a typedef for the class. We have this funny looking full_name::base_name
  # thing (it expands to, for example "typedef itk::Foo<baz, 2>::Foo"), to 
  # trick gcc_xml into creating code for the class. If we left off the trailing
  # base_name, then gcc_xml wouldn't see the typedef as a class instantiation,
  # and thus wouldn't create XML for any of the methods, etc.

  IF("${wrap_method}" MATCHES "2_SUPERCLASSES")
    ADD_SIMPLE_TYPEDEF_SWIG_INTERFACE("${full_class_name}::Superclass::Superclass::Self" "${swig_name}_Superclass_Superclass")
    ADD_SIMPLE_TYPEDEF_SWIG_INTERFACE("${full_class_name}::Superclass::Superclass::Pointer::SmartPointer" "${swig_name}_Superclass_Superclass_Pointer")
  ENDIF("${wrap_method}" MATCHES "2_SUPERCLASSES")

  IF("${wrap_method}" MATCHES "SUPERCLASS")
    ADD_SIMPLE_TYPEDEF_SWIG_INTERFACE("${full_class_name}::Superclass::Self" "${swig_name}_Superclass")
    ADD_SIMPLE_TYPEDEF_SWIG_INTERFACE("${full_class_name}::Superclass::Pointer::SmartPointer" "${swig_name}_Superclass_Pointer")
  ENDIF("${wrap_method}" MATCHES "SUPERCLASS")

  IF("${wrap_method}" MATCHES "FORCE_INSTANTIATE")
    ADD_SIMPLE_TYPEDEF_SWIG_INTERFACE("${full_class_name}" "${swig_name}")
    # cable swig part will add a peace of code for type instantiation
  ELSE("${wrap_method}" MATCHES "FORCE_INSTANTIATE")
    ADD_SIMPLE_TYPEDEF_SWIG_INTERFACE("${full_class_name}" "${swig_name}")
  ENDIF("${wrap_method}" MATCHES "FORCE_INSTANTIATE")

  IF("${wrap_method}" MATCHES "POINTER")
    # add a pointer typedef if we are so asked
    ADD_SIMPLE_TYPEDEF_SWIG_INTERFACE("${full_class_name}::Pointer::SmartPointer" "${swig_name}_Pointer")
  ENDIF("${wrap_method}" MATCHES "POINTER")

ENDMACRO(ADD_ONE_TYPEDEF_SWIG_INTERFACE)


MACRO(ADD_SIMPLE_TYPEDEF_SWIG_INTERFACE wrap_class swig_name)
  SET(SWIG_INTERFACE_TYPEDEFS "${SWIG_INTERFACE_TYPEDEFS}typedef ${wrap_class} ${swig_name};\n")
ENDMACRO(ADD_SIMPLE_TYPEDEF_SWIG_INTERFACE)

INCLUDE_DIRECTORIES("${WRAPPER_MASTER_INDEX_OUTPUT_DIR}")

# create the igenerator.py with the pygccxml path in it
SET(PYGCCXML_PATH "${CMAKE_CURRENT_SOURCE_DIR}/pygccxml-0.8.2/")
CONFIGURE_FILE("${CMAKE_CURRENT_SOURCE_DIR}/igenerator.py.in" 
  "${CMAKE_CURRENT_BINARY_DIR}/igenerator.py"
  @ONLY IMMEDIATE)

# find swig
FIND_PACKAGE(SWIG REQUIRED)
INCLUDE(${SWIG_USE_FILE})

# find python
FIND_PACKAGE(PythonInterp REQUIRED)
