# AI-Driven Meal Recommendation System Balancing Nutrition and Budget Using Random Forest

## Problem Statement
Many individuals struggle to maintain a healthy diet that meets their specific nutritional targets (Calories, Protein, Carbohydrates, Fat, Fiber) without exceeding their daily or weekly budgets. Existing solutions often focus on either budget tracking or calorie counting, but rarely combine both using intelligent decision-making.

## Objectives
This capstone project aims to build an AI-driven web application that intelligently recommends personalized meal plans. It leverages a Machine Learning model to balance conflicting constraints: maximizing nutritional alignment while minimizing cost and respecting user preferences (vegetarian, cuisine type, prep time).

## Features
- **Smart Recommendations:** Uses Machine Learning to rank meals based on personalized suitability.
- **Budget Tracking:** Enforces strict daily and weekly budget limits.
- **Nutritional Matching:** Balances Calories, Protein, Carbs, Fat, and Fiber down to the gram.
- **Explainable AI:** Displays model performance metrics (RMSE, R²) and Feature Importance to show why meals are recommended.
- **Interactive Dashboard:** Beautiful React-based UI with Recharts visualizations for both budget and nutrition.
- **Dynamic Daily/Weekly Plans:** Auto-generates full daily meal schedules.

## Technologies
- **Frontend:** React (Vite), Tailwind CSS v4, Recharts, Lucide React, React Router.
- **Backend:** Python, FastAPI, Uvicorn.
- **Machine Learning:** Scikit-Learn (RandomForestRegressor), Pandas, NumPy.

## Dataset
Since a comprehensive real-world dataset containing exact nutritional macros, prep time, and Indian/Global costs wasn't readily available, a realistic synthetic dataset (`meals.csv`) of 500 meals was generated. It includes fields like `Meal_Name`, `Calories`, `Protein`, `Cost`, `Is_Vegetarian`, `Prep_Time`, and `Base_Rating`.

## Machine Learning Workflow (Random Forest)
1. **Dynamic Target Generation:** When a user inputs their targets (e.g., 2000 kcal, ₹250 budget), the backend calculates a `Suitability_Score` for every meal in the dataset. Penalties are applied for breaking the budget or missing macro targets.
2. **Preprocessing:** Categorical variables (Cuisine, Meal Type) are One-Hot Encoded.
3. **Training:** A `RandomForestRegressor` with 100 estimators is trained *on-the-fly* on 80% of the dataset to learn the complex non-linear relationships between the features and the `Suitability_Score`.
4. **Prediction & Ranking:** The model predicts scores for the test set and ranks all meals.
5. **Model Evaluation:** The system evaluates the model using RMSE, MAE, and R², and extracts Feature Importances to display in the Explainable AI dashboard.

## System Architecture
```mermaid
graph TD;
    UI[React Frontend] -->|POST /predict (User Targets)| API[FastAPI Backend]
    API -->|Load| CSV[(meals.csv)]
    API -->|1. Calculate Targets| Preprocess[Data Preprocessing]
    Preprocess -->|2. Encode Features| ML[Random Forest Training]
    ML -->|3. Evaluate| Predict[Prediction & Ranking]
    Predict -->|4. Top Meals| API
    API -->|Return JSON| UI
    UI -->|Render| Charts[Dashboard & Charts]
```

## API Endpoints
- `POST /predict`: Accepts user requirements and returns top recommendations, daily plans, and weekly summaries.
- `GET /meals`: Returns paginated dataset for the data exploration page.
- `GET /model-metrics`: Returns metrics (RMSE, R², Train/Test Split) and Feature Importances from the last trained model.

## Installation & Running Locally

### 1. Backend Setup
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate   # On Windows
pip install fastapi uvicorn scikit-learn pandas numpy pydantic
python dataset/generate_dataset.py  # Generate the meals dataset
python app.py  # Starts server on http://localhost:8000
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev   # Starts Vite server on http://localhost:5173
```

## How to Demonstrate During Presentation
1. Start both the backend and frontend servers.
2. Open the web app and click **"Start Recommendation"**.
3. On the input form, click the **"Load Demo User"** button to auto-fill realistic values (e.g., 1850 kcal, ₹250 budget, Vegetarian).
4. Click **"Generate AI Recommendations"**. Note how fast the Random Forest trains.
5. Walk through the **Dashboard**, pointing out the Budget Doughnut chart and Nutrition Bar chart.
6. Navigate to the **ML Model** page to explain the Random Forest pipeline, showing the high R² score and feature importances.
7. Navigate to the **Dataset** page to show the underlying data.

## Future Improvements
- Connect to an external live database (e.g., Edamam or FatSecret API) for real-time meal data.
- Implement user authentication to save historical meal plans.
- Transition from Random Forest to Deep Learning (Neural Collaborative Filtering) for more complex user-item interactions.
