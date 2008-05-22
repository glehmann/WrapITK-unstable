# Copyright 2004 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

import os
import types
import pprint
import xml.sax
import warnings
import xml.sax.handler
from pygccxml.declarations import *
from pygccxml import utils

##convention
#XML_NN - XML Node Name
#XML_AN - XML Attribute Name
#also those constants are sorted for easy searching.
XML_AN_ABSTRACT = "abstract"
XML_AN_ACCESS = "access"
XML_AN_ARTIFICIAL = "artificial"
XML_AN_BASE_TYPE = "basetype"
XML_AN_BASES = "bases"
XML_AN_BITS = "bits"
XML_AN_CONST = "const"
XML_AN_CONTEXT = "context"
XML_AN_DEFAULT = "default"
XML_AN_DEMANGLED = "demangled"
XML_AN_EXTERN = "extern"
XML_AN_FILE = "file"
XML_AN_ID = "id"
XML_AN_INCOMPLETE = "incomplete"
XML_AN_INIT = "init"
XML_AN_LINE = "line"
XML_AN_MANGLED = "mangled"
XML_AN_MAX = "max"
XML_AN_MEMBERS = "members"
XML_AN_MUTABLE = "mutable"
XML_AN_NAME = "name"
XML_AN_PURE_VIRTUAL = "pure_virtual"
XML_AN_RESTRICT = "restrict"
XML_AN_RETURNS = "returns"
XML_AN_STATIC = "static"
XML_AN_THROW = "throw"
XML_AN_TYPE = "type"
XML_AN_VIRTUAL = "virtual"
XML_AN_VOLATILE = "volatile"
XML_NN_ARGUMENT = "Argument"
XML_NN_ARRAY_TYPE = "ArrayType"
XML_NN_CASTING_OPERATOR = "Converter"
XML_NN_CLASS = "Class"
XML_NN_CONSTRUCTOR = "Constructor"
XML_NN_CV_QUALIFIED_TYPE = "CvQualifiedType"
XML_NN_DESTRUCTOR = "Destructor"
XML_NN_ENUMERATION = "Enumeration"
XML_NN_ENUMERATION_VALUE = "EnumValue"
XML_NN_FIELD = "Field"
XML_NN_FILE = "File"
XML_NN_FUNCTION = "Function"
XML_NN_FUNCTION_TYPE = "FunctionType"
XML_NN_FUNDAMENTAL_TYPE = "FundamentalType"
XML_NN_FREE_OPERATOR = "OperatorFunction"
XML_NN_MEMBER_OPERATOR = "OperatorMethod"
XML_NN_METHOD = "Method"
XML_NN_METHOD_TYPE = "MethodType"
XML_NN_NAMESPACE = "Namespace"
XML_NN_OFFSET_TYPE = "OffsetType"
XML_NN_POINTER_TYPE = "PointerType"
XML_NN_REFERENCE_TYPE = "ReferenceType"
XML_NN_ROOT = "GCC_XML"
XML_NN_STRUCT = "Struct"
XML_NN_TYPEDEF = "Typedef"
XML_NN_UNION = "Union"
XML_NN_VARIABLE = "Variable"
   
class scanner_t( xml.sax.handler.ContentHandler ):
    def __init__(self, gccxml_file, decl_factory, *args ):
        xml.sax.handler.ContentHandler.__init__(self, *args )
        self.logger = utils.loggers.gccxml
        self.gccxml_file = gccxml_file
        #defining parsing tables
        self.__readers = {
               XML_NN_FILE : self.__read_file
               , XML_NN_NAMESPACE : self.__read_namespace
               , XML_NN_ENUMERATION : self.__read_enumeration
               , XML_NN_ENUMERATION_VALUE : self.__read_enumeration_value
               , XML_NN_ARRAY_TYPE : self.__read_array_type
               , XML_NN_CV_QUALIFIED_TYPE : self.__read_cv_qualified_type                   
               , XML_NN_POINTER_TYPE : self.__read_pointer_type
               , XML_NN_REFERENCE_TYPE : self.__read_reference_type
               , XML_NN_FUNDAMENTAL_TYPE : self.__read_fundamental_type                   
               , XML_NN_ARGUMENT : self.__read_argument
               , XML_NN_FUNCTION_TYPE : self.__read_function_type                   
               , XML_NN_METHOD_TYPE : self.__read_method_type
               , XML_NN_OFFSET_TYPE : self.__read_offset_type
               , XML_NN_TYPEDEF : self.__read_typedef
               , XML_NN_VARIABLE : self.__read_variable
               , XML_NN_CLASS : self.__read_class
               , XML_NN_STRUCT : self.__read_struct
               , XML_NN_UNION : self.__read_union
               , XML_NN_FIELD : self.__read_field
               , XML_NN_CASTING_OPERATOR : self.__read_casting_operator
               , XML_NN_CONSTRUCTOR : self.__read_constructor
               , XML_NN_DESTRUCTOR : self.__read_destructor
               , XML_NN_FUNCTION : self.__read_function
               , XML_NN_FREE_OPERATOR : self.__read_free_operator
               , XML_NN_MEMBER_OPERATOR : self.__read_member_operator
               , XML_NN_METHOD : self.__read_method
        }
        self.deep_declarations = [
            XML_NN_CASTING_OPERATOR
            , XML_NN_CONSTRUCTOR
            , XML_NN_DESTRUCTOR
            , XML_NN_ENUMERATION
            , XML_NN_FILE
            , XML_NN_FUNCTION
            , XML_NN_FREE_OPERATOR
            , XML_NN_MEMBER_OPERATOR
            , XML_NN_METHOD
            , XML_NN_FUNCTION_TYPE
            , XML_NN_METHOD_TYPE
        ]

        assert isinstance( decl_factory, decl_factory_t )
        self.__decl_factory = decl_factory
        
        #mapping from id -> decl
        self.__declarations = {}
        #mapping from id -> type
        self.__types = {}
        #mapping from id -> file        
        self.__files = {}
        #mapping between decl id -> access
        self.__access = {}
        #current object under construction
        self.__inst = None
        #mapping from id to members
        self.__members = {}
    
    def read( self ):
        xml.sax.parse( self.gccxml_file, self )
        #updating membership
        members_mapping = {}
        for gccxml_id, members in self.__members.iteritems():
            decl = self.__declarations.get( gccxml_id, None )
            if not decl or not isinstance( decl, scopedef_t):
                continue
            members_mapping[ id( decl ) ] = members
        self.__members = members_mapping
        
    def declarations(self):
        return self.__declarations
        
    def types(self):
        return self.__types
        
    def files(self):
        return self.__files

    def access(self):
        return self.__access
    
    def members(self):
        return self.__members

    def startElement(self, name, attrs):
        try:
            if name not in self.__readers:
                return
            obj = self.__readers[name]( attrs )
            if not obj:
                return #it means that we worked on internals
                       #for example EnumValue of function argument
            if name in self.deep_declarations:
                self.__inst = obj
            self.__read_access( attrs )
            if isinstance( obj, declaration_t ):
                self.__update_membership( attrs )
                self.__declarations[ attrs[XML_AN_ID] ] = obj
                if not isinstance( obj, namespace_t ):
                    self.__read_location( obj, attrs )
                if isinstance( obj, scopedef_t):
                    #deprecated 
                    #self.__read_members( obj, attrs )
                    if isinstance( obj, class_t ):
                        self.__read_bases( obj, attrs )
                self.__read_artificial(obj, attrs)
                self.__read_mangled( obj, attrs)
                self.__read_demangled( obj, attrs)
            elif isinstance( obj, type_t ):
                self.__types[ attrs[XML_AN_ID] ] = obj
            elif isinstance( obj, types.StringTypes ):
                self.__files[ attrs[XML_AN_ID] ] = obj
            else:
                self.logger.warning( 'Unknown object type has been found.'
                                     + ' Please report this bug to pygccxml development team.' )
        except Exception, error:
            msg = 'error occured, while parsing element with name "%s" and attrs "%s".'
            msg = msg + os.linesep + 'Error: %s.' % str( error )
            self.logger.error( msg % ( name, pprint.pformat( attrs.keys() ) ) )
            raise
        
    def endElement(self, name):
        if name in self.deep_declarations:
            self.__inst = None

    def __read_location(self, decl, attrs):
        decl.location = location_t( file_name=attrs[XML_AN_FILE], line=int( attrs[XML_AN_LINE]))

    def __update_membership(self, attrs):
        parent = attrs.get( XML_AN_CONTEXT, None )
        if not parent:
            return 
        if not self.__members.has_key( parent ):
            self.__members[ parent ] = []
        self.__members[parent].append( attrs[XML_AN_ID] )

    def __read_members(self, decl, attrs ):
        decl.declarations = attrs.get(XML_AN_MEMBERS, "")

    def __read_bases(self, decl, attrs ):
        decl.bases = attrs.get( XML_AN_BASES, "" )

    def __read_artificial( self, decl, attrs ):
        decl.is_artificial = attrs.get( XML_AN_ARTIFICIAL, False )

    def __read_mangled( self, decl, attrs ):
        decl.mangled = attrs.get( XML_AN_MANGLED, None )

    def __read_demangled( self, decl, attrs ):
        decl.demangled = attrs.get( XML_AN_DEMANGLED, None )
        
    def __read_access( self, attrs ):
        self.__access[ attrs[XML_AN_ID] ] = attrs.get( XML_AN_ACCESS, ACCESS_TYPES.PUBLIC )

    def __read_root(self, attrs):
        pass
        
    def __read_file( self, attrs ):
        return attrs.get( XML_AN_NAME, '' )

    def __read_namespace(self, attrs):
        ns_name = attrs.get( XML_AN_NAME, '' )
        if '.' in ns_name:
            #if '.' in namespace then this is mangled namespace -> in c++ namespace{...}
            #that is almost true: gcc mangale name using top file name.
            #almost all files has '.' in name
            ns_name = ''
        return self.__decl_factory.create_namespace( name=ns_name )

    def __read_enumeration(self, attrs):
        enum_name = attrs.get( XML_AN_NAME, '' )
        if '$_' in enum_name or '._' in enum_name:
            #it means that this is unnamed enum. in c++ enum{ x };
            enum_name = ''
        return self.__decl_factory.create_enumeration( name=enum_name )

    def __read_enumeration_value( self, attrs ):
        name = attrs.get( XML_AN_NAME, '' )
        num = int(attrs[XML_AN_INIT])
        self.__inst.append_value(name, num)

    def __read_array_type( self, attrs ):
        type_ = attrs[ XML_AN_TYPE ]
        size = array_t.SIZE_UNKNOWN
        if attrs.has_key(XML_AN_MAX):
            if attrs[XML_AN_MAX]:
                try:
                    size = int( attrs[XML_AN_MAX] )
                except ValueError:
                    try:
                        size = int( attrs[ XML_AN_MAX ], 16 )
                    except ValueError:
                        warnings.warn( 'unable to find out array size from expression "%s"' % attrs[ XML_AN_MAX ] )
        return array_t( type_, size + 1 )
 
    def __read_cv_qualified_type( self, attrs ):
        if attrs.has_key( XML_AN_CONST ):
            return const_t( attrs[XML_AN_TYPE] )
        elif attrs.has_key( XML_AN_VOLATILE ):
            return volatile_t( attrs[XML_AN_TYPE] )
        elif attrs.has_key( XML_AN_RESTRICT ):
            #TODO: find out what is restrict type
            #and I really don't know what I should return
            return volatile_t( attrs[XML_AN_TYPE] )
        else: 
            assert 0 

    def __read_pointer_type( self, attrs ):
        return pointer_t( attrs[XML_AN_TYPE] )
    
    def __read_reference_type( self, attrs ):
        return reference_t( attrs[XML_AN_TYPE] )

    def __read_fundamental_type(self, attrs ):
        try:
            return FUNDAMENTAL_TYPES[ attrs.get( XML_AN_NAME, '' ) ]
        except KeyError:
            raise RuntimeError( "pygccxml error: unable to find fundamental type with name '%s'."
                                % attrs.get( XML_AN_NAME, '' ) )

    def __read_offset_type( self,attrs ):
        base = attrs[ XML_AN_BASE_TYPE ]
        type_ = attrs[ XML_AN_TYPE ]
        return member_variable_type_t( class_inst=base, variable_type=type_ )

    def __read_argument( self, attrs ):
        if isinstance( self.__inst, calldef_type_t ):
            self.__inst.arguments_types.append( attrs[XML_AN_TYPE] )
        else:
            argument = argument_t()
            argument.name = attrs.get( XML_AN_NAME, 'arg%d' % len(self.__inst.arguments) )
            argument.type = attrs[XML_AN_TYPE]           
            argument.default_value = attrs.get( XML_AN_DEFAULT, None )
            if argument.default_value == '<gccxml-cast-expr>':
                argument.default_value = None
            self.__inst.arguments.append( argument )
     
    def __read_calldef( self, calldef, attrs ):
        #destructor for example doesn't have return type
        calldef.return_type =  attrs.get( XML_AN_RETURNS, None )
        if isinstance( calldef, declaration_t ):
            calldef.name = attrs.get(XML_AN_NAME, '')
            calldef.has_extern = attrs.get( XML_AN_EXTERN, False )
            calldef.exceptions = attrs.get( XML_AN_THROW, "" ).split()
 
    def __read_member_function( self, calldef, attrs ):       
        self.__read_calldef( calldef, attrs )
        calldef.has_const = attrs.get( XML_AN_CONST, False )        
        if isinstance( calldef, declaration_t ):
            calldef.has_static = attrs.get( XML_AN_STATIC, False )
            if attrs.has_key( XML_AN_PURE_VIRTUAL ):
                calldef.virtuality = VIRTUALITY_TYPES.PURE_VIRTUAL
            elif attrs.has_key( XML_AN_VIRTUAL ):
                calldef.virtuality = VIRTUALITY_TYPES.VIRTUAL
            else:
                calldef.virtuality = VIRTUALITY_TYPES.NOT_VIRTUAL
        else:
            calldef.class_inst = attrs[XML_AN_BASE_TYPE]   
    
    def __read_function_type(self, attrs):
        answer = free_function_type_t()
        self.__read_calldef( answer, attrs )
        return answer
    
    def __read_method_type(self, attrs):
        answer = member_function_type_t()
        self.__read_member_function( answer, attrs )
        return answer

    def __read_typedef(self, attrs ):
        return self.__decl_factory.create_typedef( name=attrs.get( XML_AN_NAME, '' ), type=attrs[XML_AN_TYPE])

    def __read_variable(self, attrs ):
        type_qualifiers = type_qualifiers_t()        
        type_qualifiers.has_mutable = attrs.get(XML_AN_MUTABLE, False)
        type_qualifiers.has_static = attrs.get(XML_AN_EXTERN, False)
        bits = attrs.get( XML_AN_BITS, None )
        if bits:
            bits = int( bits )
        return self.__decl_factory.create_variable( name=attrs.get( XML_AN_NAME, '' )
                           , type=attrs[XML_AN_TYPE]
                           , type_qualifiers=type_qualifiers
                           , value=attrs.get( XML_AN_INIT, None )
                           , bits=bits)
                           
    __read_field = __read_variable #just a synonim

    def __read_class_impl(self, class_type, attrs):
        decl = None
        name = attrs.get(XML_AN_NAME, '')
        if '$' in name or '.' in name:
            name = ''
        if attrs.has_key( XML_AN_INCOMPLETE ):
            decl = self.__decl_factory.create_class_declaration(name=name)
        else:
            decl = self.__decl_factory.create_class( name=name, class_type=class_type )
            if attrs.get( XML_AN_ABSTRACT, False ):
                decl.is_abstract = True
            else:
                decl.is_abstract = False
        return decl
    
    def __read_class( self, attrs ):
        return self.__read_class_impl( CLASS_TYPES.CLASS, attrs )

    def __read_struct( self, attrs ):
        return self.__read_class_impl( CLASS_TYPES.STRUCT, attrs )

    def __read_union( self, attrs ):
        return self.__read_class_impl( CLASS_TYPES.UNION, attrs )

    def __read_casting_operator(self, attrs ):
        operator = self.__decl_factory.create_casting_operator()
        self.__read_member_function( operator, attrs )
        return operator
 
    def __read_constructor( self, attrs ):
        constructor = self.__decl_factory.create_constructor()
        self.__read_member_function( constructor, attrs )
        return constructor

    def __read_function(self, attrs):
        gfunction = self.__decl_factory.create_free_function()
        self.__read_calldef( gfunction, attrs )
        return gfunction
 
    def __read_method(self, attrs):
        mfunction = self.__decl_factory.create_member_function()
        self.__read_member_function( mfunction, attrs )
        return mfunction
 
    def __read_destructor(self, attrs):
        destructor = self.__decl_factory.create_destructor()
        self.__read_member_function( destructor, attrs )
        destructor.name = '~' + destructor.name
        return destructor
 
    def __read_free_operator(self, attrs ):
        operator = self.__decl_factory.create_free_operator()
        self.__read_member_function( operator, attrs )
        if 'new' in operator.name or 'delete' in operator.name:
            operator.name = 'operator ' + operator.name
        else:
            operator.name = 'operator' + operator.name
        return operator
 
    def __read_member_operator(self, attrs):
        operator = self.__decl_factory.create_member_operator()
        self.__read_member_function( operator, attrs )
        if 'new' in operator.name or 'delete' in operator.name:
            operator.name = 'operator ' + operator.name
        else:
            operator.name = 'operator' + operator.name
        return operator
