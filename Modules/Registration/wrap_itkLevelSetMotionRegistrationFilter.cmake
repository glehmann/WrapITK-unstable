# DemonsRegistrationFilter is wrapped with POINTER_WITH_SUPERCLASS
# so this class is not.
WRAP_CLASS("itk::LevelSetMotionRegistrationFilter" POINTER)

  IF(WRAP_float)
    WRAP_IMAGE_FILTER_TYPES(F F VF 2+)
  ENDIF(WRAP_float)

  IF(WRAP_unsigned_short)
    WRAP_IMAGE_FILTER_TYPES(US US VF 2+)
  ENDIF(WRAP_unsigned_short)

END_WRAP_CLASS()
