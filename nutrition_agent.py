"""
nutrition_agent.py
Core IBM Granite-powered Nutrition Agent using ibm-watsonx-ai SDK.
"""

import os
from dotenv import load_dotenv
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams

load_dotenv()


class NutritionAgent:
    """
    Core agent that wraps IBM Granite via watsonx.ai to answer
    nutrition queries with a health-aware system persona.
    """

    SYSTEM_PROMPT = """You are NutriGenius, an expert AI nutrition assistant powered by IBM Granite.
You provide evidence-based, personalized nutrition guidance. You:
- Create detailed, culturally sensitive meal plans.
- Offer smart food-swap recommendations.
- Explain the nutritional science behind every suggestion.
- Adapt dynamically to user feedback, allergies, and medical conditions.
- Always recommend consulting a registered dietician for serious medical conditions.
- Use plain, empathetic language suitable for all literacy levels.
Respond in markdown with clear sections, bullet points, and tables where relevant."""

    # Supported models in IBM Cloud Lite (as of 2025)
    SUPPORTED_MODELS = [
        "ibm/granite-4-h-small",
        "ibm/granite-3-1-8b-base",
        "meta-llama/llama-3-3-70b-instruct",
        "meta-llama/llama-3-1-8b",
        "mistralai/mistral-small-3-1-24b-instruct-2503",
    ]

    def __init__(self):
        api_key = os.getenv("WATSONX_API_KEY", "")
        project_id = os.getenv("WATSONX_PROJECT_ID", "")
        url = os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")
        model_id = os.getenv("GRANITE_MODEL_ID", "ibm/granite-4-h-small")

        # Validate model; fall back to a known-good supported model
        if model_id not in self.SUPPORTED_MODELS:
            model_id = "ibm/granite-4-h-small"

        self._demo_mode = not (api_key and api_key != "your_ibm_cloud_api_key_here")

        if not self._demo_mode:
            credentials = Credentials(api_key=api_key, url=url)
            self._model = ModelInference(
                model_id=model_id,
                credentials=credentials,
                project_id=project_id,
                params={
                    GenParams.DECODING_METHOD: "greedy",
                    GenParams.MAX_NEW_TOKENS: 1024,
                    GenParams.MIN_NEW_TOKENS: 50,
                    GenParams.TEMPERATURE: 0.7,
                    GenParams.TOP_P: 0.9,
                    GenParams.REPETITION_PENALTY: 1.1,
                },
            )
        else:
            self._model = None

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _build_prompt(self, user_profile: dict, conversation: list, user_message: str) -> str:
        """Construct a full prompt with system context, profile, and history."""
        profile_block = ""
        if user_profile:
            lines = []
            if user_profile.get("name"):
                lines.append(f"Name: {user_profile['name']}")
            if user_profile.get("age"):
                lines.append(f"Age: {user_profile['age']}")
            if user_profile.get("weight"):
                lines.append(f"Weight: {user_profile['weight']} kg")
            if user_profile.get("height"):
                lines.append(f"Height: {user_profile['height']} cm")
            if user_profile.get("goal"):
                lines.append(f"Health Goal: {user_profile['goal']}")
            if user_profile.get("diet_type"):
                lines.append(f"Diet Preference: {user_profile['diet_type']}")
            if user_profile.get("allergies"):
                lines.append(f"Allergies / Intolerances: {user_profile['allergies']}")
            if user_profile.get("medical"):
                lines.append(f"Medical Conditions: {user_profile['medical']}")
            if user_profile.get("activity"):
                lines.append(f"Activity Level: {user_profile['activity']}")
            if user_profile.get("cuisine"):
                lines.append(f"Preferred Cuisine: {user_profile['cuisine']}")
            profile_block = "\n[USER PROFILE]\n" + "\n".join(lines) + "\n"

        history_block = ""
        if conversation:
            history_lines = []
            for msg in conversation[-6:]:  # last 3 exchanges
                role = "User" if msg["role"] == "user" else "NutriGenius"
                history_lines.append(f"{role}: {msg['content']}")
            history_block = "\n[CONVERSATION HISTORY]\n" + "\n".join(history_lines) + "\n"

        prompt = (
            f"{self.SYSTEM_PROMPT}\n"
            f"{profile_block}"
            f"{history_block}"
            f"\n[CURRENT USER MESSAGE]\n{user_message}\n\n"
            f"NutriGenius:"
        )
        return prompt

    def _demo_response(self, user_message: str, user_profile: dict) -> str:
        """Return a structured demo response when no API key is configured."""
        name = user_profile.get("name", "there") if user_profile else "there"
        goal = user_profile.get("goal", "healthy eating") if user_profile else "healthy eating"
        return (
            f"## 👋 Hello {name}! *(Demo Mode — configure `.env` to enable IBM Granite)*\n\n"
            f"You asked: **\"{user_message}\"**\n\n"
            f"Based on your goal of **{goal}**, here is a quick overview of what I can do:\n\n"
            "### 🥗 What NutriGenius Can Do For You\n"
            "| Feature | Description |\n"
            "|---|---|\n"
            "| **Meal Plans** | 7-day personalized plans tailored to your calories, preferences & culture |\n"
            "| **Food Swaps** | Smart ingredient substitutions for your dietary needs |\n"
            "| **Nutrition Q&A** | Science-backed answers to any nutrition question |\n"
            "| **Label Analysis** | Upload a food label photo for instant nutritional breakdown |\n"
            "| **Progress Tracking** | Log meals and get adaptive feedback |\n\n"
            "### 🚀 To enable full IBM Granite AI:\n"
            "1. Get a free IBM Cloud account at [cloud.ibm.com](https://cloud.ibm.com)\n"
            "2. Create a **watsonx.ai** project\n"
            "3. Copy your **API Key** and **Project ID** into `env.txt` → rename to `.env`\n\n"
            "> 💡 *IBM Granite is IBM's enterprise-grade open-source LLM — trained responsibly and "
            "optimized for trust and transparency.*"
        )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def chat(self, user_message: str, user_profile: dict, conversation: list) -> str:
        """Main entry point: send a message, get a response."""
        if self._demo_mode:
            return self._demo_response(user_message, user_profile)

        prompt = self._build_prompt(user_profile, conversation, user_message)
        try:
            response = self._model.generate_text(prompt=prompt)
            return response.strip()
        except Exception as exc:  # noqa: BLE001
            return (
                f"⚠️ **IBM Granite API Error:** {exc}\n\n"
                "Please verify your `WATSONX_API_KEY`, `WATSONX_PROJECT_ID`, and `WATSONX_URL` "
                "in your `.env` file."
            )

    def is_demo(self) -> bool:
        return self._demo_mode
