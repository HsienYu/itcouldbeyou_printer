from escpos.connections import getUSBPrinter
from PIL import Image


printer = getUSBPrinter()(idVendor=0x0519,
                          idProduct=0x2013,
                          inputEndPoint=0x81,
                          outputEndPoint=0x03)  # Create the printer object with the connection params

#image = Image.open('/home/pi/test.jpg')
#image.thumbnail((250, 250), Image.ANTIALIAS)
# image.rotate(180)
#image.save('/home/pi/thumb.jpg', 'JPEG', quality=88)

printer.upsideDown(True)
printer.text("中文\n".encode('GB18030'))
printer.lf()
printer.text("醜貓".encode('GB18030'))
printer.lf()
printer.lf()
printer.lf()
printer.upsideDown(True)
printer.align(align='full')
printer.image('/home/pi/thumb.jpg')
printer.lf()
printer.lf()
printer.lf()
printer.text('this is a cat!')
printer.lf()
