import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
pygame.init()
try:
    os.environ["DISPLAY"]
except:
    os.environ["SDL_VIDEODRIVER"] = "dummy"

class block:
    def __init__(self):
        self.size = 50
        self.velocity = 50
        self.color = (0,0,255)
        self.x = 0
        self.y = 0

if __name__ == '__main__':
    board = pygame.display.set_mode((500,500))
    pygame.display.set_caption("Stack Blocks Game")


    # Main loop of the game --> if you already beat it once, don't show start screen on restart
    start_screen = True
    while (True):
        run_game = True
        pressed = False
        blocks = [block()]
        score = 0
        downward_vel = 50
        lose = False
        win = False
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render("Stack 'Em! Click Space to Begin", True, (0,0,255))
        textRect = text.get_rect()
        textRect.center = (500 // 2, 500 // 2) 

        # While player has not started the game
        while start_screen:
            board.fill((0,0,0))
            pygame.time.delay(100)
            board.blit(text,textRect)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                start_screen = False
        pygame.time.delay(100)

        # While the game is in the meat and potatoes (user actually playing it)
        while run_game:
            board.fill((0,0,0))
            current_block = blocks[-1]
            pygame.time.delay(50)

            # Allows user to click X button to quit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            # For every block that's been placed, draw it.
            for blk in blocks:
                pygame.draw.rect(board, blk.color, (blk.x, blk.y, blk.size, blk.size))
                pygame.display.update()
            
            x = pygame.key.get_pressed()

            if not pressed: # Before the player pressed the space button
                if not x[pygame.K_SPACE]:
                    current_block.x += current_block.velocity
                else:
                    pressed = True # Signifies that the player pressed the button (placed a block)

                # Makes the block being placed change direction repeatedly until it's placed   
                if current_block.x == 450 or current_block.x == 0:
                  current_block.velocity = -1*current_block.velocity
                  
            else: # When the player presses the button
                # While the current falling block is above the previously placed blocks (has a chance to land)
                if current_block.y < 500 - (len(blocks))*current_block.size:
                    current_block.y += downward_vel # falls
                else:
                    # If missed
                    if len(blocks) > 1 and current_block.x != blocks[-2].x:
                        run_game = False # Exits game loop
                        lose = True # Indicates loss
                    # If you stacked it properly, and it was the last block
                    elif len(blocks) == 10:
                        run_game = False # Exits game loop
                        win = True # Indicates win
                        score += 100
                    # If you stacked it properly but there are more blocks to stack
                    else:
                        score += 100
                    blocks.append(block()) # Add to list of complete blocks
                    pressed = False

        # Prepare text for Game Over Screen        
        font = pygame.font.Font('freesansbold.ttf', 32)
        textRect = text.get_rect()
        textRect.center = (500 // 2, 500 // 2) # Text in xact middle
        textRect2 = text.get_rect()
        textRect2.center = (625 // 2, 300) # Eyeballed it honestly, but it looks good (to my eyeballs)
        text2 = font.render("Press Space to Restart", True, (0,0,255))
        if win:
            text = font.render("W claimed. Final Score : " + str(score), True, (0,0,255))
        if lose:
            text = font.render("   You LOST. Final Score: " + str(score), True, (0,0,255))

        # While the Game is Over, show the Game Over Screen
        end_screen = True
        while end_screen:
            board.fill((0,0,0))
            board.blit(text, textRect)
            board.blit(text2, textRect2)
            
            pygame.display.update()

            #Quit Game if user quits
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:
                    pygame.quit()

            # Allows player to reset the game with space bar
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                end_screen = False # resets game
                
    pygame.quit()
