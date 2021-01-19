from PIL import Image
import numpy as np

class Dithering:

    findClosestColor = lambda value: int(round(value/64.0))*64

    @classmethod
    def convert_img(cls, image):
        # imageData = np.asarray(image).copy()
        # for i, line in enumerate(imageData):
        #     for j, pixel in enumerate(line):
        #         oldPixel = pixel.copy()
        #         imageData[i][j] = np.array([cls.findClosestColor(val) for val in pixel])
        #
        #         error = oldPixel - imageData[i][j]
        #         to_int = lambda x: int(x)
        #         if(i + 1 < len(imageData)):
        #             imageData[i + 1][j] = imageData[i + 1][j] + np.array(list(map(to_int, error * 7/16)))
        #
        #         if(i - 1 >= 0 and j + 1 < len(imageData[0])):
        #             imageData[i - 1][j + 1] = imageData[i - 1][j + 1] + np.array(list(map(to_int, error * 3/16)))
        #
        #         if(j + 1 < len(imageData[0])):
        #             imageData[i][j + 1] = imageData[i][j + 1] + np.array(list(map(to_int, error * 5/16)))
        #
        #         if(j + 1 < len(imageData[0]) and i + 1 < len(imageData)):
        #             imageData[i + 1][j + 1] = imageData[i + 1][j + 1] + np.array(list(map(to_int, error * 1/16)))
        #
        #
        #
        # return Image.fromarray(imageData)

        image = image.convert(mode="P", dither=Image.FLOYDSTEINBERG, palette=Image.ADAPTIVE, colors=8).convert('RGB')
        return image

if __name__ == '__main__':
    Dithering.convert_img(Image.open(r'C:\Users\karol\Downloads\dragon.jpg')).save(r'C:\Users\karol\Downloads\dragonDithered.jpg')
