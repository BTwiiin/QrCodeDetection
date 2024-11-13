import torch
from ultralytics import YOLO
from helpers import display
from helpers import directories

funsd_image_dir = "data/docs-sm"
output_dir = "data/images_qr"
annotation_dir = "data/images_annotations"
json_dir = "data/images_annotations"
yolo_output_dir = "models/datasets/qr_codes/train/labels"

if __name__ == '__main__':
    # Loading and preprocessing code

    # directories.process_all_subdirectories("data/docs-sm", output_dir, annotation_dir)
    # directories.process_all_annotation_dirs("data/images_annotations", "data/labels")
    # directories.split_files("data/labels", "datasets/train/labels", "datasets/val/labels")
    # directories.split_files("data/images_qr", "datasets/train/images", "datasets/val/images")
    #
    # # Training code
    #
    # print("GPU available", torch.cuda.is_available())
    # print("Number of GPUs:", torch.cuda.device_count())
    # #
    # model = YOLO("yolov5nu.pt")
    # #
    # if torch.cuda.is_available():
    #     results = model.train(data="data.yaml", epochs=15, device=0)
    #     print("Using GPU:", torch.cuda.current_device())
    # else:
    #     results = model.train(data="data.yaml", epochs=7)
    #     print("Using CPU")

    model = YOLO("runs/detect/train9/weights/best.pt")


    # Perform prediction, predict returns list
    results = model.predict("img.png")[0]

    display.predicted_images_info_display(results.boxes)
    display.predicted_image_display("img.png", results.boxes)
