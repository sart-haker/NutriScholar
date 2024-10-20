import pandas as pd
import functions
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import OneHotEncoder
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
#from sklearn.metrics import mean_squared_error, r2_score
#import matplotlib.pyplot as plt

df = pd.read_csv('new_food_data.csv')

#Macros and nutrients
nut_dict = {"Calories": 0, "Protein (g)": 0, "Carbohydrates (g)": 0,"Fat (g)": 0, "Cholestrol (mg)": 0, "Sodium (mg)": 0, "Sugar (g)": 0, "Iron (mg)": 0, "Calcium (mg)": 0, "Fiber (g)": 0}

#Daily Values from the FDA => https://www.fda.gov/media/99059/download or for more specfiic https://www.nal.usda.gov/human-nutrition-and-food-safety/dri-calculator
# FAT = 78 (g)
# CALORIES = 2000 (Cal)
# SATURATED = 20 (g)
# CHOLESTROL = 300 (mg)
# CARBS = 275 (g)
# SODIUM = 2300 (mg)
# FIBER = 28 (g)
# PROTEIN = 50 (g)
# SUGARS = 50 (g)
# IRON = 18 (mg)
# CALCIUM = 1000 (mg)
dv_Values = {"Fat (g)": 78, "Protein (g)": 50, "Calories": 2000, "Carbohydrates (g)": 275, "Sugar (g)" : 50, "Cholestrol (mg)": 300, "Sodium (mg)":2300, "Iron (mg)":18, "Calcium (mg)": 1000, "Fiber (g)": 28}

#Input and prints
print("""
**    **  **    **  ******  *****     ****  ******  ******  **     **   *****   **           *        *****
**    **  **    **    **    **   **    **   **      **      **     **  **   **  **          * *       **   **
***   **  **    **    **    **   **    **   **      **      **     **  **   **  **         ** **      **   **
** *  **  **    **    **    *****      **   ******  **      *********  **   **  **        *******     *****
**  * **  **    **    **    **  **     **       **  **      **     **  **   **  **       **     **    **  **
**   ***  **    **    **    **   **    **       **  **      **     **  **   **  **      **       **   **   **
**    **   ******     **    **    **  ****  ******  ******  **     **   *****   *****  **         **  **    **
""", end = "")
print("\nVers:1.0 Developed by Kushal Bhattarai, Sarthak Giri, Pranav Gaddam, Navneet Cheripparakkal \n \n")

welcm = " !!! Welcome to your personal health and fitness assistant !!! "
print("=" * 110)
print(f'{welcm:^110}')
print("=" * 110 + "\n")

hasEatenFood = True if input("Have you eaten anything today? ").lower() == "yes" else False
if (hasEatenFood):
    #Calculate the macros based off what the user inputs
    nut_dict = functions.nut_tracker(nut_dict, df)
    #make a dictionary that has the target amounts based off the calculated values for the foodsEaten
    # so it takes the DV values subtracted from the value in current nutrition to determine what additional
    #nutrients is needed in the persons diet
nutrientGoal = {"Calories": 2000 - nut_dict["Calories"], "Protein (g)": 50 - nut_dict["Protein (g)"], "Carbohydrates (g)":275 - nut_dict["Carbohydrates (g)"],
                "Fat (g)": 78 - nut_dict["Fat (g)"], "Sugar (g)" : 50 - nut_dict["Sugar (g)"], "Cholestrol (mg)":300 - nut_dict["Cholestrol (mg)"], "Sodium (mg)":2300 - nut_dict["Sodium (mg)"], "Iron (mg)":18 - nut_dict["Iron (mg)"], "Calcium (mg)":1000 - nut_dict["Calcium (mg)"], "Fiber (g)":28 - nut_dict["Fiber (g)"]}

#Stores the high,low, and met intakes
high_intake = {}
low_intake = {}
met_intake = []

#Finds the high,low,and met intakes
for key in nut_dict:
    #Here is the values being exceeded. 20% greater is considered bad : https://www.fda.gov/food/nutrition-facts-label/daily-value-nutrition-and-supplement-facts-labels#:~:text=As%20a%20general%20guide%3A%205%25%20DV%20or%20less,Lower%20in%20saturated%20fat%2C%20sodium%2C%20and%20added%20sugars.
    if nut_dict[key] > dv_Values[key] * 1.2: 
            #print(f"Be careful! Your intake of {key} is higher than recomended!")
            high_intake[key] = nut_dict[key] - dv_Values[key]
    elif nut_dict[key] < dv_Values[key]:
            #print(f"You need {nutrientGoal[key]:.2f} more {key} to meet the daily value requirement!")
            low_intake[key] = abs(nut_dict[key] - dv_Values[key])
    else:
            #print(f"Great Job! You've achieved the daily goal for {key}.")
            met_intake.append(key)

print()

#Prints out the higher than recomended in a section
if len(high_intake) != 0:
    print(f"Be careful! Your intake of the following is higher than recomended!")
    for i in high_intake:
        print(f'{i} by {high_intake[i]}')

#Prints out the lower than recomended intake in a section
if len(low_intake) != 0:
    print(f"You need more of the following to meet the daily value requirement!")
    for i in low_intake:
        print(f"{i} - {low_intake[i]}")

#Prints out the met amounts
if len(met_intake) > 0:
    print(f"Great Job! You've achieved the daily goal for following.")
    for i in range(len(met_intake)):
        print(met_intake[i])

#Ask the user for parameters that they want when making the recomendation.
mealNum = "next" if hasEatenFood else "first"
msg2 = "\nDo you wish to plan your " + mealNum + " meal? "
planMeal = True if input(msg2).lower() == "yes" else False
if (planMeal):
    mealmsg = " MEAL BUILDER "
    
    print(f"\n{mealmsg:-^{len(welcm)}}\n")
    food_category = input("Choose the category of food that you want by number or press enter...\n1. Beverages\n2. Baked Foods\n3. Snacks\n4. Sweets\n5. Vegetables\n6. American Indian\n7. Restaurant Foods\n8. Meats\n9. Dairy and Egg Products\n10. Breakfast Cereals\n11. Beans and Lentils\n12. Fish\n13. Fruits\n14. Grains and Pasta\n15. Nuts and Seeds\n16. Prepared Meals\n")
    food_type = ["Beverages", "Baked Foods", "Snacks", "Sweets", "Vegetables", "American Indian", "Restaurant Foods", "Meats", "Dairy and Egg Products", "Breakfast Cereals", "Beans and Lentils", "Fish", "Fruits", "Grains and Pasta","Nuts and Seeds","Prepared Meals"]
    category = ""
    if food_category != "":
        category = food_type[int(food_category)-1]

    # Gets the values from the dictionary nutrientGoal
    calories = nutrientGoal["Calories"]
    fat = nutrientGoal["Fat (g)"]
    protein = nutrientGoal["Protein (g)"]
    carbohydrates = nutrientGoal["Carbohydrates (g)"]
    sugar = nutrientGoal["Sugar (g)"]
    fiber = nutrientGoal["Fiber (g)"]
    cholesterol = nutrientGoal["Cholestrol (mg)"]
    sodium = nutrientGoal["Sodium (mg)"]
    iron = nutrientGoal["Iron (mg)"]
    calcium = nutrientGoal["Calcium (mg)"]

    # Find the top 5 closest food items within the same or all food groups
    top_5_foods = functions.find_closest_food(category, calories, fat, protein, carbohydrates, sugar, fiber, cholesterol,sodium,calcium,iron, top_n=5)
    print("Based on your selection, here's the best meals you can have to achieve your daily goal:\n")
    #Output recomended foods by using an AI/ML 
    #based on input in the targeted nutrient goal and what the person wants to eat.
    for i, (food_name, food_group) in enumerate(top_5_foods, start=1):
        print(f"{i}: {food_name} for 100 (g)")
        print(f"\tCalories = {df['Calories'][df['Name'].tolist().index(food_name)]}")
        print(f"\tProtein (g) = {df['Protein (g)'][df['Name'].tolist().index(food_name)]}")
        print(f"\tFat (g) = {df['Fat (g)'][df['Name'].tolist().index(food_name)]}")
        print(f"\tCarbohydrates (g) = {df['Carbohydrates (g)'][df['Name'].tolist().index(food_name)]}\n")

isExercise = True if input("Do you want a workout plan for the day? ").lower() == "yes" else False
if (isExercise):
    weight = int(input("How much weight do you aim to lose (in lbs)? "))
    weeks = int(input("Within how many weeks do you target to lose weight? "))
    cal = 500 * weight / weeks
    mins = functions.time_pred(cal)
    predmsg = 'Prediction Model Running'
    print(f'\n{predmsg:-^110}\n')
    if mins < 60:
        print(f'You must workout for a minimum of {mins:.2f} mins each day to achieve your goal.')
    else:
        print(f'You must workout for a minimum of {(mins / 60):.2f} hours each day to achieve your goal.')

byemsg = " Thank you for using NUTRISCHOLAR. ENJOY YOUR MEAL "
print(f"{byemsg:=^110}")