%module def
%{
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/mman.h>
#include <fcntl.h>

#include <linux/ioctl.h>
#include <linux/types.h>
#include <sys/ioctl.h>
#include <string.h>


#include "define.h"

extern void platform_Init();
%}



extern void platform_Init();
