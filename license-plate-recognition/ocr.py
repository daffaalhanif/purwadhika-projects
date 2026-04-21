import easyocr


READER = easyocr.Reader(['en'], gpu=True)


def read_plate(plate_crop):
    """Membaca teks license plate dari crop gambar menggunakan EasyOCR.

    Args:
        plate_crop (np.ndarray): potongan gambar area license plate dari hasil deteksi YOLO.

    Returns:
        str: teks plate dalam huruf kapital. Mengembalikan 'unreadable' jika tidak ada
            teks yang terdeteksi atau semua hasil di bawah threshold confidence.
    """
    # Jalankan OCR pada crop plate, hasilnya list of (bbox, text, confidence)
    results = READER.readtext(plate_crop)

    if not results:
        return "unreadable"

    # Filter teks dengan confidence di bawah 0.3 karena dianggap tidak reliable
    texts = [text for (_, text, conf) in results if conf > 0.3]

    # Uppercase karena teks plate selalu huruf kapital
    return " ".join(texts).upper() if texts else "unreadable"