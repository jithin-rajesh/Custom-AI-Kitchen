import json
import google.generativeai as genai
import streamlit as st
import re
import math

# Function to load all recipes from the JSON file
def load_recipes():
    try:
        with open('processed_recipes.json', 'r') as file:
            recipes = json.load(file)
        return recipes
    except FileNotFoundError:
        st.error("The file 'processed_recipes.json' was not found.")
        return []
    except json.JSONDecodeError:
        st.error("Error decoding JSON.")
        return []

# Function to format and display the recipe with adjustable quantities
def format_recipe_info(recipe):
    quantities = []
    ingredients_list = []
    ingredients = recipe['ingredients']
    
    # Parse the original ingredients
    for item in ingredients:
        try:
            # Regular expression to match quantity (numbers, fractions like 1/2, etc.)
            match = re.match(r"^([\d\s\/\W]+)?\s*(.*)", item)
            quantity = match.group(1).strip() if match.group(1) else None  # Add None for missing portion sizes
            ingredient = match.group(2)
            
            # Convert quantity to a float if possible, leave None otherwise
            if quantity:
                # Remove any units and keep only the numeric part for adjustment
                clean_quantity = re.sub(r'[^\d\/]', '', quantity).strip()
                try:
                    clean_quantity = eval(clean_quantity)  # Handle fractions like 1/2
                except:
                    clean_quantity = 1  # Default to 1 if parsing fails
            else:
                clean_quantity = None  # No quantity given

            quantities.append(clean_quantity)
            ingredients_list.append(ingredient.strip())
        
        except Exception as e:
            print(f"Error parsing ingredient: {item}")
            quantities.append(None)
            ingredients_list.append(item)

    steps = "\n".join(recipe['steps'])

    return quantities, ingredients_list, (
        f"Title: {recipe['title']}\n"
        f"Prep Time: {recipe['prep']} minutes\n"
        f"Cook Time: {recipe['cook']} minutes\n"
        f"Servings: {recipe['servings']}\n\n"
        f"Ingredients:\n" + "\n".join(ingredients) + "\n\n"
        f"Steps:\n{steps}"
    )

# Configure Google Generative AI
genai.configure(api_key='YOUR_API_KEY')
model = genai.GenerativeModel('gemini-1.5-pro-latest', generation_config={"response_mime_type": "application/json"})

# Streamlit app
def main():
    st.title("Recipe Search and Generation")
    
    recipes = load_recipes()

    if recipes:
        recipe_titles = [recipe['title'] for recipe in recipes]
        selected_title = st.selectbox("Select a recipe:", recipe_titles)

        # Find the selected recipe from the list of recipes
        selected_recipe = next((recipe for recipe in recipes if recipe['title'] == selected_title), None)

        if selected_recipe:
            # Get the original quantities, ingredients, and recipe info
            quantities, ingredients_list, selected_recipe_info = format_recipe_info(selected_recipe)

            st.subheader("Original Recipe Information:")
            st.text_area("Original Recipe Information", value=selected_recipe_info, height=300)

            # Create sliders for each ingredient's quantity
            st.subheader("Adjust Ingredient Quantities:")
            adjusted_quantities = []
            for i, (quantity, ingredient) in enumerate(zip(quantities, ingredients_list)):
                # If quantity is None, don't create a slider
                if quantity is None:
                    adjusted_quantities.append(f"N/A {ingredient}")
                else:
                    # Add a slider to adjust quantity, default value is the original quantity
                    new_quantity = st.number_input(f"Adjust {ingredient} quantity", min_value=0.1, value=float(quantity), step=0.1, key=f"slider_{i}")
                    # Apply ceiling and format it to two decimal places
                    new_quantity = math.ceil(new_quantity * 100) / 100
                    adjusted_quantities.append(f"{new_quantity:.2f} {ingredient}")
            
            # Display the adjusted quantities after the sliders
            st.subheader("Adjusted Recipe Information:")
            st.text_area("Adjusted Ingredients:", value="\n".join(adjusted_quantities), height=200)

            if st.button("Generate JSON"):
                # Construct the adjusted recipe details for the prompt
                adjusted_recipe_info = (
                    f"Title: {selected_recipe['title']}\n"
                    f"Prep Time: {selected_recipe['prep']} minutes\n"
                    f"Cook Time: {selected_recipe['cook']} minutes\n"
                    f"Servings: {selected_recipe['servings']}\n\n"
                    f"Ingredients:\n" + "\n".join(adjusted_quantities) + "\n\n"
                    f"Steps:\n{'\n'.join(selected_recipe['steps'])}"
                )

                # Generate the content using Google Generative AI
                response = model.generate_content(
                    f"Using the recipe details: {adjusted_recipe_info}, create a JSON file with precise step-by-step actions for a "
                    "cooking machine. The JSON should follow this exact format:\n\n"
                    "{\n"
                    "  \"steps\": [\n"
                    "    {\n"
                    "      \"step\": <int>,\n"
                    "      \"action\": \"<string>\",\n"
                    "      \"ingredients\": [\n"
                    "        {\n"
                    "          \"name\": \"<string>\",\n"
                    "          \"quantity\": <float>,\n"
                    "          \"unit\": \"<string>\"\n"
                    "        }\n"
                    "      ],\n"
                    "      \"parameters\": \"<string>\",\n"
                    "      \"time\": <int>\n"
                    "    }\n"
                    "  ]\n"
                    "}"
                )

                try:
                    # Ensure the response is valid before loading it into JSON
                    recipe_data = json.loads(response.text)
                    st.json(recipe_data)

                    # Save the generated JSON to a file
                    with open("actions.json", "w") as outfile:
                        json.dump(recipe_data, outfile, indent=2)
                    st.success("JSON file generated and saved as 'actions.json'.")
                except json.JSONDecodeError as e:
                    st.error(f"Error decoding JSON: {e}")

if __name__ == "__main__":
    main()
