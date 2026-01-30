# Image Steganography using LSB and Edge-based LSB

This project implements image steganography techniques that allow secret messages to be hidden inside digital images without noticeable visual distortion. The system supports two spatial-domain steganography methods:

- **Least Significant Bit (LSB) Steganography**
- **Edge-based LSB Steganography (using Canny Edge Detection)**

A dynamic **Streamlit-based web interface** allows users to upload images, encode custom messages, decode hidden data, and visually compare original and encoded images.

---

##  What is Steganography?

Steganography is the practice of concealing information within another medium so that the existence of the hidden message itself is not apparent. Unlike cryptography, which hides the content of a message, steganography hides the presence of the message.

In this project, digital images are used as the carrier medium due to their high redundancy and tolerance for minor pixel modifications.

---

## Features

- Upload any image (PNG / JPG / JPEG)
- Enter a custom secret message
- Choose between:
  - LSB Steganography
  - Edge-based LSB Steganography
- Encode and download the stego image
- Decode hidden messages from encoded images
- Visual comparison between original and encoded images
- Modular and extensible code structure

---

## Steganography Techniques Used

### 1. Least Significant Bit (LSB)
- Replaces the least significant bit of pixel values with message bits
- High data capacity and fast execution
- Simple to implement
- Vulnerable to compression and statistical analysis

### 2. Edge-based LSB
- Uses Canny edge detection to identify edge pixels
- Embeds message bits only in edge regions
- Better imperceptibility and security
- Lower embedding capacity compared to standard LSB

---

## Technologies Used

- **Python 3.11+**
- **Streamlit** – Web interface
- **OpenCV** – Image processing and edge detection
- **NumPy** – Bit-level operations
- **Pillow (PIL)** – Image handling

---

## Project Structure

image-steganography/
│
├── steganography_app.py # Main Streamlit application
├── requirements.txt # Python dependencies
├── README.md # Project documentation
│
├── methods/
│ ├── lsb.py # LSB steganography implementation
│ └── edge_lsb.py # Edge-based LSB implementation
│
├── paper/
│ └── steganography_paper.tex # IEEE-format research paper
│
├── sample_images/ # Optional test images
└── .gitignore

---

##  How to Run the Project

### Clone the Repository
git clone https://github.com/YOUR_USERNAME/image-steganography.git
cd image-steganography

python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

streamlit run steganography_app.py

## Results
| Technique      | Capacity | Imperceptibility | Robustness | Speed  |
| -------------- | -------- | ---------------- | ---------- | ------ |
| LSB            | High     | Good             | Low        | Fast   |
| Edge-based LSB | Medium   | Excellent        | Moderate   | Medium |

## Author
Yash Mehta
Computer Science and Engineering
College Project – Image Steganography# image-steganography
