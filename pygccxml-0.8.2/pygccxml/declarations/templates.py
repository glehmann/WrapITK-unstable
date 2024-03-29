# Copyright 2004 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

""" 
template instantiation parser

This module implements all functionality necessary to parse C++ template
instantiations.In other words this module is able to extract next information from 
the string like this C{ std::vector<int> }.
    - name ( std::vector )
    - list of arguments ( int )

This module also defines few convenience function like L{split} and L{join}.
"""

import pattern_parser

__THE_PARSER = pattern_parser.parser_t( '<', '>', ',' )

def is_instantiation( decl_string ):
    """
    returns True if decl_string is template instantiation and False otherwise
    
    @param decl_string: string that should be checked for pattern presence
    @type decl_string: str
    
    @return: bool
    """
    global __THE_PARSER
    return __THE_PARSER.has_pattern( decl_string )

def name( decl_string ):
    """
    returns name of instantiated template
    
    @type decl_string: str
    @return: str
    """
    global __THE_PARSER
    return __THE_PARSER.name( decl_string )

def args( decl_string ):
    """
    returns list of template arguments
    
    @type decl_string: str
    @return: [str]
    """
    global __THE_PARSER
    return __THE_PARSER.args( decl_string )
        
def split( decl_string ):
    """returns (name, [arguments] )"""
    global __THE_PARSER
    return __THE_PARSER.split( decl_string )
    
def split_recursive( decl_string ):
    """returns [(name, [arguments])]"""
    global __THE_PARSER
    return __THE_PARSER.split_recursive( decl_string )

def join( name, args ):
    """returns name< argument_1, argument_2, ..., argument_n >"""
    global __THE_PARSER
    return __THE_PARSER.join( name, args )