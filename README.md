# i2i-Academy-AppliedImageProcessing-9

This project is an Automated License Plate Recognition (ALPR) system developed using Python, OpenCV, and EasyOCR. The system identifies and extracts license plate text from vehicle images through a three-stage image processing pipeline.

## Features
- **Image Preprocessing:** Grayscale conversion, bilateral filtering, and edge detection to isolate features.
- **Candidate Filtering:** Contour analysis and aspect-ratio filtering to identify potential plate regions.
- **OCR Integration:** Text extraction using EasyOCR with image enhancement (Cubic Interpolation) for higher accuracy.

## Methodology
The system follows a structured pipeline:
1. **Preprocessing:** Reduces noise and highlights boundaries.
2. **Detection:** Isolates candidates based on geometric properties.
3. **Recognition:** Upscales images and extracts text via OCR.

## Technical Requirements
To run this project, you need the following libraries:
- `opencv-python`
- `imutils`
- `easyocr`
- `numpy`

Install them with:
```bash
pip install opencv-python imutils easyocr numpy
```

## Usage
1. Place your image file as `car.jpeg` in the project directory.
2. Run the script:
```bash
   python main.py
```
