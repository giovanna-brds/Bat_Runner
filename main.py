import asyncio
import pygame
import random
from sys import exit

pygame.init() 

# config tela
tela = pygame.display.set_mode((800,600)) #larg e altura
pygame.display.set_caption('Bat Runner')
clock = pygame.time.Clock()

async def main():

    fonte = pygame.font.SysFont('Menlo', 32, bold= True )
    fonte_pequena = pygame.font.SysFont('Menlo', 22) 
    estado_jogo = "inicio"

    score = 0
    vidas =3
    tempoimune =0
    vel_jogo = 6

    cave_superficieOG =pygame.image.load('assets/imagens/backgroundCaverna.png').convert()
    cave_superficie = pygame.transform.scale(cave_superficieOG, (800,600))
    background_x = 0

    ground_superficie = pygame.image.load('assets/imagens/groundPedraRoxa4.png').convert()
    ground_x = 0


    morcego_frame1 = pygame.image.load('assets/imagens/bat_frame1.png').convert_alpha()
    morcego_frame2 = pygame.image.load('assets/imagens/bat_frame2.png').convert_alpha()
    morcego_frame3 = pygame.image.load('assets/imagens/bat_frame3.png').convert_alpha()
    morcego_sprite = [morcego_frame1, morcego_frame2, morcego_frame3]
    morcego_index = 0
    morcego_superficie = morcego_sprite[morcego_index]
    morcego_mask = pygame.mask.from_surface(morcego_superficie)
    morcego_anim = pygame.USEREVENT + 2
    pygame.time.set_timer(morcego_anim, 200)

    morcego_rect = morcego_superficie.get_rect(midbottom = (100,300))


    cristal1 = pygame.image.load("assets/imagens/cristal1.png").convert_alpha()
    cristal2 = pygame.image.load("assets/imagens/cristal2.png").convert_alpha()
    cristal3 = pygame.image.load("assets/imagens/cristal3.png").convert_alpha()
    cristal4 = pygame.image.load("assets/imagens/cristal4.png").convert_alpha()
    cristal_grande = pygame.transform.scale(cristal4, (250, 240)) 

    cristal_teto1= pygame.transform.flip(cristal1, False, True)
    cristal_teto2= pygame.transform.flip(cristal2, False, True)
    cristal_teto3= pygame.transform.flip(cristal3, False, True)
    cristal_teto4= pygame.transform.flip(cristal4, False, True)
    cristal_teto_grande = pygame.transform.flip(cristal_grande, False, True)

    opcoes_cristais = [
        (cristal1, pygame.mask.from_surface(cristal1), "chao"),
        (cristal2, pygame.mask.from_surface(cristal2), "chao"),
        (cristal3, pygame.mask.from_surface(cristal3), "chao"),
        (cristal4, pygame.mask.from_surface(cristal4), "chao"),
        (cristal_grande, pygame.mask.from_surface(cristal_grande), "chao"),
        (cristal_teto_grande, pygame.mask.from_surface(cristal_teto_grande), "teto"),
        (cristal_teto1, pygame.mask.from_surface(cristal_teto1), "teto"),
        (cristal_teto2, pygame.mask.from_surface(cristal_teto2), "teto"),
        (cristal_teto3, pygame.mask.from_surface(cristal_teto3),"teto"),
        (cristal_teto4, pygame.mask.from_surface(cristal_teto4), "teto"),
        
    ]

    obstaculo_timer = pygame.USEREVENT +1
    pygame.time.set_timer(obstaculo_timer, 650)  # Cria um novo obstáculo a cada 1.4 segundos
    lista_obstaculos = []

    pos_chao_y = 550
    pos_teto_y = 60

    dificuldade_timer = pygame.USEREVENT + 3
    pygame.time.set_timer(dificuldade_timer, 5000)

    morcego_rect = morcego_superficie.get_rect(center=(100, 300))

    await asyncio.sleep(0)

    rodando = True

    while rodando:
        tempo_atual = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
                break

            if estado_jogo =="inicio":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    estado_jogo = "jogando"
            elif estado_jogo == "game_over":
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                                    jogo_ativo = "jogando"
                                    vidas = 3
                                    score = 0
                                    vel_jogo = 6
                                    lista_obstaculos.clear()
                                    morcego_rect.center = (100,300)

            elif estado_jogo == "jogando":
                    
                    if event.type == morcego_anim:
                        morcego_index = (morcego_index + 1) % len(morcego_sprite)
                        morcego_superficie = morcego_sprite[morcego_index]
                    

                    if event.type == obstaculo_timer:
                        img_sorteada, mask_sorteada, pos_tipo = random.choice(opcoes_cristais)

                        if pos_tipo == "chao":
                            rect = img_sorteada.get_rect(midbottom=(850, 565))
                        else: 
                            rect = img_sorteada.get_rect(midtop=(850, pos_teto_y))

                        lista_obstaculos.append((img_sorteada, mask_sorteada, rect))

                    if event.type == dificuldade_timer and vel_jogo < 15:
                        vel_jogo += 0.5
            

        if estado_jogo == "inicio":

            tela.fill((20, 10, 25))
            
            texto_titulo = fonte.render("BAT RUNNER", True, "White")
            texto_start = fonte_pequena.render("Pressione ENTER para Iniciar", True, (200, 200, 200))
            texto_controles = fonte_pequena.render("Controles: Setas para CIMA e BAIXO", True, "Yellow")

            tela.blit(texto_titulo, texto_titulo.get_rect(center=(400, 200)))
            tela.blit(texto_start, texto_start.get_rect(center=(400, 320)))
            tela.blit(texto_controles, texto_controles.get_rect(center=(400, 400)))

        elif estado_jogo == "jogando":
            score +=1

            teclas = pygame.key.get_pressed()
            if (teclas[pygame.K_UP] or teclas[pygame.K_w]) and morcego_rect.top > 60:
                morcego_rect.y -= 8
            if (teclas[pygame.K_DOWN] or teclas[pygame.K_s]) and morcego_rect.bottom < 550:
                morcego_rect.y += 8
            
            ground_x -= vel_jogo
            if ground_x <= -800:
                ground_x = 0

            background_x -= (vel_jogo/3)
            if background_x <= -800:
                background_x = 0

            tela.blit(cave_superficie,(background_x,0))
            tela.blit(cave_superficie,(background_x + 800,0))
        
        

            morcego_mask = pygame.mask.from_surface(morcego_superficie)

            for item in lista_obstaculos[:]:
                img, mask_cristal, rect = item
                rect.x -= vel_jogo
                tela.blit(img,rect)

                offset_x= rect.x - morcego_rect.x
                offset_y= rect.y - morcego_rect.y


                colisao = morcego_mask.overlap(mask_cristal, (offset_x, offset_y) )

                

                if colisao and tempo_atual> tempoimune:
                        vidas -=1
                        tempoimune = tempo_atual + 1000
                        if vidas <= 0:
                            estado_jogo = "game_over"

                if rect.right < 0:
                    lista_obstaculos.remove(item)


            tela.blit(ground_superficie,(ground_x, pos_chao_y))
            tela.blit(ground_superficie,(ground_x + 800, pos_chao_y))
            
            if tempo_atual< tempoimune:
                if (tempo_atual// 100)% 2 == 0:
                    tela.blit(morcego_superficie, morcego_rect)
            else: tela.blit(morcego_superficie, morcego_rect)


            pygame.draw.rect(tela, (25, 15, 35), (0, 0, 800, 60))
            pygame.draw.line(tela, "#5a2c7a", (0, 60), (800, 60), 2)

            # Título
            texto_titulo = fonte.render("Bat Runner", True, "White")
            tela.blit(texto_titulo, texto_titulo.get_rect(center=(400, 30)))

            # Vidas
            texto_vidas = fonte_pequena.render(f"Vidas: {vidas}", True, "#98095e")
            tela.blit(texto_vidas, (20, 18))

            # Score
            texto_score = fonte_pequena.render(f"Score: {score // 10}", True, "#47e0fb")
            tela.blit(texto_score, (660, 18))

        elif estado_jogo == "game_over":
            tela.fill((20, 10, 25))
            texto_game_over = fonte_pequena.render("GAME OVER", True, "#47e0fb")
            texto_pontos = fonte_pequena.render(f"Pontuação Final: {score // 10}", True, "Yellow")
            texto_restart = fonte_pequena.render("Pressione ESPAÇO para reiniciar", True, "White")
            
            tela.blit(texto_game_over, texto_game_over.get_rect(center=(400, 200)))
            tela.blit(texto_pontos, texto_pontos.get_rect(center=(400, 290)))
            tela.blit(texto_restart, texto_restart.get_rect(center=(400, 360)))





        pygame.display.update()
        clock.tick(60)
        await asyncio.sleep(0)

    pygame.quit()
asyncio.run(main())







  
   