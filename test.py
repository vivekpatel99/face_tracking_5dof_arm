import sys
from PyQt5.QtWidgets import QApplication, QWidget
import os


if __name__ == '__main__':
    from regBlock import RegBlock
    import matplotlib.pyplot as plt
    # %matplotlib inline
    import numpy as np

    FB0 = 0x1E000000
    FB1 = 0x1E280000
    FB2 = 0x1E500000
    FB3 = 0x1E780000

    FB0_size = 10240
    FB1_size = 2400

    # --related ip cores:  rtc_dma_bridge  sbus_zybo_core ---
    # dma rd to sbus_zybo_core
    # dma wr from video_core
    CORE_BASE = 0x43C00000
    CORE_REG = 0x43C10000

    # --related ip cores:  video_dma_bridge   video_core   servo_core
    # dma rd to video_core (fullscreen 1280x720 fb)
    VID_BASE = 0x83C40000
    VID_REG = 0x83C44000
    SERVO_REG = 0x83C48000

    # --related ip cores:  img_dma_bridge
    # dma rd to video_core (640x480 fb)
    IMG_BASE = 0x83C00000

    # --setup dma transfers
    # --write cam data to 640x480 fb
    zybo_dma = RegBlock(CORE_BASE, 0x100)
    img_dma = RegBlock(IMG_BASE, 0x100)
    video_dma = RegBlock(VID_BASE, 0x100)

    servo = RegBlock(SERVO_REG, 0x100)
    video = RegBlock(VID_REG, 0x100)
    zybo = RegBlock(CORE_REG, 0x100)

    fb0 = RegBlock(FB0, 1843200)
    fb1 = RegBlock(FB1, 307200)
    fb2 = RegBlock(FB2, 307200)

    video_dma.set_u32(6, 0)
    video_dma.set_u32(4, 0)  # wr
    video_dma.set_u32(5, FB0)  # rd   --> full size screen to hdmi
    video_dma.set_u32(7, 2)
    video_dma.set_u32(8, 0)  # wr
    video_dma.set_u32(9, FB0_size)  # rd
    video_dma.set_u32(0x0D, 0x00D00010)
    video_dma.set_u32(6, 0x10300)

    # config cam buffer
    zybo_dma.set_u32(6, 0)
    zybo_dma.set_u32(4, FB1)  # wr   --> image input from camera
    zybo_dma.set_u32(5, 0)  # rd
    zybo_dma.set_u32(7, 2)
    zybo_dma.set_u32(8, FB1_size)  # wr
    zybo_dma.set_u32(0x0D, 0x00D00010)
    zybo_dma.set_u32(6, 0x10003)

    # config image buffer  --> image output to hdmi
    img_dma.set_u32(6, 0)
    img_dma.set_u32(4, 0)  # wr
    img_dma.set_u32(5, FB1)  # rd
    img_dma.set_u32(7, 2)
    img_dma.set_u32(9, FB1_size)
    img_dma.set_u32(0x0D, 0x00D00010)
    img_dma.set_u32(6, 0x10300)

    # --set the picture-in-picture values
    video.set_u32(0, 3)
    video.set_u32(4, 0x100)
    video.set_u32(5, 3)
    video.set_u32(6, 640)
    video.set_u32(7, 480)

    servo.set_u32(3, 1000)
    servo.set_u32(4, -1000)
#    os.environ["fbdev"] = "/dev/fb0"
    import sys
    from PyQt5.QtWidgets import QApplication, QWidget
    from PyQt5.QtGui import QIcon
   
    class Example(QWidget):
    
        def __init__(self):
            super().__init__()
        
            self.initUI()
        
        
        def initUI(self):
        
            self.setGeometry(300, 300, 600, 320)
            self.setWindowTitle('Icon')
            self.setWindowIcon(QIcon('web.png'))        
    
            self.show()
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
