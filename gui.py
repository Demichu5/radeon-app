import pyray as pr
import color as clr
import backend as gpu

CURRENT_VERSION_APP = "1.0.0"
currentVersion = str(gpu.checkUpdate())

def createButton(posX, posY, recX, recY, text, textSize, active, padding=8, recColor=clr.GRAY1, textColor1=clr.GRAY3, textColor2=clr.GRAY3):
    mouseX = pr.get_mouse_x()
    mouseY = pr.get_mouse_y()

    pr.draw_rectangle(posX, posY, recX, recY, recColor)
    checkCollison = pr.check_collision_point_rec((mouseX, mouseY), pr.Rectangle(posX, posY, recX, recY))
    if(checkCollison):
        pr.draw_rectangle(posX, posY, recX, recY, clr.GRAY2)
        pr.draw_text(text, posX+padding, posY+8, textSize, textColor1)
        if(active):
            pr.draw_text(text, posX+padding, posY+8, textSize, pr.WHITE)
    else:
        if(active):
            pr.draw_text(text, posX+padding, posY+8, textSize, pr.WHITE)
        else:
            pr.draw_text(text, posX+padding, posY+8, textSize, textColor2)

    if(pr.is_mouse_button_pressed(pr.MouseButton.MOUSE_BUTTON_LEFT)and(checkCollison)):
        return True

    return False

def createWindow(posX, posY, name, value, information, color, extension=False):
    pr.draw_rectangle(posX, posY, 192, 192, clr.GRAY1)
    pr.draw_text(name, posX+16, posY+16, 24, clr.GRAY2)
    pr.draw_text(str(value), posX+16, posY+64, 64, color)
    pr.draw_text(information, posX+16, posY+152, 24, clr.GRAY3)
    if(extension):
        pr.draw_rectangle(posX+112, posY+58, 56, 68, clr.GRAY2)
        pr.draw_rectangle(posX+116, posY+62, 48, 60, clr.GRAY3)
        if(int(value)//10)==1:
            pr.draw_rectangle(posX+116, posY+116, 48, 6, clr.RED1)
        elif(int(value)//10)==2:
            pr.draw_rectangle(posX+116, posY+110, 48, 12, clr.RED1)
        elif(int(value)//10)==3:
            pr.draw_rectangle(posX+116, posY+104, 48, 18, clr.RED1)
        elif(int(value)//10)==4:
            pr.draw_rectangle(posX+116, posY+98, 48, 24, clr.RED1)
        elif(int(value)//10)==5:
            pr.draw_rectangle(posX+116, posY+92, 48, 30, clr.RED1)
        elif(int(value)//10)==6:
            pr.draw_rectangle(posX+116, posY+86, 48, 36, clr.RED1)
        elif(int(value)//10)==7:
            pr.draw_rectangle(posX+116, posY+80, 48, 42, clr.RED1)
        elif(int(value)//10)==8:
            pr.draw_rectangle(posX+116, posY+74, 48, 48, clr.RED1)
        elif(int(value)//10)==9:
            pr.draw_rectangle(posX+116, posY+68, 48, 54, clr.RED1)
        elif(int(value)//10)==10:
            pr.draw_rectangle(posX+116, posY+62, 48, 60, clr.RED1)

        pr.draw_rectangle(posX+116, posY+118, 48, 2, clr.GRAY2)
        pr.draw_rectangle(posX+116, posY+110, 48, 2, clr.GRAY2)
        pr.draw_rectangle(posX+116, posY+102, 48, 2, clr.GRAY2)
        pr.draw_rectangle(posX+116, posY+94, 48, 2, clr.GRAY2)
        pr.draw_rectangle(posX+116, posY+86, 48, 2, clr.GRAY2)
        pr.draw_rectangle(posX+116, posY+78, 48, 2, clr.GRAY2)
        pr.draw_rectangle(posX+116, posY+70, 48, 2, clr.GRAY2)
        pr.draw_rectangle(posX+116, posY+62, 48, 2, clr.GRAY2)

def windowAppStatus(posX, posY):
    global currentVersion

    pr.draw_rectangle(posX, posY, 304, 32, pr.BLACK)
    pr.draw_text("App Version", posX+16, posY+4, 24, pr.WHITE)
    pr.draw_rectangle(posX, posY+32, 304, 80, clr.GRAY1)
    pr.draw_text("Current Version", posX+24, posY+44, 14, clr.GRAY3)
    pr.draw_text(CURRENT_VERSION_APP, posX+56, posY+64, 20, pr.WHITE)
    pr.draw_text("Status", posX+196, posY+44, 14, clr.GRAY3)
    pr.draw_text(currentVersion, posX+164, posY+64, 20, pr.WHITE)

    #pr.draw_rectangle(posX, posY+112, 304, 40, clr.GRAY2)
    if(createButton(posX, posY+112, 304, 40, "Check for Updates", 20, False, padding=56, recColor=clr.GRAY2, textColor1=pr.WHITE, textColor2=clr.GRAY3)):
        currentVersion = str(gpu.checkUpdate())

def windowAppHardware(posX, posY):
    pr.draw_rectangle(posX, posY, 304, 32, pr.BLACK)
    pr.draw_text("Hardware", posX+16, posY+4, 24, pr.WHITE)
    pr.draw_rectangle(posX, posY+32, 304, 80, clr.GRAY1)
    #pr.draw_rectangle(posX, posY+112, 304, 40, clr.GRAY3)
    pr.draw_text("CPU", posX+12, posY+44, 20, clr.GRAY3)
    pr.draw_text(str(gpu.getCpuModel()), posX+64, posY+44, 20, pr.WHITE)
    pr.draw_text("GPU", posX+12, posY+72, 20, clr.GRAY3)
    pr.draw_text(str(gpu.getGpuModel()), posX+64, posY+72, 20, pr.WHITE)

def windowAppDriver(posX, posY):
    pr.draw_rectangle(posX, posY, 304, 32, pr.BLACK)
    pr.draw_text("Driver Version", posX+16, posY+4, 24, pr.WHITE)
    pr.draw_rectangle(posX, posY+32, 304, 80, clr.GRAY1)
    #pr.draw_rectangle(posX, posY+112, 304, 40, clr.GRAY3)
    pr.draw_text("Driver: ", posX+12, posY+44, 20, clr.GRAY3)
    pr.draw_text(str(gpu.getGpuDriver()), posX+12, posY+72, 20, pr.WHITE)

def windowAppInfo(posX, posY):
    pr.draw_rectangle(posX, posY, 304, 32, pr.BLACK)
    pr.draw_text("System Information", posX+16, posY+4, 24, pr.WHITE)
    pr.draw_rectangle(posX, posY+32, 304, 128, clr.GRAY1)

    pr.draw_text("Kernel Name: ", posX+12, posY+44, 20, clr.GRAY3)
    pr.draw_text(str(gpu.getKernelName()), posX+152, posY+44, 20, pr.WHITE)
    pr.draw_text("Kernel Ver: ", posX+12, posY+72, 20, clr.GRAY3)
    pr.draw_text(str(gpu.getKernelVer()), posX+144, posY+72, 20, pr.WHITE)
    pr.draw_text("RAM: ", posX+12, posY+100, 20, clr.GRAY3)
    pr.draw_text(str(gpu.getMemTotal())+" GB", posX+72, posY+100, 20, pr.WHITE)
    pr.draw_text("SWAP: ", posX+12, posY+128, 20, clr.GRAY3)
    pr.draw_text(str(gpu.getMemSwap())+" GB", posX+84, posY+128, 20, pr.WHITE)
