# MAKE_DIRECTORY(Java/Tests)

# put all generated files in this list
SET(targets "")

# configure the tests

UNIQUE(types "${WRAP_ITK_SCALAR};UC")
FOREACH(JAVA_TEST_IMAGE_DIMENSION ${WRAP_ITK_DIMS})
  FOREACH(JAVA_TEST_PIXEL_TYPE ${types})

    SET(TEST_FILE_NAME simplePipeline${JAVA_TEST_PIXEL_TYPE}${JAVA_TEST_IMAGE_DIMENSION})

    CONFIGURE_FILE("${CMAKE_CURRENT_SOURCE_DIR}/simplePipeline.java.in"
                  "${CMAKE_CURRENT_BINARY_DIR}/${TEST_FILE_NAME}.java"
                  @ONLY IMMEDIATE)

    ADD_CUSTOM_COMMAND(
      OUTPUT ${TEST_FILE_NAME}.class
      DEPENDS ${WrapITK_BINARY_DIR}/Java/InsightToolkit.jar ${WrapITK_BINARY_DIR}/Java/Tests/${TEST_FILE_NAME}.java
      COMMAND ${JAVA_COMPILE}
      ARGS -classpath "${WrapITK_BINARY_DIR}/Java/InsightToolkit.jar" -d "${CMAKE_CURRENT_BINARY_DIR}" ${CMAKE_CURRENT_BINARY_DIR}/${TEST_FILE_NAME}.java
    )

    ADD_TEST(JavaSimplePipeline${JAVA_TEST_PIXEL_TYPE}${JAVA_TEST_IMAGE_DIMENSION}
      ${JAVA_RUNTIME}
      -classpath .:${WrapITK_BINARY_DIR}/Java/InsightToolkit.jar
      ${TEST_FILE_NAME}
      ${WrapITK_SOURCE_DIR}/images/cthead1.png
      ${TEST_FILE_NAME}.img
    )
    SET(targets ${targets} ${TEST_FILE_NAME}.class)

  ENDFOREACH(JAVA_TEST_PIXEL_TYPE)
ENDFOREACH(JAVA_TEST_IMAGE_DIMENSION)

# compile the test programs
# FOREACH(test )
#   ADD_CUSTOM_COMMAND(
#     OUTPUT ${test}.class
#     DEPENDS ${WrapITK_BINARY_DIR}/Java/InsightToolkit.jar ${test}.java
#     COMMAND ${JAVA_COMPILE}
#     ARGS -classpath "${WrapITK_BINARY_DIR}/Java/InsightToolkit.jar" -d "${CMAKE_CURRENT_BINARY_DIR}" ${CMAKE_CURRENT_SOURCE_DIR}/${test}.java
#   )
#   ADD_CUSTOM_TARGET(${test} ALL DEPENDS ${test}.class)
# ENDFOREACH(test)


ADD_CUSTOM_TARGET(JavaTests DEPENDS ${targets})
