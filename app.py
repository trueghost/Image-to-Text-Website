from flask import Flask, render_template, request
import cv2
import easyocr
import numpy as np
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file part"
    
    file = request.files['file']
    
    if file.filename == '':
        return "No selected file"
    
    if file:
        # Save the uploaded image to a temporary file
        image_path = 'uploaded_img.jpg'
        file.save(image_path)
        
        # Read the uploaded image
        img = cv2.imread(image_path)
        
        # Instantiate text detector
        reader = easyocr.Reader(['en'], gpu=False)
        
        # Detect text on the image
        text_results = reader.readtext(img)

        threshold = 0.25
        detected_text_list = []
        
        # Extract text with a score above the threshold
        for t_, t in enumerate(text_results):
            bbox, text, score = t
            if score > threshold:
                detected_text_list.append(text)
        
        # Save the detected text to a text file with a sans-serif font
        output_text_file = "detected_text.txt"
        with open(output_text_file, "w", encoding="utf-8") as file:
            file.write("Detected Text:\n")
            for text in detected_text_list:
                file.write(text + "\n")
        
        return render_template('result.html', detected_text_list=detected_text_list)

if __name__ == '__main__':
    app.run(debug=True)