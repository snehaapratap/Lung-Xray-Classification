# 🌟 Lung X-Ray Classification with MLOps 🚀

Welcome to the **Lung X-Ray Classification** project! This repository implements a machine learning pipeline to classify chest X-ray images into two categories: **NORMAL** and **PNEUMONIA**. The project is built with a focus on **MLOps** principles, ensuring scalability, reliability, and automation.

---

## 📖 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Pipeline Stages](#pipeline-stages)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)

---

## 🌟 Overview

Chest X-rays are a critical diagnostic tool for detecting lung diseases like pneumonia. This project automates the process of classifying X-ray images using deep learning models, integrated with MLOps tools for seamless deployment and monitoring.

---

## ✨ Features

- **End-to-End Pipeline**: Data ingestion, transformation, model training, evaluation, and deployment.
- **Deep Learning**: EfficientNetV2S architecture for high accuracy.
- **MLOps Integration**: BentoML for model serving and AWS S3 for cloud storage.
- **MongoDB**: Image storage and retrieval using GridFS.
- **Custom Logging**: Detailed logs for debugging and monitoring.


---

## ⚙️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/Lung-Xray-Classification.git
   cd Lung-Xray-Classification

   ```


2. Create a virtual environment and activate it:

  ```bash 
  python -m venv venv
  source venv/bin/activate
  ```

3.Install dependencies:
  ```bash 
  pip install -r requirements.txt

  ```

## 🚀 Usage
Run the pipeline stages sequentially using the main.py script:
``` bash
python main.py
```


## Pipeline Stages:

- Data Ingestion: Fetch images from MongoDB and split them into training and validation sets.
- Data Transformation: Apply preprocessing and augmentation to the images.
- Model Training: Train the EfficientNetV2S model on the transformed data.
- Model Evaluation: Evaluate the model's accuracy on the validation set.
- Model Deployment: Push the trained model to AWS S3 and serve it using BentoML.

---

## 🛠️ Technologies Used
- Python: Core programming language.
- PyTorch: Deep learning framework.
- Torchvision: Image transformations and datasets.
- BentoML: Model serving and deployment.
- MongoDB: Image storage and retrieval.
- AWS S3: Cloud storage for trained models.
- GridFS: MongoDB file storage.
- TQDM: Progress bar for training.
- Joblib: Serialization of Python objects.

---

## 🤝 Contributing
Feel free to open issues or submit pull requests to improve the project.

--- 

📧 Contact
For any questions or feedback, reach out to me at snehapratap248@gmail.com.

🌟 Happy Coding! 🌟
