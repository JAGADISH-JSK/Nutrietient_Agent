"""
food_advisor.py
Food swap recommendations and nutritional explanations via IBM Granite.
"""

from nutrition_agent import NutritionAgent


# ---------------------------------------------------------------------------
# Food Swap Advisor
# ---------------------------------------------------------------------------

COMMON_SWAPS = {
    "white rice": ("Brown rice or quinoa", "Higher fiber, lower glycemic index — better blood sugar control."),
    "white bread": ("Whole wheat or sourdough bread", "More fiber, B vitamins, and a slower energy release."),
    "butter": ("Avocado or olive oil", "Replaces saturated fat with heart-healthy monounsaturated fats."),
    "soda": ("Sparkling water with lemon or herbal iced tea", "Eliminates 150+ kcal of added sugar per serving."),
    "chips": ("Air-popped popcorn or roasted chickpeas", "Lower fat, more fiber, and satisfying crunch."),
    "mayonnaise": ("Greek yogurt or hummus", "Cuts fat significantly while adding protein and probiotics."),
    "sugar": ("Dates, honey, or stevia", "Lower glycemic impact; dates add fiber and minerals."),
    "cow milk": ("Oat milk or almond milk", "Lower in saturated fat; oat milk adds beta-glucan fiber."),
    "ice cream": ("Frozen banana nice cream", "Zero added sugar; natural sweetness + potassium."),
    "fried chicken": ("Baked herb-crusted chicken", "Reduces calories by ~40% while keeping protein high."),
    "cream cheese": ("Low-fat ricotta or cottage cheese", "More protein, less saturated fat."),
    "pasta": ("Zucchini noodles or lentil pasta", "Fewer carbs; lentil pasta doubles the protein."),
}


def get_food_swap(agent: NutritionAgent, food_item: str, profile: dict) -> str:
    """Get a smart food swap recommendation for the given food item."""
    # Quick lookup for common items
    food_lower = food_item.lower().strip()
    for key, (swap, reason) in COMMON_SWAPS.items():
        if key in food_lower:
            if agent.is_demo():
                return _format_quick_swap(food_item, swap, reason)

    # Use the LLM for anything not in the quick-lookup
    if agent.is_demo():
        return _demo_swap(food_item, profile)

    goal = profile.get("goal", "healthy eating")
    diet = profile.get("diet_type", "No restriction")
    allergies = profile.get("allergies", "None")
    medical = profile.get("medical", "None")

    prompt = f"""Suggest 3 smart food swaps for "{food_item}" for a person with:
- Health Goal: {goal}
- Diet: {diet}
- Allergies: {allergies}
- Medical Conditions: {medical}

For each swap provide:
1. The replacement food
2. Why it's better (nutritional science)
3. How to use it (practical tip)
4. Approximate calorie/macro change

Format as a clear markdown list with headers."""

    return agent.chat(prompt, profile, [])


def _format_quick_swap(food_item: str, swap: str, reason: str) -> str:
    return (
        f"## 🔄 Smart Swap: {food_item.title()}\n\n"
        f"### ✅ Try Instead: **{swap}**\n\n"
        f"**Why it's better:**\n{reason}\n\n"
        f"> 💡 *Enable IBM Granite AI for personalized swaps based on your health goals, allergies, and cultural preferences.*"
    )


def _demo_swap(food_item: str, profile: dict) -> str:
    goal = profile.get("goal", "healthy eating") if profile else "healthy eating"
    return (
        f"## 🔄 Smart Swaps for: **{food_item}** *(Demo Mode)*\n\n"
        f"**Your Goal:** {goal}\n\n"
        "### Option 1 — Lower Calorie\n"
        f"Replace **{food_item}** with a lighter whole-food alternative that preserves satiety.\n\n"
        "### Option 2 — Higher Protein\n"
        f"Swap **{food_item}** for a protein-rich variant to support muscle maintenance.\n\n"
        "### Option 3 — Better Nutrients\n"
        f"Choose a nutrient-dense version of **{food_item}** with added vitamins and minerals.\n\n"
        "> *Enable IBM Granite AI for specific, science-backed swaps tailored to your profile.*"
    )


# ---------------------------------------------------------------------------
# Nutritional Explainer
# ---------------------------------------------------------------------------

def explain_nutrition(agent: NutritionAgent, topic: str, profile: dict) -> str:
    """Explain a nutrition topic in the context of the user's profile."""
    if agent.is_demo():
        return _demo_explanation(topic, profile)

    goal = profile.get("goal", "general health")
    medical = profile.get("medical", "None")

    prompt = f"""Explain the following nutrition topic clearly and scientifically: "{topic}"

Tailor the explanation to someone with:
- Health Goal: {goal}
- Medical Conditions: {medical}

Structure your response with:
1. **What it is** — simple definition
2. **Why it matters** — health benefits/risks
3. **How much do I need?** — recommended amounts
4. **Best food sources** — top 5 with quantities
5. **Practical tip** — one actionable advice
6. **Watch out for** — common myths or mistakes

Use markdown formatting with bold headers."""

    return agent.chat(prompt, profile, [])


def _demo_explanation(topic: str, profile: dict) -> str:
    goal = profile.get("goal", "healthy eating") if profile else "healthy eating"
    return (
        f"## 📚 Nutrition Explainer: **{topic}** *(Demo Mode)*\n\n"
        f"*Personalized for goal: {goal}*\n\n"
        "### 1. What It Is\n"
        f"**{topic}** is an essential nutritional concept with significant impact on overall health and wellbeing.\n\n"
        "### 2. Why It Matters\n"
        "Adequate intake supports energy levels, immune function, and long-term disease prevention.\n\n"
        "### 3. How Much Do I Need?\n"
        "Recommended amounts vary by age, gender, and health status. General guidelines suggest a balanced, varied diet.\n\n"
        "### 4. Best Food Sources\n"
        "- Whole grains, legumes, vegetables\n"
        "- Lean proteins (chicken, fish, tofu)\n"
        "- Nuts and seeds\n"
        "- Fresh fruits\n"
        "- Low-fat dairy or fortified plant milks\n\n"
        "### 5. Practical Tip\n"
        "Focus on adding nutrient-dense foods rather than eliminating food groups.\n\n"
        "> *Enable IBM Granite AI for a detailed, evidence-based explanation personalized to your medical history.*"
    )
