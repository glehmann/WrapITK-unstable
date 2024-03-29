# Copyright 2004 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

import unittest
import autoconfig
import parser_test_case

from pygccxml import utils
from pygccxml import parser
from pygccxml import declarations

class tester_t( parser_test_case.parser_test_case_t ):
    COMPILATION_MODE = parser.COMPILATION_MODE.ALL_AT_ONCE    
    declarations = None
    def __init__(self, *args ):
        parser_test_case.parser_test_case_t.__init__( self, *args )
        self.header = 'type_traits.hpp'
        self.declarations = None
        
    def setUp(self):
        if not tester_t.declarations:
            tester_t.declarations = parser.parse( [self.header], self.config )
        self.declarations = tester_t.declarations
        
    def __test_type_category( self, ns_name, controller ):                
        ns_control = declarations.find_declaration( self.declarations
                                                    , type=declarations.namespace_t
                                                    , name=ns_name )
        self.failUnless( ns_control, "unable to find '%s' namespace" % ns_name )
        ns_yes = declarations.find_declaration( ns_control
                                                , type=declarations.namespace_t
                                                , name='yes' )
        self.failUnless( ns_yes, "unable to find 'yes' namespace" )
        ns_no = declarations.find_declaration( ns_control
                                               , type=declarations.namespace_t
                                               , name='no' )
        self.failUnless( ns_no, "unable to find 'no' namespace" )
        for decl in ns_yes.declarations:   
            if isinstance( decl, declarations.variable_t ):
                self.failUnless( controller( decl.type )
                                 , 'for type "%s" the answer to the question "%s" should be True' 
                                 % ( decl.type.decl_string, ns_name ) )
            else:
                self.failUnless( controller( decl )
                                 , 'for type "%s" the answer to the question "%s" should be True' 
                                 % ( decl.decl_string, ns_name ) )
        for decl in ns_no.declarations:
            self.failIf( controller( decl )
                         , 'for type "%s" the answer to the question "%s" should be False' 
                            % ( decl.decl_string, ns_name ) )

    def __test_type_transformation( self, ns_name, transformer ):
        ns_control = declarations.find_declaration( self.declarations
                                                    , type=declarations.namespace_t
                                                    , name=ns_name )
        self.failUnless( ns_control, "unable to find '%s' namespace" % ns_name )
        ns_before = declarations.find_declaration( ns_control
                                                   , type=declarations.namespace_t
                                                   , name='before' )
        self.failUnless( ns_before, "unable to find 'before' namespace" )
        ns_after = declarations.find_declaration( ns_control
                                                  , type=declarations.namespace_t
                                                  , name='after' )
        self.failUnless( ns_after, "unable to find 'after' namespace" )
        
        for tbefore in ns_before.declarations:          
            tafter = declarations.find_declaration( ns_after, name=tbefore.name )
            self.failUnless( tafter, "unable to find transformed type definition for type '%s'" % tbefore.decl_string )
            transformed = transformer( tbefore )
            self.failUnless( declarations.is_same( transformed, tafter )
                             , "there is a difference between expected type and result. typedef name: %s" % tbefore.decl_string )

    def test_is_enum(self):
        self.__test_type_category( 'is_enum', declarations.is_enum )

    def test_is_void(self):
        self.__test_type_category( 'is_void', declarations.is_void )

    def test_is_integral(self):
        self.__test_type_category( 'is_integral', declarations.is_integral )

    def test_is_pointer(self):
        self.__test_type_category( 'is_pointer', declarations.is_pointer )

    def test_is_const(self):
        self.__test_type_category( 'is_const', declarations.is_const )

    def test_is_volatile(self):
        self.__test_type_category( 'is_volatile', declarations.is_volatile )

    def test_is_reference(self):
        self.__test_type_category( 'is_reference', declarations.is_reference )

    def test_is_floating_point(self):
        self.__test_type_category( 'is_floating_point', declarations.is_floating_point )

    def test_is_array(self):
        self.__test_type_category( 'is_array', declarations.is_array)

    def test_is_fundamental(self):
        self.__test_type_category( 'is_fundamental', declarations.is_fundamental )
        
    def test_has_trivial_constructor(self):
        self.__test_type_category( 'has_trivial_constructor', declarations.has_trivial_constructor )

    def test_has_public_constructor(self):
        self.__test_type_category( 'has_public_constructor', declarations.has_public_constructor )

    def test_has_public_destructor(self):
        self.__test_type_category( 'has_public_destructor', declarations.has_public_destructor )

    def test_has_any_non_copyconstructor(self):
        self.__test_type_category( 'has_any_non_copyconstructor', declarations.has_any_non_copyconstructor)

    def test_has_trivial_copy(self):
        self.__test_type_category( 'has_trivial_copy', declarations.has_trivial_copy )

    def test_is_base_and_derived(self):
        ns = declarations.find_declaration( self.declarations
                                            , type=declarations.namespace_t
                                            , name='is_base_and_derived' )
        self.failUnless( ns, "unable to find 'is_base_and_derived' namespace" )
        base = declarations.find_declaration( ns.declarations
                                              , type=declarations.class_t
                                              , name='base' )
        derived = declarations.find_declaration( ns.declarations
                                                 , type=declarations.class_t
                                                 , name='derived' )
        self.failUnless( base and derived and declarations.is_base_and_derived( base, derived ) )

        unrelated1 = declarations.find_declaration( ns.declarations
                                                    , type=declarations.class_t
                                                    , name='unrelated1' )
        
        unrelated2 = declarations.find_declaration( ns.declarations
                                                    , type=declarations.class_t
                                                    , name='unrelated2' )
        self.failUnless( base and derived and not declarations.is_base_and_derived( unrelated1, unrelated2 ) )

    def test_is_same(self):
        self.failUnless( declarations.is_same( declarations.int_t, declarations.int_t ) ) 
        self.failIf( declarations.is_same( declarations.int_t, declarations.float_t ) )

    def test_remove_const(self):
        self.__test_type_transformation( 'remove_const', declarations.remove_const )

    def test_remove_reference(self):
        self.__test_type_transformation( 'remove_reference', declarations.remove_reference )

    def test_remove_volatile(self):
        self.__test_type_transformation( 'remove_volatile', declarations.remove_volatile )

    def test_remove_cv(self):
        self.__test_type_transformation( 'remove_cv', declarations.remove_cv )

    def test_remove_pointer(self):
        self.__test_type_transformation( 'remove_pointer', declarations.remove_pointer )

    def test_is_unary_binary_operator(self):
        operator_not = declarations.find_declaration( self.declarations
                                                      , type=declarations.operator_t
                                                      , fullname='::is_unary_operator::dummy::operator!' )
        self.failUnless( operator_not, 'operator! was not found' )
        self.failUnless( declarations.is_unary_operator( operator_not ), 'operator! should be idenitified as unary operator' )
        self.failUnless( not declarations.is_binary_operator( operator_not ), 'operator! should be idenitified as unary operator' )
        
        operator_class_p = declarations.find_declaration( self.declarations
                                                          , type=declarations.operator_t
                                                          , fullname='::is_unary_operator::dummy::operator+' )
        self.failUnless( operator_class_p, 'operator+ was not found' )
        self.failUnless( not declarations.is_unary_operator( operator_class_p ), 'operator+ should be idenitified as binary operator' )
        self.failUnless( declarations.is_binary_operator( operator_class_p ), 'operator! should be idenitified as binary operator' )
        
        operator_class_pp = declarations.find_declaration( self.declarations
                                                           , type=declarations.operator_t
                                                           , fullname='::is_unary_operator::dummy::operator++' )
        self.failUnless( operator_class_pp, 'operator++ was not found' )
        self.failUnless( declarations.is_unary_operator( operator_class_pp ), 'operator++ should be idenitified as unary operator' )
        self.failUnless( not declarations.is_binary_operator( operator_class_pp ), 'operator++ should be idenitified as unary operator' )
        
        operator_pp = declarations.find_declaration( self.declarations
                                                     , type=declarations.operator_t
                                                     , fullname='::is_unary_operator::operator++' )
        self.failUnless( operator_pp, 'operator++ was not found' )
        self.failUnless( declarations.is_unary_operator( operator_pp ), 'operator++ should be idenitified as unary operator' )
        self.failUnless( not declarations.is_binary_operator( operator_pp ), 'operator++ should be idenitified as unary operator' )

        operator_mm = declarations.find_declaration( self.declarations
                                                     , type=declarations.operator_t
                                                     , fullname='::is_unary_operator::operator*' )
        self.failUnless( operator_mm, 'operator-- was not found' )
        self.failUnless( not declarations.is_unary_operator( operator_mm ), 'operator-- should be idenitified as binary operator' )
        self.failUnless( declarations.is_binary_operator( operator_mm ), 'operator-- should be idenitified as binray operator' )

        operator_pe = declarations.find_declaration( self.declarations
                                                     , type=declarations.operator_t
                                                     , fullname='::is_unary_operator::operator+=' )
        self.failUnless( operator_pe, 'operator+= was not found' )
        self.failUnless( not declarations.is_unary_operator( operator_pe ), 'operator+= should be idenitified as binary operator' )
        self.failUnless( declarations.is_binary_operator( operator_pe ), 'operator+= should be idenitified as binray operator' )

    def __is_convertible_impl( self, decl ):
        if decl.name == 'x81':
            i = 0
        defs = decl.bases[0].related_class.declarations
        source_type = declarations.find_declaration( defs, name='source_type' )
        target_type = declarations.find_declaration( defs, name='target_type' )
        expected_type = declarations.find_declaration( defs
                                                       , name='expected'
                                                       , type=declarations.enumeration_t )
        expected_value = bool( expected_type.get_name2value_dict()['value'] )
        if expected_value != declarations.is_convertible( source_type, target_type ):
            print decl.name
        
    def test_is_convertible( self ):
        ns_is_convertible = declarations.find_declaration( self.declarations
                                                           , type=declarations.namespace_t
                                                           , name="is_convertible" )
                                                                   
        self.failUnless( ns_is_convertible, "namespace is_convertible was not found" )
        for tester in filter( lambda decl: decl.name.startswith( 'x' ), ns_is_convertible.declarations ):
            self.__is_convertible_impl( tester )
        
def create_suite():
    suite = unittest.TestSuite()        
    suite.addTest( unittest.makeSuite(tester_t))
    return suite

def run_suite():
    unittest.TextTestRunner(verbosity=2).run( create_suite() )

if __name__ == "__main__":
    run_suite()