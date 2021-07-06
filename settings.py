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
		self.ship_speed = 1.5

		# Bullet settings
		self.bullet_speed = 1.0
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = (60,60,60)
		self.bullets_allowed = 3

		# Alien settings
		self.alien_speed = 1.0
		self.fleet_drop_speed = 10
		self.fleet_direction = 1