# Copyright 2004 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

"""
defines class that describes C++ global and member variable declaration
"""

import declaration
import class_declaration

class variable_t( declaration.declaration_t ):
    """describes C++ global and member variable declaration"""

    def __init__( self, name='', type=None, type_qualifiers=None, value=None, bits=None):
        """creates class that describes C++ global or member variable"""
        declaration.declaration_t.__init__( self, name )
        self._type = type
        self._type_qualifiers = type_qualifiers
        self._value = value
        self._bits = bits

    def _get__cmp__items( self ):
        """implementation details"""
        return [ self.type, self.type_qualifiers, self.value ]

    def __eq__(self, other):
        """implementation details"""
        if not declaration.declaration_t.__eq__( self, other ):
            return False
        return self.type == other.type \
               and self.type_qualifiers == other.type_qualifiers \
               and self.value == other.value \
               and self.bits == other.bits

    def _get_type(self):
        return self._type
    def _set_type(self, type):
        self._type = type
    type = property( _get_type, _set_type
                     , doc="reference to the variable L{type<type_t>}"    )

    def _get_type_qualifiers(self):
        return self._type_qualifiers
    def _set_type_qualifiers(self, type_qualifiers):
        self._type_qualifiers = type_qualifiers
    type_qualifiers = property( _get_type_qualifiers, _set_type_qualifiers
                                , doc="reference to the L{type_qualifiers_t} instance" )

    def _get_value(self):
        return self._value
    def _set_value(self, value):
        self._value = value
    value = property( _get_value, _set_value
                      , doc="string, that contains the variable value"    )

    def _get_bits(self):
        return self._bits
    def _set_bits(self, bits):
        self._bits = bits
    bits = property( _get_bits, _set_bits
                     , doc="integer, that contains information about how many bit takes bit field")

    @property
    def access_type(self):
        if not isinstance( self.parent, class_declaration.class_t ):
            raise RuntimeError( "access_type functionality only available on member variables and not on global variables" )
        return self.parent.find_out_member_access_type( self )

