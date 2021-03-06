'''This layout is inspired by CS50 AI project 0 - https://cs50.harvard.edu/ai/2020/projects/0/tictactoe/ '''

import sys
import time
import pygame
import cs50.connect4.connect as con

pygame.init()
size = width, height = 900, 600

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)

screen = pygame.display.set_mode(size)

# Set fonts
mediumFont = pygame.font.Font("OpenSans-Regular.ttf", 28)
largeFont = pygame.font.Font("OpenSans-Regular.ttf", 40)

# Initialise empty board and no user
user = None
board = con.initial_state()
ai_turn = False


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(white)

    
    #The start screen
    if user is None:

        # Draw title
        title = largeFont.render("Connect4", True, black)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)

        # Draw buttons
        playAsRedButton = pygame.Rect((width / 8), (height / 2), width / 4, 50)
        playRed = mediumFont.render("Play as Red", True, red)
        playRedRect = playRed.get_rect()
        playRedRect.center = playAsRedButton.center
        pygame.draw.rect(screen, white, playAsRedButton)
        screen.blit(playRed, playRedRect)

        playAsBlueButton = pygame.Rect(5 * (width / 8), (height / 2), width / 4, 50)
        playBlue = mediumFont.render("Play as Blue", True, blue)
        playBlueRect = playBlue.get_rect()
        playBlueRect.center = playAsBlueButton.center
        pygame.draw.rect(screen, white, playAsBlueButton)
        screen.blit(playBlue, playBlueRect)

        # Check if button is clicked and set user
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if playAsRedButton.collidepoint(mouse):
                time.sleep(0.2)
                user = con.Red
            elif playAsBlueButton.collidepoint(mouse):
                time.sleep(0.2)
                user = con.Blue
    #Once a user (red or blue) is selected enter the game interface
    else:
        slot_size = 80
        slot_origin = (width / 2 - (3.5 * slot_size),
                       height / 2 - (3 * slot_size))
        slots = []
        #Draw the 6x7 connect4 grid and fill with the appropriate colour
        for i in range(6):
            row = []
            for j in range(7):
                rect = pygame.Rect(
                    slot_origin[0] + j * slot_size,
                    slot_origin[1] + i * slot_size,
                    slot_size, slot_size
                )
                pygame.draw.rect(screen, black, rect, 3)

                if board[i][j] == "Red":
                    screen.fill(red, rect)
                elif board[i][j] == "Blue":
                    screen.fill(blue, rect)
                row.append(rect)
            slots.append(row)

        #Check if the game is over and get which player's turn it is
        game_over = con.terminal(board)
        player = con.player(board)

        
        #Print to the screen whether the game has ended or current players turn
        if game_over:
            winner = con.winner(board)
            if winner is None:
                title = f"Game Over: Tie."
            else:
                title = f"Game Over: {winner} wins."
        elif user == player:
            title = f"{user}'s Turn"
        else:
            title = f"Computer thinking..."
        title = largeFont.render(title, True, black)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 30)
        screen.blit(title, titleRect)

        # Check if it's the AI's move and call the minimax algo from connect.py
        if user != player and not game_over:
            if ai_turn:
                time.sleep(0.5)
                move = con.AIalgo(board)
                board = con.result(board, move)
                ai_turn = False
            else:
                ai_turn = True

        # Check for a user move and update the board accordingly
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1 and user == player and not game_over:
            mouse = pygame.mouse.get_pos()
            for i in range(6):
                for j in range(7):
                    if (board[i][j] == None and slots[i][j].collidepoint(mouse)):
                        board = con.result(board, j)
                       
        # If the game is over display a play again button and reset the game
        if game_over:
            againButton = pygame.Rect(width / 3, height - 55, width / 3, 50)
            again = mediumFont.render("Play Again", True, white)
            againRect = again.get_rect()
            againRect.center = againButton.center
            pygame.draw.rect(screen, black, againButton)
            screen.blit(again, againRect)
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if againButton.collidepoint(mouse):
                    time.sleep(0.2)
                    user = None
                    board = con.initial_state()
                    ai_turn = False

    pygame.display.flip()
