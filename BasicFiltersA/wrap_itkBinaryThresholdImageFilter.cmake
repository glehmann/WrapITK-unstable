WRAP_CLASS("itk::BinaryThresholdImageFilter" POINTER_WITH_SUPERCLASS)
  WRAP_INT(2)
  WRAP_SIGN_INT(2)
  WRAP_REAL(2)
  
  FOREACH(d ${WRAP_ITK_DIMS})
    WRAP_TEMPLATE_IF_TYPES("${ITKM_ID${d}}${ITKM_IF${d}}"  "${ITKT_ID${d}},${ITKT_IF${d}}"  "D;F")
    WRAP_TEMPLATE_IF_TYPES("${ITKM_ID${d}}${ITKM_IUL${d}}" "${ITKT_ID${d}},${ITKT_IUL${d}}" "D;UL")
    WRAP_TEMPLATE_IF_TYPES("${ITKM_ID${d}}${ITKM_IUS${d}}" "${ITKT_ID${d}},${ITKT_IUS${d}}" "D;US")
    WRAP_TEMPLATE_IF_TYPES("${ITKM_ID${d}}${ITKM_IUC${d}}" "${ITKT_ID${d}},${ITKT_IUC${d}}" "D;UC")
    WRAP_TEMPLATE_IF_TYPES("${ITKM_ID${d}}${ITKM_ISL${d}}" "${ITKT_ID${d}},${ITKT_ISL${d}}" "D;SL")
    WRAP_TEMPLATE_IF_TYPES("${ITKM_ID${d}}${ITKM_ISS${d}}" "${ITKT_ID${d}},${ITKT_ISS${d}}" "D;SS")
    WRAP_TEMPLATE_IF_TYPES("${ITKM_ID${d}}${ITKM_ISC${d}}" "${ITKT_ID${d}},${ITKT_ISC${d}}" "D;SC")
    
    WRAP_TEMPLATE_IF_TYPES("${ITKM_IF${d}}${ITKM_IUL${d}}" "${ITKT_IF${d}},${ITKT_IUL${d}}" "F;UL")
    WRAP_TEMPLATE_IF_TYPES("${ITKM_IF${d}}${ITKM_IUS${d}}" "${ITKT_IF${d}},${ITKT_IUS${d}}" "F;US")
    WRAP_TEMPLATE_IF_TYPES("${ITKM_IF${d}}${ITKM_IUC${d}}" "${ITKT_IF${d}},${ITKT_IUC${d}}" "F;UC")
    WRAP_TEMPLATE_IF_TYPES("${ITKM_IF${d}}${ITKM_ISL${d}}" "${ITKT_IF${d}},${ITKT_ISL${d}}" "F;SL")
    WRAP_TEMPLATE_IF_TYPES("${ITKM_IF${d}}${ITKM_ISS${d}}" "${ITKT_IF${d}},${ITKT_ISS${d}}" "F;SS")
    WRAP_TEMPLATE_IF_TYPES("${ITKM_IF${d}}${ITKM_ISC${d}}" "${ITKT_IF${d}},${ITKT_ISC${d}}" "F;SC")
    
    WRAP_TEMPLATE_IF_TYPES("${ITKM_IUL${d}}${ITKM_IUS${d}}" "${ITKT_IUL${d}},${ITKT_IUS${d}}" "UL;US")
    WRAP_TEMPLATE_IF_TYPES("${ITKM_IUL${d}}${ITKM_IUC${d}}" "${ITKT_IUL${d}},${ITKT_IUC${d}}" "UL;UC")
    WRAP_TEMPLATE_IF_TYPES("${ITKM_IUL${d}}${ITKM_ISL${d}}" "${ITKT_IUL${d}},${ITKT_ISL${d}}" "UL;SL")
    WRAP_TEMPLATE_IF_TYPES("${ITKM_IUL${d}}${ITKM_ISS${d}}" "${ITKT_IUL${d}},${ITKT_ISS${d}}" "UL;SS")
    WRAP_TEMPLATE_IF_TYPES("${ITKM_IUL${d}}${ITKM_ISC${d}}" "${ITKT_IUL${d}},${ITKT_ISC${d}}" "UL;SC")
    
    WRAP_TEMPLATE_IF_TYPES("${ITKM_IUS${d}}${ITKM_IUC${d}}" "${ITKT_IUS${d}},${ITKT_IUC${d}}" "US;UC")
    WRAP_TEMPLATE_IF_TYPES("${ITKM_IUS${d}}${ITKM_ISC${d}}" "${ITKT_IUS${d}},${ITKT_ISC${d}}" "US;SC")
    
    WRAP_TEMPLATE_IF_TYPES("${ITKM_ISL${d}}${ITKM_IUS${d}}" "${ITKT_ISL${d}},${ITKT_IUS${d}}" "SL;US")
    WRAP_TEMPLATE_IF_TYPES("${ITKM_ISL${d}}${ITKM_IUC${d}}" "${ITKT_ISL${d}},${ITKT_IUC${d}}" "SL;UC")
    WRAP_TEMPLATE_IF_TYPES("${ITKM_ISL${d}}${ITKM_ISS${d}}" "${ITKT_ISL${d}},${ITKT_ISS${d}}" "SL;SS")
    WRAP_TEMPLATE_IF_TYPES("${ITKM_ISL${d}}${ITKM_ISC${d}}" "${ITKT_ISL${d}},${ITKT_ISC${d}}" "SL;SC")
    
    WRAP_TEMPLATE_IF_TYPES("${ITKM_ISS${d}}${ITKM_IUC${d}}" "${ITKT_ISS${d}},${ITKT_IUC${d}}" "SS;UC")
    WRAP_TEMPLATE_IF_TYPES("${ITKM_ISS${d}}${ITKM_ISC${d}}" "${ITKT_ISS${d}},${ITKT_ISC${d}}" "SS;SC")
  ENDFOREACH(d)

END_WRAP_CLASS()
