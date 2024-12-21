const form = document.getElementById("bmi-form");
const resultDiv = document.getElementById("result");
const bmiValue = document.getElementById("bmi-value");
const bmiCategory = document.getElementById("bmi-category");
const bmiAdvice = document.getElementById("bmi-advice");
const idealWeight = document.getElementById("ideal-weight");
const weightStatus = document.getElementById("weight-status");
const indicator = document.querySelector(".bmi-meter .indicator");

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const weight = parseFloat(document.getElementById("weight").value);
  const height = parseFloat(document.getElementById("height").value);
  const gender = document.getElementById("gender").value;
  const age = parseInt(document.getElementById("age").value);

  try {
    const response = await fetch("/api/calculate-bmi", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ weight, height, gender, age }),
    });

    if (!response.ok) {
      const error = await response.json();
      alert(error.detail);
      return;
    }

    const data = await response.json();
    bmiValue.textContent = data.bmi;
    bmiCategory.textContent = data.category;
    bmiAdvice.textContent = data.advice;
    idealWeight.textContent = data.ideal_weight;
    weightStatus.textContent = data.weight_status;
    resultDiv.classList.remove("hidden");

    // Update the BMI indicator position
    const bmi = data.bmi;
    const minBMI = 15;
    const maxBMI = 40;
    const meterWidth = document.querySelector(".bmi-meter").offsetWidth;

    const relativePosition = ((bmi - minBMI) / (maxBMI - minBMI)) * meterWidth;
    indicator.style.left = `${Math.min(
      Math.max(relativePosition, 0),
      meterWidth - 5
    )}px`;
  } catch (error) {
    alert("Error calculating BMI. Please try again later.");
    console.error(error);
  }
});
