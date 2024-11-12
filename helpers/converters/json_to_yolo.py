import json
import os


def convert_to_yolo_format(json_path, output_dir, class_id=0):
    print(f"Processing {json_path}...")

    with open(json_path) as f:
        data = json.load(f)

    # Get bounding box details from JSON
    file_name = data["file_name"]
    img_width = data["width"]
    img_height = data["height"]
    bbox = data["qr_code"]["position"]
    print(f"Image: {file_name}, Width: {img_width}, Height: {img_height}")
    print(f"Bounding Box (absolute): x={bbox['x']}, y={bbox['y']}, width={bbox['width']}, height={bbox['height']}")

    # Calculate YOLO format (relative values)
    x_center = (bbox["x"] + bbox["width"] / 2) / img_width
    y_center = (bbox["y"] + bbox["height"] / 2) / img_height
    width = bbox["width"] / img_width
    height = bbox["height"] / img_height
    print(
        f"YOLO Format: class_id={class_id}, x_center={x_center:.4f}, y_center={y_center:.4f}, width={width:.4f}, height={height:.4f}")

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
            print(1)
            json_path = os.path.join(json_dir, json_file)
            convert_to_yolo_format(json_path, output_dir, class_id=class_id)

    print("Batch conversion completed.")
