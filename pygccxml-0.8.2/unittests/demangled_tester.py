# Copyright 2004 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

import os
import unittest
import autoconfig
import parser_test_case

from pygccxml import utils
from pygccxml import parser
from pygccxml import declarations

class tester_impl_t( parser_test_case.parser_test_case_t ):
    def __init__(self, architecture, *args ):
        parser_test_case.parser_test_case_t.__init__( self, *args )
        self.header = 'demangled.hpp'
        self.global_ns = None
        self.architecture = architecture
        
    def setUp(self):
        reader = parser.source_reader_t( self.config )
        decls = None
        if 32 == self.architecture:
            decls = reader.read_file( self.header )
        else:
            original_get_architecture = utils.get_architecture
            utils.get_architecture = lambda: 64
            decls = reader.read_xml_file( 
                    os.path.join( autoconfig.data_directory, 'demangled_tester_64bit.xml' ) )
            utils.get_architecture = original_get_architecture
        self.global_ns = declarations.get_global_namespace( decls )
            
    def test( self ):                
        demangled = self.global_ns.namespace( 'demangled' )
        if 32 == self.architecture:
            cls = demangled.class_( 'item_t<3740067437l, 11l, 2147483648l>' )
            self.failUnless( cls._name == 'item_t<0deece66d,11,080000000>' )
        else:
            cls = demangled.class_( "item_t<25214903917l, 11l, 2147483648l>" )
            self.failUnless( cls._name == 'item_t<25214903917,11,2147483648>' )


class tester_32_t( tester_impl_t ):
    def __init__(self, *args):
        tester_impl_t.__init__(self, 32, *args)

class tester_64_t( tester_impl_t ):
    def __init__(self, *args):
        tester_impl_t.__init__(self, 64, *args)

            
def create_suite():
    suite = unittest.TestSuite()        
    suite.addTest( unittest.makeSuite(tester_32_t))    
    suite.addTest( unittest.makeSuite(tester_64_t))    
    return suite

def run_suite():
    unittest.TextTestRunner(verbosity=2).run( create_suite() )

if __name__ == "__main__":
    run_suite()