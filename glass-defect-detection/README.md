# Glass Defect Detection System

A computer vision system that detects defects in glass products using YOLOv12.

## How It Works

```
Image -> YOLOv12 (detect defect and glass) -> Annotated result
```

## Model Performance

| Metric | All | Defect | Glass |
|---|---|---|---|
| Precision | 0.814 | 0.698 | 0.930 |
| Recall | 0.774 | 0.622 | 0.927 |
| mAP50 | 0.809 | 0.643 | 0.974 |
| mAP50-95 | 0.520 | 0.240 | 0.800 |

Training stopped early at epoch 75 out of 100. Best model saved at epoch 65.

## Dataset

[Glass Defect Detection](https://universe.roboflow.com/capjamesg/glass-defect-detection-fvbcu) by Roboflow Universe Projects. Licensed under CC BY 4.0.

| Split | Images |
|---|---|
| Train | 1,210 |
| Val | 345 |
| Test | 173 |

## Tech Stack

- YOLOv12n - glass defect detection
- Gradio - web UI
- OpenCV - image annotation

## Installation

```bash
git clone https://github.com/daffaalhanif/purwadhika-projects.git
cd purwadhika-projects/glass-defect-detection

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
glass-defect-detection/
├── main.py          # Gradio UI
├── detection.py     # YOLO inference and image annotation
├── best.pt          # trained model weights
└── requirements.txt
```
