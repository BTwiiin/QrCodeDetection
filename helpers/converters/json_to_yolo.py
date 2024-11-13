import json
import os
import math


def calculate_aabb(x, y, width, height, angle):
    # Calculate the four corners of the rotated box
    cx, cy = x + width / 2, y + height / 2
    angle_rad = math.radians(angle)

    # Corner offsets relative to the center
    dx, dy = width / 2, height / 2
    corners = [
        (cx + dx * math.cos(angle_rad) - dy * math.sin(angle_rad), cy + dx * math.sin(angle_rad) + dy * math.cos(angle_rad)),
        (cx - dx * math.cos(angle_rad) - dy * math.sin(angle_rad), cy - dx * math.sin(angle_rad) + dy * math.cos(angle_rad)),
        (cx - dx * math.cos(angle_rad) + dy * math.sin(angle_rad), cy - dx * math.sin(angle_rad) - dy * math.cos(angle_rad)),
        (cx + dx * math.cos(angle_rad) + dy * math.sin(angle_rad), cy + dx * math.sin(angle_rad) - dy * math.cos(angle_rad)),
    ]

    # Determine the AABB
    min_x = min(c[0] for c in corners)
    max_x = max(c[0] for c in corners)
    min_y = min(c[1] for c in corners)
    max_y = max(c[1] for c in corners)

    return min_x, min_y, max_x, max_y


def convert_to_yolo_format(json_path, output_dir, class_id=0):
    print(f"Processing {json_path}...")

    with open(json_path) as f:
        data = json.load(f)

    # Get bounding box details and rotation angle from JSON
    file_name = data["file_name"]
    img_width = data["width"]
    img_height = data["height"]
    bbox = data["qr_code"]["position"]
    angle = data["qr_code"].get("rotation_angle", 0)  # Default to 0 if no rotation

    print(f"Image: {file_name}, Width: {img_width}, Height: {img_height}")
    print(f"Bounding Box (absolute): x={bbox['x']}, y={bbox['y']}, width={bbox['width']}, height={bbox['height']}, angle={angle}")

    # Calculate the AABB of the rotated bounding box
    min_x, min_y, max_x, max_y = calculate_aabb(bbox["x"], bbox["y"], bbox["width"], bbox["height"], angle)
    print(f"AABB (absolute): min_x={min_x}, min_y={min_y}, max_x={max_x}, max_y={max_y}")

    # Calculate YOLO format (relative values) for the AABB
    x_center = ((min_x + max_x) / 2) / img_width
    y_center = ((min_y + max_y) / 2) / img_height
    width = (max_x - min_x) / img_width
    height = (max_y - min_y) / img_height
    print(f"YOLO Format: class_id={class_id}, x_center={x_center:.4f}, y_center={y_center:.4f}, width={width:.4f}, height={height:.4f}")

    # Write to YOLO format file
    yolo_file = os.path.join(output_dir, os.path.splitext(file_name)[0] + ".txt")
    with open(yolo_file, "a") as f:
        f.write(f"{class_id} {x_center} {y_center} {width} {height}\n")
    print(f"Converted {json_path} to {yolo_file}\n")


def batch_convert_to_yolo_format(json_dir, output_dir, class_id=0):
    os.makedirs(output_dir, exist_ok=True)
    print(f"Starting batch conversion from JSON annotations in {json_dir} to YOLO format in {output_dir}")

    for json_file in os.listdir(json_dir):
        if json_file.endswith(".json"):
            json_path = os.path.join(json_dir, json_file)
            convert_to_yolo_format(json_path, output_dir, class_id=class_id)

    print("Batch conversion completed.")
