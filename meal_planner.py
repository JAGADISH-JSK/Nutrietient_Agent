"""
meal_planner.py
Generates structured 7-day meal plans using IBM Granite via NutritionAgent.
"""

from nutrition_agent import NutritionAgent


# ---------------------------------------------------------------------------
# Calorie estimation (Mifflin-St Jeor)
# ---------------------------------------------------------------------------

ACTIVITY_MULTIPLIERS = {
    "Sedentary (little/no exercise)": 1.2,
    "Lightly active (1-3 days/week)": 1.375,
    "Moderately active (3-5 days/week)": 1.55,
    "Very active (6-7 days/week)": 1.725,
    "Extra active (athlete / physical job)": 1.9,
}

GOAL_ADJUSTMENTS = {
    "Lose weight": -500,
    "Maintain weight": 0,
    "Gain muscle": +300,
    "Improve energy": 0,
    "Manage diabetes": -200,
    "Heart health": -100,
    "Gut health": 0,
    "Build endurance": +200,
}


def estimate_calories(profile: dict) -> int:
    """Estimate daily calorie target from user profile."""
    try:
        weight = float(profile.get("weight", 70))
        height = float(profile.get("height", 170))
        age = int(profile.get("age", 30))
        gender = profile.get("gender", "Male")
        activity = profile.get("activity", "Moderately active (3-5 days/week)")
        goal = profile.get("goal", "Maintain weight")

        # Mifflin-St Jeor BMR
        if gender == "Male":
            bmr = 10 * weight + 6.25 * height - 5 * age + 5
        else:
            bmr = 10 * weight + 6.25 * height - 5 * age - 161

        multiplier = ACTIVITY_MULTIPLIERS.get(activity, 1.55)
        tdee = bmr * multiplier
        adjustment = GOAL_ADJUSTMENTS.get(goal, 0)
        return max(1200, int(tdee + adjustment))
    except (TypeError, ValueError):
        return 2000


# ---------------------------------------------------------------------------
# Meal plan prompt builder
# ---------------------------------------------------------------------------

def build_meal_plan_prompt(profile: dict) -> str:
    calories = estimate_calories(profile)
    name = profile.get("name", "the user")
    goal = profile.get("goal", "healthy eating")
    diet = profile.get("diet_type", "No restriction")
    allergies = profile.get("allergies", "None")
    medical = profile.get("medical", "None")
    cuisine = profile.get("cuisine", "Any")
    days = profile.get("plan_days", 7)

    return f"""Generate a detailed {days}-day personalized meal plan for {name}.

**Health Profile:**
- Daily Calorie Target: {calories} kcal
- Health Goal: {goal}
- Diet Preference: {diet}
- Allergies/Intolerances: {allergies}
- Medical Conditions: {medical}
- Preferred Cuisine: {cuisine}

**Format Requirements:**
For each day provide:
1. Breakfast (with portion sizes and macros)
2. Mid-Morning Snack
3. Lunch (with portion sizes and macros)
4. Afternoon Snack
5. Dinner (with portion sizes and macros)
6. Daily totals: Calories | Protein | Carbs | Fat | Fiber

Use a markdown table for the daily summary.
Include brief preparation tips for at least one meal per day.
Respect all allergies and dietary restrictions strictly.
Make meals practical, affordable, and culturally appropriate for {cuisine} cuisine."""


def generate_meal_plan(agent: NutritionAgent, profile: dict) -> str:
    """Generate a meal plan by calling the agent with a structured prompt."""
    if agent.is_demo():
        calories = estimate_calories(profile)
        return _demo_meal_plan(profile, calories)

    prompt = build_meal_plan_prompt(profile)
    return agent.chat(prompt, profile, [])


def _demo_meal_plan(profile: dict, calories: int) -> str:
    name = profile.get("name", "User")
    goal = profile.get("goal", "Maintain weight")
    diet = profile.get("diet_type", "No restriction")

    return f"""## 🗓️ 7-Day Meal Plan for {name} *(Demo)*

**Daily Target:** ~{calories} kcal | **Goal:** {goal} | **Diet:** {diet}

---

### Day 1

| Meal | Food | Calories | Protein | Carbs | Fat |
|---|---|---|---|---|---|
| 🌅 Breakfast | Oats + banana + almond milk | 380 | 12g | 65g | 8g |
| 🍎 Snack | Apple + 10 almonds | 180 | 4g | 24g | 8g |
| 🥗 Lunch | Grilled chicken salad + whole wheat bread | 520 | 38g | 45g | 14g |
| 🥕 Snack | Hummus + carrot sticks | 150 | 5g | 18g | 7g |
| 🍽️ Dinner | Baked salmon + quinoa + steamed broccoli | 620 | 42g | 52g | 18g |
| **Daily Total** | | **{calories}** | **101g** | **204g** | **55g** |

> 💡 **Prep Tip:** Cook quinoa in bulk on Day 1 — it keeps for 4 days in the fridge.

---

### Day 2

| Meal | Food | Calories | Protein | Carbs | Fat |
|---|---|---|---|---|---|
| 🌅 Breakfast | Greek yogurt + berries + granola | 350 | 18g | 48g | 9g |
| 🍎 Snack | Banana + peanut butter | 200 | 6g | 28g | 9g |
| 🥗 Lunch | Lentil soup + whole grain roti | 480 | 22g | 72g | 8g |
| 🥕 Snack | Mixed nuts (30g) | 180 | 5g | 7g | 15g |
| 🍽️ Dinner | Tofu stir-fry + brown rice + bok choy | 580 | 28g | 68g | 16g |
| **Daily Total** | | **{calories - 10}** | **79g** | **223g** | **57g** |

> 💡 **Prep Tip:** Marinate tofu overnight in soy sauce, garlic and ginger for deeper flavour.

---

*⚙️ Enable IBM Granite AI to get a fully personalized 7-day plan with your exact preferences, allergies, and cultural cuisine.*"""
