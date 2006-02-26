WRAP_CLASS("itk::ErodeObjectMorphologyImageFilter" POINTER)
    FOREACH(d ${WRAP_ITK_DIMS})
    FOREACH(t ${WRAP_ITK_SCALAR})
      WRAP_TEMPLATE("${ITKM_I${t}${d}}${ITKM_I${t}${d}}${ITKM_SE${t}${d}}" 
                    "${ITKT_I${t}${d}},${ITKT_I${t}${d}},${ITKT_SE${t}${d}}")
    ENDFOREACH(t)
  ENDFOREACH(d)
END_WRAP_CLASS()
