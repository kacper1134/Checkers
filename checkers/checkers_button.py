from checkers.checkers_constants import *


class Button:
    def __init__(self, row, column, text, selected=False, confirm_button=False):
        self.color = BUTTON_COLOR
        self.text_color = BUTTON_TEXT_COLOR
        self.row = row
        self.column = column
        self.text = text
        self.pos = self.__get_position()
        self.selected = selected
        self.confirm_button = confirm_button
        if selected:
            self.select()

    def __get_position(self):
        return self.row * BUTTONS_WIDTH, self.column * BUTTONS_HEIGHT

    def draw(self, window, font):
        pg.draw.rect(window, BLACK, (self.pos[0], self.pos[1], BUTTONS_WIDTH - BUTTON_PADDING // 2,
                                     BUTTONS_HEIGHT - BUTTON_PADDING + BUTTON_BORDER))
        pg.draw.rect(window, self.color, (self.pos[0] + BUTTON_PADDING // 4, self.pos[1] + BUTTON_PADDING // 4,
                                          BUTTONS_WIDTH - BUTTON_PADDING, BUTTONS_HEIGHT - BUTTON_PADDING))
        text = font.render(self.text, True, self.text_color)
        window.blit(text, (self.pos[0] + BUTTON_PADDING // 2, self.pos[1] + 3 * BUTTON_PADDING // 4))

    def select(self):
        self.color = AVAILABLE_NEXT_MOVE_COLOR
        self.text_color = BUTTON_SELECT_TEXT_COLOR
        self.selected = True

    def unselect(self):
        self.color = BUTTON_COLOR
        self.text_color = BUTTON_TEXT_COLOR
        self.selected = False


class Buttons:
    def __init__(self, window):
        self.buttons = []
        self.window = window

    def add_button(self, button):
        self.buttons.append(button)

    def draw(self, font):
        for button in self.buttons:
            button.draw(self.window, font)

    def get_buttons(self):
        return self.buttons

    def unselect(self, row):
        for button in self.buttons:
            if button.row == row:
                button.unselect()

    def get_selected_buttons(self):
        selected_buttons = []
        for button in self.buttons:
            if button.selected and not button.confirm_button:
                selected_buttons.append(button)
        selected_buttons.sort(key=self.__comparator)
        return selected_buttons

    def __comparator(self, button):
        return button.row