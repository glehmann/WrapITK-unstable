WRAP_LIBRARY(IntensityFilters)

SET(WRAPPER_LIBRARY_DEPENDS Base Numerics)

SET(WRAPPER_LIBRARY_LINK_LIBRARIES ITKCommon ITKStatistics)

WRAPPER_LIBRARY_CREATE_WRAP_FILES()
END_WRAP_LIBRARY()

