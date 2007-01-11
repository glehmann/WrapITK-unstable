WRAP_LIBRARY(LevelSet)

SET(WRAPPER_LIBRARY_GROUPS
  itkLevelSetFunction
  itkSparseFieldLevelSetImageFilter
  itkSparseFieldFourthOrderLevelSetImageFilter
  itkSegmentationLevelSetImageFilter
  itkShapePriorSegmentationLevelSetImageFilter
)

SET(WRAPPER_LIBRARY_DEPENDS Base Numerics)

SET(WRAPPER_LIBRARY_LINK_LIBRARIES ITKCommon)

WRAPPER_LIBRARY_CREATE_WRAP_FILES()
END_WRAP_LIBRARY()

