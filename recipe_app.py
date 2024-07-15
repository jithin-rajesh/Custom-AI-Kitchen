import json
import streamlit as st

# Function to search for recipes based on a query
def search_recipes(query):
    try:
        with open('processed_recipes.json', 'r') as file:
            recipes = json.load(file)

        matching_recipes = [
            recipe for recipe in recipes if query.lower() in recipe['title'].lower()
        ]

        if not matching_recipes:
            return "No matching recipes found."

        return matching_recipes

    except FileNotFoundError:
        return "The file 'processed_recipes.json' was not found."
    except json.JSONDecodeError:
        return "Error decoding JSON."

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

# Streamlit app
def main():
    st.title("Recipe Search and Generation")

    query = st.text_input("Enter a keyword or partial title of the recipe you want to look up:")

    if st.button("Search") or query in st.session_state:
        st.session_state.query = query
        matching_recipes = search_recipes(query)
        if isinstance(matching_recipes, str):  # Error message
            st.error(matching_recipes)
            st.session_state.matching_recipes = None
        else:
            st.session_state.matching_recipes = matching_recipes

    if 'matching_recipes' in st.session_state and st.session_state.matching_recipes:
        selected_recipe = st.selectbox("Select a recipe:", st.session_state.matching_recipes,
                                       format_func=lambda recipe: recipe['title'])
        selected_recipe_info = format_recipe_info(selected_recipe)
        st.text_area("Selected Recipe Information:", value=selected_recipe_info, key='recipe_info')

        if st.button("Generate JSON"):
            # Replace this section with your actual JSON generation logic
            recipe_data = {
                "recipe_title": selected_recipe['title'],
                "ingredients": selected_recipe['ingredients'],
                "steps": selected_recipe['steps']
            }
            st.json(recipe_data)
            with open("actions.json", "w") as outfile:
                json.dump(recipe_data, outfile, indent=2)
            st.success("JSON file generated and saved as 'actions.json'.")

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
