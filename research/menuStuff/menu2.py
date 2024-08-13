import cmd

class SubMenu(cmd.Cmd):
    """
    A class representing a sub-menu.
    """
    prompt = 'SubMenu> '
    
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def do_option1(self, arg):
        'Execute Option 1 in SubMenu.'
        print("SubMenu: Executed Option 1.")

    def do_option2(self, arg):
        'Execute Option 2 in SubMenu.'
        print("SubMenu: Executed Option 2.")

    def do_back(self, arg):
        'Return to the main menu.'
        print("Returning to Main Menu...")
        return True  # Returning True exits the current cmd loop

    def do_help(self, arg):
        'List available commands in SubMenu.'
        super().do_help(arg)

class MainMenu(cmd.Cmd):
    """
    A class representing the main menu.
    """
    prompt = 'MainMenu> '

    def do_menu1(self, arg):
        'Access Menu 1.'
        print("Welcome to Menu 1.")
        submenu = SubMenu(self)
        submenu.prompt = 'Menu1> '
        submenu.cmdloop()

    def do_menu2(self, arg):
        'Access Menu 2.'
        print("Welcome to Menu 2.")
        submenu = SubMenu(self)
        submenu.prompt = 'Menu2> '
        submenu.cmdloop()

    def do_exit(self, arg):
        'Exit the application.'
        print("Exiting the application. Goodbye!")
        return True  # Returning True exits the cmd loop

    def do_help(self, arg):
        'List available commands in MainMenu.'
        super().do_help(arg)

if __name__ == '__main__':
    main_menu = MainMenu()
    print("Welcome to the Application!")
    print("Type 'help' to see available commands.\n")
    main_menu.cmdloop()
