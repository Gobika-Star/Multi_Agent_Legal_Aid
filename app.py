import streamlit as st
from main import build_graph
from agents.translator import translate_report_to_tamil
from agents.translator import translate_report_to_tamil, translate_examples_to_tamil

st.set_page_config(page_title="Legal Aid Navigator", page_icon="⚖️", layout="centered", initial_sidebar_state="collapsed")

# =========================================================
# CUSTOM CSS DESIGN SYSTEM - ROYAL PURPLE & GOLD
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=Noto+Sans+Tamil:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', 'Noto Sans Tamil', sans-serif;
}

#MainMenu, footer, header {visibility: hidden;}

.stApp {
    background: linear-gradient(160deg, #1a0b2e 0%, #2d1155 50%, #1a0b2e 100%);
}

.block-container {
    padding-top: 2rem;
    max-width: 780px;
}

.progress-wrap {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    margin-bottom: 1.8rem;
}
.step-dot {
    width: 34px;
    height: 6px;
    border-radius: 4px;
    background-color: rgba(255,255,255,0.15);
    transition: all 0.3s ease;
}
.step-dot.active {
    background: linear-gradient(90deg, #ffd700, #ffb703);
    box-shadow: 0 0 8px rgba(255,215,0,0.6);
}
.step-dot.done {
    background-color: #9d4edd;
}

.app-header {
    text-align: center;
    margin-bottom: 0.5rem;
}
.app-header h1 {
    font-weight: 800;
    font-size: 2.1rem;
    background: linear-gradient(90deg, #ffd700, #ffb703, #ff9e00);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.2rem;
    text-shadow: 0 2px 20px rgba(255,215,0,0.2);
}
.app-subtitle {
    text-align: center;
    color: #c9b6f0 !important;
    font-size: 0.95rem;
    margin-bottom: 1.5rem;
}

.page-title {
    font-size: 1.5rem;
    font-weight: 700;
    color: #ffd700 !important;
    margin-bottom: 0.3rem;
}
.page-sub {
    color: #c9b6f0 !important;
    font-size: 0.9rem;
    margin-bottom: 1.2rem;
}

.categories-label {
    font-size: 0.8rem;
    font-weight: 600;
    color: #ffd700 !important;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin-bottom: 0.6rem;
    margin-top: 0.4rem;
}

.card {
    background: linear-gradient(135deg, #ffffff, #f5f0ff);
    border: 1px solid #d8bfff;
    border-left: 5px solid #7b2cbf;
    border-radius: 14px;
    padding: 1.1rem 1.3rem;
    margin-bottom: 1rem;
    box-shadow: 0 4px 18px rgba(123,44,191,0.25);
    color: #2d1155 !important;
    line-height: 1.6;
}
.card * { color: #2d1155 !important; }

.card-highlight {
    background: linear-gradient(135deg, #fff9e6, #ffedb3);
    border: 1px solid #ffd700;
    border-left: 5px solid #d4a017;
    border-radius: 14px;
    padding: 1.1rem 1.3rem;
    margin-bottom: 1rem;
    color: #5c4400 !important;
    line-height: 1.6;
    box-shadow: 0 4px 18px rgba(255,215,0,0.25);
}
.card-highlight * { color: #5c4400 !important; }

.card-step {
    background: linear-gradient(135deg, #f0e6ff, #e0ccff);
    border-radius: 12px;
    padding: 0.9rem 1.1rem;
    margin-bottom: 0.6rem;
    display: flex;
    gap: 0.7rem;
    align-items: flex-start;
    color: #2d1155 !important;
    box-shadow: 0 3px 12px rgba(123,44,191,0.2);
}
.card-step * { color: #2d1155 !important; }

.step-num {
    background: linear-gradient(135deg, #ffd700, #ff9e00);
    color: #2d1155 !important;
    font-weight: 800;
    width: 28px;
    height: 28px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    font-size: 0.9rem;
    box-shadow: 0 2px 8px rgba(255,215,0,0.5);
}

.stButton>button {
    border-radius: 10px;
    font-weight: 700;
    padding: 0.6rem 1.2rem;
    border: none;
    background: linear-gradient(135deg, #7b2cbf, #5a189a);
    color: #ffffff !important;
    box-shadow: 0 3px 12px rgba(123,44,191,0.4);
    transition: all 0.25s ease;
}
.stButton>button:hover {
    background: linear-gradient(135deg, #9d4edd, #7b2cbf);
    box-shadow: 0 4px 18px rgba(255,215,0,0.35);
    transform: translateY(-1px);
}
.stButton>button[kind="primary"] {
    background: linear-gradient(135deg, #ffd700, #ff9e00) !important;
    color: #2d1155 !important;
    box-shadow: 0 3px 14px rgba(255,215,0,0.45);
}
.stButton>button[kind="primary"]:hover {
    background: linear-gradient(135deg, #ffed4e, #ffd700) !important;
    box-shadow: 0 5px 20px rgba(255,215,0,0.6);
}
div[data-testid="column"] .stButton>button {
    width: 100%;
}

.badge-row {
    display: flex;
    gap: 0.7rem;
    margin-bottom: 1rem;
}
.badge {
    flex: 1;
    background: linear-gradient(135deg, #f5f0ff, #e8d9ff);
    border: 1px solid #d8bfff;
    border-radius: 12px;
    padding: 0.75rem;
    text-align: center;
    box-shadow: 0 3px 12px rgba(123,44,191,0.2);
}
.badge-label {
    font-size: 0.75rem;
    color: #7b2cbf !important;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    font-weight: 600;
}
.badge-value {
    font-size: 1.1rem;
    font-weight: 700;
    color: #5a189a !important;
    margin-top: 2px;
}

.stTextArea textarea, .stSelectbox > div > div {
    border-radius: 10px !important;
    border: 1.5px solid #7b2cbf !important;
}
.streamlit-expanderHeader {
    background: linear-gradient(135deg, #f5f0ff, #e8d9ff) !important;
    border-radius: 10px !important;
    color: #2d1155 !important;
    font-weight: 600;
}

.stAlert {
    border-radius: 12px !important;
}

.cat-caption {
    text-align: center;
    color: #c9b6f0 !important;
    font-size: 0.72rem;
    margin-top: -8px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# TEXT DICTIONARY (UI labels only)
# =========================================================
UI = {
    "english": {
        "title": "⚖️ Legal Aid Navigator-Know your Rights in hands", "subtitle": "AI-powered legal guidance in your language",
        "lang_prompt": "Choose your preferred language",
        "step1_title": "Tell us your problem", "step1_sub": "Pick a category, then describe it in your own words.",
        "categories_label": "What we cover — select a category",
        "select_category_prompt": "Please select a category above to see relevant examples.",
        "example_label": "Try an example", "example_placeholder": "Select an example...",
        "input_label": "Describe your problem", "input_placeholder": "e.g. My landlord is not returning my deposit...",
        "analyze": "Analyze My Case →", "empty_warning": "Please describe your problem first.",
        "analyzing": "Analyzing your case across 6 agents...",
        "step2_title": "Case Understanding", "step2_sub": "Here's what our agents found",
        "detected_lang": "Language", "category": "Category", "section_label": "Applicable Section",
        "step3_title": "What the Law Says", "step3_sub": "Explained in plain language",
        "step4_title": "Steps to Overcome This", "step4_sub": "Your action plan",
        "step5_title": "Where to Go & What to Carry", "step5_sub": "Forum details and document checklist",
        "timeline": "Timeline", "cost": "Cost", "documents": "Documents to Carry",
        "laws_expander": "View relevant law excerpts",
        "back": "← Back", "next": "Next →", "restart": "🔄 Start New Case", "change_lang": "🌐 Language",
        "final_note": "This is general legal guidance, not a substitute for a licensed lawyer.",
    },
    "tamil": {
        "title": "⚖️ சட்ட உதவி வழிகாட்டி", "subtitle": "உங்கள் மொழியில் AI சட்ட வழிகாட்டுதல்",
        "lang_prompt": "உங்கள் விருப்பமான மொழியைத் தேர்ந்தெடுக்கவும்",
        "step1_title": "உங்கள் பிரச்சனையைச் சொல்லுங்கள்", "step1_sub": "ஒரு வகையைத் தேர்ந்தெடுத்து, உங்கள் சொந்த வார்த்தைகளில் விவரிக்கவும்.",
        "categories_label": "நாங்கள் கையாளும் விஷயங்கள் — ஒரு வகையைத் தேர்ந்தெடுக்கவும்",
        "select_category_prompt": "தொடர்புடைய எடுத்துக்காட்டுகளைக் காண மேலே ஒரு வகையைத் தேர்ந்தெடுக்கவும்.",
        "example_label": "எடுத்துக்காட்டு முயற்சிக்கவும்", "example_placeholder": "எடுத்துக்காட்டைத் தேர்ந்தெடுக்கவும்...",
        "input_label": "உங்கள் பிரச்சனையை விவரிக்கவும்", "input_placeholder": "எ.கா. என் வீட்டு உரிமையாளர் வைப்புத்தொகையைத் திருப்பித் தரவில்லை...",
        "analyze": "என் வழக்கை பகுப்பாய்வு செய் →", "empty_warning": "முதலில் உங்கள் பிரச்சனையை விவரிக்கவும்.",
        "analyzing": "6 ஏஜென்ட்கள் மூலம் பகுப்பாய்வு செய்யப்படுகிறது...",
        "step2_title": "வழக்கு புரிதல்", "step2_sub": "எங்கள் ஏஜென்ட்கள் கண்டறிந்தது",
        "detected_lang": "மொழி", "category": "வகை", "section_label": "பொருந்தும் சட்டப்பிரிவு",
        "step3_title": "சட்டம் என்ன கூறுகிறது", "step3_sub": "எளிய மொழியில் விளக்கப்பட்டுள்ளது",
        "step4_title": "இதைச் சமாளிக்க வேண்டிய படிகள்", "step4_sub": "உங்கள் செயல் திட்டம்",
        "step5_title": "எங்கு செல்ல வேண்டும் & என்ன எடுத்துச் செல்ல வேண்டும்", "step5_sub": "மன்ற விவரங்கள் மற்றும் ஆவணப் பட்டியல்",
        "timeline": "காலஅளவு", "cost": "செலவு", "documents": "எடுத்துச் செல்ல வேண்டிய ஆவணங்கள்",
        "laws_expander": "தொடர்புடைய சட்டப் பகுதிகளைக் காண்க",
        "back": "← பின்செல்", "next": "அடுத்து →", "restart": "🔄 புதிய வழக்கு", "change_lang": "🌐 மொழி",
        "final_note": "இது பொதுவான சட்ட வழிகாட்டுதல் மட்டுமே, வழக்கறிஞர் ஆலோசனைக்கு மாற்றாக அல்ல.",
    }
}

# =========================================================
# CATEGORY DATA (labels, descriptions, examples per language)
# =========================================================
CATEGORY_DATA = {
    "english": {
        "land": {
            "label": "🏠 Land & Tenancy",
            "desc": "Deposits, rent disputes, property, RERA",
            "examples": {
                "Deposit not returned": "My landlord is not returning my deposit, it has been 3 months.",
                "Builder delayed possession": "The builder has not handed over my flat even 8 months after the promised date.",
                "Neighbour built on my land": "My neighbour has built a wall extending into my property without permission.",
            }
        },
        "labor": {
            "label": "💼 Labor",
            "desc": "Wages, termination, PF, workplace harassment",
            "examples": {
                "Salary not paid": "My office has not paid my salary for 2 months.",
                "Wrongful termination": "I was fired without notice or any compensation after 3 years of service.",
                "PF not deposited": "My employer has not been depositing my PF contributions for 6 months.",
            }
        },
        "consumer": {
            "label": "🛒 Consumer",
            "desc": "Defective goods, refunds, online fraud",
            "examples": {
                "Defective product": "I bought a mixer grinder online and it stopped working in a week, seller refuses refund.",
                "Fake product delivered": "I ordered a branded phone online but received a duplicate/fake one.",
                "Service deficiency": "The AC repair company took my money but never fixed the issue.",
            }
        },
        "family": {
            "label": "👪 Family",
            "desc": "Divorce, maintenance, domestic violence, dowry",
            "examples": {
                "Maintenance not paid": "My husband is not paying maintenance after our separation.",
                "Domestic violence": "I am facing physical abuse from my husband and need protection.",
                "Dowry harassment": "My in-laws are demanding dowry and threatening me.",
            }
        },
        "cyber": {
            "label": "💻 Cyber",
            "desc": "Online fraud, hacking, harassment, morphed images",
            "examples": {
                "Bank fraud / cheating": "Someone tricked me into transferring money by pretending to be from my bank.",
                "Account hacked": "Someone hacked my Instagram account and is asking for money.",
                "Morphed photo threat": "Someone is threatening to post my morphed photos online.",
            }
        },
        "police": {
            "label": "🚔 Police & Criminal",
            "desc": "FIR issues, cheating, assault",
            "examples": {
                "FIR refused": "The police station is refusing to register my FIR.",
                "Assault at workplace": "I was physically assaulted by a colleague at work.",
                "Threatened by someone": "Someone is threatening me and I fear for my safety.",
            }
        },
        "other": {
            "label": "📋 Other",
            "desc": "RTI, defamation, general legal aid",
            "examples": {
                "False statements about me": "Someone is spreading false rumors that are damaging my reputation.",
                "Government not responding": "I filed an RTI request but haven't received a response in 2 months.",
                "Not sure which category": "I have a legal problem but I'm not sure which category it falls under.",
            }
        },
    },
    "tamil": {
        "land": {
            "label": "🏠 நிலம் & வாடகை",
            "desc": "வைப்புத்தொகை, வாடகை தகராறு, சொத்து, RERA",
            "examples": {
                "வைப்புத்தொகை திரும்பவில்லை": "My landlord is not returning my deposit, it has been 3 months.",
                "கட்டிட உரிமையாளர் தாமதம்": "The builder has not handed over my flat even 8 months after the promised date.",
                "அண்டை வீட்டார் எல்லை மீறல்": "My neighbour has built a wall extending into my property without permission.",
            }
        },
        "labor": {
            "label": "💼 தொழிலாளர்",
            "desc": "சம்பளம், பணிநீக்கம், PF, பணியிட துன்புறுத்தல்",
            "examples": {
                "சம்பளம் வழங்கப்படவில்லை": "My office has not paid my salary for 2 months.",
                "தவறான பணிநீக்கம்": "I was fired without notice or any compensation after 3 years of service.",
                "PF செலுத்தப்படவில்லை": "My employer has not been depositing my PF contributions for 6 months.",
            }
        },
        "consumer": {
            "label": "🛒 நுகர்வோர்",
            "desc": "குறைபாடுள்ள பொருட்கள், பணம் திரும்பப் பெறுதல், ஆன்லைன் மோசடி",
            "examples": {
                "குறைபாடுள்ள பொருள்": "I bought a mixer grinder online and it stopped working in a week, seller refuses refund.",
                "போலி பொருள் வழங்கப்பட்டது": "I ordered a branded phone online but received a duplicate/fake one.",
                "சேவை குறைபாடு": "The AC repair company took my money but never fixed the issue.",
            }
        },
        "family": {
            "label": "👪 குடும்பம்",
            "desc": "விவாகரத்து, ஜீவனாம்சம், குடும்ப வன்முறை, வரதட்சணை",
            "examples": {
                "ஜீவனாம்சம் வழங்கப்படவில்லை": "My husband is not paying maintenance after our separation.",
                "குடும்ப வன்முறை": "I am facing physical abuse from my husband and need protection.",
                "வரதட்சணை துன்புறுத்தல்": "My in-laws are demanding dowry and threatening me.",
            }
        },
        "cyber": {
            "label": "💻 சைபர்",
            "desc": "ஆன்லைன் மோசடி, ஹேக்கிங், துன்புறுத்தல்",
            "examples": {
                "வங்கி மோசடி": "Someone tricked me into transferring money by pretending to be from my bank.",
                "கணக்கு ஹேக் செய்யப்பட்டது": "Someone hacked my Instagram account and is asking for money.",
                "போலி புகைப்பட அச்சுறுத்தல்": "Someone is threatening to post my morphed photos online.",
            }
        },
        "police": {
            "label": "🚔 காவல் & குற்றவியல்",
            "desc": "FIR பிரச்சனைகள், ஏமாற்றுதல், தாக்குதல்",
            "examples": {
                "FIR பதிவு மறுப்பு": "The police station is refusing to register my FIR.",
                "பணியிடத்தில் தாக்குதல்": "I was physically assaulted by a colleague at work.",
                "அச்சுறுத்தல்": "Someone is threatening me and I fear for my safety.",
            }
        },
        "other": {
            "label": "📋 மற்றவை",
            "desc": "RTI, அவதூறு, பொது சட்ட உதவி",
            "examples": {
                "தவறான வதந்திகள்": "Someone is spreading false rumors that are damaging my reputation.",
                "அரசு பதிலளிக்கவில்லை": "I filed an RTI request but haven't received a response in 2 months.",
                "வகை தெரியவில்லை": "I have a legal problem but I'm not sure which category it falls under.",
            }
        },
    }
}

# =========================================================
# SESSION STATE INIT
# =========================================================
defaults = {
    "page": "language", "language": None, "query": "",
    "final_state": None, "report": None, "selected_category": None
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

def goto(page):
    st.session_state.page = page
    st.rerun()

def progress_bar(current_step, total=4):
    dots = ""
    for i in range(1, total + 1):
        cls = "active" if i == current_step else ("done" if i < current_step else "")
        dots += f'<div class="step-dot {cls}"></div>'
    st.markdown(f'<div class="progress-wrap">{dots}</div>', unsafe_allow_html=True)

# =========================================================
# PAGE: LANGUAGE SELECT
# =========================================================
if st.session_state.page == "language":
    st.markdown('<div class="app-header"><h1>⚖️ Legal Aid Navigator</h1></div>', unsafe_allow_html=True)
    st.markdown('<p class="app-subtitle">Choose your preferred language / உங்கள் மொழியைத் தேர்ந்தெடுக்கவும்</p>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("English", use_container_width=True, type="primary"):
            st.session_state.language = "english"
            goto("input")
        st.write("")
        if st.button("தமிழ் (Tamil)", use_container_width=True, type="primary"):
            st.session_state.language = "tamil"
            goto("input")

# =========================================================
# PAGE: INPUT
# =========================================================
elif st.session_state.page == "input":
    T = UI[st.session_state.language]
    is_tamil = st.session_state.language == "tamil"

    st.markdown(f'<div class="app-header"><h1>{T["title"]}</h1></div>', unsafe_allow_html=True)
    st.markdown(f'<p class="app-subtitle">{T["subtitle"]}</p>', unsafe_allow_html=True)
    progress_bar(1)

    st.markdown(f'<div class="page-title">{T["step1_title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="page-sub">{T["step1_sub"]}</div>', unsafe_allow_html=True)

    # ---- Category selection (clickable buttons) ----
    st.markdown(f'<div class="categories-label">{T["categories_label"]}</div>', unsafe_allow_html=True)

    cat_data = CATEGORY_DATA[st.session_state.language]
    cat_keys = list(cat_data.keys())

    for row_start in range(0, len(cat_keys), 2):
        row_keys = cat_keys[row_start:row_start + 2]
        cols = st.columns(2)
        for col, ckey in zip(cols, row_keys):
            with col:
                info = cat_data[ckey]
                is_selected = st.session_state.selected_category == ckey
                if st.button(info["label"], key=f"cat_{ckey}", use_container_width=True,
                             type="primary" if is_selected else "secondary"):
                    st.session_state.selected_category = ckey
                    st.rerun()
                st.markdown(f'<div class="cat-caption">{info["desc"]}</div>', unsafe_allow_html=True)

    st.write("")

    # ---- Examples filtered by selected category ----
    # ---- Examples filtered by selected category (translated live if Tamil) ----
    # ---- Examples filtered by selected category (translated live if Tamil) ----
    selected_cat = st.session_state.get("selected_category")
    if selected_cat:
        english_examples = cat_data[selected_cat]["examples"]

        if is_tamil:
            cache_key = f"examples_cache_{selected_cat}"
            if cache_key not in st.session_state:
                with st.spinner("..."):
                    st.session_state[cache_key] = translate_examples_to_tamil(english_examples)
            examples = st.session_state[cache_key]
        else:
            examples = english_examples

        example_keys = [T["example_placeholder"]] + list(examples.keys())
        selected_example = st.selectbox(T["example_label"], example_keys, label_visibility="collapsed")
        default_text = examples.get(selected_example, "")
    else:
        default_text = ""
        st.info(T.get("select_category_prompt", "Please select a category above first."))

    query = st.text_area(T["input_label"], value=default_text, height=120, placeholder=T["input_placeholder"])

    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button(T["change_lang"]):
            goto("language")
    with col2:
        if st.button(T["analyze"], type="primary"):
            if not query.strip():
                st.warning(T["empty_warning"])
            else:
                st.session_state.query = query
                goto("processing")

# =========================================================
# PAGE: PROCESSING (runs pipeline once, then auto-advances)
# =========================================================
elif st.session_state.page == "processing":
    T = UI[st.session_state.language]
    is_tamil = st.session_state.language == "tamil"

    st.markdown(f'<div class="app-header"><h1>{T["title"]}</h1></div>', unsafe_allow_html=True)
    progress_bar(1)

    with st.spinner(T["analyzing"]):
        app = build_graph()
        initial_state = {
            "raw_query": st.session_state.query, "detected_language": "", "normalized_query": "",
            "category": "", "confidence": 0.0, "applicable_section": None,
            "offense_summary": None, "laws": [], "forum_info": {},
            "explanation": "", "key_points": [], "steps_to_overcome": [], "checklist": {}
        }
        final_state = app.invoke(initial_state)

        report = {
            "category": final_state["category"].title(),
            "offense_summary": final_state.get("offense_summary") or "",
            "explanation": final_state["explanation"],
            "key_points": final_state["key_points"],
            "steps_to_overcome": final_state["steps_to_overcome"],
            "law_titles": [law["title"] for law in final_state["laws"]],
            "law_texts": [law["text"] for law in final_state["laws"]],
            "forum": final_state["forum_info"].get("forum", ""),
            "how_to_approach": final_state["forum_info"].get("how_to_approach", ""),
            "timeline": final_state["forum_info"].get("typical_timeline", ""),
            "cost": final_state["forum_info"].get("cost", ""),
            "checklist": final_state["checklist"].get("full_checklist", []),
        }

        if is_tamil:
            report = translate_report_to_tamil(report)

        st.session_state.final_state = final_state
        st.session_state.report = report

    goto("understanding")

# =========================================================
# PAGE: CASE UNDERSTANDING
# =========================================================
elif st.session_state.page == "understanding":
    T = UI[st.session_state.language]
    fs = st.session_state.final_state
    report = st.session_state.report

    st.markdown(f'<div class="app-header"><h1>{T["title"]}</h1></div>', unsafe_allow_html=True)
    progress_bar(2)
    st.markdown(f'<div class="page-title">{T["step2_title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="page-sub">{T["step2_sub"]}</div>', unsafe_allow_html=True)

    st.markdown(f'<div class="badge-row"><div class="badge"><div class="badge-label">{T["detected_lang"]}</div>'
                f'<div class="badge-value">{fs["detected_language"]}</div></div>'
                f'<div class="badge"><div class="badge-label">{T["category"]}</div>'
                f'<div class="badge-value">{report["category"]}</div></div></div>', unsafe_allow_html=True)

    if fs.get("applicable_section"):
        st.markdown(
            f'<div class="card-highlight"><b>{T["section_label"]}:</b> {fs["applicable_section"]}<br>{report.get("offense_summary","")}</div>',
            unsafe_allow_html=True
        )

    col1, col2 = st.columns(2)
    with col1:
        if st.button(T["back"]):
            goto("input")
    with col2:
        if st.button(T["next"], type="primary"):
            goto("law")

# =========================================================
# PAGE: LAW EXPLANATION
# =========================================================
elif st.session_state.page == "law":
    T = UI[st.session_state.language]
    report = st.session_state.report

    st.markdown(f'<div class="app-header"><h1>{T["title"]}</h1></div>', unsafe_allow_html=True)
    progress_bar(2)
    st.markdown(f'<div class="page-title">{T["step3_title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="page-sub">{T["step3_sub"]}</div>', unsafe_allow_html=True)

    st.markdown(f'<div class="card">{report["explanation"]}</div>', unsafe_allow_html=True)
    for point in report["key_points"]:
        st.markdown(f"- {point}")

    with st.expander(T["laws_expander"]):
        for title, text in zip(report["law_titles"], report["law_texts"]):
            st.markdown(f"**{title}**")
            st.write(text)
            st.divider()

    col1, col2 = st.columns(2)
    with col1:
        if st.button(T["back"]):
            goto("understanding")
    with col2:
        if st.button(T["next"], type="primary"):
            goto("steps")

# =========================================================
# PAGE: STEPS TO OVERCOME
# =========================================================
elif st.session_state.page == "steps":
    T = UI[st.session_state.language]
    report = st.session_state.report

    st.markdown(f'<div class="app-header"><h1>{T["title"]}</h1></div>', unsafe_allow_html=True)
    progress_bar(3)
    st.markdown(f'<div class="page-title">{T["step4_title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="page-sub">{T["step4_sub"]}</div>', unsafe_allow_html=True)

    for i, step in enumerate(report["steps_to_overcome"], 1):
        st.markdown(
            f'<div class="card-step"><div class="step-num">{i}</div>'
            f'<div style="padding-top:2px;">{step}</div></div>',
            unsafe_allow_html=True
        )

    col1, col2 = st.columns(2)
    with col1:
        if st.button(T["back"]):
            goto("law")
    with col2:
        if st.button(T["next"], type="primary"):
            goto("forum")

# =========================================================
# PAGE: FORUM + CHECKLIST
# =========================================================
elif st.session_state.page == "forum":
    T = UI[st.session_state.language]
    report = st.session_state.report

    st.markdown(f'<div class="app-header"><h1>{T["title"]}</h1></div>', unsafe_allow_html=True)
    progress_bar(4)
    st.markdown(f'<div class="page-title">{T["step5_title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="page-sub">{T["step5_sub"]}</div>', unsafe_allow_html=True)

    st.markdown(f'<div class="card"><b>{report["forum"]}</b><br>{report["how_to_approach"]}</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**{T['timeline']}:** {report['timeline']}")
    with col2:
        st.markdown(f"**{T['cost']}:** {report['cost']}")

    st.markdown(f"#### {T['documents']}")
    for item in report["checklist"]:
        st.checkbox(item, key=item)

    st.info(T["final_note"])

    col1, col2 = st.columns(2)
    with col1:
        if st.button(T["back"]):
            goto("steps")
    with col2:
        if st.button(T["restart"], type="primary"):
            st.session_state.page = "language"
            st.session_state.language = None
            st.session_state.query = ""
            st.session_state.final_state = None
            st.session_state.report = None
            st.session_state.selected_category = None
            st.rerun()