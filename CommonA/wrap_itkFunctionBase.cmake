WRAP_CLASS("itk::FunctionBase" POINTER)
  FOREACH(d ${WRAP_ITK_DIMS})
    WRAP_TYPES("${ITKM_IF${d}}${ITKM_D}"   "${ITKT_IF${d}},${ITKT_D}"  "F")
    WRAP_TYPES("${ITKM_IUS${d}}${ITKM_D}"  "${ITKT_IUS${d}},${ITKT_D}" "US")
    WRAP("${ITKM_PF${d}}${ITKM_D}"   "${ITKT_PF${d}} ,${ITKT_D}")
    WRAP("${ITKM_PD${d}}${ITKM_D}"   "${ITKT_PD${d}} ,${ITKT_D}")
    WRAP("${ITKM_CIF${d}}${ITKM_AD}" "${ITKT_CIF${d}} ,${ITKT_AD}")
    WRAP("${ITKM_CID${d}}${ITKM_AD}" "${ITKT_CID${d}} ,${ITKT_AD}")
  ENDFOREACH(d)

  WRAP("${ITKM_D}${ITKM_D}"     "${ITKT_D},${ITKT_D}")
END_WRAP_CLASS()
