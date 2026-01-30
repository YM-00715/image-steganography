import numpy as np

def message_to_bits_with_length(message: str):
    message_bytes = message.encode("utf-8")
    length = len(message_bytes)
    length_bits = [int(b) for b in format(length, "032b")]  # 32-bit header
    message_bits = [int(b) for byte in message_bytes for b in format(byte, "08b")]
    return length_bits + message_bits


def bits_to_message_with_length(bits):
    length_bits = bits[:32]
    message_length = int("".join(map(str, length_bits)), 2)
    message_bits = bits[32:32 + message_length * 8]
    message_bytes = bytearray()
    for i in range(0, len(message_bits), 8):
        byte = int("".join(map(str, message_bits[i:i+8])), 2)
        message_bytes.append(byte)
    return message_bytes.decode("utf-8", errors="ignore")


def encode(image: np.ndarray, message: str) -> np.ndarray:
    img_copy = image.copy().astype(np.uint8)
    flat_img = img_copy.flatten()

    bits = message_to_bits_with_length(message)
    if len(bits) > len(flat_img):
        raise ValueError("Message too long for the selected image!")

    for i, bit in enumerate(bits):
        flat_img[i] = (int(flat_img[i]) & ~1) | bit

    return flat_img.reshape(img_copy.shape).astype(np.uint8)


def decode(image: np.ndarray) -> str:
    flat_img = image.flatten()
    bits = [int(pixel) & 1 for pixel in flat_img]
    return bits_to_message_with_length(bits)
