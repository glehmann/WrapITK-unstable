# swig generate bad code for python with that filter for an unknown
# it seems that it is a bad interaction with FixedArray typemap
# we can't enable it for now

# WRAP_CLASS("itk::BilateralImageFilter" POINTER)
#   WRAP_IMAGE_FILTER_USIGN_INT(2)
#   WRAP_IMAGE_FILTER_SIGN_INT(2)
#   WRAP_IMAGE_FILTER_REAL(2)
# END_WRAP_CLASS()
