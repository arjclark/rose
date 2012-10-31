#!/usr/bin/env python

class CmdPage():

    """Class for converting man pages to html"""
    
    content = {}
    H2_MASK = "<h2>{0} {1}</h2>"
    H3_MASK = "<h3>{0}</h3>"
    
    def __init__(self, known_sections, program, command):
            
            self.known_sections = known_sections
            self.program = program
            self.command = command
        
            for k in known_sections:
                self.content[k] = []
                
                
    def convert_name(self):
        """Format name text to html"""
        
        content = self.content['NAME']
        
        for i, row in enumerate(content):
            if row.strip(" ").startswith(self.program):
                content[i] = "<kbd>"+ row + "</kbd><br>"
            else:
                content[i] = row + "<br>"
        content.insert(0, H3_MASK.format('NAME'))
        return content
        
    def convert_synopsis(self):
        """Format content text to html"""
        
        content = self.content['SYNOPSIS']
        
        for i, row in enumerate(content):
            if row.startswith(" "*4 + prog):
                content[i] = "<kbd>"+ row + "</kbd><br>"
            else:
                content[i] = row + "<br>"
        
        content.insert(0, H3_MASK.format('SYNOPSIS'))
        return content
        
    def convert_option(self):
        """Format options text to html"""
        
        content = self.content['OPTION']
        
        for i, row in enumerate(content):    
            if row.startswith(" "*4 + "-"):
                content[i] = "<dt><kbd>"+ row + "</kbd></dt>"
            else:
                content[i] = "<dd>" + row + "</dd>"
        
        content.insert(0, "<dl>")
        content.append("</dl>")
        
        content.insert(0, H3_MASK.format('OPTION'))
        
        return content

    def convert_other(self, key):
        """Generic converter"""
        
        content = self.content[key]
        
        for i, row in enumerate(content):
            content[i] = row + "<br>"    
        
        content.insert(0, H3_MASK.format(key.upper()))
        return content
        
        
    def print_html(self):
    
        print H2_MASK.format(self.program, self.command)
    
        for k in self.known_sections:
            #grab formatted code
            if k == "NAME":
                c = self.convert_name()
            elif k == "SYNOPSIS":
                c = self.convert_synopsis()
            elif k == "OPTION":
                c = self.convert_option()
            else:
                c = self.convert_other(k)
            #print it    
            for l in c:
                print l
            
