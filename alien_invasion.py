from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from time import sleep
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

import sys
import pygame

class AlienInvation:
    def __init__(self):
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.bg_color = self.settings.bg_color
        pygame.display.set_caption("Alien Invasion")

        #Crear una instancia para guardar las estadisticas del juego
        # y crea un marcador
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        
        self._create_fleet()

        #hace el boton play.
        self.play_button = Button(self, "Play")

    def run_game(self):
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()
        
        
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)    


    def _update_screen(self):
        self.screen.fill(self.bg_color)
        self.ship.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)

        #dibuja la informacion de la puntuacion
        self.sb.show_score()

        #dibuja el boton para jugar si el juego esta inactivo
        if not self.stats.game_active:
            self.play_button.draw_button()
        
        pygame.display.flip()

    def _update_bullets(self):
        self.bullets.update()
        # Se deshace de las balas que han desaparecido
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        #comprobar eliminacion de la balas al tocar el borde
        #print(len(self.bullets))

        self._check_bullet_alien_collisions()

        """Actualiza la posición de las balas y se deshace de las viejas"""
      



    def _check_bullet_alien_collisions(self):
        """Responed a las colisiones bala-alien"""
        #retira todas las blalas y aliens que han chocado
        #busca balas que hayan dado a aliens.
        #SWi hay, se deshace de la bala y del alien
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, False, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # Destruye las balas existentes y crea una flota.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            #aumenta el nivel
            self.stats.level +=1
            self.sb.prep_level()

    
    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """crea una bala nueva y la añade al grupo de balas"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _create_fleet(self):
        """Crea la flota ed aliens."""
        # hace un alien.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width) 
        number_aliens_x = available_space_x // ( 2 * alien_width )

        #determina el numero de filas de aliens que caben en la pantalla
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        #crear flota completa de aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)
                #crear un alien y locoloca en la fila
                alien = Alien(self)
                alien.x = alien_width + 2 * alien_width * alien_number
                alien.rect.x = alien.x
                self.aliens.add(alien)

    def _create_alien(self, alien_number, row_number):
        """Crea un alien y lo coloca en la fila"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _update_aliens(self):
        """Comprueba si la flota está en un borde,
        después actualiza las posiciones de todos los aliens de la flota"""

        self._check_fleet_edges()
        self.aliens.update()

        #busca colisiones alien-nave
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        #busca aliens llegando al fondo de la pantalla
        self._check_aliens_bottom()



    def _check_fleet_edges(self):
        """Responde adecuadamente si algun alien ha llegado alun borde"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        """Baja toda la flota y cambia su direccion"""
        for alien in  self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction  *=-1

    def _ship_hit(self):
        """Responde al impacto de un alien en la nave"""
        if self.stats.ships_left > 0:
            # Disminuye ships_left
            self.stats.ships_left -=1

            # Se deshace de los aliens y balas restantes.
            self.aliens.empty()
            self.bullets.empty
        
            # Crea una flota nueva y centra la nave.
            self._create_fleet()
            self.ship.center_ship()
            # Pausa
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Comprueba si al  gun alien ha llegado al fondo de la pantalla"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                #trata esto como si la nave hubiese sido alcanzada.
                self._ship_hit()
                break

    def _check_play_button(self, mouse_pos):
        """Inicia un juego nuevo cuando el jugador hace click en Play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            #restablece las estadisticas del juego
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()

            #se deshace de los aliens y las balas que quedan
            self.aliens.empty()
            self.bullets.empty

            #crea una flota nueva y centra la nave.
            self._create_fleet()
            self.ship.center_ship()

            #oculta el cursor del raton
            pygame.mouse.set_visible(False)

            #restablece las configuraciones del juego.
            self.settings.initialize_dynamic_settings()
    


if __name__ == '__main__':
    ai = AlienInvation()
    ai.run_game()
