FILTER_DIMS(d3 3)
IF(d3)
  WRAP_CLASS("itk::ScaleSkewVersor3DTransform" POINTER)
    WRAP_TEMPLATE("${ITKM_D}" "${ITKT_D}")
  END_WRAP_CLASS()
ENDIF(d3)
