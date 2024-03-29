# auto include feature must be disable because the class is not in the file
# with the same name
SET(WRAPPER_AUTO_INCLUDE_HEADERS OFF)
WRAP_INCLUDE("vnl/vnl_unary_function.h")
WRAP_INCLUDE("vnl/vnl_vector.h")

WRAP_CLASS("vnl_unary_function" FORCE_INSTANTIATE)
  WRAP_TEMPLATE("${ITKM_D}_vnl_vector${ITKM_D}" "${ITKT_D}, vnl_vector< ${ITKT_D} >")
END_WRAP_CLASS()