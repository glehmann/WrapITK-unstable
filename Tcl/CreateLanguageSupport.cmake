MACRO(ADD_TCL_TYPEMAP simple_name cpp_name swig_name template_params)
  # write me
ENDMACRO(ADD_TCL_TYPEMAP)

MACRO(TCL_SUPPORT_CONFIGURE_FILES)
  # write me
ENDMACRO(TCL_SUPPORT_CONFIGURE_FILES)

MACRO(END_WRAPPER_LIBRARY_TCL)

  SET(cpp_files )

  SET(modules )

  FOREACH(source ${WRAPPER_LIBRARY_CABLESWIG_INPUTS})
  
    GET_FILENAME_COMPONENT(base_name ${source} NAME_WE)
    STRING(REGEX REPLACE "^wrap_" "" group_name "${base_name}")
    
    # create the swig interface for all the groups in the module
    #
    SET(interface_file "${WRAPPER_MASTER_INDEX_OUTPUT_DIR}/${base_name}.i")
    SET(lib ${group_name}Tcl)
    SET(cpp_file "${CMAKE_CURRENT_BINARY_DIR}/${base_name}Tcl.cpp")

    ADD_CUSTOM_COMMAND(
      OUTPUT ${cpp_file}
      COMMAND swig -c++ -tcl -fcompact -O -Werror -w508 -w312 -w314 -w509 -w302 -w362
      -w365 -w366 -w367 -w368 -w378 -w503 # operator???, to be suppressed later...
      -l${WrapITK_SOURCE_DIR}/Tcl/tcl.i
      -o ${cpp_file}
#      -I${WRAPPER_MASTER_INDEX_OUTPUT_DIR}
      -outdir ${LIBRARY_OUTPUT_PATH}
      ${interface_file}
      WORKING_DIRECTORY ${WRAPPER_MASTER_INDEX_OUTPUT_DIR}/tcl
      DEPENDS ${interface_file} ${WrapITK_SOURCE_DIR}/Tcl/tcl.i
    )
    ADD_CUSTOM_TARGET(${base_name}SwigTcl DEPENDS ${cpp_file})
    
    SET(cpp_files ${cpp_files} ${cpp_file})
    
    SET(modules ${modules} ${group_name})

    ADD_LIBRARY(${lib} SHARED ${cpp_file})
    SET_TARGET_PROPERTIES(${lib} PROPERTIES PREFIX "")
    TARGET_LINK_LIBRARIES(${lib} ${WRAPPER_LIBRARY_LINK_LIBRARIES} ${TCL_LIBRARY})
    
  ENDFOREACH(source)
  
#  ADD_LIBRARY(${WRAPPER_LIBRARY_NAME}Tcl MODULE ${cpp_files})
#  SET_TARGET_PROPERTIES(${WRAPPER_LIBRARY_NAME}Tcl PROPERTIES PREFIX "_")
#  TARGET_LINK_LIBRARIES( ${WRAPPER_LIBRARY_NAME}Tcl
#    ${WRAPPER_LIBRARY_LINK_LIBRARIES} 
#    ${TCL_LIBRARY}
#  )

  ADD_CUSTOM_TARGET(${WRAPPER_LIBRARY_NAME}SwigTcl DEPENDS ${cpp_files})
  
  ADD_CUSTOM_TARGET(${WRAPPER_LIBRARY_NAME}Tcl DEPENDS ${modules})


ENDMACRO(END_WRAPPER_LIBRARY_TCL)
