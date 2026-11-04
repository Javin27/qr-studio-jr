# Barcode Studio

A lightweight Windows desktop app with three pages in one window:
- Home: choose Generator or Scanner
- Generator: create Code 128 barcodes and save PNG files
- Scanner: scan barcode images or use a webcam

## Requirements
- Python 3.10 or newer recommended
- Windows, macOS, or Linux
- A webcam for live scanning

## Setup (Windows)
1. Extract the project folder.
2. Open PowerShell or CMD in the folder.
3. Create and activate a virtual environment:

   python -m venv .venv
   .venv\\Scripts\\activate

4. Install dependencies:

   python -m pip install -r requirements.txt

5. Run:

   python main.py

## Notes
- The generator currently creates Code 128 barcodes.
- The scanner uses ZXing-C++, which supports common 1D barcode formats.
- Webcam scanning uses OpenCV. If the camera does not open, check Windows camera privacy permissions and close other apps using the camera.
