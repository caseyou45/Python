from PIL import Image
import requests
import math
from io import BytesIO
from bs4 import BeautifulSoup
from urllib.request import urlopen


def main():
    total += 1
    getLinks()
##    border = 0
##    red = 0
##
##    response = requests.get("https://cdn.star.nesdis.noaa.gov/GOES16/GLM/CONUS/EXTENT3/1250x750.jpg")
##    img = Image.open(BytesIO(response.content))
##    pix = img.load()
##    width = img.size[0] - 20
##    height = img.size[1] - 20
##
# for x in range(0, width):
# for y in range(0, height):
##            r, g, b = pix[x, y]
# if r > 200 and g < 70 and b <  70:
##                createBlueBox(x,y, pix)
##                red += 1
##
##
##
##    total = red
##
# while total >= 1:
# total /= 10
##        total /= math.pi
##
##
# print(total)
# img.save("F.jpg")


def getLinks():
    url = "https://cdn.star.nesdis.noaa.gov/GOES16/GLM/CONUS/EXTENT3/"
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    anchorTags = soup.find_all(
        lambda tag: tag.name == "a" and "2500" in tag.string)
    getImages(anchorTags)


def getImages(anchorTags):
    for i in range(0, 10):
        print(anchorTags[i]["href"])


def createBlueBox(x, y, pix):
    for i in range(x - 5, x + 5):
        pix[i,  y + 5] = (0, 0, 255)
        pix[i,  y - 5] = (0, 0, 255)
    for i in range(y - 5, y + 5):
        pix[x + 5,  i] = (0, 0, 255)
        pix[x - 5,  i] = (0, 0, 255)


main()
