WRAP_CLASS("CastImageFilter" POINTER_WITH_SUPERCLASS)

  COND_WRAP("${ITKM_ID2}${ITKM_ID2}"  "${ITKT_ID2},${ITKT_ID2}"  "D")
  COND_WRAP("${ITKM_ID2}${ITKM_IF2}"  "${ITKT_ID2},${ITKT_IF2}"  "D;F")
  COND_WRAP("${ITKM_ID2}${ITKM_IUL2}" "${ITKT_ID2},${ITKT_IUL2}" "D;UL")
  COND_WRAP("${ITKM_ID2}${ITKM_IUS2}" "${ITKT_ID2},${ITKT_IUS2}" "D;US")
  COND_WRAP("${ITKM_ID2}${ITKM_IUC2}" "${ITKT_ID2},${ITKT_IUC2}" "D") # needed to save in 8 bits
  COND_WRAP("${ITKM_ID2}${ITKM_ISL2}" "${ITKT_ID2},${ITKT_ISL2}" "D;SL")
  COND_WRAP("${ITKM_ID2}${ITKM_ISS2}" "${ITKT_ID2},${ITKT_ISS2}" "D;SS")
  COND_WRAP("${ITKM_ID2}${ITKM_ISC2}" "${ITKT_ID2},${ITKT_ISC2}" "D;SC")
  
  COND_WRAP("${ITKM_IF2}${ITKM_ID2}"  "${ITKT_IF2},${ITKT_ID2}"  "F;D")
  COND_WRAP("${ITKM_IF2}${ITKM_IF2}"  "${ITKT_IF2},${ITKT_IF2}"  "F")
  COND_WRAP("${ITKM_IF2}${ITKM_IUL2}" "${ITKT_IF2},${ITKT_IUL2}" "F;UL")
  COND_WRAP("${ITKM_IF2}${ITKM_IUS2}" "${ITKT_IF2},${ITKT_IUS2}" "F;US")
  COND_WRAP("${ITKM_IF2}${ITKM_IUC2}" "${ITKT_IF2},${ITKT_IUC2}" "F") # needed to save in 8 bits
  COND_WRAP("${ITKM_IF2}${ITKM_ISL2}" "${ITKT_IF2},${ITKT_ISL2}" "F;SL")
  COND_WRAP("${ITKM_IF2}${ITKM_ISS2}" "${ITKT_IF2},${ITKT_ISS2}" "F;SS")
  COND_WRAP("${ITKM_IF2}${ITKM_ISC2}" "${ITKT_IF2},${ITKT_ISC2}" "F;SC")
  
  COND_WRAP("${ITKM_IUL2}${ITKM_ID2}"  "${ITKT_IUL2},${ITKT_ID2}"  "UL;D")
  COND_WRAP("${ITKM_IUL2}${ITKM_IF2}"  "${ITKT_IUL2},${ITKT_IF2}"  "UL;F")
  COND_WRAP("${ITKM_IUL2}${ITKM_IUL2}" "${ITKT_IUL2},${ITKT_IUL2}" "UL")
  COND_WRAP("${ITKM_IUL2}${ITKM_IUS2}" "${ITKT_IUL2},${ITKT_IUS2}" "UL;US")
  COND_WRAP("${ITKM_IUL2}${ITKM_IUC2}" "${ITKT_IUL2},${ITKT_IUC2}" "UL") # needed to save in 8 bits
  COND_WRAP("${ITKM_IUL2}${ITKM_ISL2}" "${ITKT_IUL2},${ITKT_ISL2}" "UL;SL")
  COND_WRAP("${ITKM_IUL2}${ITKM_ISS2}" "${ITKT_IUL2},${ITKT_ISS2}" "UL;SS")
  COND_WRAP("${ITKM_IUL2}${ITKM_ISC2}" "${ITKT_IUL2},${ITKT_ISC2}" "UL;SC")
  
  COND_WRAP("${ITKM_IUS2}${ITKM_ID2}"  "${ITKT_IUS2},${ITKT_ID2}"  "US;D")
  COND_WRAP("${ITKM_IUS2}${ITKM_IF2}"  "${ITKT_IUS2},${ITKT_IF2}"  "US;F")
  COND_WRAP("${ITKM_IUS2}${ITKM_IUL2}" "${ITKT_IUS2},${ITKT_IUL2}" "US;UL")
  COND_WRAP("${ITKM_IUS2}${ITKM_IUS2}" "${ITKT_IUS2},${ITKT_IUS2}" "US")
  COND_WRAP("${ITKM_IUS2}${ITKM_IUC2}" "${ITKT_IUS2},${ITKT_IUC2}" "US") # needed to save in 8 bits
  COND_WRAP("${ITKM_IUS2}${ITKM_ISL2}" "${ITKT_IUS2},${ITKT_ISL2}" "US;SL")
  COND_WRAP("${ITKM_IUS2}${ITKM_ISS2}" "${ITKT_IUS2},${ITKT_ISS2}" "US;SS")
  COND_WRAP("${ITKM_IUS2}${ITKM_ISC2}" "${ITKT_IUS2},${ITKT_ISC2}" "US;SC")
  
  COND_WRAP("${ITKM_IUC2}${ITKM_ID2}"  "${ITKT_IUC2},${ITKT_ID2}"  "UC;D")
  COND_WRAP("${ITKM_IUC2}${ITKM_IF2}"  "${ITKT_IUC2},${ITKT_IF2}"  "UC;F")
  COND_WRAP("${ITKM_IUC2}${ITKM_IUL2}" "${ITKT_IUC2},${ITKT_IUL2}" "UC;UL")
  COND_WRAP("${ITKM_IUC2}${ITKM_IUS2}" "${ITKT_IUC2},${ITKT_IUS2}" "UC;US")
  COND_WRAP("${ITKM_IUC2}${ITKM_IUC2}" "${ITKT_IUC2},${ITKT_IUC2}" "UC")
  COND_WRAP("${ITKM_IUC2}${ITKM_ISL2}" "${ITKT_IUC2},${ITKT_ISL2}" "UC;SL")
  COND_WRAP("${ITKM_IUC2}${ITKM_ISS2}" "${ITKT_IUC2},${ITKT_ISS2}" "UC;SS")
  COND_WRAP("${ITKM_IUC2}${ITKM_ISC2}" "${ITKT_IUC2},${ITKT_ISC2}" "UC;SC")
  
  COND_WRAP("${ITKM_ISL2}${ITKM_ID2}"  "${ITKT_ISL2},${ITKT_ID2}"  "SL;D")
  COND_WRAP("${ITKM_ISL2}${ITKM_IF2}"  "${ITKT_ISL2},${ITKT_IF2}"  "SL;F")
  COND_WRAP("${ITKM_ISL2}${ITKM_IUL2}" "${ITKT_ISL2},${ITKT_IUL2}" "SL;UL")
  COND_WRAP("${ITKM_ISL2}${ITKM_IUS2}" "${ITKT_ISL2},${ITKT_IUS2}" "SL;US")
  COND_WRAP("${ITKM_ISL2}${ITKM_IUC2}" "${ITKT_ISL2},${ITKT_IUC2}" "SL") # needed to save in 8 bits
  COND_WRAP("${ITKM_ISL2}${ITKM_ISL2}" "${ITKT_ISL2},${ITKT_ISL2}" "SL")
  COND_WRAP("${ITKM_ISL2}${ITKM_ISS2}" "${ITKT_ISL2},${ITKT_ISS2}" "SL;SS")
  COND_WRAP("${ITKM_ISL2}${ITKM_ISC2}" "${ITKT_ISL2},${ITKT_ISC2}" "SL;SC")
  
  COND_WRAP("${ITKM_ISS2}${ITKM_ID2}"  "${ITKT_ISS2},${ITKT_ID2}"  "SS;D")
  COND_WRAP("${ITKM_ISS2}${ITKM_IF2}"  "${ITKT_ISS2},${ITKT_IF2}"  "SS;F")
  COND_WRAP("${ITKM_ISS2}${ITKM_IUL2}" "${ITKT_ISS2},${ITKT_IUL2}" "SS;UL")
  COND_WRAP("${ITKM_ISS2}${ITKM_IUS2}" "${ITKT_ISS2},${ITKT_IUS2}" "SS;US")
  COND_WRAP("${ITKM_ISS2}${ITKM_IUC2}" "${ITKT_ISS2},${ITKT_IUC2}" "SS") # needed to save in 8 bits
  COND_WRAP("${ITKM_ISS2}${ITKM_ISL2}" "${ITKT_ISS2},${ITKT_ISL2}" "SS;SL")
  COND_WRAP("${ITKM_ISS2}${ITKM_ISS2}" "${ITKT_ISS2},${ITKT_ISS2}" "SS")
  COND_WRAP("${ITKM_ISS2}${ITKM_ISC2}" "${ITKT_ISS2},${ITKT_ISC2}" "SS;SC")
  
  COND_WRAP("${ITKM_ISC2}${ITKM_ID2}"  "${ITKT_ISC2},${ITKT_ID2}"  "SC;D")
  COND_WRAP("${ITKM_ISC2}${ITKM_IF2}"  "${ITKT_ISC2},${ITKT_IF2}"  "SC;F")
  COND_WRAP("${ITKM_ISC2}${ITKM_IUL2}" "${ITKT_ISC2},${ITKT_IUL2}" "SC;UL")
  COND_WRAP("${ITKM_ISC2}${ITKM_IUS2}" "${ITKT_ISC2},${ITKT_IUS2}" "SC;US")
  COND_WRAP("${ITKM_ISC2}${ITKM_IUC2}" "${ITKT_ISC2},${ITKT_IUC2}" "SC") # needed to save in 8 bits
  COND_WRAP("${ITKM_ISC2}${ITKM_ISL2}" "${ITKT_ISC2},${ITKT_ISL2}" "SC;SL")
  COND_WRAP("${ITKM_ISC2}${ITKM_ISS2}" "${ITKT_ISC2},${ITKT_ISS2}" "SC;SS")
  COND_WRAP("${ITKM_ISC2}${ITKM_ISC2}" "${ITKT_ISC2},${ITKT_ISC2}" "SC")
  
  # vector types
  COND_WRAP("${ITKM_IVD22}${ITKM_IVD22}"  "${ITKT_IVD22},${ITKT_IVD22}"  "VD")
  COND_WRAP("${ITKM_IVF22}${ITKM_IVF22}"  "${ITKT_IVF22},${ITKT_IVF22}"  "VF")
  COND_WRAP("${ITKM_ICVD22}${ITKM_ICVD22}"  "${ITKT_ICVD22},${ITKT_ICVD22}"  "CVD")
  COND_WRAP("${ITKM_ICVF22}${ITKM_ICVF22}"  "${ITKT_ICVF22},${ITKT_ICVF22}"  "CVF")
  
END_WRAP_CLASS()

