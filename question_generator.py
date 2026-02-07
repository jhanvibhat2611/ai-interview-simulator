# question_generator.py

from google import genai
import os


def generate_questions(skills, experience, num_questions=5):
    """
    Generate interview questions using Gemini
    strictly aligned with experience level.
    """

    # -------- API KEY (FETCH AT RUNTIME) --------
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return ["❌ GOOGLE_API_KEY not found. Please set it in environment."]

    client = genai.Client(api_key=api_key)

    # -------- VALIDATION --------
    if not skills:
        return ["Please add at least one skill to generate questions."]

    experience = (experience or "fresher").lower()
    if experience not in ["fresher", "junior", "mid", "senior"]:
        experience = "fresher"

    skill_text = ", ".join(skills)

    experience_rules = {
        "fresher": """
- Ask ONLY basic conceptual and syntax-level questions
- No system design
- No architecture
- No performance optimization
""",
        "junior": """
- Ask implementation and logic-based questions
- Small real-world use cases
- No large-scale system design
""",
        "mid": """
- Ask optimization, internals, and trade-offs
- Include moderate design and scalability
""",
        "senior": """
- Ask system design and architecture questions
- Focus on scalability, performance, and trade-offs
"""
    }

    prompt = f"""
You are a senior technical interviewer.

Generate exactly {num_questions} interview questions.

Candidate profile:
- Experience level: {experience}
- Skills: {skill_text}

STRICT EXPERIENCE RULES:
{experience_rules[experience]}

GLOBAL RULES:
- Questions must strictly match the experience level
- One clear question per line
- No explanations
- No markdown
- No headings
"""

    response = client.models.generate_content(
        model="models/gemini-flash-latest",
        contents=prompt
    )

    if not response or not response.text:
        return ["❌ Failed to generate questions. Please try again."]

    questions = [
        q.strip(" .-0123456789")
        for q in response.text.split("\n")
        if q.strip()
    ]

    return questions[:num_questions]


