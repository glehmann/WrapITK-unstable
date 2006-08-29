# only available for dim 3

FILTER_DIMS(d 3)
IF(d)
  WRAP_NON_TEMPLATE_CLASS("itk::CylinderSpatialObject" POINTER)
ENDIF(d)
