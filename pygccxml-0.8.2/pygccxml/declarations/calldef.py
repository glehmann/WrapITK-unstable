# Copyright 2004 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

"""
defines classes, that describes "callable" declarations

This modules contains definition for next C++ declarations:
    - operator
        - member
        - free
    - function
        - member
        - free
    - constructor
    - destructor
"""

import cpptypes
import algorithm
import declaration
import type_traits
import call_invocation

class VIRTUALITY_TYPES:
    """class that defines "virtuality" constants"""
    NOT_VIRTUAL = 'not virtual'
    VIRTUAL = 'virtual'
    PURE_VIRTUAL = 'pure virtual'
    ALL = [NOT_VIRTUAL, VIRTUAL, PURE_VIRTUAL]
#preserving backward compatebility
FUNCTION_VIRTUALITY_TYPES = VIRTUALITY_TYPES

#First level in hierarchy of calldef
class argument_t(object):
    """
    class, that describes argument of "callable" declaration
    """

    def __init__( self, name='', type=None, default_value=None ):
        object.__init__(self)
        self._name = name
        self._default_value = default_value
        self._type = type

    def __str__(self):
        if self.default_value==None:
            return "%s %s"%(self.type, self.name)
        else:
            return "%s %s=%s"%(self.type, self.name, self.default_value)

    def __eq__(self, other):
        if not isinstance( other, self.__class__ ):
            return False
        return self.name == other.name \
               and self.default_value == other.default_value \
               and self.type == other.type

    def __ne__( self, other):
        return not self.__eq__( other )

    def __lt__(self, other):
        if not isinstance( other, self.__class__ ):
            return self.__class__.__name__ < other.__class__.__name__
        return self.name < other.name \
               and self.default_value < other.default_value \
               and self.type < other.type

    def _get_name(self):
        return self._name
    def _set_name(self, name):
        self._name = name
    name = property( _get_name, _set_name
                     , doc="""Argument name.
                     @type: str""" )

    def _get_default_value(self):
        return self._default_value
    def _set_default_value(self, default_value):
        self._default_value = default_value
    default_value = property( _get_default_value, _set_default_value
                              , doc="""Argument's default value or None.
                              @type: str""")

    def _get_type(self):
        return self._type
    def _set_type(self, type):
        self._type = type
    type = property( _get_type, _set_type
                     , doc="""The type of the argument.
                     @type: L{type_t}""")

class calldef_t( declaration.declaration_t ):
    """base class for all "callable" declarations"""
    def __init__( self, name='', arguments=None, exceptions=None, return_type=None, has_extern=False ):
        declaration.declaration_t.__init__( self, name )
        if not arguments:
            arguments = []
        self._arguments = arguments
        if not exceptions:
            exceptions = []
        self._exceptions = exceptions
        self._return_type = return_type
        self._has_extern = has_extern
        self._demangled_name = None

    def _get__cmp__call_items(self):
        """implementation details"""
        raise NotImplementedError()

    def _get__cmp__items( self ):
        """implementation details"""
        items = [ self.arguments
                  , self.return_type
                  , self.has_extern
                  , self._sorted_list( self.exceptions ) ]
        items.extend( self._get__cmp__call_items() )
        return items

    def __eq__(self, other):
        if not declaration.declaration_t.__eq__( self, other ):
            return False
        return self.return_type == other.return_type \
               and self.arguments == other.arguments \
               and self.has_extern == other.has_extern \
               and self._sorted_list( self.exceptions ) \
                   == other._sorted_list( other.exceptions )

    def _get_arguments(self):
        return self._arguments
    def _set_arguments(self, arguments):
        self._arguments = arguments
    arguments = property( _get_arguments , _set_arguments
                          , doc="""The argument list.
                          @type: list of L{argument_t}""")

    def _get_exceptions(self):
        return self._exceptions
    def _set_exceptions(self, exceptions):
        self._exceptions = exceptions
    exceptions = property( _get_exceptions, _set_exceptions
                           , doc="""The list of exceptions.
                           @type: list of L{declaration_t}""")

    def _get_return_type(self):
        return self._return_type
    def _set_return_type(self, return_type):
        self._return_type = return_type
    return_type = property( _get_return_type, _set_return_type
                            , doc='''The type of the return value of the "callable" or None (constructors).
                            @type: L{type_t}
                            ''')

    def _get_overloads(self):
        if not self.parent:
            return []
        # finding all functions with the same name
        return self.parent.calldefs(
            name=self.name
            , function=lambda decl: not (decl is self )
            , allow_empty=True
            , recursive=False )

    overloads = property( _get_overloads
                          , doc="""A list of overloaded "callables" (i.e. other callables with the same name within the same scope.
                          @type: list of L{calldef_t}""" )

    def _get_has_extern(self):
        return self._has_extern
    def _set_has_extern(self, has_extern):
        self._has_extern = has_extern
    has_extern = property( _get_has_extern, _set_has_extern,
                           doc="""Was this callable declared as "extern"?
                           @type: bool
                           """)

    def __remove_parent_fname( self, demangled ):
        """implementation details"""
        demangled = demangled.strip()
        parent_fname = algorithm.full_name( self.parent )
        if parent_fname.startswith( '::' ) and not demangled.startswith( '::' ):
            parent_fname = parent_fname[2:]
        demangled = demangled[ len( parent_fname ): ]
        return demangled

    def _get_demangled_name( self ):
        if not self.demangled:
            self._demangled_name = ''

        if self._demangled_name:
            return self._demangled_name

        if self._demangled_name == '':
            return self.name

        demangled = self.demangled
        if self.return_type:
            return_type = type_traits.remove_alias( self.return_type ).decl_string

            if return_type.startswith( '::' ) and not self.demangled.startswith( '::' ):
                return_type = return_type[2:]
            demangled = self.demangled
            if demangled.startswith( return_type ):
                demangled = demangled[ len( return_type ): ]
                demangled = demangled.strip()
        #removing scope
        demangled_name = call_invocation.name( self.__remove_parent_fname( demangled ) )
        if demangled_name.startswith( '::' ):
            demangled_name = demangled_name[2:]
        #to be on the safe side
        if demangled_name.startswith( self.name ):
            self._demangled_name = demangled_name
            return self._demangled_name

        #well, I am going to try an other strategy
        fname = algorithm.full_name( self )
        found = self.demangled.find( fname )
        if -1 == found:
            if fname.startswith( '::' ):
                fname = fname[2:]
            found = self.demangled.find( fname )
            if -1 == found:
                self._demangled_name = ''
                return self.name
        demangled_name = call_invocation.name( self.demangled[ found: ] )
        demangled_name = self.__remove_parent_fname( demangled_name )
        if demangled_name.startswith( '::' ):
            demangled_name = demangled_name[2:]
        #to be on the safe side
        if demangled_name.startswith( self.name ):
            self._demangled_name = demangled_name
            return self._demangled_name
        #if -1 == found:
        self._demangled_name = ''
        return self.name

    demangled_name = property( _get_demangled_name
                              , doc="returns function demangled name. It can help you to deal with function template instantiations")

#Second level in hierarchy of calldef
class member_calldef_t( calldef_t ):
    """base class for "callable" declarations that defined within C++ class or struct"""
    def __init__( self, virtuality=None, has_const=None, has_static=None, *args, **keywords ):
        calldef_t.__init__( self, *args, **keywords )
        self._virtuality = virtuality
        self._has_const = has_const
        self._has_static = has_static

    def __str__(self):
        # Get the full name of the calldef...
        name = algorithm.full_name(self)
        if name[:2]=="::":
            name = name[2:]
        # Add the arguments...
        args = map(lambda a: str(a), self.arguments)
        res = "%s(%s)"%(name, ", ".join(args))
        # Add the return type...
        if self.return_type!=None:
            res = "%s %s"%(self.return_type, res)
        # const?
        if self.has_const:
            res += " const"
        # static?
        if self.has_static:
            res = "static "+res
        # Append the declaration class
        cls = self.__class__.__name__
        if cls[-2:]=="_t":
            cls = cls[:-2]
        return "%s [%s]"%(res, cls)

    def _get__cmp__call_items(self):
        """implementation details"""
        return [ self.virtuality, self.has_static, self.has_const ]

    def __eq__(self, other):
        if not calldef_t.__eq__( self, other ):
            return False
        return self.virtuality == other.virtuality \
               and self.has_static == other.has_static \
               and self.has_const == other.has_const

    def get_virtuality(self):
        return self._virtuality
    def set_virtuality(self, virtuality):
        assert virtuality in VIRTUALITY_TYPES.ALL
        self._virtuality = virtuality
    virtuality = property( get_virtuality, set_virtuality
                           , doc="""Describes the "virtuality" of the member (as defined by the string constants in the class L{VIRTUALITY_TYPES}).
                           @type: str""")

    def _get_access_type(self):
        return self.parent.find_out_member_access_type( self )
    access_type = property( _get_access_type
                            , doc="""Return the access type of the member (as defined by the string constants in the class L{ACCESS_TYPES}.
                            @type: str""")

    def _get_has_const(self):
        return self._has_const
    def _set_has_const(self, has_const):
        self._has_const = has_const
    has_const = property( _get_has_const, _set_has_const
                          , doc="""describes, whether "callable" has const modifier or not""")

    def _get_has_static(self):
        return self._has_static
    def _set_has_static(self, has_static):
        self._has_static = has_static
    has_static = property( _get_has_static, _set_has_static
                           , doc="""describes, whether "callable" has static modifier or not""")

    def function_type(self):
        """returns function type. See L{type_t} hierarchy"""
        if self.has_static:
            return cpptypes.free_function_type_t( return_type=self.return_type
                                           , arguments_types=[ arg.type for arg in self.arguments ] )
        else:
            return cpptypes.member_function_type_t( class_inst=self.parent
                                           , return_type=self.return_type
                                           , arguments_types=[ arg.type for arg in self.arguments ]
                                           , has_const=self.has_const )

    def _create_decl_string(self):
        return self.function_type().decl_string


class free_calldef_t( calldef_t ):
    """base class for "callable" declarations that defined within C++ namespace"""
    def __init__( self, *args, **keywords ):
        calldef_t.__init__( self, *args, **keywords )

    def __str__(self):
        # Get the full name of the calldef...
        name = algorithm.full_name(self)
        if name[:2]=="::":
            name = name[2:]
        # Add the arguments...
        args = map(lambda a: str(a), self.arguments)
        res = "%s(%s)"%(name, ", ".join(args))
        # Add the return type...
        if self.return_type!=None:
            res = "%s %s"%(self.return_type, res)
        # extern?
        if self.has_extern:
            res = "extern "+res
        # Append the declaration class
        cls = self.__class__.__name__
        if cls[-2:]=="_t":
            cls = cls[:-2]
        return "%s [%s]"%(res, cls)

    def _get__cmp__call_items(self):
        """implementation details"""
        return []

    def function_type(self):
        """returns function type. See L{type_t} hierarchy"""
        return cpptypes.free_function_type_t( return_type=self.return_type
                                     , arguments_types=[ arg.type for arg in self.arguments ] )

    def _create_decl_string(self):
        return self.function_type().decl_string

class operator_t(object):
    """base class for "operator" declarations"""
    OPERATOR_WORD_LEN = len( 'operator' )
    def __init__(self):
        object.__init__(self)

    def _get_symbol(self):
        return self.name[operator_t.OPERATOR_WORD_LEN:].strip()
    symbol = property( _get_symbol,
                       doc="returns symbol of operator. For example: operator+, symbol is equal to '+'")

#Third level in hierarchy of calldef
class member_function_t( member_calldef_t ):
    """describes member function declaration"""
    def __init__( self, *args, **keywords ):
        member_calldef_t.__init__( self, *args, **keywords )


class constructor_t( member_calldef_t ):
    """describes constructor declaration"""
    def __init__( self, *args, **keywords ):
        member_calldef_t.__init__( self, *args, **keywords )

    def _get_is_copy_constructor(self):
        args = self.arguments
        if 1 != len( args ):
            return False
        arg = args[0]
        if not type_traits.is_reference( arg.type ):
            return False
        if not type_traits.is_const( arg.type.base ):
            return False
        unaliased = type_traits.remove_alias( arg.type.base )
        #unaliased now refers to const_t instance
        if not isinstance( unaliased.base, cpptypes.declarated_t ):
            return False
        return id(unaliased.base.declaration) == id(self.parent)
    is_copy_constructor = property(_get_is_copy_constructor
                                   , doc="returns True if described declaration is copy constructor, otherwise False")

class destructor_t( member_calldef_t ):
    """describes deconstructor declaration"""
    def __init__( self, *args, **keywords ):
        member_calldef_t.__init__( self, *args, **keywords )

class member_operator_t( member_calldef_t, operator_t ):
    """describes member operator declaration"""
    def __init__( self, *args, **keywords ):
        member_calldef_t.__init__( self, *args, **keywords )
        operator_t.__init__( self, *args, **keywords )

class casting_operator_t( member_calldef_t, operator_t ):
    """describes casting operator declaration"""
    def __init__( self, *args, **keywords ):
        member_calldef_t.__init__( self, *args, **keywords )
        operator_t.__init__( self, *args, **keywords )

class free_function_t( free_calldef_t ):
    """describes free function declaration"""
    def __init__( self, *args, **keywords ):
        free_calldef_t.__init__( self, *args, **keywords )

class free_operator_t( free_calldef_t, operator_t ):
    """describes free operator declaration"""
    def __init__( self, *args, **keywords ):
        free_calldef_t.__init__( self, *args, **keywords )
        operator_t.__init__( self, *args, **keywords )
