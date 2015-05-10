#pragma once

#include <arm_neon.h>
#include <inttypes.h>

namespace neon
{
    namespace traits
    {
	template<typename T, int> struct vec;
	template<typename T> struct elem;

	template<> struct vec<float,4     >{typedef float32x4_t type;};
	template<> struct vec<float,2     >{typedef float32x2_t type;};
	template<> struct elem<float32x4_t>{typedef float       type;};
	template<> struct elem<float32x2_t>{typedef float       type;};

#define MK_TRAIT(base,N)\
	template<> struct vec<base##_t,N> {typedef base##x##N##_t type;};\
	template<> struct elem<base##x##N##_t>{typedef base##_t type;};

	MK_TRAIT(uint8,  8)
	MK_TRAIT(uint8, 16)
	MK_TRAIT( int8,  8)
	MK_TRAIT( int8, 16)

	MK_TRAIT(uint16, 4)
	MK_TRAIT(uint16, 8)
	MK_TRAIT( int16, 4)
	MK_TRAIT( int16, 8)

	MK_TRAIT(uint32, 2)
	MK_TRAIT(uint32, 4)
	MK_TRAIT( int32, 2)
	MK_TRAIT( int32, 4)

	MK_TRAIT(uint64, 1)
	MK_TRAIT(uint64, 2)
	MK_TRAIT( int64, 1)
	MK_TRAIT( int64, 2)


#undef MK_TRAIT

	template<typename T>
	struct num
	{
	    static const size_t val = sizeof(T)/sizeof(typename elem<T>::type);
	};

	template<typename T, int N>
	struct U
	{
	    typedef union
	    {
		typename vec<T,N>::type vec;
		T a[N];
	    } type;
	};

	template<typename T>
	struct UU
	{
	    typedef union
	    {
		T vec;
		typename elem<T>::type a[num<T>::val];
	    } type;
	};
    }//neon::traits::
}//neon::
