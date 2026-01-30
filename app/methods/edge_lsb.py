import cv2
import numpy as np

# ---------- Shared Bit Helpers ----------
def message_to_bits_with_length(message: str):
    """Convert message to bits with 32-bit header."""
    message_bytes = message.encode("utf-8")
    length = len(message_bytes)
    length_bits = [int(b) for b in format(length, "032b")]
    message_bits = [int(b) for byte in message_bytes for b in format(byte, "08b")]
    return length_bits + message_bits


def bits_to_message_with_length(bits):
    """Extract message using 32-bit header and safely handle bit overrun."""
    if len(bits) < 32:
        return ""
    length_bits = bits[:32]
    message_length = int("".join(map(str, length_bits)), 2)
    total_bits_needed = 32 + (message_length * 8)

    # ✅ Prevent reading extra garbage bits
    bits = bits[:total_bits_needed]

    message_bits = bits[32:]
    message_bytes = bytearray()
    for i in range(0, len(message_bits), 8):
        byte = int("".join(map(str, message_bits[i:i+8])), 2)
        message_bytes.append(byte)
    return message_bytes.decode("utf-8", errors="ignore")


# ---------- Encode ----------
def encode(image: np.ndarray, message: str) -> np.ndarray:
    """Embed message bits into edge pixels of the image."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    img_copy = image.copy().astype(np.uint8)
    h, w, _ = img_copy.shape

    bits = message_to_bits_with_length(message)
    idx = 0

    # Get coordinates of edge pixels in consistent order
    edge_coords = np.column_stack(np.where(edges != 0))

    for y, x in edge_coords:
        for c in range(3):
            if idx >= len(bits):
                break
            pixel_val = int(img_copy[y, x, c])
            pixel_val = (pixel_val & ~1) | bits[idx]
            img_copy[y, x, c] = np.uint8(pixel_val)
            idx += 1
        if idx >= len(bits):
            break

    if idx < len(bits):
        raise ValueError("Message too large for available edge pixels!")

    return img_copy


# ---------- Decode ----------
def decode(image: np.ndarray) -> str:
    """Extract message bits from edge pixels."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    h, w, _ = image.shape
    bits = []

    edge_coords = np.column_stack(np.where(edges != 0))

    for y, x in edge_coords:
        for c in range(3):
            bits.append(int(image[y, x, c]) & 1)

    # ✅ Use safe truncation based on header
    return bits_to_message_with_length(bits)
                