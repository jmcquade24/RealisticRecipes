# RealisticRecipes
recipe website

To install requirements, run:

```bash
pip install -r requirements.txt
```

To setup the database, run:

```bash
python manage.py makemigrations recipes
python manage.py migrate
python population_script.py
```