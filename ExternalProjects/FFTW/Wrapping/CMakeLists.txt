FIND_PACKAGE(WrapITK REQUIRED)

# must include before to find our custom headers before the real ITK ones
INCLUDE_DIRECTORIES(BEFORE ${PROJECT_SOURCE_DIR}/src)

BEGIN_WRAPPER_LIBRARY("${PROJECT_NAME}")
SET(WRAPPER_LIBRARY_DEPENDS Base FFT)

WRAPPER_LIBRARY_CREATE_WRAP_FILES()
WRAPPER_LIBRARY_CREATE_LIBRARY()

# linking is not needed only for python !!
# ... but I can't remember how to do that for all the languages :-/
# TODO: link for all the languages
IF(WRAP_ITK_PYTHON)
  #-lfftw3f -lfftw3f_threads
  TARGET_LINK_LIBRARIES(_${WRAPPER_LIBRARY_NAME}Python ITKCommon fftw3f fftw3f_threads fftw3 fftw3_threads )
  SUBDIRS(Python)
ENDIF(WRAP_ITK_PYTHON)


