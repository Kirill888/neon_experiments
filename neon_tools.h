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

    namespace detail
    {
	template<int N> struct impl;

	template<>struct impl<1>
	{
	    template<typename T, typename Function>
	    static void for_each(T vec, Function f)
	    {
		f( get<0>(vec) );
	    }

	    template<typename R, typename T, typename Function>
	    static R apply(Function f, T vec)
	    {
		return f( get<0>(vec) );
	    }
	};

	template<>struct impl<2>
	{
	    template<typename T, typename Function>
	    static void for_each(T vec, Function f)
	    {
		f( get<0>(vec));
		f( get<1>(vec));
	    }

	    template<typename R, typename T, typename Function>
	    static R apply(Function f, T vec)
	    {
		return f( get<0>(vec), get<1>(vec) );
	    }
	};

	template<>struct impl<4>
	{
	    template<typename T, typename Function>
	    static void for_each(T vec, Function f)
	    {
		f( get<0>(vec)); f( get<1>(vec)); f( get<2>(vec)); f( get<3>(vec));
	    }

	    template<typename R, typename T, typename Function>
	    static R apply(Function f, T vec)
	    {
		return f( get<0>(vec), get<1>(vec), get<2>(vec), get<3>(vec) );
	    }
	};

	template<>struct impl<8>
	{
	    template<typename T, typename Function>
	    static void for_each(T vec, Function f)
	    {
		f( get<0>(vec)); f( get<1>(vec)); f( get<2>(vec)); f( get<3>(vec));
		f( get<4>(vec)); f( get<5>(vec)); f( get<6>(vec)); f( get<7>(vec));
	    }

	    template<typename R, typename T, typename Function>
	    static R apply(Function f, T vec)
	    {
		return f( get<0>(vec), get<1>(vec), get<2>(vec), get<3>(vec),
			  get<4>(vec), get<5>(vec), get<6>(vec), get<7>(vec));
	    }
	};

	template<>struct impl<16>
	{
	    template<typename T, typename Function>
	    static void for_each(T vec, Function f)
	    {
		f( get< 0>(vec)); f( get< 1>(vec)); f( get< 2>(vec)); f( get< 3>(vec));
		f( get< 4>(vec)); f( get< 5>(vec)); f( get< 6>(vec)); f( get< 7>(vec));
		f( get< 8>(vec)); f( get< 9>(vec)); f( get<10>(vec)); f( get<11>(vec));
		f( get<12>(vec)); f( get<13>(vec)); f( get<14>(vec)); f( get<15>(vec));
	    }

	    template<typename R, typename T, typename Function>
	    static R apply(Function f, T vec)
	    {
		return f( get< 0>(vec), get< 1>(vec), get< 2>(vec), get< 3>(vec),
			  get< 4>(vec), get< 5>(vec), get< 6>(vec), get< 7>(vec),
			  get< 8>(vec), get< 9>(vec), get<10>(vec), get<11>(vec),
			  get<12>(vec), get<13>(vec), get<14>(vec), get<15>(vec));
	    }
	};
    }

    template<typename T, typename Function>
    void for_each(T vec, Function f)
    {
	const int N = traits::num<T>::val;
	detail::impl<N>::template for_each(vec,f);
    }

    template<typename R, typename T, typename Function>
    R apply(Function f, T vec)
    {
	const int N = traits::num<T>::val;
	return detail::impl<N>::template apply<R>(f,vec);
    }
}
