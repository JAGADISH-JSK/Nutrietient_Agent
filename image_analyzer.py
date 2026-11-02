"""
image_analyzer.py
Food label / photo analysis using IBM Granite Vision model.
Falls back to OCR-based text extraction when vision model is unavailable.
"""

import os
import io
import base64
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

# Optional tesseract OCR fallback
try:
    import pytesseract
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False

try:
    from ibm_watsonx_ai import Credentials
    from ibm_watsonx_ai.foundation_models import ModelInference
    from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
    IBM_SDK_AVAILABLE = True
except ImportError:
    IBM_SDK_AVAILABLE = False


def _image_to_base64(image: Image.Image, fmt: str = "JPEG") -> str:
    buf = io.BytesIO()
    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")
    image.save(buf, format=fmt)
    return base64.b64encode(buf.getvalue()).decode("utf-8")


def _ocr_extract(image: Image.Image) -> str:
    if not OCR_AVAILABLE:
        return ""
    try:
        return pytesseract.image_to_string(image)
    except Exception:  # noqa: BLE001
        return ""


def analyze_food_image(image: Image.Image, profile: dict, agent_demo: bool = True) -> str:
    """
    Analyze a food photo or nutrition label image.
    Uses Granite Vision when available; falls back to OCR + text Granite.
    """
    api_key = os.getenv("WATSONX_API_KEY", "")
    project_id = os.getenv("WATSONX_PROJECT_ID", "")
    url = os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")
    vision_model_id = os.getenv("GRANITE_VISION_MODEL_ID", "ibm/granite-4-h-small")

    goal = profile.get("goal", "healthy eating") if profile else "healthy eating"
    allergies = profile.get("allergies", "None") if profile else "None"
    diet = profile.get("diet_type", "No restriction") if profile else "No restriction"

    is_real = (
        IBM_SDK_AVAILABLE
        and api_key
        and api_key != "your_ibm_cloud_api_key_here"
        and project_id
    )

    if is_real:
        return _granite_vision_analyze(
            image, api_key, project_id, url, vision_model_id,
            goal, allergies, diet
        )

    # --- Demo / OCR fallback ---
    ocr_text = _ocr_extract(image)
    return _demo_analysis(image, ocr_text, goal, allergies, diet)


def _granite_vision_analyze(
    image: Image.Image,
    api_key: str, project_id: str, url: str, model_id: str,
    goal: str, allergies: str, diet: str,
) -> str:
    """Call Granite Vision model with the image."""
    try:
        credentials = Credentials(api_key=api_key, url=url)
        model = ModelInference(
            model_id=model_id,
            credentials=credentials,
            project_id=project_id,
            params={
                GenParams.MAX_NEW_TOKENS: 800,
                GenParams.TEMPERATURE: 0.3,
            },
        )
        img_b64 = _image_to_base64(image)
        prompt = (
            "You are a nutrition expert. Analyze this food image or nutrition label.\n"
            f"User goal: {goal} | Allergies: {allergies} | Diet: {diet}\n\n"
            "Provide:\n"
            "1. Food identification / label reading\n"
            "2. Key nutritional facts (calories, protein, carbs, fat, fiber, sodium)\n"
            "3. Health assessment for this user's goal\n"
            "4. Specific concerns (allergens, additives, sugar content)\n"
            "5. Recommendation: Eat / Limit / Avoid — with reason\n\n"
            "Use markdown formatting."
        )
        response = model.generate_text(
            prompt=prompt,
            images=[{"type": "base64", "data": img_b64, "media_type": "image/jpeg"}],
        )
        return response.strip()
    except Exception as exc:  # noqa: BLE001
        return f"⚠️ **Vision API Error:** {exc}\n\nFalling back to OCR analysis."


def _demo_analysis(
    image: Image.Image, ocr_text: str, goal: str, allergies: str, diet: str
) -> str:
    width, height = image.size
    mode = image.mode
    has_text = bool(ocr_text.strip())

    ocr_section = ""
    if has_text:
        # Show first 400 chars of extracted text
        preview = ocr_text.strip()[:400]
        ocr_section = f"\n### 🔍 Extracted Text (OCR)\n```\n{preview}\n```\n"

    return (
        f"## 📸 Food Image Analysis *(Demo Mode)*\n\n"
        f"**Image:** {width}×{height}px | Mode: {mode}\n\n"
        f"{ocr_section}"
        f"### 🎯 Analysis for Your Profile\n"
        f"- **Goal:** {goal}\n"
        f"- **Diet:** {diet}\n"
        f"- **Allergies:** {allergies}\n\n"
        "### 🍽️ What IBM Granite Vision Would Tell You\n"
        "- Identify all visible food items with portion estimates\n"
        "- Read and parse the full nutrition facts label\n"
        "- Flag allergens and ingredients to avoid\n"
        "- Score the meal against your calorie target\n"
        "- Suggest improvements or healthier alternatives\n\n"
        "### ✅ How to Enable\n"
        "1. Add your `WATSONX_API_KEY` and `WATSONX_PROJECT_ID` to `.env`\n"
        "2. Ensure `GRANITE_VISION_MODEL_ID=ibm/granite-vision-8b-8192` is set\n"
        "3. Restart the app — image analysis will use full Granite Vision AI\n\n"
        "> 💡 *IBM Granite Vision can read nutrition labels, identify portion sizes, "
        "and flag hidden allergens from a photo — no manual entry needed.*"
    )
