import pygame
import random
import os


# funkcija vertikala gradienta taisnstura uzzimesanai uz virsmas
def draw_vertical_gradient_rect(surface, start, end, rect):
    # izveido vertikalu gradientu
    gradient = pygame.Surface((1, rect.height), pygame.SRCALPHA)

    for y in range(rect.height):
        alpha = int((y / rect.height) * 255)
        current_color = (end[0] - start[0], end[1] - start[1], end[2] - start[2], alpha)
        gradient.set_at((0, y), current_color)

    # merogo gradientu, lai aizpilditu visu taisnsturi
    gradient = pygame.transform.scale(gradient, (rect.width, rect.height))
    surface.blit(gradient, rect.topleft)


# nepieciesams statisks mainigais
text_colors = {}


# funkcija lai uzzimetu pogu ar tekstu uz virsmas
def draw_button(surface, font, text, rect, mouse, click, value=0, extra1=""):
    # saglaba ieprieksejas iteracijas teksta krasu
    global text_colors

    # saglaba teksta krasu ja ta ieprieks nav bijusi saglabata
    if text not in text_colors:
        text_colors[text] = 200

    text_color = text_colors[text]

    # kursors atrodas uz pogas
    if rect.collidepoint(mouse):
        text_color += 4
        text_color = min(text_color, 230)
    else:
        text_color -= 4
        text_color = max(text_color, 200)

    # inicialize krasas
    color = text_color - 150

    # uzzime pogu un tas konturu
    pygame.draw.rect(surface, (125, 125, 125), (rect[0] - 2, rect[1] - 2, rect[2] + 4, rect[3] + 4))
    pygame.draw.rect(surface, (0, 0, 0), (rect[0] - 1, rect[1] - 1, rect[2] + 2, rect[3] + 2))
    draw_vertical_gradient_rect(surface, (0, 0, 0), (color, color, color), rect)

    # pievieno extra simbolus
    new_text = text

    if value:
        new_text += str(value) + extra1

    # uzzime pogas tekstu
    text_surface = font.render(new_text, True, (text_color, text_color, text_color))
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)

    # saglaba jauno krasu nakamajai iteracijai
    text_colors[text] = text_color


def draw_text(surface, font, text, rect, color=(200, 200, 200)):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)


# funckija kritosu dalinu zimesanai
def draw_falling_particles(surface, particles):
    for particle in particles:
        pygame.draw.circle(surface, (100, 100, 100), particle, 2)

    for i in range(len(particles)):
        x, y = particles[i]
        # horizontala un vertikala kutiba
        y += 1
        x += random.randint(-1, 1)
        particles[i] = (x, y)

        # ja dalina nokrit zem loga tad reseto tas poziciju
        if y > 480:
            particles[i] = (random.randint(0, 854), 0)


def draw_outline(surface, rect, color, thickness=1):
    pygame.draw.line(surface, color, (rect.left, rect.top), (rect.left + rect.width, rect.top),
                     thickness)  # augseja linija
    pygame.draw.line(surface, color, (rect.left, rect.top + rect.height),
                     (rect.left + rect.width, rect.top + rect.height), thickness)  # apakseja linija
    pygame.draw.line(surface, color, (rect.left, rect.top), (rect.left, rect.top + rect.height),
                     thickness)  # kreisa linija
    pygame.draw.line(surface, color, (rect.left + rect.width, rect.top),
                     (rect.left + rect.width, rect.top + rect.height), thickness)  # laba linija


# galvena funkcija
def main():
    # nomaina aktivo direktoriju uz to kur python fails atrodas (doma uztaisit kkadu logo prieks main ekrana)
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # inicialize pygame
    pygame.init()
    clock = pygame.time.Clock()

    # resolucijas un nosaukuma iestatisana
    screen = pygame.display.set_mode((854, 480))
    pygame.display.set_caption("Starpības spēle - 1. praktiskais darbs - Mākslīgā intelekta pamati")

    # inicialize fontu
    verdana = pygame.font.Font(pygame.font.match_font("Verdana"), 16)
    verdana.set_bold(True)

    # saglaba statiskus mainigos
    running, mouse_click = True, False
    in_menu, in_options, in_game = True, False, False

    # inicialize 20 dalinu sakuma pozicijas
    particles = [(random.randint(0, 854), random.randint(0, 480)) for _ in range(75)]

    # saglaba galvenas izveles plaknes izmerus
    options_button_rect = pygame.Rect(367, 225, 120, 30)
    start_button_rect = pygame.Rect(367, 185, 120, 30)
    exit_button_rect = pygame.Rect(367, 265, 120, 30)

    # saglaba opciju izveles plaknes izmerus
    alfabeta_button_rect = pygame.Rect(165, 245, 240, 30)
    minmax_button_rect = pygame.Rect(165, 205, 240, 30)
    random_button_rect = pygame.Rect(165, 165, 240, 30)
    return_button_rect = pygame.Rect(367, 325, 120, 30)
    playerstart_button_rect = pygame.Rect(449, 205, 240, 30)
    pcstart_button_rect = pygame.Rect(449, 245, 240, 30)
    linecount_minus_rect = pygame.Rect(449, 165, 120, 30)
    linecount_plus_rect = pygame.Rect(569, 165, 120, 30)

    # saglaba speles izveles plaknes izmerus
    return_ingame_button_rect = pygame.Rect(367, 430, 120, 30)

    # izveletais algoritms, 0 - gadijumskaitlu, 1 - minimaksa, 2 - alfa-beta
    chosen_algorithm = 0
    player_starts = True

    # speles virknes garums
    line_count = 15

    while running:
        # saglaba peles poziciju
        mouse = pygame.mouse.get_pos()

        # apstrada lietotaja ievadi padarot aplikaciju interaktivu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_click = event.button != 1
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_click = pygame.mouse.get_pressed()[0] == 1

                if mouse_click:
                    if in_menu:
                        if start_button_rect.collidepoint(mouse):
                            in_game = True
                            in_menu = False
                        if exit_button_rect.collidepoint(mouse):
                            pygame.quit()
                            return
                        if options_button_rect.collidepoint(mouse):
                            in_options = True
                            in_menu = False
                    if in_options:
                        if return_button_rect.collidepoint(mouse):
                            in_options = False
                            in_menu = True
                        if linecount_minus_rect.collidepoint(mouse):
                            line_count -= 1
                            line_count = max(line_count, 15)
                        if linecount_plus_rect.collidepoint(mouse):
                            line_count += 1
                            line_count = min(line_count, 25)
                        if random_button_rect.collidepoint(mouse):
                            chosen_algorithm = 0
                        if minmax_button_rect.collidepoint(mouse):
                            chosen_algorithm = 1
                        if alfabeta_button_rect.collidepoint(mouse):
                            chosen_algorithm = 2
                        if playerstart_button_rect.collidepoint(mouse):
                            player_starts = True
                        if pcstart_button_rect.collidepoint(mouse):
                            player_starts = False
                    if in_game:
                        if return_ingame_button_rect.collidepoint(mouse):
                            in_game = False
                            in_menu = True
        # fona krasa
        screen.fill((0, 0, 0))

        # fona efekts
        draw_falling_particles(screen, particles)

        # fona apmales
        draw_outline(screen, pygame.Rect(0, 0, 854, 480), (40, 40, 40), 9)
        draw_outline(screen, pygame.Rect(6, 6, 842, 468), (150, 150, 150))

        # galvena izvele
        if in_menu:
            draw_button(screen, verdana, "Sākt spēli", start_button_rect, mouse, mouse_click)
            draw_button(screen, verdana, "Opcijas", options_button_rect, mouse, mouse_click)
            draw_button(screen, verdana, "Iziet", exit_button_rect, mouse, mouse_click)

        # opciju izvele
        if in_options:
            draw_text(screen, verdana, "Algoritma izvēlne", pygame.Rect(165, 125, 240, 30))
            draw_button(screen, verdana, "Gadījumskaitļu algoritms", random_button_rect, mouse, mouse_click)
            draw_button(screen, verdana, "Minimaksa algoritms", minmax_button_rect, mouse, mouse_click)
            draw_button(screen, verdana, "Alfa-Beta algoritms", alfabeta_button_rect, mouse, mouse_click)
            draw_button(screen, verdana, "Atgriezties", return_button_rect, mouse, mouse_click)

            draw_text(screen, verdana, "Spēles nosacījumi", pygame.Rect(449, 125, 240, 30))
            draw_button(screen, verdana, "-   Virknes garums: ", pygame.Rect(449, 165, 240, 30), mouse, mouse_click,
                        line_count, "   +")
            draw_button(screen, verdana, "Spēli sāk cilvēks", playerstart_button_rect, mouse, mouse_click)
            draw_button(screen, verdana, "Spēli sāk dators", pcstart_button_rect, mouse, mouse_click)

        # spele
        if in_game:
            draw_button(screen, verdana, "Atgriezties", return_ingame_button_rect, mouse, mouse_click)
        else:
            if chosen_algorithm == 0:
                draw_text(screen, verdana, "Gadījumskaitļu algoritms", pygame.Rect(307, 440, 240, 30), (50, 50, 50))
            if chosen_algorithm == 1:
                draw_text(screen, verdana, "Minimaksa algoritms", pygame.Rect(307, 440, 240, 30), (50, 50, 50))
            if chosen_algorithm == 2:
                draw_text(screen, verdana, "Alfa-Beta algoritms", pygame.Rect(307, 440, 240, 30), (50, 50, 50))

            if player_starts:
                draw_text(screen, verdana, "Spēli sāk cilvēks - " + str(line_count), pygame.Rect(307, 420, 240, 30),
                          (50, 50, 50))
            else:
                draw_text(screen, verdana, "Spēli sāk dators - " + str(line_count), pygame.Rect(307, 420, 240, 30),
                          (50, 50, 50))

        # atjaunina rezultatu 60 fps
        pygame.display.flip()
        clock.tick(60)

    # bez si jupyter notebook kernel crasho
    pygame.quit()


if __name__ == "__main__":
    main()
