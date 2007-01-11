SET(WRAP_ITK_MODULES
  VXLNumerics
  Base
)
  
# set Iterators module to OFF by default
# it is currently usable only when applying patches to ITK, and will only
# take place and time to build
# TODO: remove this line when iterators will be usable without patch
OPTION(WRAP_Iterators "Build Iterators module." OFF)
  
# Set FFTW to on if USE_FFTWF or USE_FFTWD are on.
IF(USE_FFTWD OR USE_FFTWF)
  OPTION(WRAP_FFTW "Build FFTW module." ON)
ELSE(USE_FFTWD OR USE_FFTWF)
  OPTION(WRAP_FFTW "Build FFTW module." OFF)
ENDIF(USE_FFTWD OR USE_FFTWF)


SET(optional_modules 
  Numerics
  Transforms
  SpatialObject
  BinaryMorphology
  Calculators
  Compose
  Interpolators  # is required by DeformableTransforms
  DeformableTransforms
  Denoising
  DistanceMap
  EdgesAndContours
  FFT
  FFTW
  Filtering
  IntensityFilters
  IO
  Iterators
  LevelSet
  Morphology
  #Patented
  PixelMath
  Resize  # required by Registration
  Registration
  Review
  SegmentationAndThreshold
  SegmentationValidation
  SimpleFilters
  UnaryPixelMath
)

FOREACH(module ${optional_modules})
  OPTION(WRAP_${module} "Build ${module} module." ON)
  MARK_AS_ADVANCED(WRAP_${module})
  IF(WRAP_${module})
    SET(WRAP_ITK_MODULES ${WRAP_ITK_MODULES} ${module})
  ENDIF(WRAP_${module})
ENDFOREACH(module)

FOREACH(module ${WRAP_ITK_MODULES} ${WRAP_ITK_EXTRA_MODULES})
  ADD_SUBDIRECTORY(${module})
ENDFOREACH(module)
