import pygame

from gfs.surface import Surface, flip, events
from gfs.music import Music

from game import Game


def main():
    surface = Surface(1280, 720, "Game jam!")
    clock = pygame.time.Clock()

    game = Game(surface.width, surface.height)

    is_running = True
    timer = 0

    while is_running:
        for event in events():
            if event.type == pygame.QUIT:
                is_running = False
            elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                game.keyboard_input(event)
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                game.mouse_input(event)
            elif event.type == pygame.MOUSEMOTION:
                game.mouse_motion(event)

        game.update()

        surface.clear((0, 0, 0))

        game.render(surface)

        flip()

        clock.tick(60)
        timer = (timer + 1) % 60

    pygame.quit()


if __name__ == "__main__":
    main()
