#!/usr/bin/env python3
"""
PDF Content Extraction Script

This script provides functions to extract text content from PDF documents
using multiple extraction methods for better reliability.
"""

import os
import re
import subprocess
from typing import List, Dict, Optional, Tuple

# PDF processing libraries
import PyPDF2
from pdfminer.high_level import extract_text as pdfminer_extract_text


class PDFExtractor:
    """Class for extracting text content from PDF documents using multiple methods."""
    
    def __init__(self, pdf_dir: str = None):
        """
        Initialize the PDF extractor.
        
        Args:
            pdf_dir: Directory containing PDF files (optional)
        """
        self.pdf_dir = pdf_dir
        
    def get_pdf_files(self) -> List[str]:
        """
        Get list of PDF files in the specified directory.
        
        Returns:
            List of PDF file paths
        """
        if not self.pdf_dir or not os.path.isdir(self.pdf_dir):
            raise ValueError(f"Invalid PDF directory: {self.pdf_dir}")
            
        pdf_files = []
        for filename in os.listdir(self.pdf_dir):
            if filename.lower().endswith('.pdf'):
                pdf_files.append(os.path.join(self.pdf_dir, filename))
        
        return pdf_files
    
    def extract_with_pdftotext(self, pdf_path: str) -> str:
        """
        Extract text using pdftotext (poppler-utils).
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Extracted text content
        """
        try:
            result = subprocess.run(
                ['pdftotext', pdf_path, '-'],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            print(f"pdftotext extraction failed: {e}")
            return ""
    
    def extract_with_pypdf2(self, pdf_path: str) -> str:
        """
        Extract text using PyPDF2.
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Extracted text content
        """
        try:
            text = ""
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    text += page.extract_text() + "\n"
            return text
        except Exception as e:
            print(f"PyPDF2 extraction failed: {e}")
            return ""
    
    def extract_with_pdfminer(self, pdf_path: str) -> str:
        """
        Extract text using pdfminer.six.
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Extracted text content
        """
        try:
            return pdfminer_extract_text(pdf_path)
        except Exception as e:
            print(f"pdfminer extraction failed: {e}")
            return ""
    
    def extract_text(self, pdf_path: str) -> str:
        """
        Extract text from PDF using multiple methods for better reliability.
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Extracted text content
        """
        # Try different extraction methods in order of preference
        text = self.extract_with_pdftotext(pdf_path)
        
        # If pdftotext failed or returned very little text, try PyPDF2
        if len(text.strip()) < 100:
            text = self.extract_with_pypdf2(pdf_path)
            
        # If PyPDF2 failed or returned very little text, try pdfminer
        if len(text.strip()) < 100:
            text = self.extract_with_pdfminer(pdf_path)
        
        # Clean up the text
        text = self._clean_text(text)
        return text
    
    def _clean_text(self, text: str) -> str:
        """
        Clean extracted text by removing extra whitespace and normalizing.
        
        Args:
            text: Raw extracted text
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
            
        # Replace multiple newlines with a single newline
        text = re.sub(r'\n\s*\n', '\n\n', text)
        
        # Replace multiple spaces with a single space
        text = re.sub(r' +', ' ', text)
        
        # Remove non-printable characters
        text = re.sub(r'[^\x20-\x7E\n]', '', text)
        
        return text.strip()
    
    def process_all_pdfs(self) -> Dict[str, str]:
        """
        Process all PDF files in the directory and extract their content.
        
        Returns:
            Dictionary mapping PDF filenames to their extracted content
        """
        pdf_contents = {}
        pdf_files = self.get_pdf_files()
        
        for pdf_path in pdf_files:
            filename = os.path.basename(pdf_path)
            print(f"Processing {filename}...")
            content = self.extract_text(pdf_path)
            pdf_contents[filename] = content
            
        return pdf_contents


if __name__ == "__main__":
    # Example usage
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python pdf_extractor.py <pdf_directory>")
        sys.exit(1)
        
    pdf_dir = sys.argv[1]
    extractor = PDFExtractor(pdf_dir)
    
    try:
        pdf_contents = extractor.process_all_pdfs()
        print(f"Successfully processed {len(pdf_contents)} PDF files.")
        
        # Print a sample of each extracted text
        for filename, content in pdf_contents.items():
            print(f"\n--- {filename} ---")
            print(content[:200] + "..." if len(content) > 200 else content)
            
    except Exception as e:
        print(f"Error processing PDFs: {e}")
        sys.exit(1)
