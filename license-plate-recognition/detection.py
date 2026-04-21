from ultralytics import YOLO
from PIL import Image
from ocr import read_plate
import cv2
import numpy as np
import os

# Construct absolute path ke best.pt relatif terhadap lokasi file ini
MODEL_PATH = os.path.join(os.path.dirname(__file__), "best.pt")
MODEL = YOLO(MODEL_PATH)

# Deteksi di bawah threshold ini diabaikan
CONF_THRESHOLD = 0.5


def detect_plate(image):
    """Menjalankan deteksi license plate pada gambar input.

    Menjalankan inferensi YOLO pada gambar, crop setiap bounding box yang terdeteksi,
    kirim crop ke OCR, lalu kembalikan gambar teranotasi beserta hasil teks dan status.

    Args:
        image (PIL.Image): gambar input dari Gradio.

    Returns:
        PIL.Image: gambar dengan bounding box dan teks OCR teranotasi.
        str: teks plate yang terbaca, satu plate per baris.
        str: ringkasan jumlah plate dan teks masing-masing.
        str: HTML status deteksi berwarna hijau atau merah.
    """
    # PIL dikonversi ke numpy karena OpenCV butuh numpy array untuk crop dan anotasi
    image_np = np.array(image)

    # predict() selalu return list, [0] karena input hanya 1 gambar
    results = MODEL.predict(source=image, save=False, conf=CONF_THRESHOLD)[0]

    # Buat salinan gambar untuk anotasi, supaya gambar asli tidak termodifikasi
    annotated = image_np.copy()

    plate_texts = []
    plate_count = 0

    for box in results.boxes:
        # Konversi tensor confidence ke Python float
        conf = float(box.conf)
        # Koordinat piksel pojok kiri atas (x1, y1) dan kanan bawah (x2, y2) bounding box
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        plate_count += 1

        # Crop numpy array di koordinat bounding box hasil YOLO
        plate_crop = image_np[y1:y2, x1:x2]
        # Kirim crop ke ocr.py untuk baca teks plate
        text = read_plate(plate_crop)
        plate_texts.append(text)

        # Gambar bounding box hijau di sekitar plate yang terdeteksi
        cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 0), 2)
        # Tulis teks OCR dan confidence score di atas bounding box
        cv2.putText(annotated, f"{text} [{conf:.2f}]", (x1, y1 - 8),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Susun teks hasil OCR per plate, satu baris per plate
    plate_text_output = "\n".join(plate_texts) if plate_texts else "No plate text detected"

    # Buat ringkasan jumlah plate dan teks masing-masing untuk output summary
    summary = f"Plates detected: {plate_count}\n" + "\n".join(
        [f"Plate {i+1}: {t}" for i, t in enumerate(plate_texts)]
    )

    # Tampilkan status hijau kalau plate ditemukan, merah kalau tidak
    if plate_count > 0:
        status_html = (
            "<div style='padding:10px; background-color:#e6ffe6; color:#006600;"
            "border-left:6px solid #00cc00; font-weight:bold;'>"
            f"{plate_count} plate(s) detected.</div>"
        )
    else:
        status_html = (
            "<div style='padding:10px; background-color:#ffe5e5; color:#a30000;"
            "border-left:6px solid #cc0000; font-weight:bold;'>"
            "No license plate detected.</div>"
        )

    # Konversi kembali numpy array ke PIL karena Gradio butuh PIL Image sebagai output
    return Image.fromarray(annotated), plate_text_output, summary, status_html