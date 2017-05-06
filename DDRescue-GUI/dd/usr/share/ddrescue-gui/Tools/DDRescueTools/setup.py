#!/usr/bin/env python
# -*- coding: utf-8 -*-
# DDRescue Tools (setup scripts) for ddrescue v1.21 (or newer) in the Tools Package for DDRescue-GUI Version 1.7
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

#Import modules.
import types

#Import tools modules.
from . import decorators
from . import allversions
from . import onePointForteen
from . import onePointEighteen
from . import onePointTwenty
from . import onePointTwentyOne
from . import onePointTwentyTwo

#Get a list of functions in all of our ddrescue tools modules.
Functions = []

for Module in (allversions, onePointForteen, onePointEighteen, onePointTwenty, onePointTwentyOne, onePointTwentyTwo):
    for Function in dir(Module):
        if isinstance(Module.__dict__.get(Function), types.FunctionType):
            Functions.append(vars(Module)[Function])

def SetupForCorrectDDRescueVersion(DDRescueVersion):
    #Select the best tools if we have an unsupported version of ddrescue.
    MinorVersion = int(DDRescueVersion.split(".")[1])

    if MinorVersion < 14:
        #Too old.
        BestVersion = "1.14"

    elif MinorVersion > 22:
        #Too new.
        BestVersion = "1.22"

    else:
        #Supported version.
        BestVersion = DDRescueVersion

    SuitableFunctions = []

    for Function in Functions:
        if BestVersion in Function.SUPPORTEDVERSIONS:
            SuitableFunctions.append(Function)

    return SuitableFunctions
