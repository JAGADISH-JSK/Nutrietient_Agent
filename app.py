"""
app.py
NutriGenius — AI Nutrition Assistant powered by IBM Granite (watsonx.ai)
Streamlit multi-page application.
"""

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# ── Page config (must be first Streamlit call) ──────────────────────────────
st.set_page_config(
    page_title="NutriGenius – AI Nutrition Assistant",
    page_icon="🥦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Lazy-import heavy modules after page config ──────────────────────────────
from nutrition_agent import NutritionAgent          # noqa: E402
from meal_planner import generate_meal_plan, estimate_calories  # noqa: E402
from food_advisor import get_food_swap, explain_nutrition        # noqa: E402
from image_analyzer import analyze_food_image                    # noqa: E402
from PIL import Image                                            # noqa: E402
import plotly.graph_objects as go                                # noqa: E402

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown(
    """
<style>
/* Global font + dark main background */
html, body, [class*="css"] { font-family: 'Segoe UI', system-ui, sans-serif; }

/* Dark background for entire app */
.stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background: #0d1b2a !important;
}
/* Main content area */
[data-testid="stMain"] > div, section.main > div {
    background: #0d1b2a !important;
}
/* All plain text → light */
.stApp p, .stApp li, .stApp span, .stApp div,
.stApp h1, .stApp h2, .stApp h3, .stApp h4 {
    color: #e8f4f8;
}
/* Main area markdown text */
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li,
[data-testid="stMarkdownContainer"] span {
    color: #e8f4f8 !important;
}
/* Streamlit widget labels in main area */
[data-testid="stMain"] label { color: #a8d8ea !important; }
/* Main area inputs */
[data-testid="stMain"] input,
[data-testid="stMain"] textarea {
    background-color: #1a3a5c !important;
    color: #e8f4f8 !important;
    border: 1px solid #3a6090 !important;
    border-radius: 8px !important;
}
/* Main area selectbox */
[data-testid="stMain"] [data-baseweb="select"] > div {
    background-color: #1a3a5c !important;
    border-color: #3a6090 !important;
}
[data-testid="stMain"] [data-baseweb="select"] span,
[data-testid="stMain"] [data-baseweb="select"] div { color: #e8f4f8 !important; }

/* Sidebar — base */
[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #0f3460 0%, #16213e 100%);
    color: #ffffff;
}
[data-testid="stSidebar"] * { color: #e8f4f8 !important; }

/* Sidebar — labels */
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stTextInput label,
[data-testid="stSidebar"] .stNumberInput label,
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stRadio label {
    color: #a8d8ea !important;
    font-weight: 600;
}

/* Sidebar — text inputs & number inputs: dark bg, light text */
[data-testid="stSidebar"] input,
[data-testid="stSidebar"] textarea {
    background-color: #1a3a5c !important;
    color: #e8f4f8 !important;
    border: 1px solid #3a6090 !important;
    border-radius: 8px !important;
}
[data-testid="stSidebar"] input::placeholder {
    color: #7aaccc !important;
}

/* Sidebar — selectbox / dropdown */
[data-testid="stSidebar"] [data-baseweb="select"] > div,
[data-testid="stSidebar"] [data-baseweb="select"] > div:hover {
    background-color: #1a3a5c !important;
    border-color: #3a6090 !important;
    border-radius: 8px !important;
}
[data-testid="stSidebar"] [data-baseweb="select"] span,
[data-testid="stSidebar"] [data-baseweb="select"] div {
    color: #e8f4f8 !important;
}

/* Sidebar — selectbox dropdown menu */
[data-baseweb="popover"] [role="listbox"],
[data-baseweb="menu"] {
    background-color: #16213e !important;
    border: 1px solid #3a6090 !important;
}
[data-baseweb="popover"] [role="option"],
[data-baseweb="menu"] li {
    background-color: #16213e !important;
    color: #e8f4f8 !important;
}
[data-baseweb="popover"] [role="option"]:hover,
[data-baseweb="menu"] li:hover {
    background-color: #0f3460 !important;
}

/* Sidebar — number input stepper buttons */
[data-testid="stSidebar"] [data-testid="stNumberInput"] button {
    background-color: #1a3a5c !important;
    color: #e8f4f8 !important;
    border-color: #3a6090 !important;
}

/* Sidebar — slider track & thumb */
[data-testid="stSidebar"] [data-testid="stSlider"] div[role="slider"] {
    background-color: #e94560 !important;
}
[data-testid="stSidebar"] [data-testid="stSlider"] > div > div {
    background-color: #3a6090 !important;
}

/* Sidebar — radio buttons */
[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] label {
    background-color: rgba(255,255,255,0.05) !important;
    border-radius: 8px !important;
    padding: 0.3rem 0.6rem !important;
    margin: 2px 0 !important;
    color: #e8f4f8 !important;
}

/* Header banner */
.hero-banner {
    background: linear-gradient(135deg, #0f3460 0%, #e94560 100%);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    color: white;
    margin-bottom: 1.5rem;
}
.hero-banner h1 { font-size: 2.4rem; font-weight: 800; margin: 0; }
.hero-banner p  { font-size: 1.1rem; opacity: 0.9; margin: 0.4rem 0 0; }

/* Chat messages — dark theme, compact */
.chat-user {
    background: rgba(15, 52, 96, 0.55);
    border-left: 4px solid #a8d8ea;
    border-radius: 10px;
    padding: 0.45rem 0.9rem;
    margin: 0.3rem 0;
}
.chat-user, .chat-user * { color: #e8f4f8 !important; }
.chat-ai {
    background: rgba(233, 69, 96, 0.12);
    border-left: 4px solid #e94560;
    border-radius: 10px;
    padding: 0.45rem 0.9rem;
    margin: 0.3rem 0;
}
.chat-ai, .chat-ai * { color: #e8f4f8 !important; }

/* Cards — dark theme */
.metric-card {
    background: rgba(15, 52, 96, 0.5);
    border: 1px solid #3a6090;
    border-radius: 12px;
    padding: 1.2rem;
    text-align: center;
}
.metric-card h3 { font-size: 2rem; color: #a8d8ea; margin: 0; }
.metric-card p  { color: #7aaccc; font-size: 0.85rem; margin: 0; }

/* IBM badge */
.ibm-badge {
    background: #0530ad;
    color: white !important;
    border-radius: 6px;
    padding: 0.25rem 0.6rem;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    display: inline-block;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #0f3460, #e94560);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 600;
    padding: 0.5rem 1.5rem;
    transition: opacity 0.2s;
}
.stButton > button:hover { opacity: 0.88; }

/* Section header */
.section-title {
    font-size: 1.4rem;
    font-weight: 700;
    color: #0f3460;
    border-bottom: 2px solid #e94560;
    padding-bottom: 0.4rem;
    margin-bottom: 1rem;
}
</style>
""",
    unsafe_allow_html=True,
)

# ── Session state initialisation ─────────────────────────────────────────────

def _init_session():
    defaults = {
        "agent": None,
        "messages": [],
        "user_profile": {
            "name": "",
            "age": 25,
            "gender": "Male",
            "weight": 70,
            "height": 170,
            "goal": "Maintain weight",
            "diet_type": "No restriction",
            "allergies": "None",
            "medical": "None",
            "activity": "Moderately active (3-5 days/week)",
            "cuisine": "Any",
            "plan_days": 7,
        },
        "meal_plan": "",
        "profile_saved": False,
        "feedback_history": [],
        "active_page": "💬 Chat",
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


_init_session()


def get_agent() -> NutritionAgent:
    if st.session_state.agent is None:
        st.session_state.agent = NutritionAgent()
    return st.session_state.agent


# ── Sidebar — User Profile ────────────────────────────────────────────────────

def render_sidebar():
    with st.sidebar:
        st.markdown("## 🥦 NutriGenius")
        st.markdown('<span class="ibm-badge">Powered by IBM Granite</span>', unsafe_allow_html=True)
        st.markdown("---")

        st.markdown("### 👤 Your Profile")
        p = st.session_state.user_profile

        p["name"] = st.text_input("Name", value=p["name"], placeholder="e.g. Priya")
        p["age"] = st.number_input("Age", min_value=5, max_value=110, value=p["age"])
        p["gender"] = st.selectbox("Gender", ["Male", "Female", "Other"],
                                   index=["Male", "Female", "Other"].index(p["gender"]))

        col1, col2 = st.columns(2)
        with col1:
            p["weight"] = st.number_input("Weight (kg)", 20.0, 300.0, float(p["weight"]), 0.5)
        with col2:
            p["height"] = st.number_input("Height (cm)", 100.0, 250.0, float(p["height"]), 0.5)

        p["goal"] = st.selectbox(
            "🎯 Health Goal",
            ["Lose weight", "Maintain weight", "Gain muscle", "Improve energy",
             "Manage diabetes", "Heart health", "Gut health", "Build endurance"],
            index=["Lose weight", "Maintain weight", "Gain muscle", "Improve energy",
                   "Manage diabetes", "Heart health", "Gut health", "Build endurance"].index(p["goal"]),
        )

        p["diet_type"] = st.selectbox(
            "🥗 Diet Preference",
            ["No restriction", "Vegetarian", "Vegan", "Keto", "Paleo",
             "Gluten-free", "Dairy-free", "Low-carb", "Mediterranean", "Jain"],
            index=["No restriction", "Vegetarian", "Vegan", "Keto", "Paleo",
                   "Gluten-free", "Dairy-free", "Low-carb", "Mediterranean", "Jain"].index(p["diet_type"]),
        )

        p["activity"] = st.selectbox(
            "🏃 Activity Level",
            ["Sedentary (little/no exercise)", "Lightly active (1-3 days/week)",
             "Moderately active (3-5 days/week)", "Very active (6-7 days/week)",
             "Extra active (athlete / physical job)"],
        )

        p["cuisine"] = st.selectbox(
            "🍛 Preferred Cuisine",
            ["Any", "Indian", "Mediterranean", "East Asian", "Latin American",
             "Middle Eastern", "Western", "African", "South-East Asian"],
        )

        p["allergies"] = st.text_input("⚠️ Allergies / Intolerances",
                                        value=p["allergies"],
                                        placeholder="e.g. nuts, gluten, dairy")
        p["medical"] = st.text_input("🏥 Medical Conditions",
                                      value=p["medical"],
                                      placeholder="e.g. Type 2 diabetes, hypertension")

        if st.button("💾 Save Profile", use_container_width=True):
            st.session_state.profile_saved = True
            st.session_state.agent = None  # reset agent so profile is fresh
            st.success("✅ Profile saved!")

        st.markdown("---")

        # Calorie estimate preview
        calories = estimate_calories(p)
        st.markdown(
            f'<div class="metric-card"><h3>{calories}</h3><p>Daily Calorie Target (kcal)</p></div>',
            unsafe_allow_html=True,
        )

        st.markdown("---")
        st.markdown("### 🗂️ Navigation")
        page = st.radio(
            "Go to",
            ["💬 Chat", "🗓️ Meal Plan", "🔄 Food Swaps", "📸 Image Analysis",
             "📊 Nutrition Dashboard", "📚 Learn Nutrition"],
            label_visibility="collapsed",
        )
        st.session_state.active_page = page

        # IBM watermark
        st.markdown("---")
        agent = get_agent()
        if agent.is_demo():
            st.warning("⚙️ Demo Mode — add IBM API key to unlock full AI")
        else:
            st.success("🟢 IBM Granite Connected")


# ── Pages ─────────────────────────────────────────────────────────────────────

def page_chat():
    st.markdown(
        '<div class="hero-banner">'
        '<h1>🥦 NutriGenius</h1>'
        '<p>Your personal AI nutrition coach — powered by <strong>IBM Granite</strong> on watsonx.ai</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    agent = get_agent()
    profile = st.session_state.user_profile

    # Greeting on first load
    if not st.session_state.messages:
        name = profile.get("name") or "there"
        greeting = (
            f"👋 Hello **{name}**! I'm NutriGenius, your AI nutrition assistant powered by "
            f"**IBM Granite**.\n\n"
            "I can help you with:\n"
            "- 🥗 **Personalized meal plans** based on your goals\n"
            "- 🔄 **Smart food swaps** for healthier choices\n"
            "- 📸 **Food photo / label analysis** (upload in Image Analysis tab)\n"
            "- 📚 **Nutrition science** explained simply\n"
            "- 💬 **Any nutrition question** you have\n\n"
            "What would you like to explore today?"
        )
        st.session_state.messages.append({"role": "assistant", "content": greeting})

    # Display conversation
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(
                f'<div class="chat-user">👤 <strong>You</strong><br>{msg["content"]}</div>',
                unsafe_allow_html=True,
            )
        else:
            with st.container():
                st.markdown(
                    f'<div class="chat-ai">🥦 <strong>NutriGenius</strong></div>',
                    unsafe_allow_html=True,
                )
                st.markdown(msg["content"])

    # Quick-action buttons
    st.markdown("**Quick actions:**")
    qcols = st.columns(4)
    quick_prompts = [
        ("🥗 Suggest Breakfast", "Suggest a healthy breakfast for my goal"),
        ("💧 Hydration Tips", "How much water should I drink daily?"),
        ("🧪 Protein Guide", "How much protein do I need per day?"),
        ("😴 Sleep & Nutrition", "How does sleep affect my nutrition and weight?"),
    ]
    for col, (label, prompt_text) in zip(qcols, quick_prompts):
        with col:
            if st.button(label, use_container_width=True, key=f"qbtn_{label}"):
                _send_message(agent, profile, prompt_text)
                st.rerun()

    # Input area
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_area(
            "Ask NutriGenius anything…",
            placeholder="e.g. What should I eat before a morning workout?",
            height=80,
            label_visibility="collapsed",
        )
        submitted = st.form_submit_button("📤 Send", use_container_width=True)

    if submitted and user_input.strip():
        _send_message(agent, profile, user_input.strip())
        st.rerun()


def _send_message(agent: NutritionAgent, profile: dict, text: str):
    st.session_state.messages.append({"role": "user", "content": text})
    with st.spinner("NutriGenius is thinking…"):
        response = agent.chat(text, profile, st.session_state.messages[:-1])
    st.session_state.messages.append({"role": "assistant", "content": response})
    # store for feedback loop
    st.session_state.feedback_history.append({"q": text, "a": response, "rating": None})


def page_meal_plan():
    st.markdown('<div class="section-title">🗓️ Personalized Meal Plan</div>', unsafe_allow_html=True)

    profile = st.session_state.user_profile
    agent = get_agent()
    calories = estimate_calories(profile)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            f'<div class="metric-card"><h3>{calories}</h3><p>Daily Calories</p></div>',
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f'<div class="metric-card"><h3>{profile.get("goal","—")}</h3><p>Health Goal</p></div>',
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            f'<div class="metric-card"><h3>{profile.get("diet_type","—")}</h3><p>Diet Type</p></div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")

    plan_days = st.slider("Number of days to plan", 1, 7, int(profile.get("plan_days", 7)))
    profile["plan_days"] = plan_days

    if st.button("🚀 Generate My Meal Plan", use_container_width=True):
        with st.spinner("IBM Granite is crafting your personalized meal plan…"):
            plan = generate_meal_plan(agent, profile)
            st.session_state.meal_plan = plan

    if st.session_state.meal_plan:
        st.markdown(st.session_state.meal_plan)

        st.markdown("---")
        st.markdown("#### 📥 Download Plan")
        st.download_button(
            label="⬇️ Download as Markdown",
            data=st.session_state.meal_plan,
            file_name="nutrigenius_meal_plan.md",
            mime="text/markdown",
            use_container_width=True,
        )

        # Feedback
        st.markdown("#### 💬 Feedback on This Plan")
        fb_col1, fb_col2 = st.columns(2)
        with fb_col1:
            if st.button("👍 Looks great!", use_container_width=True, key="mp_pos"):
                st.success("Thanks! Positive feedback recorded.")
        with fb_col2:
            if st.button("✏️ Needs adjustment", use_container_width=True, key="mp_neg"):
                tweak = st.text_input("What would you like changed?", key="mp_tweak")
                if tweak:
                    with st.spinner("Adjusting plan…"):
                        adjusted = agent.chat(
                            f"Please adjust the meal plan with this feedback: {tweak}",
                            profile,
                            [{"role": "assistant", "content": st.session_state.meal_plan}],
                        )
                        st.session_state.meal_plan = adjusted
                    st.rerun()


def page_food_swaps():
    st.markdown('<div class="section-title">🔄 Smart Food Swaps</div>', unsafe_allow_html=True)

    agent = get_agent()
    profile = st.session_state.user_profile

    st.markdown(
        "Enter any food item and NutriGenius will suggest healthier alternatives "
        "tailored to your goals and dietary needs."
    )

    food_item = st.text_input(
        "Food item to swap",
        placeholder="e.g. white rice, butter, soda, chips, white bread…",
    )

    if st.button("🔄 Find Smart Swaps", use_container_width=True) and food_item.strip():
        with st.spinner(f"Finding healthier alternatives for **{food_item}**…"):
            result = get_food_swap(agent, food_item.strip(), profile)
        st.markdown(result)

    st.markdown("---")
    st.markdown("### 📚 Explain a Nutrition Topic")
    topic = st.text_input(
        "Nutrition topic",
        placeholder="e.g. Omega-3, glycemic index, intermittent fasting, gut microbiome…",
    )
    if st.button("📖 Explain It", use_container_width=True) and topic.strip():
        with st.spinner(f"Generating nutrition explainer for **{topic}**…"):
            explanation = explain_nutrition(agent, topic.strip(), profile)
        st.markdown(explanation)


def page_image_analysis():
    st.markdown('<div class="section-title">📸 Food Image & Label Analysis</div>', unsafe_allow_html=True)

    profile = st.session_state.user_profile
    agent = get_agent()

    st.markdown(
        "Upload a **food photo** or **nutrition label** image. "
        "IBM Granite Vision will identify ingredients, parse nutritional facts, "
        "flag allergens, and assess the food against your health goals."
    )

    uploaded = st.file_uploader(
        "Choose an image",
        type=["jpg", "jpeg", "png", "webp", "bmp"],
        help="Supported: JPG, PNG, WebP, BMP",
    )

    if uploaded is not None:
        image = Image.open(uploaded)
        col_img, col_result = st.columns([1, 2])

        with col_img:
            st.image(image, caption="Uploaded Image", use_column_width=True)

        with col_result:
            if st.button("🔍 Analyze This Image", use_container_width=True):
                with st.spinner("IBM Granite Vision analyzing your image…"):
                    result = analyze_food_image(image, profile, agent.is_demo())
                st.markdown(result)


def page_dashboard():
    st.markdown('<div class="section-title">📊 Nutrition Dashboard</div>', unsafe_allow_html=True)

    profile = st.session_state.user_profile
    calories = estimate_calories(profile)

    # Macro distribution chart
    goal = profile.get("goal", "Maintain weight")
    # Macro ratios by goal
    macro_ratios = {
        "Lose weight":     {"Protein": 35, "Carbs": 35, "Fat": 30},
        "Maintain weight": {"Protein": 25, "Carbs": 50, "Fat": 25},
        "Gain muscle":     {"Protein": 40, "Carbs": 40, "Fat": 20},
        "Improve energy":  {"Protein": 20, "Carbs": 55, "Fat": 25},
        "Manage diabetes": {"Protein": 30, "Carbs": 30, "Fat": 40},
        "Heart health":    {"Protein": 25, "Carbs": 45, "Fat": 30},
        "Gut health":      {"Protein": 25, "Carbs": 50, "Fat": 25},
        "Build endurance": {"Protein": 20, "Carbs": 60, "Fat": 20},
    }
    ratios = macro_ratios.get(goal, {"Protein": 25, "Carbs": 50, "Fat": 25})

    protein_g = int(calories * ratios["Protein"] / 100 / 4)
    carbs_g = int(calories * ratios["Carbs"] / 100 / 4)
    fat_g = int(calories * ratios["Fat"] / 100 / 9)

    col1, col2 = st.columns(2)

    with col1:
        fig_pie = go.Figure(
            data=[
                go.Pie(
                    labels=["Protein", "Carbohydrates", "Fat"],
                    values=[ratios["Protein"], ratios["Carbs"], ratios["Fat"]],
                    hole=0.45,
                    marker_colors=["#0f3460", "#e94560", "#16213e"],
                    textinfo="label+percent",
                )
            ]
        )
        fig_pie.update_layout(
            title=f"Macro Distribution for: {goal}",
            showlegend=False,
            height=320,
            margin=dict(t=40, b=10, l=10, r=10),
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        fig_bar = go.Figure(
            data=[
                go.Bar(
                    x=["Protein", "Carbohydrates", "Fat"],
                    y=[protein_g, carbs_g, fat_g],
                    marker_color=["#0f3460", "#e94560", "#16213e"],
                    text=[f"{protein_g}g", f"{carbs_g}g", f"{fat_g}g"],
                    textposition="outside",
                )
            ]
        )
        fig_bar.update_layout(
            title="Daily Macro Targets (grams)",
            yaxis_title="Grams",
            height=320,
            margin=dict(t=40, b=10, l=10, r=10),
            plot_bgcolor="white",
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # BMI & health indicators
    st.markdown("### 📋 Health Metrics")
    try:
        weight = float(profile.get("weight", 70))
        height_cm = float(profile.get("height", 170))
        bmi = weight / ((height_cm / 100) ** 2)
        if bmi < 18.5:
            bmi_cat, bmi_color = "Underweight", "#f59e0b"
        elif bmi < 25:
            bmi_cat, bmi_color = "Normal weight", "#10b981"
        elif bmi < 30:
            bmi_cat, bmi_color = "Overweight", "#f59e0b"
        else:
            bmi_cat, bmi_color = "Obese", "#ef4444"
    except (TypeError, ValueError, ZeroDivisionError):
        bmi, bmi_cat, bmi_color = 0, "N/A", "#94a3b8"

    m1, m2, m3, m4 = st.columns(4)
    metrics = [
        (m1, f"{calories} kcal", "Daily Calories"),
        (m2, f"{bmi:.1f}", f"BMI — {bmi_cat}"),
        (m3, f"{protein_g}g", "Protein / day"),
        (m4, f"{carbs_g}g", "Carbs / day"),
    ]
    for col, val, label in metrics:
        with col:
            st.markdown(
                f'<div class="metric-card"><h3>{val}</h3><p>{label}</p></div>',
                unsafe_allow_html=True,
            )

    # Nutrient checklist
    st.markdown("---")
    st.markdown("### ✅ Key Nutrients to Monitor")
    nutrients = {
        "Fiber": ("25–38g/day", "Digestive health, blood sugar control"),
        "Sodium": ("<2300mg/day", "Heart health, blood pressure"),
        "Calcium": ("1000–1200mg/day", "Bone strength, muscle function"),
        "Iron": ("8–18mg/day", "Oxygen transport, energy"),
        "Vitamin D": ("600–800 IU/day", "Immunity, bone health"),
        "Omega-3": ("1.1–1.6g/day", "Brain, heart, inflammation"),
        "Potassium": ("3500–4700mg/day", "Blood pressure, muscle cramps"),
        "Magnesium": ("310–420mg/day", "Sleep, muscle recovery, energy"),
    }
    cols = st.columns(2)
    for i, (nutrient, (rda, benefit)) in enumerate(nutrients.items()):
        with cols[i % 2]:
            st.markdown(f"**{nutrient}** — `{rda}`  \n*{benefit}*")


def page_learn():
    st.markdown('<div class="section-title">📚 Learn Nutrition</div>', unsafe_allow_html=True)

    topics = {
        "🔥 Macronutrients 101": "proteins, carbohydrates, fats, macronutrients basics",
        "💊 Micronutrients": "vitamins, minerals, micronutrients deficiencies",
        "🩺 Nutrition for Weight Loss": "calorie deficit, metabolism, fat loss science",
        "💪 Sports Nutrition": "pre-workout, post-workout, protein timing, muscle gain",
        "🩸 Diabetes & Diet": "glycemic index, carbohydrate counting, blood sugar management",
        "❤️ Heart-Healthy Eating": "saturated fat, cholesterol, DASH diet, Mediterranean diet",
        "🌱 Plant-Based Nutrition": "vegan protein sources, B12, iron, zinc plant-based",
        "🧠 Brain & Gut Health": "gut microbiome, probiotics, prebiotics, omega-3 brain",
    }

    agent = get_agent()
    profile = st.session_state.user_profile

    selected = st.selectbox("Choose a topic to learn about:", list(topics.keys()))
    if st.button("📖 Explain This Topic", use_container_width=True):
        with st.spinner(f"IBM Granite is preparing an explanation on **{selected}**…"):
            explanation = explain_nutrition(agent, topics[selected], profile)
        st.markdown(explanation)


# ── Router ────────────────────────────────────────────────────────────────────

def main():
    render_sidebar()

    page = st.session_state.active_page

    if page == "💬 Chat":
        page_chat()
    elif page == "🗓️ Meal Plan":
        page_meal_plan()
    elif page == "🔄 Food Swaps":
        page_food_swaps()
    elif page == "📸 Image Analysis":
        page_image_analysis()
    elif page == "📊 Nutrition Dashboard":
        page_dashboard()
    elif page == "📚 Learn Nutrition":
        page_learn()


if __name__ == "__main__":
    main()
