        "parse_error": "ಪ್ರತಿಕ್ರಿಯೆಯನ್ನು ಓದಲು ಸಾಧ್ಯವಾಗಲಿಲ್ಲ. ದಯವಿಟ್ಟು ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.",
        "enter_message": "ವಿಶ್ಲೇಷಿಸಲು ಸಂದೇಶವನ್ನು ನಮೂದಿಸಿ.",
        "enter_url": "ವಿಶ್ಲೇಷಿಸಲು URL ಅನ್ನು ನಮೂದಿಸಿ.",
        "enter_phone": "ವಿಶ್ಲೇಷಿಸಲು ಫೋನ್ ಸಂಖೆಯನ್ನು ನಮೂದಿಸಿ.",
        "safe_label": "ಸುರಕ್ಷಿತ",
        "suspicious_label": "ಅನುಮಾನಾಸ್ಪದ",
        "scam_label": "ಸ್ಕ್ಯಾಮ್",
        "english": "ಆಂಗ್ಲ",
        "report": "ಸ್ಕ್ಯಾಮ್ ವರದಿ ಮಾಡಿ",
        "footer_model": "ಡಿಜಿಟಲ್ ಸುರಕ್ಷತೆಗಾಗಿ 💚 ನಿರ್ಮಿಸಲಾಗಿದೆ | ಮಾದರಿ: llama-3.1-8b-instant via Groq"
    }
}

# ==================== SESSION STATE ====================
if "messages_checked" not in st.session_state:
    st.session_state.messages_checked = 1274
if "scams_caught" not in st.session_state:
    st.session_state.scams_caught = 342
if "language" not in st.session_state:
    st.session_state.language = "en"
if "example_msg" not in st.session_state:
    st.session_state.example_msg = ""

# ==================== HELPER FUNCTIONS ====================
def get_text(key):
    """Fetch translated text for the currently selected language."""
    lang = st.session_state.language
    if key in UI_TRANSLATIONS.get(lang, {}):
        return UI_TRANSLATIONS[lang][key]
    if key in TRANSLATIONS.get(lang, {}):
        return TRANSLATIONS[lang][key]
    # Fallback to English
    return UI_TRANSLATIONS["en"].get(key, TRANSLATIONS["en"].get(key, key))

def get_telecom_info(phone_number):
    """Simulated telecom lookup. Replace with real API in production."""
    # This is a mock implementation for demonstration
    return {
        "valid": True,
        "carrier": "Jio / Airtel / Vi",
        "line_type": "Mobile",
        "line_status": "Active",
        "country": "India",
        "region": "South India",
        "city": "Bengaluru / Chennai / Hyderabad",
        "timezone": "IST (UTC+5:30)"
    }

def call_groq(prompt, temperature=0.2):
    """Call Groq API with the given prompt."""
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",
            temperature=temperature,
            max_tokens=1200,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def extract_json(text):
    """Extract JSON from markdown code blocks or raw text."""
    # Try code block first
    match = re.search(r'```(?:json)?\s*(.*?)\s*```', text, re.DOTALL)
    if match:
        text = match.group(1)
    # Try to find JSON object
    match = re.search(r'(\{.*\})', text, re.DOTALL)
    if match:
        text = match.group(1)
    return text

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown(f"## 🛡️ {get_text('language_label')}")
    selected_lang = st.selectbox(
        "",
        options=list(LANGUAGE_OPTIONS.keys()),
        index=list(LANGUAGE_OPTIONS.values()).index(st.session_state.language),
        label_visibility="collapsed"
    )
    st.session_state.language = LANGUAGE_OPTIONS[selected_lang]
    
    st.markdown("---")
    st.markdown(f"### {get_text('mission')}")
    st.markdown(get_text('mission_text'))
    
    st.markdown("---")
    st.markdown(f"### {get_text('stats')}")
    col1, col2, col3 = st.columns(3)
    col1.metric(get_text('stats_scams_blocked'), st.session_state.scams_caught)
    col2.metric(get_text('stats_users_protected'), "12K+")
    col3.metric(get_text('stats_accuracy'), "94%")
    
    st.markdown("---")
    st.markdown(f"### {get_text('why_raksha')}")
    st.markdown(f"- {get_text('why_1')}")
    st.markdown(f"- {get_text('why_2')}")
    st.markdown(f"- {get_text('why_3')}")
    st.markdown(f"- {get_text('why_4')}")
    
    st.markdown("---")
    st.markdown(f"*{get_text('made_for')}*")

# ==================== HERO BANNER ====================
st.markdown(f"""
    <div class="hero-banner">
        <h1>{get_text('hero_title')}</h1>
        <p>{get_text('hero_subtitle')}</p>
    </div>
""", unsafe_allow_html=True)

# ==================== MAIN TABS ====================
tab1, tab2, tab3, tab4 = st.tabs([
    f"💬 {get_text('message_checker')}", 
    f"🔗 {get_text('link_inspector')}", 
    f"📞 {get_text('call_checker')}", 
    f"🎓 {get_text('learn_quiz')}"
])

# ==================== TAB 1: MESSAGE CHECKER ====================
with tab1:
    st.header(get_text("check_message"))
    st.write(get_text("paste_any"))
    
    # Example message buttons
    st.write(f"**{get_text('try_example')}**")
    ex_cols = st.columns(3)
    with ex_cols[0]:
        if st.button(get_text("fake_lottery"), use_container_width=True):
            st.session_state.example_msg = "🎉 Congratulations! You have won Rs. 5,00,000 in a lucky draw. Call immediately on +91-98765-43210 and pay Rs. 5,000 processing fee to claim your prize. Do not delay!"
            st.rerun()
    with ex_cols[1]:
        if st.button(get_text("fake_bank"), use_container_width=True):
            st.session_state.example_msg = "🏦 Dear Customer, Your SBI account will be suspended today due to KYC update failure. Click here immediately to verify: http://sbi-secure-verify.com/update"
            st.rerun()
    with ex_cols[2]:
        if st.button(get_text("fake_delivery"), use_container_width=True):
            st.session_state.example_msg = "📦 Your Amazon package is pending delivery. Please pay Rs. 49 customs clearance fee via this link to receive it today: http://amz-delivery.in/pay"
            st.rerun()
    
    msg = st.text_area(get_text("paste_message"), value=st.session_state.get("example_msg", ""), height=150, key="msg_input")
    
    if st.button(get_text("analyze_btn"), type="primary"):
        if not msg.strip():
            st.warning(get_text("enter_message"))
        else:
            with st.spinner("🔍 AI is analyzing the message..."):
                prompt = f"""You are Raksha, a digital safety guardian for Indian families. Analyze the following message and determine if it is a scam, suspicious, or safe.

Respond STRICTLY in this JSON format:
{{
  "verdict": "Scam" | "Suspicious" | "Safe",
  "confidence": <number 0-100>,
  "red_flags": [<list of specific red flags>],
  "risk_factors": [<list of risk factors>],
  "advice": "<what the user should do>",
  "explanation": "<brief explanation of the analysis>"
}}

Message to analyze:
\"\"\"{msg}\"\"\"

Respond ONLY with the JSON object, no other text."""
                
                raw = call_groq(prompt)
                st.session_state.messages_checked += 1
                
                try:
                    clean_json = extract_json(raw)
                    result = json.loads(clean_json)
                    
                    verdict = result.get("verdict", "Unknown")
                    confidence = result.get("confidence", 0)
                    
                    if verdict == "Scam":
                        badge_class = "scam-high"
                        badge_text = get_text("scam_label")
                        st.session_state.scams_caught += 1
                    elif verdict == "Suspicious":
                        badge_class = "scam-medium"
                        badge_text = get_text("suspicious_label")
                    else:
                        badge_class = "scam-safe"
                        badge_text = get_text("safe_label")
                    
                    st.markdown(f'<div class="scam-badge {badge_class}">{badge_text}</div>', unsafe_allow_html=True)
                    
                    c1, c2 = st.columns(2)
                    c1.metric(get_text("verdict"), verdict)
                    c2.metric(get_text("confidence"), f"{confidence}%")
                    
                    with st.expander(f"🚩 {get_text('red_flags')}"):
                        for flag in result.get("red_flags", []):
                            st.write(f"- {flag}")
                    
                    with st.expander(f"⚠️ {get_text('risk_factors')}"):
                        for factor in result.get("risk_factors", []):
                            st.write(f"- {factor}")
                    
                    st.info(f"**{get_text('advice')}:** {result.get('advice', 'N/A')}")
                    st.success(f"**{get_text('explanation')}:** {result.get('explanation', 'N/A')}")
                    
                except Exception as e:
                    st.error(f"{get_text('parse_error')} ({str(e)})")
                    with st.expander(get_text("raw_response")):
                        st.code(raw)

# ==================== TAB 2: LINK INSPECTOR ====================
with tab2:
    st.header(get_text("link_inspector"))
    st.write(get_text("url_description"))
    
    url = st.text_input(get_text("paste_url"), placeholder="https://example.com/suspicious-link")
    
    if st.button(get_text("analyze_url"), type="primary"):
        if not url.strip():
            st.warning(get_text("enter_url"))
        else:
            with st.spinner("🔍 Inspecting URL..."):
                prompt = f"""Analyze this URL for phishing, malware, or scam indicators.

Respond STRICTLY in this JSON format:
{{
  "verdict": "Scam" | "Suspicious" | "Safe",
  "confidence": <number 0-100>,
  "red_flags": [<list of red flags>],
  "advice": "<what the user should do>",
  "explanation": "<brief explanation>"
}}

URL: {url}

Respond ONLY with the JSON object, no other text."""
                
                raw = call_groq(prompt)
                
                try:
                    clean_json = extract_json(raw)
                    result = json.loads(clean_json)
                    
                    verdict = result.get("verdict", "Unknown")
                    confidence = result.get("confidence", 0)
                    
                    if verdict == "Scam":
                        badge_class = "scam-high"
                        badge_text = get_text("scam_label")
                    elif verdict == "Suspicious":
                        badge_class = "scam-medium"
                        badge_text = get_text("suspicious_label")
                    else:
                        badge_class = "scam-safe"
                        badge_text = get_text("safe_label")
                    
                    st.markdown(f'<div class="scam-badge {badge_class}">{badge_text}</div>', unsafe_allow_html=True)
                    
                    c1, c2 = st.columns(2)
                    c1.metric(get_text("verdict"), verdict)
                    c2.metric(get_text("confidence"), f"{confidence}%")
                    
                    with st.expander(f"🚩 {get_text('red_flags')}"):
                        for flag in result.get("red_flags", []):
                            st.write(f"- {flag}")
                    
                    st.info(f"**{get_text('advice')}:** {result.get('advice', 'N/A')}")
                    st.success(f"**{get_text('explanation')}:** {result.get('explanation', 'N/A')}")
                    
                except Exception as e:
                    st.error(f"{get_text('parse_error')} ({str(e)})")
                    with st.expander(get_text("raw_response")):
                        st.code(raw)

# ==================== TAB 3: CALL CHECKER ====================
with tab3:
    st.header(get_text("call_checker"))
    st.write(get_text("call_checker_description"))
    
    phone = st.text_input(get_text("phone_number"), placeholder="+91 98765 43210 or 9876543210")
    call_count = st.number_input(get_text("call_count"), min_value=1, max_value=100, value=1, step=1)
    call_desc = st.text_area(get_text("call_description_label"), placeholder=get_text("call_description_placeholder"), height=100)
    
    st.caption(get_text("location_notice"))
    st.caption(get_text("privacy_notice"))
    
    if st.button(get_text("analyze_call"), type="primary"):
        if not phone.strip():
            st.warning(get_text("enter_phone"))
        else:
            with st.spinner(get_text("checking_call")):
                # Validate Indian phone number format
                cleaned = phone.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
                is_valid = False
                if cleaned.startswith("+91") and len(cleaned) == 13 and cleaned[3:].isdigit():
                    is_valid = True
                elif cleaned.isdigit() and len(cleaned) == 10:
                    is_valid = True
                
                if not is_valid:
                    st.error(get_text("invalid_phone"))
                else:
                    # Show telecom intelligence
                    telecom = get_telecom_info(cleaned)
                    
                    st.subheader(get_text("telecom_intelligence"))
                    tcols = st.columns(3)
                    tcols[0].metric(get_text("number_valid"), get_text("yes") if telecom["valid"] else get_text("no"))
                    tcols[1].metric(get_text("carrier"), telecom["carrier"])
                    tcols[2].metric(get_text("line_type"), telecom["line_type"])
                    
                    tcols = st.columns(3)
                    tcols[0].metric(get_text("country"), telecom["country"])
                    tcols[1].metric(get_text("region"), telecom["region"])
                    tcols[2].metric(get_text("registered_city"), telecom["city"])
                    
                    st.caption(get_text("telecom_not_verdict"))
                    
                    # AI Analysis
                    masked = cleaned[:4] + "****" + cleaned[-2:] if len(cleaned) > 6 else "****"
                    
                    prompt = f"""Analyze this phone call for scam/fraud indicators.

Respond STRICTLY in this JSON format:
{{
  "verdict": "Scam" | "Suspicious" | "Safe",
  "confidence": <number 0-100>,
  "red_flags": [<list of red flags>],
  "behavior_risk": "<description of behavioral risk>",
  "overall_risk": "<High/Medium/Low>",
  "advice": "<what the user should do>",
  "explanation": "<brief explanation>"
}}

Call Details:
- Phone Number (masked): {masked}
- Calls Received: {call_count}
- Caller Description: {call_desc}

Respond ONLY with the JSON object, no other text."""
                    
                    raw = call_groq(prompt)
                    
                    try:
                        clean_json = extract_json(raw)
                        result = json.loads(clean_json)
                        
                        verdict = result.get("verdict", "Unknown")
                        confidence = result.get("confidence", 0)
                        
                        if verdict == "Scam":
                            badge_class = "scam-high"
                            badge_text = get_text("scam_label")
                        elif verdict == "Suspicious":
                            badge_class = "scam-medium"
                            badge_text = get_text("suspicious_label")
                        else:
                            badge_class = "scam-safe"
                            badge_text = get_text("safe_label")
                        
                        st.markdown(f'<div class="scam-badge {badge_class}">{badge_text}</div>', unsafe_allow_html=True)
                        
                        c1, c2 = st.columns(2)
                        c1.metric(get_text("verdict"), verdict)
                        c2.metric(get_text("confidence"), f"{confidence}%")
                        
                        with st.expander(f"📊 {get_text('risk_evidence')}"):
                            st.write(f"**{get_text('behavior_risk')}:** {result.get('behavior_risk', 'N/A')}")
                            st.write(f"**{get_text('calls_received')}:** {call_count}")
                            st.write(f"**{get_text('overall_risk')}:** {result.get('overall_risk', 'N/A')}")
                        
                        with st.expander(f"🚩 {get_text('red_flags')}"):
                            for flag in result.get("red_flags", []):
                                st.write(f"- {flag}")
                        
                        st.info(f"**{get_text('advice')}:** {result.get('advice', 'N/A')}")
                        st.success(f"**{get_text('explanation')}:** {result.get('explanation', 'N/A')}")
                        
                    except Exception as e:
                        st.error(f"{get_text('parse_error')} ({str(e)})")
                        with st.expander(get_text("raw_response")):
                            st.code(raw)

# ==================== TAB 4: LEARN & QUIZ ====================
with tab4:
    st.header(get_text("quiz_title"))
    st.write(get_text("quiz_description"))
    
    quiz_data = [
        {
            "q": "You receive a message: 'Congratulations! You won Rs. 10,00,000. Pay Rs. 5,000 processing fee to claim.' What do you do?",
            "options": ["Pay the fee immediately", "Ignore and delete", "Reply with bank details", "Forward to friends"],
            "correct": 1,
            "explanation": "Legitimate lotteries never ask for upfront fees. This is a classic advance-fee scam."
        },
        {
            "q": "A caller says they are from your bank and asks for your OTP to 'unblock' your account. What is this?",
            "options": ["Normal procedure", "Possible scam", "Required verification", "Bank policy"],
            "correct": 1,
            "explanation": "Banks NEVER ask for OTPs over phone. This is a vishing (voice phishing) scam."
        },
        {
            "q": "You get a link that looks like 'amaz0n-shop.com' instead of 'amazon.in'. What should you do?",
            "options": ["Click and login", "Check URL carefully and avoid", "It's probably fine", "Download the app from link"],
            "correct": 1,
            "explanation": "Typosquatting domains (amaz0n, amzon) are classic phishing traps. Always verify the exact domain."
        },
        {
            "q": "Which of these is a major red flag in any message?",
            "options": ["Urgency and threats", "Proper grammar", "Known sender", "No links"],
            "correct": 0,
            "explanation": "Scammers create false urgency ('Act now!', 'Account suspended!') to panic you into acting without thinking."
        },
        {
            "q": "An unknown number calls 5 times in 10 minutes demanding immediate payment. What does this indicate?",
            "options": ["Important business", "Scam pressure tactic", "Government call", "Telecom verification"],
            "correct": 1,
            "explanation": "Repeated calls and pressure to act immediately are classic scam tactics to prevent you from verifying facts."
        }
    ]
    
    # Initialize quiz state
    if 'q_index' not in st.session_state:
        st.session_state.q_index = 0
    if 'q_score' not in st.session_state:
        st.session_state.q_score = 0
    if 'q_answered' not in st.session_state:
        st.session_state.q_answered = False
    
    idx = st.session_state.q_index
    
    if idx < len(quiz_data):
        q = quiz_data[idx]
        st.subheader(f"{get_text('question')} {idx + 1} / {len(quiz_data)}")
        st.write(q["q"])
        
        ans = st.radio("Choose:", q["options"], index=None, key=f"q_{idx}")
        
        if st.button(get_text("submit_answer")):
            if ans is None:
                st.warning(get_text("select_answer"))
            else:
                correct_idx = q["correct"]
                if q["options"].index(ans) == correct_idx:
                    st.success(get_text("correct"))
                    if not st.session_state.q_answered:
                        st.session_state.q_score += 1
                else:
                    st.error(get_text("incorrect"))
                
                st.session_state.q_answered = True
                st.info(f"**{get_text('explanation')}:** {q['explanation']}")
        
        if st.session_state.q_answered:
            if st.button("→ Next"):
                st.session_state.q_index += 1
                st.session_state.q_answered = False
                st.rerun()
    else:
        st.balloons()
        score = st.session_state.q_score
        total = len(quiz_data)
        st.success(f"**{get_text('score')}: {score} / {total}**")
        
        if score == total:
            st.success(get_text("perfect_score"))
        elif score >= total * 0.6:
            st.info("👍 Good job! You're learning to spot scams.")
        else:
            st.warning("Keep practicing! Scammers are getting smarter too.")
        
        if st.button("🔄 Restart Quiz"):
            st.session_state.q_index = 0
            st.session_state.q_score = 0
            st.session_state.q_answered = False
            st.rerun()

# ==================== FLOATING REPORT BUTTON ====================
st.markdown(f"""
    <a href="https://cybercrime.gov.in/Webform/CrimeAuthway.aspx?Req=oticid" target="_blank" class="fab-report" title="{get_text('report_scam')}">🚨</a>
""", unsafe_allow_html=True)

# ==================== FOOTER ====================
st.markdown("---")
st.markdown(f"""
    <div style="text-align: center; padding: 2rem 1rem; color: #64748b;">
        <p style="font-size: 1rem; margin-bottom: 0.5rem;">{get_text('footer')}</p>
        <p style="font-size: 0.85rem; opacity: 0.8;">{get_text('footer_model')}</p>
    </div>
""", unsafe_allow_html=True)