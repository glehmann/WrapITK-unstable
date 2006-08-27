WRAP_CLASS("itk::VectorCastImageFilter" POINTER_WITH_SUPERCLASS)
  # vector <-> vector
  WRAP_IMAGE_FILTER_COMBINATIONS("${WRAP_ITK_VECTOR}" "${WRAP_ITK_VECTOR}")
  
  # RGB <-> RGB
  UNIQUE(rgb "RGBUC;${WRAP_ITK_RGB}")
  WRAP_IMAGE_FILTER_COMBINATIONS("${rgb}" "${rgb}")
  
  # vector <-> RGB
  # WRAP_IMAGE_FILTER_COMBINATIONS("${WRAP_ITK_VECTOR}" "${WRAP_ITK_RGB}" 3)
  # WRAP_IMAGE_FILTER_COMBINATIONS("${WRAP_ITK_RGB}" "${WRAP_ITK_VECTOR}" 3)
END_WRAP_CLASS()