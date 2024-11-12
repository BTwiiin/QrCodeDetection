import os
import random
import json
from PIL import Image
import qrcode


def add_qr_code_with_annotation(image_path, output_image_path, annotation_path, qr_data="Sample QR Code Data"):
    try:
        image = Image.open(image_path).convert("RGB")

        # Generate QR code with an alpha channel
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=2)
        qr.add_data(qr_data)
        qr.make(fit=True)
        qr_img = qr.make_image(fill="black", back_color="white").convert("RGBA")  # Ensure QR code has an alpha channel
        print("QR code generated.")

        # Generate a random size for the QR code within a specified range
        qr_size = random.randint(50, 150)  # Adjust the range (e.g., between 50x50 and 150x150)
        qr_img = qr_img.resize((qr_size, qr_size))

        # Get random position for QR code on the document
        max_x = image.width - qr_img.width
        max_y = image.height - qr_img.height
        x = random.randint(0, max_x)
        y = random.randint(0, max_y)

        # Overlay QR code on the image
        image.paste(qr_img, (x, y), qr_img)  # Use qr_img as both source and mask
        image.save(output_image_path)
        print(f"Image saved to {output_image_path}")

        # Annotate image with QR code position and data
        annotate_image(output_image_path, qr_img, image, qr_data, x, y, annotation_path)

    except Exception as e:
        print(f"An error occurred: {e}")


def annotate_image(output_image_path, qr_img, image, qr_data, x, y, annotation_path):
    annotation = {
        "file_name": os.path.basename(output_image_path),
        "width": image.width,
        "height": image.height,
        "qr_code": {
            "position": {
                "x": x,
                "y": y,
                "width": qr_img.width,
                "height": qr_img.height
            },
            "data": qr_data
        }
    }

    # Save annotation as JSON
    with open(annotation_path, "w") as annotation_file:
        json.dump(annotation, annotation_file, indent=4)
    print(f"Annotation saved to {annotation_path}")


def generate_data(image_dir, output_dir, annotation_dir):
    # Process all images in the FUNSD dataset
    for image_filename in os.listdir(image_dir):
        if image_filename.endswith(".png"):  # Assuming FUNSD images are in PNG format
            image_path = os.path.join(image_dir, image_filename)
            output_image_path = os.path.join(output_dir, image_filename)
            annotation_path = os.path.join(annotation_dir, f"{os.path.splitext(image_filename)[0]}.json")

            # Generate a random QR code with unique data for each image
            qr_data = f"QR Code for {image_filename}"
            add_qr_code_with_annotation(image_path, output_image_path, annotation_path, qr_data=qr_data)

    print("QR codes added with annotations saved to:", annotation_dir)
