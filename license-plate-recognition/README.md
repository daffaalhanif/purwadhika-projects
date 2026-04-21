# License Plate Recognition System

A two-stage computer vision system that detects and reads license plates from images using YOLOv12 and EasyOCR.

## How It Works

```
Image -> YOLOv12 (detect plate location) -> EasyOCR (read plate text) -> Annotated result
```

## Model Performance

| Metric | Score |
|---|---|
| Precision | 0.987 |
| Recall | 0.946 |
| mAP50 | 0.971 |
| mAP50-95 | 0.687 |

Training stopped early at epoch 44 out of 50. Best model saved at epoch 39.

## Dataset

[License Plate Recognition](https://universe.roboflow.com/roboflow-universe-projects/license-plate-recognition-rxg4e) by Roboflow Universe Projects. Licensed under CC BY 4.0.

| Split | Images |
|---|---|
| Train | 7,057 |
| Val | 2,048 |
| Test | 1,020 |

## Tech Stack

- YOLOv12n - license plate detection
- EasyOCR - text recognition
- Gradio - web UI
- OpenCV - image annotation

## Installation

```bash
git clone https://github.com/daffaalhanif/license-plate-recognition.git
cd license-plate-recognition

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

## Usage

1. Run the app:

```bash
python main.py
```

2. Open `http://localhost:7860` in your browser
3. Upload an image and click **DETECT**

## Project Structure

```
license-plate-recognition/
├── main.py          # Gradio UI
├── detection.py     # YOLO inference and image annotation
├── ocr.py           # EasyOCR text recognition
├── best.pt          # trained model weights
└── requirements.txt
```
