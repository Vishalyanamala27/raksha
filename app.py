import streamlit as st
import os
from groq import Groq
import json
import re

# Page Configuration
st.set_page_config(
    page_title="Raksha - Digital Safety Guardian",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] button {
        font-size: 16px;
        font-weight: 600;
    }
    .scam-badge {
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        font-weight: 600;
        display: inline-block;
        margin: 0.5rem 0;
    }
    .scam-high {
        background-color: #fee2e2;
        color: #991b1b;
    }
    .scam-medium {
        background-color: #fef3c7;
        color: #92400e;
    }
    .scam-low {
        background-color: #dcfce7;
        color: #15803d;
    }
    .scam-safe {
        background-color: #d1fae5;
        color: #065f46;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Groq Client
@st.cache_resource
def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        st.error("❌ GROQ_API_KEY not found. Please set it in your environment variables.")
        st.stop()
    return Groq(api_key=api_key)

client = get_groq_client()

# Translations
TRANSLATIONS = {
    "en": {
        "title": "🛡️ Raksha - Family Digital Safety Guardian",
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
    },
    "te": {
        "title": "🛡️ రక్ష - కుటుంబ డిజిటల్ సేఫ్టీ గార్డియన్",
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
    }
}

# Language Selection
col1, col2 = st.columns([0.9, 0.1])
with col2:
    language = st.selectbox("🌐", ["English", "Telugu"], label_visibility="collapsed")
    lang_code = "en" if language == "English" else "te"

t = TRANSLATIONS[lang_code]

# Header
st.markdown(f"# {t['title']}")
st.markdown(f"*{t['subtitle']}*")
st.divider()

# Stats
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Safety", "100%", "✅")
with col2:
    st.metric("Availability", "24/7", "⏰")
with col3:
    st.metric("Cost", "Free", "∞")

st.divider()

# Function to analyze with Groq
def analyze_with_groq(prompt, system_message):
    """Call Groq API for analysis"""
    try:
        message = client.chat.completions.create(
            model="llama3-8b-8192",  # Updated model
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

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    f"📱 {t['message_checker']}",
    f"🔗 {t['link_inspector']}",
    f"☎️ {t['call_checker']}",
    f"📚 {t['learn_quiz']}"
])

# ==================== TAB 1: MESSAGE CHECKER ====================
with tab1:
    st.header(f"📱 {t['message_checker']}")
    st.write("Paste a suspicious SMS, WhatsApp, or email message to check if it's a scam.")
    
    message_input = st.text_area(
        t['paste_message'],
        placeholder="Enter suspicious message here...",
        height=150,
        key="message_input"
    )
    
    if st.button(t['analyze_btn'], key="msg_btn"):
        if message_input.strip():
            with st.spinner("🔍 Analyzing message..."):
                system_prompt = """You are an expert in identifying scams and fraudulent messages. 
Analyze the given message and provide a JSON response with:
{
  "verdict": "scam|suspicious|safe",
  "confidence": 0-100,
  "red_flags": ["flag1", "flag2"],
  "advice_en": "English advice",
  "advice_te": "Telugu advice"
}
Respond ONLY with valid JSON, no other text."""
                
                response = analyze_with_groq(
                    f"Analyze this message for scams: {message_input}",
                    system_prompt
                )
                
                if response is None:
                    st.stop()
                
                # Debug: show raw response
                with st.expander("Debug - Raw Response"):
                    st.code(response)
                
                try:
                    # Extract JSON from response
                    json_match = re.search(r'\{.*\}', response, re.DOTALL)
                    if json_match:
                        result = json.loads(json_match.group())
                    else:
                        result = json.loads(response)
                    
                    # Display Results
                    verdict = result.get("verdict", "unknown").upper()
                    confidence = result.get("confidence", 0)
                    
                    # Verdict Badge
                    if verdict == "SCAM":
                        st.markdown(f'<div class="scam-badge scam-high">⚠️ {verdict} ({confidence}%)</div>', unsafe_allow_html=True)
                    elif verdict == "SUSPICIOUS":
                        st.markdown(f'<div class="scam-badge scam-medium">⚠️ {verdict} ({confidence}%)</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="scam-badge scam-safe">✅ {verdict} ({confidence}%)</div>', unsafe_allow_html=True)
                    
                    # Confidence Score
                    st.progress(confidence / 100)
                    
                    # Red Flags
                    if result.get("red_flags"):
                        st.subheader(f"🚩 {t['red_flags']}")
                        for flag in result["red_flags"]:
                            st.write(f"• {flag}")
                    
                    # Advice
                    st.subheader(f"💡 {t['advice']}")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**English:**\n{result.get('advice_en', 'N/A')}")
                    with col2:
                        st.write(f"**Telugu:**\n{result.get('advice_te', 'N/A')}")
                    
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
  "explanation_te": "Telugu explanation"
}
Respond ONLY with valid JSON, no other text."""
                
                response = analyze_with_groq(
                    f"Analyze this URL for phishing and scam risks: {url_input}",
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
                    
                    # Risk Badge
                    if risk_level == "HIGH":
                        st.markdown(f'<div class="scam-badge scam-high">⚠️ {risk_level} RISK ({risk_score}%)</div>', unsafe_allow_html=True)
                    elif risk_level == "MEDIUM":
                        st.markdown(f'<div class="scam-badge scam-medium">⚠️ {risk_level} RISK ({risk_score}%)</div>', unsafe_allow_html=True)
                    elif risk_level == "LOW":
                        st.markdown(f'<div class="scam-badge scam-low">⚠️ {risk_level} RISK ({risk_score}%)</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="scam-badge scam-safe">✅ SAFE ({risk_score}%)</div>', unsafe_allow_html=True)
                    
                    # Risk Score
                    st.progress(risk_score / 100)
                    
                    # Risk Factors
                    if result.get("risk_factors"):
                        st.subheader(f"🚩 {t['risk_factors']}")
                        for factor in result["risk_factors"]:
                            st.write(f"• {factor}")
                    
                    # Explanation
                    st.subheader(f"📖 {t['explanation']}")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**English:**\n{result.get('explanation_en', 'N/A')}")
                    with col2:
                        st.write(f"**Telugu:**\n{result.get('explanation_te', 'N/A')}")
                    
                except json.JSONDecodeError as e:
                    st.error("Could not parse response. Please try again.")
                    st.text(f"Parse error: {str(e)}")
        else:
            st.warning("Please enter a URL to analyze.")

# ==================== TAB 3: CALL CHECKER ====================
with tab3:
    st.header(f"☎️ {t['call_checker']}")
    st.write("Enter a phone number to check if it's associated with scam calls.")
    
    col1, col2 = st.columns(2)
    with col1:
        phone_input = st.text_input(
            t['phone_number'],
            placeholder="+1-800-SCAMMER",
            key="phone_input"
        )
    with col2:
        call_count = st.number_input(
            t['call_count'],
            min_value=0,
            max_value=100,
            value=0,
            key="call_count_input"
        )
    
    if st.button(t['analyze_call'], key="call_btn"):
        if phone_input.strip():
            with st.spinner("🔍 Analyzing call..."):
                system_prompt = """You are an expert in identifying phone scams and spam calls.
Analyze the given phone number and call details. Provide a JSON response with:
{
  "verdict": "scam|suspicious|safe",
  "confidence": 0-100,
  "call_risk": "high|medium|low",
  "risk_factors": ["factor1", "factor2"],
  "advice_en": "English advice",
  "advice_te": "Telugu advice"
}
Respond ONLY with valid JSON, no other text."""
                
                response = analyze_with_groq(
                    f"Analyze this phone call for scams: Phone: {phone_input}, Calls: {call_count}",
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
                    call_risk = result.get("call_risk", "medium")
                    
                    # Verdict Badge
                    if verdict == "SCAM":
                        st.markdown(f'<div class="scam-badge scam-high">⚠️ {verdict} ({confidence}%)</div>', unsafe_allow_html=True)
                    elif verdict == "SUSPICIOUS":
                        st.markdown(f'<div class="scam-badge scam-medium">⚠️ {verdict} ({confidence}%)</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="scam-badge scam-safe">✅ {verdict} ({confidence}%)</div>', unsafe_allow_html=True)
                    
                    # Risk Level
                    st.write(f"**Call Risk Level:** {call_risk.upper()}")
                    st.progress(confidence / 100)
                    
                    # Risk Factors
                    if result.get("risk_factors"):
                        st.subheader(f"🚩 {t['risk_factors']}")
                        for factor in result["risk_factors"]:
                            st.write(f"• {factor}")
                    
                    # Advice
                    st.subheader(f"💡 {t['advice']}")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**English:**\n{result.get('advice_en', 'N/A')}")
                    with col2:
                        st.write(f"**Telugu:**\n{result.get('advice_te', 'N/A')}")
                    
                except json.JSONDecodeError as e:
                    st.error("Could not parse response. Please try again.")
                    st.text(f"Parse error: {str(e)}")
        else:
            st.warning("Please enter a phone number to analyze.")

# ==================== TAB 4: LEARN & QUIZ ====================
with tab4:
    st.header(f"📚 {t['learn_quiz']}")
    st.write("Test your knowledge about common scams and learn how to spot them!")
    
    # Quiz Questions
    quiz_questions = [
        {
            "question_en": "What is a common phishing tactic?",
            "question_te": "సాధారణ ఫిషింగ్ కౌశల్యం ఏమిటి?",
            "options": ["Urgent requests for personal info", "Legitimate bank emails", "Official website links", "Verified phone calls"],
            "correct": 0,
            "explanation_en": "Phishers create urgency to trick users into sharing sensitive data.",
            "explanation_te": "ఫిషర్‌లు సంవేదనశీల డేటా పంచుకోవడానికి ఆత్రుత సృష్టిస్తారు."
        },
        {
            "question_en": "How to identify a fake website?",
            "question_te": "నకిలీ వెబ్‌సైట్‌ను ఎలా గుర్తించాలి?",
            "options": ["Check for HTTPS", "Look for spelling errors in URL", "Verify company details", "All of the above"],
            "correct": 3,
            "explanation_en": "All methods help identify fake websites. Always verify before entering data.",
            "explanation_te": "నకిలీ వెబ్‌సైట్‌లను గుర్తించడానికి అన్ని పద్ధతులు సహాయపడతాయి."
        },
        {
            "question_en": "What should you do if you receive a suspicious call?",
            "question_te": "అనుమానాస్పదమైన కాల్ అందిస్తే ఏమి చేయాలి?",
            "options": ["Answer and ask questions", "Hang up immediately", "Ask for verification", "Both B and C"],
            "correct": 3,
            "explanation_en": "Never share personal info. Hang up and verify through official channels.",
            "explanation_te": "వ్యక్తిగత సమాచారం ఎప్పుడూ పంచుకోవద్దు. అధికారిక చానెల్‌ల ద్వారా ధృవీకరించండి."
        },
    ]
    
    # Initialize session state
    if 'quiz_started' not in st.session_state:
        st.session_state.quiz_started = False
        st.session_state.quiz_score = 0
        st.session_state.quiz_question_idx = 0
        st.session_state.quiz_answers = []
        st.session_state.submitted = False
    
    if not st.session_state.quiz_started:
        if st.button("🎯 Start Quiz", key="start_quiz"):
            st.session_state.quiz_started = True
            st.rerun()
    else:
        if st.session_state.quiz_question_idx < len(quiz_questions):
            q = quiz_questions[st.session_state.quiz_question_idx]
            question = q['question_en'] if lang_code == 'en' else q['question_te']
            
            st.write(f"**{t['question']} {st.session_state.quiz_question_idx + 1}/{len(quiz_questions)}**")
            st.write(question)
            
            if not st.session_state.submitted:
                answer = st.radio(
                    "Select your answer:",
                    q['options'],
                    key=f"q_{st.session_state.quiz_question_idx}"
                )
                
                if st.button(t['submit_answer'], key=f"submit_{st.session_state.quiz_question_idx}"):
                    selected_idx = q['options'].index(answer)
                    if selected_idx == q['correct']:
                        st.session_state.quiz_score += 1
                        st.success("✅ Correct!")
                    else:
                        st.error(f"❌ Wrong! Correct answer: {q['options'][q['correct']]}")
                    
                    explanation = q['explanation_en'] if lang_code == 'en' else q['explanation_te']
                    st.info(f"📖 {explanation}")
                    
                    st.session_state.quiz_answers.append(selected_idx == q['correct'])
                    st.session_state.submitted = True
                    st.rerun()
            else:
                explanation = q['explanation_en'] if lang_code == 'en' else q['explanation_te']
                if st.session_state.quiz_answers[-1]:
                    st.success("✅ Correct!")
                else:
                    st.error(f"❌ Wrong! Correct answer: {q['options'][q['correct']]}")
                st.info(f"📖 {explanation}")
                
                if st.button("Next Question →", key="next_q"):
                    st.session_state.quiz_question_idx += 1
                    st.session_state.submitted = False
                    st.rerun()
        else:
            st.success(f"🎉 Quiz Complete!")
            percentage = (st.session_state.quiz_score / len(quiz_questions)) * 100
            st.metric(t['score'], f"{st.session_state.quiz_score}/{len(quiz_questions)} ({percentage:.0f}%)")
            
            if st.button("🔄 Restart Quiz"):
                st.session_state.quiz_started = False
                st.session_state.quiz_score = 0
                st.session_state.quiz_question_idx = 0
                st.session_state.quiz_answers = []
                st.session_state.submitted = False
                st.rerun()

# Footer
st.divider()
st.markdown("""
    <div style='text-align: center; color: gray; font-size: 12px;'>
    🛡️ <b>Raksha - Family Digital Safety Guardian</b><br>
    Made with 💚 for Digital Safety<br>
    Powered by Groq AI
    </div>
""", unsafe_allow_html=True)