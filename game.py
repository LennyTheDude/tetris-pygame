from settings import *
from timer import Timer

class Game:
    def __init__(self):
        self.surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        self.display_surface = pygame.display.get_surface()
        self.rect = self.surface.get_rect(topleft = (PADDING, PADDING))
        self.sprites = pygame.sprite.Group()

        self.grid_surface = self.surface.copy()
        self.grid_surface.fill((0, 255, 0))
        self.grid_surface.set_colorkey((0, 255, 0))
        self.grid_surface.set_alpha (120)
        
        self.tetromino = Tetromino(RANDOMIZE_SHAPE(), self.sprites)

        self.timers = {
            'vertical move': Timer(UPDATE_START_SPEED, True, self.move_down),
            'horizontal move': Timer(MOVE_WAIT_TIME)
        }
        self.timers['vertical move'].activate()

    def timer_update(self):
        for timer in self.timers.values():
            timer.update()

    def move_down(self):
        self.tetromino.move_down()
        

    def draw_grid(self):
        for col in range(1, COLUMNS):
            x = col * CELL_SIZE
            pygame.draw.line(self.grid_surface, LINE_COLOR, (x, 0), (x, self.grid_surface.get_height()))
            
        for row in range(1, ROWS):
            y = row * CELL_SIZE
            pygame.draw.line(self.grid_surface, LINE_COLOR, (0, y), (self.grid_surface.get_width(), y))

        self.surface.blit(self.grid_surface, (0,0))
    
    
    def run(self):
        self.input()
        self.timer_update()
        self.sprites.update()
        self.surface.fill('black')
        self.sprites.draw(self.surface)
        self.draw_grid()
        self.display_surface.blit(self.surface, (PADDING, PADDING))
        pygame.draw.rect(self.display_surface, LINE_COLOR, self.rect, 2, 2)

    def input(self):
        keys = pygame.key.get_pressed()
        
        if not self.timers['horizontal move'].active:
            if keys[pygame.K_LEFT]:
                self.tetromino.move_horizontal(-1)
                self.timers['horizontal move'].activate()
            elif keys[pygame.K_RIGHT]:
                self.tetromino.move_horizontal(1)
                self.timers['horizontal move'].activate()

class Tetromino:
    def __init__(self, shape, group):
        self.block_positions = TETROMINOS[shape]['shape']
        self.color = TETROMINOS[shape]['color']

        self.blocks = [Block(group, pos, self.color) for pos in self.block_positions]

    def next_move_horizontal_collide(self, amount):
        collision_list = [block.horizontal_collide(int(block.pos.x + amount)) for block in self.blocks]
        return True if any(collision_list) else False

    def next_move_down_collide(self, amount):
        collision_list = [block.vertical_collide(int(block.pos.y + amount)) for block in self.blocks]
        return True if any(collision_list) else False

    def move_down(self):
        if not self.next_move_down_collide(1):
            for block in self.blocks:
                block.pos.y += 1
    
    def move_horizontal(self, amount):
        if not self.next_move_horizontal_collide(amount):
            for block in self.blocks:
                block.pos.x += amount

class Block(pygame.sprite.Sprite):
    def __init__(self, group, pos, color):
        super().__init__(group)
        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.image.fill(color)
        self.pos = pygame.Vector2(pos) + BLOCK_OFFSET
        self.rect = self.image.get_rect(topleft = self.pos * CELL_SIZE)

    def horizontal_collide(self, x):
        if not 0 <= x < COLUMNS:
            return True

    def vertical_collide(self, y):
        if not 0 <= y < ROWS:
            return True
    
    def update(self):
        self.rect.topleft = self.pos * CELL_SIZE