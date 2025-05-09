# Anton Kirilenko, 2012,
# Licensed under GPL, see http://www.gnu.org/licenses/gpl-2.0.html
# for the whole text
#
# This script will look-up command in the database and print
# possible commands with their packages.

command_not_found_handle() {
  if  [ -x /usr/bin/cnf ]; then
     /usr/bin/cnf -- "$1"
     return $?
  else
     return 127
  fi        
} 
