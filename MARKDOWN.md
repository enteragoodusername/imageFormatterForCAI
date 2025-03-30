# Image formatter for the CAI data collection

This python script takes an input directory and then makes a copy of the project where images are turned into 128x128 rbg png images. It retains the hierarchy of folders.

It also gives the new files the correct names and handles adding new images to an existing copy. 

It supports JPG, PNG, HEIC, and WEBP formats

## Installation
You need to install the pillow_heif pip module
```
    pip install pillow_heif 
```

Afterwards you can just place formatter.py in the same directory where your images directory is and run the script from there. It will then prompt you for input.
