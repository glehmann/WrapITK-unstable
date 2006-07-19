
# put all generated files in this list
SET(targets "")

# configure and build the test driver
FIND_PROGRAM(IMAGE_COMPARE ImageCompare)
SET(JAVA_TEST_ITK_JAR "${WrapITK_BINARY_DIR}/Java/${CMAKE_CFG_INTDIR}/InsightToolkit.jar")
CONFIGURE_FILE("${CMAKE_CURRENT_SOURCE_DIR}/javaTestDriver.java.in"
   "${CMAKE_CURRENT_BINARY_DIR}/javaTestDriver.java"
   @ONLY IMMEDIATE
)

ADD_CUSTOM_COMMAND(
  OUTPUT javaTestDriver.class
  DEPENDS ${WrapITK_BINARY_DIR}/Java/Tests/javaTestDriver.java
  COMMAND ${JAVA_COMPILE}
  ARGS -classpath "${CMAKE_CURRENT_SOURCE_DIR}/argparser.jar"
  -d "${CMAKE_CURRENT_BINARY_DIR}" "${CMAKE_CURRENT_BINARY_DIR}/javaTestDriver.java"
)

SET(targets ${targets} javaTestDriver.class)

# a convenient var to use in tests
SET(JAVA_DRIVER "${JAVA_RUNTIME}" -classpath ".:${CMAKE_CURRENT_SOURCE_DIR}/argparser.jar" javaTestDriver)

MACRO(BUILD_JAVA_TEST name)
  # a convenient macro to build java tests
  # 
  ADD_CUSTOM_COMMAND(
    OUTPUT ${name}.class
    DEPENDS ${WrapITK_BINARY_DIR}/Java/${CMAKE_CFG_INTDIR}/InsightToolkit.jar
    COMMAND ${JAVA_COMPILE}
    ARGS -classpath "${WrapITK_BINARY_DIR}/Java/${CMAKE_CFG_INTDIR}/InsightToolkit.jar"
    -d "${CMAKE_CURRENT_BINARY_DIR}" ${CMAKE_CURRENT_SOURCE_DIR}/${name}.java
    )
  SET(targets ${targets} ${name}.class)
	
ENDMACRO(BUILD_JAVA_TEST)




# configure the tests

BUILD_JAVA_TEST("BinaryDilateImageFilter")
ADD_TEST(JavaBinaryDilateImageFilter
  ${JAVA_DRIVER}
  BinaryDilateImageFilter
  ${WrapITK_SOURCE_DIR}/images/2th_cthead1.png
  BinaryDilateImageFilter.png
  --compare BinaryDilateImageFilter.png ${WrapITK_SOURCE_DIR}/images/BinaryDilateImageFilter.png
)

BUILD_JAVA_TEST("BinaryErodeImageFilter")
ADD_TEST(JavaBinaryErodeImageFilter
  ${JAVA_DRIVER}
  BinaryErodeImageFilter
  ${WrapITK_SOURCE_DIR}/images/2th_cthead1.png
  BinaryErodeImageFilter.png
  --compare BinaryErodeImageFilter.png ${WrapITK_SOURCE_DIR}/images/BinaryErodeImageFilter.png
)

BUILD_JAVA_TEST("BinaryThresholdImageFilter")
ADD_TEST(JavaBinaryThresholdImageFilter
  ${JAVA_DRIVER}
  BinaryThresholdImageFilter
  ${WrapITK_SOURCE_DIR}/images/cthead1.png
  BinaryThresholdImageFilter.png
  50 150
  0 65535
  --compare BinaryThresholdImageFilter.png ${WrapITK_SOURCE_DIR}/images/BinaryThresholdImageFilter.png
)

BUILD_JAVA_TEST("CastImageFilter")
ADD_TEST(JavaCastImageFilter
  ${JAVA_DRIVER}
  CastImageFilter
  ${WrapITK_SOURCE_DIR}/images/cthead1.png
  CastImageFilter.png
  --compare CastImageFilter.png ${WrapITK_SOURCE_DIR}/images/CastImageFilter.png
)

BUILD_JAVA_TEST("CurvatureAnisotropicDiffusionImageFilter")
ADD_TEST(JavaCurvatureAnisotropicDiffusionImageFilter
  ${JAVA_DRIVER}
  CurvatureAnisotropicDiffusionImageFilter
  ${WrapITK_SOURCE_DIR}/images/cthead1.png
  CurvatureAnisotropicDiffusionImageFilter.png
  5 0.125 3
  # TODO: run this test
  # --compare CurvatureAnisotropicDiffusionImageFilter.png ${WrapITK_SOURCE_DIR}/images/CurvatureAnisotropicDiffusionImageFilter.png
)

BUILD_JAVA_TEST("CurvatureFlowImageFilter")
ADD_TEST(JavaCurvatureFlowImageFilter
  ${JAVA_DRIVER}
  CurvatureFlowImageFilter
  ${WrapITK_SOURCE_DIR}/images/cthead1.png
  CurvatureFlowImageFilter.png
  5 0.125 1.0
  # TODO: run this test
  # --compare CurvatureFlowImageFilter.png ${WrapITK_SOURCE_DIR}/images/CurvatureFlowImageFilter.png
)

BUILD_JAVA_TEST("GradientAnisotropicDiffusionImageFilter")
ADD_TEST(JavaGradientAnisotropicDiffusionImageFilter
  ${JAVA_DRIVER}
  GradientAnisotropicDiffusionImageFilter
  ${WrapITK_SOURCE_DIR}/images/BrainProtonDensitySlice.png
  GradientAnisotropicDiffusionImageFilter.png
  5 0.125 1.0
  --compare GradientAnisotropicDiffusionImageFilter.png ${WrapITK_SOURCE_DIR}/images/GradientAnisotropicDiffusionImageFilter.png
)

BUILD_JAVA_TEST("MeanImageFilter")
ADD_TEST(JavaMeanImageFilter
  ${JAVA_DRIVER}
  MeanImageFilter
  ${WrapITK_SOURCE_DIR}/images/cthead1.png
  MeanImageFilter.png
  3
  --compare MeanImageFilter.png ${WrapITK_SOURCE_DIR}/images/MeanImageFilter.png
)

BUILD_JAVA_TEST("MedianImageFilter")
ADD_TEST(JavaMedianImageFilter
  ${JAVA_DRIVER}
  MedianImageFilter
  ${WrapITK_SOURCE_DIR}/images/cthead1.png
  MedianImageFilter.png
  3
  --compare MedianImageFilter.png ${WrapITK_SOURCE_DIR}/images/MedianImageFilter.png
)

BUILD_JAVA_TEST("SigmoidImageFilter")
ADD_TEST(JavaSigmoidImageFilter
  ${JAVA_DRIVER}
  SigmoidImageFilter
  ${WrapITK_SOURCE_DIR}/images/cthead1.png
  SigmoidImageFilter.png
  10 240 10 170
  --compare SigmoidImageFilter.png ${WrapITK_SOURCE_DIR}/images/SigmoidImageFilter.png
)

BUILD_JAVA_TEST("ThresholdImageFilter")
ADD_TEST(JavaThresholdImageFilter
  ${JAVA_DRIVER}
  ThresholdImageFilter
  ${WrapITK_SOURCE_DIR}/images/cthead1.png
  ThresholdImageFilter.png
  150 150
  --compare ThresholdImageFilter.png ${WrapITK_SOURCE_DIR}/images/ThresholdImageFilter.png
)




UNIQUE(types "${WRAP_ITK_SCALAR};UC")
FOREACH(JAVA_TEST_IMAGE_DIMENSION ${WRAP_ITK_DIMS})
  FOREACH(JAVA_TEST_PIXEL_TYPE ${types})

    SET(TEST_FILE_NAME simplePipeline${JAVA_TEST_PIXEL_TYPE}${JAVA_TEST_IMAGE_DIMENSION})

    CONFIGURE_FILE("${CMAKE_CURRENT_SOURCE_DIR}/simplePipeline.java.in"
                  "${CMAKE_CURRENT_BINARY_DIR}/${TEST_FILE_NAME}.java"
                  @ONLY IMMEDIATE)

    ADD_CUSTOM_COMMAND(
      OUTPUT ${TEST_FILE_NAME}.class
      DEPENDS ${WrapITK_BINARY_DIR}/Java/${CMAKE_CFG_INTDIR}/InsightToolkit.jar ${WrapITK_BINARY_DIR}/Java/Tests/${TEST_FILE_NAME}.java
      COMMAND ${JAVA_COMPILE}
      ARGS -classpath "${WrapITK_BINARY_DIR}/Java/${CMAKE_CFG_INTDIR}/InsightToolkit.jar" -d "${CMAKE_CURRENT_BINARY_DIR}" ${CMAKE_CURRENT_BINARY_DIR}/${TEST_FILE_NAME}.java
    )

    ADD_TEST(JavaSimplePipeline${JAVA_TEST_PIXEL_TYPE}${JAVA_TEST_IMAGE_DIMENSION}
      ${JAVA_DRIVER}
      ${TEST_FILE_NAME}
      ${WrapITK_SOURCE_DIR}/images/cthead1.png
      ${TEST_FILE_NAME}.img
      --compare ${TEST_FILE_NAME}.img ${WrapITK_SOURCE_DIR}/images/cthead1.png
    )
    
    SET(targets ${targets} ${TEST_FILE_NAME}.class)

  ENDFOREACH(JAVA_TEST_PIXEL_TYPE)
ENDFOREACH(JAVA_TEST_IMAGE_DIMENSION)




ADD_CUSTOM_TARGET(JavaTests ALL DEPENDS ${targets})
