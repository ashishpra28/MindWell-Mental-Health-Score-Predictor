/* ==========================================================================
   MindWell — frontend logic
   ========================================================================== */

const API_URL = "http://127.0.0.1:8000/predict";

// Countries accepted by the backend (Literal values from the FastAPI model),
// sorted alphabetically with "Other" pinned last.
const COUNTRIES = [
  "Afghanistan", "Andorra", "Argentina", "Armenia", "Australia", "Austria",
  "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Belarus", "Belgium",
  "Bhutan", "Bolivia", "Bosnia", "Brazil", "Bulgaria", "Canada", "Chile",
  "China", "Colombia", "Costa Rica", "Croatia", "Cyprus", "Czech Republic",
  "Denmark", "Ecuador", "Egypt", "Estonia", "Finland", "France", "Georgia",
  "Germany", "Ghana", "Greece", "Hong Kong", "Hungary", "Iceland", "India",
  "Indonesia", "Iraq", "Ireland", "Israel", "Italy", "Jamaica", "Japan",
  "Jordan", "Kazakhstan", "Kenya", "Kosovo", "Kuwait", "Kyrgyzstan", "Latvia",
  "Lebanon", "Liechtenstein", "Lithuania", "Luxembourg", "Malaysia",
  "Maldives", "Malta", "Mexico", "Moldova", "Monaco", "Montenegro", "Morocco",
  "Nepal", "Netherlands", "New Zealand", "Nigeria", "North Macedonia",
  "Norway", "Oman", "Pakistan", "Panama", "Paraguay", "Peru", "Philippines",
  "Poland", "Portugal", "Qatar", "Romania", "Russia", "San Marino", "Serbia",
  "Singapore", "Slovakia", "Slovenia", "South Africa", "South Korea", "Spain",
  "Sri Lanka", "Sweden", "Switzerland", "Syria", "Taiwan", "Tajikistan",
  "Thailand", "Trinidad", "Turkey", "UAE", "UK", "Ukraine", "Uruguay", "USA",
  "Uzbekistan", "Vatican City", "Venezuela", "Vietnam", "Yemen", "Other"
];

// Fields that must be sent to the API as numbers rather than strings.
const NUMERIC_FIELDS = new Set([
  "Age", "Avg_Daily_Usage_Hours", "Daily_Unlocks",
  "Study_Hours", "Physical_Activity_Hours", "Sleep_Hours_Per_Night"
]);

const form = document.getElementById("predict-form");
const submitBtn = document.getElementById("submit-btn");
const apiErrorBox = document.getElementById("api-error");
const resultSection = document.getElementById("result");
const scoreValueEl = document.getElementById("score-value");
const scoreBandEl = document.getElementById("score-band");
const scoreRingFill = document.querySelector(".score-ring__fill");
const resetBtn = document.getElementById("reset-btn");

const RING_CIRCUMFERENCE = 2 * Math.PI * 104;

init();

function init() {
  populateCountries();
  observeFormGroups();

  form.addEventListener("submit", handleSubmit);
  resetBtn.addEventListener("click", handleReset);
}

/* ---------------------------------------------------------------------- */
/* Setup                                                                   */
/* ---------------------------------------------------------------------- */

function populateCountries() {
  const select = document.getElementById("country");
  for (const country of COUNTRIES) {
    const option = document.createElement("option");
    option.value = country;
    option.textContent = country;
    select.appendChild(option);
  }
}

// Reveal each form section slightly as it scrolls into view.
function observeFormGroups() {
  const groups = document.querySelectorAll(".form__group");

  if (!("IntersectionObserver" in window)) {
    groups.forEach((g) => g.classList.add("is-visible"));
    return;
  }

  const observer = new IntersectionObserver(
    (entries, obs) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          obs.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.15 }
  );

  groups.forEach((g) => observer.observe(g));
}

/* ---------------------------------------------------------------------- */
/* Form handling                                                           */
/* ---------------------------------------------------------------------- */

function getFormData() {
  const raw = new FormData(form);
  const data = {};

  for (const [key, value] of raw.entries()) {
    data[key] = NUMERIC_FIELDS.has(key) ? Number(value) : value;
  }

  return data;
}

function validateForm(data) {
  const errors = {};

  for (const field of form.querySelectorAll("[name]")) {
    const value = data[field.name];
    const errorSlotId = field.id;

    if (value === "" || value === undefined || value === null || Number.isNaN(value)) {
      errors[errorSlotId] = "This field is required.";
      continue;
    }

    if (field.type === "number") {
      const min = field.min !== "" ? Number(field.min) : null;
      const max = field.max !== "" ? Number(field.max) : null;
      if (min !== null && value < min) errors[errorSlotId] = `Must be at least ${min}.`;
      if (max !== null && value > max) errors[errorSlotId] = `Must be at most ${max}.`;
    }
  }

  renderFieldErrors(errors);
  return Object.keys(errors).length === 0;
}

function renderFieldErrors(errors) {
  document.querySelectorAll(".field").forEach((fieldEl) => {
    const input = fieldEl.querySelector("[name]");
    const errorSlot = fieldEl.querySelector(".field__error");
    if (!input || !errorSlot) return;

    const message = errors[input.id];
    errorSlot.textContent = message || "";
    fieldEl.classList.toggle("has-error", Boolean(message));
  });
}

async function handleSubmit(event) {
  event.preventDefault();
  hideApiError();

  const data = getFormData();
  if (!validateForm(data)) return;

  setLoadingState(true);

  try {
    const score = await predictScore(data);
    displayResult(score);
  } catch (err) {
    showError(err.message);
  } finally {
    setLoadingState(false);
  }
}

function handleReset() {
  resultSection.hidden = true;
  form.reset();
  document.getElementById("predict").scrollIntoView({ behavior: "smooth" });
}

/* ---------------------------------------------------------------------- */
/* API                                                                      */
/* ---------------------------------------------------------------------- */

async function predictScore(data) {
  let response;

  try {
    response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });
  } catch {
    throw new Error(
      "Unable to connect to MindWell. Please make sure the prediction server is running."
    );
  }

  if (!response.ok) {
    throw new Error(
      "MindWell couldn't process that request. Please check your inputs and try again."
    );
  }

  let payload;
  try {
    payload = await response.json();
  } catch {
    throw new Error("MindWell returned an unexpected response. Please try again.");
  }

  if (typeof payload.predicted_mental_health_score !== "number") {
    throw new Error("MindWell returned an unexpected response. Please try again.");
  }

  return payload.predicted_mental_health_score;
}

/* ---------------------------------------------------------------------- */
/* Result display                                                          */
/* ---------------------------------------------------------------------- */

function displayResult(score) {
  resultSection.hidden = false;
  scoreBandEl.textContent = interpretScore(score);

  resultSection.scrollIntoView({ behavior: "smooth", block: "start" });

  animateScore(score);
  animateRing(score);
}

function interpretScore(score) {
  if (score < 4) return "Lower score range";
  if (score < 6) return "Moderate score range";
  if (score < 8) return "Healthy score range";
  return "Strong score range";
}

function animateScore(target) {
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  if (reduceMotion) {
    scoreValueEl.textContent = target.toFixed(1);
    return;
  }

  const duration = 900;
  const start = performance.now();

  function tick(now) {
    const progress = Math.min((now - start) / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    scoreValueEl.textContent = (target * eased).toFixed(1);

    if (progress < 1) requestAnimationFrame(tick);
    else scoreValueEl.textContent = target.toFixed(1);
  }

  requestAnimationFrame(tick);
}

function animateRing(score) {
  const clamped = Math.max(0, Math.min(score, 10));
  const offset = RING_CIRCUMFERENCE * (1 - clamped / 10);

  // Reset first so the transition always plays from empty.
  scoreRingFill.style.transition = "none";
  scoreRingFill.style.strokeDashoffset = RING_CIRCUMFERENCE;

  requestAnimationFrame(() => {
    scoreRingFill.style.transition = "";
    scoreRingFill.style.strokeDashoffset = offset;
  });
}

/* ---------------------------------------------------------------------- */
/* Loading + error states                                                  */
/* ---------------------------------------------------------------------- */

function setLoadingState(isLoading) {
  submitBtn.disabled = isLoading;
  submitBtn.querySelector(".btn__label").textContent = isLoading
    ? "Predicting…"
    : "Predict My Score";
}

function showError(message) {
  apiErrorBox.textContent = message;
  apiErrorBox.hidden = false;
  apiErrorBox.scrollIntoView({ behavior: "smooth", block: "center" });
}

function hideApiError() {
  apiErrorBox.hidden = true;
  apiErrorBox.textContent = "";
}