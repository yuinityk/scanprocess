import os
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.pagesizes import B5
from reportlab.lib.units import mm
from reportlab.lib.units import cm
from optparse import OptionParser

def drawImage(c, pagesize, img_file):
    img = Image.open(img_file)
    img_w, img_h = img.size
    
    if pagesize == 'A4':
        page_w, page_h = A4
    else:
        page_w, page_h = B5

    if (float(img_w)/img_h) < ((float(page_w)/page_h)):
        dest_h = page_h
        dest_w = img_w * (page_h / img_h)
        x = (page_w-dest_w)/2
        y = 0
    else:
        dest_w = page_w
        dest_h = img_h * (page_w / img_w)
        y = (page_h-dest_h)/2
        x = 0

    c.drawInlineImage(img_file, x, y, width=dest_w, height=dest_h)

if __name__ == '__main__':

    parser = OptionParser('usage: %prog (options) [page_size]')
    parser.add_option('-s', '--size', type='choice', 
            choices=['A4','B5'], dest='size', default='A4',
            metavar='SIZE', help='specify paper size(default: A4)')

    (options, args) = parser.parse_args()
    print(options, args)

    if options.size == 'A4':
        c = canvas.Canvas('output.pdf', pagesize=A4)
    else:
        c = canvas.Canvas('output.pdf', pagesize=B5)

    if os.path.exists('image'):
        files = os.listdir('image')
        for i in range(len(files)):
            drawImage(c, options.size, 'image/'+files[i])
            c.showPage()

    c.save()


