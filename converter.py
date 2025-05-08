from PIL import Image
from pathlib import Path    
import shutil
import os
import pathlib
from image_slicer import slice, calc_columns_rows


def Create_dir():
    #create temporary directory for movement of files
    path = os.path.join(os.getcwd(), "tmp")
    try:
        os.mkdir(path)
        print("Directory %s succesfully created" % path)
        return(path)
    except OSError:
        print("Creation of the directory %s failed" % path)
        return(path)


def img_to_dir(imgpath):
    #copy image to direcotry
    dirpath = Create_dir()
    try:
        shutil.copy(imgpath,dirpath)
        print("file succesfully copied to /tmp/")
        return dirpath
    except:
        print("encountered error while copying file")


def splitimage(path,parts):
    #split image using image_slice module
    slice(path, parts)


def imgsize(path):
    #find size of an image
    im = Image.open(path)
    return(im.size)


def AverageColor(path):
    #find the average color of an image in form of RBG list
    im = Image.open(path).convert('RGB')
    # im = Image.open(path, 'r')
    pix_val_R = list(im.getdata(0))
    pix_val_G = list(im.getdata(1))
    pix_val_B = list(im.getdata(2))
    
    avr_R = round(sum(pix_val_R)/len(pix_val_R))
    avr_G = round(sum(pix_val_G)/len(pix_val_G))
    avr_B = round(sum(pix_val_B)/len(pix_val_B))
    
    average = (avr_R,avr_G,avr_B)
    return average


def findpos(path):
    # find position from name of image
    filename = Path(path).stem
    position = (filename).split('_')

    print(position, "positionnnn")
    print(position[-2], position[-1])

    
    position = (int(position[-2])-1, int(position[-1])-1)

    print('image', position, 'placed at: ')
    return position


def imgtosolid(path):
    #change the color of sliced image to its average color
    for subdir, dirs, files in os.walk(path):
        original_files = list(files)

        for filename in files:
            filepath = subdir + os.sep + filename
            
            if filepath.endswith(".jpg") or filepath.endswith(".png"):
                image = Image.new('RGB',imgsize(filepath),AverageColor(filepath))
                string = str(filename).split('_')

                # filename = coord1_coord2_.png/.jpg
                string = str(string[-2]+'_'+string[-1])

                image.save(string)
                os.remove(filepath)
                shutil.move(string,tmpdir_path)


def createcanvas(pixels):
    #create a canvas onwhich other images will be pasted
    #this function first gets the size of a sliced image then multiplies by the total vertical and horizontal parts to create size
    col_rows = calc_columns_rows(pixels)
    size_single = imgsize(tmpdir_path+'/01_01.png')
    print((col_rows[0]*size_single[0],col_rows[1]*size_single[1]))
    img = Image.new('RGB', (col_rows[0]*size_single[0],col_rows[1]*size_single[1]), color = 'white',)
    img.save('canvas.jpg')

def pastetoimg(canvaspath,name,dir):
    #paste image onto canvas
    bg = Image.open(canvaspath)
    for subdir, dirs, files in os.walk(dir):
        for filename in files:
            filepath = subdir + os.sep + filename

            if filepath.endswith(".jpg") or filepath.endswith(".png"):
                fg = Image.open(filepath)
                pos = findpos(filepath)
                size = imgsize(filepath)
                print((pos[1]*size[0],pos[0]*size[1]), 'positions')
                bg.paste(fg, (pos[1]*size[0],pos[0]*size[1]))

    print('__________________',str(pathlib.Path(__file__).parent.resolve())+'/'+name+'.jpg')
    bg.save(str(pathlib.Path(__file__).parent.resolve())+'/'+name+'.jpg')

def imgtopxl(imgpath,pixels,name):
    #master function

    filename = Path(imgpath).name
    print(filename)
    print(imgpath)
    try:
        global tmpdir_path 
        tmpdir_path = img_to_dir(imgpath)
        tmp_img_path = tmpdir_path +"/"+ filename
        print(tmp_img_path)
    except FileNotFoundError:
        print('No such directory or file exists')

    try:
        slice(tmp_img_path, pixels)
        print(filename,'successfully split into',pixels,'pixel parts')
        print(tmp_img_path)
    except Exception as e:
        print('error occurred while slicing image')
        print(tmp_img_path)
        

    os.remove(tmp_img_path)
    print(tmpdir_path)
    try:
        imgtosolid(tmpdir_path)
    except Exception as e:
        print(e, 'exception')
    
    createcanvas(pixels)

    pastetoimg('canvas.jpg', name, tmpdir_path)
    print('deleting residual files...')

    
    try:
        os.remove(tmpdir_path)
    except PermissionError:
        print('device refused to permit deleteing of /temp, manually deleting...')
        for subdir, dirs, files in os.walk(tmpdir_path):
            for filename in files:
                filepath = subdir + os.sep + filename
                os.remove(filepath)
        try:
            os.rmdir(tmpdir_path)
            print("manual removal successful")
        except:
            print("manual removal failed, please remove /temp folder from folder containing this file")

    os.remove('canvas.jpg')

    print('photo has been successfully pixelfied, please check folder for', name+'.jpg')

final_img = imgtopxl("conceptart.png", 100, "conceptart")