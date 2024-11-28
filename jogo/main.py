import pygame
import random
import sys

# Inicializando o Pygame
pygame.init()

# Definindo as cores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Definindo as dimensões da tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Desvie das rochas")

# Definindo o relógio
clock = pygame.time.Clock()

# Carregar imagens
try:
    car_img1 = pygame.image.load('carro.png')  # Primeira imagem do carro (normal)
    car_img_broken = pygame.image.load('carro_quebrado.png')  # Imagem do carro quebrado com fundo transparente
    rock_img = pygame.image.load('rocha.png')  # Imagem da rocha
except pygame.error as e:
    print("Erro ao carregar as imagens:", e)
    pygame.quit()
    sys.exit()

# Definindo o tamanho do carro
car_width = 100
car_height = 120
rock_width = 60
rock_height = 60

# Redimensionando as imagens
car_img1 = pygame.transform.scale(car_img1, (car_width, car_height))
car_img_broken = pygame.transform.scale(car_img_broken, (car_width, car_height))
rock_img = pygame.transform.scale(rock_img, (rock_width, rock_height))

# Variáveis do jogo
score = 0
game_over = False
broken = False  # Flag para indicar se o carro está quebrado

# Função para desenhar o carro
def draw_car(x, y, broken):
    if broken:  # Exibe o carro quebrado após a colisão
        screen.blit(car_img_broken, (x, y))
    else:  # Exibe o carro normal
        screen.blit(car_img1, (x, y))

# Função para desenhar as rochas
def draw_rocks(rocks):
    for rock in rocks:
        screen.blit(rock_img, (rock.x, rock.y))  # Desenha a rocha na posição da rocha

# Função para gerar novas rochas
def generate_rocks(rocks):
    if random.randint(1, 100) <= 2:
        rock_x = random.randint(0, SCREEN_WIDTH - rock_width)
        new_rock = pygame.Rect(rock_x, -rock_height, rock_width, rock_height)
        rocks.append(new_rock)

# Função para mostrar a tela de Game Over
def show_game_over():
    font = pygame.font.SysFont("arial", 50)
    game_over_text = font.render("Se Fodeu! Pressione 'R' para reiniciar.", True, BLACK)
    game_over_rect = game_over_text.get_rect()
    game_over_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    # Exibindo o carro quebrado abaixo do texto
    screen.blit(car_img_broken, (SCREEN_WIDTH // 2 - car_width // 2, SCREEN_HEIGHT // 2 + 70))
    screen.blit(game_over_text, game_over_rect)
    pygame.display.update()

# Função para exibir a tela inicial com o botão que treme
def show_start_screen():
    font = pygame.font.SysFont("arial", 40)
    start_text = font.render("Pressione no botão para começar", True, BLACK)
    start_rect = start_text.get_rect()
    start_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)

    # Criar o botão com o texto "Iniciar"
    button_width = 200
    button_height = 60
    button_color = GREEN
    button_rect = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2 + 50, button_width, button_height)

    # Detecta se o cursor está sobre o botão
    mouse_pos = pygame.mouse.get_pos()
    tremor_offset = 0
    if button_rect.collidepoint(mouse_pos):  # Quando o mouse está sobre o botão
        # Efeito de tremor do botão
        tremor_offset = random.randint(-5, 5)

    # Desenhando o botão
    pygame.draw.rect(screen, button_color, button_rect.move(tremor_offset, 0))  # Botão com tremor horizontal

    # Desenhando o texto dentro do botão
    button_text = font.render("Iniciar", True, BLACK)
    button_text_rect = button_text.get_rect()
    button_text_rect.center = button_rect.center
    screen.blit(button_text, button_text_rect)

    # Desenhar o texto principal
    screen.blit(start_text, start_rect)

    pygame.display.update()

    return button_rect

# Função principal do jogo
def game_loop():
    global game_over, broken
    running = True
    start_screen = True
    rocks = []
    car_x = SCREEN_WIDTH // 2 - car_width // 2
    car_y = SCREEN_HEIGHT - car_height - 10

    while running:
        screen.fill(WHITE)

        # Captura de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if start_screen:
            button_rect = show_start_screen()
            # Detectar o clique do mouse no botão
            if pygame.mouse.get_pressed()[0] and button_rect.collidepoint(pygame.mouse.get_pos()):
                start_screen = False  # Começar o jogo ao clicar no botão
            continue

        if game_over:
            show_game_over()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:  # Reinicia o jogo quando pressionar 'R'
                game_over = False
                broken = False  # Resetando o estado do carro
                rocks = []
                car_x = SCREEN_WIDTH // 2 - car_width // 2
                car_y = SCREEN_HEIGHT - car_height - 10
            continue

        # Movimentação do carro
        if not game_over:  # Só move o carro se não estiver no Game Over
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and car_x > 0:
                car_x -= 10
            if keys[pygame.K_RIGHT] and car_x < SCREEN_WIDTH - car_width:
                car_x += 10

        # Gerar e mover rochas
        generate_rocks(rocks)
        for rock in rocks:
            rock.y += 4
        rocks = [rock for rock in rocks if rock.y < SCREEN_HEIGHT]

        # Verificar colisão
        car_rect = pygame.Rect(car_x, car_y, car_width, car_height)
        for rock in rocks:
            if car_rect.colliderect(rock):
                game_over = True
                broken = True
                break

        # Desenhar o carro e as rochas
        draw_car(car_x, car_y, broken)
        draw_rocks(rocks)

        pygame.display.update()
        clock.tick(60)

# Iniciar o jogo
game_loop()
