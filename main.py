from ultralytics import YOLO
from helpers import directories
from helpers import display

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

    # Training code

    # model = YOLO("yolov5nu.pt")
    # results = model.train(data="data.yaml", epochs=7)

    model = YOLO("runs/detect/train5/weights/best.pt")

    # Perform prediction, predict returns list
    results = model.predict("data/img.png")[0]

    display.predicted_images_info_display(results.boxes)
    # display.predicted_image_display("data/img.png", results.boxes)
