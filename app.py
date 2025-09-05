import openai
from fastapi import FastAPI
from pydantic import BaseModel

# Connect to inference server
client = openai.OpenAI(
    api_key="sk-ctASgYSMlbN1huB1vNDSig",
    base_url="https://ai-inference-stg.tahaluf.ae"
)

# Categories
CATEGORIES = [
    "complain", "deliver", "delivery", "issue", "lost", "shipment", "shipping",
    "توصيل", "شحنة", "شكوى", "فقد"
]

# Request body model
class EmailRequest(BaseModel):
    subject: str
    content: str

#  Functions (unchanged, using your openai client)
def classify_email(subject, content):
    examples = """
    Examples:

    Subject: I want to file a complaint
    Content: The product was damaged when I received it.
    → complain

    Subject: Package delivery confirmation
    Content: Your package #12345 has been successfully delivered.
    → delivery

    Subject: Shipping update
    Content: The shipping status of your order has changed to "In Transit".
    → shipping

    Subject: طلب توصيل
    Content: أريد توصيل الطرد الخاص بي غدًا.
    → توصيل

    Subject: شحنة جديدة
    Content: هذه شحنة جديدة من الشركة.
    → شحنة
    """

    prompt = f"""
    You are an email classifier.

    Valid categories in English: "complain", "deliver", "delivery", "issue", "lost", "shipment", "shipping"
    Valid categories in Arabic: "توصيل", "شحنة", "شكوى", "فقد"

    Rules:
    - If the email subject or content is in English → return ONLY the category in English.
    - If the email subject or content is in Arabic → return ONLY the category in Arabic.
    - DO NOT return any extra text, explanation, punctuation, or formatting.
    - Respond with ONLY one category from the list.

    {examples}

    Classify the following email into one of the categories:

    Subject: {subject}
    Content: {content}
    """


    resp = client.chat.completions.create(
        model="openai/qwen3-14b",
        messages=[{"role": "user", "content": prompt}]
    )

    return resp.choices[0].message.content.strip()

def translate_email(subject, content):
    # Detect if Arabic exists in subject or content
    is_arabic = any("\u0600" <= ch <= "\u06FF" for ch in subject + content)

    if is_arabic:
        prompt = f"""
        You are a strict translator. 
        Translate this email from Arabic to English.
        Output ONLY the translation in the following plain format:
        subject: <translated subject>
        content: <translated content>
        language: en

        Do NOT include quotes, backticks, the word JSON, or any extra formatting.
        Respond with EXACTLY the format above.

        Arabic email:
        Subject: {subject}
        Content: {content}
        """
    else:
        prompt = f"""
        You are a strict translator. 
        Translate this email from English to Arabic.
        Output ONLY as a valid JSON object in the following format:
        {{ subject: <translated subject>
        content: <translated content>
        language: ar
        }}

        Do NOT include quotes, backticks, the word JSON, or any extra formatting.
        Respond with EXACTLY the format above.

        English email:
        Subject: {subject}
        Content: {content}
        """


    resp = client.chat.completions.create(
        model="openai/gemma3-27b-it-qat",
        messages=[{"role": "user", "content": prompt}]
    )

    return resp.choices[0].message.content.strip()


# FastAPI app with your endpoints
app = FastAPI()

@app.post("/classify")
def classify_endpoint(email: EmailRequest):
    category = classify_email(email.subject, email.content)
    return {"category": category}

@app.post("/translate")
def translate_endpoint(email: EmailRequest):
    translation = translate_email(email.subject, email.content)
    return {"translation": translation}


