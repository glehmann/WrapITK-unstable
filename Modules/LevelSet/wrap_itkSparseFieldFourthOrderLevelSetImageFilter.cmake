# auto include feature must be disable because all the following classes are in the same file
SET(WRAPPER_AUTO_INCLUDE_HEADERS OFF)
WRAP_INCLUDE("itkSparseFieldFourthOrderLevelSetImageFilter.h")

WRAP_CLASS("itk::NormalBandNode")
  WRAP_IMAGE_FILTER_REAL(1)
END_WRAP_CLASS()

WRAP_CLASS("itk::Image" POINTER)
  FOREACH(d ${WRAP_ITK_DIMS})
    FOREACH(t ${WRAP_ITK_REAL})
      WRAP_TEMPLATE("NBN${ITKM_I${t}${d}}${d}" "itk::NormalBandNode< ${ITKT_I${t}${d}} >*, ${d}")    
    ENDFOREACH(t)
  ENDFOREACH(d)
END_WRAP_CLASS()

WRAP_CLASS("itk::SparseFieldFourthOrderLevelSetImageFilter" POINTER)
  # WRAP_IMAGE_FILTER_USIGN_INT(2)
  # WRAP_IMAGE_FILTER_SIGN_INT(2)
  WRAP_IMAGE_FILTER_REAL(2)
END_WRAP_CLASS()

# itk::LevelSetFunctionWithRefitTerm< itk::Image< float, 2 >, itk::SparseImage< itk::NormalBandNode< itk::Image< float, 2 > >, 2 > >
# itk::SparseImage< itk::NormalBandNode< itk::Image< float, 2 > >, 2 >
# itk::SparseFieldLayer< itk::NormalBandNode< itk::Image< float, 2 > > >

WRAP_CLASS("itk::SparseImage" POINTER)
  FOREACH(d ${WRAP_ITK_DIMS})
    FOREACH(t ${WRAP_ITK_REAL})
      WRAP_TEMPLATE("NBN${ITKM_I${t}${d}}${d}" "itk::NormalBandNode< ${ITKT_I${t}${d}} >, ${d}")    
    ENDFOREACH(t)
  ENDFOREACH(d)
END_WRAP_CLASS()

WRAP_CLASS("itk::LevelSetFunctionWithRefitTerm" POINTER)
  FOREACH(d ${WRAP_ITK_DIMS})
    FOREACH(t ${WRAP_ITK_REAL})
      WRAP_TEMPLATE("${ITKM_I${t}${d}}SINBN${ITKM_I${t}${d}}${d}" "${ITKT_I${t}${d}}, itk::SparseImage< itk::NormalBandNode< ${ITKT_I${t}${d}} >, ${d} >")    
    ENDFOREACH(t)
  ENDFOREACH(d)
END_WRAP_CLASS()

WRAP_CLASS("itk::SparseFieldLayer" POINTER)
  FOREACH(d ${WRAP_ITK_DIMS})
    FOREACH(t ${WRAP_ITK_REAL})
      WRAP_TEMPLATE("NBN${ITKM_I${t}${d}}" "itk::NormalBandNode< ${ITKT_I${t}${d}} >")
    ENDFOREACH(t)
  ENDFOREACH(d)
END_WRAP_CLASS()
