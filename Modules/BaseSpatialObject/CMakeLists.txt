WRAP_LIBRARY(BaseSpatialObject)

SET(WRAPPER_LIBRARY_GROUPS
  itkSpatialObjectBase
  itkPointBasedSpatialObject
  itkImageSpatialObject
  itkTreeNodeSO
)

SET(WRAPPER_LIBRARY_DEPENDS Base BaseTransforms)

SET(WRAPPER_LIBRARY_LINK_LIBRARIES ITKCommon ITKSpatialObject)

WRAPPER_LIBRARY_CREATE_WRAP_FILES()
END_WRAP_LIBRARY()

