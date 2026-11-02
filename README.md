# 🥦 NutriGenius — AI Nutrition Assistant
### Powered by IBM Granite on watsonx.ai

> **AICTE Internship Project — Problem Statement #8: Nutrition Agent**  
> Developed using **IBM Cloud Lite** services & **IBM Granite** LLM (mandatory requirement)

---

## 📋 Overview

NutriGenius is an intelligent, interactive, and adaptive virtual nutrition assistant built with:
- **IBM Granite** (via `ibm-watsonx-ai` SDK) as the core reasoning engine
- **Streamlit** for a beautiful, responsive web interface
- **Multimodal understanding** — text, and food image / nutrition label analysis
- **Personalized meal plans** tailored to health goals, allergies, culture, and medical conditions
- **Smart food swaps** backed by nutritional science
- **Interactive nutrition explainer** and learning hub
- **Real-time adaptive feedback** loop

---

## 🏗️ Project Structure

```
AICTE-Nutrietient-folder/
│
├── app.py                  # Main Streamlit application (UI + routing)
├── nutrition_agent.py      # IBM Granite LLM wrapper (NutritionAgent class)
├── meal_planner.py         # 7-day meal plan generation + calorie estimation
├── food_advisor.py         # Food swap recommendations + nutrition explainer
├── image_analyzer.py       # Food photo / label analysis (Granite Vision)
│
├── requirements.txt        # Python dependencies
├── env.txt                 # Environment variable template → rename to .env
├── .streamlit/
│   └── config.toml         # Streamlit theme configuration
└── README.md
```

---

## ⚙️ Setup & Installation

### 1. Clone / open the project
```bash
cd AICTE-Nutrietient-folder
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure IBM Granite credentials

Copy `env.txt` to `.env` and fill in your IBM Cloud details:

```bash
copy env.txt .env           # Windows
# cp env.txt .env           # macOS/Linux
```

Edit `.env`:
```
WATSONX_API_KEY=<your IBM Cloud API key>
WATSONX_PROJECT_ID=<your watsonx.ai project ID>
WATSONX_URL=https://us-south.ml.cloud.ibm.com
GRANITE_MODEL_ID=ibm/granite-13b-instruct-v2
GRANITE_VISION_MODEL_ID=ibm/granite-vision-8b-8192
```

#### 🆓 Get IBM Cloud Lite (Free) Account
1. Sign up at [cloud.ibm.com](https://cloud.ibm.com) — **no credit card required**
2. Search for **watsonx.ai** → create a project
3. Go to **API Keys** → create a new key
4. Copy your **Project ID** from the project settings

### 5. Run the app
```bash
streamlit run app.py
```

---

## 🖥️ Features

| Feature | Description |
|---|---|
| 💬 **AI Chat** | Natural language nutrition Q&A powered by IBM Granite |
| 🗓️ **Meal Plans** | Personalized 1–7 day plans with calories, macros, and prep tips |
| 🔄 **Food Swaps** | Science-backed ingredient substitutions |
| 📸 **Image Analysis** | Food photo / nutrition label parsing via Granite Vision |
| 📊 **Dashboard** | BMI, calorie targets, macro distribution charts |
| 📚 **Learn Nutrition** | In-depth explainers on any nutrition topic |
| ⚙️ **Demo Mode** | Works without API keys — shows all UI features immediately |

---

## 🧠 IBM Granite Models Used

| Model | Purpose |
|---|---|
| `ibm/granite-13b-instruct-v2` | Chat, meal planning, food swaps, explanations |
| `ibm/granite-vision-8b-8192` | Food image and nutrition label analysis |

---

## 🏛️ Architecture

```
User Input (text / image)
        │
        ▼
  Streamlit UI (app.py)
        │
        ├─── NutritionAgent (nutrition_agent.py)
        │         └── IBM Granite via watsonx.ai SDK
        │
        ├─── MealPlanner (meal_planner.py)
        │         └── Mifflin-St Jeor calorie estimation + Granite
        │
        ├─── FoodAdvisor (food_advisor.py)
        │         └── Smart swaps + nutrition explainer via Granite
        │
        └─── ImageAnalyzer (image_analyzer.py)
                  └── Granite Vision + OCR fallback
```

---

## 📦 Key Dependencies

- `ibm-watsonx-ai` — IBM Granite / watsonx.ai SDK
- `streamlit` — Web application framework
- `plotly` — Interactive nutrition charts
- `Pillow` — Image processing
- `python-dotenv` — Environment variable management
- `pytesseract` *(optional)* — OCR fallback for label text extraction

---

## 🔒 Demo Mode

If no `.env` file or API key is configured, the app runs in **Demo Mode**:
- All UI pages are fully functional
- Sample meal plans, swap suggestions, and explanations are shown
- A clear banner informs the user to configure IBM credentials
- No API calls are made

---

## 👨‍💻 Technologies

| Technology | Role |
|---|---|
| **IBM Granite (watsonx.ai)** | Core AI reasoning — mandatory per AICTE spec |
| **IBM Cloud Lite** | Free-tier hosting of watsonx.ai |
| **Streamlit** | Interactive web UI |
| **Python 3.10+** | Application runtime |
| **Plotly** | Data visualisation |
| **Pillow / Tesseract** | Image handling |

---

*Built for AICTE Internship 2024-25 — Problem Statement #8: Nutrition Agent*
