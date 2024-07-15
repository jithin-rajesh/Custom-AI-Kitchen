# Custom AI Kitchen

This project integrates generative AI, object detection, and Raspberry Pi to create an automated kitchen capable of preparing a dish based on user input. Leveraging a dataset with over 6,500 recipes, the system guides users from recipe selection to cooking the meal.

## 1. Problem to Solve

The aim is to develop an application that can prepare a dish by following a user's input, automating the entire cooking process.

## 2. Data

We utilized the [6000+ Recipe Dataset](https://www.kaggle.com/datasets/kanishk307/6000-indian-food-recipes-dataset) which allows users to enter keywords or partial titles to retrieve a recipe of their choice.

## 3. What We Did

### Recipe Selection

1. **Data Conversion**: The dataset was converted into a JSON format, resulting in the file [processed_recipes.json](https://github.com/jithin-rajesh/Custom-AI-Kitchen/blob/main/processed_recipes.json).
2. **Search Functionality**: Users can enter a keyword or partial title to search for a dish. A dropdown menu displays matching recipes, from which users can select one to view detailed information, including the title, ingredients, cooking time, prep time, and instructions.
3. **JSON Generation**: After selecting a recipe, users can generate a JSON file, [actions.json](). Google's LLM Gemini is employed to convert the recipe into detailed, step-by-step instructions that are machine-operable.

### Simulation

1. **Simulation Creation**: The generated JSON is used to simulate the cooking process, guiding the flow of the machine.

### Hardware Integration

1. **Execution of Instructions**: The instructions in [actions.json](https://github.com/jithin-rajesh/Custom-AI-Kitchen/blob/main/actions.json) are used to execute cooking steps.
2. **Raspberry Pi 4**: A Raspberry Pi 4 with GPIO is employed to control the execution. GPIO pins are assigned for each step, enabling the automation of various cooking tasks.

## Links to Key Files

- [Recipe Selection Code](https://github.com/jithin-rajesh/Custom-AI-Kitchen/blob/main/recipe_app.py)
- [Processed Recipes JSON](https://github.com/jithin-rajesh/Custom-AI-Kitchen/blob/main/processed_recipes.json)
- [Simulation Code](https://github.com/jithin-rajesh/Custom-AI-Kitchen/blob/main/)
- [Hardware Control Code](https://github.com/jithin-rajesh/Custom-AI-Kitchen/blob/main/hardware.py)

This comprehensive approach ensures a seamless experience from selecting a recipe to preparing a dish, making cooking an automated and effortless task.
