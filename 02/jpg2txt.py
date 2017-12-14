from PIL import Image
import argparse

ascii_char = '10'


def select_ascii_char(r, g, b):
    gray = int((19595 * r + 38469 * g + 7472 * b) >> 16)
    unit = 256.0 / len(ascii_char)
    return ascii_char[int(gray / unit)]


def preimg(img_name, width = 32, height = 32):
    img = Image.open(img_name)
    print(img.size)
    img = img.resize((width, height), Image.NEAREST)
    print(img.size)

    img.convert('L')
    return img


def img2char(img):
    res = ''
    width, height = img.size
    for h in range(height):
        for w in range(width):
            res += select_ascii_char(*img.getpixel((w, h))[:3])
        res += '\n'
    return res


def save_to_file(pic_str, filename):
    outfile = open(filename, 'a')
    outfile.write(pic_str)
    outfile.close


if __name__ == '__main__':
    img_name = 'digits/jpg/7_1.jpg'
    # file = 'test.txt'
    filename = img_name.replace('jpg', 'txt')
    img = preimg(img_name)
    pic_str = img2char(img)
    save_to_file(pic_str, filename)
