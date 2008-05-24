%include "typemaps.i"
%include "stl.i"

/*
// By default swig-java creates protected constructors, when breaking the wrapping into
// packages, we need public, ie visible, constructors.
//%typemap(javabody) SWIGTYPE, SWIGTYPE *, SWIGTYPE &, SWIGTYPE [], SWIGTYPE (CLASS::*)
%typemap(javabody) SWIGTYPE
%{
  private long swigCPtr;
  private boolean swigCMemOwn;

  public $javaclassname(long cPtr, boolean cMemoryOwn) {
    swigCPtr = cPtr;
    swigCMemOwn = cMemoryOwn;
  }

  public static long getCPtr($javaclassname obj) {
    return (obj == null) ? 0 : obj.swigCPtr;
  }
%}
// And the ame goes for the derived classes
//%typemap(javabody_derived) SWIGTYPE, SWIGTYPE *, SWIGTYPE &, SWIGTYPE [], SWIGTYPE (CLASS::*)
%typemap(javabody_derived) SWIGTYPE
%{
  private long swigCPtr;
  private boolean swigCMemOwn;

  public $javaclassname(long cPtr, boolean cMemoryOwn) {
	  super(cPtr, cMemoryOwn);
  }
%}
*/
// more compact alternative
SWIG_JAVABODY_METHODS(public, public, SWIGTYPE)


%ignore New();
%ignore Delete();

/*
%extend itkLightObject {
  public itkLightObject() {
  }
}
*/

%feature("notabstract") itkLightObject;