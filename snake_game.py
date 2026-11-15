import curses
import random
import time

def main(stdscr):
    # Clear screen
    stdscr.clear()
    
    # Turn off echo and cursor
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    curses.curs_set(0)
    
    # Get terminal size
    sh, sw = stdscr.getmaxyx()
    
    # Ensure window is large enough
    if sh < 10 or sw < 30:
        curses.endwin()
        print("Terminal size too small!")
        return

    # --- MENU PAGE ---
    stdscr.clear()
    stdscr.addstr(sh // 2 - 4, (sw - 28) // 2, "=== SNAKE GAME MENU ===")
    stdscr.addstr(sh // 2 - 2, (sw - 38) // 2, "Do you want to spend $5 for 2 extra lives?")
    stdscr.addstr(sh // 2, (sw - 20) // 2, "[y] Yes  /  [n] No")
    stdscr.refresh()
    
    extra_lives = 0
    while True:
        choice = stdscr.getch()
        if choice in [ord('y'), ord('Y')]:
            # Show bank transaction text
            stdscr.clear()
            stdscr.addstr(sh // 2 - 2, (sw - 45) // 2, "Connecting to Axis Bank secure gateway...")
            stdscr.refresh()
            time.sleep(1.2)
            
            stdscr.clear()
            stdscr.addstr(sh // 2 - 3, (sw - 42) // 2, "--- AXIS BANK TRANSACTION ALERT ---")
            stdscr.addstr(sh // 2 - 1, (sw - 40) // 2, "A/C Debit: USD 5.00 | Ref: TXN987654321")
            stdscr.addstr(sh // 2 + 1, (sw - 34) // 2, "Status: SUCCESS. 2 Extra Lives added!")
            stdscr.addstr(sh // 2 + 3, (sw - 26) // 2, "Press any key to start...")
            stdscr.refresh()
            stdscr.getch()
            extra_lives = 2
            break
        elif choice in [ord('n'), ord('N')]:
            break

    # Create window
    win = curses.newwin(sh, sw, 0, 0)
    win.keypad(True)
    win.timeout(100)
    
    lives = 3 + extra_lives
    score = 0
    
    def reset_snake_and_food():
        nonlocal snake, food, key
        snake_x = sw // 4
        snake_y = sh // 2
        snake = [
            [snake_y, snake_x],
            [snake_y, snake_x - 1],
            [snake_y, snake_x - 2]
        ]
        food = [sh // 2, sw // 2]
        key = curses.KEY_RIGHT

    snake = []
    food = []
    key = curses.KEY_RIGHT
    reset_snake_and_food()
    
    while True:
        win.clear()
        
        # Draw border
        win.border(0)
        
        # Display lives and score at top right / top left
        score_str = f"Score: {score}"
        lives_str = f"Lives: {lives}"
        try:
            win.addstr(0, 2, score_str)
            win.addstr(0, sw - len(lives_str) - 2, lives_str)
        except Exception:
            pass
            
        # Draw food
        try:
            win.addch(food[0], food[1], curses.ACS_PI)
        except Exception:
            pass
            
        # Draw snake
        for segment in snake:
            try:
                win.addch(segment[0], segment[1], curses.ACS_CKBOARD)
            except Exception:
                pass
                
        win.refresh()
        
        next_key = win.getch()
        
        # Prevent 180-degree immediate reverse crash
        if next_key != -1:
            if (key == curses.KEY_RIGHT and next_key != curses.KEY_LEFT) or                (key == curses.KEY_LEFT and next_key != curses.KEY_RIGHT) or                (key == curses.KEY_UP and next_key != curses.KEY_DOWN) or                (key == curses.KEY_DOWN and next_key != curses.KEY_UP):
                key = next_key
        
        # Calculate new head
        new_head = [snake[0][0], snake[0][1]]
        
        if key == curses.KEY_DOWN:
            new_head[0] += 1
        if key == curses.KEY_UP:
            new_head[0] -= 1
        if key == curses.KEY_LEFT:
            new_head[1] -= 1
        if key == curses.KEY_RIGHT:
            new_head[1] += 1
            
        # Check boundary collisions or self collision
        if (new_head[0] in [0, sh - 1] or 
            new_head[1] in [0, sw - 1] or 
            new_head in snake):
            
            lives -= 1
            if lives > 0:
                # Flash screen or pause briefly
                win.timeout(1000)
                win.getch()
                win.timeout(100)
                reset_snake_and_food()
                continue
            else:
                # Game over page
                stdscr.clear()
                stdscr.addstr(sh // 2 - 2, (sw - 12) // 2, "game over!!!")
                stdscr.addstr(sh // 2, (sw - 45) // 2, "Do you want to purchase one more life for $10?")
                stdscr.addstr(sh // 2 + 2, (sw - 20) // 2, "[y] Yes  /  [n] No")
                stdscr.refresh()
                
                stdscr.timeout(-1) # wait indefinitely for choice
                choice = stdscr.getch()
                if choice in [ord('y'), ord('Y')]:
                    stdscr.clear()
                    stdscr.addstr(sh // 2 - 2, (sw - 45) // 2, "Connecting to Axis Bank secure gateway...")
                    stdscr.refresh()
                    time.sleep(1.2)
                    
                    stdscr.clear()
                    stdscr.addstr(sh // 2 - 3, (sw - 42) // 2, "--- AXIS BANK TRANSACTION ALERT ---")
                    stdscr.addstr(sh // 2 - 1, (sw - 40) // 2, "A/C Debit: USD 10.00 | Ref: TXN123456789")
                    stdscr.addstr(sh // 2 + 1, (sw - 35) // 2, "Status: SUCCESS. 1 Extra Life added!")
                    stdscr.refresh()
                    time.sleep(3)
                    
                    stdscr.clear()
                    stdscr.addstr(sh // 2, (sw - 10) // 2, "Thank you!")
                    stdscr.refresh()
                    time.sleep(2)
                    
                    lives = 1
                    reset_snake_and_food()
                    win.timeout(100)
                    continue
                else:
                    break
            
        snake.insert(0, new_head)
        
        # Check if snake ate the food
        if snake[0] == food:
            score += 1
            food = None
            while food is None:
                new_food = [
                    random.randint(1, sh - 2),
                    random.randint(1, sw - 2)
                ]
                food = new_food if new_food not in snake else None
        else:
            snake.pop()
            
    curses.endwin()
    print(f"Game Over! Your score: {score}")

if __name__ == "__main__":
    curses.wrapper(main)
