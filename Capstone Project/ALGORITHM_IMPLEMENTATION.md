# Machine Learning Algorithm Implementation Details

This project uses a **Random Forest Regressor** to drive the AI meal recommendations. 

The Random Forest is an ensemble learning method that constructs a multitude of decision trees during training and outputs the average prediction of the individual trees. We used it here because it handles non-linear relationships well (like balancing strict budgets with specific macro-nutrient goals) and natively provides "Feature Importances" so we can explain the AI's decisions to the user.

Below is a breakdown of exactly **where** and **how** this algorithm is implemented across the codebase.

---

## 1. The Core Algorithm (`backend/model.py`)
This is the heart of the machine learning implementation. 
- **Function:** `preprocess_and_train()`
- **What it does:** 
  - **Data Preprocessing:** Uses `pd.get_dummies()` to One-Hot Encode categorical variables (`Cuisine`, `Meal_Type`) so the mathematical model can read them.
  - **Data Splitting:** Uses `train_test_split` to divide the dataset into 80% training data and 20% testing data.
  - **Algorithm Initialization:** Imports `RandomForestRegressor` from `sklearn.ensemble` and initializes it with 100 decision trees (`n_estimators=100`).
  - **Training:** Fits the model using `rf_model.fit(X_train, y_train)`.
  - **Evaluation:** Calculates Regression metrics (MSE, RMSE, MAE, R²) and Classification metrics (Precision, Recall, F1 Score, Confusion Matrix) by thresholding the continuous score at `>= 75`.
  - **Feature Importance:** Extracts `rf_model.feature_importances_` to understand which nutritional factors influenced the tree the most.

## 2. Generating the Target Labels (`backend/recommender.py`)
Supervised algorithms like Random Forest need a "target" variable to learn from. 
- **Function:** `calculate_suitability_score()`
- **What it does:** 
  - It acts as the "Teacher" for our AI. It looks at the User's inputs (BMI, Fitness Goal, Budget, Macro limits) and dynamically calculates a perfect `Suitability_Score` (out of 100) for every meal using strict heuristic penalties.
  - The Random Forest model then *trains* on this generated score, learning the complex patterns between the meal's features and the final score so it can predict them accurately.

## 3. Serving the Model (`backend/app.py`)
This file connects the trained algorithm to the frontend via API endpoints.
- **Endpoint:** `POST /predict`
  - When the user submits their form, this endpoint dynamically calls the recommender to generate the target scores, then calls `preprocess_and_train()` from `model.py` to train the Random Forest.
  - It then uses the trained algorithm to `.predict()` the suitability of all meals, ranks them from highest to lowest score, and returns the top recommendations.
- **Endpoint:** `GET /model-metrics`
  - Exposes the Random Forest's internal metrics (R² score, Error distribution, Feature importances, Confusion Matrix, and Hyperparameters) to the frontend.

## 4. Visualizing the Algorithm (`frontend/src/pages/MachineLearning.jsx`)
This file is the Explainable AI (XAI) dashboard for the algorithm.
- **What it does:** 
  - It fetches the stats from `/model-metrics` and uses the `recharts` library to graph the Random Forest's behavior.
  - **Visualizations included:** Actual vs Predicted scatter tracking, feature importance bar charts, categorized pie charts (Logistics vs Nutrition), and the Confusion Matrix evaluating the algorithm's performance.

---
**Summary of the ML Pipeline Flow:**
1. **User Input** &rarr; 2. **Heuristic Score Generation (`recommender.py`)** &rarr; 3. **Random Forest Training & Prediction (`model.py`)** &rarr; 4. **API Serving (`app.py`)** &rarr; 5. **UI Rendering (`MachineLearning.jsx`)**
