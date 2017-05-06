#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# BackendTools test functions for DDRescue-GUI Version 1.7
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

#If you're wondering why this is here, it's so that there are some known good/sane functions to aid testing the ones in BackendTools.

#Do future imports to prepare to support python 3. Use unicode strings rather than ASCII strings, as they fix potential problems.
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

def StartProcess(Command, ReturnOutput=False):
    """Start a given process, and return output and return value if needed"""
    runcmd = subprocess.Popen("LC_ALL=C "+Command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

    while runcmd.poll() == None:
        time.sleep(0.25)

    #Save runcmd.stdout.readlines, and runcmd.returncode, as they tend to reset fairly quickly. Handle unicode properly.
    Output = []

    for line in runcmd.stdout.readlines():
        Output.append(line.decode("UTF-8", errors="ignore"))

    Retval = int(runcmd.returncode)

    if ReturnOutput == False:
        #Return the return code back to whichever function ran this process, so it can handle any errors.
        return Retval

    else:
        #Return the return code, as well as the output.
        return Retval, ''.join(Output)

def IsMounted(Partition, MountPoint=None):
    """Checks if the given partition is mounted.
    Partition is the given partition to check.
    If MountPoint is specified, check if the partition is mounted there, rather than just if it's mounted.
    Return boolean True/False.
    """
    if MountPoint == None:
        MountInfo = StartProcess("mount", ReturnOutput=True)[1]

        Mounted = False

        #OS X fix: Handle paths with /tmp in them, as paths with /private/tmp.
        if not Linux and "/tmp" in Partition:
            Partition = Partition.replace("/tmp", "/private/tmp")

        #Linux fix: Accept any mountpoint when called with just one argument.
        for Line in MountInfo.split("\n"):
            if len(Line) != 0:
                if Line.split()[0] == Partition or Line.split()[2] == Partition:
                    Mounted = True
                    break

    else:
        #Check where it's mounted to.
        Mounted = False

        #OS X fix: Handle paths with /tmp in them, as paths with /private/tmp.
        if not Linux and "/tmp" in MountPoint:
            MountPoint = MountPoint.replace("/tmp", "/private/tmp")

        if GetMountPointOf(Partition) == MountPoint:
            Mounted = True

    return Mounted

def GetMountPointOf( Partition):
    """Returns the mountpoint of the given partition, if any.
    Otherwise, return None"""
    MountInfo = StartProcess("mount", ReturnOutput=True)[1]
    MountPoint = None

    for Line in MountInfo.split("\n"):
        SplitLine = Line.split()

        if len(SplitLine) != 0:
            if Partition == SplitLine[0]:
                MountPoint = SplitLine[2]
                break

    return MountPoint

def MountPartition(Partition, MountPoint, Options=""):
    """Mounts the given partition.
    Partition is the partition to mount.
    MountPoint is where you want to mount the partition.
    Options is non-mandatory and contains whatever options you want to pass to the mount command.
    The default value for Options is an empty string.
    """     
    MountInfo = StartProcess("mount", ReturnOutput=True)[1]

    #There is a partition mounted here. Check if our partition is already mounted in the right place.
    if MountPoint == GetMountPointOf(Partition):
        #The correct partition is already mounted here.
        return 0

    elif MountPoint in MountInfo:
        #Something else is in the way. Unmount that partition, and continue.
        if UnmountDisk(MountPoint) != 0:
            return False

    #Create the dir if needed.
    if os.path.isdir(MountPoint) == False:
        os.makedirs(MountPoint)
    
    #Mount the device to the mount point.
    #Use diskutil on OS X.
    if Linux:
        Retval = StartProcess("mount "+Options+" "+Partition+" "+MountPoint)

    else:
        Retval = StartProcess("diskutil mount "+Options+" "+Partition+" -mountPoint "+MountPoint)

    return Retval

def UnmountDisk(Disk):
    """Unmount the given disk"""
    #Check if it is mounted.
    if IsMounted(Disk) == False:
        #The disk isn't mounted.
        #Set Retval to 0.
        Retval = 0

    else:
        #The disk is mounted.
        #Unmount it.
        if Linux:
            Retval = StartProcess(Command="umount "+Disk, ReturnOutput=False)

        else:
            Retval = StartProcess(Command="diskutil umount "+Disk, ReturnOutput=False)
            
    #Return the return value
    return Retval
