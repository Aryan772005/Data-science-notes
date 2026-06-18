import pygame
import random


pygame.init()

WIDTH, HEIGHT = 600, 700
FPS = 60


BG_COLOR = (20, 20, 35)        
PLAYER_COLOR = (0, 255, 200)  
ENEMY_COLOR = (255, 50, 100)   
TEXT_COLOR = (255, 255, 255)   
UI_BG = (40, 40, 60)           


font_title = pygame.font.SysFont("Trebuchet MS", 45, bold=True)
font_medium = pygame.font.SysFont("Trebuchet MS", 30, bold=True)
font_small = pygame.font.SysFont("Trebuchet MS", 20)


stars = [[random.randint(0, WIDTH), random.randint(0, HEIGHT), random.uniform(1, 3), random.randint(1, 3)] for _ in range(75)]

def draw_text_centered(text, font, color, y, screen):
    """Helper function to draw perfectly centered text."""
    render = font.render(text, True, color)
    rect = render.get_rect(center=(WIDTH // 2, y))
    screen.blit(render, rect)

def main():
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Aryan's Block Dodge Game")
    clock = pygame.time.Clock()

    
    state = "MENU"
    
    
    player_size = 45
    player_rect = pygame.Rect(WIDTH // 2 - player_size // 2, HEIGHT - 100, player_size, player_size)
    player_speed = 8

   
    enemies = []
    enemy_size = 45
    enemy_speed = 5
    spawn_timer = 0
    spawn_delay = 40 

    
    score = 0
    high_score = 0

    running = True
    
   
    try:
        while running:
            
            screen.fill(BG_COLOR)

           
            for star in stars:
                star[1] += star[2] 
                if star[1] > HEIGHT:
                    star[1] = 0 
                    star[0] = random.randint(0, WIDTH)
                
                pygame.draw.circle(screen, (150, 150, 170), (int(star[0]), int(star[1])), star[3])

            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                
                if event.type == pygame.KEYDOWN:
                    if state == "MENU" and event.key == pygame.K_SPACE:
                        state = "PLAYING"
                    elif state == "GAMEOVER":
                        if event.key == pygame.K_r: 
                            state = "PLAYING"
                            score = 0
                            enemies.clear()
                            enemy_speed = 5
                            spawn_delay = 40
                            player_rect.x = WIDTH // 2 - player_size // 2
                        elif event.key == pygame.K_ESCAPE: 
                            running = False

            
            if state == "MENU":
                
                draw_text_centered("ARYAN'S", font_title, PLAYER_COLOR, HEIGHT // 2 - 60, screen)
                draw_text_centered("BLOCK DODGE", font_title, TEXT_COLOR, HEIGHT // 2 - 10, screen)
                draw_text_centered("Press SPACE to Start", font_medium, (200, 200, 200), HEIGHT // 2 + 80, screen)

            elif state == "PLAYING":
                
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT] and player_rect.left > 0:
                    player_rect.x -= player_speed
                if keys[pygame.K_RIGHT] and player_rect.right < WIDTH:
                    player_rect.x += player_speed

            
                spawn_timer += 1
                if spawn_timer >= spawn_delay:
                    x_pos = random.randint(0, WIDTH - enemy_size)
                    enemies.append(pygame.Rect(x_pos, -enemy_size, enemy_size, enemy_size))
                    spawn_timer = 0

                
                for enemy in enemies[:]:
                    enemy.y += enemy_speed
                    
                    
                    if enemy.top > HEIGHT:
                        enemies.remove(enemy)
                        score += 1
                        
                    
                        if score % 5 == 0:
                            enemy_speed += 0.5
                            spawn_delay = max(10, int(spawn_delay * 0.9))
                    
                
                    if player_rect.colliderect(enemy):
                        state = "GAMEOVER"
                        if score > high_score:
                            high_score = score

                
                pygame.draw.rect(screen, PLAYER_COLOR, player_rect, border_radius=10)
                pygame.draw.rect(screen, TEXT_COLOR, player_rect, width=2, border_radius=10)
                
                
                for enemy in enemies:
                    pygame.draw.rect(screen, ENEMY_COLOR, enemy, border_radius=8)
                    pygame.draw.rect(screen, (255, 150, 180), enemy, width=2, border_radius=8)

                
                ui_bar = pygame.Surface((WIDTH, 50))
                ui_bar.set_alpha(180) 
                ui_bar.fill(UI_BG)
                screen.blit(ui_bar, (0, 0))

                score_surf = font_medium.render(f"SCORE: {score}", True, TEXT_COLOR)
                screen.blit(score_surf, (20, 10))

            elif state == "GAMEOVER":

                draw_text_centered("CRASHED!", font_title, ENEMY_COLOR, HEIGHT // 2 - 80, screen)
                draw_text_centered(f"Score: {score}", font_medium, TEXT_COLOR, HEIGHT // 2 - 10, screen)
                draw_text_centered(f"High Score: {high_score}", font_medium, PLAYER_COLOR, HEIGHT // 2 + 30, screen)
                
                draw_text_centered("Press 'R' to Restart", font_small, (200, 200, 200), HEIGHT // 2 + 100, screen)
                draw_text_centered("Press 'ESC' to Quit", font_small, (150, 150, 150), HEIGHT // 2 + 130, screen)

            # 5. Refresh Screen
            pygame.display.flip()
            clock.tick(FPS)

    finally:

        pygame.quit()

if __name__ == "__main__":
    main()
