import curses
import configparser

def read_ini_file(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    return config

def display_menu(stdscr, selected_option):
    menu = ['q: Quitter', 'c: Configurer', 'g: Générer']
    height, width = stdscr.getmaxyx()
    x = 0
    for idx, item in enumerate(menu):
        stdscr.addstr(height-2, x, f"{item}")
        x += len(item) + idx + 4
    stdscr.refresh()

def main(stdscr):
    # Clear screen
    stdscr.clear()

    # Read the .ini file
    config = read_ini_file('config.ini')

    # Get the list of sections
    sections = config.sections()
    current_section_index = 0
    current_option_index = 0
    menu_selected_option = 0

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        # Display the sections and options
        stdscr.addstr(0, 0, "Configuration Sections:")
        for idx, section in enumerate(sections):
            if idx == current_section_index:
                stdscr.addstr(idx + 1, 2, f"{section}", curses.A_REVERSE)
            else:
                stdscr.addstr(idx + 1, 2, f"{section}")

        stdscr.addstr(len(sections) + 2, 0, "Options:")
        options = config.options(sections[current_section_index])
        for idx, option in enumerate(options):
            if idx == current_option_index:
                stdscr.addstr(len(sections) + 3 + idx, 2, f"-> {option}: {config.get(sections[current_section_index], option)}")
            else:
                stdscr.addstr(len(sections) + 3 + idx, 2, f"   {option}: {config.get(sections[current_section_index], option)}")

        # Display the menu at the bottom
        # stdscr.attron(curses.A_REVERSE)
        # stdscr.addstr(height - 1, 0, ' ' * (width - 1))
        # stdscr.attroff(curses.A_REVERSE)
        display_menu(stdscr, menu_selected_option)

        stdscr.refresh()

        key = stdscr.getkey()
        filename = config.get("physics", 'problem') + '.ini'
        if key == 'KEY_UP':
            if current_option_index > 0:
                current_option_index -= 1
            elif current_section_index > 0:
                current_section_index -= 1
                current_option_index = len(config.options(sections[current_section_index])) - 1
        elif key == 'KEY_DOWN':
            if current_option_index < len(options) - 1:
                current_option_index += 1
            elif current_section_index < len(sections) - 1:
                current_section_index += 1
                current_option_index = 0
        elif key == 'q':
            break
        elif key == '\n':
            # Edit the selected option
            stdscr.addstr(len(sections) + 3 + current_option_index, 2, "Enter new value: ")
            curses.echo()
            new_value = stdscr.getstr(len(sections) + 3 + current_option_index, 18)
            curses.noecho()
            config.set(sections[current_section_index], options[current_option_index], new_value.decode('utf-8'))
        elif key == 'c':
            # Handle configuration action
            pass
        elif key == 'g':
            with open(filename, 'w') as configfile:
                config.write(configfile)
            # Handle generate action
                pass

    # Save the changes to the .ini file

curses.wrapper(main)
