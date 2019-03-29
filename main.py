#This the entry point for your Repl.
#source: https://github.com/satyarth/pixelsort 


#TODO
"""
-use logging metrics to slow down pixel counting?
-options based in tuple ternary conditions
	* test = ("zero","one","two",etc...)[num]
-progress bars
-fix the random stopping and ending program? really random but annoying
	* pretty sure this is unfixable as its a problem with repl.it's server specs
	* attempted to fix by removing the dots for optimization (assigning pixels.append to a variable and using that, its faster) which increased speed on pictures around 1080p but still breaks if over
	* maybe throttle based on resolution?
-animate option from second generator
	* second gens:
	* https://github.com/okayzed/pixelsort.py
	* https://github.com/rkargon/pixelsorter 
-all in one file, likely using class command
"""

from pixelsort import main

if __name__ == "__main__":
    main()