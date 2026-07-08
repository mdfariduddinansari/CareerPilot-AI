import json
import re

from app.config import settings


class AIProvider:
    def __init__(self):
        if settings.openai_api_key:
            self.provider = 'openai'
        elif settings.gemini_api_key:
            self.provider = 'gemini'
        else:
            self.provider = 'heuristic'

    def analyze_resume(self, text: str) -> dict:
        words = len(text.split())
        has_numbers = bool(re.search(r'\d', text))
        score = min(95, max(40, words // 3 + (10 if has_numbers else 0)))
        return {
            'overall_score': score,
            'ats_score': max(35, score - 5),
            'grammar': min(100, score + 3),
            'formatting': min(100, score - 2),
            'readability': min(100, score + 1),
            'impact': min(100, score - 1),
            'problems': ['Add more quantified achievements'] if not has_numbers else ['Minor formatting consistency issues'],
            'suggestions': ['Use action verbs', 'Tailor summary to role', 'Add metrics in experience bullets'],
            'provider': self.provider,
        }

    def ats_check(self, resume_text: str, job_description: str) -> dict:
        job_keywords = {w.lower() for w in re.findall(r'[A-Za-z][A-Za-z+.#-]{2,}', job_description)}
        resume_keywords = {w.lower() for w in re.findall(r'[A-Za-z][A-Za-z+.#-]{2,}', resume_text)}
        matched = sorted(job_keywords & resume_keywords)
        missing = sorted(job_keywords - resume_keywords)
        pct = int((len(matched) / max(1, len(job_keywords))) * 100)
        return {
            'match_percent': pct,
            'matched_keywords': matched[:20],
            'missing_keywords': missing[:20],
            'top_suggested_keywords': missing[:10],
            'provider': self.provider,
        }

    def generate_cover_letter(self, company: str, role: str, tone: str, resume_text: str) -> str:
        opener = {
            'professional': 'I am excited to apply',
            'friendly': "I'd love to join",
            'startup': 'I thrive in fast-moving teams and would be thrilled to join',
            'corporate': 'I am writing to formally express my interest in',
            'creative': 'Building meaningful products is my craft, and I am eager to contribute to',
        }.get(tone, 'I am excited to apply')
        highlights = ', '.join(resume_text.split()[:15])
        return f"{opener} the {role} role at {company}. My background includes {highlights}. I am confident I can deliver impact quickly and collaborate effectively with your team."

    def interview_questions(self, company: str, round_type: str) -> list[str]:
        return [
            f'Why do you want to join {company}?',
            f'Describe a challenge relevant to a {round_type} round and how you solved it.',
            'What impact did your recent project create?'
        ]

    def evaluate_answer(self, answer: str) -> dict:
        length_factor = min(100, max(30, len(answer.split()) * 4))
        return {
            'confidence': min(100, length_factor - 3),
            'communication': min(100, length_factor),
            'technical_accuracy': min(100, length_factor - 4),
            'problem_solving': min(100, length_factor - 2),
            'leadership': min(100, length_factor - 5),
            'overall': min(100, length_factor - 3),
        }

    def linkedin_variants(self, post_type: str, tone: str, context: str) -> list[str]:
        return [
            f'[{tone}] Excited to share my {post_type} update: {context}',
            f'Quick {post_type} story: {context} #CareerGrowth',
            f'What I learned from this {post_type}: {context}'
        ]

    def skill_gap(self, target_role: str, current_skills: list[str]) -> dict:
        baseline = {'python', 'sql', 'system design', 'react', 'communication', 'dsa', 'docker'}
        current = {x.lower() for x in current_skills}
        missing = baseline - current
        return {
            'critical': sorted(list(missing))[:2],
            'medium': sorted(list(missing))[2:4],
            'low': sorted(list(missing))[4:],
            'already_strong': sorted(list(current & baseline)),
            'roadmap': {
                'week_1': f'Fundamentals for {target_role} + 2 practice tasks',
                'week_2': 'Build one mini project and improve weak areas',
                'week_3': 'Mock interviews + advanced topics',
                'week_4': 'Portfolio polish + applications sprint',
                'resources': ['Official docs', 'LeetCode', 'YouTube deep dives']
            }
        }


ai_provider = AIProvider()
