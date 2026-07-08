from pydantic import BaseModel, Field


class ResumeAnalyzeRequest(BaseModel):
    resume_text: str = Field(min_length=20)


class ATSCheckRequest(BaseModel):
    resume_text: str = Field(min_length=20)
    job_description: str = Field(min_length=20)


class CoverLetterRequest(BaseModel):
    company: str
    role: str
    tone: str
    resume_text: str


class InterviewQuestionRequest(BaseModel):
    company: str
    mode: str = 'preset'
    round_type: str


class InterviewEvalRequest(BaseModel):
    question: str
    answer: str = Field(min_length=10)


class LinkedInRequest(BaseModel):
    post_type: str
    tone: str
    context: str


class JobCreateRequest(BaseModel):
    company: str
    role: str
    status: str = 'Wishlist'


class JobUpdateRequest(BaseModel):
    status: str


class SkillGapRequest(BaseModel):
    target_role: str
    current_skills: list[str]
