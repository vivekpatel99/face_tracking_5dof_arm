# Created by viv at 12.04.19

from lib.gpio.regBlock import RegBlock
import config

#--setup dma transfers
#--write cam data to 640x480 fb
zybo_dma  = RegBlock(config.CORE_BASE, 0x100)
img_dma   = RegBlock(config.IMG_BASE, 0x100)
video_dma = RegBlock(config.VID_BASE, 0x100)

servo     = RegBlock(config.SERVO_REG, 0x100)
video     = RegBlock(config.VID_REG, 0x100)
zybo      = RegBlock(config.CORE_REG, 0x100)

fb0 = RegBlock(config.FB0,1843200)
fb1 = RegBlock(config.FB1,307200)
fb2 = RegBlock(config.FB2,307200)

video_dma.set_u32(6,0)
video_dma.set_u32(4,0)   #wr
video_dma.set_u32(5,config.FB0) #rd   --> full size screen to hdmi
video_dma.set_u32(7,2)
video_dma.set_u32(8,0)        #wr
video_dma.set_u32(9,config.FB0_size) #rd
video_dma.set_u32(0x0D,0x00D00010)
video_dma.set_u32(6,0x10300)

# config cam buffer
zybo_dma.set_u32(6,0)
zybo_dma.set_u32(4,config.FB1) #wr   --> image input from camera
zybo_dma.set_u32(5,0)   #rd
zybo_dma.set_u32(7,2)
zybo_dma.set_u32(8,config.FB1_size) #wr
zybo_dma.set_u32(0x0D,0x00D00010)
zybo_dma.set_u32(6,0x10003)

# config image buffer  --> image output to hdmi
img_dma.set_u32(6,0)
img_dma.set_u32(4,0)   #wr
img_dma.set_u32(5,config.FB1) #rd
img_dma.set_u32(7,2)
img_dma.set_u32(9,config.FB1_size)
img_dma.set_u32(0x0D,0x00D00010)
img_dma.set_u32(6,0x10300)

#--set the picture-in-picture values
video.set_u32(0,3)
video.set_u32(4,0x100)
video.set_u32(5,3)
video.set_u32(6,640)
video.set_u32(7,480)

# for r in range(0, 16):
#     print("zdma %2x:   %08x     vdma   %08x  idma   %08x  vreg %08x" % (r , zybo_dma.get_u32(r),video_dma.get_u32(r),img_dma.get_u32(r),video.get_u32(r)))
#
# for r in range(0, 460800):
#     fb0.set_u32(r,0xCC00FF00)
# for r in range(0, 76800):
#     fb2.set_u32(r,0xFC00FF00)