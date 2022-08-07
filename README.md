# Py_OCR

An OCR using Python for School Assessed Coursework in Applied Computing


<p align="center"><img src="assets\logo.png"></p>

## Demo

<p align="center"><img src="assets\CLIgif.gif"></p>




## Features

- Will be added later

## Installation

<https://0x00sec.gitbook.io/py_ocr-documentation/installation/py_ocr-installaion>

Py_OCR Only works with python3

---

## Usage/Examples

```sh
python main.py --pdf PDF_Examples/testpdf2.pdf --denoise --gray --adapt
```

---

---

### Best Results so far

```sh
python main.py --pdf "images\PDF_Examples\Gordon House [M3202]-Service-07-06-2022.pdf"  -b --psm 11
```

---

---

## Authors

- [@Envxsion](https://github.com/Envxsion)
- [@Midi.Rc](https://github.com/greube)

## Lessons Learned

- DO NOT build a GUI using python, Django exists
- Using libraries and features without understanding them properly backfires pretty regularly
- Teamwork is important, it kept us going :D

In general, we learnt loads about new libaries, inbuilt python standard libaries and dipped our toes into the wacky world of AI, Image Recognition and gained an appreciation for its complexity.
### Release History/Bug Fixes
* 0.2.5
  * Linking the UI to maingui in progress, the buttons work but the displays don't for now. Work in Progess.
* 0.2.1
  * main.gui file has been created to handle all the logic of the GUI file
* 0.2.0
  * Tried implementing easyocr to work with pytesseract, their libraries clash and until a fix can be found, all of that code has been commented.
* 0.1.9
  * Significant improvement in text detection by using <https://tesseract-ocr.github.io/tessdoc/Data-Files> tessdata-best instead of the default testdata training model along with custom oem, psm and adaptive thresholding options. **tessdata-best will _need_ to be manually installed in your local TESSERACT_OCR folder (and renamed to "tessdata") in Program Files until we implement a better solution**
* 0.1.8
  * Optimized the source code (about twice as fast)
* 0.1.7
  * Adaptive thresholding command fixed | The config in image_to_text removed, it was causing a buttload of issues with no apparent solutions | Table extraction is work in progress
* 0.1.6
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



