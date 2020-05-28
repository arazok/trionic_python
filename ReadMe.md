Dear Saab friends,

I took some time to read out trionic values from the Trionic ECU by using a Raspberry Pi and visualize them live (according to the T5Suite).
Maybe you are also interested in, and you may can help (e.g. by testing) to incorporate the one or other feature or to bugfix :-)

What do you need?

- Raspberry Pi
- CANUSB Adpater
- Python script T5LiveData.py (attached)
- optional a UPS for the Raspi (I use the S.USV +)


How to connect the CANUSB adapter to the Trionic or to the diagnostic connector is described here:
- http://www.saabcentral.com/forums/showthread.php?t=248842 or
- http://www.16s.de/Forum/LiveDiag%209k%20CANUSB.pdf


For the Raspi you need a build which also includes the so-called SLCAN module,
I had to compile the current Debian Jessie build accordingly.
For instructions please see here:
https://www.raspberrypi.org/documentation/linux/kernel/building.md

Of course you need to add the new compiled kernel modules can, can_raw and slcan into the /etc/modules.
After boot they should be listed with lsmod.

So, do a 

sudo modprobe can, can_raw, slcan

The Lawicel CanUSB Adapter is configured and started for our Trionic with this command:

sudo slcand -f -b 4037 -o /dev/ttyUSB0 slcan0


If all this is running, then you only need to execute my python script "T5LiveData.py"
I have changed my LXDE environment so that the script is started automatically in full screen mode
It works like this: ....

1) Open the "~ / .config / lxsession / LXDE / autostart"
2) Add the line "@ / usr / bin / python /home/pi/T5LiveData.py"


When the script is first started, the SW version of the Trionic is determined and the symbol table is generated and stored in a file.
This can take up to 2 minutes, so be patient :-)
Then you should see the live data.
Note:
Sometimes there are problems with the first start, the symbol table is not fully built up. Then restart the script.
You can also start the script with the parameter "SYMBOL", then only the symbol table is set up and stored in a file.
(BTW: Name of the file is the software version of Trionic).
When restarting, the read-out is omitted from the SRAM and the created file is used.


Here are some impressions of the live data:

see screenshots (png files)


I have tested so far only with a T5.5 from my Saab 9.3, over hints / problems with other control devices I would be grateful.

I am available for any questions.

cheers
Dirk
dirk.lerch@gmx.de
