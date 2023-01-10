# undeveloped idea to generate randomness from lightning strikes in the continental US

def lightningMethod():

    response = requests.get(
        "https://cdn.star.nesdis.noaa.gov/GOES16/GLM/CONUS/EXTENT3/1250x750.jpg")
    img = Image.open(BytesIO(response.content))
    pix = img.load()
    width = img.size[0] - 20
    height = img.size[1] - 20

    for x in range(0, width):
        for y in range(0, height):
            r, g, b = pix[x, y]

            if r > 200 and g < 70 and b < 70:
                createBlueBox(x, y, pix)


def createBlueBox(x, y, pix):
    for i in range(x - 5, x + 5):
        pix[i,  y + 5] = (0, 0, 255)
        pix[i,  y - 5] = (0, 0, 255)
    for i in range(y - 5, y + 5):
        pix[x + 5,  i] = (0, 0, 255)
        pix[x - 5,  i] = (0, 0, 255)
