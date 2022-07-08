import random
import json

""" 
Password generator randomly generates password and:
   => Permamently store it to the assoiciated username.
   => Functions allow to delete and change the password stored with the user.
   => Allows multiple users to be stored. 
"""


def get_password():

    """Get users current password"""

    filename = "password.json"
    with open(filename) as f:
        return json.load(f)


def get_history_password():

    """Get previously generated passwords by the user"""

    filename = "history.json"
    with open(filename) as f:
        return json.load(f)


def store_password(password_user):

    """Store user selected password"""

    filename = "password.json"
    with open(filename, "w") as f:
        json.dump(password_user, f)


def store_history_password(old_password_user):

    """Store possible passwords not selected by the user for future reference"""

    filename = "history.json"
    with open(filename, "w") as f:
        json.dump(old_password_user, f)


def generator():

    """Used to generate random sequences of characters as password"""

    characters = (
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()[]/?<>"
    )
    password = ""
    for n in range(random.randrange(20, 30)):
        password += random.choice(characters)

    return password


def password_user_checker(user, password_user):

    """When called, checks for the users current password from the json file password.json"""

    for i in password_user.keys():
        if i == user:
            password = password_user[i]
            return password
    return None


def history_password_checker(user, password_user={}, old_password_user={}):

    """When called, checks and presents passwords previously generated but weren't selected to the user"""

    for i in old_password_user.keys():
        if i[: len(user)] == user:
            prompt = input(f"\nIs\n{old_password_user[i]}\nyour password (Y/N)? ")
            if str.upper(prompt) == "Y":
                p = password_user[user]
                password_user[user] = old_password_user[i]
                old_password_user[i] = p
                store_password(password_user)
                store_history_password(old_password_user)
                print("Saving your password now.")
                return True
            elif str.upper(prompt) == "N":
                print("\nPulling next item.")
            else:
                print("\nInput not understood. Pulling next item.")

    print("\nThere are no (more) items to process.")
    return None


def password_loader(
    user, password_user={}, old_password_user={}, recycle_password=None
):

    """Loops through randgen passwords until user selects. Items not selected sen to history.json. User assigned password in password.json"""

    count = 0

    for i in old_password_user.keys():
        if i[: len(user)] == user:
            p = int(i[len(user) :])  # p for placeholder
            if p > count:
                count = p

    if recycle_password:
        count += 1
        old_password_user[user + str(count)] = recycle_password

    while True:
        password = generator()
        password_user[user] = password

        print(f"\nPassword:\n{password}")
        question = input("Is this ok (Y/N)? ")

        if str.upper(question) == "Y":
            store_password(password_user=password_user)
            store_history_password(old_password_user=old_password_user)
            print("\nYour password has been saved.")
            return password
        else:
            count += 1
            old_password_user[user + str(count)] = password_user[user]
            print(
                "\nYour password has been stored in the history list.",
                "Generating a new one.\n",
            )


def prompt_history(user, password_user, old_password_user, password):

    """Checks users history. Loops through items pregen and presents to user. User can select one until they run out."""

    print(f"\n{password}\nis your current password.")

    if str.upper(input("\nDo you want to change the password (Y/N)? ")) == "Y":
        if (
            str.upper(
                input(
                    "\nDo you want to check items in the history list for passwords (Y/N)? "
                )
            )
            == "Y"
        ):
            p = history_password_checker(user, password_user, old_password_user)
            if p:
                return None

        if str.upper(input("\nDo you want a new generated password (Y/N)? ")) == "Y":
            password_loader(
                user, password_user, old_password_user, recycle_password=password
            )
            print("Your old password has been saved to history.")
            return None

    print("\nClosing.")


def main():

    """Main hub function. Calls functions depending on given information already there."""

    user = input("\nUsername: ")
    print(f"Welcome to the passowrd generator, {user}!")

    try:
        password_user = get_password()
    except FileNotFoundError:
        password_loader(user)
    else:
        try:
            old_password_user = get_history_password()
        except FileNotFoundError:
            password_loader(user, password_user=password_user)
        else:
            password = password_user_checker(user, password_user)
            if password:
                if input("Please input original password: ") != password:
                    return 1
                prompt_history(user, password_user, old_password_user, password)
            else:
                password_loader(user, password_user, old_password_user)

# Call main function if not imported to another file
if __name__ == "__main__":
    main()