import curses
import validators

try:
    import config
except ImportError:
    print("No config.py file found. Please create one with the necessary configurations.")
    exit(1)

class SimIniEditor:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.parameters = config.Parameters()
        self.current_section_index = 0
        self.current_option_index = 0
        self.menu_selected_option = 0
        self.focus_right = False  # True if the focus is on the right panel, False otherwise
        self.menu_size = 4
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)

    def display_menu(self):
        menu = ['q: Quitter', 'c: Configurer', 'g: Générer', 'h: Aide']
        if not self.focus_right:
            menu.append('Tab/Enter : Panel droit')
        else:
            menu.append('Shift+Tab/Echap : Panel gauche')
            menu.append('Flèches G et D: Changer la valeur')
            menu.append("Enter: Editer la valeur")
        height, width = self.stdscr.getmaxyx()
        for xi in range(width):
            self.stdscr.addch(height-self.menu_size, xi, curses.ACS_HLINE)
        x = 2
        for idx, item in enumerate(menu):
            self.stdscr.addstr(height-self.menu_size+1, x, f"{item}")
            x += len(item) + idx + 4
        self.stdscr.refresh()

    def get_options(self, section):
        return [field.name for field in section.__dataclass_fields__.values()]

    def get_enum_values(self, enum_type):
        return list(enum_type)

    def draw_vertical_line(self, height, mid):
        for y in range(height):
            self.stdscr.addch(y, mid, curses.ACS_VLINE)

    def reset_cursor(self):
        self.current_option_index = 0

    def run(self):
        while True:
            self.stdscr.clear()
            height, width = self.stdscr.getmaxyx()
            mid = width // 2

            # Draw the vertical line
            self.draw_vertical_line(height-self.menu_size, mid)

            # Display the sections on the left
            self.stdscr.addstr(0, 0, "Configuration Sections:")
            sections = list(self.parameters.__dataclass_fields__.keys())
            for idx, section in enumerate(sections):
                if not self.focus_right and idx == self.current_section_index:
                    self.stdscr.addstr(idx + 1, 2, f"{section}", curses.A_REVERSE)
                else:
                    self.stdscr.addstr(idx + 1, 2, f"{section}")

            # Display the options on the right
            self.stdscr.addstr(0, mid + 2, "Options:")
            if sections:
                current_section = getattr(self.parameters, sections[self.current_section_index])
                options = self.get_options(current_section)
                for idx, option in enumerate(options):
                    value = getattr(current_section, option)
                    if self.focus_right and idx == self.current_option_index:
                        self.stdscr.addstr(idx + 1, mid + 4, f"{option}: {value}", curses.A_REVERSE)
                    else:
                        self.stdscr.addstr(idx + 1, mid + 4, f"{option}: {value}")

            # Display the menu at the bottom
            self.display_menu()

            self.stdscr.refresh()

            key = self.stdscr.getkey()
            if key == 'KEY_UP':
                if self.focus_right:
                    if self.current_option_index > 0:
                        self.current_option_index -= 1
                else:
                    if self.current_section_index > 0:
                        self.current_section_index -= 1
            elif key == 'KEY_DOWN':
                if self.focus_right:
                    if self.current_option_index < len(options) - 1:
                        self.current_option_index += 1
                else:
                    if self.current_section_index < len(sections) - 1:
                        self.current_section_index += 1
            elif key == 'q':
                break
            elif key == 'c':
                self.parameters.validate()
            elif key == 'g':
                filename = self.parameters.physics.problem
                self.parameters.write_ini(f'{filename}.ini')
                self.stdscr.clear()
                self.stdscr.addstr(len(sections) + 4 + len(options), 2, f"Configuration saved to {filename}.ini")
                self.stdscr.refresh()
            elif key in ['KEY_LEFT', 'KEY_RIGHT']:
                if self.focus_right:
                    option = options[self.current_option_index]
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
            elif key in ['\t', '\n']:  # Tab or Enter key
                # Edit the selected option
                if key=='\n' and self.focus_right:
                    self.stdscr.addstr(self.current_option_index + 1, mid + 4, "Enter new value:", curses.A_UNDERLINE)
                    curses.echo()
                    new_value = self.stdscr.getstr(self.current_option_index + 1, mid + 20).decode('utf-8')
                    curses.noecho()
                    # Convert new_value to the appropriate type
                    current_value = getattr(current_section, options[self.current_option_index])
                    field_type = type(current_value)
                    try:
                        new_value = validators.from_string(new_value=new_value, prev_value=current_value, type_=field_type)
                    except ValueError as e:
                        self.stdscr.addstr(self.current_option_index + 1, mid + 4, f"Invalid value for {options[self.current_option_index]}, {e}.", curses.color_pair(1))
                        self.stdscr.refresh()
                        self.stdscr.getkey()
                        self.stdscr.addstr(self.current_option_index + 1, mid + 4, " " * (width - mid - 4))
                        new_value = getattr(current_section, options[self.current_option_index])
                    setattr(current_section, options[self.current_option_index], new_value)
                else:
                    self.focus_right = True
                    self.reset_cursor()
            elif key in ['KEY_BTAB', '\x1b']:  # Shift + Tab or Escape key
                self.focus_right = False
                self.reset_cursor()

def main(stdscr):
    editor = SimIniEditor(stdscr)
    editor.run()

curses.wrapper(main)
