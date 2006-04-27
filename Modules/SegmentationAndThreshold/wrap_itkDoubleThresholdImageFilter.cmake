WRAP_CLASS("itk::DoubleThresholdImageFilter" POINTER)
  WRAP_IMAGE_FILTER_INT(2)
  WRAP_IMAGE_FILTER_SIGN_INT(2)
  WRAP_IMAGE_FILTER_REAL(2)
  
  # Wrap from all real types to all unsigned integral types
  WRAP_IMAGE_FILTER_COMBINATIONS("${WRAP_ITK_REAL}" "${WRAP_ITK_INT}")
END_WRAP_CLASS()