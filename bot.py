def scan(path):
    img = cv2.imread(path)

    detector = cv2.QRCodeDetector()
    data, _, _ = detector.detectAndDecode(img)

    print("DEBUG QR:", data)

    return [data] if data else []
