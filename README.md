# 🛡️ Raksha - Family Digital Safety Guardian

## Streamlit Version

A Python Streamlit application that helps families identify and avoid online scams using AI-powered analysis.

### Features

✅ **Message Checker** - Detect scams in SMS, WhatsApp, and email messages
✅ **Link Inspector** - Analyze suspicious URLs for phishing and malicious content
✅ **Call Checker** - Verify phone numbers and detect scam calls
✅ **Learn & Quiz** - Interactive quiz to educate users about common scams
✅ **Bilingual Support** - English and Telugu
✅ **Groq AI Integration** - Real-time AI analysis

### Tech Stack

- **Frontend:** Streamlit
- **Backend:** Python
- **AI:** Groq API (Mixtral 8x7B)
- **Deployment:** Streamlit Cloud

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/Vishalyanamala27/raksha-streamlit.git
cd raksha-streamlit
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

5. **Run the app:**
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

### Deployment to Streamlit Cloud

1. **Push to GitHub:**
```bash
git add .
git commit -m "Initial commit: Raksha Streamlit app"
git push origin main
```

2. **Deploy on Streamlit Cloud:**
   - Go to https://streamlit.io/cloud
   - Click "New app"
   - Select your GitHub repository
   - Select branch: `main`
   - Select file: `app.py`
   - Click "Deploy"

3. **Add Secrets:**
   - In Streamlit Cloud dashboard, click "Settings"
   - Add secret: `GROQ_API_KEY=your_key_here`

### Usage

#### Message Checker
1. Go to "Message Checker" tab
2. Paste a suspicious message
3. Click "Analyze Message"
4. View results with verdict, confidence score, red flags, and advice

#### Link Inspector
1. Go to "Link Inspector" tab
2. Paste a suspicious URL
3. Click "Analyze URL"
4. View risk level, risk factors, and explanation

#### Call Checker
1. Go to "Call Checker" tab
2. Enter phone number and call count
3. Click "Analyze Call"
4. View call risk assessment and advice

#### Learn & Quiz
1. Go to "Learn & Quiz" tab
2. Click "Start Quiz"
3. Answer multiple-choice questions
4. View score and explanations

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GROQ_API_KEY` | ✅ Yes | Groq API authentication key |

### API Models

- **Mixtral 8x7B** - Primary model for all analysis tasks

### File Structure

```
raksha-streamlit/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .streamlit/
│   └── config.toml       # Streamlit configuration
└── README.md             # This file
```

### Troubleshooting

**Error: GROQ_API_KEY not found**
- Make sure `.env` file exists with your API key
- Or set it in Streamlit Cloud secrets

**Error: Module not found**
- Run: `pip install -r requirements.txt`

**App not responding**
- Check internet connection
- Verify Groq API key is valid
- Check Streamlit Cloud logs

### Performance

- **Load Time:** < 3 seconds
- **Analysis Time:** < 2 seconds per request
- **Concurrent Users:** Unlimited (Streamlit Cloud)

### Security

✅ API keys stored in environment variables
✅ No data stored on server
✅ HTTPS only communication
✅ Input validation on all fields

### Future Enhancements

- [ ] Database for storing analysis history
- [ ] User authentication
- [ ] More languages support
- [ ] Mobile app version
- [ ] Browser extension

### Contributing

Contributions are welcome! Please feel free to submit pull requests.

### License

MIT License - See LICENSE file for details

### Support

For issues and questions, please open an issue on GitHub.

---

**Made with 💚 for Digital Safety**

🛡️ **Raksha - Family Digital Safety Guardian**
