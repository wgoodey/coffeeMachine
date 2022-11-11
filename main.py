import data


def format_money(cost):
    """Takes a number (int or float) and formats it to dollars."""
    if isinstance(cost, int):
        return "${0:.2f}".format(cost / 100)
    else:
        return "${0:.2f}".format(cost)


def print_report():
    """Prints a report of the available resources."""
    print()
    print("These are the current resources:")
    print(f'Water: {data.resources["water"]}ml')
    print(f'Milk: {data.resources["milk"]}ml')
    print(f'Coffee: {data.resources["coffee"]}g')
    print(f'Money: {format_money(data.resources["money"])}')
    print()


def check_sufficient_resources(name_of_item):
    """Takes the name of a menu item as a string and returns True if resources are available and False if not."""
    # get menu item
    menu_item = data.MENU[name_of_item]

    # get required resources for selected menu item
    try:
        water_required = menu_item["ingredients"]["water"]
    except KeyError:
        water_required = 0
    try:
        milk_required = menu_item["ingredients"]["milk"]
    except KeyError:
        milk_required = 0
    try:
        coffee_required = menu_item["ingredients"]["coffee"]
    except KeyError:
        coffee_required = 0

    resources_available = True
    # check if sufficient resources are available
    if data.resources["water"] < water_required:
        resources_available = False
        print(f"Sorry, there is not enough water to make a {name_of_item}.")
    if data.resources["milk"] < milk_required:
        resources_available = False
        print(f"Sorry, there is not enough milk to make a {name_of_item}.")
    if data.resources["coffee"] < coffee_required:
        resources_available = False
        print(f"Sorry, there is not enough coffee to make a {name_of_item}.")

    return resources_available


def process_coins(num_quarters, num_dimes, num_nickels, num_pennies):
    """Takes the number of quarters, dimes, nickels, and pennies and returns the total in cents."""
    return (num_quarters * 25) + (num_dimes * 10) + (num_nickels * 5) + num_pennies


def check_sufficient_funds(name_of_item, money_inserted):
    """Takes the name of a menu item and the amount of money inserted and returns true if money_inserted is
    enough to pay for the item."""
    # get menu item cost
    cost = int(data.MENU[name_of_item]["cost"] * 100)

    return money_inserted >= cost


def manage_resources(name_of_item, money_inserted):
    """Takes the name of an item and the amount of money inserted and adjusts resources accordingly."""
    # get menu item
    try:
        menu_item = data.MENU[name_of_item]
        cost = int(menu_item["cost"] * 100)
    except KeyError:
        print("That item isn't on the menu.")
        return

        # get required resources for selected menu item
    try:
        water_required = menu_item["ingredients"]["water"]
    except KeyError:
        water_required = 0
    try:
        milk_required = menu_item["ingredients"]["milk"]
    except KeyError:
        milk_required = 0
    try:
        coffee_required = menu_item["ingredients"]["coffee"]
    except KeyError:
        coffee_required = 0

    data.resources["money"] += money_inserted
    excess_money = money_inserted - cost

    if data.resources["money"] < excess_money:
        excess_money = data.resources["money"]

    data.resources["water"] -= water_required
    data.resources["milk"] -= milk_required
    data.resources["coffee"] -= coffee_required
    data.resources["money"] -= excess_money

    return excess_money


def add_resources():
    """Prompts user to add resources to the machine."""
    back = False
    while not back:
        print_report()
        option = input("What will you add? ").lower()
        try:
            if option not in data.resources:
                if option == "exit":
                    print("Returning to main menu.")
                    return
                else:
                    print(f"{option} is not a valid option.")
            else:
                amount = int(input(f"How much {option}? "))
                data.resources[option] += amount
        except ValueError:
            print("Please select water, milk or coffee.")


def get_selection():
    """Returns input from the user regarding which action the coffee maker should take."""
    # prompt for item selection
    menu_item = " "
    while menu_item not in data.MENU:
        try:
            menu_item = input("\nWhat would you like? (espresso/latte/cappuccino): ").lower()
            var = data.MENU[menu_item]
        except KeyError:
            if menu_item == "report" or menu_item == "off" or menu_item == "add":
                return menu_item
            else:
                print("That item isn't on the menu.")
    return menu_item


def get_coins(coin_type):
    """Takes a type of coin (plural) and asks the user how many they inserted."""
    num_coins = ""
    while not isinstance(num_coins, int):
        try:
            num_coins = int(input(f"How many {coin_type} did you insert? "))
        except ValueError:
            print("Please enter a whole number.")
    return num_coins


while True:
    item = get_selection()
    if item == "report":
        print_report()
    elif item == "add":
        add_resources()
    elif item == "off":
        # break loop
        print("Turning off coffee machine.")
        break
    else:
        # check if sufficient resources
        is_enough_resources = check_sufficient_resources(item)
        if is_enough_resources:
            print(f"{item} costs {format_money(data.MENU[item]['cost'])}")
        else:
            continue

        # get money from user
        quarters = get_coins("quarters")
        dimes = get_coins("dimes")
        nickels = get_coins("nickels")
        pennies = get_coins("pennies")
        money = process_coins(quarters, dimes, nickels, pennies)
        print(f"You inserted {format_money(money)}")

        # check if sufficient funds
        is_enough_money = check_sufficient_funds(item, money)
        if is_enough_money:
            change = manage_resources(item, money)
            if change > 0:
                print(f"Thank you! Your change is {format_money(change)}. Enjoy your {item}.")
            else:
                print(f"Thank you! Enjoy your {item}.")
        else:
            print(f"Sorry, that wasn't enough. Refunding your money: {format_money(money)}.")
