import bs4
import requests
import datetime
from PIL import Image
import os.path
import time


# Get the day
dt = datetime.datetime.today()
date = dt.strftime("%d_%m_%y")

# Retrieve the image url
res = requests.get('http://www.murciasalud.es/pagina.php?id=458440')
soup = bs4.BeautifulSoup(res.text, 'html.parser')
div = soup.find('div', id='coronavirus')
soup = bs4.BeautifulSoup(str(div), "html.parser")
ases = soup.find_all('a')
href = ases[13]['href']

# Save the image
res = requests.get('http://www.murciasalud.es/' + href, allow_redirects=True)
filename = 'C:\\Users\\GETTUP\\Desktop\\' + date + '.png'
open(filename, 'wb').write(res.content)

# Open Image
image = Image.open('C:\\Users\\GETTUP\\Desktop\\' + date + '.png')
image.show()

# time_to_wait = 10
# # time_counter = 0
# # while not os.path.exists(filename):
# #     time.sleep(1)
# #     time_counter += 1
# #     if time_counter > time_to_wait:break
# #
# # print("done")

