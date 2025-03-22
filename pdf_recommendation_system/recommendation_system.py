#!/usr/bin/env python3
"""
PDF Recommendation System

This script integrates all components of the PDF recommendation system
to provide a complete solution for recommending similar PDF documents.
"""

import os
import sys
import argparse
from pdf_extractor import PDFExtractor
from similarity_search import PDFSimilaritySearch

class PDFRecommendationSystem:
    """Main class for the PDF recommendation system."""
    
    def __init__(self, pdf_dir=None, embeddings_file=None):
        """
        Initialize the recommendation system.
        
        Args:
            pdf_dir: Directory containing PDF files (optional)
            embeddings_file: Path to the embeddings pickle file (optional)
        """
        self.base_dir = "/home/ubuntu/pdf_recommendation_system"
        self.pdf_dir = pdf_dir or os.path.join(self.base_dir, "pdfs")
        self.embeddings_file = embeddings_file or os.path.join(self.base_dir, "pdf_embeddings.pkl")
        
        # Initialize components
        self.extractor = PDFExtractor(self.pdf_dir)
        self.search = PDFSimilaritySearch(os.path.basename(self.embeddings_file), os.path.dirname(self.embeddings_file))
        
    def list_documents(self):
        """
        List all available documents.
        
        Returns:
            List of document filenames
        """
        return self.search.print_document_list()
    
    def get_document_details(self, filename):
        """
        Get details of a specific document.
        
        Args:
            filename: Name of the document
            
        Returns:
            Dictionary containing document information
        """
        try:
            return self.search.get_document_info(filename)
        except ValueError as e:
            print(f"Error: {e}")
            return None
    
    def get_recommendations(self, query_document, num_recommendations=5):
        """
        Get recommendations for a query document.
        
        Args:
            query_document: Filename of the query document
            num_recommendations: Number of similar documents to recommend
            
        Returns:
            List of recommended document filenames
        """
        try:
            return self.search.print_recommendations(query_document, num_recommendations)
        except ValueError as e:
            print(f"Error: {e}")
            return []
    
    def interactive_mode(self):
        """Run the recommendation system in interactive mode."""
        print("\n" + "=" * 60)
        print("PDF Recommendation System".center(60))
        print("=" * 60)
        
        while True:
            print("\nOptions:")
            print("1. List all documents")
            print("2. View document details")
            print("3. Get recommendations")
            print("4. Exit")
            
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == "1":
                self.list_documents()
                
            elif choice == "2":
                documents = self.search.documents.keys()
                if not documents:
                    print("No documents available.")
                    continue
                    
                print("\nAvailable documents:")
                for i, doc in enumerate(sorted(documents), 1):
                    print(f"{i}. {doc}")
                    
                try:
                    idx = int(input("\nEnter document number: ").strip()) - 1
                    filename = sorted(documents)[idx]
                    info = self.get_document_details(filename)
                    
                    if info:
                        print("\nDocument Details:")
                        print("-" * 50)
                        print(f"Filename: {info['filename']}")
                        print(f"Title: {info['title']}")
                        print("\nPreview:")
                        print(info['preview'])
                        
                except (ValueError, IndexError):
                    print("Invalid selection. Please try again.")
                
            elif choice == "3":
                documents = self.search.documents.keys()
                if not documents:
                    print("No documents available.")
                    continue
                    
                print("\nAvailable documents:")
                for i, doc in enumerate(sorted(documents), 1):
                    print(f"{i}. {doc}")
                    
                try:
                    idx = int(input("\nEnter document number to get recommendations: ").strip()) - 1
                    filename = sorted(documents)[idx]
                    
                    num_rec = input("\nEnter number of recommendations (default 5): ").strip()
                    num_rec = int(num_rec) if num_rec else 5
                    
                    self.get_recommendations(filename, num_rec)
                    
                except (ValueError, IndexError):
                    print("Invalid selection. Please try again.")
                
            elif choice == "4":
                print("\nExiting PDF Recommendation System. Goodbye!")
                break
                
            else:
                print("Invalid choice. Please try again.")

def main():
    """Run the PDF recommendation system."""
    parser = argparse.ArgumentParser(description="PDF Recommendation System")
    parser.add_argument("--pdf-dir", help="Directory containing PDF files")
    parser.add_argument("--embeddings", help="Path to embeddings file")
    parser.add_argument("--query", help="Query document for recommendations")
    parser.add_argument("--num-rec", type=int, default=5, help="Number of recommendations")
    parser.add_argument("--interactive", action="store_true", help="Run in interactive mode")
    
    args = parser.parse_args()
    
    # Create recommendation system
    system = PDFRecommendationSystem(args.pdf_dir, args.embeddings)
    
    # Run in interactive mode if specified or no query document
    if args.interactive or not args.query:
        system.interactive_mode()
    else:
        # Get recommendations for query document
        system.get_recommendations(args.query, args.num_rec)

if __name__ == "__main__":
    main()
