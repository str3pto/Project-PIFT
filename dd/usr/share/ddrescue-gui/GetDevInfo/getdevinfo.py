#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# Device Information Obtainer for DDRescue-GUI Version 1.7
# This file is part of DDRescue-GUI.
# Copyright (C) 2013-2017 Hamish McIntyre-Bhatty
# DDRescue-GUI is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3 or,
# at your option, any later version.
#
# DDRescue-GUI is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with DDRescue-GUI.  If not, see <http://www.gnu.org/licenses/>.

#Do future imports to prepare to support python 3. Use unicode strings rather than ASCII strings, as they fix potential problems.
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

#Begin Main Class.
class Main():
    def IsPartition(self, Disk, DiskList=None):
        """Check if the given Disk is a partition"""
        logger.debug("GetDevInfo: Main().IsPartition(): Checking if Disk: "+Disk+" is a partition...")

        if Linux:
            if Disk[0:7] not in ["/dev/sr", "/dev/fd"] and Disk[-1].isdigit() and Disk[0:8] in DiskInfo.keys():
                Result =  True

            else:
                Result = False

        else:
            if "s" in Disk.split("disk")[1]:
                Result = True

            else:
                Result = False

        logger.info("GetDevInfo: Main().IsPartition(): Result: "+str(Result)+"...")

        return Result

    def GetVendor(self, Node=None, Disk=None):
        """Get the vendor"""
        if Linux:
            try:
                return unicode(Node.vendor.string)

            except AttributeError:
                return "Unknown"

        else:
            if DiskInfo["/dev/"+Disk]["Type"] == "Partition":
                #We need to use the info from the host Disk, which will be whatever came before.
                logger.debug("GetDevInfo: Main().GetVendor(): Using vendor info from host Disk, because this is a partition...")
                return DiskInfo[DiskInfo["/dev/"+Disk]["HostDevice"]]["Vendor"]

            else:
                try:
                    Vendor = self.Plist["MediaName"].split()[0]
                    logger.info("GetDevInfo: Main().GetVendor(): Found vendor info: "+Vendor)

                except KeyError:
                    Vendor = "Unknown"
                    logger.warning("GetDevInfo: Main().GetVendor(): Couldn't find vendor info!")

                return Vendor

    def GetProduct(self, Node=None, Disk=None):
        """Get the product"""
        if Linux:
            try:
                return unicode(Node.product.string)

            except AttributeError:
                return "Unknown"

        else:
            if DiskInfo["/dev/"+Disk]["Type"] == "Partition":
                #We need to use the info from the host Disk, which will be whatever came before.
                logger.debug("GetDevInfo: Main().GetProduct(): Using product info from host Disk, because this is a partition...")
                return DiskInfo[DiskInfo["/dev/"+Disk]["HostDevice"]]["Product"]

            else:
                try:
                    Product = ' '.join(self.Plist["MediaName"].split()[1:])
                    logger.info("GetDevInfo: Main().GetProduct(): Found product info: "+Product)

                except KeyError:
                    Product = "Unknown"
                    logger.warning("GetDevInfo: Main().GetVendor(): Couldn't find product info!")

                return Product

    def GetCapacity(self, Node=None):
        """Get the capacity and human-readable capacity"""
        if Linux:
            try:
                RawCapacity = unicode(Node.size.string)

            except AttributeError:
                try:
                    RawCapacity = unicode(Node.capacity.string)

                except AttributeError:
                    return "Unknown", "Unknown"

            #Round the sizes to make them human-readable.
            UnitList = [None, "B", "KB", "MB", "GB", "TB", "PB", "EB"]
            Unit = "B"
            HumanSize = int(RawCapacity)

            try:
                while len(unicode(HumanSize)) > 3:
                    #Shift up one unit.
                    Unit = UnitList[UnitList.index(Unit)+1]
                    HumanSize = HumanSize//1000

            except IndexError:
                return "Unknown", "Unknown"

            #Include the unit in the result for both exact and human-readable sizes.
            return RawCapacity, unicode(HumanSize)+" "+Unit

        else:
            try:
                Size = self.Plist["TotalSize"]
                Size = unicode(Size)
                logger.info("GetDevInfo: Main().GetCapacity(): Found size info: "+Size)

            except KeyError:
                Size = "Unknown"
                logger.warning("GetDevInfo: Main().GetCapacity(): Couldn't find size info!")

            return Size

    def GetDescription(self, Disk):
        """Find description information for the given Disk. (OS X Only)"""
        logger.info("GetDevInfo: Main().GetDescription(): Getting description info for Disk: "+Disk+"...")

        #Gather info from diskutil to create some descriptions.
        #Internal or external.
        try:
            if self.Plist["Internal"]:
                InternalOrExternal = "Internal "

            else:
                InternalOrExternal = "External "

        except KeyError:
            InternalOrExternal = ""

        #Type SSD or HDD.
        try:
            if self.Plist["SolidState"]:
                Type = "Solid State Drive "

            else:
                Type = "Hard Disk Drive "

        except KeyError:
            Type = ""

        #Bus protocol.
        try:
            BusProtocol = unicode(self.Plist["BusProtocol"])

        except KeyError:
            BusProtocol = "Unknown"

        if InternalOrExternal != "" and Type != "":
            if BusProtocol != "Unknown":
                return InternalOrExternal+Type+"(Connected through "+BusProtocol+")"

            else:
                return InternalOrExternal+Type

        else:
            return "N/A"

    def GetDeviceInfo(self, Node):
        """Get Device Information"""
        HostDisk = unicode(Node.logicalname.string)
        DiskInfo[HostDisk] = {}
        DiskInfo[HostDisk]["Name"] = HostDisk
        DiskInfo[HostDisk]["Type"] = "Device"
        DiskInfo[HostDisk]["HostDevice"] = "N/A"
        DiskInfo[HostDisk]["Partitions"] = []
        DiskInfo[HostDisk]["Vendor"] = self.GetVendor(Node)
        DiskInfo[HostDisk]["Product"] = self.GetProduct(Node)

        #Ignore capacities for all optical media.
        if "/dev/cdrom" in HostDisk or "/dev/sr" in HostDisk or "/dev/dvd" in HostDisk:
            DiskInfo[HostDisk]["RawCapacity"], DiskInfo[HostDisk]["Capacity"] = ("N/A", "N/A")

        else:
            DiskInfo[HostDisk]["RawCapacity"], DiskInfo[HostDisk]["Capacity"] = self.GetCapacity(Node)

        DiskInfo[HostDisk]["Description"] = unicode(Node.description.string)

        return HostDisk

    def GetPartitionInfo(self, SubNode, HostDisk):
        """Get Partition Information"""
        try:
            Volume = unicode(SubNode.logicalname.string)

        except AttributeError:
            Volume = HostDisk+unicode(SubNode.physid.string)

        #Fix bug on Pmagic, if the volume already exists in DiskInfo, or if it is an optical drive, ignore it here.
        if Volume in DiskInfo or "/dev/cdrom" in Volume or "/dev/sr" in Volume or "/dev/dvd" in Volume:
            return Volume

        DiskInfo[Volume] = {}
        DiskInfo[Volume]["Name"] = Volume
        DiskInfo[Volume]["Type"] = "Partition"
        DiskInfo[Volume]["HostDevice"] = HostDisk
        DiskInfo[Volume]["Partitions"] = []
        DiskInfo[HostDisk]["Partitions"].append(Volume)
        DiskInfo[Volume]["Vendor"] = self.GetVendor(SubNode)
        DiskInfo[Volume]["Product"] = "Host Device: "+DiskInfo[HostDisk]["Product"]
        DiskInfo[Volume]["RawCapacity"], DiskInfo[Volume]["Capacity"] = self.GetCapacity(SubNode)
        DiskInfo[Volume]["Description"] = unicode(SubNode.description.string)
        return Volume

    def ParseLVMOutput(self):
        """Get LVM partition information"""
        LineCounter = 0

        for Line in self.LVMOutput:
            LineCounter += 1
            if "--- Logical volume ---" in Line:
                self.AssembleLVMDiskInfo(LineCounter)

    def AssembleLVMDiskInfo(self, LineCounter):
        """Assemble LVM disk info into the dictionary"""
        #Get all the info related to this partition.
        RawLVMInfo = []

        for Line in self.LVMOutput[LineCounter:]:
            RawLVMInfo.append(Line)

            #When we get to the next volume, stop adding stuff to this entry's data variable.
            if "--- Logical volume ---" in Line:
                RawLVMInfo.pop()
                break

        #Start assembling the entry.
        for Line in RawLVMInfo:
            if "LV Path" in Line:
                Temp = Line.split()[-1]
                Volume = "/dev/mapper/"+'-'.join(Temp.split("/")[2:])
                DiskInfo[Volume] = {}
                DiskInfo[Volume]["Name"] = Volume
                DiskInfo[Volume]["LVName"] = Volume.split("/")[-1]
                DiskInfo[Volume]["VGName"] = Volume.split("/")[2]
                DiskInfo[Volume]["Type"] = "Partition"
                DiskInfo[Volume]["Partitions"] = []
                DiskInfo[Volume]["Vendor"] = "Linux"
                DiskInfo[Volume]["Product"] = "LVM Partition"
                DiskInfo[Volume]["Description"] = "LVM partition "+DiskInfo[Volume]["LVName"]+" in volume group "+DiskInfo[Volume]["VGName"]

            elif "LV Size" in Line:
                DiskInfo[Volume]["Capacity"] = ' '.join(Line.split()[-2:])

            elif "Physical volume" in Line:
                DiskInfo[Volume]["HostPartition"] = Line.split()[-1]
                DiskInfo[Volume]["HostDevice"] = DiskInfo[DiskInfo[Volume]["HostPartition"]]["HostDevice"]

    def GetInfo(self, Standalone=False):
        """Get Disk Information."""
        logger.info("GetDevInfo: Main().GetInfo(): Preparing to get Disk info...")

        global DiskInfo
        DiskInfo = {}

        if Linux:
            #Run lshw to try and get disk information.
            logger.debug("GetDevInfo: Main().GetInfo(): Running 'LC_ALL=C lshw -sanitize -class disk -class volume -xml'...")
            runcmd = subprocess.Popen("LC_ALL=C lshw -sanitize -class disk -class volume -xml", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

            #Get the output.
            stdout, stderr = runcmd.communicate()

            logger.debug("GetDevInfo: Main().GetInfo(): Done.")

            #Parse XML as HTML to support Ubuntu 12.04 LTS. Otherwise output is cut off.
            self.Output = BeautifulSoup(stdout, "html.parser")

            #Support for Ubuntu 12.04 LTS as that lshw outputs XML differently in that release.
            if unicode(type(self.Output.list)) == "<type 'NoneType'>":
                ListOfDevices = self.Output.children

            else:
                ListOfDevices = self.Output.list.children

            #Find the disks.
            for Node in ListOfDevices:
                if unicode(type(Node)) != "<class 'bs4.element.Tag'>":
                    continue

                #These are devices.
                HostDisk = self.GetDeviceInfo(Node)

                #Detect any partitions and sub-partitions (logical partitions).
                Partitions = Node.find_all("node")

                #Get the info of any partitions these devices contain.
                for SubNode in Partitions:
                    if unicode(type(SubNode)) != "<class 'bs4.element.Tag'>" or SubNode.name != "node":
                        continue

                    #Partitions.
                    Volume = self.GetPartitionInfo(SubNode, HostDisk)

            #Find any LVM disks. Don't use -c because it doesn't give us enough information.
            logger.debug("GetDevInfo: Main().GetInfo(): Running 'LC_ALL=C lvdisplay --maps'...")
            cmd = subprocess.Popen("LC_ALL=C lvdisplay --maps", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            self.LVMOutput = cmd.communicate()[0].split("\n")
            logger.debug("GetDevInfo: Main().GetInfo(): Done!")

            self.ParseLVMOutput()

        else:
            #Run diskutil list to get Disk names.
            logger.debug("GetDevInfo: Main().GetInfo(): Running 'diskutil list -plist'...")
            runcmd = subprocess.Popen("diskutil list -plist", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

            #Get the output.
            stdout, stderr = runcmd.communicate()
            logger.debug("GetDevInfo: Main().GetInfo(): Done.")

            #Parse the plist (Property List).
            Plist = plistlib.readPlistFromString(stdout)

            UnitList = [None, "B", "KB", "MB", "GB", "TB", "PB"]

            #Get disk info.
            for Disk in Plist["AllDisks"]:
                DiskInfo["/dev/"+Disk] = {}
                DiskInfo["/dev/"+Disk]["Name"] = "/dev/"+Disk

                #Run diskutil info to get Disk info.
                logger.debug("GetDevInfo: Main().GetInfo(): Running 'diskutil info -plist "+Disk+"'...")
                runcmd = subprocess.Popen("diskutil info -plist "+Disk, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
                stdout, stderr = runcmd.communicate()

                #Parse the plist (Property List).
                self.Plist = plistlib.readPlistFromString(stdout)

                #Check if the Disk is a partition.
                DiskIsPartition = self.IsPartition(Disk)

                if DiskIsPartition:
                    DiskInfo["/dev/"+Disk]["Type"] = "Partition"
                    DiskInfo["/dev/"+Disk]["HostDevice"] = "/dev/disk"+Disk.split("disk")[1].split("s")[0]
                    DiskInfo["/dev/"+Disk]["Partitions"] = []
                    DiskInfo[DiskInfo["/dev/"+Disk]["HostDevice"]]["Partitions"].append("/dev/"+Disk)

                else:
                    DiskInfo["/dev/"+Disk]["Type"] = "Device"
                    DiskInfo["/dev/"+Disk]["HostDevice"] = "N/A"
                    DiskInfo["/dev/"+Disk]["Partitions"] = []

                #Get all other information, making sure it remains stable even if we found no info at all.
                Vendor = self.GetVendor(Disk=Disk)

                if Vendor != None:
                    DiskInfo["/dev/"+Disk]["Vendor"] = Vendor

                else:
                    DiskInfo["/dev/"+Disk]["Vendor"] = "Unknown"

                Product = self.GetProduct(Disk=Disk)

                if Product != None:
                    DiskInfo["/dev/"+Disk]["Product"] = Product

                else:
                    DiskInfo["/dev/"+Disk]["Product"] = "Unknown"

                Size = self.GetCapacity()

                if Size != None:
                    DiskInfo["/dev/"+Disk]["Capacity"] = Size

                else:
                    DiskInfo["/dev/"+Disk]["Capacity"] = "Unknown"

                #Round the sizes to make them human-readable. *** Move to get capacity and update test ***
                Unit = "B"

                #Catch an error in case Size is unknown.
                try:
                    HumanSize = int(Size)

                except ValueError:
                    DiskInfo["/dev/"+Disk]["HumanCapacity"] = "Unknown"

                else:
                    while len(unicode(HumanSize)) > 3:
                        #Shift up one unit.
                        Unit = UnitList[UnitList.index(Unit)+1]
                        HumanSize = HumanSize//1000

                    #Include the unit in the result for both exact and human-readable sizes.
                    DiskInfo["/dev/"+Disk]["HumanCapacity"] = unicode(HumanSize)+" "+Unit

                Description = self.GetDescription(Disk)

                if Description != None:
                    DiskInfo["/dev/"+Disk]["Description"] = Description

                else:
                    DiskInfo["/dev/"+Disk]["Description"] = "Unknown"

        #Check we found some disks.
        if len(DiskInfo) == 0:
            logger.info("GetDevInfo: Main().GetInfo(): Didn't find any disks, throwing RuntimeError!")
            raise RuntimeError("No Disks found!")

        logger.info("GetDevInfo: Main().GetInfo(): Finished!")

        return DiskInfo

    def GetBlockSize(self, Disk):
        """Run the command to get the block size, and pass it to ComputeBlockSize()"""
        logger.debug("GetDevInfo: Main().GetBlockSize(): Finding blocksize for Disk: "+Disk+"...")

        if Linux:
    	    #Run /sbin/blockdev to try and get blocksize information.
            Command = "blockdev --getpbsz "+Disk

        else:
            #Run diskutil list to get Disk names.
            Command = "diskutil info -plist "+Disk

        logger.debug("GetDevInfo: Main().GetBlockSize(): Running '"+Command+"'...")
        runcmd = subprocess.Popen(Command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

        #Get the output and pass it to ComputeBlockSize.
        return self.ComputeBlockSize(Disk, runcmd.communicate()[0])

    def ComputeBlockSize(self, Disk, stdout):
        """Called with stdout from blockdev (Linux), or dickutil (Mac) and gets block size"""
        if Linux:
            Result = stdout.replace('\n', '')

            #Check it worked (it should be convertable to an integer if it did).
            try:
                tmp = int(Result)

            except ValueError:
                #It didn't, this is probably a file, not a Disk.
                logger.warning("GetDevInfo: Main().GetBlockSize(): Couldn't get blocksize for Disk: "+Disk+"! Returning None...")
                return None

            else:
                #It did.
                logger.info("GetDevInfo: Main().GetBlockSize(): Blocksize for Disk: "+Disk+": "+Result+". Returning it...")
                return Result

        else:
            #Parse the plist (Property List).
            try:
                Plist = plistlib.readPlistFromString(stdout)

            except:
                logger.warning("GetDevInfo: Main().GetBlockSize(): Couldn't get blocksize for Disk: "+Disk+"! Returning None...")
                return None

            else:
                if "DeviceBlockSize" in Plist:
                    Result = unicode(Plist["DeviceBlockSize"])
                    logger.info("GetDevInfo: Main().GetBlockSize(): Blocksize for Disk: "+Disk+": "+Result+". Returning it...")

                elif "VolumeBlockSize" in Plist:
                    Result = unicode(Plist["VolumeBlockSize"])
                    logger.info("GetDevInfo: Main().GetBlockSize(): Blocksize for Disk: "+Disk+": "+Result+". Returning it...")

                else:
                    logger.warning("GetDevInfo: Main().GetBlockSize(): Couldn't get blocksize for Disk: "+Disk+"! Returning None...")
                    Result = None

                return Result

#End Main Class.
if __name__ == "__main__":
    #Import modules.
    import subprocess
    import re
    import platform
    import logging
    from bs4 import BeautifulSoup
    import plistlib

    #Set up basic logging to stdout.
    logger = logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s: %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p', level=logging.DEBUG)

    #Determine if running on Linux or Mac.
    global Linux
    if platform.system() == 'Linux':
        Linux = True

    elif platform.system() == "Darwin":
        Linux = False

    logger.info("Running on Linux: "+str(Linux))

    Main().GetInfo(Standalone=True)

    #Print the info in a (semi :D) readable way.
    Keys = DiskInfo.keys()
    Keys.sort()

    for Key in Keys:
        print("\n\n", DiskInfo[Key], "\n\n")
        print(Main().GetBlockSize(Key))
