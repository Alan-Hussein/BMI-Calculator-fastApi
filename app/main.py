from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="BMI Calculator API",
    description="A simple API to calculate Body Mass Index (BMI) and provide gender-specific advice.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],
    allow_headers=["*"],
)

class BMIRequest(BaseModel):
    weight: float  # in kg
    height: float  # in meters
    gender: str    # "male" or "female"
    age: int       # age in years

class BMIResponse(BaseModel):
    bmi: float
    category: str
    advice: str
    ideal_weight: float
    weight_status: str

@app.get("/")
def home():
    return "Welcome to the enhanced BMI Calculator"

@app.post("/calculate-bmi", response_model=BMIResponse, tags=["BMI Calculator"])
def calculate_bmi(data: BMIRequest):
    """
    Calculate BMI based on weight (kg), height (m), age, and gender.

    - **weight**: Your weight in kilograms (e.g., 70)
    - **height**: Your height in meters (e.g., 1.75)
    - **gender**: Your gender, either "male" or "female"
    - **age**: Your age in years
    """
    if data.height <= 0 or data.weight <= 0 or data.age <= 0:
        raise HTTPException(status_code=400, detail="Height, weight, and age must be positive values.")
    if data.gender not in ["male", "female"]:
        raise HTTPException(status_code=400, detail="Gender must be 'male' or 'female'.")

    bmi = data.weight / (data.height ** 2)
    category, advice = get_bmi_category_and_advice(bmi, data.gender)

    # Calculate ideal weight based on height and gender
    ideal_weight = calculate_ideal_weight(data.height, data.gender)
    
    # Calculate the weight status based on ideal weight
    weight_status = calculate_weight_status(data.weight, ideal_weight)

    return BMIResponse(
        bmi=round(bmi, 2),
        category=category,
        advice=advice,
        ideal_weight=round(ideal_weight, 2),
        weight_status=weight_status,
    )

def get_bmi_category_and_advice(bmi: float, gender: str) -> tuple:
    """
    Determine BMI category and give gender-specific advice.
    """
    if bmi < 18.5:
        category = "Underweight"
        advice = (
            "Try to gain weight by consuming more nutritious food and exercising regularly."
            if gender == "male" else
            "Consider consulting a healthcare provider to discuss weight gain strategies."
        )
    elif 18.5 <= bmi < 24.9:
        category = "Normal weight"
        advice = (
            "Maintain your current lifestyle and diet to stay healthy."
            if gender == "male" else
            "Keep up the good work! Focus on balanced nutrition and exercise."
        )
    elif 25 <= bmi < 29.9:
        category = "Overweight"
        advice = (
            "Consider increasing physical activity and monitoring your diet to lose weight."
            if gender == "male" else
            "Focus on a balanced diet and regular exercise to manage your weight."
        )
    else:
        category = "Obesity"
        advice = (
            "Consult a healthcare provider for advice on managing obesity."
            if gender == "male" else
            "Seek guidance from a healthcare provider to address weight-related health concerns."
        )
    return category, advice

def calculate_ideal_weight(height: float, gender: str) -> float:
    """
    Calculate ideal weight based on height (in meters) and gender.
    """
    height_in_cm = height * 100  # Convert height from meters to cm
    
    if gender == "male":
        ideal_weight = height_in_cm - 100  # Broca's Index for Men
    elif gender == "female":
        ideal_weight = height_in_cm - 104  # Broca's Index for Women
    
    # Ensure ideal weight isn't negative
    return max(ideal_weight, 0)

def calculate_weight_status(weight: float, ideal_weight: float) -> str:
    """
    Calculate the status of the person's weight compared to their ideal weight.
    """
    if weight < ideal_weight:
        return "Below ideal weight"
    elif weight == ideal_weight:
        return "At ideal weight"
    else:
        return "Above ideal weight"
