
//#include <linux/videodev2.h>


extern unsigned int  *ptr_vdma_3;

#define VDMA_MAP_SIZE           0x100//UIO-VDMA
#define VDMA_ADDR               0x43C00000
#define VDMA_ADDR_2             0x43c40000
#define VDMA_BYPASS             (0x43c40000 + (0x1000*4))
#define VDMA_INSERT             (0x43c40000 + (0x2000*4))
#define FRBUF_ADDR_0            0x1E000000
#define FRBUF_ADDR_1            0x1E280000
#define FRBUF_ADDR_2            0x1E500000
#define FRBUF_ADDR_3            0x1E780000
#define PIXEL_NUM_OF_BYTES      2
#define HORIZONTAL_PIXELS       1280
#define VERTICAL_LINES          1024
#define HORIZ_PIXELS_SMALL      640
#define VERT_LINES_SMALL        480
#define N_BUFFERS               2


int fd_usb_cam;
unsigned char *ptr_frbuf,*ptr_frbuf_2,*ptr_frbuf_3,*ptr_frbuf_4,FB_no,*RGB565_buf,*RGB888_buf;
unsigned int ALL_DISP_SMALL;
unsigned int *ptr_vdma_2;//*ptr_vdma_3; // to change the frame buffer
//v4l2_buffer bufferinfo;
