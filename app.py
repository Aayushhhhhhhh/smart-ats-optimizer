import streamlit as st
from langchain_openai import ChatOpenAI
from utils.pdf_parser import extract_text_from_pdf
from utils.scorer import calculate_hybrid_score, extract_missing_keywords

st.set_page_config(
    page_title="Smart ATS Optimizer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');
    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
    h1, h2, h3 { font-family: 'Syne', sans-serif !important; }

    .score-card {
        background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 100%);
        border: 1px solid rgba(99,102,241,0.3);
        border-radius: 16px; padding: 24px; text-align: center; color: white;
    }
    .score-number {
        font-family: 'Syne', sans-serif; font-size: 3.5rem; font-weight: 800;
        background: linear-gradient(135deg, #818cf8, #38bdf8);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; line-height: 1;
    }
    .score-label { font-size: 0.8rem; letter-spacing: 0.12em; text-transform: uppercase; color: rgba(255,255,255,0.5); margin-top: 6px; }
    .sub-score {
        background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08);
        border-radius: 10px; padding: 12px 16px; margin-top: 8px;
        display: flex; justify-content: space-between; align-items: center;
        color: white; font-size: 0.88rem;
    }
    .keyword-pill {
        display: inline-block; background: rgba(239,68,68,0.15);
        border: 1px solid rgba(239,68,68,0.4); color: #fca5a5;
        border-radius: 20px; padding: 4px 12px; margin: 4px; font-size: 0.82rem;
    }
    .keyword-pill-green {
        display: inline-block; background: rgba(34,197,94,0.15);
        border: 1px solid rgba(34,197,94,0.4); color: #86efac;
        border-radius: 20px; padding: 4px 12px; margin: 4px; font-size: 0.82rem;
    }
    .india-badge {
        display: inline-block; background: linear-gradient(135deg, rgba(255,153,0,0.2), rgba(19,136,8,0.2));
        border: 1px solid rgba(255,153,0,0.4); color: #fcd34d;
        border-radius: 8px; padding: 3px 12px; font-size: 0.78rem; letter-spacing: 0.06em;
    }
    .company-badge {
        display: inline-block; background: rgba(99,102,241,0.2);
        border: 1px solid rgba(99,102,241,0.4); color: #a5b4fc;
        border-radius: 8px; padding: 3px 12px; font-size: 0.78rem;
    }
    .stButton > button {
        background: linear-gradient(135deg, #6366f1, #38bdf8) !important;
        color: white !important; border: none !important; border-radius: 10px !important;
        padding: 0.6rem 2rem !important; font-family: 'Syne', sans-serif !important;
        font-weight: 600 !important; font-size: 1rem !important; width: 100%;
    }
    .progress-bar-wrap { background: rgba(255,255,255,0.08); border-radius: 8px; height: 8px; margin-top: 4px; }
    .progress-bar-fill { height: 8px; border-radius: 8px; background: linear-gradient(90deg, #6366f1, #38bdf8); }
</style>
""", unsafe_allow_html=True)

# API Key
try:
    api_key = st.secrets["OPENROUTER_API_KEY"]
except Exception:
    st.error("⚠️ API Key missing. Add OPENROUTER_API_KEY to Streamlit Secrets.")
    st.stop()

def get_llm_response(prompt: str) -> str:
    try:
        llm = ChatOpenAI(
            openai_api_key=api_key,
            base_url="https://openrouter.ai/api/v1",
            model_name="meta-llama/llama-3.3-70b-instruct:free",
            temperature=0.0, request_timeout=60,
        )
        return llm.invoke(prompt).content
    except Exception as e:
        return f"⚠️ AI analysis unavailable: {str(e)}"

def score_color(score: float) -> str:
    if score >= 75: return "#22c55e"
    elif score >= 50: return "#f59e0b"
    return "#ef4444"

def score_status(score: float):
    if score >= 75: return "✅ Strong Match"
    elif score >= 50: return "⚠️ Moderate Match"
    return "❌ Low Match"

def progress_bar(score: float, color: str = None) -> str:
    c = color or score_color(score)
    return f"""
    <div class="progress-bar-wrap">
      <div class="progress-bar-fill" style="width:{score}%; background: linear-gradient(90deg, {c}, {c}cc);"></div>
    </div>"""

# Sidebar
with st.sidebar:
    st.markdown("## 🎯 Smart ATS Optimizer")
    st.markdown('<span class="india-badge">🇮🇳 India Edition</span>', unsafe_allow_html=True)
    st.markdown("*Optimized for Naukri, TCS, Infosys, Wipro & more*")
    st.divider()

    jd = st.text_area("📋 Paste Job Description", height=300,
        placeholder="Paste the full job description here...\n\nWorks best with Naukri JDs, LinkedIn India, Foundit")

    uploaded_file = st.file_uploader("📄 Upload Resume (PDF)", type=["pdf"],
        help="Supports multi-column resumes via pdfplumber")

    st.divider()
    submit = st.button("🚀 Evaluate Resume", use_container_width=True)
    st.markdown("""
    <div style='font-size:0.72rem; color:rgba(255,255,255,0.3); margin-top:12px;'>
    Scoring: 30% keywords + 40% semantic + 20% India taxonomy + 10% ATS formatting
    </div>""", unsafe_allow_html=True)

# Main
st.markdown("# Smart ATS Optimizer 🎯")
st.markdown("##### Hybrid AI scoring — built for the Indian job market")

if not submit:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("**Step 1**\n\nPaste Job Description from Naukri, LinkedIn India, or Foundit")
    with col2:
        st.info("**Step 2**\n\nUpload your resume PDF")
    with col3:
        st.info("**Step 3**\n\nGet your India ATS score with company-specific feedback")

    st.markdown("---")
    st.markdown("""
    **Phase 2 — India Edition includes:**
    - 🇮🇳 **India Skills Taxonomy** — 100+ skills from Naukri/LinkedIn India 2025-26
    - 🏢 **Company-specific scoring** — TCS, Infosys, Wipro, HCL, Cognizant, Accenture, Tech Mahindra, Capgemini
    - 🏭 **Sector scoring** — IT Services, Fintech/BFSI, Startups, E-commerce
    - 📝 **ATS formatting check** — action verbs, positive flags, standard headers
    - 🔬 **Hybrid matching** — TF-IDF + semantic + India taxonomy
    """)

else:
    # Validation
    if not uploaded_file:
        st.warning("⚠️ Please upload a PDF resume.")
        st.stop()
    if not jd or len(jd.strip()) < 50:
        st.warning("⚠️ Please paste a job description (at least 50 characters).")
        st.stop()

    # Parse PDF
    with st.spinner("📄 Parsing resume..."):
        try:
            resume_text = extract_text_from_pdf(uploaded_file)
        except ValueError as e:
            st.error(str(e))
            st.stop()

    if len(resume_text.strip()) < 100:
        st.error("❌ Could not extract enough text. Make sure it's a text-based PDF.")
        st.stop()

    # Score
    with st.spinner("🔬 Running India ATS analysis..."):
        scores = calculate_hybrid_score(resume_text, jd)
        missing_keywords = extract_missing_keywords(resume_text, jd, top_n=15)

    st.divider()

    # ── Score Layout ──────────────────────────────────────────────────────────
    col_main, col_breakdown = st.columns([1, 1.8])

    with col_main:
        # Company & sector detection badges
        badge_html = ""
        if scores.get("target_company"):
            badge_html += f'<span class="company-badge">🏢 {scores["target_company"].upper()}</span> '
        if scores.get("sector"):
            sector_display = scores["sector"].replace("_", " ").title()
            badge_html += f'<span class="india-badge">🏭 {sector_display}</span>'
        if badge_html:
            st.markdown(badge_html, unsafe_allow_html=True)
            st.markdown("")

        st.markdown(f"""
        <div class="score-card">
            <div class="score-number">{scores["final_score"]}%</div>
            <div class="score-label">India ATS Match Score</div>
            <div style="margin-top:14px; font-size:1.05rem;">{score_status(scores["final_score"])}</div>
            <div style="margin-top:8px; font-size:0.75rem; color:rgba(255,255,255,0.4);">
                {"🔀 Hybrid + India" if "hybrid" in scores["method"] else "📊 TF-IDF + India"}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Sub-scores
        for label, key in [
            ("📊 Keyword Match", "keyword_score"),
            ("🧠 Semantic Match", "semantic_score"),
            ("🇮🇳 India Taxonomy", "india_skill_score"),
            ("🏢 Company Match", "company_score"),
            ("🏭 Sector Match", "sector_score"),
            ("📝 ATS Formatting", "formatting_score"),
        ]:
            val = scores.get(key)
            if val is None:
                continue
            color = score_color(val)
            st.markdown(f"""
            <div class="sub-score">
                <span>{label}</span>
                <strong style="color:{color}">{val}%</strong>
            </div>
            {progress_bar(val, color)}
            """, unsafe_allow_html=True)

    with col_breakdown:
        # Overall interpretation
        if scores["final_score"] >= 75:
            st.success(f"✅ **Strong Match** — Your resume is well-aligned. "
                       "Focus on quantifying achievements and polishing your summary.")
        elif scores["final_score"] >= 50:
            st.warning(f"⚠️ **Moderate Match** — Good foundation. "
                       "Add missing keywords naturally and strengthen experience bullets.")
        else:
            st.error(f"❌ **Low Match** — Significant work needed. "
                     "Review all missing keywords and restructure around this role.")

        # Company-specific feedback
        if scores.get("target_company") and scores.get("company_score", 0) < 80:
            company = scores["target_company"].upper()
            matched = scores.get("company_matched", [])
            missing_co = scores.get("company_missing", [])

            with st.expander(f"🏢 {company}-Specific Analysis", expanded=True):
                if matched:
                    matched_html = "".join(f'<span class="keyword-pill-green">{k}</span>' for k in matched)
                    st.markdown(f"**✅ Matched:** {matched_html}", unsafe_allow_html=True)
                if missing_co:
                    missing_html = "".join(f'<span class="keyword-pill">{k}</span>' for k in missing_co)
                    st.markdown(f"**❌ Missing:** {missing_html}", unsafe_allow_html=True)

        # ATS formatting signals
        with st.expander("📝 ATS Formatting Signals"):
            av = scores.get("action_verbs_found", 0)
            af = scores.get("ats_flags_found", 0)
            st.markdown(f"""
            - **Action verbs detected:** {av}/{len(['created','implemented','developed','optimized','deployed','automated','architected','migrated','engineered','delivered'])} ({'✅ Good' if av >= 6 else '⚠️ Add more strong action verbs'})
            - **ATS positive flags:** {af}/{len(['scalability','agile methodology','cloud migration','ci cd','sdlc','stakeholder management','end to end delivery','high performance'])} ({'✅ Good' if af >= 4 else '⚠️ Add more professional buzzwords'})
            """)

        # India skills matched
        if scores.get("india_skills_matched"):
            with st.expander("🇮🇳 India Market Skills — Matched"):
                pills = "".join(f'<span class="keyword-pill-green">{s}</span>'
                                for s in scores["india_skills_matched"])
                st.markdown(pills, unsafe_allow_html=True)

    st.divider()

    # ── Missing Keywords ──────────────────────────────────────────────────────
    st.markdown("### 🔍 Missing Keywords (Prioritized)")
    if missing_keywords:
        st.caption("India-taxonomy keywords shown first — these have highest ATS impact.")
        pills = "".join(f'<span class="keyword-pill">{kw}</span>' for kw in missing_keywords)
        st.markdown(f'<div style="margin:12px 0">{pills}</div>', unsafe_allow_html=True)
    else:
        st.success("✅ Excellent keyword coverage!")

    st.divider()

    # ── AI Analysis ───────────────────────────────────────────────────────────
    st.markdown("### 🤖 AI-Powered Feedback")

    with st.spinner("Generating detailed feedback..."):
        company_ctx = f"targeting {scores['target_company'].upper()}" if scores.get("target_company") else "for an Indian company"
        sector_ctx = scores.get("sector", "IT").replace("_", " ")
        missing_str = ", ".join(missing_keywords[:10]) if missing_keywords else "None"

        prompt = f"""
You are a senior Technical Recruiter specializing in the Indian job market.
Evaluate this resume for a {sector_ctx} role {company_ctx}.

ATS Score: {scores["final_score"]}% (Keyword: {scores["keyword_score"]}%, Semantic: {scores.get("semantic_score","N/A")}%, India Taxonomy: {scores["india_skill_score"]}%)
Missing keywords: {missing_str}

Resume (first 3000 chars):
{resume_text[:3000]}

Job Description (first 2000 chars):
{jd[:2000]}

Respond EXACTLY in this format:

## 📝 Optimized Profile Summary
Write a 3-sentence profile summary highly optimized for this specific JD and Indian market. Use keywords naturally.

## 🎯 Top 3 Action Items
Give 3 specific, concrete changes. For each: mention the exact section, what to add/change, and why it helps the ATS score.

## 🇮🇳 India Market Insight
In 2-3 sentences: what specific skills or keywords are most valued for this role in the Indian market right now, and how does this resume compare.
"""
        ai_response = get_llm_response(prompt)
        st.markdown(ai_response)

    st.divider()

    with st.expander("🔎 View Extracted Resume Text"):
        st.text_area("Verify parsing quality:", resume_text, height=250)
        st.caption(f"Characters extracted: {len(resume_text):,}")
