#!/usr/bin/env python3

import socket
import struct
import sys
import time
import signal
import subprocess
from random import randint
import threading
from tkinter import *
from tkinter import ttk
from tkinter import font

import queue
import os.path

MYSYMFILE = "A45XT2CM.35E"      # put in your Symbol filename here

TIMEOUT = "TIMEOUT"
CR = 13
NL = 10
SKRIPT_VER = "V1.0"
BG_COLOR = "#F0F0ED"
MYSYMFILE = "A45XT2CM.35E"

class GuiApp:

    def __init__(self, master, queue, endCommand):

        # class variables
        self.bMeasureMode = False
        self.kylTempMax = 0
        self.luftTempMax = 0
        self.rpmMax = 0
        self.speedMax = 0
        self.boost = 0
        self.boostMax = 0
        self.tqMax = 0
        self.powerMax = 0
        self.batt = 0
        self.battMax = 0
        self.queue = queue
        self.main = master

        self.vKyl = StringVar()
        self.vKylPeak = StringVar()
        self.vLuft = StringVar()
        self.vLuftPeak = StringVar()
        self.vRpm = StringVar()
        self.vRpmPeak = StringVar()
        self.vSpeed = StringVar()
        self.vSpeedPeak = StringVar()
        self.vBoost = StringVar()
        self.vBoostPeak = StringVar()
        self.vBatt = StringVar()
        self.vBattPeak = StringVar()
        
        self.vTQ = StringVar()
        self.vTQPeak = StringVar()
        self.vPower = StringVar()
        self.vPowerPeak = StringVar()


        self.vAFR = StringVar()
        self.vKyl.set('0')
        self.vLuft.set('0')
        self.vKylPeak.set('0')
        self.vLuftPeak.set('0')
        self.vRpm.set('0')
        self.vRpmPeak.set('0')
        self.vSpeed.set('0')
        self.vSpeedPeak.set('0')
        self.vBoost.set('0')
        self.vBoostPeak.set('0')
        self.vBatt.set('0.0')
        self.vBattPeak.set('0.0')

        self.vAFR.set('14.7')
        self.vTQ.set('0')
        self.vTQPeak.set('0')
        self.vPower.set('0')
        self.vPowerPeak.set('0')

        self.SWVer = StringVar()
        self.SWVer.set('0')


        stest = ttk.Style()
        stest.theme_use('clam')
        stest.configure("red.test", foreground='red', background='red')

        gui_style = ttk.Style()
        gui_style.configure("My.TFrame", background= BG_COLOR)
        gui_style.configure("My.TNotebook", background= BG_COLOR)
        

        self.nbook = ttk.Notebook(self.main, style = "My.TNotebook") 
        
        self.f1 = ttk.Frame(self.nbook, style = "My.TFrame")
        self.f2 = ttk.Frame(self.nbook, style = "My.TFrame")
        self.f3 = ttk.Frame(self.nbook, style = "My.TFrame")
        self.f4 = ttk.Frame(self.nbook, style = "My.TFrame")
        self.nbook.add(self.f1, text='Sensoren 1')
        self.nbook.add(self.f2, text='Sensoren 2')
        self.nbook.add(self.f3, text='Zeit')
        self.nbook.add(self.f4, text='Status')
        #self.nbook.grid()
        self.main.bind('<Button-1>', self.mclick)

        # Set up the GUI
        self.main.wm_title("Trionic Live-Daten "+ SKRIPT_VER)

        # frame 1
        Label(self.f1,text = "Sensor", padx=5, pady=5, font=('Helvetica', '18', 'bold')).grid(row=0, column=0)
        Label(self.f1,text = "aktueller Wert", padx=5, pady=5,  font=('Helvetica', '18', 'bold')).grid(row=0, column=1)
        ttk.Separator(self.f1, orient=VERTICAL).grid(column=2, row=0, rowspan=10, sticky="ns")
        Label(self.f1,text = "Peak", padx=5, pady=5,  font=('Helvetica', '18', 'bold')).grid(row=0, column=3)
        ttk.Separator(self.f1, orient=HORIZONTAL).grid(row=1, columnspan=4, sticky="ew")

        Label(self.f1, text = "Kühltemperatur", padx=25, pady=10).grid(row=3, column=0)
        Label(self.f1, text = "Einlasstemperatur", padx=5, pady=10).grid(row=4, column=0)
        Label(self.f1, text = "Geschwindigkeit", padx=5, pady=10).grid(row=5, column=0)
        Label(self.f1, text = "Drehzahl", padx=5, pady=10).grid(row=6, column=0)
        Label(self.f1, text = "Batterie", padx=5, pady=10).grid(row=7, column=0)
        


        Label(self.f1, textvariable = self.vKyl, padx=5, pady=10).grid(row=3, column=1)
        Label(self.f1, textvariable = self.vKylPeak, padx=5, pady=10).grid(row=3, column=3)
        Label(self.f1, textvariable = self.vLuft, padx=5, pady=10).grid(row=4, column=1)
        Label(self.f1, textvariable = self.vLuftPeak, padx=5, pady=10).grid(row=4, column=3)
        Label(self.f1, textvariable = self.vSpeed, padx=5, pady=10).grid(row=5, column=1)
        Label(self.f1, textvariable = self.vSpeedPeak, padx=5, pady=10).grid(row=5, column=3)
        Label(self.f1, textvariable = self.vRpm, padx=5, pady=10).grid(row=6, column=1)
        Label(self.f1, textvariable = self.vRpmPeak, padx=5, pady=10).grid(row=6, column=3)
        Label(self.f1, textvariable = self.vBatt, padx=5, pady=10).grid(row=7, column=1)
        Label(self.f1, textvariable = self.vBattPeak, padx=5, pady=10).grid(row=7, column=3)
        ttk.Separator(self.f1, orient=HORIZONTAL).grid(row=10, columnspan=4, sticky="ew")

        Label(self.f1, text = "U/min", padx=0, pady=5).grid(row=11, column=0)

        sRed = ttk.Style()
        sRed.theme_use('clam')
        sRed.configure("red.Horizontal.TProgressbar", foreground='red', background='red')

        sGreen = ttk.Style()
        sGreen.theme_use('clam')
		self.sGreen.layout("green.Horizontal.TProgressbar",
         [('green.Horizontal.TProgressbar.trough',
           {'children': [('green.Horizontal.TProgressbar.pbar',
                          {'side': 'left', 'sticky': 'ns'}),
                         ("green.Horizontal.TProgressbar.label",
                          {"sticky": ""})],
           'sticky': 'nswe'})])
        
 
        sGreen.configure("green.Horizontal.TProgressbar", foreground='green', background='green')
		self.sGreen.configure("green.Horizontal.TProgressbar", text = "4500")

        sYellow = ttk.Style()
        sYellow.theme_use('clam')
        sYellow.configure("yellow.Horizontal.TProgressbar", foreground='yellow', background='yellow')

        self.pbRPM = ttk.Progressbar(self.f1, style="green.Horizontal.TProgressbar", orient="horizontal", length=330, mode="determinate")
        self.pbRPM["value"] = 0
        self.pbRPM["maximum"] = 7500
        self.pbRPM.grid(row=11, column=1, columnspan=3, padx=1, pady=5)
        
        
        Label(self.f1, text = "Boost", padx=0, pady=5).grid(row=12, column=0)

        self.pbBoost = ttk.Progressbar(self.f1, orient="horizontal", length=330, mode="determinate")
        # boost from -1 to 2 bar --> from 0 to 3
        self.pbBoost["value"] = 0
        self.pbBoost["maximum"] = 2
        self.pbBoost.grid(row=12, column=1, columnspan=3, padx=1, pady=5)

        

        # frame 2
        Label(self.f2,text = "Sensor", padx=5, pady=5).grid(row=0, column=0)
        Label(self.f2,text = "aktueller Wert", padx=5, pady=5).grid(row=0, column=1)
        ttk.Separator(self.f2, orient=VERTICAL).grid(column=2, row=0, rowspan=7,sticky="ns")
        Label(self.f2,text = "Peak", padx=5, pady=5).grid(row=0, column=3)
        ttk.Separator(self.f2, orient=HORIZONTAL).grid(row=1, columnspan=4, sticky="ew")

        Label(self.f2, text = "A/F Ratio", padx=31, pady=10).grid(row=3, column=0)
        Label(self.f2, text = "Boost", padx=5, pady=10).grid(row=4, column=0)
        Label(self.f2, text = "Drehmoment", padx=5, pady=10).grid(row=5, column=0)
        Label(self.f2, text = "Leistung", padx=5, pady=10).grid(row=6, column=0)
        
        Label(self.f2, textvariable = self.vAFR, padx=5, pady=10).grid(row=3, column=1)
        Label(self.f2, text = "------", padx=5, pady=10).grid(row=3, column=3)
        Label(self.f2, textvariable = self.vBoost, padx=5, pady=10).grid(row=4, column=1)
        Label(self.f2, textvariable = self.vBoostPeak, padx=5, pady=10).grid(row=4, column=3)
        Label(self.f2, textvariable = self.vTQ, padx=5, pady=10).grid(row=5, column=1)
        Label(self.f2, textvariable = self.vTQPeak, padx=5, pady=10).grid(row=5, column=3)
        Label(self.f2, textvariable = self.vPower, padx=5, pady=10).grid(row=6, column=1)
        Label(self.f2, textvariable = self.vPowerPeak, padx=5, pady=10).grid(row=6, column=3)
        ttk.Separator(self.f2, orient=HORIZONTAL).grid(row=7, columnspan=4, sticky="ew")

        Label(self.f2, text = "Boost", padx=0, pady=5).grid(row=8, column=0)

        self.pbBoost2 = ttk.Progressbar(self.f2, orient="horizontal", length=330, mode="determinate")
        # boost from -1 to 2 bar --> from 0 to 3
        self.pbBoost2["value"] = 0
        self.pbBoost2["maximum"] = 2
        self.pbBoost2.grid(row=8, column=1, columnspan=3, padx=1, pady=5)


        # frame 3
        self.vStart = IntVar()

        Label(self.f3, text = "Start bei (km/h)", pady=10).grid(row=0, column=2)

        Radiobutton(self.f3, text= "60", variable = self.vStart, value = 60, padx=5).grid(row = 1, column = 0)
        Radiobutton(self.f3, text= "80", variable = self.vStart, value = 80, padx=5).grid(row = 1, column = 1)
        Radiobutton(self.f3, text= "100", variable = self.vStart, value = 100, padx=5).grid(row = 1, column = 2)
        Radiobutton(self.f3, text= "120", variable = self.vStart, value = 120, padx=5).grid(row = 1, column = 3)
        Radiobutton(self.f3, text= "140", variable = self.vStart, value = 140, padx=5).grid(row = 1, column = 4)

        self.vStart.set(100)
        Label(self.f3, text = "Stop bei (km/h)", pady=10).grid(row=2, column=2)

        self.vStop = IntVar()
        Radiobutton(self.f3, text= "120", variable = self.vStop, value = 120).grid(row = 3, column = 0)
        Radiobutton(self.f3, text= "140", variable = self.vStop, value = 140).grid(row = 3, column = 1)
        Radiobutton(self.f3, text= "160", variable = self.vStop, value = 160).grid(row = 3, column = 2)
        Radiobutton(self.f3, text= "180", variable = self.vStop, value = 180).grid(row = 3, column = 3)
        Radiobutton(self.f3, text= "200", variable = self.vStop, value = 200, pady=5).grid(row = 3, column = 4)
        self.vStop.set(160)

        self.buttStart = Button(self.f3, text = "Start", command=self.startPressed, pady=5)
        self.buttStart.grid(row=4, column=2)
        self.vTime = StringVar()
        self.lSpeed = Label(self.f3, textvariable = self.vSpeed, padx = 5, pady=10).grid(row=5, column=2)
        self.lTime = Label(self.f3, textvariable = self.vTime, font = "Verdana 10 bold",  padx = 5, pady=10)
        self.lTime.grid(row=4, column=3, columnspan=2)
        

        # frame 4
        
        Label(self.f4, text = "Motorstatus:", padx=10, pady=10).grid(row=0, column=0)

        self.cbIdle = Checkbutton(self.f4, text="Idle", padx=10, pady=5)
        self.cbIdle.grid(row=1, column=0, sticky=W)
        self.cbCL = Checkbutton(self.f4, text="Closed Loop", padx=10, pady=5)
        self.cbCL.grid(row=2, column=0, sticky=W)
        self.cbKnock = Checkbutton(self.f4, text="Knock map", padx=10, pady=5)
        self.cbKnock.grid(row=3, column=0, sticky=W)
        self.cbWarm = Checkbutton(self.f4, text="Warmup", padx=10, pady=5)
        self.cbWarm.grid(row=4, column=0, sticky=W)
        self.cbThr = Checkbutton(self.f4, text="Throttle closed", padx=10, pady=5)
        self.cbThr.grid(row=5, column=0, sticky=W)

        self.cbCheck6 = Checkbutton(self.f4, text="Check6")
        self.cbCheck6.grid(row=1, column=1, sticky=W)
        self.cbCheck7 = Checkbutton(self.f4, text="Check7")
        self.cbCheck7.grid(row=2, column=1, sticky=W)
        self.cbCheck8 = Checkbutton(self.f4, text="Check8")
        self.cbCheck8.grid(row=3, column=1, sticky=W)
        self.cbCheck9 = Checkbutton(self.f4, text="Check9")
        self.cbCheck9.grid(row=4, column=1, sticky=W)
        self.cbCheck10 = Checkbutton(self.f4, text="Check10")
        self.cbCheck10.grid(row=5, column=1, sticky=W)
        Label(self.f4, textvariable = self.SWVer, padx=0, pady=10).grid(row=0, column=1)

        # GUI stuff end

    def mclick(self, event):
        #self.pbRPM.focus_set()
        xr = self.main.winfo_pointerx()
        yr = self.main.winfo_pointery()
        #print("Mouse clicked at", event.x, event.y, xr, yr)
        frameID = self.nbook.index(self.nbook.select())
        #print ("frame", x)

    def startShowData(self):
        self.InfoBox.destroy()
        self.nbook.grid()
        

    def showInit(self):
        ShowStr = '\n\n   Reading Symbol Table...'
        self.InfoBox = Label(self.main, text=ShowStr)
        self.InfoBox.grid()
        
    def startPressed(self):
        print ("start pressed...", self.vStart.get(), self.vStop.get())
        self.bMeasureMode = True
        self.bCleanupQueue = True
        self.buttStart.config(state=DISABLED)
        self.vTime.set("")
        
    
    def getFrameID(self):
        return self.nbook.index(self.nbook.select())
    
    def processIncoming(self):

        """
        Handle all the messages currently in the queue (if any).
        """
        kylTemp = 0
        luftTemp = 0
        rpm = 0
        speed = 0
        boost = 0 
        afr = 0
        pgm = 0
        tq = 0
        power = 0
        batt = 0
        while self.queue.qsize():
            if (self.queue.qsize() > 2): # queue too full ?
                print ("Queue items: %i\n" %  self.queue.qsize())

                while self.queue.qsize() > 1:
                    msg = self.queue.get(0)
                    print (msg)

            try:
                msg = self.queue.get(0)
                # Test on  ##
                #print (msg)
                # Test off ##
                frameID = self.nbook.index(self.nbook.select())+1
                #print ("FrameID: "+ str(frameID))
                if (frameID == 3):
                    # only update frame 3
                    for item in msg:
                        if item == "txt":
                            self.vTime.set(msg[item])
                        if item == "speed":
                            speed = msg[item]
                            
                    self.vSpeed.set(str(speed) + " km/h")    
                    self.main.update_idletasks()
                
                else:
                    for item in msg:
                        if item == "kylTemp":
                            kylTemp = msg[item]
                        if item == "luftTemp":
                            luftTemp = msg[item]
                        if item == "rpm":
                            rpm = msg[item]
                        if item == "speed":                            
                            speed = msg[item]
                        if item == "boost":
                            boost = msg[item]
                        if item == "afr": 
                            afr = msg[item]
                        if item == "pgm":
                            pgm = msg[item]
                        if item == "tq":
                            tq = msg[item]
                        if item == "pgm":
                            pgm = msg[item]
                        if item == "batt":
                            batt = msg[item]
                            
                    power = tq*rpm/7121
                    #print(power, tq, rpm)

                    # calculate status bar
                    if (frameID == 4):

                        # idle --> byte 3 & 0x40
                        if (pgm & 0x0000000040000000) > 0:
                            self.cbIdle.select()
                        else:
                            self.cbIdle.deselect()

                        # closed loop --> byte 3 & 0x02
                        if (pgm & 0x0000000002000000) > 0:
                            self.cbCL.select()
                        else:
                            self.cbCL.deselect()

                        # knock (only T5.5) --> byte 1 & 0x02
                        #if (pgm & 0x0000000000000200) > 0:
                        #   self.cbKnock.select()
                        #  print ("Knock detected!")
                        #else:
                        self.cbKnock.deselect()
                            
                        # warmup --> byte 0 & 0x10
                        if (pgm & 0x0000000000000010) > 0:
                            self.cbWarm.select()
                        else:
                            self.cbWarm.deselect()
                    
                    # calculate max values
                    if (kylTemp > self.kylTempMax):
                        self.kylTempMax = kylTemp
                    if (rpm > self.rpmMax):
                        self.rpmMax = rpm
                    if (luftTemp > self.luftTempMax):
                        self.luftTempMax = luftTemp
                    if (speed > self.speedMax):
                        self.speedMax = speed
                    if (boost > self.boostMax):
                        self.boostMax = boost
                    if (batt > self.battMax):
                        self.battMax = batt
                    if (tq > self.tqMax):
                        self.tqMax = tq
                    if (power > self.powerMax):
                        self.powerMax = power

                    self.vKyl.set(str(kylTemp) + " °C")
                    self.vKylPeak.set(str(self.kylTempMax) + " °C")
                    #self.vKyl.set(str(kylTemp) + " °C")
                    #self.vKylPeak.set(str(self.kylTempMax) + " °C")
                    self.vLuft.set(str(luftTemp) + " °C")
                    self.vLuftPeak.set(str(self.luftTempMax) + " °C")
                    self.vRpm.set(str(rpm) + " U/min")
                    self.vRpmPeak.set(str(self.rpmMax) + " U/min")
                    self.pbRPM["value"] = rpm
                    self.vSpeed.set(str(speed) + " km/h")
                    self.vSpeedPeak.set(str(self.speedMax) + " km/h")
                    self.vAFR.set("%.2f" % afr)
                    self.vBatt.set("%.1f Volt" % batt)
                    self.vBattPeak.set("%.1f Volt" % (self.battMax))
                    self.vBoost.set("%.2f bar" % boost)
                    self.vBoostPeak.set("%.2f bar" % (self.boostMax))
                    self.pbBoost["value"] = (boost + 1) # convert from (-1 to 2) to (0 to 3)
                    self.pbBoost2["value"] = (boost + 1) # convert from (-1 to 2) to (0 to 3)
                    
                    if (rpm < 5000):
                        self.pbRPM.configure(style="green.Horizontal.TProgressbar")
						self.sGreen.configure(style="green.Horizontal.TProgressbar", text = rpm)
                    elif (rpm >= 5000 and rpm < 6000):
                        self.pbRPM.configure(style="yellow.Horizontal.TProgressbar")
                    else:
                        self.pbRPM.configure(style="red.Horizontal.TProgressbar")
                    if (boost < 0.55):
                        self.pbBoost.configure(style="green.Horizontal.TProgressbar")
                        self.pbBoost2.configure(style="green.Horizontal.TProgressbar")
                    elif (boost >= 0.55 and boost < 0.8):
                        self.pbBoost.configure(style="yellow.Horizontal.TProgressbar")
                        self.pbBoost2.configure(style="yellow.Horizontal.TProgressbar")
                        
                    elif (boost >= 0.8):
                        self.pbBoost.configure(style="red.Horizontal.TProgressbar")
                        self.pbBoost2.configure(style="red.Horizontal.TProgressbar")


                    self.vTQ.set(str(tq) + " Nm")
                    self.vTQPeak.set(str(self.tqMax) + " Nm")

                    self.vPower.set("%3.0f PS" % power)
                    self.vPowerPeak.set("%3.0f PS" % (self.powerMax))

                    # calculate status bar

                    self.main.update_idletasks()

            except Queue.Empty:
                pass


class CanClient:

    # class variables

    # frame format: (16 bytes)
    # "<" --> little endian
    # "I" --> unsigned int (4 bytes) --> frame ID
    # "B" --> unsigned char (1 byte) --> frame length
    # "3x" --> 3x pad byte  --> padding
    # "Q" --> unsigned long long (8 bytes) --> frame data
    #
    # example: b"\x0c\x00\x00\x00\x08\xff\xff\xff\xc7\x00\x30\x25\x80\x00\x5c\x00"
    #            ---------------- ID : 0000000c
    #                            ---- : length = 8 bytes
    #                                ------------ : padding
    #                                            -------------------------------- : data bytes
    can_frame_fmt = "<IB3xQ"

    speedStart = 0
    speedStop = 0
    
    bRecording = False
    bStartPressed = False
    thread1 = None
    pill2kill = threading.Event()
    
    count = 0
    
    ### here are the symbol adresses
    kyltemp_adr = 0x1032 # kyl_temp (1 byte)       
    lufttemp_adr = 0x1036 # luft_temp (1 byte)
    rpm_adr = 0x1062 # rpm (2 bytes)
    speed_adr = 0x101F  # bil_hast (1 byte)
    boost_adr = 0x1A62 # p_medel (1 byte)
    ad_sond_adr = 0x1016 # AD_sond (1 byte)
    pgm_adr = 0x103C # pgm_status (6 bytes)
    tq_adr = 0x1072 # TQ (2 bytes)

    demoMode = False
    dumpMode = False
    symMode = False
    swMode = False
    symbolTable = []

    def __init__(self, master):

        for i in range(len(sys.argv)):
            if (sys.argv[i].upper() == "DEMO"):
                self.demoMode = True
                print("starting in Demo mode....")
            if (sys.argv[i].upper() == "DUMP"):
                self.dumpMode = True

            if (sys.argv[i].upper() == "SYMBOL"):
                self.symMode = True

            if (sys.argv[i].upper() == "SW"):
                self.swMode = True

        # test ########## !!!!!!!!!!!!!!
        #self.symMode = True
        #self.swMode = True
        #self.dumpMode = True
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        # check if CANUSB is attached. If not --> demo mode
        cmd = "ip addr | grep slcan0"
        try:
            p = subprocess.check_output([cmd], shell=True)
            print("CanUSB/slcan0 device found !")
        except:
            self.demoMode = True
            self.recheck = True
            print("No slcan0 device found. Demo mode active")
                
        self.master = master

        # Create the queue
        self.queue = queue.Queue()

        

        # Set up the CAN connection, of no demo mode
        if (not self.demoMode):
            self.cansocket = socket.socket(socket.AF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
            self.cansocket.bind(('slcan0',))

        if self.symMode:
            # force reading from ECU and writing into file
            SW_VER = self.getT5SWVersion_T52()
            self.getT5SymbolTable(SW_VER, True)
            time.sleep(1)
            self.sendC2Cmd()
            print ("finish App")
            exit(1)
    
        elif self.swMode:
            self.getT5SWVersion_T52()
            time.sleep(1)
            self.sendC2Cmd()
            print ("finish App")
            exit(1)
            
        else:
            # normal main thread with GUI
            # Set up the thread to do asynchronous I/O
            # Set up the GUI part

            self.gui = GuiApp(master, self.queue, self.endApplication)
            master.protocol("WM_DELETE_WINDOW", self.endApplication)

            self.running = 1
            self.thread1 = threading.Thread(target=self.getT5Values,  args=(self.pill2kill,  ))
            self.thread1.start()

            # Start the periodic call in the GUI to check if the queue contains
            # anything
            self.periodicCall()
        

    # cleanup stuff
    def endApplication(self):
        if (self.dumpMode):
            print("endApplication called - CleanUp")
        self.running = 0
        self.bRecording = False
        self.sendC2Cmd()
        
        self.pill2kill.set()
        self.thread1.join()
        
        if (not self.demoMode):
            self.cansocket.close()
            
    ###################    
    # can frame stuff #
    ###################
    
    def build_can_frame(self, can_id, data):
        _s = struct.pack(self.can_frame_fmt, can_id, 8, data)
        #print ("build_can_frame:",_s) 
        return _s

    def dissect_can_frame(self, can_frame):
        can_id, can_dlc, data = struct.unpack(self.can_frame_fmt, can_frame) # check
        return (can_id, data)

    def sendReadSRAMCmd(self, address):
        if not address:
           print ("Error, adress empty!")
           return False  
        address += 5 # 5 bytes are read
        cmd = 0x00000000000000C7;
        cmd |= (address & 0x000000FF) << 4 * 8;
        cmd |= ((address & 0x0000FF00) >> 8) << 3 * 8;
        cmd |= ((address & 0x00FF0000) >> 2 * 8) << 2 * 8;
        cmd |= ((address & 0xFF000000) >> 3 * 8) << 8;
        x = self.build_can_frame(0x05, cmd)
        if (self.sendFrame(x)):
            return True
        else:
            return False
        
    def sendCmdByte(self, cmdbyte):
        cmd = 0x0000000000000000
        cmd |= cmdbyte
        cmd <<= 8
        cmd |= 0xC4
        cmd |= 0xFFFFFFFFFFFF0000
        
        x = self.build_can_frame(0x05, cmd)
        if (self.sendFrame(x)):
            return True
        else:
            return False

    def waitForResponse(self):
        returnStr = ""
        recv = self.readFrame()
        values = bytearray(recv)
        if self.demoMode:
            values[8] = 0xc6  # C6 must be content of byte 7

        if ((values[8]) != 0xc6): # 0xC6 is always in the response code in byte 7 (0 - 7)
            print ("Wrong response received!")
            return TIMEOUT
        id,data = self.dissect_can_frame(recv)
        #print ("waitForResponse -> Data received: %#.16x" % data)
        returnStr += chr((data >> 16) & 0xFF)
        #print ("waitForResponse:", returnStr)
        self.sendAck()
        return returnStr

    def sendAck(self):
        cmd = 0x00000000000000C6
        x = self.build_can_frame(0x06, cmd)
        if (self.sendFrame(x)):
            return True
        else:
            return False

    def sendCmdByteN(self, cmdbyte, nrOfBytes):
        retStr = ""
        self.sendCmdByte(cmdbyte)
        for i in range(nrOfBytes):
            str = self.waitForResponse()
            
            if (str == TIMEOUT):
                return TIMEOUT
            retStr += str
            #print ("sendCmdByteN returns:",retStr)
        return retStr

    def sendCmdByteE(self, cmdbyte, endString):
        retStr = ""
        self.sendCmdByte(cmdbyte)
        finished = False
        while not finished:
            str = self.waitForResponse()
            if (str == TIMEOUT):
                return TIMEOUT
            retStr += str
            if not endString.endswith(chr(CR)+chr(NL)):
                if len(retStr) > len(endString):
                    print ("sendCmdByteE break, returns:",retStr)
                    return retStr
            #print ("sendCmdByteE returns:",retStr)
            finished = (retStr.endswith(endString))
        return retStr

    def sendCmdByteEMax(self, cmdbyte, endString, maxLength):
        retStr = ""
        self.sendCmdByte(cmdbyte)
        finished = False
        cnt = 0
        while not finished:
            str = self.waitForResponse()
            if (str == TIMEOUT):
                return TIMEOUT
            retStr += str
            if not endString.endswith(chr(CR)+chr(NL)):
                if len(retStr) > len(endString):
                    print ("sendCmdByteEMax break, returns:",retStr)
                    return retStr
            #print ("sendCmdByteEMax returns:",retStr)
            cnt += 1
            finished = ((retStr.endswith(endString)) or (cnt >= maxLength))
                        
        return retStr

    def sendC2Cmd(self):
        cmd = 0x00000000000000C2
        x = self.build_can_frame(0x05, cmd)
        if (not self.sendFrame(x)):
                return False
        
        # Trionic answers, hence read one frame
        rcv = self.readFrame()
        return True

    def sendFrame(self, can_frame):
        if (self.dumpMode):
            self.printFrame(can_frame, True)
            
        if (self.demoMode):
            return True
        try:
            self.cansocket.send(can_frame)
            return True
        except socket.error:
            if (self.dumpMode):
                print('Error sending CAN frame')
            return False


    def readFrame(self):
        self.count += 1
        if (self.demoMode):
            recv = b"\x0c\x00\x00\x00\x08\xff\xff\xff\xc7\x00\x30\x25\x80\x00\x5c\x01", ('slcan0', 29)
        else:
            recv = (self.cansocket).recvfrom(16)
        # only for test #
        if (self.symMode and self.demoMode):
            if self.count < 5:
                recv = b"\x0c\x00\x00\x00\x08\xff\xff\xff\xc7\x00\x30\x25\x80\x00\x5c\x00", ('slcan0', 29)
                
            elif self.count == 6:
                recv = b"\x0c\x00\x00\x00\x08\xff\xff\xff\xc7\x00E\x25\x80\x00\x5c\x00", ('slcan0', 29)
               
            elif self.count == 7:
                recv = b"\x0c\x00\x00\x00\x08\xff\xff\xff\xc7\x00N\x25\x80\x00\x5c\x00", ('slcan0', 29)
               
            elif self.count == 8:
                recv = b"\x0c\x00\x00\x00\x08\xff\xff\xff\xc7\x00D\x25\x80\x00\x5c\x00", ('slcan0', 29)
               
            elif self.count == 9:
                recv = b"\x0c\x00\x00\x00\x08\xff\xff\xff\xc7\x00\x0d\x25\x80\x00\x5c\x00", ('slcan0', 29)
               
            elif self.count == 10:
                recv = b"\x0c\x00\x00\x00\x08\xff\xff\xff\xc7\x00\x0a\x25\x80\x00\x5c\x00", ('slcan0', 29)
                self.count = 0

            if (self.count > 10):
                self.count = 0
        # test end ###
        self.printFrame(recv[0], False)
        return recv[0] # only 1st element (canframe) is interesting

    def getT5SymbolTable(self, fileName, bForce = False):
        # check, if Symboltable already exists
        bSymFile = os.path.isfile(fileName)
        if (self.dumpMode):
            print(fileName, bSymFile)
        
        # read Symtable from Trionic and store it in file
        if bForce or not bSymFile:
            self.sendCmdByteN(ord('S'), 1) # capital "S" for T5.5
            symTableRaw = self.sendCmdByteE(CR,"END"+chr(CR)+chr(NL))
            ### test start
            #symTableRaw = ">A554X24L.18C\r\n48700001STSWFS\r\n38600001VSS_status\r\n3AC60002TWFS1PU\r\nEND\r\n"
            ### test end
            if (self.dumpMode):
                print ("\nTrionic has symbol table (read from ECU):\n" + symTableRaw)
            f = open(fileName, 'w')
            f.write(symTableRaw)
            f.close
            print ("Symbol table written in file")
            
        else: # read from file
            print("Symboltable: file read from filesystem...")
            f = open(fileName, 'r')
            symTableRaw = f.read() # whole file into a string
            f.close
            if (self.dumpMode):
                print ("\nTrionic has symbol table (read from file):\n" + symTableRaw)

        # store raw date into a list of tupels
        _symTbl = symTableRaw.split("\n")

        for i in range(1, len(_symTbl)-1): # w/o SW version and last line
            x = _symTbl[i]
            if ("END" not in x) and len(x) > 8:
                #print (x, len(x))
                try:
                    element = (x[8:], hex(int(x[0:4],16)), int(int(x[4:8],16)))
                    #print (element)
                    self.symbolTable.append(element)
                except:
                    print("Error creating symbol table, element :", x)
        #print ("symtbl in RAM:", self.symbolTable)            
        if (self.dumpMode):
            print ("SymbolTable:\n",self.symbolTable)
        

    def getT5SWVersion(self):
        # small "s" for T5.5, capial "S" for T5.2
        T5typ = "5.5"
        self.sendCmdByteN(ord('s'), 1)
        version = self.sendCmdByteEMax(CR,chr(CR)+chr(NL),20)
        # test only
        #version = ">>A554X24L.18C\r\n"
        version = version.lstrip('>')
        version = version.rstrip('\n')
        version = version.rstrip('\r')
        version = version.replace(">", "")
        n = len(version)
        if n < 10: # trionic 5.2 --> send capital "S", version is 1st string of symtable
            print("T5.2 found")
            self.sendCmdByteN(ord('S'), 1)
            version = self.sendCmdByteE(CR, chr(CR)+chr(NL))
            version = version.lstrip('>')
            version = version.rstrip('\n')
            version = version.rstrip('\r')
            T5typ = "5.2"

        if n > 12: 
            version = version[n-12:n]
        
        print ("\nTrionic (type: %s) has SW version: %s\n" % (T5typ,version))
        return version
    
    def getT5SWVersion_T52(self):
        
        if (MYSYMFILE != ""):
            version = MYSYMFILE
            return version
        
        if (self.demoMode):
           version = MYSYMFILE
           return version
        
        # small "s" for T5.5, capial "S" for T5.2
        T5typ = "5.2"
        self.sendCmdByteN(ord('S'), 1)
        version = self.sendCmdByteE(CR,chr(CR)+chr(NL))
        # test only
        #version = ">>A554X24L.18C\r\n"
        version = version.lstrip('>')
        version = version.rstrip('\n')
        version = version.rstrip('\r')
        #version = version.replace(">", "")
        n = len(version)
        #if n < 10: # trionic 5.2 --> send capital "S", version is 1st string of symtable
        #    self.sendCmdByteN(ord('S'), 1)
        #    version = self.sendCmdByteE(CR, chr(CR)+chr(NL))
        #    version = version.lstrip('>')
        #    version = version.rstrip('\n')
        #    version = version.rstrip('\r')
        #    T5typ = "5.2"

        if n > 12: 
            version = version[n-12:n]
        
        print ("\nTrionic (type: %s) has SW version: %s\n" % (T5typ,version))
        return version
        
    # gets the 6 data bytes out of the frame (bytes 0 - 5)
    def getSRAMReadData(self, recvframe):
        rid, rdata = self.dissect_can_frame(recvframe)
        if (rid != 12):  # 0x0C is always ID for received messages
            print("Error frame received")
            return -1
        # data byte array contains all 6 received data bytes
        databytes = bytearray(recvframe)[10:]
        databytes.reverse()
        return databytes

    def getT5Data(self, address, length, specCalc = False):
        #print(address)
        self.sendReadSRAMCmd(address)
        recvframe = self.readFrame()
        datalist = self.getSRAMReadData(recvframe)

        # for some special states like pgm_data, special calculation needed
        if (specCalc):
            return self.ConvertDataToDouble2(datalist, length)
    
        return self.ConvertDataToDouble(datalist, length)
            

    def ConvertDataToDouble(self, datalist, length):
        if length == 1:
            retval = datalist[0]
        if length == 2:
            retval = datalist[0] * 256
            retval += datalist[1]
        if length == 4:
            retval = datalist[0] *256*256*256
            retval += datalist[1] *256*256
            retval += datalist[2] *256
            retval += datalist[3]
            
        #data = 0
        #for i in range(length):
        #    data = data * (256 ** i)
        #    data += datalist[i]
        #    print (i, datalist[i], chr(datalist[i]), hex(datalist[i]), data)
        return retval

    def ConvertDataToDouble2(self, datalist, length):
        retval = 0
        # to check:simpler algorithm possible ?
        if length == 4:
            retval = datalist[3] *256*256*256
            retval += datalist[2] *256*256
            retval += datalist[1] *256
            retval += datalist[0]

        if length == 5:
            retval = datalist[4] *256*256*256*256
            retval += datalist[3] *256*256*256
            retval += datalist[2] *256*256
            retval += datalist[1] *256
            retval += datalist[0]     

        if length == 6:
            retval = datalist[5] *256*256*256*256*256
            retval += datalist[4] *256*256*256*256
            retval += datalist[3] *256*256*256
            retval += datalist[2] *256*256
            retval += datalist[1] *256
            retval += datalist[0]
            
        return retval

    def printFrame(self, can_frame, bTX):
        id,data = self.dissect_can_frame(can_frame)
        if bTX:
            s="TX"
        else:
            s="RX"
        if (self.dumpMode):
            print("--- %s: Frame ID:%.3x Data: %#.16x" % (s, id, data))

    #######################
    # can frame stuff end #
    #######################

    def periodicCall(self):
        """
        Check every 50 ms if there is something new in the queue.
        """
        if (self.recheck):
            #print("recheck..")
            cmd = "ip addr | grep slcan0"
            try:
                p = subprocess.check_output([cmd], shell=True)
                print("CanUSB/slcan0 device found !")
                self.cansocket = socket.socket(socket.AF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
                self.cansocket.bind(('slcan0',))
                self.recheck = False
            except:
                self.demoMode = True
                self.recheck = True
                #print("No slcan0 device found. Demo mode active")
            
        self.gui.processIncoming()

        if not self.running:
            # This is the brutal stop of the system. You may want to do
            # some cleanup before actually shutting it down.
            print ("Programm terminated.")
            time.sleep(1)
            sys.exit(1)
        
        self.master.after(50, self.periodicCall)

    def getAdrforSymbol(self, sym):

        for elem in self.symbolTable:
            if elem[0] == sym:
                print ("Symbol found:", elem)
                return int(elem[1],16)
        print("Symbol %s not found!" % sym)
        

    def getT5Values(self, stop_event):
        # init phase, show dialog
        self.gui.showInit()
        SWversion = self.getT5SWVersion_T52()
        #print (SWversion)
        self.gui.SWVer.set("T5 Version: " +SWversion)
        self.getT5SymbolTable(SWversion)

        # read symbol address from table
        self.kyltemp_adr = self.getAdrforSymbol("Kyl_temp")
        self.lufttemp_adr = self.getAdrforSymbol("Lufttemp")
        self.rpm_adr = self.getAdrforSymbol("Rpm")
        self.speed_adr = self.getAdrforSymbol("Bil_hast")
        self.boost_adr = self.getAdrforSymbol("P_medel")
        self.ad_sond_adr = self.getAdrforSymbol("AD_sond")
        self.pgm_adr = self.getAdrforSymbol("Pgm_status")
        self.tq_adr = self.getAdrforSymbol("TQ")
        self.batt_adr = self.getAdrforSymbol("Batt_volt")
        

        # run phase
        self.gui.startShowData()
        
        
        _speed = 0 
        _bUp = True
        values = {}
        while not stop_event.wait(0.1):
            try:
                
                fID =  (self.gui.getFrameID()) + 1

                if (fID == 1): #frame 1
                    
                    # read coolant temp
                    kylTemp = self.getT5Data(self.kyltemp_adr, 1)
                    if (kylTemp > 128):
                        kylTemp = -(256 - kylTemp)

                    #time.sleep(0.05)

                    # read lufttemp
                    luftTemp = self.getT5Data(self.lufttemp_adr, 1)
                    if (luftTemp > 128):
                        luftTemp = -(256 - luftTemp)

                    if (self.demoMode):
                        luftTemp = randint(10, 30)

                    #time.sleep(0.05)

                    # read rpm
                    rpm = self.getT5Data(self.rpm_adr, 2)
                    rpm *= 10

                    #time.sleep(0.05)


                    # read speed (bil_hast)
                    speed = self.getT5Data(self.speed_adr, 1)
                    if (self.demoMode):
                        speed = randint(0,200)
                        
                    
                    #read battery voltage
                    batt = self.getT5Data(self.batt_adr, 1)
                    batt /= 10
                    if (self.demoMode):
                        batt= randint(11,14)
                    
                    #time.sleep(0.05)
                    
                       # read boost (p_medel)
                    boost = self.getT5Data(self.boost_adr, 1)
                    if (self.demoMode):
                        boost = randint(10, 250)
                    boost *= 0.01
                    boost -= 1

                    values = {"rpm":rpm, "speed":speed, "kylTemp":kylTemp, "luftTemp":luftTemp,  "batt":batt,  "boost":boost}
                    self.queue.put(values)
                    
                    time.sleep(20/1000)  #wait for 20 ms
            

                    
                elif (fID == 2): # frame 2
                    
                    # read boost (p_medel)
                    boost = self.getT5Data(self.boost_adr, 1)
                    if (self.demoMode):
                        boost = randint(10, 250)
                    boost *= 0.01
                    boost -= 1

                    #time.sleep(0.05)

                    # read afr(ad_sond)
                    afr = self.getT5Data(self.ad_sond_adr, 1)
                    if (self.demoMode):
                        afr = 40
                    afr = abs(125 - afr) # return value is between -12 and -75
                    afr /= 100
                    afr *= 14.7

                    #time.sleep(0.05)

                    # read torque
                    tq = self.getT5Data(self.tq_adr, 2)
                    
                    #time.sleep(0.05)

                    # read rpm
                    rpm = self.getT5Data(self.rpm_adr, 2)
                    rpm *= 10

                    values = {"rpm": rpm,"boost":boost,"afr":afr, "tq":tq}
                    self.queue.put(values)
            
                    time.sleep(20/1000)  #wait for 20 ms
            
                    
                elif (fID == 3):  # frame 3
                    if not self.running:
                        break
                    lock.acquire()
                    self.speedStart = self.gui.vStart.get()
                    self.speedStop = self.gui.vStop.get()
                    self.bStartPressed = self.gui.bMeasureMode
                    lock.release()
                    values = {"speed":speed}
                    old_speed = speed

                    speed = self.getT5Data(self.speed_adr, 1)

                    if (self.demoMode):
                        if (_bUp):
                             _speed += 1
                             if (_speed >= 200): _bUp = False
                        else :
                             _speed -= 1 
                             if (_speed <= 0): _bUp = True
                        speed = _speed

                    #time.sleep(0.05)

                    if (self.bStartPressed): # start pressed, trigger matching speed

                        if ((speed > self.speedStart) and not self.bRecording):
                            textstr = "Km/h " + str('\u2193')
                            values = {"txt":textstr, "speed":speed}
                       

                        if ((speed < self.speedStart) and not self.bRecording):
                            textstr = "Km/h " + str('\u2191')
                            values = {"txt":textstr, "speed":speed}

                        # speed matched with startSpeed, start recording of time
                        if ((speed == self.speedStart) and not self.bRecording and (old_speed < speed)):
                            print ("Start set at:", speed)
                            self.bRecording = True
                            self.tStart = time.time() # start recording

                    if (self.bRecording):
                        tDelta = time.time() - self.tStart
                        textstr = ("%3.2f" % tDelta)
                        values = {"txt":textstr, "speed":speed}


                    if (self.bRecording and (speed == self.speedStop)):
                        print ("Stop reached at:" , speed)
                        self.bRecording = False
                        self.tStop = time.time()
                        tDelta = self.tStop - self.tStart
                        textstr = ("Zeit: %.3f" % tDelta)
                        values = {"txt":textstr, "speed":speed}
                        bStartPressed = False
                        lock.acquire()
                        self.gui.buttStart.config(state='normal')
                        self.gui.bMeasureMode = False
                        lock.release()
                        time.sleep(0.5)
                    ####### end if
                        
                    #print(values)
                    self.queue.put(values)
                    
                    time.sleep(20/1000)  #wait for 20 ms
            
                    
                elif (fID == 4): # frame 4

                    # read pgm_status
                    # in T5.2 only 5 bytes !!!
                    pgm = self.getT5Data(self.pgm_adr, 5,  True) 
                    if (self.demoMode):
                        pgm = 0x4433221100 
                        
                    time.sleep(20/1000)  #wait for 20 ms
            

                    values = {"pgm":pgm}
                    self.queue.put(values)
                
            except KeyboardInterrupt:
                break
            
        # while end    
        print("getValues terminated...")


def signal_handler(signum, frame): # needs always 2 arguments
    print("Signal handler called: %d" % signum)
    client.endApplication()

    
#### main loop

root = Tk()
lock = threading.Lock()

root.tk_setPalette(background='#F0F0ED', foreground='black',
               activeBackground='gray')
client = CanClient(root)
signal.signal(signal.SIGINT, signal_handler)
root.geometry('600x340')
w, h = root.winfo_screenwidth(), root.winfo_screenheight()


default_font = font.nametofont("TkDefaultFont")
#default_font = font.Font(family='Helvetica', size=20, weight='bold')
default_font.configure(size=10)
#root.overrideredirect(1)
#root.geometry("%dx%d+0+0" % (w, h))
root.option_add("*Font", default_font)
root.focus_set()
root.mainloop()
