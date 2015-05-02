#!/usr/bin/python3

import sys
import os.path
import collections

from pygments import highlight
from pygments.lexers import CppLexer
from pygments.formatters import HtmlFormatter


import pprint
pp = pprint.PrettyPrinter(indent=4)

def basic(fd, attributions):
    for attr, val in attributions.items():
        fd.write("%s: %i\n" % (attr, len(attributions[attr])))
        for current_attribution in attributions[attr]:
            fd.write("\t%s:%i\n" % (current_attribution[1], current_attribution[3]))

def html(fd, attributions):
    ordered_attributions = collections.OrderedDict(sorted(attributions.items()))
    fd.write("""
        <HTML>
          <HEAD><TITLE>Report</TITLE>
            <link rel="stylesheet" href="http://code.jquery.com/ui/1.11.4/themes/smoothness/jquery-ui.css">
            <script src="http://code.jquery.com/jquery-1.10.2.js"></script>
            <script src="http://code.jquery.com/ui/1.11.4/jquery-ui.js"></script>
  <script>
  $(function() {
    $( "#accordion1" ).accordion({collapsible:true});
  });
  </script>
	<style>""" + HtmlFormatter().get_style_defs('.highlight') + """</style>

          </HEAD>
        <BODY>
	<DIV id="accordion1">
""")

    for attr, val in ordered_attributions.items():
        fd.write("\t<h3>%s - %i</h3>\n<DIV>" % ((attr), len(attributions[attr])))
        for current_attribution in attributions[attr]:
            # file:lineno
            fd.write("<P><A href=\"file://%s\">%s</A>:%i</P>\n" % 
	             (current_attribution[1], current_attribution[0], current_attribution[3] ))
            # code block
            fd.write(__code_block(current_attribution[2]))

        fd.write("</DIV>")      
        
    
    fd.write("""
</DIV>
</BODY>       
""")

def __code_block(code_buf):
    return highlight(code_buf, CppLexer(), HtmlFormatter())

if __name__ == '__main__':
    import scan
    scan = scan.scanner2(defines=('TMP_LINKER'))

    if len(sys.argv) == 1:
        print("1 arg needed: base path to recurse.")
        sys.exit(1)

    if not os.path.isdir(sys.argv[1]):
        print("invalid dir: %s" % sys.argv[1])
        sys.exit(1)

    attributions = scan.do_scan(sys.argv[1])
    #pp.pprint(attributions)
    html(sys.stdout, attributions)
