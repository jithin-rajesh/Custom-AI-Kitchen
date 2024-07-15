# Custom AI Kitchen
This project uses generative AI, object detection and Raspberry Pi to create an automated kitchen that uses a dataset with over 6500 recipes to make a dish of a user's choice.

## 1. Problem to solve
Build an application that can create a dish after getting user's input.

## 2. Data 
We used the [6000+ Recipe Dataset](https://www.kaggle.com/datasets/kanishk307/6000-indian-food-recipes-dataset) from which user's can enter a keyword of partial title to get a recipe of their choice.

## 3. What we did
[Recipe Selection](https://github.com/jithin-rajesh/Custom-AI-Kitchen/blob/main/recipe_app.py) 

1. The dataset was converted to the JSON format, [processed_recipes.json](https://github.com/jithin-rajesh/Custom-AI-Kitchen/blob/main/processed_recipes.json).
2. The users can enter a keyword or partial title to search for a dish of their choice. A recipe can be selected from a dropdown containing matching recipes, recipe information which contains title, ingredients, cooking time, prep time and instructions will be shown.
3. Users are then given an option to G=generate a JSON file,[actions.json](). Here, Google's LLM Gemini is used to convert the recipe into detailed step-by-step instructions in a machine operable format.

[Simulation](https://github.com/jithin-rajesh/Custom-AI-Kitchen/blob/main/) 

1. The generated JSON is used to create a simulation alongside the flow of the machine.

[Hardware Side](https://github.com/jithin-rajesh/Custom-AI-Kitchen/blob/main/hardware.py)

1. The instructions in [actions.json](https://github.com/jithin-rajesh/Custom-AI-Kitchen/blob/main/actions.json) is then used to execute steps for cooking the dish.
2. A Raspberry Pi 4 with GPIO is used for the execution, GPIO pins are assigned for each step.


