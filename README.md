# Py_OCR

<p align="center"><img src="assets\logo.png"></p>

> Py_OCR is an OCR tool used to scan documents and pdfs and sort through specified data from the scan.

---

## Installation

<https://0x00sec.gitbook.io/py_ocr-documentation/installation/py_ocr-installaion>

Py_OCR Only works with python3

---

## Usage examples

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

### Release History/Bug Fixes

* 0.2.0
  * Tried implementing easyocr to work with pytesseract, their libraries clash and until a fix can be found, all of that code has been commented 
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

* Created by – Envxsion, Midi.Rc
