# auto include feature must be disable because the class is not in the file
# with the same name
SET(WRAPPER_AUTO_INCLUDE_HEADERS OFF)
WRAP_INCLUDE("vnl/vnl_file_vector.h")

WRAP_CLASS("vnl_file_vector" DEREF)
  WRAP("_double" "double")
END_WRAP_CLASS()