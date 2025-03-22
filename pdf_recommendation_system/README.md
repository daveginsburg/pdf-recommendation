# PDF Recommendation System

A system that places PDF documents in a vector database and recommends 3-5 similar documents based on internal content when a user selects one.

## Overview

This PDF recommendation system analyzes the content of PDF documents and creates vector embeddings to find similarities between them. When a user selects a document, the system recommends 3-5 other documents with similar content based on cosine similarity.

## Components

1. **PDF Extractor** (`pdf_extractor.py`): Extracts text content from PDF documents using multiple methods (pdftotext, PyPDF2, pdfminer.six) for better reliability.

2. **Vector Embeddings Creator** (`create_embeddings.py`): Creates vector embeddings for document content using TF-IDF vectorization and SVD dimensionality reduction.

3. **Similarity Search** (`similarity_search.py`): Implements cosine similarity search to find documents with similar content.

4. **Recommendation System** (`recommendation_system.py`): Integrates all components into a complete system with both command-line and interactive interfaces.

## Installation

The system requires the following packages:
- poppler-utils (for pdftotext)
- PyPDF2
- pdfminer.six
- scikit-learn

Install them using:

```bash
sudo apt-get install -y poppler-utils
pip3 install PyPDF2 pdfminer.six scikit-learn
```

## Usage

### Command-line Mode

To get recommendations for a specific document:

```bash
python3 recommendation_system.py --query document_name.pdf
```

You can specify the number of recommendations:

```bash
python3 recommendation_system.py --query document_name.pdf --num-rec 3
```

### Interactive Mode

To use the interactive interface:

```bash
python3 recommendation_system.py --interactive
```

The interactive mode allows you to:
- List all available documents
- View document details
- Get recommendations for any document

## Adding Your Own Documents

1. Place your PDF documents in the `pdfs` directory
2. Extract content from the documents:
   ```bash
   python3 pdf_extractor.py pdfs/
   ```
3. Create vector embeddings:
   ```bash
   python3 create_embeddings.py
   ```
4. Use the recommendation system:
   ```bash
   python3 recommendation_system.py --interactive
   ```

## Example Output

When selecting "Deep Learning Overview" as the query document, the system recommends:

1. Applications of Computer Vision (Similarity: 0.8030)
2. Natural Language Processing Techniques (Similarity: 0.6392)
3. Introduction to Machine Learning (Similarity: 0.2520)
4. Reinforcement Learning (Similarity: 0.2450)
5. Data Science Workflow (Similarity: 0.1180)

These recommendations make sense because computer vision and NLP are closely related to deep learning.

## Files

- `pdf_extractor.py`: Extracts text from PDF documents
- `create_sample_pdfs.py`: Creates sample PDF documents for testing
- `create_embeddings.py`: Creates vector embeddings for document content
- `similarity_search.py`: Implements similarity search functionality
- `recommendation_system.py`: Main system integrating all components
- `pdf_embeddings.pkl`: Saved embeddings and document content
- `pdfs/`: Directory containing PDF documents
