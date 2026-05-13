from openai import OpenAI

from app.config import settings


SYSTEM_PROMPT = """\
You are a content moderator for a Reddit-like platform called Leddit.
Evaluate the following post and decide whether it should be accepted or denied.
 
Deny a post if it contains:
- Hate speech, slurs, or targeted harassment
- Explicit calls to violence
- Spam or gibberish
- Illegal content
 
Otherwise, accept the post. Controversial opinions and profanity alone are NOT grounds for denial.
 
Respond with EXACTLY one word: ACCEPTED or DENIED
"""

client = OpenAI(
    api_key=settings.deepseek_api_key,
    base_url=settings.deepseek_base_url,
)

def moderate_post(title: str, content: str | None) -> bool:
    """Return True if the post is accepted, False if denied."""
    user_message = f"Title: {title}\n\nContent: {content or '(no content)'}"
 
    try:
        response = client.chat.completions.create(
            model=settings.deepseek_model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
            max_tokens=10,
            temperature=0,
        )
        answer = response.choices[0].message.content.strip().upper()
        print(f"Deepseek raw response: '{answer}'")
        return "ACCEPTED" in answer
    except Exception:
        print("Deepseek API call failed. Defaulting to accepted")
        return True
