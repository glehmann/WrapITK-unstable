
MACRO(WRAP_LIBRARY_SWIG_INTERFACE library_name)
  # store the content of the mdx file
  SET(SWIG_INTERFACE_MDX_CONTENT )
  # store the content of the .i file for the module - a set of import of all the .i files generated for the module
  SET(SWIG_INTERFACE_MODULE_CONTENT )
  # store the content of the .includes files - a set of #includes for that module
  SET(SWIG_INTERFACE_INCLUDES_CONTENT )
  # the list of .i files generated for the module
  SET(SWIG_INTERFACE_FILES )
  # the list of .idx files generated for the module
  SET(SWIG_INTERFACE_IDX_FILES )
  # That target can be created first, so we can make it depends on the individual group targets
  # (itkMedianImageFilterSwig for example), and make those individual targets depends on the whole
  # ${WRAPPER_LIBRARY_NAME}Idx
  ADD_CUSTOM_TARGET(${WRAPPER_LIBRARY_NAME}Swig)# DEPENDS ${SWIG_INTERFACE_FILES})
ENDMACRO(WRAP_LIBRARY_SWIG_INTERFACE)

MACRO(END_WRAP_LIBRARY_SWIG_INTERFACE)
  # the mdx file
  SET(mdx_file "${WRAPPER_MASTER_INDEX_OUTPUT_DIR}/${WRAPPER_LIBRARY_NAME}.mdx")
  SET(CONFIG_INDEX_FILE_CONTENT "${SWIG_INTERFACE_MDX_CONTENT}")
  CONFIGURE_FILE("${WRAP_ITK_CONFIG_DIR}/Master.mdx.in" "${mdx_file}"
     @ONLY IMMEDIATE )

  SET(module_interface_file "${WRAPPER_MASTER_INDEX_OUTPUT_DIR}/${WRAPPER_LIBRARY_NAME}.i")
  SET(deps_imports )
  FOREACH(dep ${WRAPPER_LIBRARY_DEPENDS})
    SET(deps_imports "${deps_imports}%import ${dep}.i\n")
  ENDFOREACH(dep)
  SET(CONFIG_MODULE_INTERFACE_CONTENT "${deps_imports}${SWIG_INTERFACE_MODULE_CONTENT}")  
  CONFIGURE_FILE("${WRAP_ITK_CONFIG_DIR}/module.i.in" "${module_interface_file}"
    @ONLY IMMEDIATE )
  
  # create the file which store all the includes
  SET(includes_file "${WRAPPER_MASTER_INDEX_OUTPUT_DIR}/${WRAPPER_LIBRARY_NAME}.includes")
  CONFIGURE_FILE("${WRAP_ITK_CONFIG_DIR}/module.includes.in"
     ${includes_file}
     @ONLY IMMEDIATE )

  ADD_CUSTOM_TARGET(${WRAPPER_LIBRARY_NAME}Idx DEPENDS ${SWIG_INTERFACE_IDX_FILES})
  ADD_DEPENDENCIES(${WRAPPER_LIBRARY_NAME}Swig ${WRAPPER_LIBRARY_NAME}Idx)
  FOREACH(dep ${WRAPPER_LIBRARY_DEPENDS})
    ADD_DEPENDENCIES(${WRAPPER_LIBRARY_NAME}Swig ${dep}Idx ${dep}Swig)
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
  ADD_CUSTOM_TARGET(${module}Idx DEPENDS ${idx_file})

  # store the path of the idx file to store it in the mdx file
  SET(SWIG_INTERFACE_MDX_CONTENT "${SWIG_INTERFACE_MDX_CONTENT}${idx_file}\n")
  SET(SWIG_INTERFACE_IDX_FILES ${SWIG_INTERFACE_IDX_FILES} ${idx_file})
  
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

  ADD_CUSTOM_COMMAND(
    OUTPUT ${interface_file}
    COMMAND python ${WRAP_ITK_CMAKE_DIR}/igenerator.py
      ${opts}
      --mdx ${mdx_file}
      --take-includes ${includes_file}
#       --import ${module_interface_file}
      --swig-include wrap_${module}_ext.i
      -w1 -w3 -w51 -w52 -w53 -w54 #--warning-error
      # --verbose
      ${xml_file}
      ${interface_file}
    DEPENDS ${xml_file} ${idx_file} ${includes_file} ${WRAP_ITK_CMAKE_DIR}/igenerator.py ${SWIG_INTERFACE_FILES}
  )
  ADD_CUSTOM_TARGET(${module}Swig DEPENDS ${interface_file})
  ADD_DEPENDENCIES(${module}Swig ${WRAPPER_LIBRARY_NAME}Idx)
  ADD_DEPENDENCIES(${WRAPPER_LIBRARY_NAME}Swig ${module}Swig)
  FOREACH(dep ${WRAPPER_LIBRARY_DEPENDS})
    ADD_DEPENDENCIES(${module}Swig ${dep}Idx ${dep}Swig)
    # be sure that the module is selected by the user
    IF(NOT "${WRAP_ITK_MODULES}" MATCHES "(^|;)${dep}(;|$)")
      MESSAGE(SEND_ERROR "${dep} is required by ${WRAPPER_LIBRARY_NAME} module. Please set WRAP_${dep} to ON, or WRAP_${WRAPPER_LIBRARY_NAME} to OFF.")
    ENDIF(NOT "${WRAP_ITK_MODULES}" MATCHES "(^|;)${dep}(;|$)")
  ENDFOREACH(dep)

  SET(SWIG_INTERFACE_FILES ${SWIG_INTERFACE_FILES} ${interface_file})
  SET(SWIG_INTERFACE_MODULE_CONTENT "${SWIG_INTERFACE_MODULE_CONTENT}%import wrap_${module}.i\n")
ENDMACRO(END_INCLUDE_WRAP_CMAKE_SWIG_INTERFACE)
