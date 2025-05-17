from PIL import Image
from pathlib import Path
import shutil
import os
import math
import pathlib


cached_sizes = {}


#clears any pictures still in the static folder
def clear_prev_images():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    photo_dir = os.path.join(base_dir, 'static', 'photos')
    for subdir, dirs, files in os.walk(photo_dir):
        for filename in files:
            filepath = os.path.join(subdir, filename)
            try:
                os.remove(filepath)
            except Exception as e:
                return f"Failed to delete {filepath}: {e}"



#Calculate number of columns and rows to make a grid of n parts as square as possible
def calc_columns_rows(n):
    cols = int(math.sqrt(n))
    while n % cols != 0:
        cols -= 1
    rows = n // cols
    return (cols, rows)



#create the temp directory
def create_dir():
    path = os.path.join(os.getcwd(), "tmp")
    try:
        os.mkdir(path)
    except OSError:
        pass
    return path



#move the user image/any image to the temp directory
def img_to_dir(imgpath):
    dirpath = create_dir()
    try:
        shutil.copy(imgpath, dirpath)
        return dirpath
    except Exception as e:
        return f"Error copying file: {e}"



#slice the image into smaller parts and then those smaller parts are processed so that the average colour of their pixels are calculated.
def accurate_slice(imgpath, total_parts):
    image = Image.open(imgpath)
    width, height = image.size
    cols, rows = calc_columns_rows(total_parts)

    #integer division to get width and height of each slice (this may lead to left over pixels addressed below)
    slice_width = width // cols
    slice_height = height // rows

    for row in range(rows):
        for col in range(cols):
            #creating boxes inside the photo to be cropped into sliced images
            left = col * slice_width
            upper = row * slice_height
            right = left + slice_width
            lower = upper + slice_height

            #if youre at the final colunm or row then this slice will extend itself to the width or height of the picture
            if col == cols - 1:
                right = width
            if row == rows - 1:
                lower = height

            box = (left, upper, right, lower)
            
            #convert the cropped photo to RGBA and then find the average colour
            slice = image.crop(box).convert("RGBA")
            color  = AverageColor(slice)

            solid = Image.new("RGB", slice.size, color)
            #saving with 1_1 type names so that theyre easier to put on a grid 
            filename = f"{row+1}_{col+1}.png"
    
            #cache the size in a dictionary so its easier to look up later when calculating position
            cached_sizes[filename] = slice.size

            solid.save(os.path.join(tmpdir_path, filename))
    
    return cols, rows


#returns the size of initial image
def imgsize(path):
    return Image.open(path).size



#finds the average colour inside a slice
def AverageColor(im):
    pixels = list(im.getdata())
    
    #removes all transparent pixels from slice
    visible = [px for px in pixels if px[3] > 0]
    if not visible:
        return (255, 255, 255) #i.e if all pixels are transparent return a white pixel


    num = len(visible)
    r = round(sum(px[0] for px in visible) / num)
    g = round(sum(px[1] for px in visible) / num)
    b = round(sum(px[2] for px in visible) / num)
    return (r, g, b)



#finds position that a photo has to be pasted on the canvas
def findpos(path):
    parts = Path(path).stem.split('_')
    return int(parts[0]) - 1, int(parts[1]) - 1

#creates a canvas for the sliced average colour images to be pasted onto
def createcanvas(pixels, cols, rows):

    # Read dimensions dynamically
    widths = []
    heights = []

    #for sliced image adds to the total size of the canvas
    for row in range(rows):
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



#pastes sliced average images onto a canvas
def pastetoimg(canvaspath, name, dir):
    bg = Image.open(canvaspath)
    for subdir, _, files in os.walk(dir):
        for filename in files:
            filepath = os.path.join(subdir, filename)
            if filepath.endswith((".png", ".jpg")):
                fg = Image.open(filepath)
                pos = findpos(filepath)
                
                #below code is a bit strange looking but what it does is finds the sum of the width and coloum for all the images before that image (this is a bit redundant and may have a better solution)
                x = sum(cached_sizes.get(f"{pos[0]+1}_{i+1}.png", (0, 0))[0] for i in range(pos[1]))
                y = sum(cached_sizes.get(f"{j+1}_{pos[1]+1}.png", (0, 0))[1] for j in range(pos[0]))

                bg.paste(fg, (x, y))
            
    save_path = str(pathlib.Path(__file__).parent.resolve() / 'static' / 'photos' / name)
    bg.save(save_path)



#Master function
def imgtopxl(imgpath, pixels, name):
    filename = Path(imgpath).name
    
    #check validity of file and create tmp directory then copy file into temp directory
    try:
        global tmpdir_path
        tmpdir_path = img_to_dir(imgpath)
        tmp_img_path = os.path.join(tmpdir_path, filename)
    except FileNotFoundError:
        return 'File not found.'

    #slice the image and remove the copied file 
    try:
        cols, rows = accurate_slice(tmp_img_path, pixels)
        os.remove(tmp_img_path)
    except Exception as e:
        return f"Error slicing: {e}"

    createcanvas(pixels, cols, rows)
    pastetoimg("canvas.jpg", name, tmpdir_path)


    try:
        shutil.rmtree(tmpdir_path)
    except Exception as e:
        return f"Could not remove tmp directory: {e}"

    os.remove("canvas.jpg")