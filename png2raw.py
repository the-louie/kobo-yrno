from PIL import Image, ImageFilter
import sys

try:
    original = Image.open("testimagelarge.png").convert("L").rotate(90)
except:
    print "Unable to load image"
    sys.exit(1)

print "The size of the Image is: "
print(original.format, original.size, original.mode)

output = open("testimagelarge.raw", "wb")
for y in range(original.size[1]):
    for x in range(original.size[0]):
        output.write(chr(original.getpixel((x,y))))
output.close()





# def to_hex(color):
#     hex_chars = "0123456789ABCDEF"
#     return hex_chars[color / 16] + hex_chars[color % 16]

# def convert_to_raw(surface):
#     print("Converting image . . .")
#     raw_img = ""
#     for row in range(surface.get_height()):
#         for col in range(surface.get_width()):
#             color = surface.get_at((col, row))[0]
#             raw_img += ('\\x' + to_hex(color)).decode('string_escape')
#     f = open("/tmp/img.raw", "wb")
#     f.write(raw_img)
#     f.close()
#     print("Image converted.")