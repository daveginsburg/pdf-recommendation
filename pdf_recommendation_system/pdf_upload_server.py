#!/usr/bin/env python3
"""
Simple Web Server for PDF Upload

This script creates a simple web server with a file upload interface
for uploading PDF documents.
"""

import os
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
import cgi
import socketserver
import urllib.parse
import json

# Configuration
HOST = "0.0.0.0"  # Listen on all interfaces
PORT = 8000
UPLOAD_DIR = "/home/ubuntu/pdf_recommendation_system/pdfs"

# Ensure upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

class PDFUploadHandler(BaseHTTPRequestHandler):
    """HTTP request handler for PDF upload server."""
    
    def _send_response(self, status_code, content_type, content):
        """Send HTTP response with the given status code and content."""
        self.send_response(status_code)
        self.send_header("Content-type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)
    
    def _send_html_response(self, status_code, html_content):
        """Send HTTP response with HTML content."""
        self._send_response(status_code, "text/html", html_content.encode("utf-8"))
    
    def _send_json_response(self, status_code, data):
        """Send HTTP response with JSON content."""
        json_content = json.dumps(data).encode("utf-8")
        self._send_response(status_code, "application/json", json_content)
    
    def _get_uploaded_files(self):
        """Get list of uploaded PDF files."""
        files = []
        for filename in os.listdir(UPLOAD_DIR):
            if filename.lower().endswith('.pdf'):
                file_path = os.path.join(UPLOAD_DIR, filename)
                file_size = os.path.getsize(file_path)
                files.append({
                    "name": filename,
                    "size": file_size,
                    "path": file_path
                })
        return files
    
    def do_GET(self):
        """Handle GET requests."""
        if self.path == "/":
            # Serve the upload form
            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>PDF Upload for Recommendation System</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        max-width: 800px;
                        margin: 0 auto;
                        padding: 20px;
                    }}
                    h1 {{
                        color: #333;
                    }}
                    .upload-form {{
                        background-color: #f5f5f5;
                        padding: 20px;
                        border-radius: 5px;
                        margin-bottom: 20px;
                    }}
                    .file-input {{
                        margin-bottom: 10px;
                    }}
                    .submit-button {{
                        background-color: #4CAF50;
                        color: white;
                        padding: 10px 15px;
                        border: none;
                        border-radius: 4px;
                        cursor: pointer;
                    }}
                    .submit-button:hover {{
                        background-color: #45a049;
                    }}
                    .file-list {{
                        background-color: #f9f9f9;
                        padding: 20px;
                        border-radius: 5px;
                    }}
                    .file-item {{
                        margin-bottom: 5px;
                    }}
                </style>
            </head>
            <body>
                <h1>PDF Upload for Recommendation System</h1>
                <div class="upload-form">
                    <h2>Upload PDF Documents</h2>
                    <form action="/upload" method="post" enctype="multipart/form-data">
                        <div class="file-input">
                            <input type="file" name="file" accept=".pdf" multiple>
                        </div>
                        <input type="submit" value="Upload" class="submit-button">
                    </form>
                </div>
                
                <div class="file-list">
                    <h2>Uploaded Files</h2>
                    <div id="file-list-content">
                        Loading...
                    </div>
                </div>
                
                <script>
                    // Function to fetch and display the list of uploaded files
                    function fetchFileList() {{
                        fetch('/files')
                            .then(response => response.json())
                            .then(data => {{
                                const fileListContent = document.getElementById('file-list-content');
                                if (data.files.length === 0) {{
                                    fileListContent.innerHTML = '<p>No files uploaded yet.</p>';
                                    return;
                                }}
                                
                                let html = '<ul>';
                                data.files.forEach(file => {{
                                    const fileSizeKB = Math.round(file.size / 1024);
                                    html += `<li class="file-item">${{file.name}} (${fileSizeKB} KB)</li>`;
                                }});
                                html += '</ul>';
                                
                                fileListContent.innerHTML = html;
                            }})
                            .catch(error => {{
                                console.error('Error fetching file list:', error);
                                document.getElementById('file-list-content').innerHTML = 
                                    '<p>Error loading file list. Please refresh the page.</p>';
                            }});
                    }}
                    
                    // Fetch file list when page loads
                    document.addEventListener('DOMContentLoaded', fetchFileList);
                </script>
            </body>
            </html>
            """
            self._send_html_response(200, html)
        
        elif self.path == "/files":
            # Return list of uploaded files as JSON
            files = self._get_uploaded_files()
            self._send_json_response(200, {"files": files})
        
        else:
            # Handle 404 Not Found
            self._send_html_response(404, "<h1>404 Not Found</h1>")
    
    def do_POST(self):
        """Handle POST requests."""
        if self.path == "/upload":
            # Handle file upload
            content_type, params = cgi.parse_header(self.headers.get('Content-Type', ''))
            
            if content_type == 'multipart/form-data':
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST'}
                )
                
                # Check if the file field is in the form
                if 'file' in form:
                    uploaded_files = []
                    
                    # Handle multiple files
                    if isinstance(form['file'], list):
                        file_items = form['file']
                    else:
                        file_items = [form['file']]
                    
                    for file_item in file_items:
                        if file_item.filename:
                            # Get file data and save it
                            file_data = file_item.file.read()
                            file_name = os.path.basename(file_item.filename)
                            file_path = os.path.join(UPLOAD_DIR, file_name)
                            
                            with open(file_path, 'wb') as f:
                                f.write(file_data)
                            
                            file_size = os.path.getsize(file_path)
                            uploaded_files.append({
                                "name": file_name,
                                "size": file_size,
                                "path": file_path
                            })
                    
                    # Redirect back to the main page
                    self.send_response(303)  # See Other
                    self.send_header("Location", "/")
                    self.end_headers()
                else:
                    # No file field in the form
                    self._send_html_response(400, "<h1>No file selected</h1>")
            else:
                # Not a multipart/form-data request
                self._send_html_response(400, "<h1>Invalid request</h1>")
        else:
            # Handle 404 Not Found
            self._send_html_response(404, "<h1>404 Not Found</h1>")

def run_server():
    """Run the HTTP server."""
    server = socketserver.ThreadingTCPServer((HOST, PORT), PDFUploadHandler)
    print(f"Server started at http://{HOST}:{PORT}")
    print(f"Upload directory: {UPLOAD_DIR}")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.shutdown()

if __name__ == "__main__":
    run_server()
