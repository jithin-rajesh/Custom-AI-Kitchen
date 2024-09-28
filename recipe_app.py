import json
import google.generativeai as genai
import streamlit as st

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

# Function to format recipe details
def format_recipe_info(recipe):
    ingredients = "\n".join(recipe['ingredients'])
    steps = "\n".join(recipe['steps'])
    return (
        f"Title: {recipe['title']}\n"
        f"Prep Time: {recipe['prep']} minutes\n"
        f"Cook Time: {recipe['cook']} minutes\n"
        f"Servings: {recipe['servings']}\n\n"
        f"Ingredients:\n{ingredients}\n\n"
        f"Steps:\n{steps}"
    )
genai.configure(api_key="YOUR_API_KEY")
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
            selected_recipe_info = format_recipe_info(selected_recipe)
            st.text_area("Selected Recipe Information:", value=selected_recipe_info, key='recipe_info')

            if st.button("Generate JSON"):
                response = model.generate_content(
                f"Using the recipe details: {selected_recipe_info}, create a JSON file with precise step-by-step actions for a "
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
            json_string = response.text.replace('\\', '').replace('\n', '')
            try:
                recipe_data = json.loads(json_string)
                st.json(recipe_data)
                with open("actions.json", "w") as outfile:
                    json.dump(recipe_data, outfile, indent=2)
                st.success("JSON file generated and saved as 'actions.json'.")
            except json.JSONDecodeError as e:
                st.error(f"Error decoding JSON: {e}")
    
    # CSS for dynamic text_area height based on content
    st.markdown("""
        <style>
            .st-eb {
                height: auto !important;
                min-height: 200px;
            }
        </style>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
