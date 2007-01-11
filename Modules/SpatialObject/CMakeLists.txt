WRAP_LIBRARY(SpatialObject)

SET(WRAPPER_LIBRARY_GROUPS
  itkSpatialObjectBase
  itkPointBasedSpatialObject
  itkImageSpatialObject
  itkTreeNodeSO
  itkSpatialObjectPoint
)

SET(WRAPPER_LIBRARY_DEPENDS Base Transforms)

SET(WRAPPER_LIBRARY_LINK_LIBRARIES ITKCommon ITKSpatialObject)

WRAPPER_LIBRARY_CREATE_WRAP_FILES()
END_WRAP_LIBRARY()

