WRAP_LIBRARY(Registration)

SET(WRAPPER_LIBRARY_GROUPS
  itkPDEDeformableRegistrationFilter
)

SET(WRAPPER_LIBRARY_DEPENDS 
  Base 
  BaseNumerics
  BaseTransforms 
  BaseSpatialObject
  Resize
)

SET(WRAPPER_LIBRARY_LINK_LIBRARIES ITKCommon ITKNumerics)

WRAPPER_LIBRARY_CREATE_WRAP_FILES()
END_WRAP_LIBRARY()

