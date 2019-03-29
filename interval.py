try:
    import Image
    import ImageFilter
except ImportError:
    from PIL import Image, ImageFilter
import random as rand
import util
import requests

black_pixel = (0, 0, 0, 255)
white_pixel = (255, 255, 255, 255)

def edge(pixels, args, url):
	img = Image.open(requests.get(url, stream=True).raw)
	img = img.rotate(args.angle, expand=True)
	edges = img.filter(ImageFilter.FIND_EDGES)
	edges = edges.convert('RGBA')
	edge_data = edges.load()

	filter_pixels = []
	appendF = filter_pixels.append
	edge_pixels = []
	appendE = edge_pixels.append
	intervals = []
	appendInt = intervals.append

	size1 = img.size[1]
	size0 = img.size[0]

	print("Defining edges...")
	for y in range(size1):
		appendF([])
		for x in range(size0):
			filter_pixels[y].append(edge_data[x, y])

	print("Thresholding...")
	for y in range(len(pixels)):
		appendE([])
		for x in range(len(pixels[0])):
			if util.lightness(filter_pixels[y][x]) < args.bottom_threshold:
				edge_pixels[y].append(white_pixel)
			else:
				edge_pixels[y].append(black_pixel)

	print("Cleaning up edges...")
	for y in range(len(pixels) - 1, 1, -1):
		for x in range(len(pixels[0]) - 1, 1, -1):
			if edge_pixels[y][x] == black_pixel and edge_pixels[y][x - 1] == black_pixel:
				edge_pixels[y][x] = white_pixel

	print("Defining intervals...")
	for y in range(len(pixels)):
		appendInt([])
		for x in range(len(pixels[0])):
			if edge_pixels[y][x] == black_pixel:
				intervals[y].append(x)
		intervals[y].append(len(pixels[0]))
	return intervals

def threshold(pixels, args, url):
	intervals = []
	appendInt = intervals.append

	print("Defining intervals...")
	for y in range(len(pixels)):
		appendInt([])
		for x in range(len(pixels[0])):
			if util.lightness(pixels[y][x]) < args.bottom_threshold or util.lightness(pixels[y][x]) > args.upper_threshold:
				intervals[y].append(x)
		intervals[y].append(len(pixels[0]))
	return intervals

def random(pixels, args, url):
	intervals = []
	appendInt = intervals.append

	print("Defining intervals...")
	for y in range(len(pixels)):
		appendInt([])
		x = 0
		while True:
			width = util.random_width(args.clength)
			x += width
			if x > len(pixels[0]):
				intervals[y].append(len(pixels[0]))
				break
			else:
				intervals[y].append(x)
	return intervals

def waves(pixels, args, url):
	intervals = []
	appendInt = intervals.append

	print("Defining intervals...")
	for y in range(len(pixels)):
		appendInt([])
		x = 0
		while True:
			width = args.clength + rand.randint(0, 10)
			x += width
			if x > len(pixels[0]):
				intervals[y].append(len(pixels[0]))
				break
			else:
				intervals[y].append(x)
	return intervals

def file_mask(pixels, args, url):
	intervals = []
	file_pixels = []

	int_file = input("Please enter the URL of an int file or hit enter to randomly select one:\n")
	img = Image.open(requests.get(int_file, stream=True).raw)
	img = img.convert('RGBA')
	img = img.rotate(args.angle, expand=True)
	data = img.load()
	for y in range(img.size[1]):
		file_pixels.append([])
		for x in range(img.size[0]):
			file_pixels[y].append(data[x, y])
			
	print("Cleaning up edges...")
	for y in range(len(pixels) - 1, 1, -1):
		for x in range(len(pixels[0]) - 1, 1, -1):
			if file_pixels[y][x] == black_pixel and file_pixels[y][x - 1] == black_pixel:
				file_pixels[y][x] = white_pixel
				
	print("Defining intervals...")
	for y in range(len(pixels)):
		intervals.append([])
		for x in range(len(pixels[0])):
			if file_pixels[y][x] == black_pixel:
				intervals[y].append(x)
		intervals[y].append(len(pixels[0]))
		
	return intervals

def file_edges(pixels, args, url):
	int_file = input("Please enter the URL of an int file:\n")
	img = Image.open(requests.get(int_file, stream=True).raw)
	img = img.rotate(args.angle, expand=True)
	img = img.resize((len(pixels[0]), len(pixels)), Image.ANTIALIAS)
	edges = img.filter(ImageFilter.FIND_EDGES)
	edges = edges.convert('RGBA')
	edge_data = edges.load()
	
	filter_pixels = []
	edge_pixels = []
	intervals = []
	
	print("Defining edges...")
	for y in range(img.size[1]):
		filter_pixels.append([])
		for x in range(img.size[0]):
			filter_pixels[y].append(edge_data[x, y])
			
	print("Thresholding...")
	for y in range(len(pixels)):
		edge_pixels.append([])
		for x in range(len(pixels[0])):
			if util.lightness(filter_pixels[y][x]) < args.bottom_threshold:
				edge_pixels[y].append(white_pixel)
			else:
				edge_pixels[y].append(black_pixel)
				
	print("Cleaning up edges...")
	for y in range(len(pixels) - 1, 1, -1):
		for x in range(len(pixels[0]) - 1, 1, -1):
			if edge_pixels[y][x] == black_pixel and edge_pixels[y][x - 1] == black_pixel:
				edge_pixels[y][x] = white_pixel
				
	print("Defining intervals...")
	for y in range(len(pixels)):
		intervals.append([])
		for x in range(len(pixels[0])):
			if edge_pixels[y][x] == black_pixel:
				intervals[y].append(x)
		intervals[y].append(len(pixels[0]))
	return intervals

def none(pixels, args, url):
	intervals = []
	appendInt = intervals.append
	for y in range(len(pixels)):
		appendInt([len(pixels[y])])
	return intervals