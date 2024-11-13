import os
import shutil
from helpers.data_generators import qr_code_gen
from helpers.converters import json_to_yolo


def process_all_subdirectories(main_dir, output_base_dir, annotation_base_dir):
    for root, dirs, _ in os.walk(main_dir):
        for dir_name in dirs:
            image_dir = os.path.join(root, dir_name)
            output_dir = os.path.join(output_base_dir, dir_name)
            annotation_dir = os.path.join(annotation_base_dir, dir_name)

            # Create output and annotation directories if they don't exist
            os.makedirs(output_dir, exist_ok=True)
            os.makedirs(annotation_dir, exist_ok=True)

            # Process images in the current subdirectory
            qr_code_gen.generate_data(image_dir, output_dir, annotation_dir)

    print("All directories processed.")


def process_all_annotation_dirs(main_json_dir, output_base_dir, class_id=0):
    for root, dirs, files in os.walk(main_json_dir):
        # Check if the current directory contains JSON files
        if any(file.endswith(".json") for file in files):
            # Define the output directory path, keeping the subdirectory structure
            relative_path = os.path.relpath(root, main_json_dir)
            output_dir = os.path.join(output_base_dir, relative_path)

            # Create the output directory if it doesn't exist
            os.makedirs(output_dir, exist_ok=True)

            # Call the batch conversion function for the current directory
            json_to_yolo.batch_convert_to_yolo_format(root, output_dir, class_id)

    print("All JSON directories processed.")


def split_files(source_dir, target_dir_90, target_dir_10, split_ratio=0.1):
    # Create the target directories if they don't exist
    os.makedirs(target_dir_90, exist_ok=True)
    os.makedirs(target_dir_10, exist_ok=True)

    # Collect all file paths in their original order
    all_files = []
    for root, _, files in os.walk(source_dir):
        for file in files:
            all_files.append(os.path.join(root, file))

    # Split the files by index without shuffling
    split_index = int(len(all_files) * split_ratio)
    files_10_percent = all_files[:split_index]
    files_90_percent = all_files[split_index:]

    # Move the first 10% of files to target_dir_10
    for file_path in files_10_percent:
        target_path = os.path.join(target_dir_10, os.path.basename(file_path))
        shutil.move(file_path, target_path)
        print(f"Moved {file_path} to {target_path}")

    # Move the remaining 90% of files to target_dir_90
    for file_path in files_90_percent:
        target_path = os.path.join(target_dir_90, os.path.basename(file_path))
        shutil.move(file_path, target_path)
        print(f"Moved {file_path} to {target_path}")

    print("Files have been split between the two directories.")