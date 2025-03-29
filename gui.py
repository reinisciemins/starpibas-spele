import pygame
import random
import os
from minimax import MinimaxALG
from alfabeta import AlphaBetaALG


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
    collide = rect.collidepoint(mouse)

    # fade efekts
    if collide:
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

    # atgriez true kad nokliksinata poga
    return click and collide


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


# ari nepieciesams statisks mainigais
element_colors = {}


def draw_data(surface, font, data, mouse_pos, mouse_click):
    global element_colors

    # saglaba nonenamo indeksu un vertibu
    clicked_value = 0
    to_remove = -1

    # prieks elementu kartosanas
    items = list(data.items())

    # parrekina indeksu pozicijas pec elementa nonemsanas
    new_data = {i: v for i, (old_index, v) in enumerate(items)}

    for index, value in new_data.items():
        row = index % 3  # pieskir rindu 0, 1 vai 2
        col = index // 3  # dinamiski pieskir kolonu

        # elementu skaits rinda prieks centresanas
        row_items = [k for k in new_data.keys() if k % 3 == row]
        total_width = len(row_items) * 85 - 50
        start_x = (854 - total_width) // 2

        x = start_x + col * 85
        y = 170 + row * 60

        # krasas pec vertibam
        base_colors = {1: (255, 0, 0), 2: (0, 0, 255), 3: (0, 255, 0)}
        base_color = base_colors.get(value, (255, 255, 255))

        # saglaba krasu ja ta ieprieks nav bijusi saglabata
        if index not in element_colors:
            element_colors[index] = 170

            # kursors ir uzlikts virsu
        rect = pygame.Rect(x, y, 35, 35)
        hover = rect.collidepoint(mouse_pos)

        if hover:
            element_colors[index] = min(element_colors[index] + 4, 255)
        else:
            element_colors[index] = max(element_colors[index] - 4, 170)

        # Adjust brightness based on hover
        hover_color = (
        min(base_color[0] + element_colors[index] - 170, 255), min(base_color[1] + element_colors[index] - 170, 255),
        min(base_color[2] + element_colors[index] - 170, 255))

        # sis indeks tiks nonemts
        if mouse_click and hover:
            clicked_value = value
            to_remove = index

        # uzzime pogu
        pygame.draw.rect(surface, (125, 125, 125), (rect[0] - 2, rect[1] - 2, rect[2] + 4, rect[3] + 4))
        pygame.draw.rect(surface, (0, 0, 0), (rect[0] - 1, rect[1] - 1, rect[2] + 2, rect[3] + 2))
        draw_vertical_gradient_rect(surface, (0, 0, 0), hover_color, rect)

        # teksts ieks taisnstura
        text_surface = font.render(str(value), True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=rect.center)
        surface.blit(text_surface, text_rect)

    # nonem uzspiesto pec indeksa
    if to_remove != -1:
        del new_data[to_remove]
        del element_colors[to_remove]

    # atjauno vardnicu ar jaunajiem indeksiem
    data.clear()
    data.update(new_data)

    return clicked_value  # atgriez nokliskinatas izveles vertibu


# gadijumskaitlu algoritms atgriez izveles indeksu (data - vardnica ar vertibam un indeksiem)
def get_random_choice(data):
    return random.choice(list(data.values()))


# alfabeta algoritms atgriez izveles indeksu
def get_alphabeta_choice(data):
    return alphabeta_alg.get_best_move(data, 4)

# galvena funkcija
def main():
    # nomaina aktivo direktoriju uz to kur python fails atrodas (doma uztaisit kkadu logo prieks main ekrana)
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # inicialize pygame
    pygame.init()
    minimax_alg = MinimaxALG()
    alphabeta_alg = AlphaBetaALG()
    clock = pygame.time.Clock()

    # resolucijas un nosaukuma iestatisana
    screen = pygame.display.set_mode((854, 480))
    pygame.display.set_caption("Starpības spēle - 1. praktiskais darbs - Mākslīgā intelekta pamati")

    # inicialize ikonu
    icon = pygame.image.load("icon.png")
    pygame.display.set_icon(icon)

    # inicialize main menu logo ar rgba kanaliem
    logo = pygame.image.load("logo.png").convert_alpha()

    # inicialize fontu
    verdana = pygame.font.Font(pygame.font.match_font("Verdana"), 16)
    verdana.set_bold(True)

    # saglaba statiskus mainigos
    running, mouse_click = True, False
    in_menu, in_options, in_game = True, False, False
    should_generate_game = True

    # speles gajieni
    game_data = {}

    # inicialize 20 dalinu sakuma pozicijas
    particles = [(random.randint(0, 854), random.randint(0, 480)) for _ in range(75)]

    # saglaba opciju izveles plaknes izmerus
    linecount_minus_rect = pygame.Rect(449, 165, 120, 30)
    linecount_plus_rect = pygame.Rect(569, 165, 120, 30)

    # izveletais algoritms, 0 - gadijumskaitlu, 1 - minimaksa, 2 - alfa-beta
    chosen_algorithm, game_start_time, timer, player_score, computer_score = 0, 0, 0, 80, 80
    winner = "Jūs uzvarējāt!"
    player_turn = True

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
                    if in_options:
                        if linecount_minus_rect.collidepoint(mouse):
                            line_count -= 1
                            line_count = max(line_count, 15)
                        if linecount_plus_rect.collidepoint(mouse):
                            line_count += 1
                            line_count = min(line_count, 25)

        # fona krasa
        screen.fill((0, 0, 0))

        # fona efekts
        draw_falling_particles(screen, particles)

        # fona apmales
        draw_outline(screen, pygame.Rect(0, 0, 854, 480), (40, 40, 40), 9)
        draw_outline(screen, pygame.Rect(6, 6, 842, 468), (150, 150, 150))

        # galvena izvele
        if in_menu:
            # fona logo
            screen.blit(logo, (213, 5))

            if draw_button(screen, verdana, "Sākt spēli", pygame.Rect(367, 210, 120, 30), mouse, mouse_click):
                in_game, in_menu = True, False

            if draw_button(screen, verdana, "Opcijas", pygame.Rect(367, 250, 120, 30), mouse, mouse_click):
                in_options, in_menu = True, False

            if draw_button(screen, verdana, "Iziet", pygame.Rect(367, 290, 120, 30), mouse, mouse_click):
                pygame.quit()
                return

        # opciju izvele
        if in_options:
            draw_text(screen, verdana, "Algoritma izvēlne", pygame.Rect(165, 125, 240, 30))

            if draw_button(screen, verdana, "Gadījumskaitļu algoritms", pygame.Rect(165, 165, 240, 30), mouse,
                           mouse_click):
                chosen_algorithm = 0

            if draw_button(screen, verdana, "Minimaksa algoritms", pygame.Rect(165, 205, 240, 30), mouse, mouse_click):
                chosen_algorithm = 1

            if draw_button(screen, verdana, "Alfa-Beta algoritms", pygame.Rect(165, 245, 240, 30), mouse, mouse_click):
                chosen_algorithm = 2

            if draw_button(screen, verdana, "Atgriezties", pygame.Rect(367, 325, 120, 30), mouse, mouse_click):
                in_options, in_menu = False, True

            draw_text(screen, verdana, "Spēles nosacījumi", pygame.Rect(449, 125, 240, 30))
            draw_button(screen, verdana, "-   Virknes garums: ", pygame.Rect(449, 165, 240, 30), mouse, mouse_click,
                        line_count, "   +")

            if draw_button(screen, verdana, "Spēli sāk cilvēks", pygame.Rect(449, 205, 240, 30), mouse, mouse_click):
                player_turn = True

            if draw_button(screen, verdana, "Spēli sāk dators", pygame.Rect(449, 245, 240, 30), mouse, mouse_click):
                player_turn = False

        # spele
        if in_game:
            if draw_button(screen, verdana, "Atgriezties", pygame.Rect(367, 430, 120, 30), mouse, mouse_click):
                in_game, in_menu = False, True

            # tiek izskauts vienu reizi katra speles sakuma
            if should_generate_game:
                timer = pygame.time.get_ticks() if player_turn == False else 0  # taimeris uzreiz ja dators veic pirmo gajienu
                game_data = {i: random.randint(1, 3) for i in range(line_count)}
                game_start_time = pygame.time.get_ticks()
                player_score, computer_score = 80, 80
                should_generate_game = False

            # parbauda vai 0.5 sekundes pagajusas kops speles sakuma
            # dazreiz ja kursors bija uz sakt kreisais peles kliksis nepaspej tikt 'atlaists'
            # un tad sanak netisam izveleties kadu no gajieniem to neapzinoties
            game_ready = pygame.time.get_ticks() - game_start_time > 300

            # parbauda vai var tikt veikts gajiens
            player_can_move = any(value <= player_score for value in game_data.values())
            computer_can_move = any(value <= computer_score for value in game_data.values())

            # vairs nevar veikt gajienus, nosaka uzvaretaju
            if player_can_move == False and computer_can_move == False:
                if player_score > computer_score:
                    winner = "Jūs uzvarējāt :)"
                elif computer_score > player_score:
                    winner = "Jūs zaudējāt :("
                else:
                    winner = "Neizšķirts"

                # rezultata teksts
                draw_text(screen, verdana, winner, pygame.Rect(367, 225, 120, 30), (150, 150, 150))

            # speletajs veic gajienu
            elif player_turn and player_can_move:
                turn_result = draw_data(screen, verdana, game_data, mouse, mouse_click) if game_ready else 0

                if turn_result > 0:
                    player_score -= turn_result
                    player_turn = False
                    timer = pygame.time.get_ticks()
            # datora gajiens
            elif player_turn == False and computer_can_move:
                draw_data(screen, verdana, game_data, mouse, False)

                if timer and pygame.time.get_ticks() - timer > 1000:
                    if game_data:
                        if chosen_algorithm == 0:  # Random
                            computer_choice = get_random_choice(game_data)
                        elif chosen_algorithm == 1:  # Minimax
                            # Pārveidojam game_data uz vārdnīcu ar skaitliskiem indeksiem
                            indexed_data = {i: v for i, v in enumerate(game_data.values())}
                            computer_choice = minimax_alg.get_minimax_choice(
                                indexed_data,
                                player_score,
                                computer_score
                            )
                        elif chosen_algorithm == 2:  # Alpha-beta
                            # Pārveidojam game_data uz vārdnīcu ar skaitliskiem indeksiem
                            indexed_data = {i: v for i, v in enumerate(game_data.values())}
                            computer_choice = alphabeta_alg.get_best_move(
                                indexed_data,
                                player_score,
                                computer_score,
                                depth=4
                            )

                        if computer_choice is not None and computer_choice <= computer_score:
                            computer_score -= computer_choice
                            # Meklējam pirmo atbilstošo vērtību un noņemam
                            for key, value in list(game_data.items()):
                                if value == computer_choice:
                                    del game_data[key]
                                    break

                            player_turn = True
                            timer = 0

            if player_turn and player_can_move:
                draw_text(screen, verdana, "Tavs gājiens", pygame.Rect(367, 5, 120, 30), (150, 150, 150))
            elif player_turn == False and computer_can_move:
                draw_text(screen, verdana, "Dators veic gājienu", pygame.Rect(367, 5, 120, 30), (150, 150, 150))

            draw_text(screen, verdana, "C: " + str(player_score), pygame.Rect(20, 5, 30, 30), (150, 150, 150))
            draw_text(screen, verdana, "D: " + str(computer_score), pygame.Rect(804, 5, 30, 30), (150, 150, 150))
        else:
            if chosen_algorithm == 0:
                draw_text(screen, verdana, "Gadījumskaitļu algoritms", pygame.Rect(307, 440, 240, 30), (50, 50, 50))
            if chosen_algorithm == 1:
                draw_text(screen, verdana, "Minimaksa algoritms", pygame.Rect(307, 440, 240, 30), (50, 50, 50))
            if chosen_algorithm == 2:
                draw_text(screen, verdana, "Alfa-Beta algoritms", pygame.Rect(307, 440, 240, 30), (50, 50, 50))

            if player_turn:
                draw_text(screen, verdana, "Spēli sāk cilvēks - " + str(line_count), pygame.Rect(307, 420, 240, 30),
                          (50, 50, 50))
            else:
                draw_text(screen, verdana, "Spēli sāk dators - " + str(line_count), pygame.Rect(307, 420, 240, 30),
                          (50, 50, 50))

            should_generate_game = True

        # atjaunina rezultatu 60 fps
        pygame.display.flip()
        clock.tick(60)

    # bez si jupyter notebook kernel crasho
    pygame.quit()


if __name__ == "__main__":
    main()
