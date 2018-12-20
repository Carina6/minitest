# Author: Chema Garcia (aka sch3m4)
# Contact: chema@safetybits.net | @sch3m4 | http://safetybits.net/contact
# Homepage: http://safetybits.net
# Project Site: http://github.com/sch3m4/pyadb


import os
import re
import subprocess
import sys
import threading

from logger import get_logger
from minitest.core.android.adb import ADB_PATH

LOGGER = get_logger(__name__)


class ADB(object):
    PYADB_VERSION = "0.1.5"

    __adb_path = None
    __output = None
    __error = None
    __return = 0
    __devices = None
    __target = None

    # reboot modes
    REBOOT_RECOVERY = 1
    REBOOT_BOOTLOADER = 2

    # default TCP/IP port
    DEFAULT_TCP_PORT = 5555
    # default TCP/IP host
    DEFAULT_TCP_HOST = "localhost"

    def pyadb_version(self):
        return self.PYADB_VERSION

    def __init__(self, adb_path=str(ADB_PATH), host=None, port=None, serial=None):
        self.__adb_path = adb_path
        self.host = host if host else '127.0.0.0'
        self.port = port if port else 5037
        self.serial = serial

        self._set_opt_cmd()

    def __clean__(self):
        self.__output = None
        self.__error = None
        self.__return = 0

    def __parse_output__(self, outstr):
        ret = None

        if (len(outstr) > 0):
            ret = outstr.splitlines()

        return ret

    def __build_command__(self, cmd):
        ret = None

        if self.__devices is not None and len(self.__devices) > 1 and self.__target is None and "devices" not in cmd:
            self.__error = "Must set target device first"
            self.__return = 1
            return ret

        # Modified function to directly return command set for Popen
        #
        # Unfortunately, there is something odd going on and the argument list is not being properly
        # converted to a string on the windows 7 test systems.  To accomodate, this block explitely
        # detects windows vs. non-windows and builds the OS dependent command output
        #
        # Command in 'list' format: Thanks to Gil Rozenberg for reporting the issue
        #
        if sys.platform.startswith('win'):
            ret = self.__adb_path + " "
            if (self.__target is not None):
                ret += "-s " + self.__target + " "
            if type(cmd) == type([]):
                ret += ' '.join(cmd)
            else:
                ret += cmd
        else:
            ret = [self.__adb_path]
            if (self.__target is not None):
                ret += ["-s", self.__target]

            if type(cmd) == type([]):
                for i in cmd:
                    ret.append(i)
            else:
                ret += [cmd]

        return ret

    def get_output(self):
        return self.__output

    def get_error(self):
        return self.__error

    def get_return_code(self):
        return self.__return

    def last_failed(self):
        """
        Did the last command fail?
        """
        if self.__output is None and self.__error is not None and self.__return:
            return True
        return False

    def run_cmd(self, cmd):
        """
        Runs a command by using adb tool ($ adb <cmd>)
        """
        self.__clean__()

        if self.__adb_path is None:
            self.__error = "ADB path not set"
            self.__return = 1
            return

        # For compat of windows
        cmd_list = self.__build_command__(cmd)
        LOGGER.info(cmd_list)

        try:
            adb_proc = subprocess.Popen(cmd_list, stdin=subprocess.PIPE, \
                                        stdout=subprocess.PIPE, \
                                        stderr=subprocess.PIPE, shell=False)
            (self.__output, self.__error) = adb_proc.communicate()
            self.__return = adb_proc.returncode
            self.__output = self.__output.decode('utf-8')
            self.__error = self.__error.decode('utf-8')

            if (len(self.__output) == 0):
                self.__output = None
            else:
                self.__output = [x.strip() for x in self.__output.split('\n') if len(x.strip()) > 0]

            if (len(self.__error) == 0):
                self.__error = None

        except:
            pass

        return (self.__error, self.__output)

    def get_version(self):
        """
        Returns ADB tool version
        adb version
        """
        self.run_cmd("version")
        try:
            ret = self.__output[0].split()[-1:][0]
        except:
            ret = None
        return ret

    def check_path(self):
        """
        Intuitive way to verify the ADB path
        """
        if self.get_version() is None:
            return False
        return True

    def set_adb_path(self, adb_path):
        """
        Sets ADB tool absolute path
        """
        if os.path.isfile(adb_path) is False:
            return False
        self.__adb_path = adb_path
        return True

    def get_adb_path(self):
        """
        Returns ADB tool path
        """
        return self.__adb_path

    def start_server(self):
        """
        Starts ADB server
        adb start-server
        """
        self.__clean__()
        self.run_cmd('start-server')
        return self.__output

    def kill_server(self):
        """
        Kills ADB server
        adb kill-server
        """
        self.__clean__()
        self.run_cmd('kill-server')

    def restart_server(self):
        """
        Restarts ADB server
        """
        self.kill_server()
        return self.start_server()

    def restore_file(self, file_name):
        """
        Restore device contents from the <file> backup archive
        adb restore <file>
        """
        self.__clean__()
        self.run_cmd(['restore', file_name])
        return self.__output

    def wait_for_device(self):
        """
        Blocks until device is online
        adb wait-for-device
        """
        self.__clean__()
        self.run_cmd('wait-for-device')
        return self.__output

    def get_help(self):
        """
        Returns ADB help
        adb help
        """
        self.__clean__()
        self.run_cmd('help')
        return self.__output

    def get_devices(self):
        """
        Returns a list of connected devices
        adb devices
        mode serial/usb
        """
        error = 0
        self.__devices = None
        self.run_cmd("devices")
        if self.__error is not None:
            return (1, self.__devices)
        try:
            self.__devices = [x.split()[0] for x in self.__output[1:]]
        except Exception as e:
            self.__devices = None
            error = 2

        return (error, self.__devices)

    def set_target_device(self, device):
        """
        Select the device to work with
        """
        self.__clean__()
        if device is None or not device in self.__devices:
            self.__error = 'Must get device list first'
            self.__return = 1
            return False
        self.__target = device
        return True

    def get_target_device(self):
        """
        Returns the selected device to work with
        """
        return self.__target

    def get_state(self):
        """
        Get ADB state
        adb get-state
        """
        self.__clean__()
        self.run_cmd('get-state')
        return self.__output

    def get_serialno(self):
        """
        Get serialno from target device
        adb get-serialno
        """
        self.__clean__()
        self.run_cmd('get-serialno')
        return self.__output

    def reboot_device(self, mode):
        """
        Reboot the target device
        adb reboot recovery/bootloader
        """
        self.__clean__()
        if not mode in (self.REBOOT_RECOVERY, self.REBOOT_BOOTLOADER):
            self.__error = "mode must be REBOOT_RECOVERY/REBOOT_BOOTLOADER"
            self.__return = 1
            return self.__output
        self.run_cmd(["reboot", "%s" % "recovery" if mode == self.REBOOT_RECOVERY else "bootloader"])
        return self.__output

    def set_adb_root(self):
        """
        restarts the adbd daemon with root permissions
        adb root
        """
        self.__clean__()
        self.run_cmd('root')
        return self.__output

    def set_system_rw(self):
        """
        Mounts /system as rw
        adb remount
        """
        self.__clean__()
        self.run_cmd("remount")
        return self.__output

    def get_remote_file(self, remote, local):
        """
        Pulls a remote file
        adb pull remote local
        """
        self.__clean__()
        self.run_cmd(['pull', remote, local])

        if self.__error is not None and "bytes in" in self.__error:
            self.__output = self.__error
            self.__error = None

        return self.__output

    def push_local_file(self, local, remote):
        """
        Push a local file
        adb push local remote
        """
        self.__clean__()
        self.run_cmd(['push', local, remote])
        return self.__output

    def shell_command(self, cmd):
        """
        Executes a shell command
        adb shell <cmd>
        """
        self.__clean__()
        self.run_cmd(['shell', cmd])
        return self.__output

    def listen_usb(self):
        """
        Restarts the adbd daemon listening on USB
        adb usb
        """
        self.__clean__()
        self.run_cmd("usb")
        return self.__output

    def listen_tcp(self, port=DEFAULT_TCP_PORT):
        """
        Restarts the adbd daemon listening on the specified port
        adb tcpip <port>
        """
        self.__clean__()
        self.run_cmd(['tcpip', port])
        return self.__output

    def get_bugreport(self):
        """
        Return all information from the device that should be included in a bug report
        adb bugreport
        """
        self.__clean__()
        self.run_cmd("bugreport")
        return self.__output

    def get_jdwp(self):
        """
        List PIDs of processes hosting a JDWP transport
        adb jdwp
        """
        self.__clean__()
        self.run_cmd("jdwp")
        return self.__output

    def get_logcat(self, lcfilter=""):
        """
        View device log
        adb logcat <filter>
        """
        self.__clean__()
        self.run_cmd(['logcat', lcfilter])
        return self.__output

    def run_emulator(self, cmd=""):
        """
        Run emulator console command
        """
        self.__clean__()
        self.run_cmd(['emu', cmd])
        return self.__output

    def connect_remote(self, host=DEFAULT_TCP_HOST, port=DEFAULT_TCP_PORT):
        """
        Connect to a device via TCP/IP
        adb connect host:port
        """
        self.__clean__()
        self.run_cmd(['connect', "%s:%s" % (host, port)])
        return self.__output

    def disconnect_remote(self, host=DEFAULT_TCP_HOST, port=DEFAULT_TCP_PORT):
        """
        Disconnect from a TCP/IP device
        adb disconnect host:port
        """
        self.__clean__()
        self.run_cmd(['disconnect', "%s:%s" % (host, port)])
        return self.__output

    def ppp_over_usb(self, tty=None, params=""):
        """
        Run PPP over USB
        adb ppp <tty> <params>
        """
        self.__clean__()
        if tty is None:
            return self.__output

        cmd = ["ppp", tty]
        if params != "":
            cmd += params

        self.run_cmd(cmd)
        return self.__output

    def sync_directory(self, directory=""):
        """
        Copy host->device only if changed (-l means list but don't copy)
        adb sync <dir>
        """
        self.__clean__()
        self.run_cmd(['sync', directory])
        return self.__output

    def forward_socket(self, local=None, remote=None):
        """
        Forward socket connections
        adb forward <local> <remote>
        """
        self.__clean__()
        if local is None or remote is None:
            return self.__output
        self.run_cmd(['forward', local, remote])
        return self.__output

    def uninstall(self, package=None, keepdata=False):
        """
        Remove this app package from the device
        adb uninstall [-k] package
        """
        self.__clean__()
        if package is None:
            return self.__output

        cmd = 'uninstall '
        if keepdata:
            cmd += '-k '
        cmd += package
        self.run_cmd(cmd.split())
        return self.__output

    def install(self, fwdlock=False, reinstall=False, sdcard=False, pkgapp=None):
        """
        Push this package file to the device and install it
        adb install [-l] [-r] [-s] <file>
        -l -> forward-lock the app
        -r -> reinstall the app, keeping its data
        -s -> install on sdcard instead of internal storage
        """

        self.__clean__()
        if pkgapp is None:
            return self.__output

        cmd = "install "
        if fwdlock is True:
            cmd += "-l "
        if reinstall is True:
            cmd += "-r "
        if sdcard is True:
            cmd += "-s "

        cmd += pkgapp
        self.run_cmd(cmd.split())
        return self.__output

    def find_binary(self, name=None):
        """
        Look for a binary file on the device
        """

        self.run_cmd(['shell', 'which', name])

        if self.__output is None:  # not found
            self.__error = "'%s' was not found" % name
        elif self.__output[0] == "which: not found":  # 'which' binary not available
            self.__output = None
            self.__error = "which binary not found"

    def shell_command_ext(self, cmd):
        self.__clean__()

        if self.__adb_path is None:
            self.__error = "ADB path not set"
            self.__return = 1
            return

        cmd_list = self.__build_command__(['shell', cmd])
        LOGGER.info(cmd_list)

        adb_proc = subprocess.Popen(cmd_list,
                                    stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    shell=False)

        return adb_proc

    def run_cmd_ext(self, cmd):
        self.__clean__()

        if self.__adb_path is None:
            self.__error = "ADB path not set"
            self.__return = 1
            return

        cmd_list = self.__build_command__(cmd)
        LOGGER.info(cmd_list)

        adb_proc = subprocess.Popen(cmd_list,
                                    stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    shell=False)

        return adb_proc

    def get_package_version(self, package):
        """
        Perform `adb shell dumpsys package` and search for information about given package version

        Args:
            package: package name

        Returns:
            None if no info has been found, otherwise package version

        """
        outputs = self.shell_command('dumpsys package {}'.format(package))

        for output in outputs:
            matcher = re.search(r'versionCode=(\d+)', output)
            if matcher:
                return int(matcher.group(1))
        return None

    def start_app(self, package, activity=None):
        """
         Perform `adb shell monkey` commands to start the application, if `activity` argument is `None`, then
         `adb shell am start` command is used.

         Args:
             package: package name
             activity: activity name

         Returns:
             None

         """
        if activity is None:
            self.shell_command('monkey -p {} -c android.intent.category.LAUNCHER 1'.format(package))
        else:
            self.shell_command('am start -n {}/.{}'.format(package, activity))

    def start_app_timing(self, package, activity):
        """
        Start the application and activity, and measure time

        Args:
            package: package name
            activity: activity name

        Returns:
            app launch time

        """
        return self.shell_command(
            'am start -S -W {}/{} -c android.intent.category.LAUNCHER -a android.intent.action.MAIN'.format(
                package, activity))

    def stop_app(self, package):
        """
        Perform `adb shell am force-stop` command to force stop the application

        Args:
            package: package name

        Returns:
            None

        """
        return self.shell_command('am force-stop {}'.format(package))

    def key_events(self, event):
        self.shell_command('input keyevent {}'.format(event.upper()))

    def app_path(self, package):
        """
        Perform `adb shell pm path` command to print the path to the package

        Args:
            package: package name

        Raises:
            AdbShellError: if any adb error occurs
            AirtestError: if package is not found on the device

        Returns:
            path to the package

        """

        return self.shell_command('pm path {}'.format(package))[0]

    def pull(self, remote, local):
        return self.run_cmd([remote, local])

    def _set_opt_cmd(self):
        # self.opt_cmd = [self.__adb_path]
        self.opt_cmd = []

        if self.host not in ['localhost', '127.0.0.0']:
            self.opt_cmd += ['-H', self.host]
            self.opt_cmd += ['-P', self.port]
            self.opt_cmd += ['-s', self.serial]

    def wait_for_device_ext(self, timeout=5):
        self.opt_cmd += ['wait-for-device']
        proc = self.run_cmd_ext(self.opt_cmd)
        timer = threading.Timer(timeout, proc.kill)
        timer.start()
        ret = proc.wait()
        if ret == 0:
            timer.cancel()
        else:
            raise RuntimeError('device not ready')

    def app_list(self, third_only):
        """
        Perform `adb shell pm list packages` to print all packages, optionally only
          those whose package name contains the text in FILTER.

        Options
            -f: see their associated file
            -d: filter to only show disabled packages
            -e: filter to only show enabled packages
            -s: filter to only show system packages
            -3: filter to only show third party packages
            -i: see the installer for the packages
            -u: also include uninstalled packages


        Args:
            third_only: print only third party packages

        Returns:
            list of packages

        """
        cmd = 'pm list packages'
        if third_only:
            cmd += ' -3'
        out = self.shell_command(cmd)
        return [p.split(':')[1] for p in out if p]

    def check_app(self, package):
        """
         Perform `adb shell dumpsys package` command and check if package exists on the device

         Args:
             package: package name

         Raises:
             AirtestError: if package is not found

         Returns:
             True if package has been found

         """
        out = self.shell_command('dumpsys package {}'.format(package))
        if out:
            return True
        else:
            return False

    def clear_app(self, package):
        """
         Perform `adb shell pm clear` command to clear all application data

         Args:
             package: package name

         Returns:
             None

         """
        return self.shell_command('pm clear {}'.format(package))

    # def logcat(self, grep_str="", extra_args="", read_timeout=10):
    #     cmd = 'logcat'
    #     if grep_str:
    #         cmd += ' {}'.format(grep_str)
    #
    #     if extra_args:
    #         cmd += ' |grep {}'.format(extra_args)
    #
    #     proc = self.shell_command_ext(cmd)
    #     nplc = NonBlockingStreamReader(proc.stdout)
    #     while True:
    #         line = nplc.readline(timeout=read_timeout)
    #         if line is None:
    #             break
    #         else:
    #             yield line
    #
    #     proc.kill()

    def getprop(self, key, strip):
        """
         Perform `adb shell getprop` on the device

         Args:
             key: key value for property
             strip: True or False to strip the return carriage and line break from returned string

         Returns:
             propery value

         """
        out = self.shell_command('getprop {}'.format(key))
        out = out[0]
        if strip:
            out.rstrip('\r\n')

        return out

    def get_ip_address(self):
        """
        Perform several set of commands to obtain the IP address
            * `adb shell netcfg | grep wlan0`
            * `adb shell ifconfig`
            * `adb getprop dhcp.wlan0.ipaddress`

        Returns:
            None if no IP address has been found, otherwise return the IP address

        """

        def ip_address(interface):
            res = self.shell_command('netcfg')
            if res is None:
                res = ''
            matcher = re.search(interface + r'.* ((\d+\.){3}\d+)/\d+', str(res))

            if matcher:
                return matcher.group(1)

            res = self.shell_command('ifconfig')
            if res is None:
                res = ''
            matcher = re.search(interface + r'.*?inet addr:((\d+\.){3}\d+)', str(res), re.DOTALL)
            if matcher:
                return matcher.group(1)

            res = self.shell_command('getprop dhcp.{}.ipaddress'.format(interface))
            if res is None:
                res = ''
            matcher = re.search(interface + r'.* ((\d+\.){3}\d+)/\d+', str(res))

            if matcher:
                return matcher.group(1)

        interfaces = ['wlan0', 'eth0', 'eth1']
        for i in interfaces:
            ip = ip_address(i)
            if ip and not ip.startswith('172.') and not ip.startswith('127.') and not ip.startswith('169.'):
                return ip

        return None

    def get_top_activity_info(self):
        """
        Perform `adb shell dumpsys activity top` command search for the top activity

        Raises:
            AirtestError: if top activity cannot be obtained

        Returns:
            top activity as a tuple

        """
        return self.shell_command('dumpsys activity top')

    def get_input_method_info(self):
        """
        Perform `adb shell dumpsys input_method` command and search for information if keyboard is shown

        Returns:
            True or False whether the keyboard is shown or not

        """
        return self.shell_command('dumpsys input_method')

    def get_window_policy_info(self):
        """
        Perform `adb shell dumpsys window policy` command and search for information if screen is turned on or off

        Raises:
            AirtestError: if screen state can't be detected

        Returns:
            True or False whether the screen is turned on or off

        """
        return self.shell_command('dumpsys window policy')
