#!/bin/env python

import cgi
import cgitb; cgitb.enable() # for troubleshooting
import os
import time

thisPage = "/cgi-bin/browseSnippets.cgi"
fakeCVSbrowser = "/FNALfakeCfgCVSbrowser"
fakeCVSreal = "/home/daqowner/FNALfakeCfgCVS"
fmt = "%h %d %Y %H:%M:%S %Z"

form = cgi.FieldStorage()
body = ""
if not form.getvalue('path'):
  body += '''
    <h2>FNAL snippet browser</h2>
    <a href="{0}?path={1}">{2}</a>
  '''.format(thisPage, fakeCVSbrowser, fakeCVSreal)

else:
  path = str(form.getvalue('path'))
  realName = path.replace(fakeCVSbrowser, fakeCVSreal)
  if not path.split("/")[1] == fakeCVSbrowser[1:]:
    body+="invalid path:%s" % path
    body += "[" + path.split("/")[1] + "]"
    body += "[" + path.split("/")[1] + "]"
  elif not os.path.exists(realName):
    body+="path %s not found!" % path
  else:
    dirlist = os.listdir(realName)
    dirlist = [item for item in dirlist if not item.startswith('.')]
    body+= "    <h2 style='display:inline;'>%s</h2>\n"%realName
    body+= "    &nbsp;&nbsp;&nbsp;&nbsp; <a style='display:inline;' href='{0}?path={1}'>(up)</a>\n".format(thisPage, "/".join(path.split("/")[:-1]))
    body+="    <table>"
    dirs = []
    files = []
    for item in dirlist:
      if os.path.isfile("{0}/{1}/pro".format(realName, item)):
        timestamp = os.path.getmtime("{0}/{1}/pro".format(realName, item))
        files.append(( "\n      <tr>\n        <td style='color:brown;'>file:</td>\n        <td> <a href='{2}/{1}/pro'>{0}/{1}/pro</a> </td>\n        <td>last modified: {3}</td>\n      </tr>".format(
          realName, item, path, time.strftime(fmt, time.localtime(timestamp))), timestamp )
        ) 
      elif os.path.isdir(realName):
        timestamp = os.path.getmtime("{0}/{1}".format(realName, item))
        dirs.append(( "\n      <tr>\n        <td style='color:darkgreen;'>dir:</td>\n        <td> <a href='{2}?path={3}/{1}'>{0}/{1}</a> </td>\n      </tr>".format(
          realName, item, thisPage, path, time.strftime(fmt, time.localtime(timestamp))), timestamp)
        )
      else:
        pass
  files.sort(key=lambda snip: snip[1])
  fileHTML = [snip[0] for snip in files]
  dirs.sort(key=lambda d: d[1])
  dirsHTML = [d[0] for d in dirs]
  body += "\n"
  body += "\n".join(reversed(dirsHTML))
  body += "\n"
  body += "\n".join(reversed(fileHTML))
  body += "\n"
  body+="\n    </table>"
        
print "Content-type: text/html"
print
print "<html>\n  <head>"
print '    <link rel="stylesheet" type="text/css" href="/fnalHomePage.css">'
print "  </head>\n  <body>"
print body
print "  </body>\n</html>"
