#
#  Example on the use of the BinaryErodeImageFilter
#

import itk
from sys import argv

dim = 2
IType = itk.Image[itk.US, dim]
OIType = itk.Image[itk.UC, dim]

reader = itk.ImageFileReader[IType].New( FileName=argv[1] )
kernel = itk.strel(dim, 5)
filter  = itk.BinaryErodeImageFilter[IType, IType, kernel].New( reader,
                ErodeValue=200,
                Kernel=kernel )
cast = itk.CastImageFilter[IType, OIType].New(filter)
writer = itk.ImageFileWriter[OIType].New( cast, FileName=argv[2] )

writer.Update()



