from helpers.data_generators import qr_code_gen
from helpers.converters import json_to_yolo
import torch

funsd_image_dir = "data/images"
output_dir = "models/datasets/qr_codes/train/images"
annotation_dir = "data/images_annotations"
json_dir = "data/images_annotations"
yolo_output_dir = "models/datasets/qr_codes/train/labels"

if __name__ == '__main__':
    #qr_code_gen.generate_data(funsd_image_dir, output_dir, annotation_dir)
    #qr_code_gen.generate_data("data/images_val", "models/datasets/qr_codes/val/images",
                              #"data/images_annotations_val")
    #json_to_yolo.batch_convert_to_yolo_format(json_dir, yolo_output_dir)
    #json_to_yolo.batch_convert_to_yolo_format("data/images_annotations_val",
                                              #"models/datasets/qr_codes/val/labels")
    model = torch.hub.load('ultralytics/yolov5', 'custom', path='models/yolov5/runs/train/exp8/weights/best.pt', force_reload=True)

    # Run inference
    results = model('data/test/00040534.png')

    # Display results
    results.show()  # Show the images with bounding boxes
    results.save(save_dir='data/test_results')  # Save results

    # Get the predictions as a pandas DataFrame
    df = results.pandas().xyxy[0]  # Bounding box coordinates and class info
    print(df)

