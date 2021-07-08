class Settings:
	""" A class to store all settings for Alien Invasion """

	def __init__(self):
		""" Initialize game settings """

		# Screen settings
		self.screen_width = 1000
		self.screen_height = 600
		self.bg_color = (230,230,230)
		self.fullscreen_game = False

		# Ship settings
		self.ship_limit = 3

		# Bullet settings
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = (60,60,60)
		self.bullets_allowed = 3
		self.bullet_piercing = False

		# Alien settings
		self.fleet_drop_speed = 10

		self.speedup_scale = 1.1
		self.score_scale = 1.5


	def init_dynamic_params(self):
		self.fleet_direction = 1
		self.alien_speed = 1.0
		self.bullet_speed = 1.0
		self.ship_speed = 1.5
		self.alien_points = 50

	def increase_speed(self):
		self.alien_speed *= self.speedup_scale
		self.bullet_speed *= self.speedup_scale
		self.ship_speed *= self.speedup_scale
		self.alien_points = int(self.alien_points * self.score_scale)
