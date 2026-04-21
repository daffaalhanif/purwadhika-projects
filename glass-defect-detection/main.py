import gradio as gr
from detection import detect_defect

with gr.Blocks() as demo:
    gr.Markdown("# Glass Defect Detection System")
    gr.Markdown("Upload an image of a glass product to detect any defects.")

    with gr.Row():
        with gr.Column():
            # type="pil" supaya gambar dikonversi ke PIL Image sebelum masuk ke detect_defect
            input_image = gr.Image(type="pil", label="Upload glass image")
            predict_btn = gr.Button("DETECT!")
        with gr.Column():
            # Menampilkan gambar teranotasi yang dikembalikan detect_defect
            output_image = gr.Image(type="pil", label="Detection result")
            # Ringkasan jumlah deteksi per class
            output_summary = gr.Textbox(label="Summary", lines=4)
            # Render HTML berwarna untuk status deteksi
            status_box = gr.HTML(label="Status")

    # Urutan outputs harus sama dengan urutan return di detect_defect
    predict_btn.click(
        fn=detect_defect,
        inputs=input_image,
        outputs=[output_image, output_summary, status_box]
    )

demo.launch()