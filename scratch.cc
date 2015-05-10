#include <stdio.h>
#include <stdlib.h>
#include "neon_tools.h"

template<typename T>
void print(const char * fmt, T vec)
{
    for(size_t i = 0; i < neon::len(vec); ++i)
    {
	printf(fmt, neon::nth(vec,i) );
    }
}


int main(int argc, char *argv[])
{
     (void) argc; (void) argv;

     auto x = neon::build<uint16_t>(0x1111,0x2222,0x0,0x0);
     print(" %04hx", x); printf("\n");
     printf("1: %04X  %04X\n"
	    , neon::get<1>(x)
	    , vget_lane_u16(x,1)
	    );


     uint16x4_t xx = {0};
     xx = vset_lane_u16(0x1111, xx, 0);
     xx = vset_lane_u16(0x2222, xx, 1);
     print(" %04hx", xx); printf("\n");

     {
	 int i = 0;
	 neon::for_each(xx,
			[&i](uint16_t a)->void
			{
			    printf("%d: %04hx\n", i++, a);
			}
			);
     }

     {
	 neon::apply<void>
	     ([](uint16_t a0,uint16_t a1,uint16_t a2,uint16_t a3)->void
	     {
		 printf("xx: %04hx %04hx %04hx %04hx\n", a0, a1, a2, a3);
	     }, xx);
     }

     auto y = vreinterpret_u64_u16(x);
     print(" %016llx", y); printf("\n");

     auto yy = vcombine_u64(y,y);

     for( size_t i = 0; i < 5; ++i)
     {
	 int bit_shift = i*2*8;

	 auto sh = neon::build<int64_t>(bit_shift , bit_shift - 64);

	 auto _y = vshlq_u64(yy,sh);

	 printf("%2d: ", bit_shift);
	 print(" %016llx", _y);
	 printf(" --");
	 print(" %04hx", vreinterpretq_u16_u64(_y) );

	 printf("\n");
     }

     return 0;
}

