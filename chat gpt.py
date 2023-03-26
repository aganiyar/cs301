import unittest
from flask import Flask, request, jsonify
import json
import subprocess

app = Flask(__name__)

login_details={}
Art_form_options={}

def login():
    while True:
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        if username == login_details["username"] and password == login_details["password"]:
            print("Login successful!")
            return True
        else:
            print("Invalid username or password. Please try again.")

# Function to display the available art forms and allow the user to choose one

def choose_Art_form():
    print("\nSelect an art form:")
    print("1. Music")
    print("2. Dance")
    print("3. Spoken word")
    print("4. Regional theatricals")

    Art_form = int(input("Enter a number: "))

    if Art_form == 1:
        return view_or_buy("music")
    elif Art_form == 2:
        return view_or_buy("dance")
    elif Art_form == 3:
        return view_or_buy("spoken word")
    elif Art_form == 4:
        return view_or_buy("regional theatricals")
    else:
        print("Invalid input. Please try again.")
        return choose_Art_form()


def view_or_buy(Art_form_name):
    print("\nSelect an option for", Art_form_name)
    print("1. View")
    print("2. Buy")
    print("3. Add new view or buy option")

    option = int(input("Enter a number: "))

    if option == 1:
        return view_Art_form(Art_form_name)
    elif option == 2:
        return buy_Art_form(Art_form_name)
    elif option == 3:
        return add_option(Art_form_name)
    else:
        print("Invalid input. Please try again.")
        return view_or_buy(Art_form_name)


def add_option(Art_form_name):

    option_name = input("Enter option name: ")
    option_price = input("Enter option price: ")

    try:
        option_price = int(option_price)
    except ValueError:
        print("Invalid price. Please try again.")
        return add_option(Art_form_name)

    Art_form_options[Art_form_name]['view'].append(option_name)
    Art_form_options[Art_form_name]['buy'][option_name] = option_price


    print(f"Successfully added {option_name} to {Art_form_name} {view_or_buy} options.")

    return go_back_option(Art_form_name)


def view_Art_form(Art_form_name):
    view_options = Art_form_options[Art_form_name]["view"]
    if len(view_options) == 0:
        print("No options available for", Art_form_name)
    else:
        print("View options for", Art_form_name, ":")
        for option in view_options:
            print("-", option)

    return go_back_option(Art_form_name)

def buy_Art_form(Art_form_name):
    buy_options = Art_form_options[Art_form_name]["buy"]
    if len(buy_options) == 0:
        print("No options available for", Art_form_name)
    else:
        print("Buy options for", Art_form_name, ":")
        for option in buy_options:
            print("-", option)

        option = input("Enter name of option to see buy price: ")
        if option in buy_options:
            assert buy_options[option]==Art_form_options[Art_form_name]["buy"][option],"inconsistent value"
            print("Buy price for", option, "is", buy_options[option])
        else:
            print("Invalid input. Please try again.")
            return buy_Art_form(Art_form_name)

    return go_back_option(Art_form_name)

def go_back_option(Art_form_name):
    print("\nEnter 1 to go back to", Art_form_name)
    print("Enter 2 to exit")

    option = int(input("Enter a number: "))

    if option == 1:
        return view_or_buy(Art_form_name)
    elif option == 2:
        return True
    else:
        print("Invalid input. Please try again")



#regression testing:
class TestArtForms(unittest.TestCase):

    def test_choose_Art_form(self):
        self.assertEqual(choose_Art_form(), True)

    def test_login(self):
        self.assertEqual(login(), True)



#API:
@app.route('/data', methods=['GET'])
def get_data():
    # Get the data from the request
    global login_details,Art_form_options
    data = request.get_json()

    login_details=data["login"]
    Art_form_options=data["art"]


    inpt=input("enter 1 to perform regression testing , 2 to run program , 3 to exit")
    if(inpt=='1'):
        unittest.main()
    elif inpt=='2':
        while True:
            choice = input("Press 1 to login, 2 to exit ")
            if choice == "1":
                if login():
                    # integration testing:
                    assert choose_Art_form() == True, "Execution error"
            elif choice == "2":
                print("Exiting program.")
                break
            else:
                print("invalid input")

        print("program completed")

    else:
        print("invalid input")

    # Return a success message
    return jsonify({'message': 'program execution successful'})

app.run(debug=True)


'''data to pass to http://localhost:5000/data using postman:

{"login":{
    "username": "my_username",
    "password": "my_password"
},"art":{
    "music": {
        "view": ["rock", "jazz", "blues"],
        "buy": {
            "rock": 10,
            "jazz": 15,
            "blues": 20
        }
    },
    "dance": {
        "view": ["ballet", "tap", "salsa"],
        "buy": {
            "ballet": 25,
            "tap": 20,
            "salsa": 30
        }
    },
    "spoken word": {
        "view": ["poetry", "storytelling"],
        "buy": {
            "poetry": 5,
            "storytelling": 8
        }
    },
    "regional theatricals": {
        "view": ["nautanki", "jatra"],
        "buy": {
            "nautanki": 12,
            "jatra": 18
        }
    }
}}

'''

