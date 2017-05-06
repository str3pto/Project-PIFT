# Project-PIFT
Abstract
From the moment of its release to the markets in 2012, the Raspberry Pi has set milestones in performance and portability, significantly enhanced by its ability to run from an external battery. Thanks to these factors and the Raspberry Pi’s excellent portability, the device can be an excellent portable tool to execute on-the-fly forensics extraction and analysis. This project develops a forensics tool based on the Raspberry Pi 3, with the intent to prove that this device can be used effectively within reason to perform some forensics tasks, such as write blocker and data analysis. Nowadays forensics tools are expensive and bulky, with the creation of the low power single board the same job can be achieved even with hardware limitation of the board. A special feature of this project is the integration TFT screen to facilitate, imaging, and health checks.

**Objective**

Create a software write-blocker Linux based Raspberry Pi with a PiTFT screen

**Project**

The project was designed around the Raspberry Pi 3 with a PiTFT screen. 

**DDRescue-GUI**

the maintainer for DDRescue-GUI, granted access to modify the software to fit the smaller screen, modified version of the software is available on DDRescue-GUI folder here and as a DEB file for installation. 

further modifications done to DDRescue-GUI was the implementation of a SHA512 hash calculator.

**Raspbian**
Raspbian is available on adafruit website [Link](https://learn.adafruit.com/adafruit-pitft-3-dot-5-touch-screen-for-raspberry-pi/easy-install), this is based on Jessie lite.

The Raspbian was modified to stop mounting the drives as they are connected, by editing the following file:

>~/.config/pcmanfm/LXDE/pcmanfm.conf

and make sure it contains:
```
[volume]
mount_on_startup=0
mount_removable=0
```
xserver, raspberrypi-kernel, xserver-org cannot be updated on this version of the Raspbian, it will crash the screen, to solve this issue just issue the following command.
```
echo <PackageName> hold | sudo dpkg --set-selections 
```
for example:
```
echo xserver hold | sudo dpkg --set-selections
```
Following the git from msuhanov [Link](https://github.com/msuhanov/Linux-write-blocker), a kernel level block based on the scripts and udev rules was implemented to the OS

For easier implementation, a deb file was packed with the files, to be installed on the right location, and small python script was created to make use of the rules to check the status of the USB hard drives connected to the Raspberry Pi

deb is located on the Unblocker folder

##Implementation

The installation of the ddrescue-gui1.7-pi.deb and unblocker1.0.deb, will enable all the above, apart from the manual changes on pcmanfm.conf and the dpkg command.

##Testing 

The speed of imagining from sba to an image on sdb are the following:
```
| Size | Imaging Time| Hashing Source | Hashing Destination | Total Time |
|      | (HH:MM)     |  (HH:MM)       |  (HH:MM)            |  (HH:MM)   |
|------|-------------|----------------|---------------------|------------|
| 80Gb | 01:56       | 00:48          |  00:45              | 03:29      |
| 500Gb| 12:02       | 04:45          |  04:40              | 21:27      |
| 750Gb| 17:58       | 07:10          |  07:01              | 32:09      |
|------|-------------|----------------|---------------------|------------|
```
The average speeed of the transfer was sits at 12Mb/s considering that was used a dual-caddy USB3.0 the total speed was 24Mb/s for USB2.0
