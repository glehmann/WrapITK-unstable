
SET(PYTHON_TEST_LIB_PATH "${PROJECT_BINARY_DIR}/lib:${WrapITK_DIR}/lib")
SET(PYTHON_TEST_PYTHON_PATH "${WrapITK_DIR}/Python")
SET(PYTHON_TEST_WRAPITK_PYTHON_PATH "${PROJECT_BINARY_DIR}/Python")
FIND_PROGRAM(IMAGE_COMPARE ImageCompare)

CONFIGURE_FILE("${WRAP_ITK_CMAKE_DIR}/Python/Tests/pythonTestDriver.py.in"
              "${CMAKE_CURRENT_BINARY_DIR}/pythonTestDriver.py"
              @ONLY IMMEDIATE)


SET(PYTHON "${PYTHON_EXECUTABLE}" "${CMAKE_CURRENT_BINARY_DIR}/pythonTestDriver.py")

ADD_TEST(SimpleItkVtkPipeline
  ${PYTHON}
  ${CMAKE_CURRENT_SOURCE_DIR}/simpleItkVtkPipeline.py
  ${PROJECT_SOURCE_DIR}/images/cthead1.png
  SimpleItkVtkPipeline.png
  --compare SimpleItkVtkPipeline.png ${PROJECT_SOURCE_DIR}/images/cthead1.png
)

# some tests will fail if dim=2 and unsigned short are not wrapped
INTERSECTION(WRAP_2 2 "${WRAP_ITK_DIMS}")
IF(WRAP_unsigned_short AND WRAP_2)
ENDIF(WRAP_unsigned_short AND WRAP_2)

