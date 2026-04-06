import pygame
import random

#Configuration
WIDTH, HEIGHT = 400, 2000 
GRAVITY = 0.40
FLAP_STRENGTH = -8
PIPE_SPEED = 5
GAP_SIZE = 220

# Colors
BG_COLOR = (245, 245, 220)
PACKET_COLOR = (0, 255, 255)
WALL_COLOR = (200, 0, 255)

class Packet:
    def __init__(self):
        self.x = 80
        self.y = HEIGHT // 2
        self.velocity = 0
        self.rect = pygame.Rect(self.x, self.y, 40, 30)

    def flap(self):
        self.velocity = FLAP_STRENGTH

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        self.rect.y = self.y

    def draw(self, screen):
        pygame.draw.rect(screen, PACKET_COLOR, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), (self.rect.x + 25, self.rect.y + 5, 8, 8))

class Firewall:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(150, 450)
        self.top_rect = pygame.Rect(self.x, 0, 60, self.height)
        self.bottom_rect = pygame.Rect(self.x, self.height + GAP_SIZE, 60, HEIGHT)
        self.passed = False

    def update(self):
        self.x -= PIPE_SPEED
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x

    def draw(self, screen):
        pygame.draw.rect(screen, WALL_COLOR, self.top_rect)
        pygame.draw.rect(screen, WALL_COLOR, self.bottom_rect)

def main():
    pygame.init()
    info = pygame.display.Info()
    screen_width, screen_height = info.current_w, info.current_h
    screen = pygame.display.set_mode((screen_width, screen_height))
    
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 40, bold=True)

    packet = Packet()
    walls = [Firewall(screen_width + 100)]
    score = 0
    running = True
    game_over = False

    while running:
        screen.fill(BG_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_over:
                    packet = Packet()
                    walls = [Firewall(screen_width + 100)]
                    score = 0
                    game_over = False
                else:
                    packet.flap()

        if not game_over:
            packet.update()
            
            if walls[-1].x < screen_width - 250:
                walls.append(Firewall(screen_width))

            for wall in walls[:]:
                wall.update()
                if wall.x + 60 < 0:
                    walls.remove(wall)
                
                if packet.rect.colliderect(wall.top_rect) or packet.rect.colliderect(wall.bottom_rect):
                    game_over = True
                
                if not wall.passed and wall.x < packet.x:
                    wall.passed = True
                    score += 1

            if packet.y <= 0 or packet.y >= screen_height:
                game_over = True

        # Drawing
        for wall in walls:
            wall.draw(screen)
        packet.draw(screen)
    
            
        score_text = font.render(f"Score: {score}", True, (0, 0, 255))
        screen.blit(score_text, (20, 40))

        if game_over:
            msg = font.render("YOU DUM DUM, TRY AGAIN", True, (255, 0, 0))
            tap = font.render("TAP TO REBOOT, AND GIT GUD", True, (255, 0, 0))
            screen.blit(msg, (screen_width//2 - 150, screen_height//2 - 50))
            screen.blit(tap, (screen_width//2 - 140, screen_height//2 + 20))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
