import pygame
import sys
from mutagen.mp3 import MP3

# pygame & mixer
pygame.init()
pygame.mixer.init()

# sound fx
click_sound = pygame.mixer.Sound("fx/click.wav")
bye_sound = pygame.mixer.Sound("fx/BYE.wav")

# colors
DARK_PURPLE = (38, 0, 63)
DARK_GREY = (50, 50, 50)
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)
WHITE = (200, 200, 200)

# display
width, height = 600, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('MERT\'s PLAYER')

# buttons
button_font = pygame.font.SysFont('helveticaneue', 30)
message_font = pygame.font.SysFont('helveticaneue', 20)
button_width = width // 4
button_height = 80

buttons = {
    "Toggle": pygame.Rect(button_width * 0, 0, button_width, button_height),
    "RESTART": pygame.Rect(button_width * 1, 0, button_width, button_height),
    "VISUALS": pygame.Rect(button_width * 2, 0, button_width, button_height),
    "QUIT": pygame.Rect(button_width * 3, 0, button_width, button_height)
}


# ss --> mm:ss format
def get_song_duration(path):
    audio = MP3(path)
    duration = int(audio.info.length)
    minutes = duration // 60
    seconds = duration % 60
    return f"{minutes:02}:{seconds:02}", duration


# path to song + image + duration
song_metadata = {
    "mdma": (*get_song_duration("songs/song1.mp3"), "pics/song1.jpg"),
    "journey": (*get_song_duration("songs/song2.mp3"), "pics/song2.jpg"),
    "boards": (*get_song_duration("songs/song3.mp3"), "pics/song3.jpg"),
    "zeki": (*get_song_duration("songs/song4.mp3"), "pics/song4.jpg"),
    "whitenoise": (*get_song_duration("songs/whitenoise.mp3"), None)
}

# song buttons
song_buttons = {
    "mdma": ("mdma", pygame.Rect(button_width * 0, button_height, button_width, button_height), "songs/song1.mp3"),

    "journey": (
            "journey", pygame.Rect(button_width * 1, button_height, button_width, button_height), "songs/song2.mp3"),

    "boards": (
                "boards", pygame.Rect(button_width * 2, button_height, button_width, button_height), "songs/song3.mp3"),

    "zeki": ("zeki", pygame.Rect(button_width * 3, button_height, button_width, button_height), "songs/song4.mp3")
}

# flags
show_visuals = False
paused_time = 0
playing = False
first_play = True
current_error_song = None
current_time = 0
timer_start_ticks = 0
display_remaining = False

# invisible button of timer
timer_button = pygame.Rect(0, height - button_height, width, button_height)

# arrows
arrow_color = WHITE
arrow_size = 40
arrow_left = [(30, height // 2), (30 + arrow_size, height // 2 - arrow_size // 2),
              (30 + arrow_size, height // 2 + arrow_size // 2)]
arrow_right = [(width - 30, height // 2), (width - 30 - arrow_size, height // 2 - arrow_size // 2),
               (width - 30 - arrow_size, height // 2 + arrow_size // 2)]

# invisible buttons of arrows
left_arrow_button = pygame.Rect(30, height // 2 - arrow_size // 2, arrow_size, arrow_size)
right_arrow_button = pygame.Rect(width - 30 - arrow_size, height // 2 - arrow_size // 2, arrow_size, arrow_size)


def draw_buttons():
    screen.fill(BLACK)
    for text, rect in buttons.items():
        pygame.draw.rect(screen, BLACK, rect)
        if text == "Toggle":
            if playing:
                color = DARK_GREY
            else:
                color = DARK_GREY
            text_color = BLACK
        elif text == "RESTART" or text == "VISUALS" or text == "QUIT":
            color = DARK_GREY
            text_color = WHITE
        else:
            color = DARK_PURPLE
            text_color = BLACK
        pygame.draw.rect(screen, color, rect)
        if text == "Toggle" or text == "RESTART":
            line_thickness = 4
        else:
            line_thickness = 2
        if text != "QUIT":
            pygame.draw.line(screen, BLACK, (rect.right - 1, rect.top), (rect.right - 1, rect.bottom),
                             line_thickness)
        if text == "RESTART":
            pygame.draw.line(screen, BLACK, (rect.left, rect.top), (rect.left, rect.bottom),
                             2)
    pygame.draw.line(screen, BLACK, (buttons["QUIT"].left, buttons["VISUALS"].top),
                     (buttons["QUIT"].left, buttons["QUIT"].bottom), 1)
    for text, rect in buttons.items():
        msg = button_font.render(text, True, text_color)
        screen.blit(msg, (rect.x + 10, rect.y + 10))
    if show_visuals:
        visuals_rect = pygame.Rect(0, button_height, width, height - button_height)
        pygame.draw.rect(screen, BLACK, visuals_rect)
    if playing:
        text = "| | PAUSE"
    else:
        text = " > PLAY"
    pygame.draw.rect(screen, (30, 30, 30), buttons["Toggle"])
    msg = button_font.render(text, True, WHITE)
    screen.blit(msg, (buttons["Toggle"].x + 10, buttons["Toggle"].y + 10))


def draw_song_buttons():
    for name, (text, rect, _) in song_buttons.items():
        pygame.draw.rect(screen, BLACK, rect)
        msg = button_font.render(text, True, WHITE)
        screen.blit(msg, (rect.x + 10, rect.y + 10))
        if name == current_song:  # display artwork for the currently playing song
            # display corresponding JPEG image
            image_path = song_metadata[name][2]
            image = pygame.image.load(image_path)
            # resize the artwork to 100x100
            image = pygame.transform.scale(image, (300, 300))
            image_rect = image.get_rect()
            # position the image lower
            image_rect.centerx = width // 2
            image_rect.top = rect.bottom + 30
            screen.blit(image, image_rect)


def draw_arrows():
    pygame.draw.polygon(screen, arrow_color, arrow_left)
    pygame.draw.polygon(screen, arrow_color, arrow_right)


def display_message(message):
    message_text = message_font.render(message, True, WHITE)
    message_rect = message_text.get_rect(center=(width // 2, height - button_height // 2))
    screen.blit(message_text, message_rect)
    pygame.display.flip()


def display_bye_message():
    bye_font = pygame.font.SysFont('helveticaneue', 100)
    bye_text = bye_font.render("BYE", True, WHITE)
    bye_text_rect = bye_text.get_rect(center=(width // 2, height // 2))
    screen.fill(BLACK)
    screen.blit(bye_text, bye_text_rect)
    pygame.display.flip()

    pygame.time.wait(1100)


def adjust_song_time(delta):
    global current_time, paused_time, timer_start_ticks, current_song
    if current_song is not None:
        current_time += delta
        if current_time < 0:
            current_time = 0
        elif current_time > song_metadata[current_song][1]:
            current_time = song_metadata[current_song][1]
        if not playing:
            paused_time = current_time
        pygame.mixer.music.play(start=current_time)
        timer_start_ticks = pygame.time.get_ticks() - current_time * 1000


def toggle_visuals():
    global show_visuals
    show_visuals = not show_visuals


def play_song(song_path, clicked_song):
    global current_error_song, paused_time, current_time, timer_start_ticks, playing, first_play
    try:
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play()
        playing = True
        first_play = False
        paused_time = 0
        current_time = 0
        timer_start_ticks = pygame.time.get_ticks()
        click_sound.play()
    except pygame.error:
        if current_error_song == clicked_song:
            pygame.time.wait(800)
        else:
            current_error_song = clicked_song
            display_message(f'{clicked_song} cannot be played')
            pygame.time.wait(800)


def format_time(seconds):
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02}:{seconds:02}"


def draw_timer():
    global current_time
    try:
        if playing:
            elapsed_ticks = pygame.time.get_ticks() - timer_start_ticks
            current_time = paused_time + elapsed_ticks // 1000
        if display_remaining:
            remaining_time = song_metadata[current_song][1] - current_time
            timer_text = f'-{format_time(remaining_time)}'
        else:
            timer_text = f'{format_time(current_time)}'

        timer_surface = button_font.render(timer_text, True, WHITE)
        timer_rect = timer_surface.get_rect(center=(width // 2, height - button_height // 2))
        pygame.draw.rect(screen, BLACK, timer_rect.inflate(20, 20))
        screen.blit(timer_surface, timer_rect)

        # rectangle over the timer if a song button is not clicked
        if current_song is None:
            timer_rect = pygame.Rect(0, height - button_height, width, button_height)
            pygame.draw.rect(screen, BLACK, timer_rect)
    except KeyError:
        pass


def main():
    global show_visuals, playing, paused_time, first_play, current_song, display_remaining, timer_start_ticks
    running = True
    pygame.mixer.music.load("songs/whitenoise.mp3")
    current_song = None

    while running:
        draw_buttons()
        draw_song_buttons()
        draw_arrows()
        draw_timer()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if buttons["Toggle"].collidepoint(event.pos):
                    # pause/play
                    if playing:
                        pygame.mixer.music.pause()
                        paused_time += (pygame.time.get_ticks() - timer_start_ticks) // 1000
                    else:
                        if first_play:
                            pygame.mixer.music.play()
                            first_play = False
                        else:
                            pygame.mixer.music.unpause()
                        timer_start_ticks = pygame.time.get_ticks()
                    playing = not playing
                    click_sound.play()
                elif buttons["RESTART"].collidepoint(event.pos):
                    # restart
                    pygame.mixer.music.rewind()
                    pygame.mixer.music.play()
                    playing = True
                    first_play = False
                    paused_time = 0
                    current_time = 0
                    timer_start_ticks = pygame.time.get_ticks()
                    click_sound.play()
                elif buttons["QUIT"].collidepoint(event.pos):
                    # quit
                    pygame.mixer.music.stop()
                    bye_sound.play()
                    display_bye_message()
                    running = False
                elif buttons["VISUALS"].collidepoint(event.pos):
                    # visuals button (EMPTY)
                    toggle_visuals()
                    click_sound.play()
                elif timer_button.collidepoint(event.pos):
                    # timer
                    if current_song != "whitenoise":  # Check if the current song is not "whitenoise"
                        display_remaining = not display_remaining
                        click_sound.play()  # Play clicking sound when the timer button is clicked
                elif left_arrow_button.collidepoint(event.pos):
                    # left arrow
                    try:
                        adjust_song_time(-10)
                        if not playing:
                            pygame.mixer.music.pause()
                    except pygame.error:
                        pass
                elif right_arrow_button.collidepoint(event.pos):
                    # right arrow
                    try:
                        adjust_song_time(10)
                        if not playing:
                            pygame.mixer.music.pause()
                    except pygame.error:
                        pass

                else:
                    for name, (_, rect, song_path) in song_buttons.items():
                        if rect.collidepoint(event.pos):
                            current_song = name
                            play_song(song_path, name)
                            # rectangle disappears when a song button is clicked
                            current_time = 0

        pygame.display.flip()
        pygame.time.Clock().tick(30)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
