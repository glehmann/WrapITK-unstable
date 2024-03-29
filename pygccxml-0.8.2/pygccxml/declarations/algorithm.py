# Copyright 2004 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

"""defines few unrelated algorithms, that works on declarations"""

import types

def declaration_path( decl ):
    """
    returns a list of parent declarations names

    @param decl: declaration for which declaration path should be calculated
    @type decl: L{declaration_t}

    @return: [names], where first item contains top parent name and last item
             contains decl name
    """
    #TODO:
    #If parent declaration cache already has declaration_path, reuse it for
    #calculation.
    if not decl:
        return []
    if not decl.cache.declaration_path:
        result = [ decl.name ]
        parent = decl.parent
        while parent:
            result.append( parent.name )
            parent = parent.parent
        result.reverse()
        decl.cache.declaration_path = result
        return result
    else:
        return decl.cache.declaration_path

def full_name( decl ):
    """
    returns full name of the declaration
    @param decl: declaration for which full name should be calculated. If decl
    belongs to unnamed namespace, then L{full_name} is not valid C++ full name.

    @type decl: L{declaration_t}

    @return: full name of declarations.
    """
    if None is decl:
        raise RuntimeError( "Unable to generate full name for None object!" )
    if not decl.cache.full_name:
        decl_path = declaration_path( decl )
        ##Here I have lack of knowledge:
        ##TODO: "What is the full name of declaration declared in unnamed namespace?"
        result = filter( None, decl_path )
        result = result[0] + '::'.join( result[1:] )
        decl.cache.full_name = result
        return result
    else:
        return decl.cache.full_name


def make_flatten( decl_or_decls ):
    """
    converts tree representation of declarations to flatten one.

    @param decl_or_decls: reference to list of declaration's or single declaration
    @type decl_or_decls: L{declaration_t} or [ L{declaration_t} ]

    @return: [ all internal declarations ]
    """
    import pygccxml.declarations #prevent cyclic import
    def proceed_single( decl ):
        answer = [ decl ]
        if not isinstance( decl, pygccxml.declarations.scopedef_t ):
            return answer
        for elem in decl.declarations:
            if isinstance( elem, pygccxml.declarations.scopedef_t ):
                answer.extend( proceed_single( elem ) )
            else:
                answer.append( elem )
        return answer

    decls = []
    if isinstance( decl_or_decls, types.ListType ):
        decls.extend( decl_or_decls )
    else:
        decls.append( decl_or_decls )
    answer = []
    for decl in decls:
        answer.extend( proceed_single( decl ) )
    return answer

def __make_flatten_generator( decl_or_decls ):
    """
    converts tree representation of declarations to flatten one.

    @param decl_or_decls: reference to list of declaration's or single declaration
    @type decl_or_decls: L{declaration_t} or [ L{declaration_t} ]

    @return: [ all internal declarations ]
    """

    import pygccxml.declarations
    def proceed_single( decl ):
        yield decl
        if not isinstance( decl, pygccxml.declarations.scopedef_t):
            return
        for internal in decl.declarations:
            if isinstance( internal, pygccxml.declarations.scopedef_t):
                for internal_internal in proceed_single( internal ):
                    yield internal_internal
            else:
                yield internal

    if isinstance( decl_or_decls, types.ListType ):
        for creator in decl_or_decls:
            for internal in proceed_single( creator ):
                yield internal
    else:
        for internal in proceed_single( decl_or_decls ):
            yield internal

def get_global_namespace(decls):
    import pygccxml.declarations
    found = filter( lambda decl: decl.name == '::'
                                 and isinstance( decl, pygccxml.declarations.namespace_t )
                    , make_flatten( decls ) )
    if len( found ) == 1:
        return found[0]
    raise RuntimeError( "Unable to find global namespace." )

class match_declaration_t:
    """
    helper class for different search algorithms.

    This class will help developer to match declaration by:
        - declaration type, for example L{class_t} or L{operator_t}.
        - declaration name
        - declaration full name
        - reference to parent declaration
    """

    def __init__( self, type=None, name=None, fullname=None, parent=None ):
        self.type = type
        self.name = name
        self.fullname = fullname
        self.parent = parent

    def does_match_exist(self, inst):
        """
        returns True if inst do match one of specified criteria

        @param inst: declaration instance
        @type inst: L{declaration_t}

        @return: bool
        """
        answer = True
        if None != self.type:
            answer &= isinstance( inst, self.type)
        if None != self.name:
            answer &= inst.name == self.name
        if None != self.parent:
            answer &= self.parent is inst.parent
        if None != self.fullname:
            if inst.name:
                answer &= self.fullname == full_name( inst )
            else:
                answer = False
        return answer

    def __call__(self, inst):
        """C{return self.does_match_exist(inst)}"""
        return self.does_match_exist(inst)

def find_all_declarations( declarations
                           , type=None
                           , name=None
                           , parent=None
                           , recursive=True
                           , fullname=None ):
    """
    returns a list of all declarations that match criteria, defined by developer

    For more information about arguments see L{match_declaration_t} class.

    @return: [ matched declarations ]
    """
    decls = []
    if recursive:
        decls = make_flatten( declarations )
    else:
        decls = declarations

    return filter( match_declaration_t(type, name, fullname, parent), decls )

def find_declaration( declarations
                      , type=None
                      , name=None
                      , parent=None
                      , recursive=True
                      , fullname=None ):
    """
    returns single declaration that match criteria, defined by developer.
    If more the one declaration was found None will be returned.

    For more information about arguments see L{match_declaration_t} class.

    @return: matched declaration L{declaration_t} or None
    """
    decl = find_all_declarations( declarations, type=type, name=name, parent=parent, recursive=recursive, fullname=fullname )
    if len( decl ) == 1:
        return decl[0]

def find_first_declaration( declarations, type=None, name=None, parent=None, recursive=True, fullname=None ):
    """
    returns first declaration that match criteria, defined by developer

    For more information about arguments see L{match_declaration_t} class.

    @return: matched declaration L{declaration_t} or None
    """
    matcher = match_declaration_t(type, name, fullname, parent)
    if recursive:
        decls = make_flatten( declarations )
    else:
        decls = declarations
    for decl in decls:
        if matcher( decl ):
            return decl
    return None

def declaration_files(decl_or_decls):
    """
    returns set of files

    Every declaration is declared in some file. This function returns set, that
    contains all file names of declarations.

    @param decl_or_decls: reference to list of declaration's or single declaration
    @type decl_or_decls: L{declaration_t} or [ L{declaration_t} ]

    @return: set( declaration file names )
    """
    files = set()
    decls = make_flatten( decl_or_decls )
    for decl in decls:
        if decl.location:
            files.add( decl.location.file_name )
    return files

class visit_function_has_not_been_found_t( RuntimeError ):
    """
    exception that is raised, from L{apply_visitor}, when a visitor could not be
    applied.

    """
    def __init__( self, visitor, decl_inst ):
        RuntimeError.__init__( self )
        self.__msg = \
            "Unable to find visit function. Visitor class: %s. Declaration instance class: %s'" \
            % ( visitor.__class__.__name__, decl_inst.__class__.__name__ )
    def __str__(self):
        return self.__msg

def apply_visitor( visitor, decl_inst):
    """
    applies a visitor on declaration instance

    @param visitor: instance
    @type visitor: L{type_visitor_t} or L{decl_visitor_t}
    """
    fname = 'visit_' + decl_inst.__class__.__name__[:-2] #removing '_t' from class name
    if not hasattr(visitor, fname ):
        raise visit_function_has_not_been_found_t( visitor, decl_inst )
    getattr( visitor, fname )()
