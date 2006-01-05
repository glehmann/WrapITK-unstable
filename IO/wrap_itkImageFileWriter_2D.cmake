WRAP_CLASS("ImageFileWriter" POINTER)

  COND_WRAP("${ITKM_IF2}"  "${ITKT_IF2}"  "F")
  COND_WRAP("${ITKM_ID2}"  "${ITKT_ID2}"  "D")
  COND_WRAP("${ITKM_IUC2}" "${ITKT_IUC2}" "")  # neded to save in 8 bits
  COND_WRAP("${ITKM_IUS2}" "${ITKT_IUS2}" "US")
  COND_WRAP("${ITKM_IUL2}" "${ITKT_IUL2}" "UL")
  COND_WRAP("${ITKM_ISC2}" "${ITKT_ISC2}" "SC")
  COND_WRAP("${ITKM_ISS2}" "${ITKT_ISS2}" "SS")
  COND_WRAP("${ITKM_ISL2}" "${ITKT_ISL2}" "SL")

END_WRAP_CLASS()
