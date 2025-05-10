from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_openai_response(language, level, subject, topic, question):
    prompt = (
        f"You are a helpful tutor. The student is in {level}, learning in {language}. "
        f"The subject is {subject}, and the topic is {topic}. "
        f"Explain the answer to the following question in a simple way:\n\n{question}"
    )

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a supportive and knowledgeable tutor."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"
