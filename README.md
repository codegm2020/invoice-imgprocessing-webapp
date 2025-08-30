# AI-Powered Invoice Data Extractor
High-Level Architecture

Frontend (HTML/CSS): A simple web page with a file upload form.

Backend (Flask): A Python server that receives the image, orchestrates the AI calls, and displays the results.

AI Services (Google Cloud):
Cloud Vision API: Performs the initial, powerful OCR to get all raw text from the invoice.
Vertex AI (Gemini Pro): Takes the raw text and uses generative AI to understand the context and extract specific fields into a structured format (JSON).

The Problem Solved:

In many businesses, the accounts payable process involves manually reading data from invoices (e.g., PDFs, scanned images) and entering it into a financial system. This process is:

-Time-Consuming: Manual entry is slow and takes valuable employee time away from more critical tasks.

-Error-Prone: Human error during data entry can lead to incorrect payments and complex accounting reconciliations.

-Inefficient: It creates a significant bottleneck, delaying payments and financial reporting.

This application provides a streamlined, AI-driven solution that automates the extraction process, increasing speed, accuracy, and overall efficiency.


<img width="725" height="325" alt="Screenshot 2025-08-30 at 11 45 11 AM" src="https://github.com/user-attachments/assets/cad2ef10-d950-4ec2-9124-ac4eacafef0b" />

<img width="725" height="325" alt="Screenshot 2025-08-30 at 11 45 20 AM" src="https://github.com/user-attachments/assets/0f7293e6-c177-4889-8c01-18a7489e5a22" />

