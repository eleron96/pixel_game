import pygame

class Menu:
    def __init__(self, screen, items, screen_width, screen_height):  # Добавляем аргументы screen_width и screen_height
        self.screen = screen
        self.items = items
        self.selected = 0
        self.font_size = 36
        self.font_path = None
        self.font = pygame.font.Font(self.font_path, self.font_size)
        self.running = True
        self.screen_width = screen_width  # Сохраняем размеры окна
        self.screen_height = screen_height

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected = (self.selected - 1) % len(self.items)
                    elif event.key == pygame.K_DOWN:
                        self.selected = (self.selected + 1) % len(self.items)
                    elif event.key == pygame.K_RETURN:
                        return self.selected

            self.screen.fill((0, 0, 0))
            self.draw_menu()
            pygame.display.flip()

    def draw_menu(self):
        for index, item in enumerate(self.items):
            if index == self.selected:
                label = self.font.render(f"> {item}", True, (255, 255, 255))
            else:
                label = self.font.render(item, True, (255, 255, 255))
            x = (self.screen_width - label.get_width()) // 2  # Выравниваем метку по центру по горизонтали
            y = (self.screen_height - len(self.items) * 30) // 2 + index * 30  # Выравниваем по центру по вертикали
            self.screen.blit(label, (x, y))

