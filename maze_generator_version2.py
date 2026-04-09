import questionary


def main():
    # The menu will "pop up" over the current terminal line
    choice = questionary.select(
        "What would you like to do?",
        choices=[
            "View Profile",
            "Upload File",
            "Settings",
            "Exit"
        ]
    ).ask()
    print(type(choice))
    # Handling the logic based on choice
    if choice == "Exit":
        print("Goodbye!")
    else:
        print(f"You selected: {choice}")


if __name__ == "__main__":
    main()
