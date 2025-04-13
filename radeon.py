# Biblioteki
import pyray as pr
import backend as gpu
import color as clr
import gui as gui

#Zmienne stale
WIDTH = 1280
HEIGHT = 720

WIDTH_ERROR = 640
HEIGHT_ERROR = 360

FPS = 30

#Funkcje
def homePanel():
    global i, gpuTemp, gpuVram, gpuUtil, gpuFans, gpuClc, gpuVolt, cpuLoad, memLoad
    pr.clear_background(pr.BLACK)
    pr.draw_texture(bg1, 0, 0, pr.WHITE)

    gui.windowAppStatus(960-32, 64+32)
    gui.windowAppHardware(960-32, 232+32)
    gui.windowAppDriver(960-32, 360+32)
    gui.windowAppInfo(960-32, 488+32)

    i+=1
    if(i>=30):
        gpuTemp = gpu.gpuTemp()
        gpuVram = gpu.gpuVram()
        gpuUtil = gpu.gpuUTIL()
        gpuFans = gpu.gpuFans()
        gpuClc = gpu.gpuClock()
        gpuVolt = gpu.gpuVolt()

        cpuLoad = gpu.cpuUtil()
        memLoad = gpu.memLoad()
        i=0

    gui.createWindow(32, 64+32, "CPU", int(cpuLoad), "PERCENT (%)", clr.PURPLE1, True)
    gui.createWindow(224+32, 64+32, "RAM", int(memLoad), "PERCENT (%)", clr.YELLOW1, True)
    gui.createWindow(480, 64+32, "GPU", gpuUtil, "PERCENT (%)", clr.RED1, True)
    gui.createWindow(672+32, 64+32, "VRAM", gpuVram, "PERCENT (%)", clr.RED1, True)

    gui.createWindow(32, 64+256, "GPU TEMP", f"{gpuTemp}", "°C", clr.PURPLE1, True)
    gui.createWindow(224+32, 64+256, "FANS", f"{gpuFans}", "RPM", clr.PURPLE1)
    gui.createWindow(480, 64+256, "CLOCK", f"{gpuClc}", "MHz", clr.YELLOW1)
    gui.createWindow(672+32, 64+256, "VOLTAGE", gpuVolt, "Volt (V)", clr.RED1)


def perfPanel():
    pr.clear_background(pr.BLACK)
    pr.draw_texture(bg2, 0, 0, pr.WHITE)

def infoPanel():
    pr.clear_background(pr.BLACK)
    pr.draw_texture(bg3, 0, 0, pr.WHITE)

def topPanel(scene):
    global activeScene
    pr.draw_rectangle(0, 0, WIDTH, 48, clr.GRAY1)
    #gui.createButton(32, 0, 96, 48, "Home", 32, True)
    if(gui.createButton(32, 0, 96, 48, "Home", 32, False)):
        activeScene = "home"
    if(gui.createButton(144, 0, 224, 48, "Performance", 32, False)):
        activeScene = "perf"
    if(gui.createButton(384, 0, 196, 48, "Information", 32, False)):
        activeScene = "info"

    if(activeScene == "home"):
        gui.createButton(32, 0, 96, 48, "Home", 32, True)
    elif(activeScene == "perf"):
        gui.createButton(144, 0, 224, 48, "Performance", 32, True)
    elif(activeScene == "info"):
        gui.createButton(384, 0, 196, 48, "Information", 32, True)

#Inicjacja
if(gpu.checkCompatibility()):
    pr.init_window(WIDTH, HEIGHT, "GPU Software")
    pr.set_target_fps(FPS)
else:
    pr.init_window(WIDTH_ERROR, HEIGHT_ERROR, "GPU Software Error")
    pr.set_target_fps(FPS)
    while(not(pr.window_should_close())):
        pr.begin_drawing()
        pr.clear_background(pr.GRAY)
        pr.draw_text("Unsupported GPU", 32, 128, 64, pr.WHITE)
        pr.end_drawing()
    pr.close_window()

#Zmienne Globalne
activeScene = "perf"
bg1 = pr.load_texture("/home/michu/Programming/Python/off-topic/radeon-app/bg1.png")
bg2 = pr.load_texture("/home/michu/Programming/Python/off-topic/radeon-app/bg2.png")
bg3 = pr.load_texture("/home/michu/Programming/Python/off-topic/radeon-app/bg3.png")
i=25

gpuTemp = gpu.gpuTemp()
gpuVram = gpu.gpuVram()
gpuUtil = gpu.gpuUTIL()
gpuFans = gpu.gpuFans()
gpuClc = gpu.gpuClock()
gpuVolt = gpu.gpuVolt()
cpuLoad = gpu.cpuUtil()
memLoad = gpu.memLoad()

#Pętla główna
while(not(pr.window_should_close())):
    pr.begin_drawing()

    if(activeScene=="home"):
        homePanel()

    if(activeScene=="perf"):
        perfPanel()

    if(activeScene=="info"):
        infoPanel()

    topPanel(activeScene)

    pr.end_drawing()

pr.unload_texture(bg1)
pr.unload_texture(bg2)
pr.unload_texture(bg3)
pr.close_window()
