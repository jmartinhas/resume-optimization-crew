from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from typing_extensions import Annotated


class SkillScore(BaseModel):
    """Represents the score and relevance of a specific skill for a candidate in relation to a job requirement.

    Attributes:
        skill_name (str): Name of the skill being scored.
        required (bool): Indicates whether this skill is required (True) or nice-to-have (False).
        match_level (float): Degree to which the candidate's experience matches the skill requirement (range: 0 to 1).
        years_experience (Optional[float]): Number of years the candidate has experience with this skill.
        context_score (float): Relevance of the skill usage context to the job requirements (range: 0 to 1).

    Methods:
        to_markdown():
            Generates a markdown-formatted string representation of the skill score, including all attributes.
    """
    skill_name: str = Field(description="Name of the skill being scored")
    required: bool = Field(description="Whether this skill is required or nice-to-have")
    match_level: Annotated[float, Field(ge=0, le=1, description="How well the candidate's experience matches (0-1)")]
    years_experience: Optional[float] = Field(description="Years of experience with this skill", default=None)
    context_score: Annotated[float, Field(ge=0, le=1, description="How relevant the skill usage context is to the job requirements", default=0.5)]

    @classmethod
    def to_markdown(cls):
        """Generates a markdown-formatted string representation of the CompanyResearch model.

        Returns:
            str: A markdown string containing the company's recent developments, culture and values,
                 market position, growth trajectory, and interview questions, formatted as sections
                 with bullet points for each item.
        """
        markdown = f"""
        **Skill:** {cls.skill_name}
        **Required:** {'Yes' if cls.required else 'No'}
        **Match Level:** {cls.match_level:.2f}
        **Years Experience:** {cls.years_experience if cls.years_experience is not None else 'N/A'}
        **Context Score:** {cls.context_score:.2f}
        """.strip()
        return markdown

class JobMatchScore(BaseModel):
    """
    Represents the scoring breakdown for how well a candidate matches a job posting.

    Attributes:
        overall_match (float): Overall match percentage (0-100).
        technical_skills_match (float): Technical skills match percentage.
        soft_skills_match (float): Soft skills match percentage.
        experience_match (float): Experience level match percentage.
        education_match (float): Education requirements match percentage.
        industry_match (float): Industry experience match percentage.
        skill_details (List[SkillScore]): Detailed scoring for each skill.
        strengths (List[str]): List of areas where candidate exceeds requirements.
        gaps (List[str]): List of areas needing improvement.
        scoring_factors (Dict[str, float]): Weights used for different scoring components.

    Methods:
        to_markdown():
            Generates a markdown-formatted string representation of the job match score,
            including all scoring components, strengths, gaps, skill details, and scoring factors.
    """
    overall_match: Annotated[float, Field(ge=0, le=100, description="Overall match percentage (0-100)")] = Field(
        description="Overall match percentage (0-100)"
    )
    technical_skills_match: Annotated[float, Field(ge=0, le=100, description="Technical skills match percentage")] = Field(
        description="Technical skills match percentage"
    )
    soft_skills_match: Annotated[float, Field(ge=0, le=100, description="Soft skills match percentage")] = Field(
        description="Soft skills match percentage"
    )
    experience_match: Annotated[float, Field(ge=0, le=100, description="Experience level match percentage")] = Field(
        description="Experience level match percentage"
    )
    education_match: Annotated[float, Field(ge=0, le=100, description="Education requirements match percentage")] = Field(
        description="Education requirements match percentage"
    )
    industry_match: Annotated[float, Field(ge=0, le=100, description="Industry experience match percentage")] = Field(
        description="Industry experience match percentage"
    )
    skill_details: List[SkillScore] = Field(
        description="Detailed scoring for each skill",
        default_factory=list
    )
    strengths: List[str] = Field(
        description="List of areas where candidate exceeds requirements",
        default_factory=list
    )
    gaps: List[str] = Field(
        description="List of areas needing improvement",
        default_factory=list
    )
    scoring_factors: Dict[str, float] = Field(
        description="Weights used for different scoring components",
        default_factory=lambda: {
            "technical_skills": 0.35,
            "soft_skills": 0.20,
            "experience": 0.25,
            "education": 0.10,
            "industry": 0.10
        }
    )
    
    @classmethod
    def to_markdown(cls):
        """Generates a markdown-formatted string representation of the CompanyResearch model.

        Returns:
            str: A markdown string containing the company's recent developments, culture and values,
                 market position, growth trajectory, and interview questions, formatted as sections
                 with bullet points for each item.
        """
        markdown = f"""
        **Job Match Score**
        
        **Overall Match:** {cls.overall_match:.2f}%
        **Technical Skills Match:** {cls.technical_skills_match:.2f}%
        **Soft Skills Match:** {cls.soft_skills_match:.2f}%
        **Experience Match:** {cls.experience_match:.2f}%
        **Education Match:** {cls.education_match:.2f}%
        **Industry Match:** {cls.industry_match:.2f}%
        
        **Strengths:**\n{chr(10).join(f'- {s}' for s in cls.strengths)}
        **Gaps:**\n{chr(10).join(f'- {g}' for g in cls.gaps)}
        
        **Skill Details:**\n{''.join(f'- {s.skill_name}: {s.match_level:.2f} (Exp: {s.years_experience}, Context: {s.context_score:.2f})\n' for s in cls.skill_details)}
        
        **Scoring Factors:**\n{chr(10).join(f'- {k}: {v:.2f}' for k, v in cls.scoring_factors)}
        """.strip()
        return markdown

class JobRequirements(BaseModel):
    """
    Represents the comprehensive set of requirements and details for a job posting.

    Attributes:
        technical_skills (List[str]): List of required technical skills.
        soft_skills (List[str]): List of required soft skills.
        experience_requirements (List[str]): List of experience requirements.
        key_responsibilities (List[str]): List of key job responsibilities.
        education_requirements (List[str]): List of education requirements.
        nice_to_have (List[str]): List of preferred but not required skills.
        job_title (str): Official job title.
        department (Optional[str]): Department or team within the company.
        reporting_structure (Optional[str]): Who this role reports to and any direct reports.
        job_level (Optional[str]): Level of the position (e.g., Entry, Senior, Lead).
        location_requirements (Dict[str, str]): Location details including remote/hybrid options.
        work_schedule (Optional[str]): Expected work hours and schedule flexibility.
        travel_requirements (Optional[str]): Expected travel frequency and scope.
        compensation (Dict[str, str]): Salary range and compensation details if provided.
        benefits (List[str]): List of benefits and perks.
        tools_and_technologies (List[str]): Specific tools, software, or technologies used.
        industry_knowledge (List[str]): Required industry-specific knowledge.
        certifications_required (List[str]): Required certifications or licenses.
        security_clearance (Optional[str]): Required security clearance level if any.
        team_size (Optional[str]): Size of the immediate team.
        key_projects (List[str]): Major projects or initiatives mentioned.
        cross_functional_interactions (List[str]): Teams or departments this role interacts with.
        career_growth (List[str]): Career development and growth opportunities.
        training_provided (List[str]): Training or development programs offered.
        diversity_inclusion (Optional[str]): D&I statements or requirements.
        company_values (List[str]): Company values mentioned in the job posting.
        job_url (str): URL of the job posting.
        posting_date (Optional[str]): When the job was posted.
        application_deadline (Optional[str]): Application deadline if specified.
        special_instructions (List[str]): Any special application instructions or requirements.
        match_score (JobMatchScore): Detailed scoring of how well the candidate matches the job requirements.
        score_explanation (List[str]): Detailed explanation of how scores were calculated.
    """
    technical_skills: List[str] = Field(
        description="List of required technical skills",
        default_factory=list
    )
    soft_skills: List[str] = Field(
        description="List of required soft skills",
        default_factory=list
    )
    experience_requirements: List[str] = Field(
        description="List of experience requirements",
        default_factory=list
    )
    key_responsibilities: List[str] = Field(
        description="List of key job responsibilities",
        default_factory=list
    )
    education_requirements: List[str] = Field(
        description="List of education requirements",
        default_factory=list
    )
    nice_to_have: List[str] = Field(
        description="List of preferred but not required skills",
        default_factory=list
    )
    job_title: str = Field(
        description="Official job title",
        default=""
    )
    department: Optional[str] = Field(
        description="Department or team within the company",
        default=None
    )
    reporting_structure: Optional[str] = Field(
        description="Who this role reports to and any direct reports",
        default=None
    )
    job_level: Optional[str] = Field(
        description="Level of the position (e.g., Entry, Senior, Lead)",
        default=None
    )
    location_requirements: Dict[str, str] = Field(
        description="Location details including remote/hybrid options",
        default_factory=dict
    )
    work_schedule: Optional[str] = Field(
        description="Expected work hours and schedule flexibility",
        default=None
    )
    travel_requirements: Optional[str] = Field(
        description="Expected travel frequency and scope",
        default=None
    )
    compensation: Dict[str, str] = Field(
        description="Salary range and compensation details if provided",
        default_factory=dict
    )
    benefits: List[str] = Field(
        description="List of benefits and perks",
        default_factory=list
    )
    tools_and_technologies: List[str] = Field(
        description="Specific tools, software, or technologies used",
        default_factory=list
    )
    industry_knowledge: List[str] = Field(
        description="Required industry-specific knowledge",
        default_factory=list
    )
    certifications_required: List[str] = Field(
        description="Required certifications or licenses",
        default_factory=list
    )
    security_clearance: Optional[str] = Field(
        description="Required security clearance level if any",
        default=None
    )
    team_size: Optional[str] = Field(
        description="Size of the immediate team",
        default=None
    )
    key_projects: List[str] = Field(
        description="Major projects or initiatives mentioned",
        default_factory=list
    )
    cross_functional_interactions: List[str] = Field(
        description="Teams or departments this role interacts with",
        default_factory=list
    )
    career_growth: List[str] = Field(
        description="Career development and growth opportunities",
        default_factory=list
    )
    training_provided: List[str] = Field(
        description="Training or development programs offered",
        default_factory=list
    )
    diversity_inclusion: Optional[str] = Field(
        description="D&I statements or requirements",
        default=None
    )
    company_values: List[str] = Field(
        description="Company values mentioned in the job posting",
        default_factory=list
    )
    job_url: str = Field(
        description="URL of the job posting",
        default=""
    )
    posting_date: Optional[str] = Field(
        description="When the job was posted",
        default=None
    )
    application_deadline: Optional[str] = Field(
        description="Application deadline if specified",
        default=None
    )
    special_instructions: List[str] = Field(
        description="Any special application instructions or requirements",
        default_factory=list
    )
    match_score: JobMatchScore = Field(
        description="Detailed scoring of how well the candidate matches the job requirements",
        default_factory=JobMatchScore
    )
    score_explanation: List[str] = Field(
        description="Detailed explanation of how scores were calculated",
        default_factory=list
    )

    @classmethod
    def to_markdown(cls):
        """
        Generates a markdown-formatted string representation of the JobRequirements model.

        Returns:
            str: A markdown string containing all job requirements and details, formatted as sections
                 with bullet points for each item.
        """
        markdown = f"""
        **Job Requirements**
        
        **Job Title:** {cls.job_title}
        **Department:** {cls.department or 'N/A'}
        **Job Level:** {cls.job_level or 'N/A'}
        **Reporting Structure:** {cls.reporting_structure or 'N/A'}
        **Location Requirements:** {cls.location_requirements}
        **Work Schedule:** {cls.work_schedule or 'N/A'}
        **Travel Requirements:** {cls.travel_requirements or 'N/A'}
        **Compensation:** {cls.compensation}
        **Benefits:**\n{chr(10).join(f'- {b}' for b in cls.benefits)}
        **Technical Skills:**\n{chr(10).join(f'- {s}' for s in cls.technical_skills)}
        **Soft Skills:**\n{chr(10).join(f'- {s}' for s in cls.soft_skills)}
        **Experience Requirements:**\n{chr(10).join(f'- {e}' for e in cls.experience_requirements)}
        **Key Responsibilities:**\n{chr(10).join(f'- {k}' for k in cls.key_responsibilities)}
        **Education Requirements:**\n{chr(10).join(f'- {e}' for e in cls.education_requirements)}
        **Nice to Have:**\n{chr(10).join(f'- {n}' for n in cls.nice_to_have)}
        **Tools and Technologies:**\n{chr(10).join(f'- {t}' for t in cls.tools_and_technologies)}
        **Industry Knowledge:**\n{chr(10).join(f'- {i}' for i in cls.industry_knowledge)}
        **Certifications Required:**\n{chr(10).join(f'- {c}' for c in cls.certifications_required)}
        **Security Clearance:** {cls.security_clearance or 'N/A'}
        **Team Size:** {cls.team_size or 'N/A'}
        **Key Projects:**\n{chr(10).join(f'- {k}' for k in cls.key_projects)}
        **Cross Functional Interactions:**\n{chr(10).join(f'- {c}' for c in cls.cross_functional_interactions)}
        **Career Growth:**\n{chr(10).join(f'- {c}' for c in cls.career_growth)}
        **Training Provided:**\n{chr(10).join(f'- {t}' for t in cls.training_provided)}
        **Diversity & Inclusion:** {cls.diversity_inclusion or 'N/A'}
        **Company Values:**\n{chr(10).join(f'- {v}' for v in cls.company_values)}
        **Job URL:** {cls.job_url}
        **Posting Date:** {cls.posting_date or 'N/A'}
        **Application Deadline:** {cls.application_deadline or 'N/A'}
        **Special Instructions:**\n{chr(10).join(f'- {s}' for s in cls.special_instructions)}
        
        **Match Score:**\n{cls.match_score}
        **Score Explanation:**\n{chr(10).join(f'- {s}' for s in cls.score_explanation)}
        """.strip()
        return markdown

class ResumeOptimization(BaseModel):
    content_suggestions: List[Dict[str, str]] = Field(
        description="List of content optimization suggestions with 'before' and 'after' examples"
    )
    skills_to_highlight: List[str] = Field(
        description="List of skills that should be emphasized based on job requirements"
    )
    achievements_to_add: List[str] = Field(
        description="List of achievements that should be added or modified"
    )
    keywords_for_ats: List[str] = Field(
        description="List of important keywords for ATS optimization"
    )
    formatting_suggestions: List[str] = Field(
        description="List of formatting improvements"
    )

    @classmethod
    def to_markdown(cls):
        """Generates a markdown-formatted string representation of the CompanyResearch model.

        Returns:
            str: A markdown string containing the company's recent developments, culture and values,
                 market position, growth trajectory, and interview questions, formatted as sections
                 with bullet points for each item.
        """
        markdown = f"""
        **Resume Optimization Suggestions**
        
        **Content Suggestions:**\n{''.join(f"- Before: {s['before']}\n  After: {s['after']}\n" for s in cls.content_suggestions)}
        **Skills to Highlight:**\n{chr(10).join(f'- {s}' for s in cls.skills_to_highlight)}
        **Achievements to Add:**\n{chr(10).join(f'- {a}' for a in cls.achievements_to_add)}
        **Keywords for ATS:**\n{chr(10).join(f'- {k}' for k in cls.keywords_for_ats)}
        **Formatting Suggestions:**\n{chr(10).join(f'- {f}' for f in cls.formatting_suggestions)}
        """.strip()
        return markdown
        

class CompanyResearch(BaseModel):
    """
    Represents research information about a company relevant to job applications and interviews.

    Attributes:
        recent_developments (List[str]): List of recent company news and developments.
        culture_and_values (List[str]): Key points about company culture and values.
        market_position (Dict[str, List[str]]): Information about market position, including competitors and industry standing.
        growth_trajectory (List[str]): Information about company's growth and future plans.
        interview_questions (List[str]): Strategic questions to ask during the interview.

    Methods:
        to_markdown():
            Generates a markdown-formatted string representation of the company research, including all attributes as sections with bullet points.
    """
    recent_developments: List[str] = Field(
        description="List of recent company news and developments"
    )
    culture_and_values: List[str] = Field(
        description="Key points about company culture and values"
    )
    market_position: Dict[str, List[str]] = Field(
        description="Information about market position, including competitors and industry standing"
    )
    growth_trajectory: List[str] = Field(
        description="Information about company's growth and future plans"
    )
    interview_questions: List[str] = Field(
        description="Strategic questions to ask during the interview"
    )

    @classmethod
    def to_markdown(cls):
        """Generates a markdown-formatted string representation of the CompanyResearch model.

        Returns:
            str: A markdown string containing the company's recent developments, culture and values,
                 market position, growth trajectory, and interview questions, formatted as sections
                 with bullet points for each item.
        """
        markdown = f"""
        **Company Research**\n\n
        **Recent Developments:**\n
        {'\n'.join(f'- {item}' for item in cls.recent_developments)}\n\n
        **Culture and Values:**\n
        {'\n'.join(f'- {item}' for item in cls.culture_and_values)}\n\n
        **Market Position:**\n
        {''.join(f'**{key}:**\n' + '\n'.join(f'  - {v}' for v in value) + '\n' for key, value in cls.market_position)}\n
        **Growth Trajectory:**\n
        {'\n'.join(f'- {item}' for item in cls.growth_trajectory)}\n\n
        **Interview Questions:**\n
        {'\n'.join(f'- {item}' for item in cls.interview_questions)}\n\n
        """
        return markdown.strip()

def to_md():  
    import json
    with open('output/company_research.json', 'r') as f:
        data = json.load(f)
    # Use model_validate for Pydantic v2, parse_obj for v1
    try:
        md = CompanyResearch.model_validate(data)
    except AttributeError:
        md = CompanyResearch.parse_obj(data)
    print(md.to_markdown())
    with open('output/resume_optimization.json', 'r') as f:
        data = json.load(f)

     # Use model_validate for Pydantic v2, parse_obj for v1
    try:
        md = ResumeOptimization.model_validate(data)
    except AttributeError:
        md = ResumeOptimization.parse_obj(data)
    print(md.to_markdown())

if __name__ == '__main__':
    to_md()