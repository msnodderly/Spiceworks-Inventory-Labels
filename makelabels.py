# Matt Snodderly
# 5/10/11
# Usage: python makelabels.py  > names.dat && pdflatex labels.tex
#
# Uses pdflatex and Google chart API to create labels with asset info and 
# a 2D QR code link to the item in Spiceworks. 
#
# Works with Avery 5160 labels. Assumes that a copy Spiceworks sqlite db 
# is in the current directory (spiceworks_prod.db)



import commands
import urllib2

# spiceworks server
swserver="spiceworks.example.com"

inv = commands.getoutput("sqlite3 spiceworks_prod.db 'SELECT name,ip_address,asset_tag,id FROM devices  order by name;'").split("\n");


charturl = "http://chart.googleapis.com/chart?chs=100x100&cht=qr&chl=http%3A%2F%2F" + swserver + "%3A8080%2Finventory%2Fgroups%2Fdevices%2F"

for item in inv:
    (name, ip, asset_tag, urlid) = item.split("|")

    qrurl = charturl + urlid

    myqr = urllib2.urlopen(qrurl)

    imgoutput = open("./images/" + urlid + ".png",'w')
    imgoutput.write(myqr.read())
    imgoutput.close()

    print
    print '\\begin{wrapfigure}{15mm}{-10mm}\includegraphics[scale=.75, trim=10mm 15mm 10mm 20mm]{images/' + urlid + '.png}\end{wrapfigure} \\begin{mbox}  Property of MYCOMPANY \\\\  $\\star$ ', asset_tag, ' $\\star$ \\\\ ', name, ' \\end{mbox} '
    print

