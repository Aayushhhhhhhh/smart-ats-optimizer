"""
India Skills Taxonomy
Built from Manus AI research — Indian tech job market 2025-2026.
Sources: Naukri.com, LinkedIn India, Foundit, company JD analysis.

This is your moat vs Jobscan/Teal — they have NO India-specific data.
"""

# ---------------------------------------------------------------------------
# TOP 100 IN-DEMAND SKILLS — Indian tech market 2025-2026
# ---------------------------------------------------------------------------
INDIA_TOP_SKILLS = [
    "artificial intelligence", "generative ai", "machine learning",
    "data science", "data analytics", "cloud computing",
    "cybersecurity", "ethical hacking", "devops", "full stack development",
    "python", "sql", "java", "javascript", "react", "nodejs",
    "typescript", "kubernetes", "docker", "terraform",
    "selenium", "ansible", "ui ux design", "product management",
    "digital marketing", "blockchain", "agile", "scrum",
    "microsoft fabric", "azure data factory", "power bi", "tableau",
    "data engineering", "mlops", "large language model", "prompt engineering",
    "r language", "cpp", "golang", "rust", "swift", "kotlin",
    "flutter", "react native", "microservices", "rest api", "graphql",
    "serverless", "snowflake", "databricks", "apache spark", "kafka",
    "mongodb", "postgresql", "redis", "jenkins", "ci cd",
    "git", "github", "site reliability engineering", "finops",
    "edge computing", "iot", "5g", "salesforce", "sap",
    "oracle cloud", "servicenow", "rpa", "uipath", "automation anywhere",
    "low code", "no code", "nlp", "computer vision", "reinforcement learning",
    "big data", "hadoop", "etl", "data governance",
    "payment gateway", "credit risk", "aml", "kyc",
    "performance marketing", "seo", "sem", "crm", "erp",
    "network engineering", "system administration", "active directory",
    "software testing", "langchain", "rag", "spring boot", "angular",
    "pyspark", "infrastructure management", "sdlc", "code review",
]

# ---------------------------------------------------------------------------
# COMPANY-SPECIFIC KEYWORDS
# What each major Indian IT company specifically looks for
# ---------------------------------------------------------------------------
COMPANY_KEYWORDS = {
    "tcs": [
        "sql", "java", "javascript", "python", "cpp",
        "system engineer", "specialist programmer", "digital specialist engineer",
        "agile", "cloud migration", "microservices", "devops",
    ],
    "infosys": [
        "specialist programmer", "digital specialist engineer", "power programmer",
        "java", "spring boot", "microservices", "rest api",
        "react", "angular", "aws", "azure", "gcp",
        "kubernetes", "docker", "terraform", "generative ai",
        "large language model", "rag", "etl", "snowflake",
        "sap abap", "sap fico", "sap s4hana",
    ],
    "wipro": [
        "java", "python", "azure", "sql", "react", "nodejs",
        "spring boot", "microservices", "kubernetes", "docker",
        "selenium", "ci cd", "cybersecurity",
    ],
    "hcl": [
        "network engineering", "cloud native", "java", "python",
        "pyspark", "data engineering", "etl", "apache spark",
        "databricks", "snowflake", "cybersecurity",
        "infrastructure management", "site reliability engineering",
    ],
    "cognizant": [
        "full stack", "artificial intelligence", "cloud computing",
        "generative ai", "react", "nodejs", "spring boot",
        "microservices", "sql", "devops", "selenium", "cypress",
    ],
    "accenture": [
        "artificial intelligence", "generative ai", "large language model",
        "rag", "prompt engineering", "langchain", "data analytics",
        "cloud migration", "aws", "azure", "gcp",
    ],
    "tech mahindra": [
        "automation", "5g", "java", "python", "cloud computing",
        "microservices", "api development", "rpa", "uipath",
        "network virtualization",
    ],
    "capgemini": [
        "java", "sql", "cloud computing", "data engineering",
        "etl", "snowflake", "databricks", "sap", "salesforce",
        "full stack development", "react", "angular", "nodejs",
    ],
}

# ---------------------------------------------------------------------------
# SECTOR-SPECIFIC KEYWORDS
# ---------------------------------------------------------------------------
SECTOR_KEYWORDS = {
    "it_services": [
        "artificial intelligence", "cloud computing", "cybersecurity",
        "devops", "full stack development", "java", "python", "sql",
        "automation", "data analytics", "site reliability engineering",
        "microservices", "api development", "kubernetes", "docker",
        "terraform", "ci cd", "agile", "project management", "sap",
    ],
    "fintech_bfsi": [
        "machine learning", "credit risk", "digital banking",
        "rbi compliance", "aml", "kyc", "sql", "data science",
        "cybersecurity", "blockchain", "payment gateway",
        "python", "r language", "power bi", "tableau",
        "cloud computing", "fraud detection", "customer analytics",
    ],
    "startups_product": [
        "generative ai", "agentic ai", "large language model",
        "prompt engineering", "langchain", "react", "nodejs",
        "golang", "rust", "flutter", "react native", "ui ux design",
        "product management", "mlops", "data engineering",
        "aws", "snowflake", "kafka", "microservices",
    ],
    "ecommerce": [
        "kafka", "apache spark", "data lakes", "streaming analytics",
        "supply chain", "logistics tech", "performance marketing",
        "seo", "sem", "quality assurance", "react", "nodejs",
        "python", "golang", "sql", "ui ux design",
        "personalization", "order management",
    ],
}

# ---------------------------------------------------------------------------
# ATS-POSITIVE BUZZWORDS
# ---------------------------------------------------------------------------
ATS_ACTION_VERBS = [
    "created", "implemented", "developed", "diagnosed", "modeled",
    "programmed", "reviewed", "optimized", "architected", "engineered",
    "deployed", "automated", "migrated", "spearheaded", "orchestrated",
    "executed", "delivered", "mentored", "refactored", "designed",
    "built", "launched", "led", "managed", "reduced", "improved",
    "increased", "streamlined", "integrated", "established",
]

ATS_POSITIVE_FLAGS = [
    "scalability", "cross functional", "stakeholder management",
    "agile methodology", "cloud migration", "cost optimization",
    "revenue growth", "process improvement", "end to end delivery",
    "high performance", "sdlc", "ci cd", "unit testing",
    "code review", "technical documentation", "safe",
    "scaled agile", "problem solving",
]

# Standard ATS-friendly section headers
STANDARD_HEADERS = [
    "summary", "professional experience", "technical skills",
    "projects", "education", "certifications", "achievements",
    "work experience", "skills", "internships",
]

# ---------------------------------------------------------------------------
# SKILL ALIASES — India-specific additions
# Extends the base aliases in scorer.py
# ---------------------------------------------------------------------------
INDIA_SKILL_ALIASES = {
    # Indian company aliases
    "tcs": "tata consultancy services",
    "infy": "infosys",
    "wipro tech": "wipro",
    "hclt": "hcl technologies",
    "cognizant": "cognizant technology solutions",
    "accenture india": "accenture",
    "tech m": "tech mahindra",
    "capgem": "capgemini",

    # Indian market specific
    "naukri": "naukri job portal",
    "bfsi": "banking financial services insurance",
    "sde1": "software development engineer",
    "sde2": "senior software development engineer",
    "sse": "senior software engineer",
    "tl": "tech lead",
    "sa": "solution architect",
    "ba": "business analyst",

    # SAP variants
    "sap s4": "sap s4hana",
    "s/4hana": "sap s4hana",
    "sap fi": "sap fico",
    "sap co": "sap fico",

    # Cloud shortforms common in India
    "az": "azure",
    "gke": "google kubernetes engine",
    "eks": "amazon elastic kubernetes service",
    "ec2": "amazon ec2",

    # GenAI (very hot in India 2025-26)
    "gen ai": "generative ai",
    "genai": "generative ai",
    "llms": "large language model",
    "langchain": "langchain",
    "llamaindex": "llamaindex",
    "rag pipeline": "rag",
    "agentic": "agentic ai",

    # Testing
    "qa engineer": "quality assurance",
    "sdet": "software development engineer in test",
    "manual testing": "software testing",
    "automation testing": "selenium",
}


def get_all_india_skills() -> list[str]:
    """Returns flat list of all India-specific skills for taxonomy matching."""
    all_skills = set(INDIA_TOP_SKILLS)

    for skills in COMPANY_KEYWORDS.values():
        all_skills.update([s.lower() for s in skills])

    for skills in SECTOR_KEYWORDS.values():
        all_skills.update([s.lower() for s in skills])

    return list(all_skills)


def get_company_keywords(company_name: str) -> list[str]:
    """
    Returns keywords for a specific Indian company.
    Fuzzy matches company name.
    """
    company_lower = company_name.lower()
    for company, keywords in COMPANY_KEYWORDS.items():
        if company in company_lower or company_lower in company:
            return keywords
    return []


def detect_target_company(jd_text: str) -> str | None:
    """
    Detects if the JD is for a specific Indian IT company.
    Returns company name or None.
    """
    jd_lower = jd_text.lower()
    company_mentions = {
        "tcs": ["tcs", "tata consultancy"],
        "infosys": ["infosys", "infy"],
        "wipro": ["wipro"],
        "hcl": ["hcl technologies", "hcltech"],
        "cognizant": ["cognizant", "ctsh"],
        "accenture": ["accenture"],
        "tech mahindra": ["tech mahindra", "techm"],
        "capgemini": ["capgemini"],
    }
    for company, aliases in company_mentions.items():
        if any(alias in jd_lower for alias in aliases):
            return company
    return None


def detect_sector(jd_text: str) -> str | None:
    """
    Detects the industry sector from JD text.
    Returns sector key or None.
    """
    jd_lower = jd_text.lower()
    sector_signals = {
        "fintech_bfsi": ["bank", "fintech", "bfsi", "insurance", "nbfc", "rbi", "kyc", "aml", "lending"],
        "ecommerce": ["e-commerce", "ecommerce", "marketplace", "d2c", "quick commerce", "logistics"],
        "startups_product": ["startup", "product company", "saas", "series a", "series b", "seed"],
        "it_services": ["it services", "consulting", "offshore", "outsourcing", "delivery center"],
    }
    for sector, signals in sector_signals.items():
        if any(signal in jd_lower for signal in signals):
            return sector
    return None
