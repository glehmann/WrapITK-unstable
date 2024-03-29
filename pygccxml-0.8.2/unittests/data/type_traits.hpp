// Copyright 2004 Roman Yakovenko.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)

//Almost all test cases have been taken
//from boost.type_traits (http://www.boost.org) library.

#define TYPE_PERMUTATION( BASE, NAME )                        \
    typedef BASE NAME##_t;                                     \
    typedef BASE const NAME##_const_t;                         \
    typedef BASE volatile NAME##_volatile_t;                   

struct some_struct_t{
    void do_smth();
    int member;
};

struct incomplete_type;

namespace is_void{
namespace yes{
    typedef void void_t;
    typedef void const void_cont_t;
    typedef void volatile void_volatile_t;
}
namespace no{
    typedef void* void_ptr_t;
    typedef int int_t;
    typedef some_struct_t some_struct_alias_t;
    typedef incomplete_type incomplete_type_alias_t;
    typedef void(*function_t)();
    typedef void (some_struct_t::*member_function_t)();
} }

namespace is_integral{
namespace yes{   

    TYPE_PERMUTATION( bool, bool )
    TYPE_PERMUTATION( char, char )
    TYPE_PERMUTATION( unsigned char, uchar )
    TYPE_PERMUTATION( short, short )
    TYPE_PERMUTATION( unsigned short, ushort )
    TYPE_PERMUTATION( int, int )
    TYPE_PERMUTATION( unsigned int, uint )
    TYPE_PERMUTATION( long, long )
    TYPE_PERMUTATION( unsigned long, ulong )
    TYPE_PERMUTATION( long long int, llint )
    TYPE_PERMUTATION( long long unsigned int, ulli )
}
namespace no{
    typedef some_struct_t some_struct_alias_t;
    typedef float* float_ptr_t;
    typedef float& float_ref_t;
    typedef const float& const_float_ref_t;
    typedef incomplete_type incomplete_type_alias;
    typedef void(*function_t)();
    typedef void (some_struct_t::*member_function_t)();
    TYPE_PERMUTATION( void, void )
    TYPE_PERMUTATION( float, float )
    TYPE_PERMUTATION( double, double )
    TYPE_PERMUTATION( long double, ldouble )
} }

namespace is_floating_point{
namespace yes{   
    
    TYPE_PERMUTATION( float, float )
    TYPE_PERMUTATION( double, double )
    TYPE_PERMUTATION( long double, ldouble )
}
namespace no{
    typedef some_struct_t some_struct_alias_t;
    typedef float* float_ptr_t;
    typedef float& float_ref_t;
    typedef const float& const_float_ref_t;
    typedef incomplete_type incomplete_type_alias;
    typedef void(*function_t)();
    typedef void (some_struct_t::*member_function_t)();
    TYPE_PERMUTATION( void, void )   
    TYPE_PERMUTATION( bool, bool )
    TYPE_PERMUTATION( char, char )
    TYPE_PERMUTATION( unsigned char, uchar )
    TYPE_PERMUTATION( short, short )
    TYPE_PERMUTATION( unsigned short, ushort )
    TYPE_PERMUTATION( int, int )
    TYPE_PERMUTATION( unsigned int, uint )
    TYPE_PERMUTATION( long, long )
    TYPE_PERMUTATION( unsigned long, ulong )
    TYPE_PERMUTATION( long long int, llint )
    TYPE_PERMUTATION( long long unsigned int, ulli )   
} }

namespace is_fundamental{
namespace yes{   

#define FUNDAMENTAL_TYPE_PERMUTATION( BASE, NAME )            \
    typedef BASE NAME##_t;                                     \
    typedef BASE const NAME##_const_t;                         \
    typedef BASE volatile NAME##_volatile_t;                   

    TYPE_PERMUTATION( void, void )
    TYPE_PERMUTATION( bool, bool )
    TYPE_PERMUTATION( char, char )
    TYPE_PERMUTATION( unsigned char, uchar )
    TYPE_PERMUTATION( short, short )
    TYPE_PERMUTATION( unsigned short, ushort )
    TYPE_PERMUTATION( int, int )
    TYPE_PERMUTATION( unsigned int, uint )
    TYPE_PERMUTATION( long, long )
    TYPE_PERMUTATION( unsigned long, ulong )
    TYPE_PERMUTATION( long long int, llint )
    TYPE_PERMUTATION( long long unsigned int, ulli )
    TYPE_PERMUTATION( float, float )
    TYPE_PERMUTATION( double, double )
    TYPE_PERMUTATION( long double, ldouble )
}
namespace no{
    typedef some_struct_t some_struct_alias_t;
    typedef float* float_ptr_t;
    typedef float& float_ref_t;
    typedef const float& const_float_ref_t;
    typedef incomplete_type incomplete_type_alias;
    typedef void(*function_t)();
    typedef void (some_struct_t::*member_function_t)();

} }

namespace is_pointer{
namespace yes{
    typedef int* int_ptr_t;
    typedef const int* const_int_ptr_t;
    typedef volatile int* volatile_int_ptr_t;
    typedef some_struct_t* some_struct_ptr_t;
    typedef int* const int_const_ptr_t;
    typedef int* volatile int_volatile_ptr_t;
    typedef void(*function_t)();
    typedef void (some_struct_t::*member_function_t)();   
}
    
namespace no{
    typedef int int_t;
    typedef int& int_ref_t;
    typedef some_struct_t some_struct_alias_t;
    typedef int*& int_ptr_ref_t;
} }


namespace remove_pointer{
namespace before{
    typedef int* x1;
    typedef const int* x2;
    typedef volatile int* x3;
    typedef some_struct_t* x4;
    typedef int* const x5;
    typedef int* volatile x6;
    typedef void(*x7)();
    typedef void (some_struct_t::*x8)();   
}
    
namespace after{
    typedef int x1;
    typedef const int x2;
    typedef volatile int x3;
    typedef some_struct_t x4;
    typedef int const x5;
    typedef int volatile x6;
    typedef void(*x7)();
    typedef void (some_struct_t::*x8)();      
} }


namespace is_reference{
namespace yes{

    typedef int& int_ref_t;
    typedef const int& const_int_ref_t;
    typedef int const& int_const_ref_t;
    typedef some_struct_t& some_struct_ref_t;
    typedef int*& int_ptr_ref_t;   
}
    
namespace no{
    typedef int* int_ptr_t;
    typedef const int* const_int_ptr_t;
    typedef volatile int* volatile_int_ptr_t;
    typedef some_struct_t* some_struct_ptr_t;
    typedef int* const int_const_ptr_t;
    typedef int* volatile int_volatile_ptr_t;
    typedef void(*function_t)();
    typedef void (some_struct_t::*member_function_t)();   
    typedef int int_t;
} }

namespace remove_reference{
namespace before{

    typedef int& x1;
    typedef const int& x2;
    typedef some_struct_t& x3;
    typedef int*& x4;   
    typedef void (some_struct_t::*x5)();   
}
    
namespace after{
    typedef int x1;
    typedef const int x2;
    typedef some_struct_t x3;
    typedef int* x4;   
    typedef void (some_struct_t::*x5)();   
} }

namespace is_const{
namespace yes{

    typedef const void const_void_t;
    typedef const incomplete_type const_incomplete_type_t;
    typedef int* const int_const_t;
    //TODO typedef const int& const_int_ref_t;
}
    
namespace no{
    typedef int* int_ptr_t;
    typedef const int* const_int_ptr_t;
    typedef volatile int* volatile_int_ptr_t;
    typedef some_struct_t* some_struct_ptr_t;
    typedef int* volatile int_volatile_ptr_t;
    typedef void(*function_t)();
    typedef void (some_struct_t::*member_function_t)();   
    typedef int int_t;
} }

namespace remove_const{
namespace before{

    typedef const void x1;
    typedef const incomplete_type x2;
    typedef int* const x3;
    typedef int* volatile x4;
}
    
namespace after{
    typedef void x1;
    typedef incomplete_type x2;
    typedef int* x3;
    typedef int* volatile x4;
} }

namespace is_volatile{
namespace yes{

    typedef void * volatile vvoid_ptr_t;
    typedef volatile int volatile_int_t;
}
    
namespace no{
    typedef int* int_ptr_t;
    typedef const int* const_int_ptr_t;
    typedef int* volatile_int_ptr_t;
    typedef some_struct_t* some_struct_ptr_t;
    typedef int* int_volatile_ptr_t;
    typedef void(*function_t)();
    typedef void (some_struct_t::*member_function_t)();   
    typedef int int_t;
} }

namespace remove_volatile{
namespace before{

    typedef void * volatile x1;
    typedef volatile int x2;
    typedef int* x3;
}
    
namespace after{
    typedef void * x1;
    typedef int x2;
    typedef int* x3;
} }


namespace remove_cv{
namespace before{

    typedef void * volatile x10;
    typedef void * const volatile x11;
    typedef void * const x12;
    
    typedef volatile int x20;
    typedef const volatile int x21;
    typedef const int x22;
    
    typedef int* volatile x30;
    typedef int* const volatile x31;
    typedef int* const x32;
    
    typedef void(*x40)();
}
    
namespace after{
    typedef void * x10;
    typedef void * x11;
    typedef void * x12;
    
    typedef int x20;
    typedef int x21;
    typedef int x22;
    
    typedef int* x30;
    typedef int* x31;
    typedef int* x32;
    
    typedef void(*x40)();
} }


namespace is_enum{

    enum color{ red, green, blue };
    
namespace yes{   
    typedef color COLOR;
}
    
namespace no{
    typedef int* int_ptr_t;
    typedef const int* const_int_ptr_t;
    typedef int* volatile_int_ptr_t;
    typedef some_struct_t* some_struct_ptr_t;
    typedef int* int_volatile_ptr_t;
    typedef void(*function_t)();
    typedef void (some_struct_t::*member_function_t)();   
    typedef int int_t;
} }

namespace has_trivial_constructor{
namespace yes{
    struct x{
        x(){}
    };
}
    
namespace no{
    class y{
        private: 
        y(){}
    };
} }

namespace has_public_constructor{
namespace yes{
    struct x{
        x(){}
    };
}
    
namespace no{
    class y{
        private: 
        y(){}
    };
} }

namespace has_public_destructor{
namespace yes{
    struct x{
        ~x(){}
    };
}
    
namespace no{
    class y{
        private: 
        ~y(){}
    };
} }

namespace has_trivial_copy{
namespace yes{
    struct x{
        x(const x&){}
    };
}
    
namespace no{
    class y{
        private: 
        y(const y&){}
    };
} }

namespace is_base_and_derived{
namespace yes{
    struct base{};
    struct derived : public base {};
}
    
namespace no{
    struct unrelated1{};
    struct unrelated2{};
} }

namespace has_any_non_copyconstructor{
namespace yes{
    struct x{
        x(int){}
    };
}
    
namespace no{
    class y{
        private: 
        y(){}
    };
} }

namespace is_unary_operator{

struct dummy{
    bool operator!(){ return true; }
    int operator++(){ return 0; }
    int operator+(const dummy& ){ return 0; }
};

inline int operator++( dummy& ){ return 0; }
inline int operator*( const dummy&, const dummy& ){ return 0; }

dummy& operator+=( dummy& x, const dummy& ){
    return x;
}

} 

namespace is_array{

namespace yes{
    int yes1[2];
    const int yes2[2] = {0};
    const volatile int yes3[2] = {0};
    int yes4[2][3];
}
    
namespace no{
    typedef int no1;
    typedef int* no2;
    typedef const int* no3;
    typedef const volatile int* no4;
    typedef int*const no5;
    typedef const int*volatile no6;
    typedef const volatile int*const no7;
    typedef void( * no8)( const int[2] );    
} }

namespace is_convertible{

template <class T>
struct convertible_from{     
    convertible_from(T);
};

template <class T>
struct convertible_to{ 
    operator T ();
    
};

struct base{};
    
struct other{};
    
struct derived : base {};
    
struct derived_protected : protected base {};    

struct derived_private : private base {};        

struct base2{};
    
struct middle2 : virtual base2 {};
    
struct derived2 : middle2 {};
    
enum fruit{ apple };    

template < typename source_type_, typename target_type_, int value_ >
struct tester_t{
    typedef source_type_ source_type;
    typedef target_type_ target_type;
    enum expected{ value=value_ };
};

template < typename source_type_, typename target_type_, int value_ >
struct tester_source_t{
    typedef source_type_ source_type;
    typedef target_type_ target_type;
    enum expected{ value=value_ };
    
private:
    enum { sizeof_source = sizeof( source_type ) };
};

template < typename source_type_, typename target_type_, int value_ >
struct tester_target_t{
    typedef source_type_ source_type;
    typedef target_type_ target_type;
    enum expected{ value=value_ };
    
private:
    enum { sizeof_target = sizeof( target_type ) };
};

template < typename source_type_, typename target_type_, int value_ >
struct tester_both_t{
    typedef source_type_ source_type;
    typedef target_type_ target_type;
    enum expected{ value=value_ };
    
private:
    enum { sizeof_source = sizeof( source_type ) };
    enum { sizeof_target = sizeof( target_type ) };
};

struct  x1 : public tester_t< const int *, int*, false >{};
struct  x2 : public tester_t< int *, const int*, true >{};
struct  x3 : public tester_t< const int&, int&, false >{};
struct  x4 : public tester_t< const int&, int, true >{};
struct  x5 : public tester_t< const int&, char, true >{};
struct  x6 : public tester_t< const int&, char&, false >{};
struct  x7 : public tester_t< const int&, char*, false >{};
struct  x8 : public tester_t< int&, const int&, true >{};
struct  x9 : public tester_t< int *, const int*, true >{};
struct x10 : public tester_t< int&, const int&, true >{};
struct x11 : public tester_t< float, int, true >{};
struct x12 : public tester_t< double, int, true >{};
struct x13 : public tester_t< double, float, true >{};
struct x14 : public tester_t< long, int, true >{};
struct x15 : public tester_t< int, char, true >{};
struct x16 : public tester_t< long long, int, true >{};
struct x17 : public tester_t< long long, char, true >{};
struct x18 : public tester_t< long long, float, true >{};
struct x19 : public tester_t< float, int, true >{};
struct x20 : public tester_t< float, void, false >{};
struct x21 : public tester_t< void, void, true >{};
struct x22 : public tester_t< double, void*, true >{};
struct x23 : public tester_t< double, int*, false >{};
struct x24 : public tester_t< int, int*, false >{};
struct x25 : public tester_t< const int, int*, false >{};
struct x26 : public tester_t< const int&, int*, false >{};
struct x27 : public tester_t< double*, int*, false >{};
struct x28 : public tester_source_t< convertible_to<int>, int, true >{};
struct x29 : public tester_target_t< int, convertible_to<int>, false >{};
struct x30 : public tester_source_t< convertible_to<float const&>, float, true >{};
struct x31 : public tester_target_t< float, convertible_to<float const&>, false >{};
struct x32 : public tester_source_t< convertible_to<float&>, float, true >{};
struct x33 : public tester_target_t< float, convertible_to<float&>, false >{};
struct x34 : public tester_source_t< convertible_to<char>, float, true >{};
struct x35 : public tester_target_t< float, convertible_to<char>, false >{};
struct x36 : public tester_source_t< convertible_to<char const&>, float, true >{};
struct x37 : public tester_target_t< float, convertible_to<char const&>, false >{};
struct x38 : public tester_source_t< convertible_to<char&>, float, true >{};
struct x39 : public tester_target_t< float, convertible_to<char&>, false >{};
struct x40 : public tester_source_t< convertible_to<char>, char, true >{};
struct x41 : public tester_source_t< convertible_to<char const&>, char, true >{};
struct x42 : public tester_source_t< convertible_to<char&>, char, true >{};
struct x43 : public tester_source_t< convertible_to<float>, float&, true >{};
struct x44 : public tester_source_t< convertible_to<float>, float const&, true >{};
struct x45 : public tester_source_t< convertible_to<float&>, float&, true >{};
struct x46 : public tester_source_t< convertible_to<float const&>, float const&, true >{};
struct x47 : public tester_source_t< convertible_to<float const&>, float&, false >{};
struct x48 : public tester_target_t< float, convertible_from<float>, true >{};
struct x49 : public tester_target_t< float, convertible_from<float const&>, true >{};
struct x50 : public tester_target_t< float, convertible_from<float&>, true >{};
struct x51 : public tester_target_t< float, convertible_from<char>, true >{};
struct x52 : public tester_target_t< float, convertible_from<char const&>, true >{};
struct x53 : public tester_target_t< float, convertible_from<char&>, false >{};
struct x54 : public tester_target_t< char, convertible_from<char>, true >{};
struct x55 : public tester_target_t< char, convertible_from<char const&>, true >{};
struct x56 : public tester_target_t< char, convertible_from<char&>, true >{};
struct x57 : public tester_target_t< float&, convertible_from<float> , true >{};
struct x58 : public tester_target_t< float const&, convertible_from<float> , true >{};
struct x59 : public tester_target_t< float&, convertible_from<float&> , true >{};
struct x60 : public tester_target_t< float const&, convertible_from<float const&>, true >{};
struct x61 : public tester_target_t< float&, convertible_from<float const&>, true >{};
struct x62 : public tester_target_t< int,  convertible_from<int>, true >{};
struct x63 : public tester_t< const int*, int[3], false >{};
struct x64 : public tester_t< int(&)[4], const int*, true >{};
struct x65 : public tester_t< int(&)(int), int(*)(int), true >{};
struct x66 : public tester_t< int[2], int*, true >{};
struct x67 : public tester_t< int[2], const int*, true >{};
struct x68 : public tester_t< const int[2], int*, false >{};
struct x69 : public tester_t< int*, int[3], false >{};
struct x70 : public tester_t< float, int&, false >{};
struct x71 : public tester_t< float, const int&, true >{};
struct x72 : public tester_t< other, void*, true >{};
struct x73 : public tester_t< int, void*, true >{};
struct x74 : public tester_t< fruit, void*, true >{};
struct x75 : public tester_t< other, int*, false >{};
struct x76 : public tester_t< other*, int*, false >{};
struct x77 : public tester_t< fruit, int, true >{};   
struct x78 : public tester_t< fruit, double, true >{};
struct x79 : public tester_t< fruit, char, true >{};
struct x80 : public tester_t< fruit, wchar_t, true >{};
struct x81 : public tester_t< derived, base, true >{};   
struct x82 : public tester_t< derived, derived, true >{};
struct x83 : public tester_t< base, base, true >{};
struct x84 : public tester_t< base, derived, false >{};
struct x85 : public tester_t< other, base, false >{};  
struct x86 : public tester_t< middle2, base2, true >{};
struct x87 : public tester_t< derived2, base2, true >{};   
struct x88 : public tester_t< derived*, base*, true >{};
struct x89 : public tester_t< base*, derived*, false >{};
struct x90 : public tester_t< derived&, base&, true >{};
struct x91 : public tester_t< base&, derived&, false >{};
struct x92 : public tester_t< const derived*, const base*, true >{};
struct x93 : public tester_t< const base*, const derived*, false >{};
struct x94 : public tester_t< const derived&, const base&, true >{};
struct x95 : public tester_t< const base&, const derived&, false >{};
struct x96 : public tester_t< derived_private, base, false >{};   
struct x97 : public tester_t< derived_protected, base, true >{};
struct x98 : public tester_t< derived_protected, derived_private, false >{};



// : public tester_t< test_abc3, const test_abc1&, true >{};
// : public tester_t< non_int_pointer, void*, true >{};
// : public tester_t< test_abc1&, test_abc2&, false >{};
// : public tester_t< test_abc1&, int_constructible, false >{};
// : public tester_t< int_constructible, test_abc1&, false >{};
// : public tester_t< test_abc1&, test_abc2, false >{};
 
//~  : public tester_t< polymorphic_derived1,polymorphic_base, true >{};
//~  : public tester_t< polymorphic_derived2,polymorphic_base, true >{};
//~  : public tester_t< polymorphic_base,polymorphic_derived1, false >{};
//~  : public tester_t< polymorphic_base,polymorphic_derived2, false >{};
//~ #ifndef BOOST_NO_IS_ABSTRACT
//~  : public tester_t< test_abc1,test_abc1, false >{};
//~  : public tester_t< Base,test_abc1, false >{};
//~  : public tester_t< polymorphic_derived2,test_abc1, false >{};
//~  : public tester_t< int,test_abc1, false >{};
//~ #endif
   
 
}



















