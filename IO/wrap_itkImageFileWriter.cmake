WRAP_CLASS("itk::ImageFileWriter" POINTER)
  # Force uchar image IO 
  UNIQUE(image_types "UC;${WRAP_ITK_ALL_TYPES}")
  WRAP_IMAGE_FILTER("${image_types}" 1)
END_WRAP_CLASS()
