WRAP_CLASS("itk::ImageToImageFilter" POINTER)
  # Wrap from each scalar type to each other, and also to uchar (for 8-bit saving)
  # and to ulong (for watershed).
  UNIQUE(from_types "UC;${WRAP_ITK_SCALAR}")
  UNIQUE(to_types "UC;UL;${WRAP_ITK_SCALAR}")
  WRAP_IMAGE_FILTER_COMBINATIONS("${from_types}" "${to_types}")
  
  # Wrap from ulong to other integral types, even if ulong isn't wrapped. This
  # is needed for the relabel components image filter.
  IF(NOT WRAP_unsigned_long)
    WRAP_IMAGE_FILTER_COMBINATIONS("UL" "${WRAP_ITK_INT}")
  ENDIF(NOT WRAP_unsigned_long)
  
  # Vector types
  WRAP_IMAGE_FILTER_VECTOR_REAL(2)
  WRAP_IMAGE_FILTER_COV_VECTOR_REAL(2)
  
  # RGB types
  WRAP_IMAGE_FILTER_RGB(2)
 
  # int <-> RGB
  IF(WRAP_rgb_unsigned_char AND WRAP_unsigned_char)
    WRAP_IMAGE_FILTER_TYPES(RGBUC UC)
  ENDIF(WRAP_rgb_unsigned_char AND WRAP_unsigned_char)

  IF(WRAP_rgb_unsigned_short AND WRAP_unsigned_short)
    WRAP_IMAGE_FILTER_TYPES(RGBUS US)
  ENDIF(WRAP_rgb_unsigned_short AND WRAP_unsigned_short)

  IF(WRAP_rgb_unsigned_char)
    UNIQUE(types "UL;${WRAP_ITK_SCALAR}")
    WRAP_IMAGE_FILTER_COMBINATIONS("${types}" "RGBUC")
  ENDIF(WRAP_rgb_unsigned_char)

  IF(WRAP_rgb_unsigned_short)
    UNIQUE(types "UL;${WRAP_ITK_SCALAR}")
    WRAP_IMAGE_FILTER_COMBINATIONS("${types}" "RGBUS")
  ENDIF(WRAP_rgb_unsigned_short)

  # VectorImage <-> scalar
  UNIQUE(to_types "UC;${WRAP_ITK_SCALAR}")
    FOREACH(d ${WRAP_ITK_DIMS})
      FOREACH(t ${to_types})
        WRAP_TEMPLATE("${ITKM_VI${t}${d}}${ITKM_I${t}${d}}" "${ITKT_VI${t}${d}},${ITKT_I${t}${d}}")
        WRAP_TEMPLATE("${ITKM_I${t}${d}}${ITKM_VI${t}${d}}" "${ITKT_I${t}${d}},${ITKT_VI${t}${d}}")
      ENDFOREACH(t)
    ENDFOREACH(d)
      
  # Vector <-> scalar
  IF(WRAP_vector_double AND WRAP_double)
    WRAP_IMAGE_FILTER_TYPES(VD D)
    WRAP_IMAGE_FILTER_TYPES(D VD)
  ENDIF(WRAP_vector_double AND WRAP_double)
		    
  IF(WRAP_vector_float AND WRAP_float)
    WRAP_IMAGE_FILTER_TYPES(VF F)
    WRAP_IMAGE_FILTER_TYPES(F VF)
  ENDIF(WRAP_vector_float AND WRAP_float)
				
  # complex <-> scalar
  IF(WRAP_complex_float AND WRAP_float)
    WRAP_IMAGE_FILTER_TYPES(CF F)
    WRAP_IMAGE_FILTER_TYPES(F CF)
  ENDIF(WRAP_complex_float AND WRAP_float)

  IF(WRAP_complex_double AND WRAP_double)
    WRAP_IMAGE_FILTER_TYPES(CD D)
    WRAP_IMAGE_FILTER_TYPES(D CD)
  ENDIF(WRAP_complex_double AND WRAP_double)

  # Wrap dim=3 -> dim=2, dim=3 -> dim=2, etc.
  FOREACH(d ${WRAP_ITK_DIMS})    
    FOREACH(d2 ${WRAP_ITK_DIMS})
      IF (NOT "${d}" EQUAL "${d2}") # this was already taken care of elsewhere
        FOREACH(t ${WRAP_ITK_SCALAR})
          WRAP_TEMPLATE("${ITKM_I${t}${d}}${ITKM_I${t}${d2}}"
                        "${ITKT_I${t}${d}},${ITKT_I${t}${d2}}")
        ENDFOREACH(t)
      ENDIF(NOT "${d}" EQUAL "${d2}")
    ENDFOREACH(d2)
  ENDFOREACH(d)

END_WRAP_CLASS()

