/*
* @Author: vivekpatel99
* @Date:   2018-10-07 17:42:48
* @Last Modified by:   vivekpatel99
* @Last Modified time: 2018-10-07 17:56:35




g++ def.cpp -o def.out

g++ -fPIC -O2 -c def.cpp
g++ -shared define.o -o define.so

swig -python def.i
g++ -fPIC -O2 -c def.cpp def_wrap.c -I/usr/local/lib/python3.4/

*/
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/mman.h>
#include <fcntl.h>

//#include <iostream>
#include <linux/ioctl.h>
#include <linux/types.h>
#include <sys/ioctl.h>
#include <string.h>
//#include <fstream>
//#include <string>

//#include <png.h>

#include "define.h"

unsigned int  *ptr_vdma_3;


/*****************************************************************************/
void platform_Init()
{

    int fd_frbuf,fd_frbuf_2,fd_frbuf_3,fd_frbuf_4;
    unsigned int ALL_DISP_ADDRESS = (HORIZONTAL_PIXELS*VERTICAL_LINES*PIXEL_NUM_OF_BYTES);
    ALL_DISP_SMALL = (HORIZ_PIXELS_SMALL*VERT_LINES_SMALL*PIXEL_NUM_OF_BYTES);

    /******************************frame buffer mapping*******************************/
             fd_frbuf = open("/dev/fb0", O_RDWR|O_SYNC);
                 if (fd_frbuf < 1) {
                    printf("Invalid fb0 device file\n");
                }
            ptr_frbuf = (unsigned char*)mmap(NULL, ALL_DISP_ADDRESS, PROT_READ|PROT_WRITE, MAP_SHARED, fd_frbuf, 0);
            printf("frame buff 1 virtual address: 0x%08x \n",ptr_frbuf);
            memset(ptr_frbuf, 50, ALL_DISP_ADDRESS);

    /******************************frame buffer 2 mapping*******************************/
             fd_frbuf_2 = open("/dev/fb1", O_RDWR|O_SYNC);
                 if (fd_frbuf_2 < 1) {
                    printf("Invalid fb1 device file\n");
                }
            ptr_frbuf_2 = (unsigned char*)mmap(NULL, ALL_DISP_SMALL, PROT_READ|PROT_WRITE, MAP_SHARED, fd_frbuf_2, 0);
            printf("frame buff 2 virtual address: 0x%08x \n",ptr_frbuf_2);
            memset(ptr_frbuf_2, 200, ALL_DISP_SMALL);

    /******************************frame buffer 3 mapping*******************************/
             fd_frbuf_3 = open("/dev/fb2", O_RDWR|O_SYNC);
                 if (fd_frbuf_3 < 1) {
                    printf("Invalid fb2 device file\n");
                }
            ptr_frbuf_3 = (unsigned char*)mmap(NULL, ALL_DISP_SMALL, PROT_READ|PROT_WRITE, MAP_SHARED, fd_frbuf_3, 0);
            printf("frame buff 3 virtual address: 0x%08x \n",ptr_frbuf_3);
            memset(ptr_frbuf_3, 0, ALL_DISP_SMALL);
    /******************************frame buffer 3 mapping*******************************/
            fd_frbuf_4 = open("/dev/fb3", O_RDWR|O_SYNC);
                 if (fd_frbuf_4 < 1) {
                       printf("Invalid fb3 device file\n");
                    }
             ptr_frbuf_4 = (unsigned char*)mmap(NULL, ALL_DISP_SMALL, PROT_READ|PROT_WRITE, MAP_SHARED, fd_frbuf_4, 0);
             printf("frame buff 4 virtual address: 0x%08x \n",ptr_frbuf_4);
             memset(ptr_frbuf_4, 0, ALL_DISP_SMALL);
    /******************************vdma config********************************************/

   int fd_vdma = open("/dev/mem", O_RDWR|O_SYNC);	// open uiox device for vdma access
    if (fd_vdma < 1) {
        printf("Invalid mem device file\n");
    }
//     mmap the vdma device for vdma access

    unsigned int *ptr_vdma;
    ptr_vdma = (unsigned int*)mmap(NULL, VDMA_MAP_SIZE, PROT_READ|PROT_WRITE, MAP_SHARED, fd_vdma, VDMA_ADDR);
    printf("DMA 1 virtual address: 0x%08x \n",ptr_vdma);

    *(ptr_vdma+5) = FRBUF_ADDR_0;
    *(ptr_vdma+7) = 2;  // use internal fifos to trigger xfer
    *(ptr_vdma+8) = 20480;
    *(ptr_vdma+6) = 0x10300;  // turn vesa master xfer on
    *(ptr_vdma+0x0D) = 200;  // no. FIFO threshhold .. max.. 240

   printf("vdma_configuration end .... \n");

   /********************************2nd vdma config************************************/


   ptr_vdma_2 = (unsigned int*)mmap(NULL, VDMA_MAP_SIZE, PROT_READ|PROT_WRITE, MAP_SHARED, fd_vdma, VDMA_ADDR_2);
    printf("RTC virtual address: 0x%08x \n",ptr_vdma_2);

    *(ptr_vdma_2+5) = FRBUF_ADDR_1;
    *(ptr_vdma_2+4) = FRBUF_ADDR_1;
    *(ptr_vdma_2+7) = 2;  // use internal fifos to trigger xfer
    *(ptr_vdma_2+8) = ((ALL_DISP_SMALL/128)-1);  // ring buffer size
    *(ptr_vdma_2+6) = 0x00010300;     // enable read transfers, continuous mode

    printf("RTC_configuration end .... \n");

    /******************************** config DMA bypass************************************/
   unsigned int *ptr_vdma_4;
    ptr_vdma_4 = (unsigned int*)mmap(NULL, VDMA_MAP_SIZE, PROT_READ|PROT_WRITE, MAP_SHARED, fd_vdma, VDMA_BYPASS);
    printf("DMA_RTC_bypass virtual address: 0x%08x \n",ptr_vdma_4);
    *(ptr_vdma_4+0x0E) = (1<<30); //DMA_RTC_bypass
    printf("DMA_RTC_bypass configuration end .... \n");
   /******************************** config for child window size ************************************/

    unsigned int *ptr_vdma_3;
    ptr_vdma_3 = (unsigned int*)mmap(NULL, VDMA_MAP_SIZE, PROT_READ|PROT_WRITE, MAP_SHARED, fd_vdma, VDMA_INSERT);
    printf("RTC_small window virtual address: 0x%08x \n",ptr_vdma_3);

    //*(ptr_vdma_3+9) = (100 << 16) + ( 640+100); // x0<<16 +  x1
    //*(ptr_vdma_3+0x0A) = (200 << 16)+  ( 480+200); // y0<<16 +  y1

    *(ptr_vdma_3+6) = (75 << 16) + (HORIZ_PIXELS_SMALL+75); // x0<<16 +  x1
    *(ptr_vdma_3+7) = (150 << 16)+  (VERT_LINES_SMALL+150); // y0<<16 +  y1
    *(ptr_vdma_3+5) = 0x70B;//rgb565 and insertion enable
     printf("RTC_small window configuration end .... \n");

        /******* usb cam device *************/
    fd_usb_cam = open("/dev/video0",O_RDWR);
    if(fd_usb_cam < 0){
        printf("Failed to open video0 device ");
    }

   //  close(fd_vdma);
  //  int close(fd_frbuf);
   // int close(fd_frbuf_2);
   // int close(fd_frbuf_3);
//return ptr_frbuf, ptr_frbuf_2, ptr_frbuf_3, ptr_frbuf_4, ptr_vdma, ptr_vdma_2, ptr_vdma_3, ptr_vdma_4;
}

int main(){
platform_Init();
}


