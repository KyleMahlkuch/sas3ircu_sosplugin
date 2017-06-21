# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.



#Much of this code is from Rodrigo Rosatti Galvao's nvme plugin
#I used it as a jumping off point



from sos.plugins import Plugin, RedHatPlugin, DebianPlugin, UbuntuPlugin
import os


class LSIAdapter(Plugin, RedHatPlugin, DebianPlugin, UbuntuPlugin):

    plugin_name = "lsiadapter"
    packages = ('scsi0',) #*** need to figure out correct package

    def get_devices(self):
        devices = [dev for dev in os.listdir('/sys/bus/scsi/devices/')] #*** which device(s) will I need?

        return devices

#*** comment out copied code, do I need this functions?
    ''' 
    def check_fw_mode(self, cat_cpuinfo_out):
        """ Recieves the output from 'cat /proc/cpuinfo' and check whether the firmware
        mode is OPAL or not """
        for line in cat_cpuinfo_out.splitlines():
            if "firmware" in line:
                if "OPAL" in line:
                    return True
                else:
                    return False
        return False
    '''

    def get_block_size(self, cmd_lsblk_out, dev):
        """ Recieves the output from 'lsblk' and get the block size for the
        specified device"""
        for line in cmd_lsblk_out.splitlines():
            if dev in line:
                return line.split()[3]
        return

    def get_pci_slot_location(self, cmd_lscfg_out, op):
        """ Recieves the output from 'lscfg -vl <device-name>' and get the line
        corresponding to 'mass-storage' or 'pci', depending of the firmware
        mode """
        for line in cmd_lscfg_out.splitlines():
            if op in line:
                return line.split()
        return []



    def setup(self):

        '''
        # check if the firmware mode is OPAL
        cat_cpuinfo = self.call_ext_prog("cat /proc/cpuinfo")
        if cat_cpuinfo['status'] == 0:
            is_opal = self.check_fw_mode(cat_cpuinfo['output'])
            if is_opal:
                op = "mass-storage"
            else:
                op = "pci"
        '''
        #instead of current func, use sas3ircu list for list of devices. 
        for dev in self.get_devices():

            # get block size
            cmd_lsblk = self.call_ext_prog("lsblk")
            if cmd_lsblk['status'] == 0:
                blk_size = self.get_block_size(cmd_lsblk['output'], dev)
                self.add_string_as_file(blk_size, "block-size.%s" % dev)


            # get info about slot location and pci location
            cmd_lscfg = self.call_ext_prog("lscfg -vl %s" % dev[0:-2])
            if cmd_lscfg['status'] == 0:
                pci_slot_location = self.get_pci_slot_location(
                                cmd_lscfg['output'], op)

                if pci_slot_location:
                    pci_loc = pci_slot_location[0]
                    slot_loc = pci_slot_location[3]
                    self.add_string_as_file(pci_loc, "pci_loc.%s" % dev)
                    self.add_string_as_file(slot_loc, "slot_loc.%s" % dev)

           

            #example input

            cont_num = 0 
            
            #runs commands

            self.add_cmd_output([
                                "sas3ircu LIST",
                                "sas3ircu {} DISPLAY".format(cont_num)
                                ])

            #which commands do we want? start with list and display
            #other commands

            '''
                                "sas3ircu {} CREATE {} {}".format(cont_num, vol_type, size),
                                "sas3ircu {} DELETE".format(cont_num),
                                "sas3ircu {} DELETEVOLUME {}".format(cont_num, volID),

                                "sas3ircu {} HOTSPARE {}".format(cont_num, enc_bay),
                                "sas3ircu {} STATUS".format(cont_num),

                                "sas3ircu {} CONSTCHK {}".format(cont_num, volID),
                                "sas3ircu {} ACTIVATE {}".format(cont_num, volID),
                                "sas3ircu {} LOCATE {} {}".format(cont_num, enc_bay, action),
                                "sas3ircu {} LOGIR {}".format(cont_num, action), 
                                "sas3ircu {} BOOTIR {}".format(cont_num, volID),
                                "sas3ircu {} BOOTENCL {}".format(cont_num, enc_bay),
                                "sas3ircu HELP {}".format(command_name),
                               ])
            '''

            #more example inputs
            '''
            vol_type = "RAID 0"
            size = 16
            volID = "id"
            enc_bay = 1
            action = "ON" #"OFF"
            command_name = "CREATE"
            '''



















