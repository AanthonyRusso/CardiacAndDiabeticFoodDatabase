import db
import models

db.init_db()

while True:
    print("\nFood Tracker")
    print("1. Add food")
    print("2. View all foods")
    print("3. Search for food")
    print("0. Exit")

    choice = input("Choice: ")

    if choice == "1":
        name = input("Name: ")
        category = input("Category: ")
        carbs = float(input("Carbs (g): "))
        GI = float(input("Glycemic Index: "))
        GINote = input("GI note: ")
        sodium = float(input("Sodium (mg): "))
        SodiumStatus = input("Sodium status (Low/Medium/High): ")
        calories = float(input("Calories: "))
        ServingSize = input("Serving Size: ")

        models.add_food(name, category, carbs, GI, GINote, sodium, SodiumStatus, calories, ServingSize)
    
    elif choice == "2":
        for food in models.get_all_foods():
            print(food)
    elif choice == "3":
        food_name = input("What food would you like to search for?")

        result = models.find_food_info(food_name)

        if result is None:
            print("could not find food")
        else:
            print(result)
    elif choice == "0":
        break