WRAP_LIBRARY(BaseTransforms)

SET(WRAPPER_LIBRARY_GROUPS
  itkTransform
  itkMatrixOffsetTransformBase
  ITKRigidTransforms
  ITKEulerTransform
  itkVersorTransform
  ITKVersorRigidTransform
  ITKSimilarityTransforms
  itkAffineTransform
  itkScalableAffineTransform
  itkScaleTransform
)

SET(WRAPPER_LIBRARY_DEPENDS Base)

SET(WRAPPER_LIBRARY_LINK_LIBRARIES ITKCommon)

WRAPPER_LIBRARY_CREATE_WRAP_FILES()
END_WRAP_LIBRARY()
