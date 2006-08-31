WRAP_CLASS("itk::BSplineDeformableTransform" POINTER)
  FOREACH(d ${WRAP_ITK_DIMS})
    # only order 3 (the default value) for now, as I'm not sure what may be
    # useful
    FOREACH(order 3)
      WRAP_TEMPLATE("${ITKM_D}${d}${order}" "${ITKT_D},${d},${order}")
    ENDFOREACH(order)
  ENDFOREACH(d)
END_WRAP_CLASS()
