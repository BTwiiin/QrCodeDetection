import cv2


def predicted_image_display(path_img, boxes):
    img = cv2.imread(path_img)

    for box in boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])  # Convert coordinates to integers
        confidence = box.conf[0]
        class_id = int(box.cls[0])

        # Draw the rectangle and add the label
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        label = f"Class {class_id} ({confidence:.2f})"
        cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display the image
    cv2.imshow("Detected Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def predicted_images_info_display(boxes):
    for box in boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box coordinates
        class_id = int(box.cls[0])  # Predicted class ID
        probability = box.conf[0]  # Confidence score (probability)

        print(f"Class ID: {class_id}, Probability: {probability:.2f}, Box: ({x1}, {y1}), ({x2}, {y2})")