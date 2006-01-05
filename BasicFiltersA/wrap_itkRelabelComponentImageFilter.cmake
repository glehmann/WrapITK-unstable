WRAP_CLASS("RelabelComponentImageFilter" POINTER)
  WRAP_INT(2)
  WRAP_SIGN_INT(2)
  # needed with watershed filter to return to a non UL type
  COND_WRAP("${ITKM_IUL2}${ITKM_IUS2}" "${ITKT_IUL2},${ITKT_IUS2}" "US")
  COND_WRAP("${ITKM_IUL2}${ITKM_IUC2}" "${ITKT_IUL2},${ITKT_IUC2}" "UC")
  COND_WRAP("${ITKM_IUL2}${ITKM_ISL2}" "${ITKT_IUL2},${ITKT_ISL2}" "SL")
  COND_WRAP("${ITKM_IUL2}${ITKM_ISS2}" "${ITKT_IUL2},${ITKT_ISS2}" "SS")
  COND_WRAP("${ITKM_IUL2}${ITKM_ISC2}" "${ITKT_IUL2},${ITKT_ISC2}" "SC")
  
  COND_WRAP("${ITKM_IUS2}${ITKM_IUC2}" "${ITKT_IUS2},${ITKT_IUC2}" "US;UC")
  COND_WRAP("${ITKM_IUS2}${ITKM_ISC2}" "${ITKT_IUS2},${ITKT_ISC2}" "US;SC")
  
  COND_WRAP("${ITKM_ISL2}${ITKM_IUS2}" "${ITKT_ISL2},${ITKT_IUS2}" "SL;US")
  COND_WRAP("${ITKM_ISL2}${ITKM_IUC2}" "${ITKT_ISL2},${ITKT_IUC2}" "SL;UC")
  COND_WRAP("${ITKM_ISL2}${ITKM_ISS2}" "${ITKT_ISL2},${ITKT_ISS2}" "SL;SS")
  COND_WRAP("${ITKM_ISL2}${ITKM_ISC2}" "${ITKT_ISL2},${ITKT_ISC2}" "SL;SC")
  
  COND_WRAP("${ITKM_ISS2}${ITKM_IUC2}" "${ITKT_ISS2},${ITKT_IUC2}" "SS;UC")
  COND_WRAP("${ITKM_ISS2}${ITKM_ISC2}" "${ITKT_ISS2},${ITKT_ISC2}" "SS;SC")
  
  
  COND_WRAP("${ITKM_IUL3}${ITKM_IUS3}" "${ITKT_IUL3},${ITKT_IUS3}" "US")
  COND_WRAP("${ITKM_IUL3}${ITKM_IUC3}" "${ITKT_IUL3},${ITKT_IUC3}" "UC")
  COND_WRAP("${ITKM_IUL3}${ITKM_ISL3}" "${ITKT_IUL3},${ITKT_ISL3}" "SL")
  COND_WRAP("${ITKM_IUL3}${ITKM_ISS3}" "${ITKT_IUL3},${ITKT_ISS3}" "SS")
  COND_WRAP("${ITKM_IUL3}${ITKM_ISC3}" "${ITKT_IUL3},${ITKT_ISC3}" "SC")
  
  COND_WRAP("${ITKM_IUS3}${ITKM_IUC3}" "${ITKT_IUS3},${ITKT_IUC3}" "US;UC")
  COND_WRAP("${ITKM_IUS3}${ITKM_ISC3}" "${ITKT_IUS3},${ITKT_ISC3}" "US;SC")
  
  COND_WRAP("${ITKM_ISL3}${ITKM_IUS3}" "${ITKT_ISL3},${ITKT_IUS3}" "SL;US")
  COND_WRAP("${ITKM_ISL3}${ITKM_IUC3}" "${ITKT_ISL3},${ITKT_IUC3}" "SL;UC")
  COND_WRAP("${ITKM_ISL3}${ITKM_ISS3}" "${ITKT_ISL3},${ITKT_ISS3}" "SL;SS")
  COND_WRAP("${ITKM_ISL3}${ITKM_ISC3}" "${ITKT_ISL3},${ITKT_ISC3}" "SL;SC")
  
  COND_WRAP("${ITKM_ISS3}${ITKM_IUC3}" "${ITKT_ISS3},${ITKT_IUC3}" "SS;UC")
  COND_WRAP("${ITKM_ISS3}${ITKM_ISC3}" "${ITKT_ISS3},${ITKT_ISC3}" "SS;SC")

END_WRAP_CLASS()
