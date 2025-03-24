#!/usr/bin/env python3
"""
Vector Embeddings Creator for Cisco PDFs

This script creates vector embeddings for Cisco PDF document content using scikit-learn's
TF-IDF vectorizer and dimensionality reduction techniques.
"""

import os
import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import normalize

class PDFVectorizer:
    """Class for creating vector embeddings from PDF document content."""
    
    def __init__(self, pdf_dir=None, output_dir=None):
        """
        Initialize the PDF vectorizer.
        
        Args:
            pdf_dir: Directory containing PDF files (optional)
            output_dir: Directory to save embeddings (optional)
        """
        self.pdf_dir = pdf_dir or "/home/ubuntu/pdf-recommendation/pdf_recommendation_system/cisco_pdfs"
        self.output_dir = output_dir or "/home/ubuntu/pdf-recommendation/pdf_recommendation_system"
        self.documents = {}
        self.vectorizer = None
        self.svd = None
        self.embeddings = {}
        
    def load_document_content(self):
        """
        Load extracted content from PDF files.
        
        Returns:
            Dictionary mapping filenames to their content
        """
        documents = {}
        
        # Process each PDF file in the directory
        for filename in os.listdir(self.pdf_dir):
            if filename.lower().endswith('.pdf'):
                pdf_path = os.path.join(self.pdf_dir, filename)
                
                # Use the PDF extractor to get content
                from pdf_extractor import PDFExtractor
                extractor = PDFExtractor()
                content = extractor.extract_text(pdf_path)
                
                if content:
                    documents[filename] = content
                    print(f"Loaded content from {filename}")
                else:
                    print(f"Warning: No content extracted from {filename}")
        
        self.documents = documents
        return documents
    
    def create_embeddings(self, n_components=100):
        """
        Create vector embeddings for document content using TF-IDF and SVD.
        
        Args:
            n_components: Number of components for dimensionality reduction
            
        Returns:
            Dictionary mapping filenames to their vector embeddings
        """
        if not self.documents:
            print("No documents loaded. Loading document content...")
            self.load_document_content()
            
        if not self.documents:
            raise ValueError("No document content available for creating embeddings")
            
        # Extract document content and filenames
        filenames = list(self.documents.keys())
        contents = [self.documents[filename] for filename in filenames]
        
        # Create TF-IDF vectorizer
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=2,
            max_df=0.85
        )
        
        # Create TF-IDF matrix
        tfidf_matrix = self.vectorizer.fit_transform(contents)
        
        # Create SVD for dimensionality reduction
        n_components = min(n_components, min(tfidf_matrix.shape) - 1)
        self.svd = TruncatedSVD(n_components=n_components)
        
        # Apply SVD to reduce dimensions
        reduced_matrix = self.svd.fit_transform(tfidf_matrix)
        
        # Normalize the vectors
        normalized_embeddings = normalize(reduced_matrix)
        
        # Map filenames to embeddings
        self.embeddings = {filenames[i]: normalized_embeddings[i] for i in range(len(filenames))}
        
        print(f"Created {len(self.embeddings)} document embeddings with {n_components} dimensions")
        return self.embeddings
    
    def save_embeddings(self, filename="cisco_pdf_embeddings.pkl"):
        """
        Save embeddings and documents to a pickle file.
        
        Args:
            filename: Name of the pickle file
            
        Returns:
            Path to the saved file
        """
        if not self.embeddings:
            raise ValueError("No embeddings available to save")
            
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Save embeddings, documents, and vectorizer to pickle file
        output_path = os.path.join(self.output_dir, filename)
        with open(output_path, 'wb') as f:
            pickle.dump({
                'embeddings': self.embeddings,
                'documents': self.documents,
                'vectorizer': self.vectorizer,
                'svd': self.svd
            }, f)
            
        print(f"Saved embeddings and documents to {output_path}")
        return output_path
    
    def load_embeddings(self, filename="cisco_pdf_embeddings.pkl"):
        """
        Load embeddings and documents from a pickle file.
        
        Args:
            filename: Name of the pickle file
            
        Returns:
            Dictionary containing embeddings and documents
        """
        input_path = os.path.join(self.output_dir, filename)
        
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Embeddings file not found: {input_path}")
            
        with open(input_path, 'rb') as f:
            data = pickle.load(f)
            
        self.embeddings = data['embeddings']
        self.documents = data['documents']
        self.vectorizer = data['vectorizer']
        self.svd = data['svd']
        
        print(f"Loaded {len(self.embeddings)} document embeddings from {input_path}")
        return data

def main():
    """Create vector embeddings for Cisco PDF documents."""
    vectorizer = PDFVectorizer()
    
    # Load document content
    print("Loading document content...")
    vectorizer.load_document_content()
    
    # Create embeddings
    print("\nCreating vector embeddings...")
    vectorizer.create_embeddings()
    
    # Save embeddings
    print("\nSaving embeddings...")
    vectorizer.save_embeddings()
    
    print("\nVector embeddings creation complete!")

if __name__ == "__main__":
    main()
