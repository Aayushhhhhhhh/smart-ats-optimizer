"""
Hybrid Scoring Engine — Phase 2 (India Edition)
Combines TF-IDF + semantic embeddings + India-specific taxonomy scoring.
"""

import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils.india_taxonomy import (
    INDIA_SKILL_ALIASES, get_all_india_skills,
    get_company_keywords, detect_target_company, detect_sector,
    ATS_ACTION_VERBS, ATS_POSITIVE_FLAGS, STANDARD_HEADERS,
    COMPANY_KEYWORDS, SECTOR_KEYWORDS,
)

# ---------------------------------------------------------------------------
# SKILL ALIASES — base + India-specific merged
# ---------------------------------------------------------------------------
BASE_ALIASES = {
    "py": "python", "python3": "python", "python 3": "python",
    "js": "javascript", "node": "nodejs", "node.js": "nodejs",
    "ts": "typescript", "c++": "cpp", "golang": "go",
    "ml": "machine learning", "dl": "deep learning",
    "nlp": "natural language processing", "cv": "computer vision",
    "llm": "large language model", "genai": "generative ai",
    "gen ai": "generative ai", "rl": "reinforcement learning",
    "reactjs": "react", "react.js": "react",
    "vuejs": "vue", "vue.js": "vue", "angularjs": "angular",
    "nextjs": "next.js", "aws": "amazon web services",
    "gcp": "google cloud platform", "k8s": "kubernetes",
    "postgres": "postgresql", "mongo": "mongodb",
    "mssql": "sql server", "powerbi": "power bi",
    "ci/cd": "ci cd", "cicd": "ci cd",
    "oop": "object oriented programming",
    "swe": "software engineer", "sde": "software development engineer",
}

SKILL_ALIASES = {**BASE_ALIASES, **INDIA_SKILL_ALIASES}


def normalize_text(text: str) -> str:
    """Lowercases and resolves skill aliases to canonical forms."""
    text = text.lower()
    for alias, canonical in sorted(SKILL_ALIASES.items(), key=lambda x: -len(x[0])):
        pattern = r'\b' + re.escape(alias) + r'\b'
        text = re.sub(pattern, canonical, text)
    return text


# ---------------------------------------------------------------------------
# CORE SCORING FUNCTIONS
# ---------------------------------------------------------------------------

def calculate_tfidf_score(resume_text: str, jd_text: str) -> float:
    norm_resume = normalize_text(resume_text)
    norm_jd = normalize_text(jd_text)
    vectorizer = TfidfVectorizer(
        stop_words='english', ngram_range=(1, 2),
        min_df=1, sublinear_tf=True,
    )
    try:
        matrix = vectorizer.fit_transform([norm_resume, norm_jd])
        score = cosine_similarity(matrix)[0][1] * 100
        return round(float(score), 2)
    except Exception:
        return 0.0


def calculate_semantic_score(resume_text: str, jd_text: str) -> float | None:
    try:
        from sentence_transformers import SentenceTransformer, util
        model = SentenceTransformer('all-MiniLM-L6-v2')
        embeddings = model.encode(
            [resume_text[:2000], jd_text[:2000]],
            convert_to_tensor=True, show_progress_bar=False
        )
        score = util.cos_sim(embeddings[0], embeddings[1]).item() * 100
        return round(float(score), 2)
    except ImportError:
        return None
    except Exception:
        return None


def calculate_india_taxonomy_score(resume_text: str, jd_text: str) -> dict:
    """
    India-specific scoring layer.
    Checks resume against Indian market skills, company keywords, sector keywords.
    Returns a score + breakdown dict.
    """
    norm_resume = normalize_text(resume_text)
    norm_jd = normalize_text(jd_text)

    # 1. India top skills present in both resume and JD
    india_skills = get_all_india_skills()
    jd_india_skills = [s for s in india_skills if s in norm_jd]
    resume_india_skills = [s for s in jd_india_skills if s in norm_resume]

    india_skill_score = (
        (len(resume_india_skills) / len(jd_india_skills) * 100)
        if jd_india_skills else 0
    )

    # 2. Company-specific boost
    target_company = detect_target_company(jd_text)
    company_score = 0.0
    company_matched = []
    company_missing = []

    if target_company:
        company_kws = get_company_keywords(target_company)
        company_kws_norm = [normalize_text(k) for k in company_kws]
        company_matched = [k for k in company_kws_norm if k in norm_resume]
        company_missing = [k for k in company_kws_norm if k not in norm_resume]
        company_score = (
            (len(company_matched) / len(company_kws_norm) * 100)
            if company_kws_norm else 0
        )

    # 3. Sector-specific boost
    sector = detect_sector(jd_text)
    sector_score = 0.0
    if sector and sector in SECTOR_KEYWORDS:
        sector_kws = [normalize_text(k) for k in SECTOR_KEYWORDS[sector]]
        sector_matched = [k for k in sector_kws if k in norm_resume]
        sector_score = (
            (len(sector_matched) / len(sector_kws) * 100)
            if sector_kws else 0
        )

    # 4. ATS formatting signals
    action_verb_count = sum(1 for v in ATS_ACTION_VERBS if v in norm_resume)
    positive_flag_count = sum(1 for f in ATS_POSITIVE_FLAGS if f in norm_resume)
    header_count = sum(1 for h in STANDARD_HEADERS if h in norm_resume)

    formatting_score = min(100, (
        (action_verb_count / len(ATS_ACTION_VERBS) * 40) +
        (positive_flag_count / len(ATS_POSITIVE_FLAGS) * 40) +
        (header_count / len(STANDARD_HEADERS) * 20)
    ) * 100 / 100)

    return {
        "india_skill_score": round(india_skill_score, 1),
        "company_score": round(company_score, 1),
        "sector_score": round(sector_score, 1),
        "formatting_score": round(formatting_score, 1),
        "target_company": target_company,
        "sector": sector,
        "company_matched": company_matched[:8],
        "company_missing": company_missing[:8],
        "india_skills_matched": resume_india_skills[:10],
        "india_skills_missing": [s for s in jd_india_skills if s not in norm_resume][:10],
        "action_verbs_found": action_verb_count,
        "ats_flags_found": positive_flag_count,
    }


def calculate_hybrid_score(resume_text: str, jd_text: str) -> dict:
    """
    Master scoring function — Phase 2 India Edition.

    Formula:
      - 30% TF-IDF keyword match
      - 40% Semantic similarity
      - 20% India taxonomy match
      - 10% ATS formatting score

    Falls back gracefully if sentence-transformers not installed.
    """
    keyword_score = calculate_tfidf_score(resume_text, jd_text)
    semantic_score = calculate_semantic_score(resume_text, jd_text)
    india_data = calculate_india_taxonomy_score(resume_text, jd_text)

    india_combined = (
        india_data["india_skill_score"] * 0.5 +
        india_data["company_score"] * 0.3 +
        india_data["sector_score"] * 0.2
    )

    formatting_score = india_data["formatting_score"]

    if semantic_score is not None:
        final_score = (
            0.30 * keyword_score +
            0.40 * semantic_score +
            0.20 * india_combined +
            0.10 * formatting_score
        )
        method = "hybrid_india"
    else:
        final_score = (
            0.50 * keyword_score +
            0.35 * india_combined +
            0.15 * formatting_score
        )
        method = "tfidf_india"

    return {
        "final_score": round(final_score, 1),
        "keyword_score": keyword_score,
        "semantic_score": semantic_score,
        "india_skill_score": india_data["india_skill_score"],
        "company_score": india_data["company_score"],
        "sector_score": india_data["sector_score"],
        "formatting_score": formatting_score,
        "method": method,
        "target_company": india_data["target_company"],
        "sector": india_data["sector"],
        "company_matched": india_data["company_matched"],
        "company_missing": india_data["company_missing"],
        "india_skills_matched": india_data["india_skills_matched"],
        "india_skills_missing": india_data["india_skills_missing"],
        "action_verbs_found": india_data["action_verbs_found"],
        "ats_flags_found": india_data["ats_flags_found"],
    }


def extract_missing_keywords(resume_text: str, jd_text: str, top_n: int = 15) -> list[str]:
    """
    Smart missing keywords — combines TF-IDF + India taxonomy misses.
    India taxonomy misses are prioritized (more actionable).
    """
    norm_resume = normalize_text(resume_text)
    norm_jd = normalize_text(jd_text)

    # TF-IDF missing keywords
    vectorizer = TfidfVectorizer(
        stop_words='english', ngram_range=(1, 2), min_df=1,
    )
    tfidf_missing = []
    try:
        vectorizer.fit([norm_jd])
        feature_names = vectorizer.get_feature_names_out()
        jd_vector = vectorizer.transform([norm_jd]).toarray()[0]
        top_indices = jd_vector.argsort()[::-1][:top_n * 2]
        jd_keywords = [feature_names[i] for i in top_indices if jd_vector[i] > 0]
        tfidf_missing = [kw for kw in jd_keywords if kw not in norm_resume and len(kw) > 2]
    except Exception:
        pass

    # India taxonomy missing keywords (high priority)
    india_data = calculate_india_taxonomy_score(resume_text, jd_text)
    india_missing = india_data["india_skills_missing"] + india_data["company_missing"]

    # Merge: India-specific first, then TF-IDF
    seen = set()
    merged = []
    for kw in india_missing + tfidf_missing:
        if kw not in seen:
            seen.add(kw)
            merged.append(kw)

    return merged[:top_n]
