WRAP_CLASS("GrayscaleMorphologicalClosingImageFilter" POINTER)

  COND_WRAP("${ITKM_IF2}${ITKM_IF2}${ITKM_SEF2}"    "${ITKT_IF2},${ITKT_IF2},${ITKT_SEF2}"    "F")
  COND_WRAP("${ITKM_IF3}${ITKM_IF3}${ITKM_SEF3}"    "${ITKT_IF3},${ITKT_IF3},${ITKT_SEF3}"    "F")
  
  COND_WRAP("${ITKM_ID2}${ITKM_ID2}${ITKM_SED2}"    "${ITKT_ID2},${ITKT_ID2},${ITKT_SED2}"    "D")
  COND_WRAP("${ITKM_ID3}${ITKM_ID3}${ITKM_SED3}"    "${ITKT_ID3},${ITKT_ID3},${ITKT_SED3}"    "D")
  
  COND_WRAP("${ITKM_IUL2}${ITKM_IUL2}${ITKM_SEUL2}" "${ITKT_IUL2},${ITKT_IUL2},${ITKT_SEUL2}" "UL")
  COND_WRAP("${ITKM_IUL3}${ITKM_IUL3}${ITKM_SEUL3}" "${ITKT_IUL3},${ITKT_IUL3},${ITKT_SEUL3}" "UL")
  
  COND_WRAP("${ITKM_IUS2}${ITKM_IUS2}${ITKM_SEUS2}" "${ITKT_IUS2},${ITKT_IUS2},${ITKT_SEUS2}" "US")
  COND_WRAP("${ITKM_IUS3}${ITKM_IUS3}${ITKM_SEUS3}" "${ITKT_IUS3},${ITKT_IUS3},${ITKT_SEUS3}" "US")
  
  COND_WRAP("${ITKM_IUC2}${ITKM_IUC2}${ITKM_SEUC2}" "${ITKT_IUC2},${ITKT_IUC2},${ITKT_SEUC2}" "UC")
  COND_WRAP("${ITKM_IUC3}${ITKM_IUC3}${ITKM_SEUC3}" "${ITKT_IUC3},${ITKT_IUC3},${ITKT_SEUC3}" "UC")
  
  COND_WRAP("${ITKM_ISL2}${ITKM_ISL2}${ITKM_SESL2}" "${ITKT_ISL2},${ITKT_ISL2},${ITKT_SESL2}" "SL")
  COND_WRAP("${ITKM_ISL3}${ITKM_ISL3}${ITKM_SESL3}" "${ITKT_ISL3},${ITKT_ISL3},${ITKT_SESL3}" "SL")
  
  COND_WRAP("${ITKM_ISS2}${ITKM_ISS2}${ITKM_SESS2}" "${ITKT_ISS2},${ITKT_ISS2},${ITKT_SESS2}" "SS")
  COND_WRAP("${ITKM_ISS3}${ITKM_ISS3}${ITKM_SESS3}" "${ITKT_ISS3},${ITKT_ISS3},${ITKT_SESS3}" "SS")
  
  COND_WRAP("${ITKM_ISC2}${ITKM_ISC2}${ITKM_SESC2}" "${ITKT_ISC2},${ITKT_ISC2},${ITKT_SESC2}" "SC")
  COND_WRAP("${ITKM_ISC3}${ITKM_ISC3}${ITKM_SESC3}" "${ITKT_ISC3},${ITKT_ISC3},${ITKT_SESC3}" "SC")

END_WRAP_CLASS()
