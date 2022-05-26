from PIL import Image, ExifTags
from PIL import ImageDraw
from PIL import ImageFont
import pathlib

pics_path = "pics_to_edit"
edited_pics = "./edited_pics"
font_path = "./fonts/Jonathan-www.Dfonts.org/Jonathan.ttf"
msg = "YOUR MESSAGE HERE"

px_from_bottom = 10
font_size = 120
rgb_colour = (255, 255, 255)

path = pathlib.Path(pics_path)


for entry in path.iterdir():
    if entry.is_file():
        print(str(entry))
        str_file = str(entry)[7:]

        img = Image.open(f"{pics_path}/{str_file}")

        try:
            if hasattr(img, '_getexif'):  # only present in JPEGs
                for orientation in ExifTags.TAGS.keys():
                    if ExifTags.TAGS[orientation] == 'Orientation':
                        break
                e = img._getexif()  # returns None if no EXIF data
                if e is not None:
                    exif = dict(e.items())
                    orientation = exif[orientation]

                    if orientation == 3:
                        img = img.transpose(Image.ROTATE_180)
                    elif orientation == 6:
                        img = img.transpose(Image.ROTATE_270)
                    elif orientation == 8:
                        img = img.transpose(Image.ROTATE_90)
        except SyntaxError:
            pass

        img_width, img_height = img.size

        I1 = ImageDraw.Draw(img)

        myFont = ImageFont.truetype(font_path, font_size)

        w, h = I1.textsize(msg, font=myFont)

        font_x = ((img_width - w) / 2)
        font_y = ((img_height - h) - px_from_bottom)

        I1.text((font_x, font_y), msg, font=myFont, fill=rgb_colour)

        img.save(f"./edited_pics/edited_{str_file}")
