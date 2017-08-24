# coding=UTF-8
#
# Samsung-Tools
#
# Part of the 'Linux On My Samsung' project - <http://loms.voria.org>
#
# Copyleft (C) 2010 by
# Fortunato Ventre - <vorione@gmail.com> - <http://www.voria.org>
#
# 'Samsung-Tools' is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# <http://www.gnu.org/licenses/gpl.txt>

import os
import shutil
import ConfigParser

from backends.globals import *

# Options defaults
USE_HOTKEYS_DEFAULT = "true"
BACKLIGHT_HOTKEY_DEFAULT = "XF86Launch1"
BLUETOOTH_HOTKEY_DEFAULT = "XF86Launch2"
CPU_HOTKEY_DEFAULT = "XF86Launch3"
WEBCAM_HOTKEY_DEFAULT = "Alt+KP_Insert"
WIRELESS_HOTKEY_DEFAULT = "XF86WLAN"
USE_HOTKEYS_ACCEPTED_VALUES = ['true', 'false']


class SessionConfig():
    """ Manage session service configuration file """

    def __init__(self, configfile):
        self.config = ConfigParser.SafeConfigParser()
        # Avoid to lowercase options names, this fixes Turkish locale
        self.config.optionxform = str
        self.configfile = configfile
        try:
            self.config.readfp(open(configfile, "r"))
        except:
            # configfile not found?
            # Use default options
            sessionlog.write(
                "WARNING: 'SessionConfig' - '" +
                configfile +
                "' not found. Using default values for all options.")
            self.config.add_section("Main")
            self.config.set("Main", "USE_HOTKEYS", USE_HOTKEYS_DEFAULT)
            self.config.set(
                "Main",
                "BACKLIGHT_HOTKEY",
                BACKLIGHT_HOTKEY_DEFAULT)
            self.config.set(
                "Main",
                "BLUETOOTH_HOTKEY",
                BLUETOOTH_HOTKEY_DEFAULT)
            self.config.set("Main", "CPU_HOTKEY", CPU_HOTKEY_DEFAULT)
            self.config.set("Main", "WEBCAM_HOTKEY", WEBCAM_HOTKEY_DEFAULT)
            self.config.set("Main", "WIRELESS_HOTKEY", WIRELESS_HOTKEY_DEFAULT)
        # Check if all options are specified in the config file
        else:
            if not self.config.has_section("Main"):
                self.config.add_section("Main")
            try:
                self.config.get("Main", "USE_HOTKEYS")
            except:
                self.config.set("Main", "USE_HOTKEYS", USE_HOTKEYS_DEFAULT)
            try:
                self.config.get("Main", "BACKLIGHT_HOTKEY")
            except:
                self.config.set(
                    "Main",
                    "BACKLIGHT_HOTKEY",
                    BACKLIGHT_HOTKEY_DEFAULT)
            try:
                self.config.get("Main", "BLUETOOTH_HOTKEY")
            except:
                self.config.set(
                    "Main",
                    "BLUETOOTH_HOTKEY",
                    BLUETOOTH_HOTKEY_DEFAULT)
            try:
                self.config.get("Main", "CPU_HOTKEY")
            except:
                self.config.set("Main", "CPU_HOTKEY", CPU_HOTKEY_DEFAULT)
            try:
                self.config.get("Main", "WEBCAM_HOTKEY")
            except:
                self.config.set("Main", "WEBCAM_HOTKEY", WEBCAM_HOTKEY_DEFAULT)
            try:
                self.config.get("Main", "WIRELESS_HOTKEY")
            except:
                self.config.set(
                    "Main",
                    "WIRELESS_HOTKEY",
                    WIRELESS_HOTKEY_DEFAULT)
        # Options sanity check
        if self.config.get(
                "Main", "USE_HOTKEYS") not in USE_HOTKEYS_ACCEPTED_VALUES:
            # Option is invalid, set default value
            sessionlog.write("WARNING: 'SessionConfig' - 'USE_HOTKEYS' option specified in '" +
                             configfile + "' is invalid. Using default value ('" + USE_HOTKEYS_DEFAULT + "').")
            self.config.set("Main", "USE_HOTKEYS", USE_HOTKEYS_DEFAULT)

    def __write(self, option):
        """ Write the new 'option' in the config file. """
        """ If 'option' does not exists in file, add it. """
        """ Return "True" on success, "False" otherwise. """
        # We don't use the ConfigParser builtin write function,
        # because it seems to be impossible to add comments to config file.
        value = self.config.get("Main", option)
        optionfound = False
        sectionfound = False
        try:
            oldfile = open(self.configfile, "r")
        except:
            sessionlog.write(
                "ERROR: 'SessionConfig.__write()' - '" +
                self.configfile +
                "' not found. Creating a new one.")
            try:
                shutil.copy(SESSION_CONFIG_FILE, self.configfile)
            except:
                sessionlog.write(
                    "ERROR: 'SessionConfig.__write()' - Cannot find the global user configuration file. " +
                    "Creating an empty one.")
                try:
                    oldfile = open(self.configfile, "w").close()
                except:
                    sessionlog.write(
                        "ERROR: 'SessionConfig.__write()' - Cannot create a new config file.")
                    return False
            try:
                oldfile = open(self.configfile, "r")
            except:
                sessionlog.write(
                    "ERROR: 'SessionConfig.__write()' - cannot read the config file.")
                return False
        try:
            newfile = open(self.configfile + ".new", "w")
        except:
            sessionlog.write(
                "ERROR: 'SessionConfig.__write()' - cannot write the new config file.")
            oldfile.close()
            return False
        for line in oldfile:
            if line[0:1] == "#" or line == "\n":
                newfile.write(line)
            elif line == "[Main]\n":
                newfile.write(line)
                sectionfound = True
            else:
                currentoption = line.split('=')[0].strip()
                if currentoption != option:  # not the option we are searching for
                    newfile.write(line)
                else:
                    optionfound = True
                    try:
                        newfile.write(option + "=" + value + "\n")
                    except:
                        sessionlog.write(
                            "ERROR: 'SessionConfig.__write()' - cannot write the new value for '" +
                            option +
                            "' in the new config file.")
                        oldfile.close()
                        newfile.close()
                        os.remove(self.configfile + ".new")
                        return False
        oldfile.close()
        if not sectionfound:  # probably an empty file, write section
            newfile.write("[Main]\n")
        if not optionfound:  # option not found in current config file, add it
            newfile.write(option + "=" + value + "\n")
        newfile.close()
        try:
            os.remove(self.configfile)
        except:
            sessionlog.write(
                "ERROR: 'SessionConfig.__write()' - cannot replace old '" +
                self.configfile +
                "' with the new version.")
            os.remove(self.configfile + ".new")
            return False
        shutil.move(self.configfile + ".new", self.configfile)
        return True

    def getUseHotkeys(self):
        """ Return the USE_HOTKEYS option. """
        return self.config.get("Main", "USE_HOTKEYS")

    def getBacklightHotkey(self):
        """ Return the BACKLIGHT_HOTKEY option. """
        return self.config.get("Main", "BACKLIGHT_HOTKEY")

    def getBluetoothHotkey(self):
        """ Return the BLUETOOTH_HOTKEY option. """
        return self.config.get("Main", "BLUETOOTH_HOTKEY")

    def getCpuHotkey(self):
        """ Return the CPU_HOTKEY option. """
        return self.config.get("Main", "CPU_HOTKEY")

    def getWebcamHotkey(self):
        """ Return the WEBCAM_HOTKEY option. """
        return self.config.get("Main", "WEBCAM_HOTKEY")

    def getWirelessHotkey(self):
        """ Return the WIRELESS_HOTKEY option. """
        return self.config.get("Main", "WIRELESS_HOTKEY")

    def setUseHotkeys(self, value):
        """ Set the USE_HOTKEYS option. """
        """ Return 'True' on success, 'False' otherwise. """
        if value == "default":  # set default
            value = USE_HOTKEYS_DEFAULT
        if value not in USE_HOTKEYS_ACCEPTED_VALUES:
            return False
        self.config.set("Main", "USE_HOTKEYS", value)
        return self.__write("USE_HOTKEYS")

    def setBacklightHotkey(self, value):
        """ Set the BACKLIGHT_HOTKEY option. """
        """ Return 'True' on success, 'False' otherwise. """
        if value == "default":  # set default
            value = BACKLIGHT_HOTKEY_DEFAULT
        self.config.set("Main", "BACKLIGHT_HOTKEY", value)
        return self.__write("BACKLIGHT_HOTKEY")

    def setBluetoothHotkey(self, value):
        """ Set the BLUETOOTH_HOTKEY option. """
        """ Return 'True' on success, 'False' otherwise. """
        if value == "default":  # set default
            value = BLUETOOTH_HOTKEY_DEFAULT
        self.config.set("Main", "BLUETOOTH_HOTKEY", value)
        return self.__write("BLUETOOTH_HOTKEY")

    def setCpuHotkey(self, value):
        """ Set the CPU_HOTKEY option. """
        """ Return 'True' on success, 'False' otherwise. """
        if value == "default":  # set default
            value = CPU_HOTKEY_DEFAULT
        self.config.set("Main", "CPU_HOTKEY", value)
        return self.__write("CPU_HOTKEY")

    def setWebcamHotkey(self, value):
        """ Set the WEBCAM_HOTKEY option. """
        """ Return 'True' on success, 'False' otherwise. """
        if value == "default":  # set default
            value = WEBCAM_HOTKEY_DEFAULT
        self.config.set("Main", "WEBCAM_HOTKEY", value)
        return self.__write("WEBCAM_HOTKEY")

    def setWirelessHotkey(self, value):
        """ Set the WIRELESS_HOTKEY option. """
        """ Return 'True' on success, 'False' otherwise. """
        if value == "default":  # set default
            value = WIRELESS_HOTKEY_DEFAULT
        self.config.set("Main", "WIRELESS_HOTKEY", value)
        return self.__write("WIRELESS_HOTKEY")
