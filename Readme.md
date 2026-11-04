# Barcode Studio

A simple desktop app to create and scan barcodes, built with Python and Tkinter.

## Features

- Generate Code 128 barcodes and save them as PNG
- Scan barcodes from an image
- Scan barcodes live with your webcam

## Installation

1. Install dependencies:

```bash
pip install python-barcode pillow opencv-python zxing-cpp numpy
```

2. Run the app:

```bash
python main.py
```

## Usage

**Generator:** type your text, click **Generate**, then **Save PNG**.

**Scanner:** click **Upload Image** or **Start Webcam**. The result appears in the box, and you can copy it with **Copy**.

<details>
<summary><b>📷 Webcam not opening / Camera permission errors</b></summary>

1. Close other applications using the camera (e.g., Zoom, Teams, Chrome).
2. Restart the script or application.

</details>

<details>
<summary><b>🔍 No barcode detected in image</b></summary>

- Ensure the image is well-lit and not blurry.
- Make sure the entire barcode is visible and uncropped.
- Try lowering image resolution if processing large high-DPI images.

</details>
