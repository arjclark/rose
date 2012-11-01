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
            if row.startswith("NAME"):
                content[i] = ""
            elif row.strip(" ").startswith(self.program):
                content[i] = "<kbd>"+ row + "</kbd><br>"
            else:
                content[i] = row + "<br>"
        content.insert(0, self.H3_MASK.format('NAME'))
        return content
        
    def convert_synopsis(self):
        """Format content text to html"""
        
        content = self.content['SYNOPSIS']
        
        for i, row in enumerate(content):
            if row.startswith("SYNOPSIS"):#
                content[i] = ""
            elif row.startswith(" "*4 + self.program):
                content[i] = "<kbd>"+ row + "</kbd><br>"
            else:
                content[i] = row + "<br>"
        
        content.insert(0, self.H3_MASK.format('SYNOPSIS'))
        return content
        
    def convert_option(self):
        """Format options text to html"""
        
        content = self.content['OPTIONS']
        
        for i, row in enumerate(content):
            if row.startswith("OPTION"):
                content[i] = ""
            elif row.startswith(" "*4 + "-"):
                content[i] = "<dt><kbd>"+ row + "</kbd></dt>"
            else:
                content[i] = "<dd>" + row + "</dd>"
        
        content.insert(0, "<dl>")
        content.append("</dl>")
        
        content.insert(0, self.H3_MASK.format('OPTIONS'))
        
        return content

    def convert_description(self):
    
        content = self.content['DESCRIPTION']
        """
        for i, row in enumerate(content):
            if row.startswith("DESCRIPTION"):
                content[i] = "<pre>"
        content.append("</pre>")
        """
        
        content.insert(0, self.H3_MASK.format('DESCRIPTION'))
        
        return content

    def convert_arguments(self):
    
        content = self.content['ARGUMENTS']
        for i, row in enumerate(content):
            if row.startswith("ARGUMENTS"):
                content[i] = ""
            elif row.split(" ")[0].isupper():
                content[i] = "<td><kbd>" + row + "</kbd></dt>"
            else:
                content[i] = "<dd>" + row + "</dd>"
        
        content.insert(0, self.H3_MASK.format('ARGUMENTS'))
        return content

    def convert_other(self, key):
        """Generic converter"""
        
        content = self.content[key]
        
        for i, row in enumerate(content):
            if content[i].startswith(key):
                content[i] = ""
            else:
                content[i] = row + "<br>"    
        
        content.insert(0, self.H3_MASK.format(key.upper()))
        return content
        
        
    def get_html(self):
    
        content = []
    
        #content += [self.H2_MASK.format(self.program, self.command)]
    
        for k in self.known_sections:
            #grab formatted code
            if k == "NAME":
                content += self.convert_name()
            elif k == "SYNOPSIS":
                content += self.convert_synopsis()
            elif k == "OPTIONS":
                content += self.convert_option()
            #elif k == "DESCRIPTION":
            #    content += self.convert_description()
            elif k == "ARGUMENTS":
                content += self.convert_arguments()
            else:
                content += self.convert_other(k)

        return content            
