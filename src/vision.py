
import cv2
import numpy as np


def detect_obstacles(image):
    """
    Demonstration detector for red regions in an image.
    Returns an annotated image and the number of detected regions.

    This is a color-based demo, not a general-purpose obstacle detector.
    """
    if image is None:
        raise ValueError("Input image is empty or could not be loaded.")

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Red wraps around the HSV hue range, so use two masks.
    lower_red_1 = np.array([0, 100, 80])
    upper_red_1 = np.array([10, 255, 255])
    lower_red_2 = np.array([170, 100, 80])
    upper_red_2 = np.array([179, 255, 255])

    mask_1 = cv2.inRange(hsv, lower_red_1, upper_red_1)
    mask_2 = cv2.inRange(hsv, lower_red_2, upper_red_2)
    mask = cv2.bitwise_or(mask_1, mask_2)

    contours, _ = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    annotated = image.copy()
    detected = 0

    for contour in contours:
        if cv2.contourArea(contour) < 500:
            continue

        x, y, width, height = cv2.boundingRect(contour)
        cv2.rectangle(
            annotated, (x, y), (x + width, y + height), (0, 255, 0), 2
        )
        cv2.putText(
            annotated, "Red region", (x, max(20, y - 8)),
            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2
        )
        detected += 1

    return annotated, detected


def main():
    image = np.zeros((400, 600, 3), dtype=np.uint8)
    image[:] = (235, 235, 235)  # Light gray background in BGR.
    cv2.rectangle(image, (150, 100), (300, 250), (0, 0, 255), -1)

    annotated, count = detect_obstacles(image)

    output_path = "outputs/vision_demo.png"
    if not cv2.imwrite(output_path, annotated):
        raise RuntimeError(f"Could not save image to {output_path}")

    print(f"Detected red regions: {count}")
    print(f"Annotated image saved to {output_path}")

    cv2.imshow("OpenCV Red-Region Detection", annotated)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
