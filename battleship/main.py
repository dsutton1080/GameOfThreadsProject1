sensible_input = False
while not sensible_input:
    choice = input("GUI or Terminal: ")
    if choice.upper() == "GUI":
        sensible_input = True
        import gui_control
    elif choice.upper() == "TERMINAL":
        sensible_input = True
        import setup
    else:
        print("Come on, Man.")