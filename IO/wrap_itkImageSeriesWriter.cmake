WRAP_CLASS("ImageSeriesWriter" POINTER)
# 
#   COND_WRAP("${ITKM_IF3}${ITKM_IF2}"   "${ITKT_IF3},${ITKT_IF2}"   "F")
#   COND_WRAP("${ITKM_ID3}${ITKM_ID2}"   "${ITKT_ID3},${ITKT_ID2}"   "D")
#   COND_WRAP("${ITKM_IUC3}${ITKM_IUC2}" "${ITKT_IUC3},${ITKT_IUC2}" "") # needed to write in 8 bits
#   COND_WRAP("${ITKM_IUS3}${ITKM_IUS2}" "${ITKT_IUS3},${ITKT_IUS2}" "US")
#   COND_WRAP("${ITKM_IUL3}${ITKM_IUL2}" "${ITKT_IUL3},${ITKT_IUL2}" "UL")
#   COND_WRAP("${ITKM_ISC3}${ITKM_ISC2}" "${ITKT_ISC3},${ITKT_ISC2}" "SC")
#   COND_WRAP("${ITKM_ISS3}${ITKM_ISS2}" "${ITKT_ISS3},${ITKT_ISS2}" "SS")
#   COND_WRAP("${ITKM_ISL3}${ITKM_ISL2}" "${ITKT_ISL3},${ITKT_ISL2}" "SL")
# 
END_WRAP_CLASS()
