##################################################################################################################
#                                                                                                                #
# Music Box Strip Maker                                                                                          #
# Version 4.0                                                                                                    #
#                                                                                                                #
# This program converts a DXF file of a music box strip to an SVG file suitable for a Cricut Explore Air 2.      #
#                                                                                                                #
# Copyright: (c) 2020, Joseph Zakar <observing@gmail.com>                                                        #
# GNU General Public License v3.0+ (see LICENSE or                                                               #
# https://tldrlegal.com/license/gnu-general-public-license-v3-(gpl-3)#fulltext)                                  #
#                                                                                                                #
##################################################################################################################

import sys
import tkinter
from tkinter import *
import tkinter.filedialog
import tkinter.font as font
from tkinter import messagebox
import ezdxf
from operator import itemgetter

def main(argv):
    global inputfile
    global outputfile
    global leader
    global maxlength
    global killme
    killme = False
    inputfile = ''
    outputfile = ''
    leader = 1.0
    maxlength = 11.5
    top = tkinter.Tk()
    top.title("Music Box Strip Maker")
    pane = PanedWindow(top, orient=VERTICAL)
    pane.pack(fill=BOTH, expand=1)
    F1 = Frame(pane)
    L1 = tkinter.Label(F1, text="Input File Name   ")
    L1.pack( side = tkinter.LEFT)
    E1 = tkinter.Entry(F1, bd =5, width=30)
    E1.pack(side = tkinter.LEFT)
    F2 = Frame(pane)
    L2 = tkinter.Label(F2, text="Output File Name")
    L2.pack( side = tkinter.LEFT)
    E2 = tkinter.Entry(F2, bd =5, width=30)
    E2.pack(side = tkinter.LEFT)
    F3 = Frame(pane)
    L3 = tkinter.Label(F3, text="Length of First Strip Leader in inches")
    L3.pack( side = tkinter.LEFT)
    E3 = tkinter.Entry(F3, bd =5, width=5)
    E3.insert(0,str(leader))
    E3.pack(side = tkinter.LEFT)
    F4 = Frame(pane)
    L4 = tkinter.Label(F4, text="Maximum Length of Strip(s) in inches")
    L4.pack( side = tkinter.LEFT)
    E4 = tkinter.Entry(F4, bd =5, width=6)
    E4.insert(0,str(maxlength))
    E4.pack(side = tkinter.LEFT)
    # This is the handler for the input file browse button
    def InfileCallBack():
        ftypes = [('dxf files','.dxf'), ('All files','*')]
        inputfile = tkinter.filedialog.askopenfilename(title = "Select File", filetypes = ftypes, defaultextension='.dxf')
        E1.delete(0,tkinter.END)
        E1.insert(0, inputfile)

    # This is the handler for the output file browse button
    def OutfileCallBack():
        ftypes = [('svg files','.svg'), ('All files','*')]
        outputfile = tkinter.filedialog.asksaveasfilename(title = "Save File As", filetypes = ftypes, defaultextension='.svg')
        E2.delete(0,tkinter.END)
        E2.insert(0,outputfile)

    # This is the handler for the cancel button
    def CancelCallBack():
        global killme
        killme = True
        top.destroy()

    # This is the handler for the OK button
    def OKCallBack():
        global inputfile
        global outputfile
        global leader
        global maxlength
        inputfile = E1.get()
        outputfile = E2.get()
        leader = float(E3.get())
        maxlength = float(E4.get())
        top.destroy()
    B1 = tkinter.Button(F1, text="Browse", command=InfileCallBack)
    B1.pack(side = tkinter.LEFT)
    B2 = tkinter.Button(F2, text="Browse", command=OutfileCallBack)
    B2.pack(side = tkinter.LEFT)
    F6 = Frame(pane)
    bfont = font.Font(size=12)
    B3 = tkinter.Button(F6, text="Cancel", command=CancelCallBack)
    B3['font'] = bfont
    B3.pack(side = tkinter.LEFT, ipadx=30)
    B4 = tkinter.Button(F6, text="OK", command=OKCallBack)
    B4['font'] = bfont
    B4.pack(side = tkinter.RIGHT,ipadx=40)
    pane.add(F1)
    pane.add(F2)
    pane.add(F3)
    pane.add(F4)
    pane.add(F6)
    top.mainloop()
    if killme == True:
        sys.exit(4)
    if inputfile == '':
      root = tkinter.Tk()
      root.withdraw()
      messagebox.showerror('Program Input Error', 'Input File is Required', parent=root)
      sys.exit(5)
    if outputfile == '':
      root = tkinter.Tk()
      root.withdraw()
      messagebox.showerror('Program Input Error', 'Output File is Required', parent=root)
      sys.exit(5)
    bp = '<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n'+\
'<svg\n'+\
'   xmlns:dc=\"http://purl.org/dc/elements/1.1/\"\n'+\
'   xmlns:cc=\"http://creativecommons.org/ns#\"\n'+\
'   xmlns:rdf=\"http://www.w3.org/1999/02/22-rdf-syntax-ns#\"\n'+\
'   xmlns:svg=\"http://www.w3.org/2000/svg\"\n'+\
'   xmlns=\"http://www.w3.org/2000/svg\"\n'+\
'   height=\"2.75in\"\n'+\
'   version=\"1.1\"\n'+\
'   viewBox=\"0.0 0.0 828.0 198.0\"\n'+\
'   width=\"11.5in\"\n'+\
'   id=\"svg18\">\n'+\
'  <metadata\n'+\
'     id=\"metadata22\">\n'+\
'    <rdf:RDF>\n'+\
'      <cc:Work\n'+\
'         rdf:about=\"\">\n'+\
'        <dc:format>image/svg+xml</dc:format>\n'+\
'        <dc:type\n'+\
'           rdf:resource=\"http://purl.org/dc/dcmitype/StillImage\" />\n'+\
'        <dc:title></dc:title>\n'+\
'      </cc:Work>\n'+\
'    </rdf:RDF>\n'+\
'  </metadata>\n'+\
'  <defs\n'+\
'     id=\"defs2\" />\n'+\
'  <g\n'+\
'     id=\"layer1\" />\n'
    svg_scale = 72.0 # Cricut needs 72 dpi
    header = leader*svg_scale # Sets the leader on the first strip
    # Centers of notes are offset from their actual locations for multiple strips
    xoffset = 0.0
    yoffset = 0.0
    ymargin = 0.0 # Actual value will be derived later
    ypad = 0.1*svg_scale # distance between strips
    max_strip = maxlength*svg_scale
    tab_width = 0.25*svg_scale
    opaths = []
    stroke_width = 0.01*svg_scale
    style = '\"fill:#ffffff;stroke:#000000;stroke-width:{0};stroke-miterlimit:4;stroke-dasharray:none\"'.format(stroke_width)
    strip_num = 1
    group_num = 1
    try:  # Read in the DXF file
        doc = ezdxf.readfile(inputfile)
    except IOError:
        print(f'Not a DXF file or a generic I/O error.')
        sys.exit(1)
    except ezdxf.DXFStructureError:
        print(f'Invalid or corrupted DXF file.')
        sys.exit(2)
    outf = open(outputfile, mode='w')
    outf.write(bp)
    msp = doc.modelspace()
    '''
    There will be two types of entities in this file:
    1. Polylines. One will be the boundary of the strip. The other will be
       the boundary of the notes, which we don't really need if we've
       scaled the drawing correctly.
    2. Circles. These are the notes
    '''
    strip_bbx = False
    bbx = []
    for e in msp.query('POLYLINE'):
        if ymargin == 0.0:  # We're looking for the strip boundary
            for pp in e.points():
                if (pp[0]==0.0) and (pp[1]==0.0):
                    strip_bbx = True # This is the strip boundary. Capture it
                    bbx.append(pp[0])
                    bbx.append(pp[1])
                else:
                    if strip_bbx:
                        bbx.append(pp[0]*svg_scale)
                        bbx.append(pp[1]*svg_scale)
            ymargin = bbx[5] - bbx[3]
    notes = [] # store the notes here
    note_radius = 0.0 # the radius will always be the same
    for e in msp.query('CIRCLE'):
        notes.append(e.dxf.center)
        note_radius = e.dxf.radius
    note_num = 0
    notes.sort(key=itemgetter(0)) # sort by x coordinate in ascending order
    circles = []
    for note in notes:
        rad = note_radius*svg_scale
        cx = note[0]*svg_scale + xoffset # Notes start after leader (applies to first strip only)
        cy = note[1]*svg_scale + yoffset
        startx = cx - rad
        starty = cy
        endx = cx + rad
        endy = cy
        if (endx + stroke_width + (strip_num > 1)*tab_width + (strip_num == 1)*header) > max_strip:  # end the current strip
            outf.write('     <g\n       id=\"g'+str(group_num)+'\">\n')
            outf.write('         <path\n           id=\"'+str(strip_num)+str(group_num)+'\"\n           style='+style+\
                       '\n           d=\"')
            for circle in circles:
                outf.write(circle)
                outf.write(" ")
            breakx = (last_endx + startx)/2.0 # find the break point (ASSUMES X CHANGES FIRST in CW direction)
            # We include interlocking tab cutout at the end
            outf.write('M '+ str(bbx[0]-(strip_num == 1)*header) + ',' + str(bbx[1]) + ' L '+ str(breakx) + ',' + str(bbx[3]) + \
                    ' L '+ str(breakx) + ',' + str(bbx[3]+8) + ' L '+ str(breakx-10) + ',' + str(bbx[3]+5) + \
                    ' L '+ str(breakx-10) + ',' + str(bbx[3]+13) + ' L '+ str(breakx) + ',' + str(bbx[3]+13) + \
                    ' L '+ str(breakx) + ',' + str(bbx[5]-13) + ' L '+ str(breakx-10) + ',' + str(bbx[5]-13) + \
                    ' L '+ str(breakx-10) + ',' + str(bbx[5]-5) + ' L '+ str(breakx) + ',' + str(bbx[5]-8) + \
                    ' L '+ str(breakx) + ',' + str(bbx[5]) + ' L '+ str(bbx[6]-(strip_num == 1)*header/2) + ',' + str(bbx[7]))
            if strip_num > 1: # We add an interlocking tab to the beginning of the strip if it is not the first one
                outf.write(' L '+ str(bbx[6]) + ',' + str(bbx[7]-8) + ' L '+ str(bbx[6]-10) + ',' + str(bbx[7]-5) + \
                    ' L '+ str(bbx[6]-10) + ',' + str(bbx[7]-13) + ' L '+ str(bbx[6]) + ',' + str(bbx[7]-13) + \
                    ' L '+ str(bbx[0]) + ',' + str(bbx[1]+13) + ' L '+ str(bbx[0]-10) + ',' + str(bbx[1]+13) + \
                    ' L '+ str(bbx[6]-10) + ',' + str(bbx[1]+5) + ' L '+ str(bbx[0]) + ',' + str(bbx[1]+8))
            outf.write(' Z\" />\n     </g>\n')
            xoffset = xoffset - breakx  # move to new starting location
            yoffset = yoffset + ymargin + ypad
            bbx[0] = 0.0  # create the next strip boundary
            bbx[1] = yoffset
            bbx[3] = yoffset
            bbx[5] = yoffset + ymargin
            bbx[6] = 0.0
            bbx[7] = yoffset + ymargin
            strip_num = strip_num + 1
            group_num = group_num + 1
            circles.clear()
            cx = note[0]*svg_scale + xoffset
            cy = note[1]*svg_scale + yoffset
            startx = cx - rad
            starty = cy
            endx = cx + rad
            endy = cy
        last_endx = endx
        d = 'M '+str(endx)+','+str(endy)
        d = d +' A '+str(rad)+','+str(rad)+' 0 0 1 '+str(endx-rad)+','+str(endy+rad)
        d = d +' A '+str(rad)+','+str(rad)+' 0 0 1 '+str(endx-(2*rad))+','+str(endy)
        d = d +' A '+str(rad)+','+str(rad)+' 0 0 1 '+str(endx-rad)+','+str(endy-rad)
        d = d +' A '+str(rad)+','+str(rad)+' 0 0 1 '+str(endx)+','+str(endy)
        circles.append(d)
        note_num = note_num + 1
    outf.write('     <g\n       id=\"g'+str(group_num)+'\">\n')
    outf.write('         <path\n           id=\"'+str(strip_num)+str(group_num)+'\"\n           style='+style+\
               '\n           d=\"')
    for circle in circles:
        outf.write(circle)
        outf.write(" ")
    trailer = header
    if (trailer + endx + stroke_width + (strip_num > 1)*tab_width) > max_strip:
        trailer = max_strip - endx  - stroke_width - (strip_num > 1)*tab_width
    outf.write('M '+ str(bbx[0]) + ',' + str(bbx[1]) + ' L '+ str(endx+trailer) + ',' + str(bbx[3]) + \
            ' L '+ str(endx+trailer) + ',' + str(bbx[5]) + ' L '+ str(bbx[6]) + ',' + str(bbx[7]))
    if strip_num > 1:
        outf.write(' L '+ str(bbx[6]) + ',' + str(bbx[7]-8) + ' L '+ str(bbx[6]-10) + ',' + str(bbx[7]-5) + \
            ' L '+ str(bbx[6]-10) + ',' + str(bbx[7]-13) + ' L '+ str(bbx[6]) + ',' + str(bbx[7]-13) + \
            ' L '+ str(bbx[0]) + ',' + str(bbx[1]+13) + ' L '+ str(bbx[0]-10) + ',' + str(bbx[1]+13) + \
            ' L '+ str(bbx[6]-10) + ',' + str(bbx[1]+5) + ' L '+ str(bbx[0]) + ',' + str(bbx[1]+8))
    outf.write(' Z\" />\n     </g>\n')
    outf.write('</svg>')
    outf.close()

if __name__ == "__main__":
   main(sys.argv[1:])
