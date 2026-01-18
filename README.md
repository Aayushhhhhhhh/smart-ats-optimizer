# Smart ATS: Resume Optimizer 🚀

An AI-powered resume optimization tool that helps job seekers improve their resume's compatibility with Applicant Tracking Systems (ATS) using machine learning and large language models.

## 🔗 Live Demo

**Try it now:** [https://smart-ats-optimizer-25sxivjo9gqdvezegc627k.streamlit.app/](https://smart-ats-optimizer-25sxivjo9gqdvezegc627k.streamlit.app/)


## Overview

Smart ATS Optimizer analyzes your resume against a job description and provides:
- **Quantitative Match Score**: Uses cosine similarity to calculate how well your resume matches the job description
- **AI-Powered Feedback**: Leverages LLaMA 3.3 70B to provide actionable insights and recommendations
- **Missing Keywords Analysis**: Identifies critical keywords you should include
- **Profile Summary Suggestions**: Generates optimized profile summaries tailored to the job

## Features

- 📊 **ATS Match Score**: Mathematical calculation using vector similarity
- 🤖 **AI Analysis**: Detailed feedback powered by Meta's LLaMA 3.3
- 📝 **Keyword Detection**: Identifies missing technical keywords from job descriptions
- ✍️ **Profile Rewrite**: AI-generated profile summaries optimized for specific roles
- 🎯 **Action Plan**: Specific recommendations to improve your resume

## Tech Stack

- **Frontend**: Streamlit
- **PDF Processing**: PyPDF2
- **ML/NLP**: scikit-learn (CountVectorizer, Cosine Similarity)
- **LLM Integration**: LangChain + OpenRouter API (LLaMA 3.3 70B)
- **Language**: Python 3.x

## Installation

### Prerequisites

- Python 3.8 or higher
- OpenRouter API key ([Get one here](https://openrouter.ai/))

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Aayushhhhhhhh/smart-ats-optimizer.git
cd smart-ats-optimizer
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.streamlit/secrets.toml` file in the project root:
```toml
OPENROUTER_API_KEY = "your_openrouter_api_key_here"
```

## Usage

1. Start the Streamlit app:
```bash
streamlit run app.py
```

2. Open your browser and navigate to the provided local URL (typically `http://localhost:8501`)

3. Use the application:
   - Paste the job description in the sidebar text area
   - Upload your resume (PDF format)
   - Click "Evaluate Resume"
   - Review your match score and AI-generated recommendations

## How It Works

### 1. Vector-Based Matching
The app uses **Cosine Similarity** to calculate how closely your resume matches the job description:
- Converts both texts into numerical vectors using CountVectorizer
- Calculates the angle between vectors to determine similarity
- Returns a percentage score (0-100%)

### 2. AI Analysis
Powered by LLaMA 3.3 70B through OpenRouter, the AI provides:
- Missing critical keywords
- Optimized profile summary rewrite
- Specific action items for improvement

### Score Interpretation

- **75-100%**: ✅ High Match - Your resume is well-optimized
- **50-74%**: ⚠️ Moderate Match - Needs improvement
- **0-49%**: ⚠️ Low Match - Significant changes required

## Dependencies

Create a `requirements.txt` file with:
```
streamlit
PyPDF2
langchain-openai
scikit-learn
```

## Configuration

The app uses Streamlit secrets for API key management. For deployment on Streamlit Cloud:

1. Go to your app settings
2. Navigate to Secrets
3. Add your OpenRouter API key:
```toml
OPENROUTER_API_KEY = "your_key_here"
```

## Project Structure

```
smart-ats-optimizer/
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── .streamlit/
│   └── secrets.toml      # API keys (local development)
└── README.md             # Project documentation
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## Future Enhancements

- [ ] Support for multiple resume formats (DOCX, TXT)
- [ ] Batch processing for multiple resumes
- [ ] Resume template suggestions
- [ ] Industry-specific optimization
- [ ] Export analysis reports as PDF
- [ ] Resume version comparison

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- AI powered by [OpenRouter](https://openrouter.ai/) and Meta's LLaMA 3.3
- NLP processing with [scikit-learn](https://scikit-learn.org/)

## Author

**Aayush**
- GitHub: [@Aayushhhhhhhh](https://github.com/Aayushhhhhhhh)

---

⭐ If you find this project helpful, please consider giving it a star on GitHub!
