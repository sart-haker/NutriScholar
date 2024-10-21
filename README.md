# NutriScholar
AI-based personal fitness and health assistant

Vers:1.0 Developed by Kushal Bhattarai, Sarthak Giri, Pranav Gaddam, Navneet Cheripparakkal

Problem: It's really likely for college students not to meet their daily nutrition requirements, 
so NutriScholar will allow them to put their diet at the forefront.

Solution: NutriScholar is a program with AI aspects targeted towards college students to help them meet daily nutrient values as established by the FDA, and generates a personalized workout plan based on their requirements.

How does it work?
1. A user can enter the foods they have eaten over the day and the program uses the fuzzyWuzzy NLP to find the closest match in our database with its associated macromolecules. These values for the macromolecules then get updated within a dictionary and are later used to calculate how much more the user needs to meet the DVs set by the FDA. These calculated values are then inputted into the nearest neighbor machine learning algorithm to find foods that best match the macromolecules.
2. Furthermore, users are offered a prompt to build their next/first meal by entering the type of food (if they wish to) or simply letting the program give options from the whole food items list.
3. Lastly, the fitness aspect comes into play when the program generates a workout plan for the user based on their weight-loss goal. Currently, it just advises the amount of time the user needs to exercise to burn the calories required to achieve the said goal, based on a linear regression model made using data obtained from chatGPT. 

Table of Contents:
1. functions.py - Includes the various functions used in the program, including the fuzzyWuzzy and Nearest Neighbors algorithms to match input to our database and output best meal options in accordance with the food type chosen by the user respectively, and uses the resulting calculations to make recommendations. 
2. main.py - Runs the functions and contains the print functionality. 
3. new_food_data.csv - CSV file containing all the data
4. cal_and_min.csv - CSV file containing data for calories vs. minutes of exercise regression model


Library Credits:
-fuzzyWuzzy by Jake Bayer

-levenshtein by Zdenek Nozicka

-SKLearn

-pandas
