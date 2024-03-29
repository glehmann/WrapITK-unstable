# auto include feature must be disable because the class is not in the file
# with the same name
SET(WRAPPER_AUTO_INCLUDE_HEADERS OFF)
WRAP_INCLUDE("vnl/vnl_matrix_fixed.h")

WRAP_CLASS("vnl_matrix_fixed")
  WRAP_TEMPLATE("${ITKM_D}_2_2" "${ITKT_D},2,2")
  WRAP_TEMPLATE("${ITKM_D}_2_3" "${ITKT_D},2,3")
  WRAP_TEMPLATE("${ITKM_D}_2_6" "${ITKT_D},2,6")
  WRAP_TEMPLATE("${ITKM_D}_3_12" "${ITKT_D},3,12")
  WRAP_TEMPLATE("${ITKM_D}_3_3" "${ITKT_D},3,3")
  WRAP_TEMPLATE("${ITKM_D}_3_4" "${ITKT_D},3,4")
  WRAP_TEMPLATE("${ITKM_D}_4_3" "${ITKT_D},4,3")
  WRAP_TEMPLATE("${ITKM_D}_4_4" "${ITKT_D},4,4")
  WRAP_TEMPLATE("${ITKM_F}_3_3" "${ITKT_F},3,3")
END_WRAP_CLASS()
