#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# GetDevInfo tests for DDRescue-GUI Version 1.7
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

#import modules.
import unittest
import wx
import os
import plistlib

#import test data.
from . import GetDevInfoTestData as Data

#Set up resource path and determine OS.
if "wxGTK" in wx.PlatformInfo:
    #Set the resource path to /usr/share/ddrescue-gui/
    ResourcePath = '/usr/share/ddrescue-gui'
    Linux = True

    #Check if we're running on Parted Magic.
    if os.uname()[1] == "PartedMagic":
        PartedMagic = True

    else:
        PartedMagic = False

elif "wxMac" in wx.PlatformInfo:
    try:
        #Set the resource path from an environment variable, as mac .apps can be found in various places.
        ResourcePath = os.environ['RESOURCEPATH']

    except KeyError:
        #Use '.' as the rescource path instead as a fallback.
        ResourcePath = "."

    Linux = False
    PartedMagic = False

class TestIsPartition(unittest.TestCase):
    def setUp(self):
        #Create a fictional DiskInfo distionary for it to test against.
        if Linux:
            GetDevInfo.getdevinfo.DiskInfo = Data.ReturnFakeDiskInfoLinux()

        else:
            GetDevInfo.getdevinfo.DiskInfo = Data.ReturnFakeDiskInfoMac()

    def tearDown(self):
        del GetDevInfo.getdevinfo.DiskInfo

    @unittest.skipUnless(Linux, "Linux-specific test")
    def testIsPartitionLinux(self):
        #Cdrom drives.
        for CDROM in ["/dev/cdrom", "/dev/dvd", "/dev/sr0", "/dev/sr1", "/dev/sr10", "/dev/scd0", "/dev/scd1", "/dev/scd10"]:
            self.assertFalse(DevInfoTools().IsPartition(CDROM))

        #Floppy drives.
        for FLOPPY in ["/dev/fd0", "/dev/fd1", "/dev/fd10"]:
            self.assertFalse(DevInfoTools().IsPartition(FLOPPY))

        #Devices.
        for DEVICE in ["/dev/sda", "/dev/sdb", "/dev/hda", "/dev/hdb"]:
            self.assertFalse(DevInfoTools().IsPartition(DEVICE))

        #Partitions.
        for PARTITION in ["/dev/sda1", "/dev/sda2", "/dev/sda11", "/dev/sda56"]:
            self.assertTrue(DevInfoTools().IsPartition(PARTITION))

    @unittest.skipUnless(not Linux, "Mac-specific test")
    def testIsPartitionMac(self):
        #Devices.
        for DEVICE in ["/dev/disk0", "/dev/disk1", "/dev/disk10"]:
            self.assertFalse(DevInfoTools().IsPartition(DEVICE))

        #Partitions.
        for PARTITION in ["/dev/disk0s2", "/dev/disk0s1", "/dev/disk0s45", "/dev/disk1s5", "/dev/disk1s45"]:
            self.assertTrue(DevInfoTools().IsPartition(PARTITION))

class TestGetVendorProductCapacityDescription(unittest.TestCase):
    def setUp(self):
        if Linux:
            self.Node1 = Data.Node1().GetCopy()
            self.Node2 = Data.Node2().GetCopy()
            self.BadNode1 = Data.BadNode1().GetCopy()
            self.BadNode2 = Data.BadNode2().GetCopy()
            self.BadNode3 = Data.BadNode3().GetCopy()

        else:
            GetDevInfo.getdevinfo.DiskInfo = Data.ReturnFakeDiskInfoMac()
            self.BadPlist0 = plistlib.readPlistFromString(Data.ReturnFakeDiskutilInfoBadDisk0Plist())
            self.Plist0 = plistlib.readPlistFromString(Data.ReturnFakeDiskutilInfoDisk0Plist())
            self.Plist0s1 = plistlib.readPlistFromString(Data.ReturnFakeDiskutilInfoDisk0s1Plist())
            self.Plist0s2 = plistlib.readPlistFromString(Data.ReturnFakeDiskutilInfoDisk0s2Plist())
            self.Plist0s3 = plistlib.readPlistFromString(Data.ReturnFakeDiskutilInfoDisk0s3Plist())

    def tearDown(self):
        if Linux:
            del self.Node1
            del self.Node2
            del self.BadNode1
            del self.BadNode2
            del self.BadNode3

        else:
            del GetDevInfo.getdevinfo.DiskInfo
            del self.BadPlist0
            del self.Plist0
            del self.Plist0s1
            del self.Plist0s2
            del self.Plist0s3

    @unittest.skipUnless(Linux, "Linux-specific test")
    def testGetVendorLinux(self):
        self.assertEqual(DevInfoTools().GetVendor(Node=self.Node1), "FakeVendor")
        self.assertEqual(DevInfoTools().GetVendor(Node=self.Node2), "FakeVendor2")
        self.assertEqual(DevInfoTools().GetVendor(Node=self.BadNode1), "Unknown")

    @unittest.skipUnless(not Linux, "Mac-specific test")
    def testGetVendorMac(self):
        #baddisk0
        GetDevInfo.getdevinfo.Main.Plist = self.BadPlist0
        self.assertEqual(DevInfoTools().GetVendor(Disk="disk0"), "Unknown")

        #disk0
        GetDevInfo.getdevinfo.Main.Plist = self.Plist0
        self.assertEqual(DevInfoTools().GetVendor(Disk="disk0"), "VBOX")

        #disk0s1
        GetDevInfo.getdevinfo.Main.Plist = self.Plist0s1
        self.assertEqual(DevInfoTools().GetVendor(Disk="disk0s1"), "ThereIsNone")

        #disk0s2
        GetDevInfo.getdevinfo.Main.Plist = self.Plist0s2
        self.assertEqual(DevInfoTools().GetVendor(Disk="disk0s2"), "ThereIsNone")

        #disk0s3
        GetDevInfo.getdevinfo.Main.Plist = self.Plist0s3
        self.assertEqual(DevInfoTools().GetVendor(Disk="disk0s3"), "ThereIsNone")

    @unittest.skipUnless(Linux, "Linux-specific test")
    def testGetProductLinux(self):
        self.assertEqual(DevInfoTools().GetProduct(Node=self.Node1), "FakeProduct")
        self.assertEqual(DevInfoTools().GetProduct(Node=self.Node2), "FakeProduct2")
        self.assertEqual(DevInfoTools().GetProduct(Node=self.BadNode1), "Unknown")

    @unittest.skipUnless(not Linux, "Mac-specific test")
    def testGetProductMac(self):
        #baddisk0
        GetDevInfo.getdevinfo.Main.Plist = self.BadPlist0
        self.assertEqual(DevInfoTools().GetProduct(Disk="disk0"), "Unknown")

        #disk0
        GetDevInfo.getdevinfo.Main.Plist = self.Plist0
        self.assertEqual(DevInfoTools().GetProduct(Disk="disk0"), "HARDDISK")

        #disk0s1
        GetDevInfo.getdevinfo.Main.Plist = self.Plist0s1
        self.assertEqual(DevInfoTools().GetProduct(Disk="disk0s1"), "FakeDisk")

        #disk0s2
        GetDevInfo.getdevinfo.Main.Plist = self.Plist0s2
        self.assertEqual(DevInfoTools().GetProduct(Disk="disk0s2"), "FakeDisk")

        #disk0s3
        GetDevInfo.getdevinfo.Main.Plist = self.Plist0s3
        self.assertEqual(DevInfoTools().GetProduct(Disk="disk0s3"), "FakeDisk")

    @unittest.skipUnless(Linux, "Linux-specific test")
    def testGetCapacityLinux(self):
        #1st good node.
        RawCapacity, HumanSize = DevInfoTools().GetCapacity(Node=self.Node1)
        self.assertEqual(RawCapacity, "100000000000")
        self.assertEqual(HumanSize, "100 GB")

        #2nd good node.
        RawCapacity, HumanSize = DevInfoTools().GetCapacity(Node=self.Node2)
        self.assertEqual(RawCapacity, "10000000000000000000")
        self.assertEqual(HumanSize, "10 EB")

        #1st bad node.
        self.assertEqual(DevInfoTools().GetCapacity(Node=self.BadNode1), ("Unknown", "Unknown"))

        #2nd bad node.
        self.assertEqual(DevInfoTools().GetCapacity(Node=self.BadNode2), ("Unknown", "Unknown"))

    @unittest.skipUnless(Linux, "Linux-specific test")
    @unittest.expectedFailure
    def testBadGetCapacityLinux(self):
        #3rd bad node.
        self.assertEqual(DevInfoTools().GetCapacity(Node=self.BadNode3), ("Unknown", "Unknown"))

    @unittest.skipUnless(not Linux, "Mac-specific test")
    def testGetCapacityMac(self):
        #baddisk0
        GetDevInfo.getdevinfo.Main.Plist = self.BadPlist0
        self.assertEqual(DevInfoTools().GetCapacity(), "Unknown")

        #disk0
        GetDevInfo.getdevinfo.Main.Plist = self.Plist0
        self.assertEqual(DevInfoTools().GetCapacity(), "42948853248")

        #disk0s1
        GetDevInfo.getdevinfo.Main.Plist = self.Plist0s1
        self.assertEqual(DevInfoTools().GetCapacity(), "209715200")

        #disk0s2
        GetDevInfo.getdevinfo.Main.Plist = self.Plist0s2
        self.assertEqual(DevInfoTools().GetCapacity(), "42089095168")

        #disk0s3
        GetDevInfo.getdevinfo.Main.Plist = self.Plist0s3
        self.assertEqual(DevInfoTools().GetCapacity(), "650002432")

    @unittest.skipUnless(not Linux, "Mac-specific test")
    def testGetDescriptionMac(self):
        #baddisk0
        GetDevInfo.getdevinfo.Main.Plist = self.BadPlist0
        self.assertEqual(DevInfoTools().GetDescription(Disk="disk0"), "N/A")

        #disk0
        GetDevInfo.getdevinfo.Main.Plist = self.Plist0
        self.assertEqual(DevInfoTools().GetDescription(Disk="disk0"), "Internal Hard Disk Drive (Connected through SATA)")

        #disk0s1
        GetDevInfo.getdevinfo.Main.Plist = self.Plist0s1
        self.assertEqual(DevInfoTools().GetDescription(Disk="disk0s1"), "Internal Hard Disk Drive (Connected through SATA)")

        #disk0s2
        GetDevInfo.getdevinfo.Main.Plist = self.Plist0s2
        self.assertEqual(DevInfoTools().GetDescription(Disk="disk0s2"), "Internal Hard Disk Drive (Connected through SATA)")

        #disk0s3
        GetDevInfo.getdevinfo.Main.Plist = self.Plist0s3
        self.assertEqual(DevInfoTools().GetDescription(Disk="disk0s3"), "Internal Hard Disk Drive (Connected through SATA)")

class TestParseLVMOutput(unittest.TestCase):
    def setUp(self):
        GetDevInfo.getdevinfo.Main.LVMOutput = Data.ReturnFakeLVMOutput()
        GetDevInfo.getdevinfo.DiskInfo = Data.ReturnFakeDiskInfoLinux()
        self.CorrectDiskInfo = Data.ReturnFakeLVMDiskInfo()

    def tearDown(self):
        del GetDevInfo.getdevinfo.Main.LVMOutput
        del GetDevInfo.getdevinfo.DiskInfo
        del self.CorrectDiskInfo

    @unittest.skipUnless(Linux, "Linux-specific test")
    def testParseAndAssembleLVMOutput(self):
        DevInfoTools().ParseLVMOutput()
        self.assertEqual(GetDevInfo.getdevinfo.DiskInfo, self.CorrectDiskInfo)

class TestComputeBlockSize(unittest.TestCase):
    def setUp(self):
        if Linux:
            self.BlockSizes, self.CorrectResults = (Data.ReturnFakeBlockDevOutput(), [None, "512", "1024", "2048", "4096", "8192"])

        else:
            self.BlockSizes, self.CorrectResults = (["Not a plist", Data.ReturnFakeDiskutilInfoBadDisk0Plist(), Data.ReturnFakeDiskutilInfoDisk0Plist(), Data.ReturnFakeDiskutilInfoDisk0s1Plist(), Data.ReturnFakeDiskutilInfoDisk0s2Plist(), Data.ReturnFakeDiskutilInfoDisk0s3Plist()], [None, None, "512", "1024", "2048", "4096"])
        
        GetDevInfo.getdevinfo.plistlib = plistlib

    def tearDown(self):
        del self.BlockSizes
        del self.CorrectResults
        del GetDevInfo.getdevinfo.plistlib

    def testComputeBlockSize(self):
        for Data in self.BlockSizes:
            self.assertEqual(DevInfoTools().ComputeBlockSize("FakeDisk", Data), self.CorrectResults[self.BlockSizes.index(Data)])
