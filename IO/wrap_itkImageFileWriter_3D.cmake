WRAP_CLASS("ImageFileWriter" POINTER)

  COND_WRAP("${ITKM_IF3}"  "${ITKT_IF3}"  "F")
  COND_WRAP("${ITKM_ID3}"  "${ITKT_ID3}"  "D")
  COND_WRAP("${ITKM_IUC3}" "${ITKT_IUC3}" "")  # neded to save in 8 bits
  COND_WRAP("${ITKM_IUS3}" "${ITKT_IUS3}" "US")
  COND_WRAP("${ITKM_IUL3}" "${ITKT_IUL3}" "UL")
  COND_WRAP("${ITKM_ISC3}" "${ITKT_ISC3}" "SC")
  COND_WRAP("${ITKM_ISS3}" "${ITKT_ISS3}" "SS")
  COND_WRAP("${ITKM_ISL3}" "${ITKT_ISL3}" "SL")

END_WRAP_CLASS()
