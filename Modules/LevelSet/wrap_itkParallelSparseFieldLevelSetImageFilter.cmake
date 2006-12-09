WRAP_INCLUDE("itkIndex.h")

WRAP_CLASS("itk::ParallelSparseFieldLevelSetImageFilter" POINTER)
  WRAP_IMAGE_FILTER_REAL(2)
END_WRAP_CLASS()


SET(WRAPPER_AUTO_INCLUDE_HEADERS OFF)
WRAP_CLASS("itk::ParallelSparseFieldLevelSetNode")
  FOREACH(d ${WRAP_ITK_DIMS})
    WRAP_TEMPLATE("I${d}" "itk::Index< ${d} >")
  ENDFOREACH(d)
END_WRAP_CLASS()
SET(WRAPPER_AUTO_INCLUDE_HEADERS ON)


WRAP_CLASS("itk::SparseFieldLayer" POINTER)
  FOREACH(d ${WRAP_ITK_DIMS})
    WRAP_TEMPLATE("PSFLSNI${d}" "itk::ParallelSparseFieldLevelSetNode< itk::Index< ${d} > >")
  ENDFOREACH(d)
END_WRAP_CLASS()
