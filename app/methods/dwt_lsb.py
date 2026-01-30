import numpy as np
import cv2

def message_to_bits_with_length(message: str):
    message_bytes = message.encode("utf-8")
    length = len(message_bytes)
    length_bits = [int(b) for b in format(length, "032b")]
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
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    low = cv2.pyrDown(gray)
    flat_low = low.flatten().astype(np.uint8)
    bits = message_to_bits_with_length(message)

    if len(bits) > len(flat_low):
        raise ValueError("Message too large for this image!")

    for i, bit in enumerate(bits):
        flat_low[i] = (int(flat_low[i]) & ~1) | bit

    low_mod = flat_low.reshape(low.shape)
    upscaled = cv2.pyrUp(low_mod)
    upscaled = cv2.resize(upscaled, (image.shape[1], image.shape[0]))
    encoded = cv2.merge([upscaled, upscaled, upscaled])
    return cv2.addWeighted(image, 0.6, encoded, 0.4, 0).astype(np.uint8)


def decode(image: np.ndarray) -> str:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    low = cv2.pyrDown(gray)
    bits = [int(pixel) & 1 for pixel in low.flatten()]
    return bits_to_message_with_length(bits)
