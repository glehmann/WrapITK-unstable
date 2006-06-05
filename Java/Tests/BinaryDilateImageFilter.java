/**
 *  Example on the use of the BinaryDilateImageFilter
 *
 */

import InsightToolkit.*;

public class BinaryDilateImageFilter
{
  public static void main( String argv[] )
  {
    System.out.println("BinaryDilateImageFilter Example");

    itkImageFileReaderIUS2_Pointer reader = itkImageFileReaderIUS2.itkImageFileReaderIUS2_New();
    itkImageFileWriterIUC2_Pointer writer = itkImageFileWriterIUC2.itkImageFileWriterIUC2_New();
    itkCastImageFilterIUS2IUC2_Pointer caster = itkCastImageFilterIUS2IUC2.itkCastImageFilterIUS2IUC2_New();

    itkBinaryDilateImageFilterIUS2IUS2_Pointer filter = itkBinaryDilateImageFilterIUS2IUS2.itkBinaryDilateImageFilterIUS2IUS2_New();

    filter.SetInput( reader.GetOutput() );
    caster.SetInput( filter.GetOutput() );
    writer.SetInput( caster.GetOutput() );

    reader.SetFileName( argv[0] );
    writer.SetFileName( argv[1] );


    itkBinaryBallStructuringElementB2 element = new itkBinaryBallStructuringElementB2();

    element.SetRadius( 5 );
    element.CreateStructuringElement();

    filter.SetKernel( element );

    short value = 200;

    filter.SetDilateValue( value );

    writer.Update();
  }

}


