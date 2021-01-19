from effects.dithering import Dithering
from PIL import Image, ImageFilter, ImageOps, ImageEnhance

class ImageEditor:
    def __init__(self):
        self.effects = [
            (lambda im: im.filter(ImageFilter.BoxBlur(2)), "Box blur"),
            (lambda im: im.filter(ImageFilter.EMBOSS), "Emboss"),
            (lambda im: ImageOps.grayscale(im), "Grayscale"),
            (lambda im: Dithering.convert_img(im), "Dithering"),
            (lambda im: ImageEnhance.Brightness(im).enhance(2.0), 'Brightness'),
            (lambda im: ImageOps.flip(im), "Flip"),
            (lambda im: ImageOps.mirror(im), "Mirror"),
            (lambda im: ImageOps.invert(im), "Invert")
        ]
        self.img: Image = None


    def load_image(self, img):
        self.img = img

    def get_effect(self, index):
        return (lambda im: ImageEditor.rgba_validate(im, self.effects[index][0]), self.effects[index][1])

    def get_images_with_effects(self):
        if self.img == None:
            return

        images_and_names = []
        for effect in self.effects:
            img_eff = ImageEditor.rgba_validate(self.img.copy(), effect[0])
            images_and_names.append((img_eff, effect[1]))
        return images_and_names

    @staticmethod
    def rgba_validate(im, operation):
        if im.mode == "RGBA":
            r, g, b, a = im.split()
            rgb_im = Image.merge('RGB', (r,g,b))
            inverted_im = operation(rgb_im)
            if inverted_im.mode != 'RGB':
                inverted_im = inverted_im.convert(mode="RGB")
            r2, g2, b2 = inverted_im.split()
            return Image.merge('RGBA', (r2,g2,b2,a))
        else:
            return operation(im)
