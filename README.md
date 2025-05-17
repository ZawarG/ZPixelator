# 🧩 Pixelator Web App

A clean and responsive web application that allows users to upload an image and pixelate it based on a specified number of pixels. At its core is Zpyxel, a custom image pixelation algorithm I developed when I was 14. The application uses Flask for the backend and HTML, CSS, and JavaScript for the frontend.

<div align="center">
  <img src="https://github.com/user-attachments/assets/c5a257c8-c4fb-40cd-a195-c831e54bb88d">
</div>

1. **Clone the repository** `git clone https://github.com/ZawarG/ZPixelator`

2. **Install dependencies** `pip install -r requirements.txt`

3. **Run the application** `app.py`

4. **Open your browser and visit** `http://127.0.0.1:5000`

##  Tech Stack

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript

## How It Works
**1. Temporary Directory Setup**

A `/temp` directory is created (if it doesn’t already exist), and the user’s uploaded image is copied into this directory. This isolates file operations and keeps the main project directory clean.

**2. Image Slicing with `accurate_slice()`**

The image is divided into a grid of smaller slices based on the user's desired number of total pixels. The slicing algorithm calculates the most square-like arrangement possible (e.g., 32 × 32 for 1024 pixels) and crops out the slices accordingly, adjusting the edges to capture leftover pixels.

**3. Solid Color Conversion (`imgtosolid`)**

Each image slice is opened, and the average visible (non-transparent) color is computed. A new image filled with this average color replaces the original slice. This drastically reduces detail, producing a pixelated aesthetic.

**4. Canvas Generation (`createcanvas`)**

A blank white canvas is created with dimensions based on the combined sizes of all the slices. This ensures the final composition reflects the original image size, even if slice sizes vary slightly due to rounding.

**5. Reconstruction (`pastetoimg`)**

Each solid-colored slice is pasted back into its appropriate position on the canvas. The exact placement is calculated from the filenames (e.g., `3_2.png` → row 3, column 2) and their respective dimensions.

**6. Saving and Cleanup**

The final pixelated image is saved to the `/static/photos/` directory using the user-defined filename. Temporary files and the canvas image are deleted, and the `/temp` directory is removed, keeping the environment clean for future conversions.
