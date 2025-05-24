import json
from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from typing_extensions import Annotated


class SkillScore(BaseModel):
    skill_name: str = Field(description="Name of the skill being scored")
    required: bool = Field(description="Whether this skill is required or nice-to-have")
    match_level: Annotated[float, Field(ge=0, le=1, description="How well the candidate's experience matches (0-1)")]
    years_experience: Optional[float] = Field(description="Years of experience with this skill", default=None)
    context_score: Annotated[float, Field(ge=0, le=1, description="How relevant the skill usage context is to the job requirements", default=0.5)]
    def to_markdown(self):
        """
        Generates a markdown string representation of the SkillScore model.
        Uses the model's attributes and documentation.
        """
        markdown = f"""
        **Skill:** {self.skill_name}
        **Required:** {'Yes' if self.required else 'No'}
        **Match Level:** {self.match_level:.2f}
        **Years Experience:** {self.years_experience if self.years_experience is not None else 'N/A'}
        **Context Score:** {self.context_score:.2f}
        """.strip()
        return markdown

class JobMatchScore(BaseModel):
    overall_match: Annotated[float, Field(ge=0, le=100, description="Overall match percentage (0-100)")]
    technical_skills_match: Annotated[float, Field(ge=0, le=100, description="Technical skills match percentage")]
    soft_skills_match: Annotated[float, Field(ge=0, le=100, description="Soft skills match percentage")]
    experience_match: Annotated[float, Field(ge=0, le=100, description="Experience level match percentage")]
    education_match: Annotated[float, Field(ge=0, le=100, description="Education requirements match percentage")]
    industry_match: Annotated[float, Field(ge=0, le=100, description="Industry experience match percentage")]
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

    def to_markdown(self):
        """
        Generates a markdown string representation of the CompanyResearch model.
        Uses the model's attributes and documentation.
        """
        markdown = f"""
        **Job Match Score**
        
        **Overall Match:** {self.overall_match:.2f}%
        **Technical Skills Match:** {self.technical_skills_match:.2f}%
        **Soft Skills Match:** {self.soft_skills_match:.2f}%
        **Experience Match:** {self.experience_match:.2f}%
        **Education Match:** {self.education_match:.2f}%
        **Industry Match:** {self.industry_match:.2f}%
        
        **Strengths:**\n{chr(10).join(f'- {s}' for s in self.strengths)}
        **Gaps:**\n{chr(10).join(f'- {g}' for g in self.gaps)}
        
        **Skill Details:**\n{''.join(f'- {s.skill_name}: {s.match_level:.2f} (Exp: {s.years_experience}, Context: {s.context_score:.2f})\n' for s in self.skill_details)}
        
        **Scoring Factors:**\n{chr(10).join(f'- {k}: {v:.2f}' for k, v in self.scoring_factors)}
        """.strip()
        return markdown

class JobRequirements(BaseModel):
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

    def to_markdown(self):
        """
        Generates a markdown string representation of the CompanyResearch model.
        Uses the model's attributes and documentation.
        """
        markdown = f"""
        **Job Requirements**
        
        **Job Title:** {self.job_title}
        **Department:** {self.department or 'N/A'}
        **Job Level:** {self.job_level or 'N/A'}
        **Reporting Structure:** {self.reporting_structure or 'N/A'}
        **Location Requirements:** {self.location_requirements}
        **Work Schedule:** {self.work_schedule or 'N/A'}
        **Travel Requirements:** {self.travel_requirements or 'N/A'}
        **Compensation:** {self.compensation}
        **Benefits:**\n{chr(10).join(f'- {b}' for b in self.benefits)}
        **Technical Skills:**\n{chr(10).join(f'- {s}' for s in self.technical_skills)}
        **Soft Skills:**\n{chr(10).join(f'- {s}' for s in self.soft_skills)}
        **Experience Requirements:**\n{chr(10).join(f'- {e}' for e in self.experience_requirements)}
        **Key Responsibilities:**\n{chr(10).join(f'- {k}' for k in self.key_responsibilities)}
        **Education Requirements:**\n{chr(10).join(f'- {e}' for e in self.education_requirements)}
        **Nice to Have:**\n{chr(10).join(f'- {n}' for n in self.nice_to_have)}
        **Tools and Technologies:**\n{chr(10).join(f'- {t}' for t in self.tools_and_technologies)}
        **Industry Knowledge:**\n{chr(10).join(f'- {i}' for i in self.industry_knowledge)}
        **Certifications Required:**\n{chr(10).join(f'- {c}' for c in self.certifications_required)}
        **Security Clearance:** {self.security_clearance or 'N/A'}
        **Team Size:** {self.team_size or 'N/A'}
        **Key Projects:**\n{chr(10).join(f'- {k}' for k in self.key_projects)}
        **Cross Functional Interactions:**\n{chr(10).join(f'- {c}' for c in self.cross_functional_interactions)}
        **Career Growth:**\n{chr(10).join(f'- {c}' for c in self.career_growth)}
        **Training Provided:**\n{chr(10).join(f'- {t}' for t in self.training_provided)}
        **Diversity & Inclusion:** {self.diversity_inclusion or 'N/A'}
        **Company Values:**\n{chr(10).join(f'- {v}' for v in self.company_values)}
        **Job URL:** {self.job_url}
        **Posting Date:** {self.posting_date or 'N/A'}
        **Application Deadline:** {self.application_deadline or 'N/A'}
        **Special Instructions:**\n{chr(10).join(f'- {s}' for s in self.special_instructions)}
        
        **Match Score:**\n{self.match_score}
        **Score Explanation:**\n{chr(10).join(f'- {s}' for s in self.score_explanation)}
        """.strip()
        return markdown
    
    @classmethod
    def json_to_md(cls, file_path='output/job_analysis.json'):
        with open(file_path, 'r') as f:
            data = json.load(f)
        # Use model_validate for Pydantic v2, parse_obj for v1
        try:
            md = JobRequirements.model_validate(data)
        except AttributeError:
            md = JobRequirements.parse_obj(data)
        return md.to_markdown()

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

    def to_markdown(self):
        """
        Generates a markdown string representation of the CompanyResearch model.
        Uses the model's attributes and documentation.
        """
        markdown = f"""
        **Resume Optimization Suggestions**
        
        **Content Suggestions:**\n{''.join(f"- Before: {s['before']}\n  After: {s['after']}\n" for s in self.content_suggestions)}
        **Skills to Highlight:**\n{chr(10).join(f'- {s}' for s in self.skills_to_highlight)}
        **Achievements to Add:**\n{chr(10).join(f'- {a}' for a in self.achievements_to_add)}
        **Keywords for ATS:**\n{chr(10).join(f'- {k}' for k in self.keywords_for_ats)}
        **Formatting Suggestions:**\n{chr(10).join(f'- {f}' for f in self.formatting_suggestions)}
        """.strip()
        return markdown

    @classmethod
    def json_to_md(cls, file_path='output/resume_optimization.json'):
        with open(file_path, 'r') as f:
            data = json.load(f)
        # Use model_validate for Pydantic v2, parse_obj for v1
        try:
            md = ResumeOptimization.model_validate(data)
        except AttributeError:
            md = ResumeOptimization.parse_obj(data)
        return md.to_markdown()


class CompanyResearch(BaseModel):
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

    def to_markdown(self):
        """
        Generates a markdown string representation of the CompanyResearch model.
        Uses the model's attributes and documentation.
        """
        markdown = f"""
        **Company Research**\n\n
        **Recent Developments:**\n
        {'\n'.join(f'- {item}' for item in self.recent_developments)}\n\n
        **Culture and Values:**\n
        {'\n'.join(f'- {item}' for item in self.culture_and_values)}\n\n
        **Market Position:**\n
        {''.join(f'**{key}:**\n' + '\n'.join(f'  - {v}' for v in value) + '\n' for key, value in self.market_position.items())}\n
        **Growth Trajectory:**\n
        {'\n'.join(f'- {item}' for item in self.growth_trajectory)}\n\n
        **Interview Questions:**\n
        {'\n'.join(f'- {item}' for item in self.interview_questions)}\n\n
        """.strip()
        return markdown
    
    @classmethod
    def json_to_md(cls, file_path='output/company_research.json'):
        with open(file_path, 'r') as f:
            data = json.load(f)
        # Use model_validate for Pydantic v2, parse_obj for v1
        try:
            md = CompanyResearch.model_validate(data)
        except AttributeError:
            md = CompanyResearch.parse_obj(data)
        return md.to_markdown()


if __name__ == '__main__':
    print(CompanyResearch.json_to_md())
    print(ResumeOptimization.json_to_md())
