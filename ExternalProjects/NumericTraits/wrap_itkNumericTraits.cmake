
# SET(WRAPPER_AUTO_INCLUDE_HEADERS OFF)
# WRAP_INCLUDE("itkNumericTraits.h")
WRAP_INCLUDE("itkNumericTraitsRGBPixel.h")
WRAP_INCLUDE("itkNumericTraitsTensorPixel.h")
WRAP_INCLUDE("itkNumericTraitsVariableLengthVectorPixel.h")
WRAP_INCLUDE("itkNumericTraitsVectorPixel.h")


WRAP_CLASS("itk::NumericTraits")
  # the basic types
  FOREACH(t UC US UI UL SC SS SI SL F D LD B)
    WRAP_TEMPLATE("${ITKM_${t}}" "${ITKT_${t}}")
  ENDFOREACH(t)
  
  # the ITK types
#  SET(WRAPPER_TEMPLATES ${WRAPPER_TEMPLATES} ${itk_Wrap_Vector} ${itk_Wrap_CovariantVector} ${itk_Wrap_RGBPixel})
  
  # TODO: the VariableLengthVectorPixel, which is not defined in WraITKTypes.cmake
  
END_WRAP_CLASS()
