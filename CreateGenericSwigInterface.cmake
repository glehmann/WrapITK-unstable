
MACRO(END_WRAP_LIBRARY)
  # variables used:
  # WRAPPER_LIBRARY_NAME
  # WRAPPER_LIBRARY_OUTPUT_DIR
  # WRAPPER_LIBRARY_CABLESWIG_INPUTS
  # WRAPPER_LIBRARY_DEPENDS
  # WRAPPER_MASTER_INDEX_OUTPUT_DIR
  # MODULE_INCLUDES
  
  # create the file which store all the includes
  #
  SET(includes_file "${WRAPPER_MASTER_INDEX_OUTPUT_DIR}/${WRAPPER_LIBRARY_NAME}.includes")
  CONFIGURE_FILE("${WRAP_ITK_CONFIG_DIR}/module.includes.in"
     "${WRAPPER_MASTER_INDEX_OUTPUT_DIR}/${WRAPPER_LIBRARY_NAME}.includes"
     ${includes_file}
     @ONLY IMMEDIATE )
     
  # create the files used to pass the file to include to gccxml
  SET(gccxml_inc_file "${WRAPPER_LIBRARY_OUTPUT_DIR}/gcc_xml.inc")
  SET(CONFIG_GCCXML_INC_CONTENTS)
  GET_DIRECTORY_PROPERTY(include_dir_list INCLUDE_DIRECTORIES)
  FOREACH(dir ${include_dir_list})
    SET(CONFIG_GCCXML_INC_CONTENTS "${CONFIG_GCCXML_INC_CONTENTS}-I${dir}\n")
  ENDFOREACH(dir)
  CONFIGURE_FILE("${WRAP_ITK_CONFIG_DIR}/gcc_xml.inc.in" "${gccxml_inc_file}"
    @ONLY IMMEDIATE)

  # the master idx file
  SET(mdx_file "${WRAPPER_MASTER_INDEX_OUTPUT_DIR}/${WRAPPER_LIBRARY_NAME}.mdx")
  
  # to store the content of the mdx file, to be write later
  SET(mdx_content )
  
  SET(module_target_depend )
  FOREACH(dep ${WRAPPER_LIBRARY_DEPENDS})
    # MESSAGE("${dep}_SWIG_FILES: ${${dep}_SWIG_FILES}")
    SET(module_target_depend ${module_target_depend} ${${dep}_SWIG_FILES})
  ENDFOREACH(dep)
  # MESSAGE("${module_target_depend}")

  FOREACH(source ${WRAPPER_LIBRARY_CABLESWIG_INPUTS})
  
    GET_FILENAME_COMPONENT(base_name ${source} NAME_WE)
    
    # generate the xml file for all the groups of the module
    #
    SET(xml_file "${WRAPPER_LIBRARY_OUTPUT_DIR}/${base_name}.xml")
    ADD_CUSTOM_COMMAND(
      OUTPUT ${xml_file}
      COMMAND ${GCCXML}
           -fxml-start=_cable_
           -fxml=${xml_file}
           --gccxml-gcc-options ${gccxml_inc_file}
           -DCSWIG
           -DCABLE_CONFIGURATION
           ${source}
      DEPENDS ${GCCXML} ${source}
    )
    ADD_CUSTOM_TARGET(${base_name}Xml DEPENDS ${xml_file})
    
    # generate the idx file for all the groups of the module
    #
    SET(idx_file "${WRAPPER_LIBRARY_OUTPUT_DIR}/${base_name}.idx")
    ADD_CUSTOM_COMMAND(
      OUTPUT ${idx_file}
      COMMAND ${CABLE_INDEX}
           ${xml_file} ${idx_file}
      DEPENDS ${CABLE_INDEX} ${xml_file}
    )
    ADD_CUSTOM_TARGET(${base_name}Idx DEPENDS ${idx_file})

    # store the path of the idx file to store it in the mdx file
    #
    SET(mdx_content ${mdx_content} ${idx_file})
  
  ENDFOREACH(source)
  
  
  # clear the variable used to store the content of %{module.i}
  SET(module_interface_content )

  SET(module_interface_file "${WRAPPER_MASTER_INDEX_OUTPUT_DIR}/${WRAPPER_LIBRARY_NAME}.i")
  
  SET(interface_files )

  # must make a new for each loop, to have a full mdx_content
  FOREACH(source ${WRAPPER_LIBRARY_CABLESWIG_INPUTS})
  
    GET_FILENAME_COMPONENT(base_name ${source} NAME_WE)
    
    # create the swig interface for all the groups in the module
    #
    SET(interface_file "${WRAPPER_MASTER_INDEX_OUTPUT_DIR}/${base_name}.i")
    SET(xml_file "${WRAPPER_LIBRARY_OUTPUT_DIR}/${base_name}.xml")
    # prepare the options
    SET(opts )
    FOREACH(dep ${WRAPPER_LIBRARY_DEPENDS})
      SET(opts ${opts} --mdx "${WRAPPER_MASTER_INDEX_OUTPUT_DIR}/${dep}.mdx")
      SET(opts ${opts} --take-includes "${WRAPPER_MASTER_INDEX_OUTPUT_DIR}/${dep}.includes")
      SET(opts ${opts} --import "${WRAPPER_MASTER_INDEX_OUTPUT_DIR}/${dep}.i")
    ENDFOREACH(dep)
    # import the interface files previously defined instead of importing all the files defined
    # in the module to avoid many warnings when running swig
    FOREACH(i ${interface_files})
      SET(opts ${opts} --import "${i}")
    ENDFOREACH(i)
    ADD_CUSTOM_COMMAND(
      OUTPUT ${interface_file}
      COMMAND python ${WRAP_ITK_CMAKE_DIR}/igenerator.py
         ${opts}
         --mdx ${mdx_file}
         --take-includes ${includes_file}
#         --import ${module_interface_file}
         --swig-include ${base_name}_ext.i
         -w 1 -W
         ${xml_file}
         ${interface_file}
      DEPENDS ${xml_file} ${mdx_content} ${includes_file} ${WRAP_ITK_CMAKE_DIR}/igenerator.py ${module_target_depend}
    )
    ADD_CUSTOM_TARGET(${base_name}Swig DEPENDS ${interface_file}  ${module_target_depend})
  
    SET(module_interface_content "${module_interface_content}%import ${base_name}.i\n")
    
    SET(interface_files ${interface_files} ${interface_file})
    
    # create an empty file so swig will find it if the tehre is no customization for the target language.
    FILE(WRITE ${WRAPPER_MASTER_INDEX_OUTPUT_DIR}/${base_name}_ext.i "")
    
  ENDFOREACH(source)
  
  SET(CONFIG_INDEX_FILE_CONTENT )
  FOREACH(f ${mdx_content})
    SET(CONFIG_INDEX_FILE_CONTENT "${CONFIG_INDEX_FILE_CONTENT}${f}\n")
  ENDFOREACH(f)
  CONFIGURE_FILE("${WRAP_ITK_CONFIG_DIR}/Master.mdx.in" "${mdx_file}"
     @ONLY IMMEDIATE )

  SET(CONFIG_MODULE_INTERFACE_CONTENT "${module_interface_content}")  
  CONFIGURE_FILE("${WRAP_ITK_CONFIG_DIR}/module.i.in" "${module_interface_file}"
     @ONLY IMMEDIATE )
     
  # create the target which depends on all the interface files
  ADD_CUSTOM_TARGET(${WRAPPER_LIBRARY_NAME}Swig DEPENDS ${interface_files}) # ${module_target_depend})
  
  # and store the interface files in a var, to be reused later
  SET(${WRAPPER_LIBRARY_NAME}_SWIG_FILES ${interface_files} CACHE INTERNAL "Store in cache to be usable even if not in the same dir")
  # MESSAGE("SET ${WRAPPER_LIBRARY_NAME}_SWIG_FILES: ${${WRAPPER_LIBRARY_NAME}_SWIG_FILES}")
  
  # OK, so let the language specific parts make their job
  END_WRAP_LIBRARY_ALL_LANGUAGES()
  
ENDMACRO(END_WRAP_LIBRARY)



MACRO(WRAPPER_LIBRARY_CREATE_LIBRARY)
  MESSAGE("Deprecation warning: WRAPPER_LIBRARY_CREATE_LIBRARY is replaced by END_WRAP_LIBRARY.")
  END_WRAP_LIBRARY()
ENDMACRO(WRAPPER_LIBRARY_CREATE_LIBRARY)
