WRAP_CLASS("itk::ImageSeriesWriter" POINTER)
  # Force uchar image IO 
  UNIQUE(image_types "UC;${WRAP_ITK_SCALAR};${WRAP_ITK_RGB}")
  FOREACH(d1 ${WRAP_ITK_DIMS})
    FOREACH(d2 ${WRAP_ITK_DIMS})
      IF("${d1}" GREATER "${d2}")
        FOREACH(t ${image_types})
#          WRAP_TEMPLATE("${ITKM_I${t}${d1}}${ITKM_I${t}${d2}}"
#                        "${ITKT_I${t}${d1}},${ITKT_I${t}${d2}}")        
        ENDFOREACH(t)
      ENDIF("${d1}" GREATER "${d2}")
    ENDFOREACH(d2)
  ENDFOREACH(d1)
END_WRAP_CLASS()
