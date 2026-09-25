import cv2
import os

IMAGE_W = 800
IMAGE_H = 600

image_id = "000997"

image_path = f"data/week1_1000/images/{image_id}.png"
label_path = f"data/week1_1000/labels_yolo/{image_id}.txt"

image = cv2.imread(image_path)

with open(label_path, "r") as f:
    lines = f.readlines()

for line in lines:
    parts = line.strip().split()

    if len(parts) != 5:
        continue

    class_id, x_center, y_center, width, height = map(float, parts)

    x_center *= IMAGE_W
    y_center *= IMAGE_H
    width *= IMAGE_W
    height *= IMAGE_H

    x1 = int(x_center - width / 2)
    y1 = int(y_center - height / 2)
    x2 = int(x_center + width / 2)
    y2 = int(y_center + height / 2)

    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv2.putText(
        image,
        "vehicle",
        (x1, max(y1 - 5, 0)),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (0, 255, 0),
        2
    )

output_path = "data/week1_1000/check_000500.png"
cv2.imwrite(output_path, image)

print("Saved:", output_path)
print("Number of labels:", len(lines))
