from PIL import Image
from pathlib import Path
import shutil
import os
import math
import pathlib

def calc_columns_rows(n):
    #Calculate number of columns and rows to make a grid of n parts as square as possible
    cols = int(math.sqrt(n))
    while n % cols != 0:
        cols -= 1
    rows = n // cols
    return (cols, rows)

def clear_prev_images():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    photo_dir = os.path.join(base_dir, 'static', 'photos')
    for subdir, dirs, files in os.walk(photo_dir):
        for filename in files:
            filepath = os.path.join(subdir, filename)
            try:
                os.remove(filepath)
            except Exception as e:
                print(f"Failed to delete {filepath}: {e}")

def Create_dir():
    path = os.path.join(os.getcwd(), "tmp")
    try:
        os.mkdir(path)
    except OSError:
        pass
    return path

def img_to_dir(imgpath):
    dirpath = Create_dir()
    try:
        shutil.copy(imgpath, dirpath)
        return dirpath
    except Exception as e:
        print(f"Error copying file: {e}")

def accurate_slice(image_path, total_parts):
    image = Image.open(image_path)
    width, height = image.size
    cols, rows = calc_columns_rows(total_parts)

    slice_width = width // cols
    slice_height = height // rows

    remaining_width = width % cols
    remaining_height = height % rows

    for row in range(rows):
        for col in range(cols):
            left = col * slice_width
            upper = row * slice_height
            right = left + slice_width
            lower = upper + slice_height

            if col == cols - 1:
                right = width
            if row == rows - 1:
                lower = height

            box = (left, upper, right, lower)
            slice_img = image.crop(box)
            filename = f"{row+1}_{col+1}.png"
            slice_img.save(os.path.join(tmpdir_path, filename))

def imgsize(path):
    return Image.open(path).size

def AverageColor(path):
    im = Image.open(path).convert('RGBA')
    pixels = list(im.getdata())
    visible = [px for px in pixels if px[3] > 0]

    if not visible:
        return (255, 255, 255)

    num = len(visible)
    r = round(sum(px[0] for px in visible) / num)
    g = round(sum(px[1] for px in visible) / num)
    b = round(sum(px[2] for px in visible) / num)
    return (r, g, b)

def findpos(path):
    parts = Path(path).stem.split('_')
    return int(parts[0]) - 1, int(parts[1]) - 1

def imgtosolid(path):
    for subdir, _, files in os.walk(path):
        for filename in files:
            filepath = os.path.join(subdir, filename)
            if filepath.endswith((".png", ".jpg")):
                size = imgsize(filepath)
                color = AverageColor(filepath)
                new_img = Image.new("RGB", size, color)
                name = Path(filename).name
                temp_path = os.path.join(tmpdir_path, name)
                os.remove(filepath)
                new_img.save(temp_path)
    
def createcanvas(pixels):
    cols, rows = calc_columns_rows(pixels)

    # Read dimensions dynamically
    widths = []
    heights = []

    for row in range(rows):
        row_heights = []
        for col in range(cols):
            img_path = os.path.join(tmpdir_path, f"{row+1}_{col+1}.png")
            if os.path.exists(img_path):
                w, h = imgsize(img_path)
                if col == 0:
                    heights.append(h)
                if row == 0:
                    widths.append(w)

    canvas_width = sum(widths)
    canvas_height = sum(heights)

    canvas = Image.new("RGB", (canvas_width, canvas_height), color="white")
    canvas.save("canvas.jpg")

def pastetoimg(canvaspath, name, dir):
    bg = Image.open(canvaspath)
    for subdir, _, files in os.walk(dir):
        for filename in files:
            filepath = os.path.join(subdir, filename)
            if filepath.endswith((".png", ".jpg")):
                fg = Image.open(filepath)
                pos = findpos(filepath)
                size = imgsize(filepath)
                x = sum(imgsize(os.path.join(dir, f"{pos[0]+1}_{i+1}.png"))[0] for i in range(pos[1]))
                y = sum(imgsize(os.path.join(dir, f"{j+1}_{pos[1]+1}.png"))[1] for j in range(pos[0]))
                bg.paste(fg, (x, y))
    save_path = str(pathlib.Path(__file__).parent.resolve() / 'static' / 'photos' / name)
    bg.save(save_path)


def imgtopxl(imgpath, pixels, name):
    filename = Path(imgpath).name
    try:
        global tmpdir_path
        tmpdir_path = img_to_dir(imgpath)
        tmp_img_path = os.path.join(tmpdir_path, filename)
    except FileNotFoundError:
        print('File not found.')
        return

    try:
        accurate_slice(tmp_img_path, pixels)
        os.remove(tmp_img_path)
    except Exception as e:
        print(f"Error slicing: {e}")
        return

    imgtosolid(tmpdir_path)
    createcanvas(pixels)
    pastetoimg("canvas.jpg", name, tmpdir_path)

    try:
        shutil.rmtree(tmpdir_path)
    except Exception as e:
        print(f"Could not remove tmp directory: {e}")

    os.remove("canvas.jpg")
    print(f"Image saved to: static/photos/{name}")
