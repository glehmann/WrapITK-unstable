# Copyright 2004 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

"""
defines few algorithms, that deals with different properties of C++ types

Do you aware of boost::type_traits library? pygccxml has functionality similar to
it. Using functions defined in this module you can
    - find out some properties of the type
    - modify type

Those functions are very valuable for code generation. Almost all functions
within this module works on L{type_t} class hierarchy and\\or L{class_t}.
"""

import types
import matchers
import typedef
import calldef
import cpptypes
import variable
import algorithm
import namespace
import templates
import enumeration
import class_declaration
import types as build_in_types

def __remove_alias(type_):
    """implementation details"""
    if isinstance( type_, typedef.typedef_t ):
        return __remove_alias( type_.type )
    if isinstance( type_, cpptypes.declarated_t ) and isinstance( type_.declaration, typedef.typedef_t ):
        return __remove_alias( type_.declaration.type )
    if isinstance( type_, cpptypes.compound_t ):
        type_.base = __remove_alias( type_.base )
        return type_
    return type_

def remove_alias(type_):
    """returns type without typedefs"""
    type_ref = None
    if isinstance( type_, cpptypes.type_t ):
        type_ref = type_
    elif isinstance( type_, typedef.typedef_t ):
        type_ref = type_.type
    else:
        pass #not a valid input, just return it
    if not type_ref:
        return type_
    if type_ref.cache.remove_alias:
        return type_ref.cache.remove_alias
    no_alias = __remove_alias( type_ref.clone() )
    type_ref.cache.remove_alias = no_alias
    return no_alias

def create_cv_types( base ):
    """implementation details"""
    return [ base
             , cpptypes.const_t( base )
             , cpptypes.volatile_t( base )
             , cpptypes.volatile_t( cpptypes.const_t( base ) ) ]

def decompose_type(tp):
    """implementation details"""
    #implementation of this function is important
    if isinstance( tp, cpptypes.compound_t ):
        return [tp] + decompose_type( tp.base )
    elif isinstance( tp, typedef.typedef_t ):
        return decompose_type( tp.type )
    elif isinstance( tp, cpptypes.declarated_t ) and isinstance( tp.declaration, typedef.typedef_t ):
        return decompose_type( tp.declaration.type )
    else:
        return [tp]

def decompose_class(type):
    """implementation details"""
    types = decompose_type( type )
    return [ tp.__class__ for tp in types ]

def base_type(type):
    """returns base type.

    For C{const int} will return C{int}
    """
    types = decompose_type( type )
    return types[-1]

def does_match_definition(given, main, secondary ):
    """implementation details"""
    assert isinstance( secondary, build_in_types.TupleType )
    assert 2 == len( secondary ) #general solution could be provided
    types = decompose_type( given )
    if isinstance( types[0], main ):
        return True
    elif 2 <= len( types ) and \
       ( ( isinstance( types[0], main ) and isinstance( types[1], secondary ) ) \
         or ( isinstance( types[1], main ) and isinstance( types[0], secondary ) ) ):
        return True
    elif 3 <= len( types ):
        classes = set( [tp.__class__ for tp in types[:3]] )
        desired = set( [main] + list( secondary ) )
        return classes == desired
    else:
        return False

def is_void( type ):
    """returns True, if type represents C{void}, False otherwise"""
    return remove_alias( type ) in create_cv_types( cpptypes.void_t() )

def is_void_pointer( type ):
    """returns True, if type represents C{void*}, False otherwise"""
    return is_same( type, cpptypes.pointer_t( cpptypes.void_t() ) )

def is_integral( type ):
    """returns True, if type represents C++ integral type, False otherwise"""
    integral_def = create_cv_types( cpptypes.char_t() )                    \
                   + create_cv_types( cpptypes.unsigned_char_t() )         \
                   + create_cv_types( cpptypes.signed_char_t() )         \
                   + create_cv_types( cpptypes.wchar_t() )                 \
                   + create_cv_types( cpptypes.short_int_t() )             \
                   + create_cv_types( cpptypes.short_unsigned_int_t() )    \
                   + create_cv_types( cpptypes.bool_t() )                  \
                   + create_cv_types( cpptypes.int_t() )                   \
                   + create_cv_types( cpptypes.unsigned_int_t() )          \
                   + create_cv_types( cpptypes.long_int_t() )              \
                   + create_cv_types( cpptypes.long_unsigned_int_t() )     \
                   + create_cv_types( cpptypes.long_long_int_t() )         \
                   + create_cv_types( cpptypes.long_long_unsigned_int_t() )

    return remove_alias( type ) in integral_def

def is_floating_point( type ):
    """returns True, if type represents C++ floating point type, False otherwise"""
    float_def = create_cv_types( cpptypes.float_t() )                   \
                + create_cv_types( cpptypes.double_t() )                \
                + create_cv_types( cpptypes.long_double_t() )

    return remove_alias( type ) in float_def

def is_arithmetic( type ):
    """returns True, if type represents C++ integral or floating point type, False otherwise"""
    return is_integral( type ) or is_floating_point( type )

def is_pointer(type):
    """returns True, if type represents C++ pointer type, False otherwise"""
    return does_match_definition( type
                                  , cpptypes.pointer_t
                                  , (cpptypes.const_t, cpptypes.volatile_t) )

def remove_pointer(type):
    """removes pointer from the type definition

    If type is not pointer type, it will be returned as is.
    """
    nake_type = remove_alias( type )
    if not is_pointer( nake_type ):
        return type
    elif isinstance( nake_type, cpptypes.volatile_t ) and isinstance( nake_type.base, cpptypes.pointer_t ):
        return cpptypes.volatile_t( nake_type.base.base )
    elif isinstance( nake_type, cpptypes.const_t ) and isinstance( nake_type.base, cpptypes.pointer_t ):
        return cpptypes.const_t( nake_type.base.base )
    elif isinstance( nake_type.base, cpptypes.calldef_type_t ):
        return type
    else:
        return nake_type.base

def is_reference(type):
    """returns True, if type represents C++ reference type, False otherwise"""
    nake_type = remove_alias( type )
    return isinstance( nake_type, cpptypes.reference_t )

def is_array(type):
    """returns True, if type represents C++ array type, False otherwise"""
    nake_type = remove_alias( type )
    nake_type = remove_reference( nake_type )
    nake_type = remove_cv( nake_type )
    return isinstance( nake_type, cpptypes.array_t )

def array_size(type):
    """returns array size"""
    nake_type = remove_alias( type )
    nake_type = remove_reference( nake_type )
    nake_type = remove_cv( nake_type )
    assert isinstance( nake_type, cpptypes.array_t )
    return nake_type.size

def array_item_type(type):
    """returns array item type"""
    assert is_array(type)
    nake_type = remove_alias( type )
    nake_type = remove_reference( nake_type )
    nake_type = remove_cv( nake_type )
    return nake_type.base

def remove_reference(type):
    """removes reference from the type definition

    If type is not reference type, it will be returned as is.
    """
    nake_type = remove_alias( type )
    if not is_reference( nake_type ):
        return type
    else:
        return nake_type.base

def is_const(type):
    """returns True, if type represents C++ const type, False otherwise"""
    nake_type = remove_alias( type )
    return isinstance( nake_type, cpptypes.const_t )

def remove_const(type):
    """removes const from the type definition

    If type is not const type, it will be returned as is
    """

    nake_type = remove_alias( type )
    if not is_const( nake_type ):
        return type
    else:
        return nake_type.base

def remove_declarated( type ):
    """removes type-declaration class-binder L{declarated_t} from the type

    If type is not L{declarated_t}, it will be returned as is
    """
    type = remove_alias( type )
    if isinstance( type, cpptypes.declarated_t ):
        type = type.declaration
    return type

def is_same(type1, type2):
    """returns True, if type1 and type2 are same types"""
    nake_type1 = remove_declarated( type1 )
    nake_type2 = remove_declarated( type2 )
    return nake_type1 == nake_type2

def is_volatile(type):
    """returns True, if type represents C++ volatile type, False otherwise"""
    nake_type = remove_alias( type )
    return isinstance( nake_type, cpptypes.volatile_t )

def remove_volatile(type):
    """removes volatile from the type definition

    If type is not volatile type, it will be returned as is
    """
    nake_type = remove_alias( type )
    if not is_volatile( nake_type ):
        return type
    else:
        return nake_type.base

def remove_cv(type):
    """removes const and volatile from the type definition"""

    nake_type = remove_alias(type)
    if not is_const( nake_type ) and not is_volatile( nake_type ):
        return type
    result = nake_type
    if is_const( nake_type ):
        result = nake_type.base
    if is_volatile( result ):
        result = result.base
    return result

def is_fundamental(type):
    """returns True, if type represents C++ fundamental type"""
    return does_match_definition( type
                                  , cpptypes.fundamental_t
                                  , (cpptypes.const_t, cpptypes.volatile_t) )

class declaration_xxx_traits:
    """this class implements the functionality needed for convinient work with
    declaration classes

    Implemented functionality:
        - find out whether a declaration is a desired one
        - get reference to the declaration
    """
    sequence = [ remove_alias, remove_cv, remove_declarated ]
    def __init__( self, declaration_class ):
        self.declaration_class = declaration_class

    def __apply_sequence( self, type ):
        for f in self.sequence:
            type = f( type )
        return type

    def is_my_case( self, type ):
        """returns True, if type represents the desired declaration, False otherwise"""
        return isinstance( self.__apply_sequence( type ), self.declaration_class )

    def get_declaration( self, type ):
        """returns reference to the declaration

        Precondition: self.is_my_case( type ) == True
        """
        assert self.is_my_case( type )
        return self.__apply_sequence( type )

enum_traits = declaration_xxx_traits( enumeration.enumeration_t )
"""implements functionality, needed for convinient work with C++ enums"""

is_enum = enum_traits.is_my_case
"""returns True, if type represents C++ enumeration declaration, False otherwise"""

enum_declaration = enum_traits.get_declaration
"""returns reference to enum declaration"""

class_traits = declaration_xxx_traits( class_declaration.class_t )
"""implements functionality, needed for convinient work with C++ classes"""

is_class = class_traits.is_my_case
"""returns True, if type represents C++ class definition, False otherwise"""

class_declaration_traits = declaration_xxx_traits( class_declaration.class_declaration_t )
"""implements functionality, needed for convinient work with C++ class declarations"""

is_class_declaration = class_declaration_traits.is_my_case
"""returns True, if type represents C++ class declaration, False otherwise"""

def find_trivial_constructor( type ):
    """returns reference to trivial constructor or None"""
    assert isinstance( type, class_declaration.class_t )
    constructors = filter( lambda x: isinstance( x, calldef.constructor_t ) \
                                     and 0 == len( x.arguments ) \
                           , type.public_members )
    if constructors:
        return constructors[0]
    else:
        return None

def has_trivial_constructor( type ):
    """returns True, if class has trivial constructor, False otherwise"""
    return None != find_trivial_constructor( type )

def has_trivial_copy( type):
    """returns True, if class has copy constructor, False otherwise"""
    assert isinstance( type, class_declaration.class_t )
    constructors = filter( lambda x: isinstance( x, calldef.constructor_t ) \
                                     and x.is_copy_constructor
                           , type.public_members )
    return bool( constructors )

def has_destructor(type):
    """returns True, if class has destructor, False otherwise"""
    assert isinstance( type, class_declaration.class_t )
    return bool( algorithm.find_declaration( type.get_members()
                                             , type=calldef.destructor_t
                                             , recursive=False ) )

def has_public_constructor(type):
    """returns True, if class has public constructor, False otherwise"""
    assert isinstance( type, class_declaration.class_t )
    decls = algorithm.find_all_declarations( type.public_members
                                             , type=calldef.constructor_t
                                             , recursive=False )
    constructors = filter( lambda decl: not decl.is_copy_constructor, decls )
    return bool( constructors )

def has_public_assign(type):
    """returns True, if class has public assign operator, False otherwise"""
    assert isinstance( type, class_declaration.class_t )
    decls = algorithm.find_all_declarations( type.public_members
                                             , type=calldef.member_operator_t
                                             , recursive=False )
    decls = filter( lambda decl: decl.symbol == '=', decls )
    return bool( decls )

def has_public_destructor(type):
    """returns True, if class has public destructor, False otherwise"""
    assert isinstance( type, class_declaration.class_t )
    return bool( algorithm.find_declaration( type.public_members
                                             , type=calldef.destructor_t
                                             , recursive=False ) )


def is_base_and_derived( based, derived ):
    """returns True, if there is "base and derived" relationship between classes, False otherwise"""
    assert isinstance( based, class_declaration.class_t )
    assert isinstance( derived, class_declaration.class_t )

    for base_desc in derived.recursive_bases:
        if base_desc.related_class == based:
            return True
    return False

def has_any_non_copyconstructor( type):
    """returns True, if class has any non "copy constructor", otherwise False"""
    assert isinstance( type, class_declaration.class_t )
    constructors = filter( lambda x: isinstance( x, calldef.constructor_t ) \
                                     and not x.is_copy_constructor
                           , type.public_members )
    return bool( constructors )

def has_public_binary_operator( type, operator_symbol ):
    """returns True, if type has public binary operator, otherwise False"""
    not_artificial = lambda decl: decl.is_artificial == False
    type = remove_alias( type )
    type = remove_cv( type )
    type = remove_declarated( type )
    assert isinstance( type, class_declaration.class_t )

    if is_std_string( type ) or is_std_wstring( type ):
        #In some case compare operators of std::basic_string are not instantiated
        return True

    operators = type.member_operators( function=matchers.custom_matcher_t( not_artificial ) \
                                                & matchers.access_type_matcher_t( 'public' )
                                       , symbol=operator_symbol
                                       , allow_empty=True
                                       , recursive=False )
    if operators:
        return True

    t = cpptypes.declarated_t( type )
    t = cpptypes.const_t( t )
    t = cpptypes.reference_t( t )
    operators = type.top_parent.operators( function=not_artificial
                                           , arg_types=[t, None]
                                           , symbol=operator_symbol
                                           , allow_empty=True
                                           , recursive=True )
    if operators:
        return True
    for bi in type.recursive_bases:
        assert isinstance( bi, class_declaration.hierarchy_info_t )
        if bi.access_type != class_declaration.ACCESS_TYPES.PUBLIC:
            continue
        operators = bi.related_class.member_operators( function=matchers.custom_matcher_t( not_artificial ) \
                                                             & matchers.access_type_matcher_t( 'public' )
                                                       , symbol=operator_symbol
                                                       , allow_empty=True
                                                       , recursive=False )
        if operators:
            return True
    return False

def has_public_equal( type ):
    """returns True, if class has public operator==, otherwise False"""
    return has_public_binary_operator( type, '==' )

def has_public_less( type ):
    """returns True, if class has public operator<, otherwise False"""
    return has_public_binary_operator( type, '<' )

def is_unary_operator( oper ):
    """returns True, if operator is unary operator, otherwise False"""
    #~ definition:
        #~ memeber in class
          #~ ret-type operator symbol()
          #~ ret-type operator [++ --](int)
        #~ globally
          #~ ret-type operator symbol( arg )
          #~ ret-type operator [++ --](X&, int)
    symbols = [ '!', '&', '~', '*', '+', '++', '-', '--' ]
    if not isinstance( oper, calldef.operator_t ):
        return False
    if oper.symbol not in symbols:
        return False
    if isinstance( oper, calldef.member_operator_t ):
        if 0 == len( oper.arguments ):
            return True
        elif oper.symbol in [ '++', '--' ] and isinstance( oper.arguments[0].type, cpptypes.int_t ):
            return True
        else:
            return False
    else:
        if 1 == len( oper.arguments ):
            return True
        elif oper.symbol in [ '++', '--' ] \
             and 2 == len( oper.arguments ) \
             and isinstance( oper.arguments[1].type, cpptypes.int_t ):
            #may be I need to add additional check whether first argument is reference or not?
            return True
        else:
            return False

def is_binary_operator( oper ):
    """returns True, if operator is binary operator, otherwise False"""
    #~ definition:
        #~ memeber in class
          #~ ret-type operator symbol(arg)
        #~ globally
          #~ ret-type operator symbol( arg1, arg2 )
    symbols = [ ',', '()', '[]', '!=', '%', '%=', '&', '&&', '&=', '*', '*=', '+', '+='
                , '-', '-=', '->', '->*', '/', '/=', '<', '<<', '<<=', '<='
                , '=', '==', '>', '>=', '>>', '>>=', '^', '^=', '|', '|=', '||'
    ]
    if not isinstance( oper, calldef.operator_t ):
        return False
    if oper.symbol not in symbols:
        return False
    if isinstance( oper, calldef.member_operator_t ):
        if 1 == len( oper.arguments ):
            return True
        else:
            return False
    else:
        if 2 == len( oper.arguments ):
            return True
        else:
            return False

class __is_convertible_t:
    """implementation details"""
    def __init__( self, source, target ):
        self.__source = self.__normalize( source )
        self.__target = self.__normalize( target )

    def __find_class_by_class_declaration( self, class_decl ):
        found = algorithm.find_declaration( class_decl.parent.declarations
                                            , name=class_decl.name
                                            , type=class_declaration.class_t )
        return found

    def __normalize( self, type_ ):
        type_ = remove_alias( type_ )
        bt_of_type = base_type( type_ )
        if isinstance( bt_of_type, cpptypes.declarated_t ) \
           and isinstance( bt_of_type.declaration, class_declaration.class_declaration_t ):
            type_ = type_.clone()
            bt_of_type = base_type( type_ )
            bt_of_type.declaration = self.__find_class_by_class_declaration( bt_of_type.declaration )
        return type_

    def __test_trivial( self, source, target ):
        if not ( source and target ):
            return False
        if is_same( source, target ):
            return True #X => X
        if is_const( target ) and is_same( source, target.base ):
            return True #X => const X
        if is_reference( target ) and is_same( source, target.base ):
            return True #X => X&
        if is_reference( target ) and is_const( target.base ) and is_same( source, target.base.base ):
            return True #X => const X&
        if is_same( target, cpptypes.pointer_t( cpptypes.void_t() ) ):
            return True #X => void*
        if is_pointer( source ) and is_pointer( target ):
            if is_const( target.base ) and is_same( source.base, target.base.base ):
                return True#X* => const X*
        if is_reference( source ) and is_reference( target ):
            if is_const( target.base ) and is_same( source.base, target.base.base ):
                return True#X& => const X&
        if not is_const( source ) and is_array( source ) and is_pointer( target ):
            if is_same( base_type(source), target.base ):
                return True#X[2] => X*
        if is_array( source ) and is_pointer( target ) and is_const( target.base ):
            if is_same( base_type(source), target.base.base ):
                return True

    def __test_pointer_to_func_or_mv__to__func_or_mv( self, source, target ):
        if is_pointer( source ) \
           and is_reference( target ) \
           and isinstance( target.base
                           , ( cpptypes.free_function_type_t
                               , cpptypes.member_function_type_t
                               , cpptypes.member_variable_type_t ) ) \
           and is_same( source.base, target.base ):
                return True

        if is_pointer( source ) \
           and isinstance( target
                           , ( cpptypes.free_function_type_t
                               , cpptypes.member_function_type_t
                               , cpptypes.member_variable_type_t ) ) \
           and is_same( source.base, target ):
                return True

        if is_pointer( target ) \
           and is_reference( source ) \
           and isinstance( source.base
                           , ( cpptypes.free_function_type_t
                               , cpptypes.member_function_type_t
                               , cpptypes.member_variable_type_t ) ) \
           and is_same( source.base, target.base ):
                return True

        if is_pointer( target ) \
           and isinstance( source
                           , ( cpptypes.free_function_type_t
                               , cpptypes.member_function_type_t
                               , cpptypes.member_variable_type_t ) ) \
           and is_same( target.base, source ):
                return True


    def __test_const_x_ref__to__x( self, source, target ):
        if not is_reference( source ) \
           or not is_const( source.base ) \
           or not is_same( source.base.base, target ):
            return False
        if is_fundamental( target ):
            return True
        if is_enum( target ):
            return True
        if isinstance( target, cpptypes.declarated_t ):
            assert isinstance( target.declaration, class_declaration.class_t )
            if has_trivial_copy( target.declaration ):
                return True #we have copy constructor
        return False

    def __test_const_ref_x__to__y(self, source, target):
        if not is_reference( source ) or not is_const( source.base ):
            return False
        if is_fundamental( source.base.base ) and is_fundamental( target ):
            return True
        if is_convertible( source.base.base, cpptypes.int_t() ) and is_enum( target ):
            return True
        if isinstance( target, cpptypes.declarated_t ):
            assert isinstance( target.declaration, class_declaration.class_t )
            if has_trivial_copy( target.declaration ):
                return True #we have copy constructor
        return False

    def __test_ref_x__to__x( self, source, target ):
        if not is_reference( source ) or not is_same( source.base, target ):
            return False
        if is_fundamental( target ):
            return True
        if is_enum( target ):
            return True
        if isinstance( target, cpptypes.declarated_t ):
            assert isinstance( target.declaration, class_declaration.class_t )
            if has_trivial_copy( target.declaration ):
                return True #we have copy constructor
        return False

    def __test_ref_x__to__y(self, source, target):
        if not is_reference( source ):
            return False
        if is_fundamental( source.base ) and is_fundamental( target ):
            return True
        if is_convertible( source.base, cpptypes.int_t() ) and is_enum( target ):
            return True
        if isinstance( target, cpptypes.declarated_t ):
            assert isinstance( target.declaration, class_declaration.class_t )
            if has_trivial_copy( target.declaration ):
                return True #we have copy constructor
        return False

    def __test_fundamental__to__fundamental(self, source, target):
        if not is_fundamental( base_type( source ) ) or not is_fundamental( base_type( target ) ):
            return False
        if is_void( base_type( source ) ) or is_void( base_type( target ) ):
            return False
        if is_fundamental( source ) and is_fundamental( target ):
            return True
        if not is_pointer( source ) and is_fundamental( target ):
            return True
        if not is_pointer( source ) and is_const( target ) and is_fundamental( target.base ):
            return True
        if is_fundamental( source ) \
           and is_reference( target ) \
           and is_const( target.base ) \
           and is_fundamental( target.base.base ):
            return True #X => const Y&
        return False

    def __test_derived_to_based( self, source, target ):
        derived = base_type( source )
        base = base_type( target )
        if not ( isinstance( derived, cpptypes.declarated_t ) \
                 and isinstance( derived.declaration, class_declaration.class_t ) ):
            return False
        if not ( isinstance( base, cpptypes.declarated_t ) \
                 and isinstance( base.declaration, class_declaration.class_t ) ):
            return False
        base = base.declaration
        derived = derived.declaration
        if not is_base_and_derived( base, derived ):
            return False
        for b in derived.recursive_bases:
            if ( b.related_class is base ) and b.access_type != class_declaration.ACCESS_TYPES.PRIVATE:
                break
        else:
            return False

        base = target
        derived = source
        is_both_declarated = lambda x, y: isinstance( x, cpptypes.declarated_t ) \
                                          and isinstance( y, cpptypes.declarated_t )
        #d => b
        if is_both_declarated( base, derived ):
            return True
        #d* => b*
        if is_pointer( derived ) and is_pointer( base ) \
           and is_both_declarated( base.base, derived.base ):
            return True
        #const d* => const b*
        if is_pointer( derived ) and is_pointer( base ) \
           and is_const( derived.base ) and is_const( base.base ) \
           and is_both_declarated( base.base.base, derived.base.base ):
            return True
        #d* => const b*
        if is_pointer( derived ) and is_pointer( base ) \
           and is_const( derived.base )\
           and is_both_declarated( base.base.base, derived.base ):
            return True

        #d& => b&
        if is_reference( derived ) and is_reference( base ) \
           and is_both_declarated( base.base, derived.base ):
            return True
        #const d& => const b&
        if is_reference( derived ) and is_reference( base ) \
           and is_const( derived.base ) and is_const( base.base ) \
           and is_both_declarated( base.base.base, derived.base.base ):
            return True
        #d& => const b&
        if is_reference( derived ) and is_reference( base ) \
           and is_const( derived.base )\
           and is_both_declarated( base.base.base, derived.base ):
            return True
        return False

    def is_convertible( self ):
        source = self.__source
        target = self.__target

        if self.__test_trivial(source, target):
            return True
        if is_array( source ) or is_array( target ):
            return False
        if self.__test_const_x_ref__to__x(source, target):
            return True
        if self.__test_const_ref_x__to__y(source, target):
            return True
        if self.__test_ref_x__to__x(source, target):
            return True
        if self.__test_ref_x__to__y(source, target):
            return True
        if self.__test_fundamental__to__fundamental( source, target ):
            return True
        if self.__test_pointer_to_func_or_mv__to__func_or_mv( source, target ):
            return True
        if self.__test_derived_to_based( source, target ):
            return True

        if isinstance( source, cpptypes.declarated_t ):
            if isinstance( source.declaration, enumeration.enumeration_t ) \
               and is_fundamental( target ) \
               and not is_void( target ):
                return True # enum could be converted to any integral type

            assert isinstance( source.declaration, class_declaration.class_t )
            source_inst = source.declaration
            #class instance could be convertible to something else if it has operator
            casting_operators = algorithm.find_all_declarations( source_inst.declarations
                                                                 , type=calldef.casting_operator_t
                                                                 , recursive=False )
            if casting_operators:
                for operator in casting_operators:
                    if is_convertible( operator.return_type, target ):
                        return True

        #may be target is class too, so in this case we should check whether is
        #has constructor from source
        if isinstance( target, cpptypes.declarated_t ):
            assert isinstance( target.declaration, class_declaration.class_t )
            constructors = algorithm.find_all_declarations( target.declaration.declarations
                                                            , type=calldef.constructor_t
                                                            , recursive=False )
            if constructors:
                for constructor in constructors:
                    if 1 != len( constructor.arguments ):
                        continue
                    #TODO: add test to check explicitness
                    if is_convertible( source, constructor.arguments[0].type ):
                        return True

        return False

def is_convertible( source, target ):
    """returns True, if source could be converted to target, otherwise False"""
    return __is_convertible_t( source, target ).is_convertible()

def __is_noncopyable_single( class_ ):
    """implementation details"""
    #It is not enough to check base classes, we should also to check
    #member variables.
    mvars = filter( lambda x: isinstance( x, variable.variable_t )
                    , class_.declarations )
    for mvar in mvars:
        if mvar.type_qualifiers.has_static:
            continue
        type_ = remove_alias( mvar.type )
        type_ = remove_reference( type_ )
        if is_const( type_ ):
            no_const = remove_const( type_ )
            if is_fundamental( no_const ) or is_enum( no_const):
                return True
            if is_class( no_const ):
                return True
        if is_class( type_ ):
            cls = type_.declaration
            if is_noncopyable( cls ):
                return True
    return False

def is_noncopyable( class_ ):
    """returns True, if class is noncopyable, False otherwise"""
    if class_.class_type == class_declaration.CLASS_TYPES.UNION:
        return False
    for base_desc in class_.recursive_bases:
        assert isinstance( base_desc, class_declaration.hierarchy_info_t )
        if base_desc.related_class.decl_string in ('::boost::noncopyable', '::boost::noncopyable_::noncopyable' ):
            return True
        if not has_trivial_copy( base_desc.related_class ):
            protected_ctrs = filter( lambda x: isinstance( x, calldef.constructor_t ) \
                                               and x.is_copy_constructor
                                     , base_desc.related_class.protected_members )
            if not protected_ctrs:
                return True

        if __is_noncopyable_single( base_desc.related_class ):
            return True

    if not has_trivial_copy( class_ ) \
       or not has_public_constructor( class_ )\
       or class_.is_abstract \
       or ( has_destructor( class_ ) and not has_public_destructor( class_ ) ):
        return True

    return __is_noncopyable_single( class_ )


def is_defined_in_xxx( xxx, cls ):
    """small helper function, that checks whether class ( C{cls} ) is defined
    under C{::xxx} namespace"""
    if not cls.parent:
        return False

    if not isinstance( cls.parent, namespace.namespace_t ):
        return False

    if xxx != cls.parent.name:
        return False

    xxx_ns = cls.parent
    if not xxx_ns.parent:
        return False

    if not isinstance( xxx_ns.parent, namespace.namespace_t ):
        return False

    if '::' != xxx_ns.parent.name:
        return False

    global_ns = xxx_ns.parent
    return None is global_ns.parent

class impl_details:
    """implementation details"""
    @staticmethod
    def is_defined_in_xxx( xxx, cls ):
        """implementation details"""
        if not cls.parent:
            return False

        if not isinstance( cls.parent, namespace.namespace_t ):
            return False

        if xxx != cls.parent.name:
            return False

        xxx_ns = cls.parent
        if not xxx_ns.parent:
            return False

        if not isinstance( xxx_ns.parent, namespace.namespace_t ):
            return False

        if '::' != xxx_ns.parent.name:
            return False

        global_ns = xxx_ns.parent
        return None is global_ns.parent

    @staticmethod
    def find_value_type( global_ns, value_type_str ):
        """implementation details"""
        if not value_type_str.startswith( '::' ):
            value_type_str = '::' + value_type_str
        found = global_ns.decls( name=value_type_str
                                 , function=lambda decl: not isinstance( decl, calldef.calldef_t )
                                 ,  allow_empty=True )
        if not found:
            if cpptypes.FUNDAMENTAL_TYPES.has_key( value_type_str ):
                return cpptypes.FUNDAMENTAL_TYPES[value_type_str]
            elif is_std_string( value_type_str ):
                string_ = global_ns.typedef( '::std::string' )
                return remove_declarated( string_ )
            elif is_std_wstring( value_type_str ):
                string_ = global_ns.typedef( '::std::wstring' )
                return remove_declarated( string_ )
            else:
                return None
        if len( found ) == 1:
            return found[0]
        else:
            return None

class smart_pointer_traits:
    """implements functionality, needed for convinient work with smart pointers"""

    @staticmethod
    def is_smart_pointer( type ):
        """returns True, if type represents instantiation of C{boost::shared_ptr}, False otherwise"""
        type = remove_alias( type )
        type = remove_cv( type )
        type = remove_declarated( type )
        if not isinstance( type, ( class_declaration.class_declaration_t, class_declaration.class_t ) ):
            return False
        if not impl_details.is_defined_in_xxx( 'boost', type ):
            return False
        return type.decl_string.startswith( '::boost::shared_ptr<' )

    @staticmethod
    def value_type( type ):
        """returns reference to boost::shared_ptr value type"""
        if not smart_pointer_traits.is_smart_pointer( type ):
            raise TypeError( 'Type "%s" is not instantiation of boost::shared_ptr' % type.decl_string )
        type = remove_alias( type )
        cls = remove_cv( type )
        cls = remove_declarated( type )
        if isinstance( cls, class_declaration.class_t ):
            return remove_declarated( cls.typedef( "value_type", recursive=False ).type )
        elif not isinstance( cls, ( class_declaration.class_declaration_t, class_declaration.class_t ) ):
            raise RuntimeError( "Unable to find out shared_ptr value type. shared_ptr class is: %s" % cls.decl_string )
        else:
            value_type_str = templates.args( cls.name )[0]
            ref = impl_details.find_value_type( cls.top_parent, value_type_str )
            if None is ref:
                raise RuntimeError( "Unable to find out shared_ptr value type. shared_ptr class is: %s" % cls.decl_string )
            return ref

def is_std_string( type ):
    """returns True, if type represents C++ std::string, False otherwise"""
    decl_strings = [
        '::std::basic_string<char,std::char_traits<char>,std::allocator<char> >'
        , '::std::basic_string<char, std::char_traits<char>, std::allocator<char> >'
        , '::std::string' ]
    if isinstance( type, types.StringTypes ):
        return type in decl_strings
    else:
        type = remove_alias( type )
        return remove_cv( type ).decl_string in decl_strings

def is_std_wstring( type ):
    """returns True, if type represents C++ std::wstring, False otherwise"""
    decl_strings = [
        '::std::basic_string<wchar_t,std::char_traits<wchar_t>,std::allocator<wchar_t> >'
        , '::std::basic_string<wchar_t, std::char_traits<wchar_t>, std::allocator<wchar_t> >'
        , '::std::wstring' ]
    if isinstance( type, types.StringTypes ):
        return type in decl_strings
    else:
        type = remove_alias( type )
        return remove_cv( type ).decl_string in decl_strings











