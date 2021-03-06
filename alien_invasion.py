import sys
import pygame
from time import sleep

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

class AlienInvasion:
	""" Overall class to manage assets and behavior.  """

	def __init__(self):
		""" Initialize the game, and create game resources. """
		pygame.init()



		self.settings = Settings()
		if self.settings.fullscreen_game:
			self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
		else:
			self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))

		self.settings.screen_width = self.screen.get_rect().width
		self.settings.screen_height = self.screen.get_rect().height

		pygame.display.set_caption("Alien Invasion")

		self.stats = GameStats(self)
		self.sb = Scoreboard(self)
		self.ship = Ship(self)
		self.bullets = pygame.sprite.Group()

		self.aliens = pygame.sprite.Group()
		self._create_fleet()

		# Set the background color
		self.bg_color = self.settings.bg_color

		self.play_button = Button(self,"Play")

	def run_game(self):
		""" Start the main loop for the game. """
		while True:
			self._check_events()
			if self.stats.game_active and not self.stats.game_paused:
				self.ship.update()
				self._update_bullets()
				self._update_aliens()
			self._update_screen()

	def _ship_hit(self):
		""" Repond to the ship being hit by an alien """
		
		# Decrement ships left
		self.stats.ships_left -= 1
		self.sb.prep_ships()		
		if self.stats.ships_left > 0:


			# print(self.stats.ships_left)
			# Get rid of any remaining aliens and bullets
			self.aliens.empty()
			self.bullets.empty()

			# Create new sheep and fleet
			self._create_fleet()
			self.ship.center_ship()

			# Pause
			sleep(0.5)

		else:
			self.stats.game_active = False
			pygame.mouse.set_visible(True)

	def _check_high_score(self):
		if self.stats.high_score < self.stats.score:
			self.stats.high_score = self.stats.score
			self.sb.prep_high_score()				

	def _check_events(self):
		# watch for keyboard and mouse events.
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				self._check_keydown_events(event)
			elif event.type == pygame.KEYUP:
				self._check_keyup_events(event)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				self._check_play_button(mouse_pos)


	def _check_keydown_events(self,event):
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = True
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = True
		elif event.key == pygame.K_q:
			sys.exit()
		elif event.key == pygame.K_SPACE:
			self._fire_bullet()
		elif event.key == pygame.K_p:
			self.stats.game_paused = not self.stats.game_paused 

	def _check_keyup_events(self,event):
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = False
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = False		

	def _check_play_button(self,mouse_pos):
		if not self.stats.game_active and self.play_button.rect.collidepoint(mouse_pos):
			self.stats.reset_stats()
			self.stats.game_active = True
			pygame.mouse.set_visible(False)

			self.aliens.empty()
			self.bullets.empty()

			self._create_fleet()
			self.ship.center_ship()
			self.settings.init_dynamic_params()

			self.sb.prep_level()
			self.sb.prep_score()
			self.sb.prep_ships()



	def _fire_bullet(self):
		""" Create a new bullet and add it to the bullets. """
		if len(self.bullets) < self.settings.bullets_allowed:
			new_bullet = Bullet(self)
			self.bullets.add(new_bullet)

	def _update_bullets(self):

		self.bullets.update()
		for bullet in self.bullets.copy():
			if bullet.rect.bottom <= 0:
				self.bullets.remove(bullet)
		self._check_bulet_alien_collisions()


	def _check_bulet_alien_collisions(self):

		collisions = pygame.sprite.groupcollide(self.bullets,self.aliens,not self.settings.bullet_piercing,True)
		if collisions:
			for aliens in collisions.values():
				self.stats.score += ( self.settings.alien_points * len(aliens))
			self.sb.prep_score()
			self._check_high_score()

		if not self.aliens:
			self.bullets.empty()
			self._create_fleet()
			self.settings.increase_speed()
			self.stats.level += 1

			self.sb.prep_level()
			

	def _create_fleet(self):
		""" Create the fleet of aliens. """
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size 
		available_space_x = self.settings.screen_width - 2 * alien_width
		number_aliens_x = available_space_x // (2*alien_width)
		ship_height = self.ship.rect.height
		avaliable_space_y = self.settings.screen_height - (3 * alien_height) - ship_height
		number_aliens_y = avaliable_space_y // (2 * alien_height)
		# Create firs row of aliens.

		for row_number in range(number_aliens_y):
			for alien_number in range(number_aliens_x):
				self._create_alien(alien_number,row_number)

	def _create_alien(self,alien_number,row_number):
		alien = Alien(self)
		alien_width,alien_height = alien.rect.size 
		alien.x = alien_width + 2 * alien_width * alien_number
		alien.rect.y = alien_height + 2 * alien_height * row_number
		alien.rect.x = alien.x
		self.aliens.add(alien) 

	def _check_fleet_edges(self):
		for alien in self.aliens.sprites():
			if alien.check_edges():
				self._change_fleet_direction()
				break

	def _check_aliens_bottom(self):
		screen_rect = self.screen.get_rect()
		for alien in self.aliens.sprites():
			if alien.rect.bottom >= screen_rect.bottom:
				self._ship_hit()
				break

	def _change_fleet_direction(self):
		for alien in self.aliens.sprites():
			alien.rect.y += self.settings.fleet_drop_speed
		self.settings.fleet_direction *= -1

	def _update_aliens(self):
		self._check_fleet_edges()
		self.aliens.update()
		if pygame.sprite.spritecollideany(self.ship,self.aliens):
			self._ship_hit()
		self._check_aliens_bottom()

	def _update_screen(self):
		""" redraw the screen during each pass through the loop """
		self.screen.fill(self.bg_color)
		self.ship.blitme()
		for bullet in self.bullets.sprites():
			bullet.draw_bullet()

		self.aliens.draw(self.screen)

		if not self.stats.game_active:
			self.play_button.draw_button()

		self.sb.show_score()

		# make the most recently drawn screen visible.
		pygame.display.flip()

if __name__ == '__main__':
	# Make a game instance, and run the gameb
	ai = AlienInvasion()
	ai.run_game()