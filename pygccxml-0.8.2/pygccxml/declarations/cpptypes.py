# Copyright 2004 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

"""
defines classes, that describe C++ types
"""

import algorithms_cache

class type_t(object):
    """base class for all types"""
    def __init__(self):
        object.__init__( self )
        self.cache = algorithms_cache.type_algs_cache_t()

    def __str__(self):
        res = self.decl_string
        if res[:2]=="::":
            res = res[2:]
        return res

    def __eq__(self, other):
        if not isinstance( other, type_t ):
            return False
        return self.decl_string == other.decl_string

    def __ne__( self, other):
        return not self.__eq__( other )

    def __lt__(self, other):
        if not isinstance( other, self.__class__ ):
            return self.__class__.__name__ < other.__class__.__name__
        return self.decl_string < other.decl_string

    def _create_decl_string(self):
        raise NotImplementedError()

    def _get_decl_string( self ):
        return self._create_decl_string()
    decl_string = property( _get_decl_string )

    def _clone_impl( self ):
        raise NotImplementedError()

    def clone( self ):
        "returns new instance of the type"
        answer = self._clone_impl()
        return answer

#There are cases when GCC-XML reports something like this
#<Unimplemented id="_9482" tree_code="188" tree_code_name="template_type_parm" node="0xcc4d5b0"/>
#In this case I will use this as type


class dummy_type_t( type_t ):
    """provides L{type_t} interface for a string, that defines C++ type.

    This class could be very useful in the code generator.
    """
    def __init__( self, decl_string ):
        type_t.__init__( self )
        self._decl_string = decl_string

    def _create_decl_string(self):
        return self._decl_string

    def _clone_impl( self ):
        return dummy_type_t( self._decl_string )

class unknown_t( type_t ):
    "type, that represents all C++ types, that could not be parsed  by GCC-XML"
    def __init__( self ):
        type_t.__init__( self )

    def _create_decl_string(self):
        return '?unknown?'

    def _clone_impl( self ):
        return self

################################################################################
## Fundamental types:

class fundamental_t( type_t ):
    """base class for all fundamental, build-in types"""
    def __init__( self, name ):
        type_t.__init__( self )
        self._name = name

    def _create_decl_string(self):
        return self._name

    def _clone_impl( self ):
        return self

class java_fundamental_t( fundamental_t ):
    """base class for all JNI defined fundamental types"""
    def __init__( self, name ):
        fundamental_t.__init__( self, name )

class void_t( fundamental_t ):
    """represents void type"""
    CPPNAME = 'void'
    def __init__( self ):
        fundamental_t.__init__( self,void_t.CPPNAME )

class char_t( fundamental_t ):
    """represents char type"""
    CPPNAME = 'char'
    def __init__( self ):
        fundamental_t.__init__( self, char_t.CPPNAME )

class signed_char_t( fundamental_t ):
    """represents signed char type"""
    CPPNAME = 'signed char'
    def __init__( self ):
        fundamental_t.__init__( self, signed_char_t.CPPNAME )

class unsigned_char_t( fundamental_t ):
    """represents unsigned char type"""
    CPPNAME = 'unsigned char'
    def __init__( self ):
        fundamental_t.__init__( self, unsigned_char_t.CPPNAME )

class wchar_t( fundamental_t ):
    """represents wchar_t type"""
    CPPNAME = 'wchar_t'
    def __init__( self ):
        fundamental_t.__init__( self, wchar_t.CPPNAME )

class short_int_t( fundamental_t ):
    """represents short int type"""
    CPPNAME = 'short int'
    def __init__( self ):
        fundamental_t.__init__( self, short_int_t.CPPNAME )

class short_unsigned_int_t( fundamental_t ):
    """represents short unsigned int type"""
    CPPNAME = 'short unsigned int'
    def __init__( self ):
        fundamental_t.__init__( self, short_unsigned_int_t.CPPNAME )

class bool_t( fundamental_t ):
    """represents bool type"""
    CPPNAME = 'bool'
    def __init__( self ):
        fundamental_t.__init__( self, bool_t.CPPNAME )

class int_t( fundamental_t ):
    """represents int type"""
    CPPNAME = 'int'
    def __init__( self ):
        fundamental_t.__init__( self, int_t.CPPNAME )

class unsigned_int_t( fundamental_t ):
    """represents unsigned int type"""
    CPPNAME = 'unsigned int'
    def __init__( self ):
        fundamental_t.__init__( self, unsigned_int_t.CPPNAME )

class long_int_t( fundamental_t ):
    """represents long int type"""
    CPPNAME = 'long int'
    def __init__( self ):
        fundamental_t.__init__( self, long_int_t.CPPNAME )

class long_unsigned_int_t( fundamental_t ):
    """represents long unsigned int type"""
    CPPNAME = 'long unsigned int'
    def __init__( self ):
        fundamental_t.__init__( self, long_unsigned_int_t.CPPNAME )

class long_long_int_t( fundamental_t ):
    """represents long long int type"""
    CPPNAME = 'long long int'
    def __init__( self ):
        fundamental_t.__init__( self, long_long_int_t.CPPNAME )

class long_long_unsigned_int_t( fundamental_t ):
    """represents long long unsigned int type"""
    CPPNAME = 'long long unsigned int'
    def __init__( self ):
        fundamental_t.__init__( self, long_long_unsigned_int_t.CPPNAME )

class float_t( fundamental_t ):
    """represents float type"""
    CPPNAME = 'float'
    def __init__( self ):
        fundamental_t.__init__( self, float_t.CPPNAME )

class double_t( fundamental_t ):
    """represents double type"""
    CPPNAME = 'double'
    def __init__( self ):
        fundamental_t.__init__( self, double_t.CPPNAME )

class long_double_t( fundamental_t ):
    """represents long double type"""
    CPPNAME = 'long double'
    def __init__( self ):
        fundamental_t.__init__( self, long_double_t.CPPNAME )

class complex_double_t( fundamental_t ):
    """represents complex double type"""
    CPPNAME = 'complex double'
    def __init__( self ):
        fundamental_t.__init__( self, complex_double_t.CPPNAME )

class complex_long_double_t( fundamental_t ):
    """represents complex long double type"""
    CPPNAME = 'complex long double'
    def __init__( self ):
        fundamental_t.__init__( self, complex_long_double_t.CPPNAME )

class complex_float_t( fundamental_t ):
    """represents complex float type"""
    CPPNAME = 'complex float'
    def __init__( self ):
        fundamental_t.__init__( self, complex_float_t.CPPNAME )

class jbyte_t( java_fundamental_t ):
    """represents jbyte type"""
    JNAME = 'jbyte'
    def __init__( self ):
        java_fundamental_t.__init__( self, jbyte_t.JNAME )

class jshort_t( java_fundamental_t ):
    """represents jshort type"""
    JNAME = 'jshort'
    def __init__( self ):
        java_fundamental_t.__init__( self, jshort_t.JNAME )

class jint_t( java_fundamental_t ):
    """represents jint type"""
    JNAME = 'jint'
    def __init__( self ):
        java_fundamental_t.__init__( self, jint_t.JNAME )

class jlong_t( java_fundamental_t ):
    """represents jlong type"""
    JNAME = 'jlong'
    def __init__( self ):
        java_fundamental_t.__init__( self, jlong_t.JNAME )

class jfloat_t( java_fundamental_t ):
    """represents jfloat type"""
    JNAME = 'jfloat'
    def __init__( self ):
        java_fundamental_t.__init__( self, jfloat_t.JNAME )

class jdouble_t( java_fundamental_t ):
    """represents jdouble type"""
    JNAME = 'jdouble'
    def __init__( self ):
        java_fundamental_t.__init__( self, jdouble_t.JNAME )

class jchar_t( java_fundamental_t ):
    """represents jchar type"""
    JNAME = 'jchar'
    def __init__( self ):
        java_fundamental_t.__init__( self, jchar_t.JNAME )

class jboolean_t( java_fundamental_t ):
    """represents jboolean type"""
    JNAME = 'jboolean'
    def __init__( self ):
        java_fundamental_t.__init__( self, jboolean_t.JNAME )

FUNDAMENTAL_TYPES = {
    void_t.CPPNAME : void_t()
    , char_t.CPPNAME : char_t()
    , signed_char_t.CPPNAME : signed_char_t()
    , unsigned_char_t.CPPNAME : unsigned_char_t()
    , wchar_t.CPPNAME : wchar_t()
    , short_int_t.CPPNAME : short_int_t()
    , 'signed ' + short_int_t.CPPNAME : short_int_t()
    , short_unsigned_int_t.CPPNAME : short_unsigned_int_t()
    , bool_t.CPPNAME : bool_t()
    , int_t.CPPNAME : int_t()
    , 'signed ' + int_t.CPPNAME : int_t()
    , unsigned_int_t.CPPNAME : unsigned_int_t()
    , long_int_t.CPPNAME : long_int_t()
    , long_unsigned_int_t.CPPNAME : long_unsigned_int_t()
    , long_long_int_t.CPPNAME : long_long_int_t()
    , long_long_unsigned_int_t.CPPNAME : long_long_unsigned_int_t()
    , float_t.CPPNAME : float_t()
    , double_t.CPPNAME : double_t()
    , long_double_t.CPPNAME : long_double_t()
    , complex_long_double_t.CPPNAME : complex_long_double_t()
    , complex_double_t.CPPNAME : complex_double_t()
    , complex_float_t.CPPNAME : complex_float_t()
    ##adding java types
    , jbyte_t.JNAME : jbyte_t()
    , jshort_t.JNAME : jshort_t()
    , jint_t.JNAME : jint_t()
    , jlong_t.JNAME : jlong_t()
    , jfloat_t.JNAME : jfloat_t()
    , jdouble_t.JNAME : jdouble_t()
    , jchar_t.JNAME : jchar_t()
    , jboolean_t.JNAME : jboolean_t()
    , '__java_byte' : jbyte_t()
    , '__java_short' : jshort_t()
    , '__java_int' : jint_t()
    , '__java_long' : jlong_t()
    , '__java_float' : jfloat_t()
    , '__java_double' : jdouble_t()
    , '__java_char' : jchar_t()
    , '__java_boolean' : jboolean_t()
}
"""
defines a mapping between fundamental type name and its synonym to the instance
of class that describes the type
"""

################################################################################
## Compaund types:

class compound_t( type_t ):
    """class that allows to represent compound types like C{const int*}"""
    def __init__( self, base ):
        type_t.__init__( self )
        self._base = base

    def _get_base(self):
        return self._base
    def _set_base(self, new_base):
        self._base = new_base

    base = property( _get_base, _set_base
                     , doc="reference to internal/base class")

class volatile_t( compound_t ):
    """represents C{volatile whatever} type"""
    def __init__( self, base ):
        compound_t.__init__( self, base)

    def _create_decl_string(self):
        return 'volatile ' + self.base.decl_string

    def _clone_impl( self ):
        return volatile_t( self.base.clone() )

class const_t( compound_t ):
    """represents C{whatever const} type"""
    def __init__( self, base ):
        compound_t.__init__( self, base )

    def _create_decl_string(self):
        return self.base.decl_string + ' const'

    def _clone_impl( self ):
        return const_t( self.base.clone() )

class pointer_t( compound_t ):
    """represents C{whatever*} type"""
    def __init__( self, base ):
        compound_t.__init__( self, base )

    def _create_decl_string(self):
        return self.base.decl_string + ' *'

    def _clone_impl( self ):
        return pointer_t( self.base.clone() )

class reference_t( compound_t ):
    """represents C{whatever&} type"""
    def __init__( self, base ):
        compound_t.__init__( self, base)

    def _create_decl_string(self):
        return self.base.decl_string + ' &'

    def _clone_impl( self ):
        return reference_t( self.base.clone() )

class array_t( compound_t ):
    """represents C++ array type"""
    SIZE_UNKNOWN = -1
    def __init__( self, base, size ):
        compound_t.__init__( self, base )
        self._size = size

    def _get_size(self):
        return self._size
    def _set_size(self, size):#sometimes there is a need to update the size of the array
        self._size = size
    size = property( _get_size, _set_size,
                     doc="returns array size" )

    def _create_decl_string(self):
        return self.base.decl_string + '[%d]' %  self.size

    def _clone_impl( self ):
        return array_t( self.base.clone(), self.size )

class calldef_type_t( object ):
    """base class for all types that describes "callable" declaration"""
    def __init__( self, return_type=None, arguments_types=None ):
        object.__init__( self )
        self._return_type = return_type
        if arguments_types is None:
            arguments_types = []
        self._arguments_types = arguments_types

    def _get_return_type(self):
        return self._return_type
    def _set_return_type(self, new_return_type):
        self._return_type = new_return_type
    return_type = property( _get_return_type, _set_return_type
                            , doc="reference to L{return type<type_t>}")

    def _get_arguments_types(self):
        return self._arguments_types
    def _set_arguments_types(self, new_arguments_types):
        self._arguments_types = new_arguments_types
    arguments_types = property( _get_arguments_types, _set_arguments_types
                                , doc="list of argument L{types<type_t>}")

class free_function_type_t( type_t, calldef_type_t ):
    """describes free function type"""
    NAME_TEMPLATE = '%(return_type)s (*)( %(arguments)s )'
    TYPEDEF_NAME_TEMPLATE = '%(return_type)s ( *%(typedef_name)s )( %(arguments)s )'
    def __init__( self, return_type=None, arguments_types=None ):
        type_t.__init__(self)
        calldef_type_t.__init__( self, return_type, arguments_types )

    @staticmethod
    def create_decl_string( return_type, arguments_types ):
        """
        returns free function type

        @param return_type: function return type
        @type return_type: L{type_t}

        @param arguments_types: list of argument L{type<type_t>}

        @return: L{free_function_type_t}
        """
        return free_function_type_t.NAME_TEMPLATE % {
                  'return_type' : return_type.decl_string
                , 'arguments' : ','.join( map( lambda x: x.decl_string, arguments_types ) ) }

    def _create_decl_string(self):
        return self.create_decl_string( self.return_type, self.arguments_types )

    def _clone_impl( self ):
        rt_clone = None
        if self.return_type:
            rt_clone = self.return_type.clone()
        return free_function_type_t( rt_clone
                                     , [ arg.clone() for arg in self.arguments_types ] )

    #TODO: create real typedef
    def create_typedef( self, typedef_name, unused=None):
        """returns string, that contains valid C++ code, that defines typedef to function type

        @param name: the desired name of typedef
        """
        #unused argument simplifies user code
        return free_function_type_t.TYPEDEF_NAME_TEMPLATE % {
            'typedef_name' : typedef_name
            , 'return_type' : self.return_type.decl_string
            , 'arguments' : ','.join( map( lambda x: x.decl_string, self.arguments_types ) ) }

class member_function_type_t( type_t, calldef_type_t ):
    """describes member function type"""
    NAME_TEMPLATE = '%(return_type)s ( %(class)s::* )( %(arguments)s ) %(has_const)s'
    TYPEDEF_NAME_TEMPLATE = '%(return_type)s ( %(class)s::*%(typedef_name)s )( %(arguments)s ) %(has_const)s'

    def __init__( self, class_inst=None, return_type=None, arguments_types=None, has_const=False):
        type_t.__init__(self)
        calldef_type_t.__init__( self, return_type, arguments_types )
        self._has_const = has_const
        self._class_inst = class_inst

    def _get_has_const(self):
        return self._has_const
    def _set_has_const(self, has_const ):
        self._has_const = has_const
    has_const = property( _get_has_const, _set_has_const
                          , doc="describes, whether function has const modifier")

    def _get_class_inst(self):
        return self._class_inst
    def _set_class_inst(self, class_inst ):
        self._class_inst = class_inst
    class_inst = property( _get_class_inst, _set_class_inst
                           ,doc="reference to parent L{class<declaration_t>}" )

    #TODO: create real typedef
    def create_typedef( self, typedef_name, class_alias=None):
        """creates typedef to the function type

        @param typedef_name: desired type name
        @return: string
        """
        has_const_str = ''
        if self.has_const:
            has_const_str = 'const'
        if None is class_alias:
            class_alias = self.class_inst.decl_string
        return member_function_type_t.TYPEDEF_NAME_TEMPLATE % {
            'typedef_name' : typedef_name
            , 'return_type' : self.return_type.decl_string
            , 'class' : class_alias
            , 'arguments' : ','.join( map( lambda x: x.decl_string, self.arguments_types ) )
            , 'has_const' : has_const_str }

    def create(self):
        return self.create_decl_string( self.return_type
                                        , self.class_inst.decl_string
                                        , self.arguments_types
                                        , self.has_const )


    @staticmethod
    def create_decl_string(return_type, class_decl_string, arguments_types, has_const):
        has_const_str = ''
        if has_const:
            has_const_str = 'const'
        return_type_decl_string = ''
        if return_type:
            return_type_decl_string = return_type.decl_string
        return member_function_type_t.NAME_TEMPLATE % {
              'return_type' : return_type_decl_string
            , 'class' : class_decl_string
            , 'arguments' : ','.join( map( lambda x: x.decl_string, arguments_types ) )
            , 'has_const' : has_const_str }

    def _create_decl_string(self):
        return self.create_decl_string( self.return_type
                                        , self.class_inst.decl_string
                                        , self.arguments_types
                                        , self.has_const )

    def _clone_impl( self ):
        rt_clone = None
        if self.return_type:
            rt_clone = self.return_type.clone()

        return member_function_type_t( self.class_inst
                                       , rt_clone
                                       , [ arg.clone() for arg in self.arguments_types ]
                                       , self.has_const )


class member_variable_type_t( compound_t ):
    """describes member variable type"""
    NAME_TEMPLATE = '%(type)s ( %(class)s::* )'
    def __init__( self, class_inst=None, variable_type=None ):
        compound_t.__init__(self, class_inst)
        self._mv_type = variable_type

    def _get_variable_type(self):
        return self._mv_type
    def _set_variable_type(self, new_type):
        self._mv_type = new_type
    variable_type = property( _get_variable_type, _set_variable_type
                              , doc="describes member variable L{type<type_t>}")

    def _create_decl_string(self):
        return self.NAME_TEMPLATE % { 'type' : self.variable_type.decl_string, 'class' : self.base.decl_string }

    def _clone_impl( self ):
        return member_variable_type_t( class_inst=self.base
                                       , variable_type=self.variable_type.clone() )


################################################################################
## declarated types:

class declarated_t( type_t ):
    """class that binds between to hierarchies: L{type_t} and L{declaration_t}"""
    def __init__( self, declaration ):
        type_t.__init__( self )
        self._declaration = declaration

    def _get_declaration(self):
        return self._declaration
    def _set_declaration(self, new_declaration):
        self._declaration = new_declaration
    declaration = property( _get_declaration, _set_declaration
                            , doc="reference to L{declaration<declaration_t>}")

    def _create_decl_string(self):
        return self._declaration.decl_string

    def _clone_impl( self ):
        return declarated_t( self._declaration )

class type_qualifiers_t( object ):
    """contains additional information about type: mutable, static, extern"""
    def __init__(self, has_static=False, has_mutable=False ):
        self._has_static = has_static
        self._has_mutable = has_mutable

    def __eq__(self, other):
        if not isinstance( other, type_qualifiers_t ):
            return False
        return self.has_static == other.has_static \
               and self.has_mutable == other.has_mutable

    def __ne__( self, other):
        return not self.__eq__( other )

    def __lt__(self, other):
        if not isinstance( other, type_qualifiers_t ):
            return object.__lt__( self, other )
        return self.has_static < other.has_static \
               and self.has_mutable < other.has_mutable

    def _get_has_static(self):
        return self._has_static
    def _set_has_static(self, has_static ):
        self._has_static = has_static
    has_static = property( _get_has_static, _set_has_static )
    has_extern = has_static #synonim to static

    def _get_has_mutable(self):
        return self._has_mutable
    def _set_has_mutable(self, has_mutable ):
        self._has_mutable = has_mutable
    has_mutable = property( _get_has_mutable, _set_has_mutable )
