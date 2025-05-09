#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Anton Kirilenko, 2012,
# Licensed under GPL 2.0, see http://www.gnu.org/licenses/gpl-2.0.html
# for the whole text

import sys

import codecs

import gettext

gettext.bindtextdomain('command-not-found')
gettext.textdomain('command-not-found')

_ = gettext.gettext

if not sys.stderr.isatty():
    print(_("%s: command not found") % sys.argv[1], file=sys.stderr)
    exit(127)
    
safemode = True
import json
import argparse
import os

def get_installed_pkgs():
    '''Returns a list of installed packages names'''
    # we don't do it at the top of file because it takes too much time (0.1 sec).
    #if not rpm:
    rpm = __import__('rpm')
    ts = rpm.TransactionSet() 
    mi = ts.dbMatch() 
    output = []
    
    for h in mi: 
        output.append(h['name'])
    return output
    
def parse_command_line():
    global command_line
    arg_parser = argparse.ArgumentParser(description=_(' Search for commands in repository. Remember: a normal program exit code is 127!'), 
            # translating this string, do not care anout spaces or new lines, it will be autoformatted by argparse
            epilog=_('''In case of single possibile package, containing the given command,
            cnf will suggest you a command to install it and will ask you whether you want to do it right now
            (with question and y/N options). If you do not want cnf to ask user anything - 
            set COMMAND_NOT_FOUND_TURN_OFF_INSTALL_PROMPT environment variable to 1.'''))
    arg_parser.add_argument('command', action='store', nargs='?', help=_('Command to search for.'))
    args = sys.argv[1:]
    if not args:
        exit(127)
    command_line  = arg_parser.parse_args(args)
    
def similar_words(word):
    """
    return a set with spelling1 distance alternative spellings
    based on http://norvig.com/spell-correct.html
    """
    alphabet = 'abcdefghijklmnopqrstuvwxyz-_0123456789'
    s = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [a + b[1:] for a, b in s if b]
    transposes = [a + b[1] + b[0] + b[2:] for a, b in s if len(b) > 1]
    replaces = [a + c + b[1:] for a, b in s for c in alphabet if b]
    inserts = [a + c + b     for a, b in s for c in alphabet]
    return set(deletes + transposes + replaces + inserts)

def main():
    inst_prompt = 'COMMAND_NOT_FOUND_TURN_OFF_INSTALL_PROMPT'
    show_inst_prompts = True
    if inst_prompt in os.environ and os.environ[inst_prompt] == '1':
        show_inst_prompts = False

    parse_command_line()

    if not command_line.command:
        return
        
    with open('/usr/share/command-not-found/data.json', 'r') as fd:
        binaries = json.load(fd)

    param = command_line.command
    inst_pkgs = get_installed_pkgs()
    if param in binaries:
        
        print(_(" Command '%s' can be found in:") % param, file=sys.stderr)
        for item in binaries[param]:
            if item[1] in inst_pkgs:
                
                # mark that the package is already installed. Looks like e. g. (main, installed)
                installed = _(', installed')
            else:
                installed = ''
            print("    " + _("package") + " '%s' (%s%s)" % (item[1], item[0], installed), file=sys.stderr)
        if len(binaries[param]) == 1:
            if installed:
                to_try = ['/usr/sbin', '/sbin', '/usr/local/sbin']
                to_try = [x + '/' + param for x in to_try]
                for t in to_try:
                    if os.path.isfile(t):
                        print(_('File %s exists! Check your PATH variable, or call it using an absolute path.') % t)
                        break
            else:
                pkg = binaries[param][0][1]
                print(_(" You can install it by typing:"), file=sys.stderr)
                print("   sudo  dnf install %s" % pkg, file=sys.stderr)
                if show_inst_prompts:
                    res = input(_('Do you want to install it? (y/N)'))
                    # any not 'y' string rejects the installation
                    res = res.lower().strip()
                    if  res == _('y'):
                        os.system('sudo dnf install ' + pkg)
        return
        
    params = similar_words(param)
    found = []
    for p in params:
        if p in binaries:
            found.append(((p, binaries[p])))
                
    if not found:
        print(_("%s: command not found") % param)
        return
    print(_(" No command '%s' found, did you mean:") % (param), file=sys.stderr)
    for item in found:
        cmd_name, locations = item
        loc_string = ', '.join([(_("package") + " '%s' (%s)" % (c, r)) for r, c in locations])
        print(_("  Command '%(cmd)s' from %(locations)s") % {'cmd': cmd_name, 'locations': loc_string}, file=sys.stderr)
        

if __name__ == "__main__":
    if safemode:
        try:
            main()
        except:
            pass
        finally:
            #ever, EVER return 127!
            exit(127)
    else:
        main()
        exit(127)
