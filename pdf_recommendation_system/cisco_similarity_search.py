#!/usr/bin/env python3
"""
Similarity Search Function for Cisco PDFs

This script implements a similarity search function for Cisco PDF documents
using vector embeddings to find similar documents based on content.
"""

import os
import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class PDFSimilaritySearch:
    """Class for finding similar PDF documents based on content."""
    
    def __init__(self, embeddings_file="cisco_pdf_embeddings.pkl", output_dir=None):
        """
        Initialize the similarity search.
        
        Args:
            embeddings_file: Path to the embeddings pickle file
            output_dir: Directory containing the embeddings file (optional)
        """
        self.output_dir = output_dir or "/home/ubuntu/pdf-recommendation/pdf_recommendation_system"
        self.embeddings_file = os.path.join(self.output_dir, embeddings_file)
        self.embeddings = {}
        self.documents = {}
        self.vectorizer = None
        self.svd = None
        
        # Load embeddings
        self.load_embeddings()
    
    def load_embeddings(self):
        """
        Load embeddings and documents from the pickle file.
        
        Returns:
            Dictionary containing embeddings and documents
        """
        if not os.path.exists(self.embeddings_file):
            raise FileNotFoundError(f"Embeddings file not found: {self.embeddings_file}")
            
        with open(self.embeddings_file, 'rb') as f:
            data = pickle.load(f)
            
        self.embeddings = data['embeddings']
        self.documents = data['documents']
        self.vectorizer = data['vectorizer']
        self.svd = data['svd']
        
        print(f"Loaded {len(self.embeddings)} document embeddings from {self.embeddings_file}")
        return data
    
    def find_similar_documents(self, query_document, num_recommendations=5):
        """
        Find similar documents to the query document.
        
        Args:
            query_document: Filename of the query document
            num_recommendations: Number of similar documents to recommend
            
        Returns:
            List of tuples (filename, similarity_score) for similar documents
        """
        if query_document not in self.embeddings:
            raise ValueError(f"Query document not found: {query_document}")
            
        # Get the embedding for the query document
        query_embedding = self.embeddings[query_document]
        
        # Calculate similarity scores for all documents
        similarity_scores = {}
        for filename, embedding in self.embeddings.items():
            if filename != query_document:  # Exclude the query document itself
                # Calculate cosine similarity
                similarity = cosine_similarity([query_embedding], [embedding])[0][0]
                similarity_scores[filename] = similarity
        
        # Sort documents by similarity score (descending)
        similar_documents = sorted(
            similarity_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        # Return top N similar documents
        return similar_documents[:num_recommendations]
    
    def get_document_info(self, filename):
        """
        Get information about a document.
        
        Args:
            filename: Name of the document
            
        Returns:
            Dictionary containing document information
        """
        if filename not in self.documents:
            raise ValueError(f"Document not found: {filename}")
            
        # Extract title from the first line of the document
        content = self.documents[filename]
        lines = content.strip().split('\n')
        title = lines[0] if lines else filename
        
        # Get a preview of the content (first 200 characters)
        preview = content[:200] + "..." if len(content) > 200 else content
        
        return {
            "filename": filename,
            "title": title,
            "preview": preview,
            "content": content
        }
    
    def print_document_list(self):
        """
        Print a list of all available documents.
        
        Returns:
            List of document filenames
        """
        print("\nAvailable Cisco Documents:")
        print("-" * 50)
        
        for i, filename in enumerate(sorted(self.documents.keys()), 1):
            info = self.get_document_info(filename)
            print(f"{i}. {info['title']} ({filename})")
            
        return sorted(self.documents.keys())
    
    def print_document_details(self, filename):
        """
        Print details of a specific document.
        
        Args:
            filename: Name of the document
        """
        if filename not in self.documents:
            print(f"Document not found: {filename}")
            return
            
        info = self.get_document_info(filename)
        
        print("\nDocument Details:")
        print("-" * 50)
        print(f"Filename: {info['filename']}")
        print(f"Title: {info['title']}")
        print("\nPreview:")
        print(info['preview'])
    
    def print_recommendations(self, query_document, num_recommendations=5):
        """
        Print recommendations for a query document.
        
        Args:
            query_document: Filename of the query document
            num_recommendations: Number of similar documents to recommend
            
        Returns:
            List of recommended document filenames
        """
        try:
            similar_documents = self.find_similar_documents(
                query_document, 
                num_recommendations
            )
            
            print(f"\nRecommendations for '{query_document}':")
            print("-" * 50)
            
            # Print details of the query document
            query_info = self.get_document_info(query_document)
            print(f"Selected Document: {query_info['title']}")
            print(f"Preview: {query_info['preview']}")
            
            print("\nSimilar Documents:")
            for i, (filename, similarity) in enumerate(similar_documents, 1):
                info = self.get_document_info(filename)
                print(f"{i}. {info['title']} (Similarity: {similarity:.4f})")
                print(f"   Preview: {info['preview']}")
                print()
                
            return [filename for filename, _ in similar_documents]
            
        except ValueError as e:
            print(f"Error: {e}")
            return []

def main():
    """Demonstrate the similarity search functionality for Cisco PDFs."""
    search = PDFSimilaritySearch()
    
    # Print list of available documents
    documents = search.print_document_list()
    
    if not documents:
        print("No documents available for similarity search.")
        return
    
    # Select a document for demonstration
    query_document = documents[0]  # Use the first document as an example
    
    # Print recommendations for the selected document
    search.print_recommendations(query_document)
    
    print("\nSimilarity search demonstration complete!")

if __name__ == "__main__":
    main()
