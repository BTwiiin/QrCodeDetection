import cv2


def qr_code_detect(path_to_image) -> bool:
    img = cv2.imread(path_to_image)
    detector = cv2.QRCodeDetector()
    value, pts = detector.detect(img)

    if pts is not None:
        # Draw a rectangle around the QR code
        pts = pts[0].astype(int)  # Convert points to integer
        cv2.polylines(img, [pts], isClosed=True, color=(0, 255, 0), thickness=2)

        # Display the result
        cv2.imshow("Detected QR Code", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("QR code not detected")

    return value