#------------------------------------------------------------------------------

# set the default include files for the generated wrapper files
# itk::Command has to be available in all ITK wrapped files
SET(WRAPPER_DEFAULT_INCLUDE "itkCommand.h")

# define some macro to help creation of types vars

MACRO(WRAP_TYPE class prefix)
   # begin the creation of a type vars
   # call to this macro should be followed by one or several call to ADD_TEMPLATE()
   # and one call to END_WRAP_TYPE to really create the vars
   SET(WRAPPER_TEMPLATES "")
   SET(itk_Wrap_Prefix "${prefix}")
   SET(itk_Wrap_Class "${class}")

   # If the type is ITK class, add apropriate include file
   IF("${class}" MATCHES "itk::")
     STRING(REGEX REPLACE "itk.*::(.*)" "itk\\1" includeFileName "${class}")
     SET(WRAPPER_DEFAULT_INCLUDE ${WRAPPER_DEFAULT_INCLUDE} "${includeFileName}.h")
   ENDIF("${class}" MATCHES "itk::")
ENDMACRO(WRAP_TYPE)

MACRO(END_WRAP_TYPE)
   # create the type vars.
   # must be called after END_WRAP_TYPE
   # Create the vars used for to designe types in all the cmake
   # files. This method ensure all the type names are constructed
   # with the same method
   FOREACH(wrap ${WRAPPER_TEMPLATES})
      STRING(REGEX REPLACE "([0-9A-Za-z]*)[ ]*#[ ]*(.*)" "\\1" wrapTpl "${wrap}")
      STRING(REGEX REPLACE "([0-9A-Za-z]*)[ ]*#[ ]*(.*)" "\\2" wrapType "${wrap}")
      SET(ITKT_${itk_Wrap_Prefix}${wrapTpl} "${itk_Wrap_Class}< ${wrapType} >")
      SET(ITKM_${itk_Wrap_Prefix}${wrapTpl} "${itk_Wrap_Prefix}${wrapTpl}")
   ENDFOREACH(wrap)
ENDMACRO(END_WRAP_TYPE)

MACRO(ADD_TEMPLATE name types)
  SET(WRAPPER_TEMPLATES ${WRAPPER_TEMPLATES} "${name} # ${types}")
ENDMACRO(ADD_TEMPLATE)


#------------------------------------------------------------------------------

# now, define types vars
# the result is stored in itk_Wrap_XXX where XXX is the name of the class
# to be wrapped in there own file, most of the time in CommonA


WRAP_TYPE("itk::Offset" "O")
  UNIQUE(dims "${WRAP_ITK_DIMS};1")
  FOREACH(d ${dims})
    ADD_TEMPLATE("${d}"  "${d}")
  ENDFOREACH(d)
END_WRAP_TYPE()
SET(itk_Wrap_Offset ${WRAPPER_TEMPLATES})

WRAP_TYPE("itk::Vector" "V")
  # dim 6 is used by ScaleSkewVersor3DTransform
  UNIQUE(vector_sizes "${WRAP_ITK_DIMS};6")
  FOREACH(d ${vector_sizes})
    ADD_TEMPLATE("${ITKM_F}${d}"  "${ITKT_F},${d}")
    ADD_TEMPLATE("${ITKM_D}${d}"  "${ITKT_D},${d}")
  ENDFOREACH(d)
END_WRAP_TYPE()
SET(itk_Wrap_Vector ${WRAPPER_TEMPLATES})

WRAP_TYPE("itk::CovariantVector" "CV")
  FOREACH(d ${WRAP_ITK_DIMS})
    ADD_TEMPLATE("${ITKM_F}${d}"  "${ITKT_F},${d}")
    ADD_TEMPLATE("${ITKM_D}${d}"  "${ITKT_D},${d}")
  ENDFOREACH(d)
END_WRAP_TYPE()
SET(itk_Wrap_CovariantVector ${WRAPPER_TEMPLATES})

WRAP_TYPE("itk::ContinuousIndex" "CI")
  FOREACH(d ${WRAP_ITK_DIMS})
    ADD_TEMPLATE("${ITKM_F}${d}"  "${ITKT_F},${d}")
    ADD_TEMPLATE("${ITKM_D}${d}"  "${ITKT_D},${d}")
  ENDFOREACH(d)
END_WRAP_TYPE()
SET(itk_Wrap_ContinuousIndex ${WRAPPER_TEMPLATES})

WRAP_TYPE("itk::Array" "A")
  ADD_TEMPLATE("${ITKM_D}" "${ITKT_D}")
  ADD_TEMPLATE("${ITKM_F}" "${ITKT_F}")
  ADD_TEMPLATE("${ITKM_UL}" "${ITKT_UL}")
END_WRAP_TYPE()
SET(itk_Wrap_Array ${WRAPPER_TEMPLATES})

WRAP_TYPE("itk::FixedArray" "FA")
  SET(dims ${WRAP_ITK_DIMS})
  FOREACH(d ${WRAP_ITK_DIMS})
    MATH(EXPR d2 "${d} * 2")
    SET(dims ${dims} ${d2})
  ENDFOREACH(d)
  UNIQUE(array_sizes "${dims};1;3;4;6")
  # make sure that 1-D FixedArrays are wrapped. Also wrap for each selected
  # image dimension.
  # 3-D FixedArrays are required as superclass of rgb pixels
  # TODO: Do we need fixed arrays for all of these types? For just the selected
  # pixel types plus some few basic cases? Or just for a basic set of types?
  FOREACH(d ${array_sizes})
    ADD_TEMPLATE("${ITKM_D}${d}"  "${ITKT_D},${d}")
    ADD_TEMPLATE("${ITKM_F}${d}"  "${ITKT_F},${d}")
    ADD_TEMPLATE("${ITKM_UL}${d}" "${ITKT_UL},${d}")
    ADD_TEMPLATE("${ITKM_US}${d}" "${ITKT_US},${d}")
    ADD_TEMPLATE("${ITKM_UC}${d}" "${ITKT_UC},${d}")
    ADD_TEMPLATE("${ITKM_UI}${d}" "${ITKT_UI},${d}")
    ADD_TEMPLATE("${ITKM_SL}${d}" "${ITKT_SL},${d}")
    ADD_TEMPLATE("${ITKM_SS}${d}" "${ITKT_SS},${d}")
    ADD_TEMPLATE("${ITKM_SC}${d}" "${ITKT_SC},${d}")
    ADD_TEMPLATE("${ITKM_B}${d}"  "${ITKT_B},${d}")
  ENDFOREACH(d)
END_WRAP_TYPE()
SET(itk_Wrap_FixedArray ${WRAPPER_TEMPLATES})

WRAP_TYPE("itk::RGBPixel" "RGB")
  ADD_TEMPLATE("${ITKM_UC}" "${ITKT_UC}")
  
  IF(WRAP_rgb_unsigned_short)
    ADD_TEMPLATE("${ITKM_US}" "${ITKT_US}")
  ENDIF(WRAP_rgb_unsigned_short)
END_WRAP_TYPE()
SET(itk_Wrap_RGBPixel ${WRAPPER_TEMPLATES})

WRAP_TYPE("std::complex" "C")
  IF(WRAP_complex_float)
    ADD_TEMPLATE("${ITKM_F}"  "${ITKT_F}")
  ENDIF(WRAP_complex_float)
  IF(WRAP_complex_double)
    ADD_TEMPLATE("${ITKM_D}"  "${ITKT_D}")
  ENDIF(WRAP_complex_double)
END_WRAP_TYPE()
SET(itk_Wrap_vcl_complex ${WRAPPER_TEMPLATES})

WRAP_TYPE("itk::Image" "I")
  # Make a list of all of the selected image pixel types and also double (for
  # BSplineDeformableTransform), uchar (for 8-bit image output), and ulong
  # (for the watershed and relabel filters).
  UNIQUE(wrap_image_types "${WRAP_ITK_ALL_TYPES};D;UC;UL;RGBUC")
  
  FOREACH(d ${WRAP_ITK_DIMS})
    FOREACH(type ${wrap_image_types})
      IF("${WRAP_ITK_VECTOR}" MATCHES "(^|;)${type}(;|$)")
        # if the type is a vector type with no dimension specified, make the 
        # vector dimension match the image dimension.
        SET(type "${type}${d}")
      ENDIF("${WRAP_ITK_VECTOR}" MATCHES "(^|;)${type}(;|$)")
      
      ADD_TEMPLATE("${ITKM_${type}}${d}"  "${ITKT_${type}},${d}")
    ENDFOREACH(type)
    
    # FixedArray types required by level set filters
    ADD_TEMPLATE("${ITKM_FAF${d}}${d}"  "${ITKT_FAF${d}},${d}")
    
    # Offset, used by Danielsson's filter
    ADD_TEMPLATE("${ITKM_O${d}}${d}"  "${ITKT_O${d}},${d}")
    
  ENDFOREACH(d)
END_WRAP_TYPE()
SET(itk_Wrap_Image ${WRAPPER_TEMPLATES})

WRAP_TYPE("itk::VectorImage" "VI")
  # Make a list of all of the selected image pixel types and also uchar 
  # (for 8-bit image output)
  UNIQUE(wrap_image_types "${WRAP_ITK_SCALAR};UC")
  
  FOREACH(d ${WRAP_ITK_DIMS})
    FOREACH(type ${wrap_image_types})
      ADD_TEMPLATE("${ITKM_${type}}${d}"  "${ITKT_${type}},${d}")
    ENDFOREACH(type)
  ENDFOREACH(d)
END_WRAP_TYPE()
SET(itk_Wrap_VectorImage ${WRAPPER_TEMPLATES})

WRAP_TYPE("itk::VariableLengthVector" "VLV")
  # Make a list of all of the selected image pixel types and also uchar 
  # (for 8-bit image output)
  UNIQUE(wrap_image_types "${WRAP_ITK_SCALAR};UC")
  
  FOREACH(type ${wrap_image_types})
    ADD_TEMPLATE("${ITKM_${type}}"  "${ITKT_${type}}")
  ENDFOREACH(type)
END_WRAP_TYPE()
SET(itk_Wrap_VariableLengthVector ${WRAPPER_TEMPLATES})

WRAP_TYPE("itk::Point" "P")
  FOREACH(d ${WRAP_ITK_DIMS})
    ADD_TEMPLATE("${ITKM_F}${d}"  "${ITKT_F},${d}")
    ADD_TEMPLATE("${ITKM_D}${d}"  "${ITKT_D},${d}")
  ENDFOREACH(d)
END_WRAP_TYPE()
SET(itk_Wrap_Point ${WRAPPER_TEMPLATES})

WRAP_TYPE("itk::LevelSetNode" "LSN")
  # Only make level set nodes for the selected image pixel types
  FOREACH(d ${WRAP_ITK_DIMS})
    FOREACH(type ${WRAP_ITK_SCALAR})
      ADD_TEMPLATE("${ITKM_${type}}${d}"  "${ITKT_${type}},${d}")
    ENDFOREACH(type)
  ENDFOREACH(d)
END_WRAP_TYPE()
SET(itk_Wrap_LevelSetNode ${WRAPPER_TEMPLATES})

WRAP_TYPE("itk::FlatStructuringElement" "SE")
  FOREACH(d ${WRAP_ITK_DIMS})
    ADD_TEMPLATE("${d}"  "${d}")
  ENDFOREACH(d)
END_WRAP_TYPE()
SET(itk_Wrap_StructuringElement ${WRAPPER_TEMPLATES})

WRAP_TYPE("itk::SpatialObject" "SO")
  FOREACH(d ${WRAP_ITK_DIMS})
    ADD_TEMPLATE("${d}"  "${d}")
  ENDFOREACH(d)
END_WRAP_TYPE()
SET(itk_Wrap_SpatialObject ${WRAPPER_TEMPLATES})

#------------------------------------------------------------------------------
