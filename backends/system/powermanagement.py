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
import stat
import dbus.service

from backends.globals import *


class SysCtl(dbus.service.Object):
    """ Manage sysctl options """

    def __init__(self, conn=None, object_path=None, bus_name=None):
        dbus.service.Object.__init__(self, conn, object_path, bus_name)
        self.available = self.IsAvailable()

    def __write(self, file, option, value):
        """ Write the 'option = value' in the 'file' configfile. """
        """ If 'option' is not found in the config file, add it. """
        """ Return "True" on success, "False" otherwise. """
        if not self.available:
            return False

        optionfound = False
        try:
            oldfile = open(file, "r")
        except:
            systemlog.write(
                "ERROR: 'SysCtl.__write()' - '" + file + "' not found.")
            return False
        try:
            newfile = open(file + ".new", "w")
        except:
            systemlog.write(
                "ERROR: 'SysCtl.__write()' - cannot write the new config file.")
            oldfile.close()
            return False
        for line in oldfile:
            if line[0:1] == "#" or line == "\n":
                newfile.write(line)
            else:
                currentoption = line.split('=')[0].strip()
                if currentoption != option:  # not the option we are searching for
                    newfile.write(line)
                else:
                    optionfound = True
                    try:
                        newfile.write(option + " = " + value + "\n")
                    except:
                        systemlog.write(
                            "ERROR: 'SysCtl.__write()' - cannot write the new value for '" + option +
                            "' in the new config file.")
                        oldfile.close()
                        newfile.close()
                        os.remove(file + ".new")
                        return False
        oldfile.close()
        if not optionfound:  # option not found in current config file, add it
            newfile.write(option + " = " + value + "\n")
        newfile.close()
        try:
            os.remove(file)
        except:
            systemlog.write(
                "ERROR: 'SysCtl.__write()' - cannot replace old '" + file + "' with the new version.")
            os.remove(file + ".new")
            return False
        shutil.move(file + ".new", file)
        return True

    def __read(self, file, option):
        """ Read the 'option' value in the 'file' configfile. """
        """ Return the read value, or 'None' if any error. """
        if not self.available:
            return None
        try:
            f = open(file, "r")
        except:
            systemlog.write(
                "ERROR: 'SysCtl.__read()' - '" + file + "' not found.")
            return None
        for line in f:
            if line[0:1] != "#" and line != "\n":
                currentoption = line.split('=')[0].strip()
                if currentoption == option:
                    f.close()
                    return line.split('=')[1].strip()
        # Option not found
        f.close()
        return None

    @dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature=None, out_signature='b',
                         sender_keyword='sender', connection_keyword='conn')
    def IsAvailable(self, sender=None, conn=None):
        if not os.path.exists(SYSCTL_CONFIG_FILE):
            try:
                open(SYSCTL_CONFIG_FILE, "w").close()
            except:
                systemlog.write(
                    "ERROR: 'SysCtl.IsAvailable()' - cannot write the config file.")
                return False
        return True

    @dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature=None, out_signature='i',
                         sender_keyword='sender', connection_keyword='conn')
    def GetSwappiness(self, sender=None, conn=None):
        from subprocess import Popen, PIPE
        command = COMMAND_SYSCTL + " vm.swappiness"
        process = Popen(command.split(), stdout=PIPE, stderr=PIPE)
        return int(process.communicate()[0].split(" = ")[1])

    @dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature='i', out_signature='b',
                         sender_keyword='sender', connection_keyword='conn')
    def SetSwappiness(self, value, sender=None, conn=None):
        if value < 0 or value > 100:
            return False
        return self.__write(SYSCTL_CONFIG_FILE, "vm.swappiness", str(value))

    @dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature=None, out_signature='b',
                         sender_keyword='sender', connection_keyword='conn')
    def ApplySettings(self, sender=None, conn=None):
        from subprocess import Popen, PIPE
        try:
            value = self.__read(SYSCTL_CONFIG_FILE, "vm.swappiness")
            if value is None:
                return False

            command = COMMAND_SYSCTL + " vm.swappiness=" + value
            process = Popen(command.split(), stdout=PIPE, stderr=PIPE)
            process.communicate()
            if process.returncode != 0:
                systemlog.write(
                    "ERROR: 'SysCtl.ApplySettings()' - COMMAND: '" + command + "' FAILED.")
                return False
            return True
        except:
            systemlog.write(
                "ERROR: 'SysCtl.ApplySettings()' - COMMAND: '" + command + "' - Exception thrown.")
            return False


class PowerManagement(dbus.service.Object):
    """ Manage power save options """

    def __init__(self, conn=None, object_path=None, bus_name=None):
        dbus.service.Object.__init__(self, conn, object_path, bus_name)

    @dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature=None, out_signature='b',
                         sender_keyword='sender', connection_keyword='conn')
    def IsValid(self, script, sender=None, conn=None):
        """ Check if the script exists and if it's one of the scripts we can manage. """
        """ Return "True" if it exists and we can work on it, "False" otherwise. """
        # Check if the script is one of the scripts of Samsung Tools,
        # in order to avoid security issues.
        if script in PM_SCRIPTS:
            return os.access(script, os.F_OK)
        return False

    @dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature=None, out_signature='b',
                         sender_keyword='sender', connection_keyword='conn')
    def IsEnabled(self, script, sender=None, conn=None):
        """ Check if the script has the executable bit set. """
        """ Return "True" if it's set, "False" otherwise. """
        if not self.IsValid(script):
            return False
        return os.access(script, os.X_OK)

    @dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature=None, out_signature='b',
                         sender_keyword='sender', connection_keyword='conn')
    def Enable(self, script, sender=None, conn=None):
        """ Set the executable bit on script. """
        """ Return 'True' on success, 'False' otherwise. """
        if not self.IsValid(script):
            return False
        # Make script 755
        os.chmod(script, stat.S_IRWXU | stat.S_IRGRP |
                 stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
        # Check if everything is ok and return the result
        return os.access(script, os.X_OK)

    @dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature=None, out_signature='b',
                         sender_keyword='sender', connection_keyword='conn')
    def Disable(self, script, sender=None, conn=None):
        """ Unset the executable bit on script. """
        """ Return 'True' on success, 'False' otherwise. """
        if not self.IsValid(script):
            return False
        # Make script 644
        os.chmod(script, stat.S_IRUSR | stat.S_IWUSR |
                 stat.S_IRGRP | stat.S_IROTH)
        # Check if everything is ok and return the result
        return not os.access(script, os.X_OK)

    @dbus.service.method(SYSTEM_INTERFACE_NAME, in_signature=None, out_signature='b',
                         sender_keyword='sender', connection_keyword='conn')
    def Toggle(self, script, sender=None, conn=None):
        """ Toggle the executable bit on script. """
        """ Return 'True' on success, 'False' otherwise. """
        if self.IsEnabled(script):
            return self.Disable(script)
        else:
            return self.Enable(script)
