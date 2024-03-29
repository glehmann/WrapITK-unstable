// Copyright 2004 Roman Yakovenko.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)

#ifndef __bit_fields_hpp__
#define __bit_fields_hpp__

namespace bit_fields{

struct fields_t{
    unsigned int x : 1;
    unsigned int y : 7;
    unsigned int z;
};

}

#endif//__bit_fields_hpp__