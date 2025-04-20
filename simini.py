import curses
import validators

try:
    import config
except ImportError:
    print("No config.py file found. Please create one with the necessary configurations.")
    exit(1)

def display_menu(stdscr, selected_option):
    menu = ['q: Quitter', 'c: Configurer', 'g: Générer']
    height, width = stdscr.getmaxyx()
    x = 0
    for idx, item in enumerate(menu):
        stdscr.addstr(height-2, x, f"{item}")
        x += len(item) + idx + 4
    stdscr.refresh()

def get_options(section):
    return [field.name for field in section.__dataclass_fields__.values()]

def get_enum_values(enum_type):
    return list(enum_type)

def main(stdscr):
    # Clear screen
    stdscr.clear()

    # Get the list of sections
    sections = list(config.Parameters.__dataclass_fields__.keys())
    current_section_index = 0
    current_option_index = 0
    menu_selected_option = 0

    parameters = config.Parameters()

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
        current_section = getattr(parameters, sections[current_section_index])
        options = get_options(current_section)
        for idx, option in enumerate(options):
            value = getattr(current_section, option)
            if idx == current_option_index:
                stdscr.addstr(len(sections) + 3 + idx, 2, f"{option}: {value}", curses.A_REVERSE)
            else:
                stdscr.addstr(len(sections) + 3 + idx, 2, f"{option}: {value}")

        # Display the menu at the bottom
        display_menu(stdscr, menu_selected_option)

        stdscr.refresh()

        key = stdscr.getkey()
        if key == 'KEY_UP':
            if current_option_index > 0:
                current_option_index -= 1
            elif current_section_index > 0:
                current_section_index -= 1
                current_option_index = len(get_options(getattr(parameters, sections[current_section_index]))) - 1
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
            new_value = stdscr.getstr(len(sections) + 3 + current_option_index, 18).decode('utf-8')
            curses.noecho()
            # Convert new_value to the appropriate type
            field_type = type(getattr(current_section, options[current_option_index]))
            setattr(current_section, options[current_option_index], field_type(new_value))
        elif key == 'c':
            # Handle configuration action
            pass
        elif key == 'g':
            # Handle generate action
            pass
        elif key in ['KEY_LEFT', 'KEY_RIGHT']:
            option = options[current_option_index]
            value = getattr(current_section, option)
            field_type = type(value)
            if isinstance(value, str): continue # on ne doit pas pouvoir changer la valeur d'une chaîne de caractères avec les flèches
            if key == 'KEY_LEFT':
                new_value = value.prev()
            elif key == 'KEY_RIGHT':
                new_value = next(value)
            else:
                continue

            setattr(current_section, option, new_value)

curses.wrapper(main)
