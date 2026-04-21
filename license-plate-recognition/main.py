import gradio as gr
from detection import detect_plate


# Gradio Blocks dipakai supaya layout bisa dikustomisasi per kolom dan baris
with gr.Blocks() as demo:
    gr.Markdown("# License Plate Recognition System")
    gr.Markdown("Upload an image to detect and read the license plate.")

    with gr.Row():
        with gr.Column():
            # type="pil" agar gambar dikonversi ke PIL Image sebelum masuk ke detect_plate
            input_image = gr.Image(type="pil", label="Upload image")
            predict_button = gr.Button("DETECT!")
        with gr.Column():
            # Menampilkan gambar teranotasi yang dikembalikan detect_plate
            output_image = gr.Image(type="pil", label="Detection result")
            # Teks plate mentah hasil OCR
            output_plate_text = gr.Textbox(label="Plate text", lines=2)
            # Ringkasan jumlah plate dan teks masing-masing
            output_summary = gr.Textbox(label="Summary", lines=3)
            # Render HTML untuk tampilan berwarna berdasarkan status deteksi
            status_box = gr.HTML(label="Status")

    # Hubungkan tombol ke fungsi deteksi dengan input dan output yang sesuai
    predict_button.click(
        fn=detect_plate,
        inputs=input_image,
        outputs=[output_image, output_plate_text, output_summary, status_box]
    )

demo.launch()