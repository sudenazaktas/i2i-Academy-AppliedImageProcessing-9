import cv2
import imutils
import easyocr
import numpy as np

def process_image(image_path):
    # Loads the image, applies preprocessing steps, and saves intermediate steps.
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Image not found! Please check the file path.")
        
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("step_1_grayscale.jpg", gray)
    bfilter = cv2.bilateralFilter(gray, 11, 17, 17) 
    cv2.imwrite("step_2_blur.jpg", bfilter)
    edged = cv2.Canny(bfilter, 100, 200)
    cv2.imwrite("step_3_edges.jpg", edged)
    return img, edged

def get_plate_candidates(img, edged):
    # Finds contours and crops candidate regions based on aspect ratio.
    keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(keypoints)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:30]
    candidates = []
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        aspect_ratio = w / float(h)
        if 2.0 <= aspect_ratio <= 6.0 and w > 60 and h > 15:
            cropped = img[y:y+h, x:x+w]
            candidates.append(cropped)
    return candidates

def main():
    image_path = 'car.jpeg' 
    try:
        print("Processing the image...")
        img, edged = process_image(image_path)
        candidates = get_plate_candidates(img, edged)
        if not candidates:
            print("Error: No candidate shapes found.")
            return
        
        print("Starting OCR analysis...")
        reader = easyocr.Reader(['en'])
        for candidate in candidates:
            candidate_enlarged = cv2.resize(candidate, None, fx=2.5, fy=2.5, interpolation=cv2.INTER_CUBIC)
            candidate_gray = cv2.cvtColor(candidate_enlarged, cv2.COLOR_BGR2GRAY)
            allowed_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 "
            result = reader.readtext(candidate_gray, allowlist=allowed_chars, mag_ratio=2)
            
            if result:
                text = " ".join([res[-2] for res in result])
                clean_text = "".join(e for e in text if e.isalnum())
                if len(clean_text) >= 5:
                    print(f"DETECTED LICENSE PLATE: {text}")
                    cv2.imwrite("step_4_final_plate.jpg", candidate)
                    break 
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()