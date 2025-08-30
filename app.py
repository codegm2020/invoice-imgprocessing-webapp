# app.py
import os
import json
from flask import Flask, request, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
from google.cloud import vision
import vertexai
from vertexai.generative_models import GenerativeModel, Part

# --- Configuration ---
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'supersecretkey' # Needed for flash messages

# --- Google Cloud Authentication ---
# Set the environment variable for authentication
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'credentials.json'

# --- Vertex AI Initialization ---
PROJECT_ID = "your-gcp-project-id"  # <--- CHANGE THIS
LOCATION = "us-central1" # Or any other supported region
vertexai.init(project=PROJECT_ID, location=LOCATION)
generative_model = GenerativeModel("gemini-1.0-pro-vision")

# --- Helper Functions ---
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_invoice(image_path):
    """
    Extracts text using Cloud Vision API and then structures it using Vertex AI.
    """
    # 1. OCR with Google Cloud Vision API
    client = vision.ImageAnnotatorClient()
    with open(image_path, 'rb') as image_file:
        content = image_file.read()
    
    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)
    ocr_text = response.full_text_annotation.text

    if not ocr_text:
        return None, "No text found in the image."

    # 2. Structuring with Vertex AI (Gemini)
    prompt = f"""
    Given the following raw text extracted from an invoice, please identify and extract the following fields:
    - Vendor Name
    - Invoice Number
    - Invoice Date
    - Total Amount
    - A list of line items, with description, quantity, and price for each.

    Please return the result as a clean JSON object. Do not include any explanatory text before or after the JSON.

    Raw Text:
    ---
    {ocr_text}
    ---
    """
    
    try:
        # Gemini Vision model can take text and image, but for this workflow,
        # we're just passing the OCR'd text to the standard text model for simplicity and cost.
        # Re-initialize for a text-only model if needed, or use the vision model with just text.
        text_model = GenerativeModel("gemini-1.0-pro")
        response = text_model.generate_content(prompt)
        
        # Clean up the response to get pure JSON
        json_string = response.text.strip().replace('```json', '').replace('```', '').strip()
        extracted_data = json.loads(json_string)
        return extracted_data, None
    except Exception as e:
        print(f"Error during Vertex AI processing: {e}")
        return None, f"Failed to parse AI response. Raw response: {response.text}"


# --- Flask Routes ---
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Process the image
            extracted_data, error = process_invoice(filepath)
            
            if error:
                flash(error)
                return redirect(request.url)

            # Pass data to the results page
            return render_template('results.html', data=extracted_data, filename=filename)

    return render_template('index.html')

if __name__ == '__main__':
    # Ensure the uploads directory exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
