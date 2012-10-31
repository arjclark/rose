#!/usr/bin/env python

import os
import sys

import command_pages

#os.getenv("ROSE_HOME")
sys.path.append("../lib/python/")
from rose.popen import RosePopener

BOOKMARK_LINK = "<a HREF=\"#{0}-{1}\">{0} {1}</a>"
CMD_HELP_FORMAT = "{0} help {1}"
CODE_FORMAT = "<kbd>{0}</kbd>"
H2_FORMAT = "<h2>{0}</h2>"
SECTION_ANCHOR = "<a NAME=\"{0}-{1}\">"
KNOWN_SECTIONS = ["NAME","SYNOPSIS", "DESCRIPTION", "OPTION", "CONFIGURATION",
                  "ARGUMENTS", "SEE ALSO", "NOTE ON CYCLE TIME", "ENVIRONMENT"]


def html_writer(content=None):
    """generate the appropriate html code"""

    content, cmds = prog_hlp_formatter(content)

    #print "<pre>"
    for row in content:
        if not row == "":
            print row
    
    for c in cmds['rose']:
        if c is not "":
            print "<hr/>"
            print SECTION_ANCHOR.format('rose', c) + "<h2>rose " + c + "</h2></a><br>"
            cmd_hlp = help_grabber("rose", c)
            cmd_hlp = cmd_hlp_formatter(cmd_hlp, "rose", c)
            for l in cmd_hlp:
                print l
            
    for c in cmds['rosie']:
        if c is not "":
            print "<hr/>"
            print SECTION_ANCHOR.format('rosie', c) + "<h2>rosie " + c + "</h2></a><br>"
            cmd_hlp = help_grabber("rosie", c)
            cmd_hlp = cmd_hlp_formatter(cmd_hlp, "rosie", c)
            for l in cmd_hlp:
                print l
    #print "</pre>"

def cmd_hlp_formatter(content, prog, cmd):
    """html format help from program commands"""

    keys = []
    
    for row in content:
        if row.split(" ")[0].isupper():
            keys.append(row.split(" ")[0])
    
    cmd_page = command_pages.CmdPage(keys, prog, cmd)
    
    mode = "reading"

    for i, row in enumerate(content):
    
        if row.startswith("NAME"):
            mode = "name"
        elif row.startswith("DESCRIPTION"):
            mode = "description"
        elif row.startswith("SYNOPSIS"):
            mode = "synopsis"
        elif row.startswith("OPTION"):
            mode = "option"
        elif row.split(" ")[0].isupper():
            mode = row.split(" ")[0]

        if mode == "name":
            cmd_page.content['NAME'].append(row)
            if row.startswith(" "*4 + prog):
                content[i] = "<kbd>"+ row + "</kbd><br>"
            else:
                content[i] = row + "<br>"
        elif mode == "synopsis":
            cmd_page.content['SYNOPSIS'].append(row)
            if row.startswith(" "*4 + prog):
                content[i] = "<kbd>"+ row + "</kbd><br>"
            else:
                content[i] = row + "<br>"
        elif mode == "option":
            cmd_page.content['OPTION'].append(row)
            if row.startswith(" "*4 + "-"):
                content[i] = "<kbd>"+ row + "</kbd><br>"
            else:
                content[i] = row + "<br>"
        else:
            cmd_page.content[mode].append(row)
            content[i] = row + "<br>"

    print "cmd formatter printed this:"
    cmd_page.print_html()
    
                                        
    return content

def prog_hlp_formatter(content):
    """html format help from programs"""
    cmds = {}
    cmds['rose'] = []
    cmds['rosie'] = []
    curr_block = ""
    for i, row in enumerate(content):
        if not row.startswith("usage: "):
            if row.startswith("rose"):
                content[i] = row.replace("rose", CODE_FORMAT.format("rose"), 1) + "<br>"
                curr_block = "rose"
            elif row.startswith("rosie"):
                content[i] = row.replace("rosie", CODE_FORMAT.format("rosie"), 1) + "<br>"
                curr_block = "rosie"
            else:
                if row.startswith(" "*4) and not row.startswith(" "*8):
                    tmp = row.split(" ")
                    cmd = tmp[4]
                    if cmd == curr_block or cmd.endswith("~"):
                        warnings['cmd'] += 1
                    else:
                        if not cmd.endswith("~"):
                            cmds[curr_block].append(cmd)
                    tmp[4] = BOOKMARK_LINK.format(curr_block, tmp[4])+"</a>"
                    content[i] = " ".join(tmp) + " - "
                elif row.startswith(" ") and (not row.startswith(" "*4)) and (not row.startswith(" "*8)):
                    warnings['indentation'] += 1
                else:
                    content[i] = row + "<br>"
        else:
             content[i] = ""    
    
    return content, cmds
    
def help_grabber(prog, cmd=""):
    popen = RosePopener()
    try:
        rows = popen(CMD_HELP_FORMAT.format(prog, cmd), shell=True)[0].split("\n")
    except:
        rows = []
    return rows

if __name__ == "__main__":
    show_warnings = False
    warnings = {}
    warnings['indentation'] = 0
    warnings['cmd'] = 0
    content = help_grabber("rose")
    content = content + help_grabber("rosie")
    html_writer(content)
    if show_warnings:
        if warnings['indentation'] > 0:
            print "%s indentation warnings found"%warnings['indentation']
        if warnings['cmd'] > 0:
            print "%s command warnings found"%warnings['cmd']
    
