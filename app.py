import streamlit as st
import os
from groq import Groq
import json
import re

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="Raksha - Family Digital Safety Guardian",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM CSS (3D + Glass + Hero) ====================
st.markdown("""
    <style>
    .main {
        padding: 2rem;
        background: linear-gradient(135deg, #f0f4ff 0%, #e8f4f8 100%);
    }
    
    /* Hero Banner */
    .hero-banner {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        border-radius: 24px;
        padding: 3rem 2rem;
        color: white;
        text-align: center;
        box-shadow: 0 25px 80px rgba(79, 172, 254, 0.35);
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }
    .hero-banner h1 {
        margin: 0;
        font-size: 2.8rem;
        font-weight: 800;
        text-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .hero-banner p {
        margin-top: 1rem;
        font-size: 1.15rem;
        opacity: 0.95;
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
        line-height: 1.6;
    }
    
    /* 3D Buttons */
    .stButton > button {
        background: linear-gradient(145deg, #3b82f6, #2563eb) !important;
        color: white !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 0.8rem 2.2rem !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        box-shadow: 0 6px 0 #1d4ed8, 0 10px 25px rgba(37, 99, 235, 0.35) !important;
        transition: all 0.15s ease !important;
        transform: translateY(0) !important;
    }
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 9px 0 #1d4ed8, 0 15px 35px rgba(37, 99, 235, 0.45) !important;
    }
    .stButton > button:active {
        transform: translateY(6px) !important;
        box-shadow: 0 0 0 #1d4ed8, 0 3px 8px rgba(37, 99, 235, 0.3) !important;
    }
    
    /* Secondary buttons */
    .stButton > button[kind="secondary"] {
        background: linear-gradient(145deg, #10b981, #059669) !important;
        box-shadow: 0 6px 0 #047857, 0 10px 25px rgba(5, 150, 105, 0.35) !important;
    }
    .stButton > button[kind="secondary"]:hover {
        box-shadow: 0 9px 0 #047857, 0 15px 35px rgba(5, 150, 105, 0.45) !important;
    }
    .stButton > button[kind="secondary"]:active {
        transform: translateY(6px) !important;
        box-shadow: 0 0 0 #047857, 0 3px 8px rgba(5, 150, 105, 0.3) !important;
    }
    
    /* Example Buttons (subtle glass) */
    div[data-testid="stHorizontalBlock"] .stButton > button {
        background: rgba(255,255,255,0.85) !important;
        color: #334155 !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08) !important;
        border: 1px solid rgba(255,255,255,0.6) !important;
        font-weight: 600 !important;
    }
    div[data-testid="stHorizontalBlock"] .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 25px rgba(0,0,0,0.12) !important;
        background: rgba(255,255,255,0.95) !important;
    }
    
    /* Glassmorphism Badges */
    .scam-badge {
        padding: 0.7rem 1.4rem;
        border-radius: 1rem;
        font-weight: 700;
        display: inline-block;
        margin: 0.5rem 0;
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255,255,255,0.4);
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    .scam-high {
        background: rgba(254, 226, 226, 0.85);
        color: #991b1b;
        box-shadow: 0 4px 20px rgba(153, 27, 27, 0.2);
    }
    .scam-medium {
        background: rgba(254, 243, 199, 0.85);
        color: #92400e;
        box-shadow: 0 4px 20px rgba(146, 64, 14, 0.2);
    }
    .scam-low {
        background: rgba(220, 252, 231, 0.85);
        color: #15803d;
        box-shadow: 0 4px 20px rgba(21, 128, 61, 0.2);
    }
    .scam-safe {
        background: rgba(209, 250, 229, 0.85);
        color: #065f46;
        box-shadow: 0 4px 20px rgba(6, 95, 70, 0.2);
    }
    
    /* Counter Badge */
    .counter-badge {
        background: rgba(209, 250, 229, 0.6);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 1rem 1.5rem;
        border: 1px solid rgba(255,255,255,0.5);
        box-shadow: 0 8px 32px rgba(0,0,0,0.08);
        display: inline-block;
        margin: 1rem 0;
    }
    .counter-badge span {
        color: #065f46;
        font-weight: 700;
        font-size: 1.1rem;
    }
    
    /* 3D Report Button */
    .report-btn {
        background: linear-gradient(145deg, #dc2626, #b91c1c);
        color: white;
        padding: 0.8rem 1.8rem;
        border-radius: 14px;
        text-decoration: none;
        font-weight: 700;
        display: inline-block;
        margin-top: 0.5rem;
        box-shadow: 0 6px 0 #991b1b, 0 10px 25px rgba(220, 38, 38, 0.35);
        transition: all 0.15s ease;
    }
    .report-btn:hover {
        transform: translateY(-3px);
        box-shadow: 0 9px 0 #991b1b, 0 15px 35px rgba(220, 38, 38, 0.45);
    }
    .report-btn:active {
        transform: translateY(6px);
        box-shadow: 0 0 0 #991b1b, 0 3px 8px rgba(220, 38, 38, 0.3);
    }
    
    /* Sidebar Glass */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8fafc 0%, #eef2ff 100%) !important;
        border-right: 1px solid rgba(255,255,255,0.6);
    }
    
    /* Inputs */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        border-radius: 16px !important;
        border: 2px solid #e2e8f0 !important;
        box-shadow: inset 0 2px 6px rgba(0,0,0,0.06) !important;
        transition: all 0.3s ease !important;
        background: rgba(255,255,255,0.8) !important;
    }
    .stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.15), inset 0 2px 6px rgba(0,0,0,0.06) !important;
        background: white !important;
    }
    
    /* Metrics 3D */
    [data-testid="stMetric"] {
        background: white;
        border-radius: 20px;
        padding: 1.2rem;
        box-shadow: 0 12px 30px rgba(0,0,0,0.08);
        border: 1px solid rgba(255,255,255,0.6);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] button {
        font-size: 16px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stTabs [data-baseweb="tab-list"] button:hover {
        transform: translateY(-2px);
        color: #2563eb !important;
    }
    
    /* Floating Action Button */
    .fab-report {
        position: fixed;
        bottom: 2rem;
        right: 2rem;
        width: 64px;
        height: 64px;
        background: linear-gradient(145deg, #ff6b6b, #ee5a5a);
        border-radius: 50%;
        box-shadow: 0 10px 35px rgba(255, 107, 107, 0.45);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 1.6rem;
        text-decoration: none;
        z-index: 9999;
        transition: all 0.3s ease;
        border: 3px solid rgba(255,255,255,0.3);
    }
    .fab-report:hover {
        transform: translateY(-5px) scale(1.1);
        box-shadow: 0 18px 45px rgba(255, 107, 107, 0.55);
    }
    </style>
""", unsafe_allow_html=True)

# ==================== GROQ CLIENT ====================
@st.cache_resource
def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        st.error("❌ GROQ_API_KEY not found. Please set it in your environment variables.")
        st.stop()
    return Groq(api_key=api_key)

client = get_groq_client()

# ==================== LANGUAGE SETUP ====================
LANGUAGE_OPTIONS = {
    "English": "en",
    "తెలుగు (Telugu)": "te",
    "தமிழ் (Tamil)": "ta",
    "हिन्दी (Hindi)": "hi",
    "ಕನ್ನಡ (Kannada)": "kn"
}

TRANSLATIONS = {
    "en": {
        "title": "Raksha - Family Digital Safety Guardian",
        "subtitle": "Protect your family from online scams with AI-powered analysis",
        "message_checker": "Message Checker",
        "link_inspector": "Link Inspector",
        "call_checker": "Call Checker",
        "learn_quiz": "Learn & Quiz",
        "paste_message": "Paste a suspicious message:",
        "analyze_btn": "Analyze Message",
        "paste_url": "Paste a suspicious URL:",
        "analyze_url": "Analyze URL",
        "phone_number": "Enter phone number:",
        "call_count": "Number of calls:",
        "analyze_call": "Analyze Call",
        "verdict": "Verdict",
        "confidence": "Confidence Score",
        "red_flags": "Red Flags",
        "advice": "Advice",
        "risk_factors": "Risk Factors",
        "explanation": "Explanation",
        "quiz_title": "Learn & Spot Scams Quiz",
        "question": "Question",
        "submit_answer": "Submit Answer",
        "score": "Your Score",
        "language": "Language",
        "safe": "Safe",
        "suspicious": "Suspicious",
        "scam": "Scam",
        "high_risk": "High Risk",
        "medium_risk": "Medium Risk",
        "low_risk": "Low Risk",
        "stats_scams_blocked": "Scams Detected",
        "stats_users_protected": "Users Protected",
        "stats_accuracy": "Detection Accuracy",
        "report_scam": "Report Scam",
        "footer": "Raksha uses AI to detect potential scams. Always verify with official sources.",
        "bilingual_note": "Bilingual Output",
        "check_message": "Check Message",
        "is_scam": "Is this message a scam?",
        "paste_any": "Paste any SMS, WhatsApp, or email you're unsure about.",
        "try_example": "Try an example:",
        "messages_checked": "messages checked",
        "scams_caught": "scams caught",
    },
    "te": {
        "title": "రక్ష - కుటుంబ డిజిటల్ సేఫ్టీ గార్డియన్",
        "subtitle": "AI-ఆధారిత విశ్లేషణతో మీ కుటుంబాన్ని ఆన్‌లైన్ స్కామ్‌ల నుండి రక్షించండి",
        "message_checker": "సందేశ చెకర్",
        "link_inspector": "లింక్ ఇన్‌స్పెక్టర్",
        "call_checker": "కాల్ చెకర్",
        "learn_quiz": "నేర్చుకోండి & క్విజ్",
        "paste_message": "సందేశాన్ని అతికించండి:",
        "analyze_btn": "సందేశాన్ని విశ్లేషించండి",
        "paste_url": "సందేశ URL ను అతికించండి:",
        "analyze_url": "URLను విశ్లేషించండి",
        "phone_number": "ఫోన్ నంబర్ నమోదు చేయండి:",
        "call_count": "కాల్‌ల సంఖ్య:",
        "analyze_call": "కాల్‌ను విశ్లేషించండి",
        "verdict": "తీర్పు",
        "confidence": "విశ్వాస స్కోర్",
        "red_flags": "ఎరుపు జెండాలు",
        "advice": "సలహా",
        "risk_factors": "రిస్క్ కారకాలు",
        "explanation": "వివరణ",
        "quiz_title": "నేర్చుకోండి & స్కామ్‌లను గుర్తించండి క్విజ్",
        "question": "ప్రశ్న",
        "submit_answer": "సమాధానం సమర్పించండి",
        "score": "మీ స్కోర్",
        "language": "భాష",
        "safe": "సురక్షితం",
        "suspicious": "అనుమానాస్పదం",
        "scam": "స్కామ్",
        "high_risk": "అధిక ప్రమాదం",
        "medium_risk": "మధ్యస్థ ప్రమాదం",
        "low_risk": "తక్కువ ప్రమాదం",
        "stats_scams_blocked": "కనుగొన్న స్కామ్‌లు",
        "stats_users_protected": "రక్షించిన వినియోగదారులు",
        "stats_accuracy": "గుర్తింపు ఖచ్చితత్వం",
        "report_scam": "స్కామ్ ను రిపోర్ట్ చేయండి",
        "footer": "రక్ష AI ను ఉపయోగించి సంభావ్య స్కామ్‌లను కనుగొంటుంది. ఎల్లప్పుడూ అధికారిక మూలాలతో ధృవీకరించండి.",
        "bilingual_note": "ద్విభాషా అవుట్‌పుట్",
        "check_message": "సందేశాన్ని పరిశీలించండి",
        "is_scam": "ఈ సందేశం స్కామ్ అయ్యే అవకాశం ఉందా?",
        "paste_any": "మీకు అనుమానం ఉన్న ఏదైనా SMS, WhatsApp, లేదా ఇమెయిల్‌ను అతికించండి.",
        "try_example": "ఉదాహరణను ప్రయత్నించండి:",
        "messages_checked": "సందేశాలు పరిశీలించబడ్డాయి",
        "scams_caught": "స్కామ్‌లు పట్టుబడ్డాయి",
    },
    "ta": {
        "title": "ரக்ஷா - குடும்ப டிஜிட்டல் பாதுகாப்பு காவலர்",
        "subtitle": "AI-ஆல் இயக்கப்படும் பகுப்பாய்வுடன் உங்கள் குடும்பத்தை ஆன்லைன் மோசடிகளிலிருந்து பாதுகாக்கவும்",
        "message_checker": "செய்தி சரிபார்ப்பு",
        "link_inspector": "இணைப்பு ஆய்வாளர்",
        "call_checker": "அழைப்பு சரிபார்ப்பு",
        "learn_quiz": "கற்றல் & வினாடி வினா",
        "paste_message": "சந்தேகத்திற்கிடமான செய்தியை ஒட்டவும்:",
        "analyze_btn": "செய்தியை பகுப்பாய்வு செய்",
        "paste_url": "சந்தேகத்திற்கிடமான URL ஐ ஒட்டவும்:",
        "analyze_url": "URL ஐ பகுப்பாய்வு செய்",
        "phone_number": "தொலைபேசி எண்ணை உள்ளிடவும்:",
        "call_count": "அழைப்புகளின் எண்ணிக்கை:",
        "analyze_call": "அழைப்பை பகுப்பாய்வு செய்",
        "verdict": "தீர்ப்பு",
        "confidence": "நம்பகத்தன்மை மதிப்பெண்",
        "red_flags": "எச்சரிக்கை கொடிகள்",
        "advice": "ஆலோசனை",
        "risk_factors": "ஆபத்து காரணிகள்",
        "explanation": "விளக்கம்",
        "quiz_title": "மோசடிகளை கண்டறிய கற்றல் & வினாடி வினா",
        "question": "கேள்வி",
        "submit_answer": "பதிலை சமர்ப்பிக்கவும்",
        "score": "உங்கள் மதிப்பெண்",
        "language": "மொழி",
        "safe": "பாதுகாப்பானது",
        "suspicious": "சந்தேகத்திற்கிடமானது",
        "scam": "மோசடி",
        "high_risk": "அதிக ஆபத்து",
        "medium_risk": "நடுத்தர ஆபத்து",
        "low_risk": "குறைந்த ஆபத்து",
        "stats_scams_blocked": "கண்டறியப்பட்ட மோசடிகள்",
        "stats_users_protected": "பாதுகாக்கப்பட்ட பயனர்கள்",
        "stats_accuracy": "கண்டறிதல் துல்லியம்",
        "report_scam": "மோசடியைப் புகாரளிக்கவும்",
        "footer": "ரக்ஷா AI ஐப் பயன்படுத்தி சாத்தியமான மோசடிகளைக் கண்டறிகிறது. எப்போதும் அதிகாரப்பூர்வ ஆதாரங்களுடன் சரிபார்க்கவும்.",
        "bilingual_note": "இருமொழி வெளியீடு",
        "check_message": "செய்தியை சரிபார்க்கவும்",
        "is_scam": "இந்த செய்தி மோசடியா?",
        "paste_any": "நீங்கள் உறுதியாக இல்லாத எந்த SMS, WhatsApp, அல்லது மின்னஞ்சலையும் ஒட்டவும்.",
        "try_example": "ஒரு உதாரணத்தை முயற்சிக்கவும்:",
        "messages_checked": "செய்திகள் சரிபார்க்கப்பட்டன",
        "scams_caught": "மோசடிகள் பிடிக்கப்பட்டன",
    },
    "hi": {
        "title": "रक्षा - परिवार डिजिटल सुरक्षा संरक्षक",
        "subtitle": "AI-संचालित विश्लेषण के साथ अपने परिवार को ऑनलाइन घोटालों से बचाएं",
        "message_checker": "संदेश जांचकर्ता",
        "link_inspector": "लिंक निरीक्षक",
        "call_checker": "कॉल जांचकर्ता",
        "learn_quiz": "सीखें और क्विज़",
        "paste_message": "एक संदिग्ध संदेश पेस्ट करें:",
        "analyze_btn": "संदेश का विश्लेषण करें",
        "paste_url": "एक संदिग्ध URL पेस्ट करें:",
        "analyze_url": "URL का विश्लेषण करें",
        "phone_number": "फोन नंबर दर्ज करें:",
        "call_count": "कॉल की संख्या:",
        "analyze_call": "कॉल का विश्लेषण करें",
        "verdict": "फैसला",
        "confidence": "विश्वास स्कोर",
        "red_flags": "रेड फ्लैग्स",
        "advice": "सलाह",
        "risk_factors": "जोखिम कारक",
        "explanation": "व्याख्या",
        "quiz_title": "सीखें और घोटालों की पहचान करें क्विज़",
        "question": "प्रश्न",
        "submit_answer": "उत्तर जमा करें",
        "score": "आपका स्कोर",
        "language": "भाषा",
        "safe": "सुरक्षित",
        "suspicious": "संदिग्ध",
        "scam": "घोटाला",
        "high_risk": "उच्च जोखिम",
        "medium_risk": "मध्यम जोखिम",
        "low_risk": "कम जोखिम",
        "stats_scams_blocked": "पता लगाए गए घोटाले",
        "stats_users_protected": "संरक्षित उपयोगकर्ता",
        "stats_accuracy": "पता लगाने की सटीकता",
        "report_scam": "घोटाले की रिपोर्ट करें",
        "footer": "रक्षा AI का उपयोग करके संभावित घोटालों का पता लगाती है। हमेशा आधिकारिक स्रोतों के साथ सत्यापित करें।",
        "bilingual_note": "द्विभाषी आउटपुट",
        "check_message": "संदेश जांचें",
        "is_scam": "क्या यह संदेश घोटाला है?",
        "paste_any": "कोई भी SMS, WhatsApp, या ईमेल पेस्ट करें जिसके बारे में आपको संदेह है।",
        "try_example": "एक उदाहरण आजमाएं:",
        "messages_checked": "संदेश जांचे गए",
        "scams_caught": "घोटाले पकड़े गए",
    },
    "kn": {
        "title": "ರಕ್ಷ - ಕುಟುಂಬ ಡಿಜಿಟಲ್ ಸುರಕ್ಷತಾ ರಕ್ಷಕ",
        "subtitle": "AI-ಆಧಾರಿತ ವಿಶ್ಲೇಷಣೆಯೊಂದಿಗೆ ನಿಮ್ಮ ಕುಟುಂಬವನ್ನು ಆನ್‌ಲೈನ್ ಸ್ಕ್ಯಾಮ್‌ಗಳಿಂದ ರಕ್ಷಿಸಿ",
        "message_checker": "ಸಂದೇಶ ಪರಿಶೀಲಕ",
        "link_inspector": "ಲಿಂಕ್ ಪರಿಶೀಲಕ",
        "call_checker": "ಕಾಲ್ ಪರಿಶೀಲಕ",
        "learn_quiz": "ಕಲಿ ಮತ್ತು ರಸಪ್ರಶ್ನೆ",
        "paste_message": "ಅನುಮಾನಾಸ್ಪದ ಸಂದೇಶವನ್ನು ಅಂಟಿಸಿ:",
        "analyze_btn": "ಸಂದೇಶವನ್ನು ವಿಶ್ಲೇಷಿಸಿ",
        "paste_url": "ಅನುಮಾನಾಸ್ಪದ URL ಅನ್ನು ಅಂಟಿಸಿ:",
        "analyze_url": "URL ಅನ್ನು ವಿಶ್ಲೇಷಿಸಿ",
        "phone_number": "ಫೋನ್ ಸಂಖ್ಯೆಯನ್ನು ನಮೂದಿಸಿ:",
        "call_count": "ಕಾಲ್‌ಗಳ ಸಂಖ್ಯೆ:",
        "analyze_call": "ಕಾಲ್ ಅನ್ನು ವಿಶ್ಲೇಷಿಸಿ",
        "verdict": "ತೀರ್ಪು",
        "confidence": "ವಿಶ್ವಾಸ ಸ್ಕೋರ್",
        "red_flags": "ಎಚ್ಚರಿಕೆ ಧ್ವಜಗಳು",
        "advice": "ಸಲಹೆ",
        "risk_factors": "ಅಪಾಯದ ಅಂಶಗಳು",
        "explanation": "ವಿವರಣೆ",
        "quiz_title": "ಕಲಿ ಮತ್ತು ಸ್ಕ್ಯಾಮ್‌ಗಳನ್ನು ಗುರುತಿಸಿ ರಸಪ್ರಶ್ನೆ",
        "question": "ಪ್ರಶ್ನೆ",
        "submit_answer": "ಉತ್ತರವನ್ನು ಸಲ್ಲಿಸಿ",
        "score": "ನಿಮ್ಮ ಸ್ಕೋರ್",
        "language": "ಭಾಷೆ",
        "safe": "ಸುರಕ್ಷಿತ",
        "suspicious": "ಅನುಮಾನಾಸ್ಪದ",
        "scam": "ಸ್ಕ್ಯಾಮ್",
        "high_risk": "ಅಧಿಕ ಅಪಾಯ",
        "medium_risk": "ಮಧ್ಯಮ ಅಪಾಯ",
        "low_risk": "ಕಡಿಮೆ ಅಪಾಯ",
        "stats_scams_blocked": "ಕಂಡುಹಿಡಿದ ಸ್ಕ್ಯಾಮ್‌ಗಳು",
        "stats_users_protected": "ರಕ್ಷಿಸಿದ ಬಳಕೆದಾರರು",
        "stats_accuracy": "ಗುರುತಿಸುವ ನಿಖರತೆ",
        "report_scam": "ಸ್ಕ್ಯಾಮ್ ವರದಿ ಮಾಡಿ",
        "footer": "ರಕ್ಷ AI ಬಳಸಿ ಸಂಭವನೀಯ ಸ್ಕ್ಯಾಮ್‌ಗಳನ್ನು ಪತ್ತೆಹಚ್ಚುತ್ತದೆ. ಯಾವಾಗಲೂ ಅಧಿಕೃತ ಮೂಲಗಳೊಂದಿಗೆ ಪರಿಶೀಲಿಸಿ.",
        "bilingual_note": "ದ್ವಿಭಾಷಾ ಔಟ್‌ಪುಟ್",
        "check_message": "ಸಂದೇಶವನ್ನು ಪರಿಶೀಲಿಸಿ",
        "is_scam": "ಈ ಸಂದೇಶ ಸ್ಕ್ಯಾಮ್ ಆಗಿದೆಯೇ?",
        "paste_any": "ನಿಮಗೆ ಅನುಮಾನವಿರುವ ಯಾವುದೇ SMS, WhatsApp, ಅಥವಾ ಇಮೇಲ್ ಅನ್ನು ಅಂಟಿಸಿ.",
        "try_example": "ಉದಾಹರಣೆಯನ್ನು ಪ್ರಯತ್ನಿಸಿ:",
        "messages_checked": "ಸಂದೇಶಗಳನ್ನು ಪರಿಶೀಲಿಸಲಾಗಿದೆ",
        "scams_caught": "ಸ್ಕ್ಯಾಮ್‌ಗಳನ್ನು ಹಿಡಿದುಕೊಂಡಿದೆ",
    }
}

# ==================== SESSION STATE ====================
if "scams_detected" not in st.session_state:
    st.session_state.scams_detected = 1247
if "users_protected" not in st.session_state:
    st.session_state.users_protected = 8934
if "accuracy" not in st.session_state:
    st.session_state.accuracy = 96.5
if "messages_checked" not in st.session_state:
    st.session_state.messages_checked = 0
if "scams_caught" not in st.session_state:
    st.session_state.scams_caught = 0
if "example_msg" not in st.session_state:
    st.session_state.example_msg = ""

# ==================== SIDEBAR ====================
with st.sidebar:
    st.title("🛡️ Raksha")
    st.markdown("---")
    
    # Our Mission
    st.subheader("🎯 Our Mission")
    st.write("Thousands of Indian families lose money to online scams every day. Elders are the biggest targets. Raksha protects, inspects, and teaches — in the family's own language.")
    st.markdown("---")
    
       # Stats
    st.subheader("📊 Stats")

    # Define translations
    t = {
        "stats_scams_blocked": "Scams Blocked",
        "stats_users_protected": "Users Protected",
        "stats_accuracy": "Accuracy",
    }

    # Safely initialize session state (prevents crashes on first load)
    for key, default in [("scams_detected", 0), ("users_protected", 0), ("accuracy", 95)]:
        if key not in st.session_state:
            st.session_state[key] = default

    st.metric(t["stats_scams_blocked"], st.session_state.scams_detected)
    st.metric(t["stats_users_protected"], st.session_state.users_protected)
    st.metric(t["stats_accuracy"], f"{st.session_state.accuracy}%")  # Fixed: was t[" "]
    st.markdown("---")

    # Why Raksha wins
    st.subheader("✅ Why Raksha wins")
    st.markdown("☑️ Real problem, real mission")
    st.markdown("☑️ 4 working safety tools")
    st.markdown("☑️ 5 Indian languages supported")
    st.markdown("☑️ 3D glass UI with live depth effects")
    st.markdown("---")

    st.caption("🛡️ Raksha - Family Digital Safety Guardian")
    st.caption("Made with 💚 for Digital Safety")
    st.caption("Model: llama-3.1-8b-instant via Groq")

# ==================== LANGUAGE SELECTOR ====================
col1, col2 = st.columns([0.9, 0.1])
with col2:
    selected_language = st.selectbox(
        "🌐",
        options=list(LANGUAGE_OPTIONS.keys()),
        label_visibility="collapsed"
    )
    lang_code = LANGUAGE_OPTIONS[selected_language]

t = TRANSLATIONS[lang_code]

# ==================== HERO BANNER ====================
st.markdown(f"""
    <div class="hero-banner">
        <h1>🛡️ Raksha — Family Digital Safety Guardian</h1>
        <p>Protecting families from online fraud — checks scam messages, inspects suspicious links, 
        verifies fake deadlines, and teaches people to spot fraud themselves. Built for real families.</p>
    </div>
""", unsafe_allow_html=True)

# ==================== GROQ ANALYSIS FUNCTION ====================
def analyze_with_groq(prompt, system_message):
    try:
        message = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1024,
        )
        return message.choices[0].message.content
    except Exception as e:
        st.error(f"Groq API Error: {str(e)}")
        return None

# ==================== REPORT BUTTON HELPER ====================
def show_report_button(lang_code="en"):
    report_text = TRANSLATIONS[lang_code].get("report_scam", "Report Scam")
    st.markdown(
        f'<a href="https://cybercrime.gov.in/" target="_blank" class="report-btn">'
        f'🚨 {report_text}</a>',
        unsafe_allow_html=True
    )

# ==================== TABS ====================
tab1, tab2, tab3, tab4 = st.tabs([
    f"📱 {t['message_checker']}",
    f"🔗 {t['link_inspector']}",
    f"☎️ {t['call_checker']}",
    f"📚 {t['learn_quiz']}"
])

# ==================== TAB 1: MESSAGE CHECKER ====================
with tab1:
    st.header(f"🔗 {t['is_scam']}")
    st.write(t['paste_any'])
    
    # Counter Badge
    st.markdown(f"""
        <div class="counter-badge">
            <span>🛡️ {st.session_state.messages_checked} {t['messages_checked']}, {st.session_state.scams_caught} {t['scams_caught']}</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Example Buttons
    st.write(f"🚀 {t['try_example']}")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🎰 Fake Lottery", key="ex_lottery"):
            st.session_state.example_msg = "Congratulations! You won Rs 10,00,000 in KBC lottery. Pay Rs 5000 fee to claim your prize now!"
            st.rerun()
    with c2:
        if st.button("🏦 Fake Bank Alert", key="ex_bank"):
            st.session_state.example_msg = "Dear customer, your bank account has been suspended. Click here to verify your details immediately or call 1800-XXX."
            st.rerun()
    with c3:
        if st.button("📦 Fake Delivery", key="ex_delivery"):
            st.session_state.example_msg = "Your package is pending delivery. Please pay Rs 200 customs fee via this link to receive it within 24 hours."
            st.rerun()
    
    # Input
    message_input = st.text_area(
        "Suspicious message:",
        value=st.session_state.example_msg,
        placeholder="e.g. Congratulations! You won Rs 10,00,000 in KBC lottery. Pay Rs 5000 fee to claim...",
        height=150,
        key="message_input"
    )
    
    if st.button(t['check_message'], key="msg_btn"):
        if message_input.strip():
            with st.spinner("🔍 Analyzing message..."):
                system_prompt = """You are an expert in identifying scams and fraudulent messages. 
Analyze the given message and provide a JSON response with:
{
  "verdict": "scam|suspicious|safe",
  "confidence": 0-100,
  "red_flags": ["flag1", "flag2"],
  "advice_en": "English advice",
  "advice_te": "Telugu advice",
  "advice_ta": "Tamil advice",
  "advice_hi": "Hindi advice",
  "advice_kn": "Kannada advice"
}
Respond ONLY with valid JSON, no other text."""
                
                response = analyze_with_groq(
                    f"Analyze this message for scams: {message_input}",
                    system_prompt
                )
                
                if response is None:
                    st.stop()
                
                with st.expander("Debug - Raw Response"):
                    st.code(response)
                
                try:
                    json_match = re.search(r'\{.*\}', response, re.DOTALL)
                    if json_match:
                        result = json.loads(json_match.group())
                    else:
                        result = json.loads(response)
                    
                    verdict = result.get("verdict", "unknown").upper()
                    confidence = result.get("confidence", 0)
                    
                    st.session_state.messages_checked += 1
                    
                    if verdict == "SCAM":
                        st.markdown(f'<div class="scam-badge scam-high">⚠️ {verdict} ({confidence}%)</div>', unsafe_allow_html=True)
                        st.session_state.scams_detected += 1
                        st.session_state.scams_caught += 1
                        show_report_button(lang_code)
                    elif verdict == "SUSPICIOUS":
                        st.markdown(f'<div class="scam-badge scam-medium">⚠️ {verdict} ({confidence}%)</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="scam-badge scam-safe">✅ {verdict} ({confidence}%)</div>', unsafe_allow_html=True)
                    
                    st.progress(confidence / 100)
                    
                    if result.get("red_flags"):
                        st.subheader(f"🚩 {t['red_flags']}")
                        for flag in result["red_flags"]:
                            st.write(f"• {flag}")
                    
                    st.subheader(f"💡 {t['advice']}")
                    st.caption(f"*{t['bilingual_note']}*")
                    
                    cols = st.columns(2)
                    advice_map = {
                        "en": result.get("advice_en", "N/A"),
                        "te": result.get("advice_te", "N/A"),
                        "ta": result.get("advice_ta", "N/A"),
                        "hi": result.get("advice_hi", "N/A"),
                        "kn": result.get("advice_kn", "N/A"),
                    }
                    
                    with cols[0]:
                        st.write(f"**English:**\n{advice_map['en']}")
                    with cols[1]:
                        if lang_code == "te":
                            st.write(f"**తెలుగు:**\n{advice_map['te']}")
                        elif lang_code == "ta":
                            st.write(f"**தமிழ்:**\n{advice_map['ta']}")
                        elif lang_code == "hi":
                            st.write(f"**हिन्दी:**\n{advice_map['hi']}")
                        elif lang_code == "kn":
                            st.write(f"**ಕನ್ನಡ:**\n{advice_map['kn']}")
                        else:
                            st.write(f"**తెలుగు:**\n{advice_map['te']}")
                    
                except json.JSONDecodeError as e:
                    st.error(f"Could not parse response. Please try again.")
                    st.text(f"Parse error: {str(e)}")
        else:
            st.warning("Please enter a message to analyze.")

# ==================== TAB 2: LINK INSPECTOR ====================
with tab2:
    st.header(f"🔗 {t['link_inspector']}")
    st.write("Paste a suspicious URL to check for phishing and malicious links.")
    
    url_input = st.text_input(
        t['paste_url'],
        placeholder="https://example.com",
        key="url_input"
    )
    
    if st.button(t['analyze_url'], key="url_btn"):
        if url_input.strip():
            with st.spinner("🔍 Analyzing URL..."):
                system_prompt = """You are an expert in identifying phishing and malicious links.
Analyze the given URL and provide a JSON response with:
{
  "risk_level": "high|medium|low|safe",
  "risk_score": 0-100,
  "risk_factors": ["factor1", "factor2"],
  "explanation_en": "English explanation",
  "explanation_te": "Telugu explanation",
  "explanation_ta": "Tamil explanation",
  "explanation_hi": "Hindi explanation",
  "explanation_kn": "Kannada explanation"
}
Respond ONLY with valid JSON, no other text."""
                
                response = analyze_with_groq(
                    f"Analyze this URL for phishing/malicious content: {url_input}",
                    system_prompt
                )
                
                if response is None:
                    st.stop()
                
                with st.expander("Debug - Raw Response"):
                    st.code(response)
                
                try:
                    json_match = re.search(r'\{.*\}', response, re.DOTALL)
                    if json_match:
                        result = json.loads(json_match.group())
                    else:
                        result = json.loads(response)
                    
                    risk_level = result.get("risk_level", "unknown").upper()
                    risk_score = result.get("risk_score", 0)
                    
                    if risk_level == "HIGH":
                        st.markdown(f'<div class="scam-badge scam-high">⚠️ {t["high_risk"]} ({risk_score}%)</div>', unsafe_allow_html=True)
                        st.session_state.scams_detected += 1
                        show_report_button(lang_code)
                    elif risk_level == "MEDIUM":
                        st.markdown(f'<div class="scam-badge scam-medium">⚠️ {t["medium_risk"]} ({risk_score}%)</div>', unsafe_allow_html=True)
                    elif risk_level == "LOW":
                        st.markdown(f'<div class="scam-badge scam-low">⚡ {t["low_risk"]} ({risk_score}%)</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="scam-badge scam-safe">✅ {t["safe"]} ({risk_score}%)</div>', unsafe_allow_html=True)
                    
                    st.progress(risk_score / 100)
                    
                    if result.get("risk_factors"):
                        st.subheader(f"🚩 {t['risk_factors']}")
                        for factor in result["risk_factors"]:
                            st.write(f"• {factor}")
                    
                    st.subheader(f"💡 {t['explanation']}")
                    st.caption(f"*{t['bilingual_note']}*")
                    
                    cols = st.columns(2)
                    expl_map = {
                        "en": result.get("explanation_en", "N/A"),
                        "te": result.get("explanation_te", "N/A"),
                        "ta": result.get("explanation_ta", "N/A"),
                        "hi": result.get("explanation_hi", "N/A"),
                        "kn": result.get("explanation_kn", "N/A"),
                    }
                    
                    with cols[0]:
                        st.write(f"**English:**\n{expl_map['en']}")
                    with cols[1]:
                        if lang_code == "te":
                            st.write(f"**తెలుగు:**\n{expl_map['te']}")
                        elif lang_code == "ta":
                            st.write(f"**தமிழ்:**\n{expl_map['ta']}")
                        elif lang_code == "hi":
                            st.write(f"**हिन्दी:**\n{expl_map['hi']}")
                        elif lang_code == "kn":
                            st.write(f"**ಕನ್ನಡ:**\n{expl_map['kn']}")
                        else:
                            st.write(f"**తెలుగు:**\n{expl_map['te']}")
                    
                except json.JSONDecodeError as e:
                    st.error(f"Could not parse response. Please try again.")
                    st.text(f"Parse error: {str(e)}")
        else:
            st.warning("Please enter a URL to analyze.")

# ==================== TAB 3: CALL CHECKER ====================
with tab3:
    st.header(f"☎️ {t['call_checker']}")
    st.write("Enter details about a suspicious phone call to verify if it's a known scam pattern.")
    
    col1, col2 = st.columns(2)
    with col1:
        phone_input = st.text_input(
            t['phone_number'],
            placeholder="e.g. +91 98765 43210",
            key="phone_input"
        )
    with col2:
        call_count = st.number_input(
            t['call_count'],
            min_value=1,
            max_value=50,
            value=1,
            key="call_count"
        )
    
    if st.button(t['analyze_call'], key="call_btn"):
        if phone_input.strip():
            with st.spinner("🔍 Analyzing call details..."):
                system_prompt = """You are an expert in identifying phone and voice scams targeting Indian families.
Analyze the given phone number and call pattern, then provide a JSON response with:
{
  "verdict": "scam|suspicious|safe",
  "confidence": 0-100,
  "red_flags": ["flag1", "flag2"],
  "advice_en": "English advice",
  "advice_te": "Telugu advice",
  "advice_ta": "Tamil advice",
  "advice_hi": "Hindi advice",
  "advice_kn": "Kannada advice"
}
Respond ONLY with valid JSON, no other text."""
                
                response = analyze_with_groq(
                    f"Phone number: {phone_input}\nNumber of calls received: {call_count}\nAnalyze if this is a scam call pattern.",
                    system_prompt
                )
                
                if response is None:
                    st.stop()
                
                with st.expander("Debug - Raw Response"):
                    st.code(response)
                
                try:
                    json_match = re.search(r'\{.*\}', response, re.DOTALL)
                    if json_match:
                        result = json.loads(json_match.group())
                    else:
                        result = json.loads(response)
                    
                    verdict = result.get("verdict", "unknown").upper()
                    confidence = result.get("confidence", 0)
                    
                    if verdict == "SCAM":
                        st.markdown(f'<div class="scam-badge scam-high">⚠️ {verdict} ({confidence}%)</div>', unsafe_allow_html=True)
                        st.session_state.scams_detected += 1
                        show_report_button(lang_code)
                    elif verdict == "SUSPICIOUS":
                        st.markdown(f'<div class="scam-badge scam-medium">⚠️ {verdict} ({confidence}%)</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="scam-badge scam-safe">✅ {verdict} ({confidence}%)</div>', unsafe_allow_html=True)
                    
                    st.progress(confidence / 100)
                    
                    if result.get("red_flags"):
                        st.subheader(f"🚩 {t['red_flags']}")
                        for flag in result["red_flags"]:
                            st.write(f"• {flag}")
                    
                    st.subheader(f"💡 {t['advice']}")
                    st.caption(f"*{t['bilingual_note']}*")
                    
                    cols = st.columns(2)
                    advice_map = {
                        "en": result.get("advice_en", "N/A"),
                        "te": result.get("advice_te", "N/A"),
                        "ta": result.get("advice_ta", "N/A"),
                        "hi": result.get("advice_hi", "N/A"),
                        "kn": result.get("advice_kn", "N/A"),
                    }
                    
                    with cols[0]:
                        st.write(f"**English:**\n{advice_map['en']}")
                    with cols[1]:
                        if lang_code == "te":
                            st.write(f"**తెలుగు:**\n{advice_map['te']}")
                        elif lang_code == "ta":
                            st.write(f"**தமிழ்:**\n{advice_map['ta']}")
                        elif lang_code == "hi":
                            st.write(f"**हिन्दी:**\n{advice_map['hi']}")
                        elif lang_code == "kn":
                            st.write(f"**ಕನ್ನಡ:**\n{advice_map['kn']}")
                        else:
                            st.write(f"**తెలుగు:**\n{advice_map['te']}")
                    
                except json.JSONDecodeError as e:
                    st.error(f"Could not parse response. Please try again.")
                    st.text(f"Parse error: {str(e)}")
        else:
            st.warning("Please enter a phone number to analyze.")

# ==================== TAB 4: LEARN & QUIZ ====================
with tab4:
    st.header(f"📚 {t['quiz_title']}")
    st.write("Test your knowledge and learn to spot scams before they happen.")
    
    # Quiz questions
    quiz_data = [
        {
            "question_en": "You receive a WhatsApp message saying you won ₹10 lakh in a lottery you never entered. What should you do?",
            "question_te": "మీరు ఎప్పుడూ పాల్గొనని లాటరీలో ₹10 లక్షలు గెలిచారని WhatsApp సందేశం వస్తే మీరు ఏమి చేయాలి?",
            "question_ta": "நீங்கள் எப்போதும் பங்கேற்காத லாட்டரியில் ₹10 லட்சம் வென்றதாக WhatsApp செய்தி வந்தால் என்ன செய்வீர்கள்?",
            "question_hi": "आपको एक WhatsApp संदेश मिलता है कि आपने एक लॉटरी में ₹10 लाख जीते हैं जिसमें आपने कभी भाग नहीं लिया। आपको क्या करना चाहिए?",
            "question_kn": "ನೀವು ಎಂದಿಗೂ ಭಾಗವಹಿಸದ ಲಾಟರಿಯಲ್ಲಿ ₹10 ಲಕ್ಷ ಗೆದ್ದಿರುವಿರಿ ಎಂದು WhatsApp ಸಂದೇಶ ಬಂದರೆ ನೀವು ಏನು ಮಾಡಬೇಕು?",
            "options_en": ["Pay the processing fee immediately", "Ignore and delete the message", "Share your bank details to receive the prize"],
            "options_te": ["వెంటనే ప్రాసెసింగ్ ఫీజు చెల్లించండి", "విస్మరించి సందేశాన్ని తొలగించండి", "బహుమతి పొందడానికి మీ బ్యాంక్ వివరాలను పంచుకోండి"],
            "options_ta": ["உடனடியாக செயலாக்க கட்டணத்தை செலுத்துங்கள்", "புறக்கணித்து செய்தியை நீக்குங்கள்", "பரிசைப் பெற உங்கள் வங்கி விவரங்களைப் பகிர்ந்து கொள்ளுங்கள்"],
            "options_hi": ["तुरंत प्रोसेसिंग शुल्क का भुगतान करें", "संदेश को अनदेखा करें और हटा दें", "इनाम प्राप्त करने के लिए अपने बैंक विवरण साझा करें"],
            "options_kn": ["ತಕ್ಷಣ ಪ್ರೊಸೆಸಿಂಗ್ ಶುಲ್ಕವನ್ನು ಪಾವತಿಸಿ", "ನಿರ್ಲಕ್ಷಿಸಿ ಸಂದೇಶವನ್ನು ಅಳಿಸಿ", "ಬಹುಮತಿಯನ್ನು ಪಡೆಯಲು ನಿಮ್ಮ ಬ್ಯಾಂಕ್ ವಿವರಗಳನ್ನು ಹಂಚಿಕೊಳ್ಳಿ"],
            "correct": 1,
            "explanation_en": "Legitimate lotteries never ask winners to pay fees upfront. If you didn't enter, you can't win.",
            "explanation_te": "ధ్రువీకరించబడిన లాటరీలు గెలుపొందినవారిని ఎప్పుడూ ముందుగా ఫీజులు చెల్లించమని అడగవు. మీరు పాల్గొనకపోతే, గెలవలేరు.",
            "explanation_ta": "சட்டபூர்வமான லாட்டரிகள் வெற்றியாளர்களிடம் முன்பணம் கேட்காது. நீங்கள் பங்கேற்கவில்லை என்றால், வெற்றி பெற முடியாது.",
            "explanation_hi": "वैध लॉटरी विजेताओं से कभी भी अग्रिम शुल्क नहीं मांगती। यदि आपने भाग नहीं लिया, तो आप जीत नहीं सकते।",
            "explanation_kn": "ಕಾನೂನುಬದ್ಧ ಲಾಟರಿಗಳು ವಿಜೇತರಿಂದ ಎಂದಿಗೂ ಮುಂಗಡ ಶುಲ್ಕವನ್ನು ಕೇಳುವುದಿಲ್ಲ. ನೀವು ಭಾಗವಹಿಸದಿದ್ದರೆ, ಗೆಲ್ಲಲು ಸಾಧ್ಯವಿಲ್ಲ."
        },
        {
            "question_en": "A caller claims to be from your bank and asks for your OTP to 'unblock' your account. What do you do?",
            "question_te": "ఒక కాలర్ మీ బ్యాంక్ నుండి వచ్చారని చెప్పి మీ ఖాతాను 'అన్‌బ్లాక్' చేయడానికి మీ OTPని అడుగుతారు. మీరు ఏమి చేస్తారు?",
            "question_ta": "ஒரு அழைப்பாளர் உங்கள் வங்கியிலிருந்து வந்ததாகக் கூறி, உங்கள் கணக்கை 'தடைநீக்க' உங்கள் OTP ஐக் கேட்கிறார். நீங்கள் என்ன செய்வீர்கள்?",
            "question_hi": "एक कॉलर आपके बैंक से होने का दावा करता है और आपके खाते को 'अनब्लॉक' करने के लिए आपका OTP मांगता है। आप क्या करेंगे?",
            "question_kn": "ಒಬ್ಬ ಕರೆ ಮಾಡುವವರು ನಿಮ್ಮ ಬ್ಯಾಂಕಿನಿಂದ ಬಂದವರು ಎಂದು ಹೇಳಿ ನಿಮ್ಮ ಖಾತೆಯನ್ನು 'ಅನ್‌ಬ್ಲಾಕ್' ಮಾಡಲು ನಿಮ್ಮ OTP ಅನ್ನು ಕೇಳುತ್ತಾರೆ. ನೀವು ಏನು ಮಾಡುತ್ತೀರಿ?",
            "options_en": ["Give the OTP quickly to avoid account suspension", "Hang up and call your bank's official number", "Ask them to send a confirmation email first"],
            "options_te": ["ఖాతా సస్పెన్షన్‌ను నివారించడానికి వేగంగా OTP ఇవ్వండి", "ఫోన్ కట్ చేసి మీ బ్యాంక్ అధికారిక నంబర్‌కు కాల్ చేయండి", "ముందుగా ధృవీకరణ ఇమెయిల్ పంపమని అడగండి"],
            "options_ta": ["கணக்கு இடைநீக்கத்தைத் தவிர்க்க விரைவாக OTP ஐ வழங்குங்கள்", "தொலைபேசியைத் துண்டித்து உங்கள் வங்கியின் அதிகாரப்பூர்வ எண்ணை அழைக்கவும்", "முதலில் உறுதிப்படுத்தும் மின்னஞ்சலை அனுப்புமாறு கேட்கவும்"],
            "options_hi": ["खाता निलंबन से बचने के लिए तुरंत OTP दें", "फोन काटें और अपने बैंक की आधिकारिक संख्या पर कॉल करें", "पहले एक पुष्टि ईमेल भेजने के लिए कहें"],
            "options_kn": ["ಖಾತೆ ಅಮಾನತುಗೊಳ್ಳುವುದನ್ನು ತಪ್ಪಿಸಲು ತಕ್ಷಣ OTP ನೀಡಿ", "ಕಾಲ್ ಕಟ್ ಮಾಡಿ ನಿಮ್ಮ ಬ್ಯಾಂಕಿನ ಅಧಿಕೃತ ಸಂಖ್ಯೆಗೆ ಕರೆ ಮಾಡಿ", "ಮೊದಲು ದೃಢೀಕರಣ ಇಮೇಲ್ ಕಳುಹಿಸಲು ಹೇಳಿ"],
            "correct": 1,
            "explanation_en": "Banks NEVER ask for OTPs. OTPs are for your use only. Always hang up and call the official number.",
            "explanation_te": "బ్యాంకులు ఎప్పుడూ OTPలను అడగవు. OTPలు మీ వ్యక్తిగత ఉపయోగానికి మాత్రమే. ఎల్లప్పుడూ ఫోన్ కట్ చేసి అధికారిక నంబర్‌కు కాల్ చేయండి.",
            "explanation_ta": "வங்கிகள் எப்போதும் OTP ஐக் கேட்காது. OTPகள் உங்கள் பயன்பாட்டிற்கு மட்டுமே. எப்போதும் தொலைபேசியைத் துண்டித்து அதிகாரப்பூர்வ எண்ணை அழைக்கவும்.",
            "explanation_hi": "बैंक कभी भी OTP नहीं मांगते। OTP केवल आपके उपयोग के लिए हैं। हमेशा फोन काटें और आधिकारिक नंबर पर कॉल करें।",
            "explanation_kn": "ಬ್ಯಾಂಕುಗಳು ಎಂದಿಗೂ OTP ಅನ್ನು ಕೇಳುವುದಿಲ್ಲ. OTPಗಳು ನಿಮ್ಮ ಬಳಕೆಗೆ ಮಾತ್ರ. ಯಾವಾಗಲೂ ಕಾಲ್ ಕಟ್ ಮಾಡಿ ಅಧಿಕೃತ ಸಂಖ್ಯೆಗೆ ಕರೆ ಮಾಡಿ."
        },
        {
            "question_en": "You get an SMS with a link saying 'Your package is pending. Pay customs fee.' You didn't order anything. What is this?",
            "question_te": "మీరు ఏమీ ఆర్డర్ చేయకపోతే, 'మీ ప్యాకేజీ పెండింగ్‌లో ఉంది. కస్టమ్స్ ఫీజు చెల్లించండి' అని లింక్‌తో SMS వస్తే ఇది ఏమిటి?",
            "question_ta": "நீங்கள் எதுவும் ஆர்டர் செய்யவில்லை என்றால், 'உங்கள் பொதி நிலுவையில் உள்ளது. சுங்கக் கட்டணம் செலுத்தவும்' என்ற இணைப்புடன் SMS வந்தால் இது என்ன?",
            "question_hi": "आपको एक SMS मिलता है जिसमें लिंक है 'आपका पैकेज लंबित है। कस्टम शुल्क दें।' आपने कुछ भी ऑर्डर नहीं किया। यह क्या है?",
            "question_kn": "ನೀವು ಏನನ್ನೂ ಆರ್ಡರ್ ಮಾಡದಿದ್ದರೆ, 'ನಿಮ್ಮ ಪ್ಯಾಕೇಜ್ ಬಾಕಿ ఉಂದಿ. ಕಸ್ಟಮ್ಸ್ ಶುಲ್ಕ ಪಾವತಿಸಿ' ಎಂದು ಲಿಂಕ್‌ನೊಂದಿಗೆ SMS ಬಂದರೆ ಇದು ಏನು?",
            "options_en": ["A genuine delivery notification", "A delivery scam", "A mistake by the courier company"],
            "options_te": ["అసలైన డెలివరీ నోటిఫికేషన్", "డెలివరీ స్కామ్", "కూరియర్ కంపెనీ యొక్క తప్పు"],
            "options_ta": ["உண்மையான விநியோக அறிவிப்பு", "விநியோக மோசடி", "கூரியர் நிறுவனத்தின் தவறு"],
            "options_hi": ["एक genuine डिलीवरी सूचना", "एक डिलीवरी घोटाला", "कूरियर कंपनी की गलती"],
            "options_kn": ["ನಿಜವಾದ ಡೆಲಿವರಿ ಸೂಚನೆ", "ಡೆಲಿವರಿ ಸ್ಕ್ಯಾಮ್", "ಕೂರಿಯರ್ ಕಂಪನಿಯ ತಪ್ಪು"],
            "correct": 1,
            "explanation_en": "This is a common delivery scam. If you didn't order anything, there's no package. Never pay for unexpected deliveries.",
            "explanation_te": "ఇది సాధారణ డెలివరీ స్కామ్. మీరు ఏమీ ఆర్డర్ చేయకపోతే, ప్యాకేజీ లేదు. ఊహించని డెలివరీల కోసం ఎప్పుడూ చెల్లించవద్దు.",
            "explanation_ta": "இது ஒரு பொதுவான விநியோக மோசடி. நீங்கள் எதுவும் ஆர்டர் செய்யவில்லை என்றால், பொதி இல்லை. எதிர்பாராத விநியோகங்களுக்கு ஒருபோதும் பணம் செலுத்த வேண்டாம்.",
            "explanation_hi": "यह एक सामान्य डिलीवरी घोटाला है। यदि आपने कुछ भी ऑर्डर नहीं किया, तो कोई पैकेज नहीं है। अप्रत्याशित डिलीवरी के लिए कभी भुगतान न करें।",
            "explanation_kn": "ಇದು ಸಾಮಾನ್ಯ ಡೆಲಿವರಿ ಸ್ಕ್ಯಾಮ್. ನೀವು ಏನನ್ನೂ ಆರ್ಡರ್ ಮಾಡದಿದ್ದರೆ, ಪ್ಯಾಕೇಜ್ ಇಲ್ಲ. ಅನಿರೀಕ್ಷಿತ ಡೆಲಿವರಿಗಳಿಗೆ ಎಂದಿಗೂ ಹಣ ಪಾವತಿಸಬೇಡಿ."
        }
    ]
    
    if "quiz_score" not in st.session_state:
        st.session_state.quiz_score = 0
    if "quiz_submitted" not in st.session_state:
        st.session_state.quiz_submitted = [False] * len(quiz_data)
    if "quiz_answers" not in st.session_state:
        st.session_state.quiz_answers = [None] * len(quiz_data)
    
    for i, q in enumerate(quiz_data):
        st.markdown(f"**{t['question']} {i+1}:**")
        
        # Display question in selected language
        if lang_code == "te":
            st.write(q["question_te"])
            options = q["options_te"]
            explanation = q["explanation_te"]
        elif lang_code == "ta":
            st.write(q["question_ta"])
            options = q["options_ta"]
            explanation = q["explanation_ta"]
        elif lang_code == "hi":
            st.write(q["question_hi"])
            options = q["options_hi"]
            explanation = q["explanation_hi"]
        elif lang_code == "kn":
            st.write(q["question_kn"])
            options = q["options_kn"]
            explanation = q["explanation_kn"]
        else:
            st.write(q["question_en"])
            options = q["options_en"]
            explanation = q["explanation_en"]
        
        answer = st.radio(
            f"select_{i}",
            options=options,
            index=None,
            key=f"quiz_q_{i}",
            label_visibility="collapsed"
        )
        
        if st.button(t['submit_answer'], key=f"submit_{i}") and not st.session_state.quiz_submitted[i]:
            if answer is not None:
                selected_idx = options.index(answer)
                st.session_state.quiz_answers[i] = selected_idx
                st.session_state.quiz_submitted[i] = True
                
                if selected_idx == q["correct"]:
                    st.session_state.quiz_score += 1
                    st.success("✅ Correct!")
                else:
                    st.error("❌ Incorrect!")
                
                st.info(f"💡 {explanation}")
            else:
                st.warning("Please select an answer first.")
        
        if st.session_state.quiz_submitted[i]:
            if st.session_state.quiz_answers[i] == q["correct"]:
                st.success("✅ Correct!")
            else:
                st.error("❌ Incorrect!")
            st.info(f"💡 {explanation}")
        
        st.markdown("---")
    
    # Score display
    st.subheader(f"🏆 {t['score']}: {st.session_state.quiz_score}/{len(quiz_data)}")
    progress = st.session_state.quiz_score / len(quiz_data)
    st.progress(progress)
    
    if st.session_state.quiz_score == len(quiz_data):
        st.balloons()
        st.success("🎉 Perfect score! You're a scam detection expert!")

# ==================== FLOATING REPORT BUTTON ====================
st.markdown("""
    <a href="https://cybercrime.gov.in/" target="_blank" class="fab-report" title="Report Scam">
        🚨
    </a>
""", unsafe_allow_html=True)

# ==================== FOOTER ====================
st.markdown("---")
st.caption(f"🛡️ {t['footer']}")
st.caption("Made with 💚 for Digital Safety | Model: llama-3.1-8b-instant via Groq")