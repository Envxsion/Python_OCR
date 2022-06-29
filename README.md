# Py_OCR

<p align="center"><img src="assets\logo.png"></p>

> Py_OCR is an OCR tool used to scan documents and pdfs and sort through specified data from the scan.


## Installation



```sh
pip install -r requirements.txt
```
Py_OCR Only works with python3

## Usage example

```sh
python main.py --image images/test-1.png  --gray --denoise
```

## Release History
*0.1.6
    * Multipage pdfs can now be converted, converted pdfs are stored in the "frompdf" folder
* 0.1.5
    * Pdfs can now be converted to images for text recognition (though it is very inaccurate)
* 0.1.1
    * Fixed a major issue where the original image was being taken in for text conversion, and not the modified version (I'm dumb)
* 0.1.0 - Initial closed-release with command-line features
    * Arguments can now be passed through the command-line to modify and customise the result as needed
* 0.0.5
    * Word detection is now live :D
* 0.0.4 
    * Boxes around detected characters with prediction added
* 0.0.3
    * image_to_string working, a bit inaccurate but fixable
* 0.0.2
    * Image correction working, new requirements
* 0.0.1
    * Base functionality (Work in progress)



* Created by – Envxsion, Midi.Rc




