import pandas as pd
import json

# Load the CSV file
df = pd.read_csv('IndianFoodDatasetCSV.csv')

# Function to clean and standardize text
def clean_text(text):
    if pd.isna(text):
        return ""
    return str(text).replace('\xa0', ' ').strip()  # Replace non-breaking spaces and trim

# Function to parse and standardize the recipes
def parse_recipe(row):
    title = clean_text(row['TranslatedRecipeName'])
    
    ingredients = clean_text(row['TranslatedIngredients']).split(',')
    steps = clean_text(row['TranslatedInstructions']).split('.')
    
    prep = row['PrepTimeInMins']
    cook = row['CookTimeInMins']
    servings = row['Servings']
    
    return {
        'title': title,
        'ingredients': [i.strip() for i in ingredients if i.strip()],
        'steps': [s.strip() for s in steps if s.strip()],
        'prep': prep,
        'cook': cook,
        'servings': servings
    }

# Apply the function to each row
recipes = df.apply(parse_recipe, axis=1)

# Convert the result to a list of dictionaries
recipes_list = recipes.tolist()

# Print the first recipe
print(recipes_list[0])

# Save to JSON
with open('processed_recipes.json', 'w') as f:
    json.dump(recipes_list, f, indent=4)

# Save to CSV
processed_df = pd.DataFrame(recipes_list)
processed_df.to_csv('processed_recipes.csv', index=False)
