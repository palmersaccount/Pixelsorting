try:
    import Image
except ImportError:
    from PIL import Image
import argparse
import os
import random
import sys
import time

import pyimgur
import requests
import arrow
import interval
import psutil
import sorter
import sorting
import util


def clear():
    return os.system('cls' if os.name == 'nt' else 'clear')

def read_image_input(url_input):
    ###return order: url, url_given, url_random, random_url
    try:
        url = url_input
        Image.open(requests.get(url, stream=True).raw)
        return url, True, False, None
    except IOError:
        random_url = str(random.randint(0,5))
        url_options = {
            '0': "https://i.imgur.com/1UBT6fK.png",
            '1': "https://i.imgur.com/5VqeP6Y.jpg?1",
            '2': "https://i.imgur.com/rfasPI6.jpg?1",
            '3': "https://i.imgur.com/wFzJ6ua.jpg?1",
            '4': "https://i.imgur.com/pZRkMzP.jpg?1",
            '5': "https://i.imgur.com/HwchiaD.jpg?1",
            '6': "https://i.imgur.com/Z438D1L.jpg"
            }
        try:
            return ((url_options[(url_input if url_input in ['0','1','2','3','4','5','6'] else random_url)] if url_input in ['',' ','0','1','2','3','4','5','6'] else url_input), 
            (False if url_input in ['',' ','0','1','2','3','4','5','6'] else True), 
            (True if url_input in ['',' '] else False), 
            (random_url if url_input in ['',' '] else None))
        except KeyError:
            return url_options[random_url], False, True, random_url

def read_interval_function(int_func_input):
    try:
        return {
            "random": interval.random,
            "threshold": interval.threshold,
            "edges": interval.edge,
            "waves": interval.waves,
            "snap": interval.snap_sort,
            "file": interval.file_mask,
            "file-edges": interval.file_edges,
            "shuffle-total": interval.shuffle_total,
            "shuffle-axis": interval.shuffled_axis,
            "none": interval.none,
            }[int_func_input]
    except KeyError:
        return interval.random 

def read_sorting_function(sort_func_input):
    try:
        return {
            "lightness": sorting.lightness,
            "hue": sorting.hue,
            "intensity": sorting.intensity,
            "minimum": sorting.minimum,
            "saturation": sorting.saturation,
            }[sort_func_input]
    except KeyError:
        return sorting.lightness

def read_preset(preset_input):
    try:
        #order-- arg_parse_input, int_func_input, sort_func_input, preset_true, int_rand, sort_rand
        int_func_input = {
                '1': 'random',
                '2': 'threshold',
                '3': 'edges',
                '4': 'waves'}
        sort_func_input = {
                '1': 'lightness',
                '2': 'hue',
                '3': 'intensity',
                '4': 'minimum',
                '5': 'saturation'}
        return {
            "main": (("-r 50 -c 250 -a 45"), "random", "intensity", True, False, False),
            "full random": (("-a "+str(random.randrange(0, 360))+" -c "+str(random.randrange(50, 500, 15))+" -u "+str((random.randrange(50, 100, 5)/100))+" -t "+str((random.randrange(5, 50, 5)/100))+" -r "+str(random.randrange(5, 100, 5))), int_func_input[str(random.randint(1,4))], sort_func_input[str(random.randint(1,5))], True, True, True)
        }[preset_input]
    except KeyError:
        print("[WARNING] Invalid preset name, no preset will be applied")
        return None, None, None, False, None, None

def main():
    clear()

    print("Pixel sorting based on web hosted images.\nRewritten by @wolfembers for usage on web based IDEs.\nThe output image is uploaded to imgur after being sorted.\n"+(35*'--')+"\nTo see any past runs, args used, and the result\nopen 'output.txt'\n"+(35*'--')+"\nThanks for using this program!\nPress any key to continue...")
    input()
    clear()

    #url input
    url_input = input("Please input the URL of the image or the default image #:\n(this might take a while depending the image resolution)\n")
    url, url_given, url_random, random_url = read_image_input(url_input)
    input_img = Image.open(requests.get(url, stream=True).raw)
    width, height = input_img.size
    resolution_msg = "Resolution: "+str(width)+"x"+str(height)
    image_msg = (("[WARNING] No image url given, using " + ("random" if url_random else "chosen") + " default image " + (random_url if url_random else str(url_input))) if not url_given else "Using given image " + resolution_msg)
    clear()

    #preset input
    print(image_msg+"\n"+resolution_msg)
    preset_q = input("\nDo you wish to apply a preset? (y/n)\n")
    clear()
    if preset_q in ['y','yes','1']:
        print("Preset options:\n-1|main -- Main args (r 50, c 250, a 45, random, intensity)\n-2|full random -- Randomness in every arg!")
        preset_input = input("\nChoice: ").lower()
        preset_options = ['main', 'full random']
        if preset_input in preset_options:
            preset_choices = {
                'main': '1',
                'full random': '2'
            }
            preset_input = preset_choices[preset_input]
        if preset_input in ['1','2']:
            preset_input = {
                '1': 'main',
                '2': 'full random'
            }[preset_input]
        #if presets are applied, they take over args
        arg_parse_input, int_func_input, sort_func_input, preset_true, int_rand, sort_rand = read_preset(preset_input)
    else:
        preset_true = False
    clear()

    #int func, sort func
    if not preset_true:
        #int func input
        print(image_msg+"\n"+resolution_msg)
        print("\nWhat interval function are you using?\nOptions (default is random):\n-1|random\n-2|threshold\n-3|edges\n-4|waves\n-5|snap\n-6|shuffle-total\n-7|shuffle-axis\n-8|file\n-9|file-edges\n-10|none\n-11|random select")
        int_func_input = input("\nChoice: ").lower()
        int_func_options = ["random","threshold","edges","waves","shuffle-total","shuffle-axis","file","file-edges","none"]
        if int_func_input in ['1','2','3','4','5','6','7','8','9','10']:
            int_func_input = {
                '1': 'random',
                '2': 'threshold',
                '3': 'edges',
                '4': 'waves',
                '5': 'snap',
                '6': 'shuffle-total',
                '7': 'shuffle-axis',
                '8': 'file',
                '9': 'file-edges',
                '10': 'none'
            }[int_func_input]
            int_rand = False
        elif int_func_input in ['11','random select']:
            int_func_input = int_func_options[random.randint(0,3)]
            int_rand = True
        shuffled = True if int_func_input in ['shuffle-total', 'shuffle-axis'] else False
        snapped = True if int_func_input in ['snap'] else False

        int_msg = ("Interval function: " if not int_rand else "Interval function (randomly selected): ") + int_func_input if int_func_input in int_func_options else "Interval function: random (default)"
        clear()

        #sort func input
        print(image_msg+"\n"+int_msg+"\n"+resolution_msg)
        print("\nWhat sorting function are you using?\nOptions (default is lightness):\n-1|lightness\n-2|hue\n-3|intensity\n-4|minimum\n-5|saturation\n-6|random select")
        sort_func_input = input("\nChoice: ").lower()
        sort_func_options = ["lightness","hue","intensity","minimum","saturation"]
        if sort_func_input in ['1','2','3','4','5']:
            sort_func_input = {
                '1': 'lightness',
                '2': 'hue',
                '3': 'intensity',
                '4': 'minimum',
                '5': 'saturation'
            }[sort_func_input]
            sort_rand = False
        elif sort_func_input in ['6','random select']:
            sort_func_input = sort_func_options[random.randint(0,4)]
            sort_rand = True
        else:
            sort_rand = False
        sort_rand is False if sort_func_input in ['1','2','3','4','5',"lightness","hue","intensity","minimum","saturation"] else (sort_rand is True if sort_func_input in ['6','random select'] else False)
        sort_msg = ("Sorting function: " if not sort_rand else "Sorting function (randomly selected): ") + sort_func_input if sort_func_input in sort_func_options else "Sorting function: lightness (default)"
        clear()

    #int func msg, sort func msg
    if preset_true:
        int_msg = ("Interval function: " if not int_rand else "Interval function (randomly selected): ") + int_func_input if int_func_input in ["random","threshold","edges","waves","file","file-edges","none"] else "Interval function: random (default)"
        
        sort_msg = ("Sorting function: " if not sort_rand else "Sorting function (randomly selected): ") + sort_func_input if sort_func_input in ["lightness","hue","intensity","minimum","saturation"] else "Sorting function: lightness (default)"

    #args
    if not preset_true:
        needs_help = input("Do you need help with args? (y/n)\n")
        clear()
        if needs_help in ['y','yes','1']:
            print(("[WARNING] No image url given, using default image "+str(random_url) if url_given is False else "Using given image")+
            ("\nInterval function: " + int_func_input if int_func_input in int_func_options else "\nInterval function: threshold (default)")+
            ("\nSorting function: "+sort_func_input if sort_func_input in sort_func_options else "\nSorting function: lightness (default)")+"\n"+resolution_msg+
            "\n\nWhat args will you be adding?\n" +
                '{:21}'.format("Parameter") + '{:>6}'.format("| Flag |") + '{:>12}'.format("Description") + "\n" +
                '{:21}'.format("---------------------") + '{:>6}'.format("|------|") + '{:>12}'.format("------------") + "\n" +
                '{:21}'.format("Randomness") + '{:>6}'.format("| -r   |") + "What percentage of intervals not to sort. 0 by default." + "\n" +
                '{:21}'.format("Char. length") + '{:>6}'.format("| -c   |") + "Characteristic length for the random width generator.\n"+ 29 * ' ' + "Used in mode random." + "\n" +
                '{:21}'.format("Angle") + '{:>6}'.format("| -a   |") + "Angle at which you're pixel sorting in degrees. 0 (horizontal) by default." + "\n" +
                '{:21}'.format("Threshold (lower)") + '{:>6}'.format("| -t   |") + "How dark must a pixel be to be considered as a 'border' for sorting?\n" + 29 * ' ' + "Takes values from 0-1. 0.25 by default. Used in edges and threshold modes." + "\n" +
                '{:21}'.format("Threshold (upper)") + '{:>6}'.format("| -u   |") + "How bright must a pixel be to be considered as a 'border' for sorting?\n"+29*' '+"Takes values from 0-1. 0.8 by default. Used in threshold mode.")
        else:
            print(("[WARNING] No image url given, using default image "+str(random_url) if url_given is False else "Using given image")+
            ("\nInterval function: " + int_func_input if int_func_input in int_func_options else "\nInterval function: threshold (default)")+
            ("\nSorting function: "+sort_func_input if sort_func_input in sort_func_options else "\nSorting function: lightness (default)")+"\n"+resolution_msg+
            "\n\nWhat args will you be adding?\n" +
                '{:21}'.format("Parameter") + '{:>6}'.format("| Flag |") +  "\n" +
                '{:21}'.format("---------------------") + '{:>6}'.format("|------|") + "\n" +
                '{:21}'.format("Randomness") + '{:>6}'.format("| -r   |") + "\n" +
                '{:21}'.format("Char. length") + '{:>6}'.format("| -c   |") + "\n" +
                '{:21}'.format("Angle") + '{:>6}'.format("| -a   |") + "\n" +
                '{:21}'.format("Threshold (lower)") + '{:>6}'.format("| -t   |") + "\n" +
                '{:21}'.format("Threshold (upper)") + '{:>6}'.format("| -u   |"))
        arg_parse_input = input("\n\nArgs: ")
        clear()

    ##args
    p = argparse.ArgumentParser(description="pixel mangle an image")
    p.add_argument("-t", "--bottom_threshold", type=float, help="Pixels darker than this are not sorted, between 0 and 1", default=0.25)
    p.add_argument("-u", "--upper_threshold", type=float, help="Pixels darker than this are not sorted, between 0 and 1", default=0.8)
    p.add_argument("-c", "--clength", type=int, help="Characteristic length of random intervals", default=50)
    p.add_argument("-a", "--angle", type=float, help="Rotate the image by an angle (in degrees) before sorting", default=0)
    p.add_argument("-r", "--randomness", type=float, help="What percentage of intervals are NOT sorted", default=15)

    #add a space in front of arg parse unless there is one or none was entered
    arg_parse_input = None if (arg_parse_input in ['',' '] or arg_parse_input[0]==' ') else (' ' + arg_parse_input)

    if arg_parse_input is not None:
        args_in=arg_parse_input.split(' -')
        args_in[:]=['-'+x for x in args_in]
        args_in.pop(0)
    else:
        print("No args given")
        args_in = ""

    __args = p.parse_args(args_in)

    output_image_path = "image.png"
    interval_function = read_interval_function(int_func_input)
    sorting_function = read_sorting_function(sort_func_input)
    angle = __args.angle
    randomness = __args.randomness

    #remove old image files that didn't get deleted before
    if os.path.isfile(output_image_path):
        print("Detected old files...")
        os.remove(output_image_path)
        print("Removed old files!")
        clear()
    
    print(image_msg+"\n"+("Preset: "+preset_input if preset_true else "No preset applied")+"\n"+int_msg+"\n"+sort_msg)
    

    #even if they were never given, at some point they need to be assigned to default values properly
    if int_func_input in ['',' ']:
        int_func_input = 'threshold'
    if sort_func_input in ['',' ']:
        sort_func_input = 'lightness'


    if int_func_input in ["threshold", "edges", "file-edges"]:
        print("Lower threshold: ", __args.bottom_threshold)
    if int_func_input == "threshold":
        print("Upper threshold: ", __args.upper_threshold)
    if int_func_input in ["random", "waves"]:
        print("Characteristic length: ", __args.clength)
    print("Randomness: ", __args.randomness, "%") 
    print("Angle: ", __args.angle, "°")
    print("------------------------------")

    print("Opening image...")
    print(resolution_msg)

    print("Converting to RGBA...")
    input_img.convert('RGBA')
    
    print("Rotating image...")
    input_img = input_img.rotate(angle, expand=True)
    
    print("Getting data...")
    data = input_img.load()

    print("Getting pixels...")
    pixels = []
    append = pixels.append
    size1 = input_img.size[1]
    size0 = input_img.size[0]

    for y in range(size1):
        append([])
        for x in range(size0):
            pixels[y].append(data[x, y])

    print("Determining intervals...")
    intervals = interval_function(pixels, __args, url)
    
    if not shuffled or snapped:
        print("Sorting pixels...")
        sorted_pixels = sorter.sort_image(pixels, intervals, randomness, sorting_function)
    else:
        sorted_pixels = intervals

    print("Placing pixels in output image...")
    output_img = Image.new('RGBA', input_img.size)
    size1 = output_img.size[1]
    size0 = output_img.size[0]
    for y in range(size1):
        for x in range(size0):
            output_img.putpixel((x, y), sorted_pixels[y][x])
            
    if angle is not 0:
        print("Rotating output image back to original orientation...")
        output_img = output_img.rotate(360-angle, expand=True)
        
        print("Crop image to apropriate size...")
        output_img = util.crop_to(output_img, url)
        
    print("Saving image...")
    output_img.save(output_image_path)

    #upload to imgur
    CLIENT_ID = "d7155a81c1e37bd"
    PATH = output_image_path
    date_time = str(arrow.utcnow().format('MM-DD-YYYY HH:mm'))

    out_msg = "\nStarting image url: "+url+("\nInt func: " if not int_rand else "\nInt func (randomly chosen): ")+int_func_input+("\nSort func: " if not sort_rand else "\nSort func (randomly chosen): ")+sort_func_input+"\nArgs: "+(arg_parse_input if arg_parse_input is not None else "No args")+"\nSorted on: "+date_time
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(PATH, title="Pixel sorted", description=out_msg)
    print("Image uploaded!")

    #delete old file, seeing as its uploaded
    print("Removing local file...")
    os.remove(output_image_path)

    #output to 'output.txt'
    print("Saving config to 'output.txt'...")
    with open("output.txt", "a") as f:
        f.write("\nStarting image url: "+url+("\nInt func: " if not int_rand else "\nInt func (randomly chosen): ")+int_func_input+("\nSort func: " if not sort_rand else "\nSort func (randomly chosen): ") +
                sort_func_input+"\nArgs: "+(arg_parse_input if arg_parse_input is not None else "No args")+"\nSorted on: "+date_time+"\n\nSorted image: "+uploaded_image.link+"\n"+(35*'-'))
    
    print("Done!")
    print("Link to image: " + uploaded_image.link)
    output_img.show()
