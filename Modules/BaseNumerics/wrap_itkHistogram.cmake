WRAP_CLASS("itk::Statistics::Histogram" POINTER)
  WRAP_TEMPLATE("${ITKM_F}1DFC" "${ITKT_F}, 1, itk::Statistics::DenseFrequencyContainer")
  WRAP_TEMPLATE("${ITKM_D}1DFC" "${ITKT_D}, 1, itk::Statistics::DenseFrequencyContainer")
END_WRAP_CLASS()
