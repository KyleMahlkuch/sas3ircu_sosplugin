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



#This sosreport plugin is meant for sas3ircu adapters.
#This plugin currently displays basic info about each adapter it finds.  


from sos.plugins import Plugin, RedHatPlugin, DebianPlugin, UbuntuPlugin
import os


class LSIAdapter(Plugin, RedHatPlugin, DebianPlugin, UbuntuPlugin):

    plugin_name = "lsiadapter"
    packages = ('scsi0',) #*** is this the correct package?


    def setup(self):

        output = self.call_ext_prog("sh -c '~/sas3ircu list'") #get list of adapters
        self.add_cmd_output(["sh -c '~/sas3ircu list'"])

        dev_lst = output["output"].splitlines()[10:-1] #just want devices
        print(dev_lst)

        for dev_info in dev_lst: #for each adapter get some basic info  
            dev_num = dev_info.split()[0]    
            self.add_cmd_output([
                                "sh -c '~/sas3ircu {} DISPLAY'".format(dev_num)
                                ])

