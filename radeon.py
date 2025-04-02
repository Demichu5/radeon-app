import pyray as pr
import sys, os

import information as inf
import color as c

WIDTH = 1280
HEIGHT = 720
scene = "home"
current_version = "None"

pr.init_window(WIDTH, HEIGHT, "GPU software")
pr.set_target_fps(30)
i = 20
bg1 = pr.load_texture("bg1.png")
bg2 = pr.load_texture("bg2.png")
bg3 = pr.load_texture("bg3.png")

gpuTemp = inf.gpuTemp()
gpuVram = inf.gpuVram()
gpuUtil = inf.gpuUTIL()
gpuFans = inf.gpuFans()
gpuClc = inf.gpuClock()
gpuVolt = inf.gpuVolt()
cpuLoad = inf.cpuUtil()
memLoad = inf.memLoad()


def windowAppStatus(x, y):
    global current_version

    pr.draw_rectangle(x, y, 304, 32, pr.BLACK)
    pr.draw_text("App Version", x+16, y+4, 24, pr.WHITE)
    pr.draw_rectangle(x, y+32, 304, 80, c.GRAY1)
    pr.draw_text("Current Version", x+24, y+44, 14, c.GRAY3)
    pr.draw_text(inf.APP_VERSION, x+56, y+64, 20, pr.WHITE)
    pr.draw_text("Status", x+196, y+44, 14, c.GRAY3)
    pr.draw_text(current_version, x+164, y+64, 20, pr.WHITE)

    mouseX = pr.get_mouse_x()
    mouseY = pr.get_mouse_y()

    pr.draw_rectangle(x, y+112, 304, 40, c.GRAY2)
    pr.draw_text("Check for Updates", x+56, y+120, 20, c.GRAY3)
    checkCollison = pr.check_collision_point_rec((mouseX, mouseY), pr.Rectangle(x, y+112, 304, 40))
    if(checkCollison):
        pr.draw_rectangle(x, y+112, 304, 40, c.GRAY3)
        pr.draw_text("Check for Updates", x+56, y+120, 20, pr.WHITE)
        if((pr.is_mouse_button_pressed(pr.MouseButton.MOUSE_BUTTON_LEFT))and(checkCollison)):
            current_version = str(inf.checkUpdate())

def windowAppHardware(x, y):
    pr.draw_rectangle(x, y, 304, 32, pr.BLACK)
    pr.draw_text("Hardware", x+16, y+4, 24, pr.WHITE)
    pr.draw_rectangle(x, y+32, 304, 80, c.GRAY1)
    #pr.draw_rectangle(x, y+112, 304, 40, c.GRAY3)
    pr.draw_text("CPU", x+12, y+44, 20, c.GRAY3)
    pr.draw_text(str(inf.getCpuModel()), x+64, y+44, 20, pr.WHITE)
    pr.draw_text("GPU", x+12, y+72, 20, c.GRAY3)
    pr.draw_text(str(inf.getGpuModel()), x+64, y+72, 20, pr.WHITE)

def windowAppDriver(x, y):
    pr.draw_rectangle(x, y, 304, 32, pr.BLACK)
    pr.draw_text("Driver Version", x+16, y+4, 24, pr.WHITE)
    pr.draw_rectangle(x, y+32, 304, 80, c.GRAY1)
    #pr.draw_rectangle(x, y+112, 304, 40, c.GRAY3)
    pr.draw_text("Driver: ", x+12, y+44, 20, c.GRAY3)
    pr.draw_text(str(inf.getGpuDriver()), x+12, y+72, 20, pr.WHITE)

def windowAppInfo(x, y):
    pr.draw_rectangle(x, y, 304, 32, pr.BLACK)
    pr.draw_text("System Information", x+16, y+4, 24, pr.WHITE)
    pr.draw_rectangle(x, y+32, 304, 128, c.GRAY1)

    pr.draw_text("Kernel Name: ", x+12, y+44, 20, c.GRAY3)
    pr.draw_text(str(inf.getKernelName()), x+152, y+44, 20, pr.WHITE)
    pr.draw_text("Kernel Ver: ", x+12, y+72, 20, c.GRAY3)
    pr.draw_text(str(inf.getKernelVer()), x+144, y+72, 20, pr.WHITE)
    pr.draw_text("RAM: ", x+12, y+100, 20, c.GRAY3)
    pr.draw_text(str(inf.getMemTotal())+" GB", x+72, y+100, 20, pr.WHITE)
    pr.draw_text("SWAP: ", x+12, y+128, 20, c.GRAY3)
    pr.draw_text(str(inf.getMemSwap())+" GB", x+84, y+128, 20, pr.WHITE)

def buttonPanel(x, y, text, size, active):
    lenght = len(text) * int(size/1.75)
    mouseX = pr.get_mouse_x()
    mouseY = pr.get_mouse_y()

    checkCollison = pr.check_collision_point_rec((mouseX, mouseY), pr.Rectangle(x, y, int(lenght*1.15), size*2))
    if(checkCollison):
        pr.draw_rectangle(x, y, lenght+16, size+16, c.GRAY2)
        pr.draw_text(text, x+8, y+8, size, c.GRAY3)
        if(active):
            pr.draw_text(text, x+8, y+8, size, pr.WHITE)
    else:
        if(active):
            pr.draw_text(text, x+8, y+8, size, pr.WHITE)
        else:
            pr.draw_text(text, x+8, y+8, size, c.GRAY3)

    if((pr.is_mouse_button_pressed(pr.MouseButton.MOUSE_BUTTON_LEFT))and(checkCollison)):
        return True

    return False

def topPanel(sceneP):
    global scene
    pr.draw_rectangle(0, 0, WIDTH, 48, c.GRAY1)
    if(buttonPanel(int(32*1), 0, "Home ", 32, False)):
        scene = "home"

    if(buttonPanel(int(32*4.5), 0, "Information", 32, False)):
        scene = "info"

    if(buttonPanel(int(32*11.5), 0, "Performance ", 32, False)):
        scene = "perf"

    if(sceneP=="home"):
        buttonPanel(int(32*1), 0, "Home", 32, True)
    elif(sceneP=="info"):
        buttonPanel(int(32*4.5), 0, "Information", 32, True)
    elif(sceneP=="perf"):
        buttonPanel(int(32*11.5), 0, "Performance", 32, True)

def homePanel():
    global i, gpuTemp, gpuVram, gpuUtil, gpuFans, gpuClc, gpuVolt, cpuLoad, memLoad
    pr.clear_background(pr.BLACK)
    pr.draw_texture(bg1, 0, 0, pr.WHITE)

    windowAppStatus(960-32, 64+32)
    windowAppHardware(960-32, 232+32)
    windowAppDriver(960-32, 360+32)
    windowAppInfo(960-32, 488+32)

    i+=1
    if(i>=30):
        gpuTemp = inf.gpuTemp()
        gpuVram = inf.gpuVram()
        gpuUtil = inf.gpuUTIL()
        gpuFans = inf.gpuFans()
        gpuClc = inf.gpuClock()
        gpuVolt = inf.gpuVolt()

        cpuLoad = inf.cpuUtil()
        memLoad = inf.memLoad()
        i=0

    createWindow(32, 64+32, "CPU", int(cpuLoad), "PERCENT (%)", c.PURPLE1)
    createWindow(224+32, 64+32, "RAM", int(memLoad), "PERCENT (%)", c.YELLOW1)
    createWindow(480, 64+32, "GPU", gpuUtil, "PERCENT (%)", c.RED1)
    createWindow(672+32, 64+32, "VRAM", gpuVram, "PERCENT (%)", c.RED1)

    createWindow(32, 64+256, "GPU TEMP", f"{gpuTemp}", "°C", c.PURPLE1)
    createWindowLower(224+32, 64+256, "FANS", f"{gpuFans}", "RPM", c.PURPLE1)
    createWindowLower(480, 64+256, "CLOCK", f"{gpuClc}", "MHz", c.YELLOW1)
    createWindowLower(672+32, 64+256, "VOLTAGE", gpuVolt, "Volt (V)", c.RED1)

def infoPanel():
    global i
    #i+=1
    if(i>=30):
        pr.clear_background(pr.BLACK)
        pr.draw_texture(bg2, 0, 0, pr.WHITE)
        createWindow(50, 50, "TEMP", f"{inf.gpuTemp()}", "percent", c.PURPLE1)
        createWindow(250, 50, "VRAM", f"{inf.gpuVram()}", "percent", c.YELLOW1)
        createWindow(450, 50, "GPU", inf.gpuUTIL(), "percent", c.RED1)
        i = 0

def perfPanel():
    pr.clear_background(pr.BLACK)
    pr.draw_texture(bg3, 0, 0, pr.WHITE)
    pr.draw_text("WORK IN PROGRESS", 128, 256, 96, c.RED2)

def createWindow(x, y, name, value, information, color):
    pr.draw_rectangle(x, y, 192, 192, c.GRAY1)
    pr.draw_text(name, x+16, y+16, 24, c.GRAY2)
    pr.draw_text(str(value), x+16, y+64, 64, color)
    pr.draw_text(information, x+16, y+152, 24, c.GRAY3)

    pr.draw_rectangle(x+112, y+58, 56, 68, c.GRAY2)
    pr.draw_rectangle(x+116, y+62, 48, 60, c.GRAY3)
    if(int(value)//10)==1:
        pr.draw_rectangle(x+116, y+116, 48, 6, c.RED1)
    elif(int(value)//10)==2:
        pr.draw_rectangle(x+116, y+110, 48, 12, c.RED1)
    elif(int(value)//10)==3:
        pr.draw_rectangle(x+116, y+104, 48, 18, c.RED1)
    elif(int(value)//10)==4:
        pr.draw_rectangle(x+116, y+98, 48, 24, c.RED1)
    elif(int(value)//10)==5:
        pr.draw_rectangle(x+116, y+92, 48, 30, c.RED1)
    elif(int(value)//10)==6:
        pr.draw_rectangle(x+116, y+86, 48, 36, c.RED1)
    elif(int(value)//10)==7:
        pr.draw_rectangle(x+116, y+80, 48, 42, c.RED1)
    elif(int(value)//10)==8:
        pr.draw_rectangle(x+116, y+74, 48, 48, c.RED1)
    elif(int(value)//10)==9:
        pr.draw_rectangle(x+116, y+68, 48, 54, c.RED1)
    elif(int(value)//10)==10:
        pr.draw_rectangle(x+116, y+62, 48, 60, c.RED1)

    pr.draw_rectangle(x+116, y+118, 48, 2, c.GRAY2)
    pr.draw_rectangle(x+116, y+110, 48, 2, c.GRAY2)
    pr.draw_rectangle(x+116, y+102, 48, 2, c.GRAY2)
    pr.draw_rectangle(x+116, y+94, 48, 2, c.GRAY2)
    pr.draw_rectangle(x+116, y+86, 48, 2, c.GRAY2)
    pr.draw_rectangle(x+116, y+78, 48, 2, c.GRAY2)
    pr.draw_rectangle(x+116, y+70, 48, 2, c.GRAY2)
    pr.draw_rectangle(x+116, y+62, 48, 2, c.GRAY2)

def createWindowLower(x, y, name, value, information, color):
    pr.draw_rectangle(x, y, 192, 192, c.GRAY1)
    pr.draw_text(name, x+16, y+16, 24, c.GRAY2)
    pr.draw_text(str(value), x+16, y+64, 64, color)
    pr.draw_text(information, x+16, y+152, 24, c.GRAY3)

current_version = str(inf.checkUpdate())

while(not(pr.window_should_close())):
    pr.begin_drawing()

    if(scene=="home"):
        homePanel()

    if(scene=="info"):
        infoPanel()

    if(scene=="perf"):
        perfPanel()
        i+=10

    topPanel(scene)

    if(i>=10000):
        i = 50

    pr.end_drawing()

pr.unload_texture(bg1)
pr.unload_texture(bg2)
pr.unload_texture(bg3)
pr.close_window()
