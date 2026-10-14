
from pathlib import Path
from ultralytics import YOLO

ROOT = Path(__file__).resolve().parent.parent
image_path = ROOT / "images" / "test.jpg"
output_dir = ROOT / "outputs"

if not image_path.exists():
    raise FileNotFoundError(f"Image not found: {image_path}")

# Load the pretrained object-detection model
model = YOLO("yolo11n.pt")

results = model.predict(
    source=str(image_path),
    conf=0.35,
    save=True,
    project=str(output_dir),
    name="yolo_detection",
    exist_ok=True,
)

print("\n--- YOLO Object Detections ---")

for result in results:
    if result.boxes is None or len(result.boxes) == 0:
        print("No objects detected.")
        continue

    for box in result.boxes:
        class_id = int(box.cls[0].item())
        confidence = float(box.conf[0].item())

        # Bounding box: left, top, right, bottom
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        object_name = result.names[class_id]

        print(
            f"Object: {object_name} | "
            f"Confidence: {confidence:.2f} | "
            f"Box: ({x1:.0f}, {y1:.0f}, {x2:.0f}, {y2:.0f})"
        )

print(f"\nAnnotated image: {output_dir / 'yolo_detection' / image_path.name}")
