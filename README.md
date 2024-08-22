# NLP-TO-SQL

## Introduction

* NLP-to-SQL is a technique that converts natural language(Text) queries into SQL queries, enabling databases to execute them with the assistance of large language models (LLMs). Although large language models (LLMs) can understand and    transform natural language, generating accurate SQL queries tailored to a specific schema can be challenging.

* To address this challenge, we utilize a domain-specific LLM to achieve more accurate results. Specifically, we employ ```SQLcoder-8B```, which is fine-tuned on top of ```Llama-3``` for the text-to-SQL task.


## UI
![image](https://github.com/user-attachments/assets/198c884d-399d-4de8-8c31-8325d5eb1f8f)

## Chatbot Solution Architecture
![image](https://github.com/user-attachments/assets/8626c8c2-9691-4b8c-822d-a1c9e11ea13d)

## Steps:
1. **Run the Jupyter Notebook:**
   - Open the `.ipynb` file in Kaggle and run it with GPU enabled. This notebook will generate an API.

2. **Update the `.env` File:**
   - Replace the existing API key in the `.env` file with the one generated from the notebook.

3. **Install Required Dependencies:**
   - Install the necessary dependencies by running:
     ```bash
     pip install -r requirements.txt
     ```

4. **Run the Application:**
   - Start the application using the following command:
     ```bash
     streamlit run main.py
     ```
## SQLCoder-8b Benchmark 
![Image](https://cdn-uploads.huggingface.co/production/uploads/603bbad3fd770a9997b57cb6/h52Z_OKYBaDDQMFZyU5pF.png)

## Limitations
1. Deploying this app requires a high-performance GPU to support SQLcoder and the Llama 3.1 LLM.
2. The app currently only supports text-based responses.
3. The inference speed is somewhat slow.
4. As of now, we only support publicly available databases, specifically ```.sql``` files.
