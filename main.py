from faker import Faker
from flask import Flask, render_template
import random
from escpos.connections import getUSBPrinter
from PIL import Image
import json
import os

# printer = getUSBPrinter()(idVendor=0x0519,
#                           idProduct=0x2013,
#                           inputEndPoint=0x81,
#                           outputEndPoint=0x03)  # Create the printer object with the connection params

fake = Faker(['zh_TW'])
Faker.seed(0)
fake.seed_instance(0)

app = Flask(__name__)

path_dirs = ['/home/pi/fake_portraits/fake_females','/home/pi/fake_portraits/fake_males']

def getRandomFile(path):
  """
  Returns a random filename, chosen among the files of the given path.
  """
  files = os.listdir(path)
  index = random.randrange(0, len(files))
  file_path = path + '/' + files[index]
  return file_path

def get_syth_data():
    printer = getUSBPrinter()(idVendor=0x0519,
                          idProduct=0x2013,
                          inputEndPoint=0x81,
                          outputEndPoint=0x03)  # Create the printer object with the connection params

    fake.seed_locale('zh_TW', random.randint(0, 6000))
    data = []
    or_imgfile = getRandomFile(path_dirs[random.randint(0, 1)])
    image = Image.open(or_imgfile)
    image.thumbnail((250, 250), Image.ANTIALIAS)
    image.rotate(180)
    image.save('/home/pi/thumb.jpg', 'JPEG', quality=80)
    for _ in range(1):
        temp = {}
        temp['name'] = fake.name()
        temp['phone'] = fake.phone_number()
        temp['email'] = fake.ascii_free_email()
        temp['ip_address'] = f"{random.randint(100,255)}.{random.randint(100,255)}.{random.randint(100,255)}.{random.randint(100,255)}"
        temp['file_path'] = or_imgfile
        data.append(temp)
    # print(f"data is : {data}")
    printer.lf()
    printer.lf()
    printer.lf()
    printer.align(align='full')
    printer.image('/home/pi/thumb.jpg')
    printer.lf()
    printer.underline()
    printer.text(f"IP_ADDRESS：{data[0]['ip_address']}\n".encode('GB18030'))
    printer.underline()
    printer.lf()
    printer.text(f"姓名：{data[0]['name']}\n".encode('GB18030'))
    printer.lf()
    printer.text(f"行動電話：{data[0]['phone']}\n".encode('GB18030'))
    printer.lf()
    printer.text(f"E-Mail：{data[0]['email']}\n".encode('GB18030'))
    printer.lf()
    printer.lf()
    printer.lf()   

    return data[0]


@app.route('/print')
def hello():
    # os.system('sudo python esc_printer.py')
    data = get_syth_data()
    dump = {
        "name":data['name'],
        "phone":data['phone'],
        "email":data['email'],
        "ip_address":data['ip_address'],
        "file_path":data['file_path']
    }
    return dump

if __name__ == '__main__':
   app.run(host='0.0.0.0', port= 8090, debug = True)
