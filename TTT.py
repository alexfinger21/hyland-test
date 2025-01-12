import cv2
import numpy as np

def enhance_contrast(image):
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    
    enhanced_img = cv2.merge((cl, a, b))
    return cv2.cvtColor(enhanced_img, cv2.COLOR_LAB2BGR)

def detect_edges(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    edges = cv2.Canny(blurred, 50, 150)
    return edges

def find_document_contour(edges):
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    
    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
        
        if len(approx) == 4:
            return approx
    return None

def apply_perspective_transform(image, contour):
    pts = contour.reshape(4, 2)
    rect = np.zeros((4, 2), dtype="float32")
    
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    
    (tl, tr, br, bl) = rect
    widthA = np.linalg.norm(br - bl)
    widthB = np.linalg.norm(tr - tl)
    maxWidth = max(int(widthA), int(widthB))
    
    heightA = np.linalg.norm(tr - br)
    heightB = np.linalg.norm(tl - bl)
    maxHeight = max(int(heightA), int(heightB))
    
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]
    ], dtype="float32")
    
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    return warped

def process_image(image_path):
    image = cv2.imread(image_path)
    original = image.copy()
    
    edges = detect_edges(image)
    cv2.imwrite("detect_edges.jpg", edges)
    
    contour = find_document_contour(edges)
    contour_image = original.copy()
    cv2.drawContours(contour_image, contour, -1, (0, 255, 0), 2)
    cv2.imwrite("draw_contours.jpg", contour_image)

    if contour is None:
        print("No document found!")
        return
    
    scanned = apply_perspective_transform(original, contour)
    cv2.imwrite("perspective_transform.jpg", scanned)
    
    final = enhance_contrast(scanned)
    
    cv2.imwrite("enhance_contrast.jpg", final)

process_image("raw.jpg")
