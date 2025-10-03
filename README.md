# BiteWise — Smart Meal Planner & Weight-loss Coach

BiteWise is a Django REST Framework API that helps users plan meals, generate grocery lists, and track progress toward their weight loss or fitness goals.  

## Features (so far)
- **User Authentication** (JWT): Register, Login, Refresh, `/users/me`
- **Custom User Model**: email login, profile fields (sex, dob, height, activity level, timezone)
- **Preferences & Goals**:
  - User preferences (diet type, allergens, disliked ingredients)
  - Goals with one-active constraint (lose, maintain, gain weight)
  - Weight logs (unique per date, progress tracking)
- **Nutrition**:
  - Recipes with macros (kcal, protein, carbs, fat)
  - Ingredients & tags
  - Search and filter recipes (diet, tags, exclude ingredients, order by macros)
  - Seed command to preload demo recipes and ingredients
- **API Documentation**: Swagger UI at `/api/docs`

## Tech Stack
- Django 5.x + Django REST Framework
- JWT authentication (`djangorestframework-simplejwt`)
- drf-spectacular (OpenAPI/Swagger docs)
- PostgreSQL (planned), SQLite (dev)

## Setup
```bash
# clone repo
git clone https://github.com/YOUR-USERNAME/bitewise.git
cd bitewise

# create venv
python3 -m venv venv
source venv/bin/activate

# install dependencies
pip install -r requirements.txt

# run migrations
python manage.py migrate

# create superuser
python manage.py createsuperuser 

# run server
python manage.py runserver
