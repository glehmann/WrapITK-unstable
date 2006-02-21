WRAP_CLASS("itk::GrayscaleDilateImageFilter" POINTER)
  FOREACH(d ${WRAP_ITK_DIMS})
    WRAP_TYPES("${ITKM_IF${d}}${ITKM_IF${d}}${ITKM_SEF${d}}"    "${ITKT_IF${d}},${ITKT_IF${d}},${ITKT_SEF${d}}"    "F")
    WRAP_TYPES("${ITKM_ID${d}}${ITKM_ID${d}}${ITKM_SED${d}}"    "${ITKT_ID${d}},${ITKT_ID${d}},${ITKT_SED${d}}"    "D")
    WRAP_TYPES("${ITKM_IUL${d}}${ITKM_IUL${d}}${ITKM_SEUL${d}}" "${ITKT_IUL${d}},${ITKT_IUL${d}},${ITKT_SEUL${d}}" "UL")
    WRAP_TYPES("${ITKM_IUS${d}}${ITKM_IUS${d}}${ITKM_SEUS${d}}" "${ITKT_IUS${d}},${ITKT_IUS${d}},${ITKT_SEUS${d}}" "US")
    WRAP_TYPES("${ITKM_IUC${d}}${ITKM_IUC${d}}${ITKM_SEUC${d}}" "${ITKT_IUC${d}},${ITKT_IUC${d}},${ITKT_SEUC${d}}" "UC")
    WRAP_TYPES("${ITKM_ISL${d}}${ITKM_ISL${d}}${ITKM_SESL${d}}" "${ITKT_ISL${d}},${ITKT_ISL${d}},${ITKT_SESL${d}}" "SL")
    WRAP_TYPES("${ITKM_ISS${d}}${ITKM_ISS${d}}${ITKM_SESS${d}}" "${ITKT_ISS${d}},${ITKT_ISS${d}},${ITKT_SESS${d}}" "SS")
    WRAP_TYPES("${ITKM_ISC${d}}${ITKM_ISC${d}}${ITKM_SESC${d}}" "${ITKT_ISC${d}},${ITKT_ISC${d}},${ITKT_SESC${d}}" "SC")
  ENDFOREACH(d)
END_WRAP_CLASS()
