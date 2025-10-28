## Resume Application Tracking System (ATS)

This project is a Streamlit web application that leverages Google's Gemini Pro Vision API to help candidates analyze how well their resume matches a specific job description. It provides feedback, highlights strengths and weaknesses, and gives a percentage match between the uploaded resume and the entered job description.

### Features

- **Upload Your Resume:** Securely upload your resume in PDF format.
- **Job Description Analysis:** Paste the job description of your desired job.
- **AI-Powered Review:** Get a detailed, AI-generated evaluation of your resume against the job description.
- **Percentage Match:** Instantly see how closely your resume matches the job requirements, along with feedback on missing keywords and improvement suggestions.

### How It Works

1. **Upload Resume:** Upload your resume in PDF format directly to the Streamlit app.
2. **Input Job Description:** Paste the relevant job description into the provided text area.
3. **AI Analysis:** Use the provided buttons to receive:
    - A professional evaluation of your resume against the job description.
    - A percentage match, missing keywords, and final feedback.

The application uses Google Gemini's Vision model to analyze and compare the resume (converted to image) with the job description.

### Requirements

- Python 3.8+
- [Streamlit](https://streamlit.io/)
- [google-generativeai](https://pypi.org/project/google-generativeai/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [pdf2image](https://pypi.org/project/pdf2image/)
- [Pillow](https://pypi.org/project/Pillow/)

Install all dependencies using:

```
pip install -r requirements.txt
```

### Setup

1. **Clone the repository**

```
git clone https://github.com/yourusername/Resume-Application-Tracking-System-ATS.git
cd Resume-Application-Tracking-System-ATS
```

2. **Set up your environment variables**

Create a `.env` file in the project root with your [Google Gemini API key](https://aistudio.google.com/app/apikey):

```
GOOGLE_API_KEY=your_google_api_key_here
```

3. **Run the Streamlit app**

```
streamlit run app.py
```

### Usage

- Paste the job description in the first text area.
- Upload your resume PDF.
- Click "Tell Me About the Resume" for a qualitative assessment.
- Click "Percentage match" for a quantitative score and suggestions.

### Notes

- The application only analyzes the **first page** of the resume for simplicity.
- Make sure your Google Gemini API key has access to the Vision model.

### License

This project is for educational purposes. Adapt and expand for your own use!

### Acknowledgements

- [Streamlit](https://streamlit.io/)
- [Google Gemini Pro Vision](https://ai.google.dev/)
- [pdf2image](https://github.com/Belval/pdf2image)

---

