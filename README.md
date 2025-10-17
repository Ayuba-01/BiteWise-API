# 🍽️ BiteWise API – Smart Meal Planner & Weight-loss Coach

**BiteWise** is a Django REST Framework API that helps users plan healthy meals, generate grocery lists, and track progress toward their weight goals.  
It combines nutrition data, personalized meal planning, and adherence tracking into one intelligent backend system.

---

## 🚀 Features

### 🔐 Authentication
- Register, Login, Refresh, Logout (JWT-based)
- Custom user model with email login
- `/api/v1/auth/register/`, `/api/v1/auth/login/`, `/api/v1/users/me/`

### 👤 User Profile & Preferences
- Set dietary type (vegan, halal, etc.)
- Manage allergens & disliked ingredients
- One-to-one relation with user

### 🎯 Goals & Progress
- Create weight-loss or gain goals (only one active goal per user)
- Log daily weights (unique per date)
- `/api/v1/progress/summary/` → view adherence & goal tracking summary

### 🥗 Nutrition
- Recipe, Ingredient, and Tag models
- Search recipes by query, diet, or tags
- Filter out unwanted ingredients
- `/api/v1/recipes/?query=salad&diet=vegan`

### 📅 Meal Planning
- Auto-generate 7-day meal plans based on goal and preferences
- 3 meals per day (breakfast, lunch, dinner)
- Substitute recipes and mark meals as eaten
- `/api/v1/meal-plans/`, `/api/v1/meal-plans/{id}/substitute/`

### 🛒 Grocery Lists
- Generate grocery list from a meal plan
- Aggregate ingredient quantities
- `/api/v1/grocery-lists/{plan_id}/generate`

### 📊 Adherence Tracking
- Track calories/macros consumed vs planned
- `/api/v1/meal-plans/{id}/adherence/`

---

## ⚙️ Tech Stack

- **Backend:** Django 5 + Django REST Framework
- **Auth:** JWT (`djangorestframework-simplejwt`)
- **Docs:** drf-spectacular (Swagger UI)
- **Database:** SQLite (dev) / PostgreSQL (production) (In future)
- **Tools:** Postman
---

---

## 📚 API Documentation

Interactive Swagger UI:  
👉 [http://127.0.0.1:8000/api/docs/]
---

## 🧰 Setup Instructions

```bash
git clone https://github.com/Ayuba-01/BiteWise-API.git
cd BiteWise-API

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate (For MacBook)

# Install dependencies
pip install -r requirements.txt

# Run migrations and seed sample recipes
python manage.py migrate
python manage.py seed_nutrition

# Run local server
python manage.py runserver
```

## 🧪 Testing the API with Postman

A full **Postman Collection** and Environment are provided for testing.

[https://www.postman.com/property-api-5769/workspace/bitewise-api/folder/40632603-84c8c926-beae-4348-8dd5-9d3b2c916d99?action=share&creator=40632603&ctx=documentation]