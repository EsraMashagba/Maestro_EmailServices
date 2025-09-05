
# 📧 Email Classifier & Translator API

This project provides a **FastAPI service** that:
- Classifies emails into predefined categories (English & Arabic).
- Translates emails between English and Arabic.

It uses the **OpenAI inference API** for classification and translation.


## 🚀 Features
- **Classification**: Detects if an email is about complaints, delivery, shipping, etc.
- **Translation**: 
  - Arabic ➝ English
  - English ➝ Arabic
- **Validation**: Uses **Pydantic models** to validate input.
- **FastAPI docs**: Interactive API docs auto-generated at `/docs`.


## ⚙️ Setup & Installation

1. **Clone the repository**
   ```bash
 git clone https://github.com/EsraMashagba/Maestro_EmailServices.git
 cd Maestro_EmailServices
````

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux / Mac
   venv\Scripts\activate      # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install fastapi uvicorn openai pydantic
   ```

4. **Configure environment variables**

   * Replace the hardcoded API key in `app.py`:

     ```python
     client = openai.OpenAI(
         api_key="YOUR_API_KEY",
         base_url="https://ai-inference-stg.tahaluf.ae"
     )
     ```
   * (Recommended) Use environment variables instead:

     ```python
     import os

     client = openai.OpenAI(
         api_key=os.getenv("OPENAI_API_KEY"),
         base_url="https://ai-inference-stg.tahaluf.ae"
     )
     ```

   Then set your key:

   ```bash
   export OPENAI_API_KEY="sk-xxxxx"   # Linux / Mac
   setx OPENAI_API_KEY "sk-xxxxx"     # Windows
   ```

5. **Run the app**

   ```bash
   uvicorn app:app --reload
   ```

6. **Open Swagger UI**

   * Go to: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📬 API Endpoints

### 1. Classify Email

* **POST** `/classify`
* **Request body:**

  ```json
  {
    "subject": "Package delivery confirmation",
    "content": "Your package #12345 has been successfully delivered."
  }
  ```
* **Response:**

  ```json
  {
    "category": "delivery"
  }
  ```

---

### 2. Translate Email

* **POST** `/translate`
* **Request body:**

  ```json
  {
    "subject": "طلب توصيل",
    "content": "أريد توصيل الطرد الخاص بي غدًا."
  }
  ```
* **Response:**

  ```json
  {
    "translation": "subject: Delivery request\ncontent: I want my package delivered tomorrow.\nlanguage: en"
  }


## 🛠️ Technologies Used

* [FastAPI](https://fastapi.tiangolo.com/) – Web framework
* [OpenAI API](https://platform.openai.com/docs/) – Classification & translation
* [Uvicorn](https://www.uvicorn.org/) – ASGI server

---

## 📌 Notes

* This example uses **hardcoded categories** (`complain`, `delivery`, `shipping`, `شكوى`, `شحنة`, etc.).
* The **OpenAI models** used:

  * `openai/qwen3-14b` for classification
  * `openai/gemma3-27b-it-qat` for translation
* You can replace them with other models depending on your use case.

---

## 👩‍💻 Author

Developed by **Esra’a Mashagba**
AI Solutions Specialist
