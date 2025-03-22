#!/usr/bin/env python3
"""
Create Sample PDF Documents

This script creates sample PDF documents with different content for testing
the PDF recommendation system.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

# Define output directory
OUTPUT_DIR = "/home/ubuntu/pdf_recommendation_system/pdfs"

# Sample document topics and content
SAMPLE_DOCUMENTS = [
    {
        "filename": "machine_learning_basics.pdf",
        "title": "Introduction to Machine Learning",
        "content": """
        Machine learning is a branch of artificial intelligence (AI) and computer science which focuses on the use of data and algorithms to imitate the way that humans learn, gradually improving its accuracy.
        
        Machine learning is an important component of the growing field of data science. Through the use of statistical methods, algorithms are trained to make classifications or predictions, and to uncover key insights in data mining projects. These insights subsequently drive decision making within applications and businesses, ideally impacting key growth metrics.
        
        The primary aim is to allow the computers to learn automatically without human intervention or assistance and adjust actions accordingly. Machine learning algorithms are typically created using frameworks that accelerate solution development, such as TensorFlow and PyTorch.
        
        Supervised learning, unsupervised learning, and reinforcement learning are the three main categories of machine learning algorithms. Supervised learning uses labeled datasets to train algorithms to classify data or predict outcomes. Unsupervised learning uses unlabeled data to identify patterns and relationships. Reinforcement learning trains algorithms to make decisions based on rewards and punishments.
        """
    },
    {
        "filename": "deep_learning_overview.pdf",
        "title": "Deep Learning: A Comprehensive Overview",
        "content": """
        Deep learning is a subset of machine learning that is inspired by the structure and function of the human brain, specifically the interconnecting of many neurons. Artificial Neural Networks (ANNs) are algorithms that mimic the biological structure of the brain.
        
        In deep learning, each level transforms its input data into a slightly more abstract and composite representation. For instance, in an image recognition application, the raw input may be a matrix of pixels; the first representational layer may abstract the pixels and encode edges; the second layer may compose and encode arrangements of edges; the third layer may encode a nose and eyes; and the fourth layer may recognize that the image contains a face.
        
        Deep learning has produced results comparable to and in some cases surpassing human expert performance. It has been applied to various fields including computer vision, speech recognition, natural language processing, audio recognition, social network filtering, machine translation, bioinformatics, drug design, medical image analysis, and board game programs, where they have produced results comparable to and in some cases surpassing human expert performance.
        
        Convolutional Neural Networks (CNNs) and Recurrent Neural Networks (RNNs) are two popular types of deep learning architectures. CNNs are primarily used for image processing and computer vision tasks, while RNNs are designed for sequential data like time series or natural language.
        """
    },
    {
        "filename": "natural_language_processing.pdf",
        "title": "Natural Language Processing Techniques",
        "content": """
        Natural Language Processing (NLP) is a field of artificial intelligence that gives computers the ability to understand text and spoken words in much the same way human beings can. NLP combines computational linguistics—rule-based modeling of human language—with statistical, machine learning, and deep learning models.
        
        These technologies enable computers to process human language in the form of text or voice data and to 'understand' its full meaning, complete with the speaker or writer's intent and sentiment. NLP drives computer programs that translate text from one language to another, respond to spoken commands, and summarize large volumes of text rapidly—even in real time.
        
        There's a tremendous amount of information stored in free text files, such as patients' medical records. Before deep learning-based NLP models, this information was inaccessible to computer-assisted analysis and could not be analyzed in any systematic way. With NLP, we can analyze this text and extract information such as whether a patient has a certain disease or what medications they are taking.
        
        Modern NLP applications include sentiment analysis, text summarization, named entity recognition, relationship extraction, speech recognition, and machine translation. Transformer models like BERT, GPT, and T5 have revolutionized NLP by enabling more accurate language understanding and generation.
        """
    },
    {
        "filename": "computer_vision_applications.pdf",
        "title": "Applications of Computer Vision",
        "content": """
        Computer vision is a field of artificial intelligence that trains computers to interpret and understand the visual world. Using digital images from cameras and videos and deep learning models, machines can accurately identify and classify objects and then react to what they "see."
        
        Computer vision works in three basic steps: acquiring an image, processing the image, and understanding the image. Image acquisition can be as simple as retrieving a digital image from a database or as complex as capturing video frames from multiple cameras. Image processing involves various operations such as noise reduction, contrast enhancement, and image sharpening to prepare the image for analysis. Image understanding is where machine learning and deep learning algorithms come into play to recognize patterns and objects.
        
        Applications of computer vision include autonomous vehicles, facial recognition, augmented reality, healthcare imaging analysis, manufacturing quality control, and retail analytics. In autonomous vehicles, computer vision helps the car "see" and navigate its surroundings. In healthcare, it assists in diagnosing diseases from medical images. In retail, it enables automated checkout systems and customer behavior analysis.
        
        Recent advances in deep learning, particularly Convolutional Neural Networks (CNNs), have significantly improved the accuracy of computer vision systems. These networks can automatically learn hierarchical features from images, eliminating the need for manual feature engineering.
        """
    },
    {
        "filename": "reinforcement_learning.pdf",
        "title": "Reinforcement Learning: Principles and Applications",
        "content": """
        Reinforcement learning is an area of machine learning concerned with how intelligent agents ought to take actions in an environment in order to maximize the notion of cumulative reward. Reinforcement learning differs from supervised learning in that labeled input/output pairs need not be presented, and sub-optimal actions need not be explicitly corrected.
        
        The environment is typically stated in the form of a Markov decision process (MDP), because many reinforcement learning algorithms for this context utilize dynamic programming techniques. The main difference between the classical dynamic programming methods and reinforcement learning algorithms is that the latter do not assume knowledge of an exact mathematical model of the MDP and they target large MDPs where exact methods become infeasible.
        
        Reinforcement learning has been applied successfully to various problems, including robot control, game playing, and resource management. In game playing, reinforcement learning has achieved remarkable results, such as defeating world champions in chess, Go, and poker. In robotics, it has enabled robots to learn complex tasks like walking, grasping objects, and navigating through environments.
        
        Key concepts in reinforcement learning include the agent, the environment, states, actions, rewards, and policies. The agent is the learner or decision-maker. The environment is everything the agent interacts with. States are situations in which the agent finds itself. Actions are what the agent can do. Rewards are the feedback from the environment. Policies are the strategies that the agent employs to determine the next action based on the current state.
        """
    },
    {
        "filename": "data_science_workflow.pdf",
        "title": "The Data Science Workflow",
        "content": """
        Data science is an interdisciplinary field that uses scientific methods, processes, algorithms and systems to extract knowledge and insights from structured and unstructured data. The data science workflow typically consists of several stages: data collection, data cleaning, exploratory data analysis, feature engineering, model training, model evaluation, and deployment.
        
        Data collection involves gathering data from various sources such as databases, APIs, web scraping, or manual entry. The quality and quantity of data collected significantly impact the performance of the final model. Data cleaning, also known as data preprocessing, involves handling missing values, removing duplicates, correcting errors, and transforming data into a suitable format for analysis.
        
        Exploratory data analysis (EDA) is the process of analyzing and visualizing data to understand its patterns, relationships, and trends. This step helps in formulating hypotheses and identifying important features for model building. Feature engineering involves selecting, transforming, or creating new features to improve model performance. This step requires domain knowledge and creativity.
        
        Model training involves selecting an appropriate algorithm and training it on the prepared data. The choice of algorithm depends on the problem type, data characteristics, and desired outcomes. Model evaluation assesses the performance of the trained model using various metrics such as accuracy, precision, recall, F1-score, or mean squared error. This step often involves cross-validation to ensure the model generalizes well to unseen data.
        
        Deployment is the process of integrating the trained model into a production environment where it can make predictions on new data. This step requires considerations for scalability, reliability, and monitoring. The data science workflow is iterative, with feedback from later stages often leading to refinements in earlier stages.
        """
    },
    {
        "filename": "big_data_technologies.pdf",
        "title": "Big Data Technologies and Frameworks",
        "content": """
        Big data refers to data sets that are too large or complex to be dealt with by traditional data-processing application software. Big data technologies are designed to economically extract value from very large volumes of a wide variety of data by enabling high-velocity capture, discovery, and/or analysis.
        
        Hadoop is one of the most popular frameworks for big data processing. It is an open-source framework that allows for the distributed processing of large data sets across clusters of computers using simple programming models. Hadoop consists of the Hadoop Distributed File System (HDFS) for storage and MapReduce for processing.
        
        Apache Spark is another powerful open-source processing engine built around speed, ease of use, and sophisticated analytics. It was developed to overcome the limitations of Hadoop MapReduce, providing in-memory processing capabilities that significantly speed up iterative algorithms and interactive data analysis.
        
        Other important big data technologies include Apache Kafka for real-time data streaming, Apache Flink for stream and batch processing, Apache Cassandra for distributed NoSQL database management, and Apache HBase for distributed, scalable big data store. These technologies form the backbone of modern big data architectures.
        
        Big data technologies have applications in various domains such as business intelligence, healthcare, finance, telecommunications, and scientific research. In business intelligence, they help in customer analytics, market analysis, and fraud detection. In healthcare, they assist in patient monitoring, disease prediction, and drug discovery. In finance, they enable risk assessment, algorithmic trading, and customer segmentation.
        """
    },
    {
        "filename": "cloud_computing_services.pdf",
        "title": "Cloud Computing Services and Architectures",
        "content": """
        Cloud computing is the delivery of computing services—including servers, storage, databases, networking, software, analytics, and intelligence—over the Internet ("the cloud") to offer faster innovation, flexible resources, and economies of scale. Cloud computing services are typically categorized into three main types: Infrastructure as a Service (IaaS), Platform as a Service (PaaS), and Software as a Service (SaaS).
        
        Infrastructure as a Service (IaaS) provides virtualized computing resources over the internet. IaaS providers, such as AWS, Microsoft Azure, and Google Cloud Platform, offer virtual machines, storage, networks, and operating systems on a pay-as-you-go basis. This model allows businesses to avoid the upfront cost and complexity of buying and managing physical servers and datacenter infrastructure.
        
        Platform as a Service (PaaS) provides a platform allowing customers to develop, run, and manage applications without the complexity of building and maintaining the infrastructure typically associated with developing and launching an app. Examples include AWS Elastic Beanstalk, Microsoft Azure App Services, and Google App Engine.
        
        Software as a Service (SaaS) delivers software applications over the internet, on a subscription basis. With SaaS, cloud providers host and manage the software application and underlying infrastructure, and handle any maintenance, like software upgrades and security patching. Examples include Google Workspace, Microsoft Office 365, and Salesforce.
        
        Cloud architectures can be public, private, or hybrid. Public clouds are owned and operated by third-party cloud service providers. Private clouds are used exclusively by a single business or organization. Hybrid clouds combine public and private clouds, allowing data and applications to be shared between them.
        """
    },
    {
        "filename": "cybersecurity_fundamentals.pdf",
        "title": "Fundamentals of Cybersecurity",
        "content": """
        Cybersecurity is the practice of protecting systems, networks, and programs from digital attacks. These cyberattacks are usually aimed at accessing, changing, or destroying sensitive information; extorting money from users; or interrupting normal business processes. Implementing effective cybersecurity measures is particularly challenging today because there are more devices than people, and attackers are becoming more innovative.
        
        The core principles of cybersecurity are confidentiality, integrity, and availability, often referred to as the CIA triad. Confidentiality ensures that information is not disclosed to unauthorized individuals, entities, or processes. Integrity maintains the accuracy and completeness of data over its entire lifecycle. Availability ensures that information is accessible to authorized users when needed.
        
        Common types of cyber threats include malware, phishing, man-in-the-middle attacks, denial-of-service attacks, SQL injection, and zero-day exploits. Malware is malicious software designed to cause damage to a computer, server, or network. Phishing is the practice of sending fraudulent communications that appear to come from a reputable source. Man-in-the-middle attacks occur when attackers insert themselves into a two-party transaction.
        
        Cybersecurity measures include network security, application security, information security, operational security, and end-user education. Network security protects the network infrastructure from unauthorized access and misuse. Application security involves securing software applications from threats. Information security protects the integrity and privacy of data. Operational security includes the processes and decisions for handling and protecting data assets. End-user education addresses the most unpredictable cyber-security factor: people.
        """
    },
    {
        "filename": "blockchain_technology.pdf",
        "title": "Blockchain Technology and Applications",
        "content": """
        Blockchain is a distributed ledger technology that enables the secure transfer of ownership without the need for a trusted third party. It is essentially a chain of blocks, where each block contains a number of transactions. Each block is linked to the previous one through cryptographic hashes, forming a chain. This structure makes the blockchain resistant to modification of the data.
        
        The key features of blockchain technology include decentralization, transparency, immutability, and security. Decentralization means that the blockchain operates on a peer-to-peer network, with no central authority. Transparency ensures that all transactions are visible to anyone on the network. Immutability means that once data is recorded on the blockchain, it cannot be altered. Security is achieved through cryptographic techniques.
        
        Blockchain technology has various applications beyond cryptocurrencies. In supply chain management, it can track the journey of products from manufacturer to consumer, ensuring authenticity and preventing fraud. In healthcare, it can securely store and share patient records, improving interoperability while maintaining privacy. In voting systems, it can provide a transparent and tamper-proof record of votes.
        
        Different types of blockchains include public, private, and consortium blockchains. Public blockchains, like Bitcoin and Ethereum, are open to anyone and are fully decentralized. Private blockchains are controlled by a single organization and have restricted access. Consortium blockchains are controlled by a group of organizations and offer a balance between the transparency of public blockchains and the control of private ones.
        """
    }
]

def create_pdf(doc_info):
    """Create a PDF document with the given information."""
    filename = os.path.join(OUTPUT_DIR, doc_info["filename"])
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Create custom title style
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.darkblue,
        spaceAfter=12
    )
    
    # Create content elements
    elements = []
    
    # Add title
    elements.append(Paragraph(doc_info["title"], title_style))
    elements.append(Spacer(1, 12))
    
    # Add content paragraphs
    content_style = styles["Normal"]
    paragraphs = [p.strip() for p in doc_info["content"].split('\n\n') if p.strip()]
    
    for paragraph in paragraphs:
        elements.append(Paragraph(paragraph, content_style))
        elements.append(Spacer(1, 10))
    
    # Build the PDF
    doc.build(elements)
    print(f"Created PDF: {filename}")

def main():
    """Create all sample PDF documents."""
    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Create each sample PDF
    for doc_info in SAMPLE_DOCUMENTS:
        create_pdf(doc_info)
    
    print(f"Successfully created {len(SAMPLE_DOCUMENTS)} sample PDF documents in {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
