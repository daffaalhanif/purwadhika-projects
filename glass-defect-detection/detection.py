from ultralytics import YOLO
from collections import Counter
from PIL import Image
import cv2
import numpy as np
import os

# Construct absolute path ke best.pt relatif terhadap lokasi file ini
MODEL_PATH = os.path.join(os.path.dirname(__file__), "best.pt")
# Di-load sekali saat module di-import supaya tidak reload tiap fungsi dipanggil
MODEL = YOLO(MODEL_PATH)

CLASS_NAME = ["defect", "glass"]
# Deteksi di bawah threshold ini diabaikan
CONF_THRESHOLD = 0.3


def detect_defect(image):
    """Menjalankan deteksi defect pada gambar produk kaca.

    Menjalankan inferensi YOLO pada gambar, anotasi setiap objek yang terdeteksi,
    lalu kembalikan gambar teranotasi beserta ringkasan dan status.

    Args:
        image (PIL.Image): gambar input dari Gradio.

    Returns:
        PIL.Image: gambar dengan bounding box dan label teranotasi.
        str: ringkasan jumlah deteksi per class.
        str: HTML status deteksi berwarna merah atau hijau.
    """
    # predict() selalu return list, [0] karena input hanya 1 gambar
    results = MODEL.predict(source=image, save=False, conf=CONF_THRESHOLD)[0]
    # PIL dikonversi ke numpy karena OpenCV butuh numpy array untuk anotasi
    image_np = np.array(image)
    # Salinan untuk anotasi supaya gambar asli tidak termodifikasi
    annotated_img = image_np.copy()

    class_counter = Counter()
    defect_found = False

    for box in results.boxes:
        # Ambil class id untuk mapping ke nama class
        cls_id = int(box.cls)
        label = CLASS_NAME[cls_id]
        # Konversi tensor confidence ke Python float
        conf = float(box.conf)
        # Koordinat piksel pojok kiri atas (x1,y1) dan kanan bawah (x2,y2) bounding box
        x1, y1, x2, y2 = map(int, box.xyxy[0])

        class_counter[label] += 1

        # Flag defect ditemukan untuk menentukan status di akhir
        if label == "defect":
            defect_found = True

        # Hijau untuk glass, merah untuk defect
        color = (0, 255, 0) if label == "glass" else (0, 0, 255)
        # Gambar bounding box di sekitar objek yang terdeteksi
        cv2.rectangle(annotated_img, (x1, y1), (x2, y2), color, 2)
        # Tulis label dan confidence score di atas bounding box
        cv2.putText(annotated_img, f"{label} [{conf:.2f}]", (x1, y1 - 8),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    # Susun ringkasan jumlah deteksi per class
    summary = "\n".join([f"{label}: {count}" for label, count in class_counter.items()])

    # Status merah kalau defect ditemukan, hijau kalau tidak
    if defect_found:
        status_html = (
            "<div style='padding:10px; background-color:#ffe5e5; color:#a30000;"
            "border-left:6px solid #cc0000; font-weight:bold;'>"
            "DEFECT DETECTED! PLEASE INSPECT!</div>"
        )
    else:
        status_html = (
            "<div style='padding:10px; background-color:#e6ffe6; color:#006600;"
            "border-left:6px solid #00cc00; font-weight:bold;'>"
            "NO DEFECT FOUND!</div>"
        )

    # Konversi numpy ke PIL karena Gradio butuh PIL Image sebagai output
    return Image.fromarray(annotated_img), summary or "NO OBJECT DETECTED!", status_html