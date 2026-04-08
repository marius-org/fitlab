from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Optional
import math

app = FastAPI(title="FitLab")
templates = Jinja2Templates(directory="templates")
templates.env.globals["enumerate"] = enumerate

# ──────────────────────────────────────────────
# WORKOUT DATA
# ──────────────────────────────────────────────

WORKOUTS = {
    "chest": {
        "beginner": [
            {"exercise": "Push-Ups", "sets": 3, "reps": "10-12", "rest": "60s", "tip": "Keep your core tight and back straight."},
            {"exercise": "Incline Push-Ups", "sets": 3, "reps": "12-15", "rest": "60s", "tip": "Hands on a bench or wall to reduce difficulty."},
            {"exercise": "Dumbbell Chest Press", "sets": 3, "reps": "10-12", "rest": "90s", "tip": "Lower slowly, press explosively."},
            {"exercise": "Dumbbell Flyes", "sets": 3, "reps": "12", "rest": "60s", "tip": "Slight bend in elbows throughout."},
            {"exercise": "Wide Push-Ups", "sets": 2, "reps": "10", "rest": "60s", "tip": "Wide grip targets the outer chest."},
        ],
        "intermediate": [
            {"exercise": "Barbell Bench Press", "sets": 4, "reps": "8-10", "rest": "90s", "tip": "Arch your back naturally, feet flat on floor."},
            {"exercise": "Incline Dumbbell Press", "sets": 3, "reps": "10-12", "rest": "90s", "tip": "30-45° incline hits upper chest."},
            {"exercise": "Cable Crossovers", "sets": 3, "reps": "12-15", "rest": "60s", "tip": "Squeeze at the peak of the movement."},
            {"exercise": "Dips (chest lean)", "sets": 3, "reps": "10-12", "rest": "90s", "tip": "Lean forward to emphasize chest over triceps."},
            {"exercise": "Push-Up with Pause", "sets": 3, "reps": "8", "rest": "60s", "tip": "2-second hold at the bottom builds strength."},
        ],
        "advanced": [
            {"exercise": "Heavy Barbell Bench Press", "sets": 5, "reps": "5", "rest": "3min", "tip": "Focus on progressive overload."},
            {"exercise": "Weighted Dips", "sets": 4, "reps": "8-10", "rest": "2min", "tip": "Add a belt or hold a dumbbell between legs."},
            {"exercise": "Incline Barbell Press", "sets": 4, "reps": "8", "rest": "2min", "tip": "Don't go too steep — 30° is ideal."},
            {"exercise": "Cable Flyes (low-to-high)", "sets": 3, "reps": "12-15", "rest": "60s", "tip": "Targets the upper chest fibers."},
            {"exercise": "Plyometric Push-Ups", "sets": 3, "reps": "8-10", "rest": "90s", "tip": "Explosive power — clap at the top if you can."},
            {"exercise": "Decline Dumbbell Press", "sets": 3, "reps": "10", "rest": "90s", "tip": "Hits the lower chest, often neglected."},
        ],
    },
    "back": {
        "beginner": [
            {"exercise": "Assisted Pull-Ups / Band Pull-Ups", "sets": 3, "reps": "8-10", "rest": "90s", "tip": "Full range of motion, chin over bar."},
            {"exercise": "Dumbbell Bent-Over Row", "sets": 3, "reps": "10-12", "rest": "90s", "tip": "Keep your back flat, pull to your hip."},
            {"exercise": "Seated Cable Row", "sets": 3, "reps": "12", "rest": "60s", "tip": "Squeeze shoulder blades together at the end."},
            {"exercise": "Lat Pulldown", "sets": 3, "reps": "12-15", "rest": "60s", "tip": "Pull to your upper chest, not behind your neck."},
            {"exercise": "Superman Hold", "sets": 3, "reps": "12", "rest": "45s", "tip": "Squeeze your glutes and hold for 2 seconds."},
        ],
        "intermediate": [
            {"exercise": "Pull-Ups", "sets": 4, "reps": "8-10", "rest": "2min", "tip": "Full dead hang at the bottom each rep."},
            {"exercise": "Barbell Bent-Over Row", "sets": 4, "reps": "8-10", "rest": "90s", "tip": "Hinge at the hips, back parallel to floor."},
            {"exercise": "Single-Arm Dumbbell Row", "sets": 3, "reps": "10-12 each", "rest": "60s", "tip": "Brace on a bench, pull elbow to ceiling."},
            {"exercise": "Face Pulls", "sets": 3, "reps": "15", "rest": "60s", "tip": "Great for rear delts and rotator cuff health."},
            {"exercise": "Straight-Arm Pulldown", "sets": 3, "reps": "12-15", "rest": "60s", "tip": "Keep arms straight, feel the lat stretch."},
        ],
        "advanced": [
            {"exercise": "Weighted Pull-Ups", "sets": 5, "reps": "6-8", "rest": "2min", "tip": "Add weight via belt for progressive overload."},
            {"exercise": "Deadlift", "sets": 4, "reps": "5", "rest": "3min", "tip": "King of all back exercises. Keep bar close to body."},
            {"exercise": "T-Bar Row", "sets": 4, "reps": "8-10", "rest": "2min", "tip": "Great for mid-back thickness."},
            {"exercise": "Meadows Row", "sets": 3, "reps": "10-12 each", "rest": "90s", "tip": "Landmine variant for incredible lat stretch."},
            {"exercise": "Rack Pulls", "sets": 3, "reps": "5", "rest": "3min", "tip": "Partial deadlift focusing on the upper pull."},
            {"exercise": "Close-Grip Lat Pulldown", "sets": 3, "reps": "12", "rest": "60s", "tip": "Supinated grip hits lower lats harder."},
        ],
    },
    "legs": {
        "beginner": [
            {"exercise": "Bodyweight Squats", "sets": 3, "reps": "15", "rest": "60s", "tip": "Knees track over toes, chest tall."},
            {"exercise": "Lunges", "sets": 3, "reps": "10 each leg", "rest": "60s", "tip": "Step far enough so front knee stays over ankle."},
            {"exercise": "Glute Bridge", "sets": 3, "reps": "15", "rest": "60s", "tip": "Squeeze at the top for 2 seconds."},
            {"exercise": "Step-Ups", "sets": 3, "reps": "10 each", "rest": "60s", "tip": "Drive through the heel of the elevated foot."},
            {"exercise": "Calf Raises", "sets": 3, "reps": "20", "rest": "45s", "tip": "Full range — all the way up and down."},
        ],
        "intermediate": [
            {"exercise": "Barbell Back Squat", "sets": 4, "reps": "8-10", "rest": "2min", "tip": "Break parallel for full quad development."},
            {"exercise": "Romanian Deadlift", "sets": 3, "reps": "10-12", "rest": "90s", "tip": "Push hips back, feel the hamstring stretch."},
            {"exercise": "Leg Press", "sets": 3, "reps": "12-15", "rest": "90s", "tip": "Don't lock knees at the top."},
            {"exercise": "Walking Lunges", "sets": 3, "reps": "12 each leg", "rest": "90s", "tip": "Add dumbbells for extra challenge."},
            {"exercise": "Seated Calf Raise", "sets": 4, "reps": "15-20", "rest": "60s", "tip": "Soleus-focused, different from standing calf raises."},
        ],
        "advanced": [
            {"exercise": "Heavy Back Squat", "sets": 5, "reps": "5", "rest": "3min", "tip": "Brace hard, big breath before each rep."},
            {"exercise": "Bulgarian Split Squat", "sets": 4, "reps": "8-10 each", "rest": "2min", "tip": "Brutal but unmatched for single-leg strength."},
            {"exercise": "Hack Squat", "sets": 4, "reps": "10-12", "rest": "2min", "tip": "Feet low on platform for more quad emphasis."},
            {"exercise": "Nordic Hamstring Curl", "sets": 3, "reps": "6-8", "rest": "2min", "tip": "One of the best hamstring strength exercises."},
            {"exercise": "Leg Press (high volume)", "sets": 4, "reps": "15-20", "rest": "90s", "tip": "Drop sets work great here."},
            {"exercise": "Standing Calf Raise (weighted)", "sets": 5, "reps": "15", "rest": "60s", "tip": "Pause at the bottom for full stretch."},
        ],
    },
    "shoulders": {
        "beginner": [
            {"exercise": "Dumbbell Shoulder Press", "sets": 3, "reps": "10-12", "rest": "90s", "tip": "Don't lock elbows at the top."},
            {"exercise": "Lateral Raises", "sets": 3, "reps": "12-15", "rest": "60s", "tip": "Lead with your elbows, not wrists."},
            {"exercise": "Front Raises", "sets": 3, "reps": "12", "rest": "60s", "tip": "Alternate arms to reduce fatigue."},
            {"exercise": "Arnold Press", "sets": 3, "reps": "10", "rest": "90s", "tip": "Great for all three deltoid heads."},
            {"exercise": "Band Pull-Apart", "sets": 3, "reps": "15", "rest": "45s", "tip": "Great for rear delt and posture."},
        ],
        "intermediate": [
            {"exercise": "Barbell Overhead Press", "sets": 4, "reps": "8-10", "rest": "2min", "tip": "Brace your core, press directly overhead."},
            {"exercise": "Cable Lateral Raise", "sets": 3, "reps": "15", "rest": "60s", "tip": "Cable keeps constant tension vs dumbbells."},
            {"exercise": "Rear Delt Flyes", "sets": 3, "reps": "15", "rest": "60s", "tip": "Hinge forward, elbows slightly bent."},
            {"exercise": "Upright Row", "sets": 3, "reps": "10-12", "rest": "90s", "tip": "Don't pull past chin level."},
            {"exercise": "Face Pulls", "sets": 3, "reps": "15-20", "rest": "60s", "tip": "External rotation at the end protects your shoulders."},
        ],
        "advanced": [
            {"exercise": "Push Press", "sets": 4, "reps": "6-8", "rest": "2min", "tip": "Use leg drive to move heavier weight overhead."},
            {"exercise": "Seated Dumbbell Press (heavy)", "sets": 4, "reps": "8", "rest": "2min", "tip": "Seated removes leg drive — pure shoulder work."},
            {"exercise": "Cable Lateral Raise (drop set)", "sets": 3, "reps": "12+8+6", "rest": "90s", "tip": "Drop weight immediately after each mini-set."},
            {"exercise": "Handstand Push-Up (or progression)", "sets": 3, "reps": "6-8", "rest": "2min", "tip": "Pike push-ups are a great stepping stone."},
            {"exercise": "Rear Delt Cable Pull", "sets": 4, "reps": "15", "rest": "60s", "tip": "Often undertrained — crucial for balanced shoulders."},
            {"exercise": "Shrugs (trap focus)", "sets": 3, "reps": "15", "rest": "60s", "tip": "Hold at the top for 2 seconds."},
        ],
    },
    "arms": {
        "beginner": [
            {"exercise": "Dumbbell Bicep Curl", "sets": 3, "reps": "12", "rest": "60s", "tip": "Don't swing — control the negative."},
            {"exercise": "Tricep Dips (bench)", "sets": 3, "reps": "10-12", "rest": "60s", "tip": "Keep elbows pointing back, not flaring out."},
            {"exercise": "Hammer Curl", "sets": 3, "reps": "12", "rest": "60s", "tip": "Neutral grip hits the brachialis too."},
            {"exercise": "Overhead Tricep Extension", "sets": 3, "reps": "12", "rest": "60s", "tip": "Keep upper arms close to ears."},
            {"exercise": "Concentration Curl", "sets": 2, "reps": "12 each", "rest": "45s", "tip": "Great for peak bicep contraction."},
        ],
        "intermediate": [
            {"exercise": "Barbell Curl", "sets": 4, "reps": "8-10", "rest": "90s", "tip": "Supinate at the top for full contraction."},
            {"exercise": "Close-Grip Bench Press", "sets": 4, "reps": "8-10", "rest": "90s", "tip": "Best compound tricep builder."},
            {"exercise": "Incline Dumbbell Curl", "sets": 3, "reps": "10-12", "rest": "60s", "tip": "The stretch at the bottom hits the long head."},
            {"exercise": "Skull Crushers", "sets": 3, "reps": "10-12", "rest": "90s", "tip": "Lower to forehead slowly, explode up."},
            {"exercise": "Cable Rope Hammer Curl", "sets": 3, "reps": "15", "rest": "60s", "tip": "Constant cable tension beats dumbbells here."},
        ],
        "advanced": [
            {"exercise": "Barbell Curl (21s)", "sets": 3, "reps": "21 (7+7+7)", "rest": "2min", "tip": "7 bottom half, 7 top half, 7 full range."},
            {"exercise": "Weighted Chin-Ups", "sets": 4, "reps": "6-8", "rest": "2min", "tip": "Best bicep mass builder, period."},
            {"exercise": "Overhead Cable Tricep Extension", "sets": 4, "reps": "12-15", "rest": "60s", "tip": "Rope attachment gives better range of motion."},
            {"exercise": "Spider Curl", "sets": 3, "reps": "12", "rest": "60s", "tip": "Chest on incline bench, removes cheat potential."},
            {"exercise": "Tricep Pushdown (drop set)", "sets": 3, "reps": "12+10+8", "rest": "90s", "tip": "No rest between drops, rest between sets."},
            {"exercise": "Reverse Curl", "sets": 3, "reps": "12", "rest": "60s", "tip": "Trains brachialis and forearms — often skipped."},
        ],
    },
    "full body": {
        "beginner": [
            {"exercise": "Bodyweight Squat", "sets": 3, "reps": "15", "rest": "60s", "tip": "Great foundation movement for lower body."},
            {"exercise": "Push-Ups", "sets": 3, "reps": "10-12", "rest": "60s", "tip": "Scale by doing incline push-ups if needed."},
            {"exercise": "Dumbbell Row", "sets": 3, "reps": "10 each", "rest": "60s", "tip": "Flat back, pull to your hip."},
            {"exercise": "Glute Bridge", "sets": 3, "reps": "15", "rest": "45s", "tip": "Squeeze at the top for posterior chain activation."},
            {"exercise": "Plank", "sets": 3, "reps": "30-45s", "rest": "45s", "tip": "Don't let your hips sag or rise."},
            {"exercise": "Jumping Jacks", "sets": 2, "reps": "30", "rest": "30s", "tip": "Great warm-up and cardio finisher."},
        ],
        "intermediate": [
            {"exercise": "Goblet Squat", "sets": 4, "reps": "12", "rest": "90s", "tip": "Hold dumbbell at chest, elbows inside knees."},
            {"exercise": "Dumbbell Romanian Deadlift", "sets": 3, "reps": "10-12", "rest": "90s", "tip": "Push hips back, feel hamstring stretch."},
            {"exercise": "Dumbbell Bench Press", "sets": 3, "reps": "10", "rest": "90s", "tip": "Full range of motion, controlled descent."},
            {"exercise": "Pull-Ups or Lat Pulldown", "sets": 3, "reps": "8-10", "rest": "90s", "tip": "Pull elbows to your sides."},
            {"exercise": "Dumbbell Shoulder Press", "sets": 3, "reps": "10-12", "rest": "90s", "tip": "Seated or standing — both work great."},
            {"exercise": "Mountain Climbers", "sets": 3, "reps": "20 each leg", "rest": "45s", "tip": "Keep hips level, drive knees fast."},
        ],
        "advanced": [
            {"exercise": "Barbell Squat", "sets": 4, "reps": "6-8", "rest": "2min", "tip": "The cornerstone of any serious program."},
            {"exercise": "Deadlift", "sets": 4, "reps": "5", "rest": "3min", "tip": "Heaviest lift of the session — go first."},
            {"exercise": "Weighted Pull-Ups", "sets": 3, "reps": "8", "rest": "2min", "tip": "Full dead hang, chin over bar."},
            {"exercise": "Barbell Overhead Press", "sets": 3, "reps": "8", "rest": "2min", "tip": "Brace your core, lock out at the top."},
            {"exercise": "Dips (weighted)", "sets": 3, "reps": "8-10", "rest": "2min", "tip": "Full range — chest and triceps engaged."},
            {"exercise": "Farmers Walk", "sets": 3, "reps": "40m", "rest": "90s", "tip": "Heavy dumbbells, chest up, grip challenged."},
        ],
    },
}


# ──────────────────────────────────────────────
# FITNESS CALCULATION HELPERS
# ──────────────────────────────────────────────

def calculate_bmi(weight_kg: float, height_cm: float) -> dict:
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    if bmi < 18.5:
        category = "Underweight"
        color = "#3b82f6"
    elif bmi < 25:
        category = "Normal weight"
        color = "#22c55e"
    elif bmi < 30:
        category = "Overweight"
        color = "#f59e0b"
    else:
        category = "Obese"
        color = "#ef4444"
    return {"value": round(bmi, 1), "category": category, "color": color}


def calculate_tdee(weight_kg: float, height_cm: float, age: int, gender: str, activity: str) -> int:
    # Mifflin-St Jeor BMR
    if gender == "male":
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    else:
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161

    multipliers = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725,
        "very_active": 1.9,
    }
    return round(bmr * multipliers.get(activity, 1.2))


def calculate_macros(tdee: int) -> dict:
    protein_cal = tdee * 0.30
    carbs_cal = tdee * 0.40
    fats_cal = tdee * 0.30
    return {
        "protein": round(protein_cal / 4),
        "carbs": round(carbs_cal / 4),
        "fats": round(fats_cal / 9),
        "protein_pct": 30,
        "carbs_pct": 40,
        "fats_pct": 30,
    }


# ──────────────────────────────────────────────
# ROUTES
# ──────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def calculator_page(request: Request):
    return templates.TemplateResponse("calculator.html", {"request": request, "result": None})


@app.post("/calculate", response_class=HTMLResponse)
async def calculate(
    request: Request,
    age: int = Form(...),
    gender: str = Form(...),
    weight: float = Form(...),
    height: float = Form(...),
    activity: str = Form(...),
):
    bmi = calculate_bmi(weight, height)
    tdee = calculate_tdee(weight, height, age, gender, activity)
    macros = calculate_macros(tdee)

    result = {
        "bmi": bmi,
        "tdee": tdee,
        "macros": macros,
        "weight": weight,
        "height": height,
        "age": age,
    }
    return templates.TemplateResponse("calculator.html", {"request": request, "result": result})


@app.get("/workout", response_class=HTMLResponse)
async def workout_page(request: Request):
    muscle_groups = list(WORKOUTS.keys())
    return templates.TemplateResponse("workout.html", {
        "request": request,
        "muscle_groups": muscle_groups,
        "result": None,
    })


@app.post("/workout", response_class=HTMLResponse)
async def generate_workout(
    request: Request,
    muscle_group: str = Form(...),
    difficulty: str = Form(...),
):
    muscle_groups = list(WORKOUTS.keys())
    exercises = WORKOUTS.get(muscle_group, {}).get(difficulty, [])
    result = {
        "muscle_group": muscle_group.title(),
        "difficulty": difficulty.title(),
        "exercises": exercises,
        "total": len(exercises),
    }
    return templates.TemplateResponse("workout.html", {
        "request": request,
        "muscle_groups": muscle_groups,
        "result": result,
    })
