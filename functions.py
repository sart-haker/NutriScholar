import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
#from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors
from fuzzywuzzy import process

# Load the dataset
df = pd.read_csv('new_food_data.csv')

food_names = df['Name'].tolist()

# Function to find the top match in the CSV database and return its name so that macros can properly be tracked.
def find_top_match_name(input_name):
    # Use fuzzywuzzy to find the top match in the 'Name' column
    top_match = process.extract(input_name, food_names, limit = 5)
    
    top_match_names = [match[0] for match in top_match]
    return top_match_names

#updates nutrients dictionary based on user input
def nut_tracker(nut_dict, df):
    nut_local = nut_dict
    meals = int(input("How many meals did you have today? "))
    for i in range(meals):
        print("\nMEAL", i + 1, "-\n")
        msg = "Please enter what you had in meal " + str(i+1) + ", type 'Done' to quit: "
        foodEaten = input(msg)
        while(foodEaten.lower() != "done"):
            foodPossible = find_top_match_name(foodEaten) #Finds the top matches
            foodOptions = "Choose one (by number):\n"
            for i in range(5):
                foodOptions += str(i+1) + ". " + foodPossible[i] + "\n"
            
            foodSpec = int(input(foodOptions))
            for i in range(len(df['Name'])):
                if df['Name'][i] == foodPossible[foodSpec - 1]:
                    for nut in nut_local:
                        nut_local[nut] += df[nut][i]
                    break
            print("")
            foodEaten = input(msg)
        print("")
    return nut_local

# def nut_remaining(nut_dict, nut_goal):
 
# Select relevant columns
data = df[['Name', 'Food Group', 'Calories', 'Fat (g)', 'Protein (g)', 
           'Carbohydrates (g)', 'Sugar (g)', 'Fiber (g)', 'Cholestrol (mg)'
            , 'Sodium (mg)','Calcium (mg)','Iron (mg)']]

# Function to train the Nearest Neighbors model for a specific food group (or all food groups if food_group is empty)
def train_model_for_food_group(food_group, n_neighbors=5):
    # If food_group is not empty, filter the dataset to only include rows from the specified food group
    if food_group:
        group_data = data[data['Food Group'] == food_group]
    else:
        # Use the entire dataset if food_group is empty
        group_data = data
    
    # If the group is empty, return None
    if group_data.empty:
        return None, None
    
    # Get the numeric features for the selected data
    numeric_features = group_data[['Calories', 'Fat (g)', 'Protein (g)', 'Carbohydrates (g)', 
                                   'Sugar (g)', 'Fiber (g)', 'Cholestrol (mg)', 
                                    'Sodium (mg)','Calcium (mg)','Iron (mg)']].values
    
    # Train a Nearest Neighbors model on the selected data with n_neighbors = 5
    model = NearestNeighbors(n_neighbors=n_neighbors)
    model.fit(numeric_features)
    
    return model, group_data

# Function to find the top N closest food items within the same food group or across all food groups based on nutritional values
def find_closest_food(food_group, calories, fat, protein, carbohydrates, sugar, fiber, cholestrol, sodium,calcium,iron, top_n=5):
    # Train the model on the specified food group (or all groups if food_group is empty)
    model, group_data = train_model_for_food_group(food_group, n_neighbors=top_n)
    
    # If no data is available for the food group, return a message
    if model is None:
        return f"No data available for the specified food group."
    
    # Prepare the input nutritional data
    input_data = [[calories, fat, protein, carbohydrates, sugar, fiber, cholestrol, sodium,calcium,iron]]
    
    # Find the top N closest matches within the same (or all) food group(s)
    distances, indices = model.kneighbors(input_data)
    
    # Get the corresponding food names and groups
    closest_foods = []
    for idx in indices[0]:
        food_name = group_data.iloc[idx]['Name']
        food_group = group_data.iloc[idx]['Food Group']
        closest_foods.append((food_name, food_group))
    
    return closest_foods

def time_pred(cals):
    data = pd.read_csv('cal_and_min.csv') 
    X = data[['Calories_Burned']]
    y = data['Minutes of Exercise']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=23)

    model = LinearRegression()
    # print(X_train, X_test, y_train, y_test, sep='\n')

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    #mse = mean_squared_error(y_test, y_pred)
    #r2 = r2_score(y_test, y_pred)
    c = model.intercept_
    m = model.coef_[0]
    pred = m * cals + c
    return pred
    