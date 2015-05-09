#pragma once

#include "neon_traits.h"

namespace neon
{
    template<int V> struct imm
    {
	static const int val = V;
    };

    template<typename T>
    size_t len(T){return traits::num<T>::val;}

    template<typename T>
    typename traits::vec<T,1>::type build(T a0)
    {
	typename traits::U<T,1>::type u = {a0};
	return u.vec;
    }

    template<typename T>
    typename traits::vec<T,2>::type build(T a0, T a1)
    {
	typename traits::U<T,2>::type u = {a0,a1};
	return u.vec;
    }

    template<typename T>
    typename traits::vec<T,4>::type build(T a0, T a1, T a2, T a3)
    {
	typename traits::U<T,4>::type u = {a0,a1,a2,a3};
	return u.vec;
    }

    template<typename T>
    typename traits::vec<T,8>::type build(T a0, T a1, T a2, T a3, T a4, T a5, T a6, T a7)
    {
	typename traits::U<T,8>::type u = {a0,a1,a2,a3,a4,a5,a6,a7};
	return u.vec;
    }

    template<typename T>
    typename traits::vec<T,16>::type build(T a0, T a1, T a2, T a3, T a4, T a5, T a6, T a7,
					   T b0, T b1, T b2, T b3, T b4, T b5, T b6, T b7)
    {
	typename traits::U<T,16>::type u = {a0,a1,a2,a3,a4,a5,a6,a7,
					    b0,b1,b2,b3,b4,b5,b6,b7};
	return u.vec;
    }


    template<typename T>
    typename traits::elem<T>::type nth(T vec, int idx)
    {
	typename neon::traits::UU<T>::type u = {vec};
	return u.a[idx];
    }

    template<typename T, int idx>
    typename traits::elem<T>::type nth(T vec, imm<idx>)
    {
	typename neon::traits::UU<T>::type u = {vec};
	return u.a[idx];
    }

    template<int idx, typename T>
    typename traits::elem<T>::type get(T vec)
    {
	typename neon::traits::UU<T>::type u = {vec};
	return u.a[idx];
    }


    template<typename T, int N, typename S>
    typename traits::vec<T,N>::type as(S x)
    {
	return (typename traits::vec<T,N>::type)(x);
    }

}
