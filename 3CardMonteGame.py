from  scene import *
import sound
import random
import ui

# --- to do ---
#high scores. creat, open and write to a file. 

#stop flashing winner text from becoming too big the second time it happens. 

#add status function to prevent the status from updating early before bet is won or lost or while bets are being made and bank roll is fluctuating
							
A = Action
						
class GameOver(Scene):
	def setup(self):
						
		self.go_node = Node(parent=self)
		
		self.game_over = SpriteNode('GameOver.PNG',position=(self.size.w/2, self.size.h/2), scale=1.10, parent=self.go_node)

		self.new_game = SpriteNode('StartNewGame.PNG', position=(self.size.w/2, self.size.h/2 * 0.32), scale=0.32, parent=self.go_node)	
				
	def dismiss_scene(self):
		self.dismiss_modal_scene()	
						
	def touch_began(self, touch):
		if touch.location in self.new_game.frame:
			self.main.bankroll_amount = 10_000
			self.main.bankroll_amount_label.text = f'{self.main.currency_type}{self.main.bankroll_amount:,}'
			self.main.main_node.run_action(A.fade_to(1, 1.5))	
			self.go_node.run_action(
				A.sequence(
					A.fade_to(0, 2), 
					A.wait(2), 
					A.call(self.dismiss_scene)))
													
class Rules(Scene):
	def setup(self):
		self.shadow=('black', 0, 10, 1)
		
		sound.set_volume(.25)
		self.rules_node = Node(parent=self)
		
		self.bg_color = ShapeNode(
			ui.Path.rounded_rect(0, 0, self.size.w * 0.73, self.size.h * 0.75, 10),
			color='#477148', 
			position=(self.size.w/2, self.size.h/2 * 0.95),
			alpha=0.7,
			stroke_color='black',
			shadow=self.shadow,			
			parent=self.rules_node)
		self.bg_color.line_width=3

		self.bg_color_2 = ShapeNode(
			ui.Path.rounded_rect(0, 0, self.size.w * 0.69, self.size.h * 0.69, 10),
			color='#477148', 
			position=(self.size.w/2, self.size.h/2),
			alpha=0.7,
			stroke_color='black',			
			parent=self.rules_node)
		self.bg_color_2.line_width=3
		
		self.rules_text = LabelNode(
			'Find the Ace of Spades', 
			('Arial Rounded MT Bold', 38), 
			position=(self.size.w/2, self.size.h/2 * 1.10), 
			color='black', 
			parent=self.rules_node)
			
		self.close_rules = LabelNode(
			'CLOSE',
			('American Typewriter ', 25), 
			position=(self.size.w/2, self.size.h/2 * 0.75), 
			color= 'black',
			parent=self.rules_node)
			
		self.rules_node.alpha=0
		self.rules_node.run_action(A.fade_to(1, 2))

	def dismiss_scene(self):
		self.dismiss_modal_scene()
		
	def touch_began(self, touch):
		if touch.location in self.close_rules.frame:
			self.rules_node.run_action(
				A.sequence(
					A.fade_to(0, 2), 
					A.wait(1), 
					A.call(self.dismiss_scene)))
			sound.set_volume(.6)
			
class Main(Scene):
	def setup(self):
		bg_music = sound.play_effect('3CardBeat.wav', volume=0.25)
		bg_music.looping = True
		self.allow_bets = True
		self.shuffle_active = True
		self.two_multiplier_active = False
		self.five_multiplier_active = False	
		self.reveal = False
		self.place_bet = False
		self.currency_type  = '$'
		self.bankroll_amount = 10_000
		self.stake_amount = 0
		self.floating_stakes = 0
		self.status = ''
		self.back_of_card = 'SkullBlueCard.PNG'
		self.cards = [
			'ace_of_spades.png',
			'ace_of_spades.png', 
			'ace_of_spades.png']
		self.status_dict = {
			10_000: 'Hustler', 
			15_000: 'Small Time', 
			20_000: 'Big Money', 
			25_000: 'Baller', 
			30_000: 'Top Dawg', 
			35_000: 'Boss', 
			40_000: 'Triple OG'}	
		self.money_bags_dict = {
			15_000: 1, 
			30_000: 2, 
			45_000: 3, 
			60_000: 4, 
			75_000: 5,
			90_000: 6,
			105_000: 7}
		self.background_color = '#477148'
		self.wooden_border()

		#--- nodes ---
		self.main_node = Node(parent=self)
		self.inc_bet_node = Node(parent=self.main_node)
		self.dec_bet_node = Node(parent=self.main_node)
		self.multiplier_node = Node(parent=self.main_node)
		self.bankroll_node = Node(parent=self.main_node)
		self.title_node = Node(parent=self.main_node)
		self.pos_node = Node(parent=self.main_node)
		self.money_pile_node = Node(position= (30, -5), parent=self.main_node)
		
		self.main_node.alpha=0
		self.main_node.run_action(A.fade_to(1, 1.5))
		
		#--- shape nodes ---
		self.oval_title = ShapeNode(ui.Path.oval(0,0,367,60), parent=self)
		self.oval_title.position = self.size.w/2 * 1.01, self.size.h/2 * 1.70
		self.oval_title.color = '#3b5e3c'
		self.oval_title.stroke_color = 'black'
		self.oval_title.line_width = 2
		self.oval_title.shadow =  ('black', 10, 15, 20)
		
		for yel in (self.size.w/2 * 0.55, self.size.h/2), (self.size.w/2, self.size.h/2), (self.size.w/2 * 1.45, self.size.h/2):
			self.yellow_rings = ShapeNode(ui.Path.rounded_rect(207,448, 160, 214, 20))
			self.yellow_rings.color = 'yellow'
			self.yellow_rings.position = yel
			self.yellow_rings.line_width = 4
			self.yellow_rings.fill_color = 'clear'
			self.yellow_rings.stroke_color = 'yellow'
			self.yellow_rings.z_position=-1
			self.add_child(self.yellow_rings)
			
		for oval in (self.size.w/2 * 0.55, self.size.h / 2 * 0.28), (self.size.w/2, self.size.h / 2 * 0.28), (self.size.w/2 * 1.45, self.size.h/2 * 0.28):
			self.oval_1 = ShapeNode(ui.Path.oval(0,0,128,55))
			self.oval_1.position = oval
			self.oval_1.color = '#3b5e3c'
			self.oval_1.stroke_color = 'black'
			self.oval_1.line_width = 2
			self.oval_1.shadow =  ('gray', 0, 0, 20)
			self.add_child(self.oval_1)
		
		self.button_color = '#2f4b30'
		self.button_alpha = 1
		self.button_shadow=('black', 0, 4, 2)
	
		self.shuffle_rect = ShapeNode(ui.Path.rounded_rect(800, 260, 125, 40, 10))
		self.shuffle_rect.position = (self.size.w/2 * 1.79, self.size.h/2 * 1.25)
		self.shuffle_rect.color = self.button_color
		self.shuffle_rect.alpha = self.button_alpha
		self.shuffle_rect.shadow=self.button_shadow
		self.main_node.add_child(self.shuffle_rect)
		
		#green ring for bet mutiplier
		self.green_ring = ShapeNode(ui.Path.rounded_rect(207,448, 128, 125, 20))
		self.green_ring.color = 'yellow'
		self.green_ring.position = self.size.w/2 * 1.79, self.size.h/2 * 0.80
		self.green_ring.line_width = 4
		self.green_ring.fill_color = 'clear'
		self.green_ring.stroke_color = '#3b5e3c'
		self.multiplier_node.add_child(self.green_ring)	
		
		self.two_rect = ShapeNode(ui.Path.rounded_rect(800, 260, 113, 42, 10))
		self.two_rect.position = (self.size.w/2 * 1.79, self.size.h/2 * 0.89)
		self.two_rect.line_width = 4
		self.two_rect.fill_color = 'clear'
		self.two_rect.stroke_color = '#3b5e3c'
		self.multiplier_node.add_child(self.two_rect)
		
		self.five_rect = ShapeNode(ui.Path.rounded_rect(800, 260, 113, 42, 10))
		self.five_rect.position = (self.size.w/2 * 1.79, self.size.h/2 * 0.65)
		self.five_rect.line_width = 4
		self.five_rect.fill_color = 'clear'
		self.five_rect.stroke_color = '#3b5e3c'		
		self.multiplier_node.add_child(self.five_rect)
		
		self.place_bet_rect = ShapeNode(ui.Path.rounded_rect(800, 260, 125, 40, 10))
		self.place_bet_rect.position = (self.size.w/2 * 1.79, self.size.h/2 * 0.30)
		self.place_bet_rect.color = self.button_color
		self.place_bet_rect.alpha = self.button_alpha
		self.place_bet_rect.shadow=self.button_shadow
		self.main_node.add_child(self.place_bet_rect)
			
		for bb in (self.size.w * .11, self.size.h * 0.54), (self.size.w * .11, self.size.h * 0.34):
			self.bet_rect = ShapeNode(ui.Path.rounded_rect(800, 260, 100, 40, 10))
			self.bet_rect.position = bb
			self.bet_rect.color = self.button_color
			self.bet_rect.alpha = self.button_alpha
			self.bet_rect.shadow= self.button_shadow
			self.inc_bet_node.add_child(self.bet_rect)
		
		#--- label nodes ---
		title_font = 'Hoefler Text'
		three_font = 'Bodoni 72'
		title_f_size = 37
		z_pos = 1
		
		self.layered_text('Card MONTE', title_font, title_f_size, self.size.w/2, self.size.h/2 * 1.76, 1, -1, 'black', 'black', 'white', parent=self)
		self.layered_text('3', three_font, title_f_size, self.size.w/2 *0.70, self.size.h/2 * 1.78, 1, -1, 'black', 'black', 'white', parent=self)

		self.stake_label = LabelNode(
			'Stakes', 
			font = ('Hoefler Text', 28), 
			position = (self.size.w * .11, self.size.h/2 * 1.79), 
			color= 'black',
			parent=self.main_node)
		
		self.stake_amount_label = LabelNode(
			f'{self.currency_type}{self.stake_amount:,}', 
			font = ('Bodoni 72', 28), 
			position = (self.size.w * .11, self.size.h/2 * 1.66),
			parent=self.main_node)		
		
		self.floating_stakes_label = LabelNode(
			f'{self.currency_type}{self.floating_stakes:,}', 
			font = ('Bodoni 72', 28), 
			position = (self.size.w * .11, self.size.h/2 * 1.66))	
			
		self.bankroll_label = LabelNode(
			'BankRoll', 
			font = ('Hoefler Text', 28), 
			position = (self.size.w/2 * 1.79, self.size.h/2 * 1.79), 
			color = 'black',
			parent=self.main_node)		
		
		self.bankroll_amount_label = LabelNode(
			f'{self.currency_type}{self.bankroll_amount:,}', 
			font = ('Bodoni 72', 28), 
			position = (self.size.w/2 * 1.79, self.size.h/2 * 1.66), 
			color = 'gold', 
			parent=self.main_node)		
	
		self.status_title_label = LabelNode(
			'Status', 
			font = ('Snell Roundhand', 16), 
			position = (self.size.w/2 * 1.68, self.size.h/2 * 1.51), 
			color = 'gold', 
			parent=self.main_node)
		
		self.status_title_label.rotation= 0.8

		self.status_label = LabelNode(
			f'{self.status}', 
			font = ('Hiragino Mincho ProN', 20), 
			position = (self.size.w/2 * 1.71, self.size.h/2 * 1.39), 
			color = 'gold', 
			anchor_point= (0.1, 0), 
			parent=self.main_node)
		
		self.button_font = 'Avenir Next Condensed Bold'		
					
		self.shuffle_btn = LabelNode(
			'SHUFFLE', 
			font = (self.button_font, 30), 
			position = (self.size.w/2 * 1.79, self.size.h/2 * 1.25), 
			parent=self.main_node)
		
		self.place_bet_label = LabelNode(
			'Place Bet', 
			font = (self.button_font, 28), 
			position = (self.size.w/2 * 1.79, self.size.h/2 * 0.30), 
			parent=self.main_node)

		self.inc_bet_0 = LabelNode(
			'+ bet', 
			(self.button_font, 30), 
			position=(self.size.w * .11, self.size.h * 0.545),
			color='black',
			parent=self.inc_bet_node)
			
		self.inc_bet = LabelNode(
			'+ bet', 
			(self.button_font, 30), 
			position=(self.size.w * .11, self.size.h * 0.55),
			parent=self.inc_bet_node)

		self.dec_bet_0 = LabelNode(
			'- bet', 
			font = (self.button_font, 30), 
			position = (self.size.w * .11, self.size.h * 0.345), 
			color='black',
			parent=self.dec_bet_node)

		self.dec_bet = LabelNode(
			'- bet', 
			font = (self.button_font, 30), 
			position = (self.size.w * .11, self.size.h * 0.35), 
			parent=self.dec_bet_node)

		multiplier_text = 'Bodoni 72'
		self.bet_multiplier = LabelNode(
			'BET MULTIPLIER', 
			font = ('Hoefler Text', 12), 
			position = (self.size.w/2 * 1.79, self.size.h/2 * 1.04), 
			parent=self.multiplier_node)

		self.two_multiplier = LabelNode(
			'2x', 
			font = (multiplier_text, 35), 
			position = (self.size.w/2 * 1.79, self.size.h/2 * 0.89), 
			alpha = 0.5, 
			parent=self.multiplier_node)
		
		self.five_multiplier = LabelNode(
			'5x', 
			font = (multiplier_text, 35), 
			position = (self.size.w/2 * 1.79, self.size.h/2 * 0.65), 
			alpha = 0.5, 
			parent=self.multiplier_node)
		
		#position marker
		pos_font = 'Baskerville'
		
		self.first_pos = self.layered_text('1st', pos_font, 40, self.size.w/2 * 0.55, self.size.h / 2 * 0.30, 1, -1, 'black', 'black', 'black', 'white', parent=self)
			
		self.second_pos = self.layered_text('2nd', pos_font, 40, self.size.w/2, self.size.h / 2 * 0.30, 1, -1, 'black', 'black', 'black', 'white',parent=self)
		
		self.third_pos = self.layered_text('3rd', pos_font, 40, self.size.w/2 * 1.45, self.size.h/2 * 0.30, 1, -1, 'black', 'black', 'black', 'white', parent=self)

		self.winner_text_1 = LabelNode(
			'WINNER!', 
			font = ('MarkerFelt-Wide', 30), 
			position = (self.size/2), 
			color = 'red')
		
		self.winner_text_2 = LabelNode(
			'WINNER!', 
			font = ('MarkerFelt-Wide', 30), 
			position = (self.size.w/2 + 1, self.size.h/2 -1), 
			color = 'white')
		
		#--- sprite nodes ---
		self.card_pos_1 = SpriteNode(
			self.back_of_card, 
			position = (self.size.w/2 * 0.55, self.size.h/2),
			scale=0.28,
			z_position=2,
			parent=self.main_node)
		
		self.card_pos_2 = SpriteNode(
			self.back_of_card, 
			position = (self.size/2),
			scale=0.28,
			z_position=2,
			parent=self.main_node)

		self.card_pos_3 = SpriteNode(
			self.back_of_card, 
			position = (self.size.w/2 * 1.45, self.size.h/2),
			scale=0.28,
			z_position=2,
			parent=self.main_node)		

		self.money_bags = [SpriteNode('emj:Money_Bag', position = (self.size.w/2 * 0.20 + i * random.randrange(15), self.size.h/2 * 0.30 + i * random.randrange(7)), scale=1, parent=self.main_node) for i in range(5)]
		
		self.dollar_bills = SpriteNode(
			'emj:Banknote', 
			position= (67,50), 
			parent=self.money_pile_node)	
						
		self.wing_money = SpriteNode(
			'emj:Money_With_Wings', 
			position= (self.size.w * .11, self.size.h/2 * 1.66),
			scale=0.25)
			
		self.info_btn = SpriteNode(
			'iow:information_circled_24',
			position=(self.size.w/2 * 0.48, self.size.h/2 * 1.75), 
			parent=self.main_node)
			
		self.all_in_btn = SpriteNode(
			'emj:High_Voltage_Sign',
			position =(self.size.w * .11, self.size.h * 0.70),
			scale= 0.75, 
			parent=self.main_node)
					
	def wooden_border(self):
		#wooden block border
		border = Node(parent=self)
		x = 0		
		while x <= self.size.w * 1.06:
			for i in (x, 0), (x, self.size.h * 1.06), (-6, x), (self.size.w+6, x):
				wood = SpriteNode(
					'plc:Wood_Block', 
					position = i,
					z_position= 1, 
					parent=border)
			x += 50
		
		for c in (self.size.w * 0.015, self.size.h * 0.015), (self.size.w * 0.015, self.size.h * 0.96), (self.size.w * 0.985, self.size.h * 0.98), (self.size.w * 1.003, self.size.h * .000):
			corner = SpriteNode(
				'plc:Wood_Block', 
				parent=border)
			corner.position = (c)		
			corner.rotation= 180				
						
	def ding_sound(self):
		sound.play_effect(
			'rpg:ClothBelt')
		sound.play_effect(
			'game:Ding_3')
		
	def update_br(self):
		self.bankroll_amount += self.stake_amount * 3
		self.bankroll_amount_label.text = f'{self.currency_type}{self.bankroll_amount:,}'
	
	def update_s_a_l(self):
		self.stake_amount = 0
		self.stake_amount_label.text = f'{self.currency_type}{self.stake_amount:,}'	

	def wing_money_sound(self):
		sound.play_effect('digital:ThreeTone1')	
		
	def layered_text(self, text, font, size, x, y, x_offset, y_offset, *colors, parent=None, **kwargs):
		colors = [*colors]
		for color in colors:
			name = LabelNode(
				text, 
				font = (font, size), 
				position = (x, y), 
				color = color,
				parent=self)	
			x += x_offset
			y += y_offset
					
	def scaling_text(self):				
		self.winner_text_1.run_action(
			A.repeat(
				A.sequence(
					A.scale_by(3, .5), 
					A.scale_to(0, 1)), 0))

		self.winner_text_2.run_action(
			A.repeat(
				A.sequence(
					A.scale_by(3, .5),
					A.scale_to(0, 1)), 0))
	
	def	start_bets(self):
		self.allow_bets = True
							
	def update(self):
		for key, value in self.status_dict.items():
			if key <= self.bankroll_amount:
				self.status = value
				self.status_label.text = f'{self.status}'
	
		if self.bankroll_amount == 0 and self.stake_amount == 0:
			self.main_node.run_action(A.fade_to(0, 1))
			go = GameOver()
			go.main = self
			self.present_modal_scene(go)	
						
	def touch_began(self, touch):
		#--- inc bet button ---
		if touch.location in self.inc_bet.frame and self.allow_bets == True:
			self.inc_bet.font = (self.button_font, 35)
			self.inc_bet_0.font = (self.button_font, 35)
			
			if self.bankroll_amount == 0:
				pass
				
			elif self.five_multiplier_active == True:
				if self.bankroll_amount < 500:
					self.five_multiplier_active = False
					self.five_rect.stroke_color = '#3b5e3c'
					self.five_multiplier.alpha = 0.5
					self.stake_amount += self.bankroll_amount
					self.bankroll_amount -= self.bankroll_amount
					self.stake_amount_label.text = f'{self.currency_type}{self.stake_amount:,}'
					self.bankroll_amount_label.text = f'{self.currency_type}{self.bankroll_amount:,}'
					sound.play_effect('casino:ChipsStack3')		
							
				else:
					self.stake_amount += 500
					self.stake_amount_label.text = f'{self.currency_type}{self.stake_amount:,}'
					self.bankroll_amount -= 500
					if self.bankroll_amount < 0:
						self.bankroll_amount = 0
					self.bankroll_amount_label.text = f'{self.currency_type}{self.bankroll_amount:,}'
					sound.play_effect('casino:ChipsStack3')		
		
			elif self.two_multiplier_active == True:
				if self.bankroll_amount < 200:
					self.two_multiplier_active = False
					self.two_rect.stroke_color = '#3b5e3c'
					self.two_multiplier.alpha = 0.5
					self.stake_amount += self.bankroll_amount
					self.bankroll_amount -= self.bankroll_amount
					self.stake_amount_label.text = f'{self.currency_type}{self.stake_amount:,}'
					self.bankroll_amount_label.text = f'{self.currency_type}{self.bankroll_amount:,}'
					sound.play_effect('casino:ChipsStack3')	
						
				else:
					self.stake_amount += 200
					self.stake_amount_label.text = f'{self.currency_type}{self.stake_amount:,}'
					self.bankroll_amount -= 200
					if self.bankroll_amount < 0:
						self.bankroll_amount = 0
					self.bankroll_amount_label.text = f'{self.currency_type}{self.bankroll_amount:,}'
					sound.play_effect('casino:ChipsStack3')
				
			else:
				self.stake_amount += 100
				self.stake_amount_label.text = f'{self.currency_type}{self.stake_amount:,}'
				self.bankroll_amount -= 100
				if self.bankroll_amount < 0:
					self.bankroll_amount = 0
				self.bankroll_amount_label.text = f'{self.currency_type}{self.bankroll_amount:,}'
				sound.play_effect('casino:ChipsStack3')

		#--- dec bet button ---						
		if touch.location in self.dec_bet.frame and self.allow_bets == True:
			self.dec_bet.font = (self.button_font, 35)
			self.dec_bet_0.font = (self.button_font, 35)	
					
			if self.stake_amount == 0:
				pass

			elif self.five_multiplier_active == True and self.stake_amount >= 500:
				self.stake_amount -= 500
				self.stake_amount_label.text = f'{self.currency_type}{self.stake_amount:,}'
				self.bankroll_amount += 500
				if self.bankroll_amount < 0:
					self.bankroll_amount = 0
				self.bankroll_amount_label.text = f'{self.currency_type}{self.bankroll_amount:,}'	
				sound.play_effect('casino:ChipsStack2')	
				
			elif self.two_multiplier_active == True and self.stake_amount >= 200:
				self.stake_amount -= 200
				self.stake_amount_label.text = f'{self.currency_type}{self.stake_amount:,}'
				self.bankroll_amount += 200
				if self.bankroll_amount < 0:
					self.bankroll_amount = 0
				self.bankroll_amount_label.text = f'{self.currency_type}{self.bankroll_amount:,}'
				sound.play_effect('casino:ChipsStack2')
				
			else:
				self.stake_amount -= 100
				self.stake_amount_label.text = f'{self.currency_type}{self.stake_amount:,}'
				self.bankroll_amount += 100
				if self.bankroll_amount < 0:
					self.bankroll_amount = 0
				self.bankroll_amount_label.text = f'{self.currency_type}{self.bankroll_amount:,}'
				sound.play_effect('casino:ChipsStack2')
		
		#--- bet multipliers ---		
		if touch.location in self.five_multiplier.frame:
			if self.five_multiplier.alpha == 1:
				self.five_rect.stroke_color = '#3b5e3c'
				self.five_multiplier.alpha = 0.5
				self.five_multiplier_active = False
				sound.play_effect('ui:switch11', pitch = 3)
				
			else:
				self.five_rect.stroke_color = 'red'
				self.five_multiplier.alpha = 1
				self.five_multiplier_active = True
				self.two_multiplier_active = False
				self.two_multiplier.alpha = .5
				self.two_rect.stroke_color = '#3b5e3c'
				sound.play_effect('ui:switch11', pitch = 3)
				
		if touch.location in self.two_multiplier.frame:
			if self.two_multiplier.alpha == 1:
				sound.play_effect('ui:switch11', pitch = 3)
				self.two_rect.stroke_color = '#3b5e3c'
				self.two_multiplier.alpha = 0.5
				self.two_multiplier_active = False
				
			else:
				sound.play_effect('ui:switch11', pitch = 3)
				self.two_rect.stroke_color = 'red'
				self.two_multiplier.alpha = 1
				self.two_multiplier_active = True
				self.five_multiplier_active = False
				self.five_multiplier.alpha = 0.5
				self.five_rect.stroke_color = '#3b5e3c'
				
		#----flips cards ----
		# reveal 1st card
		if touch.location in self.card_pos_1.frame and self.reveal == True:
			self.card_pos_1.remove_from_parent()
			self.card_pos_1 = SpriteNode(
				self.cards[0], 
				position = (self.size.w/2 * 0.55, self.size.h/2),
				x_scale=0.28,
				y_scale=0.27,
				parent=self.main_node)
			self.card_pos_1.alpha=0.5
			self.card_pos_1.run_action(A.sequence(A.group(A.fade_to(1, 0.3), A.scale_to(0.35, 0.25)), A.scale_to(0.28, 0.25)))
			
			self.floating_stakes = self.stake_amount
			self.reveal = False		
			self.shuffle_active = True
			self.place_bet = False
			self.place_bet_rect.color = '#25430e'
						
			if self.cards[0] == 'ace_of_spades.png':
				sound.play_effect('casino:CardShove2')			
				self.add_child(self.winner_text_1)
				self.add_child(self.winner_text_2)
				self.scaling_text()
				self.floating_stakes_label.position = (self.size.w * .11, self.size.h/2 * 1.66)
				self.add_child(self.floating_stakes_label)
				self.floating_stakes_label.run_action(
					A.sequence(
						A.scale_by(0.5, 1), 
						A.move_to(self.size.w/2 * 1.79, self.size.h/2 * 1.66, 3), 
						A.scale_to(0, 1), 
						A.fade_to(0, 1), 
						A.move_to(self.size.w * .11, self.size.h/2 * 1.66), 
						A.scale_to(1, 1)))
				self.stake_amount_label.run_action(A.fade_to(0, 3))
				self.bankroll_amount_label.run_action(
					A.sequence(
						A.wait(5), 
						A.fade_to(0, 0.5), 
						A.call(self.update_br), 
						A.wait(1), 
						A.call(self.ding_sound), 
						A.fade_to(1, 1.75)))		
				#action allows betting
				self.stake_amount_label.run_action(
					A.sequence(
						A.wait(6.5),
						A.call(self.update_s_a_l),
						A.fade_to(1, 2), A.call(self.start_bets)))
							
			else:
				self.stake_amount_label.run_action(
					A.sequence(
						A.fade_to(0), 
						A.call(self.update_s_a_l),
						A.wait(3),
						A.fade_to(1,2, TIMING_SINODIAL)))
				self.stake_amount_label.text = f'{self.currency_type}{self.stake_amount:,}'
				self.floating_stakes_label.remove_from_parent()
				sound.play_effect('game:Error', volume=.18)
				self.wing_money.alpha=0.01
				self.wing_money.scale=0.25
				self.wing_money.position=(self.size.w * 0.11, self.size.h/2 * 1.66)
				self.add_child(self.wing_money)
				self.wing_money.run_action(
					A.sequence(
						A.fade_to(0.80),
						A.group(
							A.fade_to(0, 5, TIMING_EASE_IN_2),
							A.scale_to(1, 6), 
							A.move_by(0,40, 5))))
			
		# reveal 2nd card	
		if touch.location in self.card_pos_2.frame and self.reveal == True:
			self.floating_stakes = self.stake_amount
			self.card_pos_2.remove_from_parent()
			self.card_pos_2 = SpriteNode(
				self.cards[1], 
				position = (self.size/2),
				x_scale=0.28,
				y_scale=0.27,
				parent=self.main_node)
			self.reveal = False		
			self.shuffle_active = True
			self.place_bet = False
			self.place_bet_rect.color = '#25430e'
			
			self.card_pos_2.alpha=0.5
			self.card_pos_2.run_action(A.sequence(A.group(A.fade_to(1, 0.3), A.scale_to(0.35, 0.25)), A.scale_to(0.28, 0.25)))			
			if self.cards[1] == 'ace_of_spades.png':
				sound.play_effect('casino:CardShove2')			
				self.add_child(self.winner_text_1)
				self.add_child(self.winner_text_2)

				self.scaling_text()
			
				self.floating_stakes_label.position = (self.size.w * .11, self.size.h/2 * 1.66)
				self.add_child(self.floating_stakes_label)
				self.floating_stakes_label.run_action(
					A.sequence(
						A.scale_by(0.5, 1), 
						A.move_to(self.size.w/2 * 1.79, self.size.h/2 * 1.66, 3), 
						A.scale_to(0, 1), 
						A.fade_to(0, 1), 
						A.move_to(self.size.w * .11, self.size.h/2 * 1.66), 
						A.scale_to(1, 1)))
				
				self.stake_amount_label.run_action(A.fade_to(0, 3))
				
				self.bankroll_amount_label.run_action(
					A.sequence(
						A.wait(5), 
						A.fade_to(0, 0.5), 
						A.call(self.update_br), 
						A.wait(1), 
						A.call(self.ding_sound), 
						A.fade_to(1, 1.75)))
						
				#actiom allows betting		
				self.stake_amount_label.run_action(
					A.sequence(
						A.wait(6.5),
						A.call(self.update_s_a_l),
						A.fade_to(1, 2), A.call(self.start_bets)))
							
			else:
				self.stake_amount_label.run_action(
					A.sequence(
						A.fade_to(0), 
						A.call(self.update_s_a_l),
						A.wait(3),
						A.fade_to(1,2, TIMING_SINODIAL)))
				
				self.stake_amount_label.text = f'{self.currency_type}{self.stake_amount:,}'
				self.floating_stakes_label.remove_from_parent()
				sound.play_effect('game:Error', volume=.18)
				self.wing_money.alpha=0.01
				self.wing_money.scale=0.25
				self.wing_money.position=(self.size.w * 0.11, self.size.h/2 * 1.66)
				self.add_child(self.wing_money)
		
				self.wing_money.run_action(
					A.sequence(
						A.fade_to(0.80),
						A.group(
							A.fade_to(0, 5, TIMING_EASE_IN_2),
							A.scale_to(1, 6), 
							A.move_by(0,40, 5))))
			
		# reveal 3rd card								
		if touch.location in self.card_pos_3.frame and self.reveal == True:
			self.floating_stakes = self.stake_amount
			self.card_pos_3.remove_from_parent()
			self.card_pos_3 = SpriteNode(
				self.cards[2], 
				position = (self.size.w/2 * 1.45, self.size.h/2),
				x_scale=0.28,
				y_scale=0.27,
				parent=self.main_node)
			self.reveal = False		
			self.shuffle_active = True
			self.place_bet = False
			self.place_bet_rect.color = '#25430e'
			
			self.card_pos_3.alpha=0.5
			self.card_pos_3.run_action(A.sequence(A.group(A.fade_to(1, 0.3), A.scale_to(0.35, 0.25)), A.scale_to(0.28, 0.25)))
						
			if self.cards[2] == 'ace_of_spades.png':
				sound.play_effect('casino:CardShove2')			
				self.add_child(self.winner_text_1)
				self.add_child(self.winner_text_2)
				self.scaling_text()			
				self.floating_stakes_label.position = (self.size.w * .11, self.size.h/2 * 1.66)
				self.add_child(self.floating_stakes_label)
				self.floating_stakes_label.run_action(
					A.sequence(
						A.scale_by(0.5, 1), 
						A.move_to(self.size.w/2 * 1.79, self.size.h/2 * 1.66, 3), 
						A.scale_to(0, 1), 
						A.fade_to(0, 1), 
						A.move_to(self.size.w * .11, self.size.h/2 * 1.66), 
						A.scale_to(1, 1)))				
				self.stake_amount_label.run_action(A.fade_to(0, 3))				
				self.bankroll_amount_label.run_action(
					A.sequence(
						A.wait(5), 
						A.fade_to(0, 0.5), 
						A.call(self.update_br), 
						A.wait(1), 
						A.call(self.ding_sound), 
						A.fade_to(1, 1.75)))						
				#action allows betting
				self.stake_amount_label.run_action(
					A.sequence(
						A.wait(6.5),
						A.call(self.update_s_a_l),
						A.fade_to(1, 2), A.call(self.start_bets)))
							
			else:
				self.stake_amount_label.run_action(
					A.sequence(
						A.fade_to(0), 
						A.call(self.update_s_a_l),
						A.wait(3),
						A.fade_to(1,2, TIMING_SINODIAL)))				
				self.stake_amount_label.text = f'{self.currency_type}{self.stake_amount:,}'
				self.floating_stakes_label.remove_from_parent()
				sound.play_effect('game:Error', volume=.18)
				self.wing_money.alpha=0.01
				self.wing_money.scale=0.25
				self.wing_money.position=(self.size.w * 0.11, self.size.h/2 * 1.66)
				self.add_child(self.wing_money)		
				self.wing_money.run_action(
					A.sequence(
						A.fade_to(0.80),
						A.group(
							A.fade_to(0, 5, TIMING_EASE_IN_2),
							A.scale_to(1, 6), 
							A.move_by(0,40, 5))))	
			
		#--- shuffle button ---
		if touch.location in self.shuffle_btn.frame and self.shuffle_active == True:
			self.shuffle_active = False
			self.place_bet = True	
			self.shuffle_rect.alpha = 0.1					
			self.winner_text_1.remove_from_parent()
			self.winner_text_2.remove_from_parent()	
			self.card_pos_1.remove_from_parent()
			self.card_pos_2.remove_from_parent()
			self.card_pos_3.remove_from_parent()
			random.shuffle(self.cards)
			random.shuffle(self.cards)
			random.shuffle(self.cards)
			sound.play_effect('casino:CardShuffle', 0.3)

			self.card_pos_1 = SpriteNode(
				self.back_of_card, 
				position = (self.size.w/2 * 0.55, self.size.h/2),
				scale=0.28,
				parent=self.main_node)			
			
			self.card_pos_2 = SpriteNode(
				self.back_of_card, 
				position = (self.size/2),
				scale=0.28,
				parent=self.main_node)
			
			self.card_pos_3 = SpriteNode(
				self.back_of_card, 
				position = (self.size.w/2 * 1.45, self.size.h/2),
				scale=0.28,
				parent=self.main_node)

			move_to_1 = A.move_to(self.size.w/2 * 0.55, self.size.h/2)
			move_to_2 = A.move_to(self.size.w/2, self.size.h/2)
			move_to_3 = A.move_to(self.size.w/2 * 1.45, self.size.h/2)
			
			self.card_pos_1.run_action(
				A.sequence(
					move_to_2, 
					move_to_2, 
					move_to_1, 
					move_to_3,
					move_to_2,
					move_to_1))

			self.card_pos_2.run_action(
				A.sequence(
					move_to_3, 
					move_to_2, 
					move_to_3, 
					move_to_2,
					move_to_2,
					move_to_2))
	
			self.card_pos_3.run_action(
				A.sequence(
					move_to_2, 
					move_to_2, 
					move_to_1, 
					move_to_2,
					move_to_2,
					move_to_3))
							
		#--- place bet button ---
		if touch.location in self.place_bet_label.frame and self.place_bet == True and self.stake_amount != 0:		
			self.reveal = True
			self.place_bet = False
			self.allow_bets = False
			self.shuffle_active = False
			self.place_bet_label.text = "Bet Placed"
			self.place_bet_rect.color = 'red'
			self.floating_stakes_label.run_action(Action.fade_to(1, 1))
			self.floating_stakes_label.text = f'{self.currency_type}{self.stake_amount:,}'
			sound.play_effect('rpg:MetalClick', pitch=2, volume= .5)

		#--- info button ---	
		if touch.location in self.info_btn.frame:
			rl = Rules()
			rl.main = self
			self.present_modal_scene(rl)

		#--- all in button ---
		if touch.location in self.all_in_btn.frame and self.bankroll_amount != 0 and self.allow_bets == True:
			self.all_in_btn.scale=0.90
			self.stake_amount += self.bankroll_amount
			self.bankroll_amount = 0
			self.stake_amount_label.text = f'{self.currency_type}{self.stake_amount:,}'
			self.bankroll_amount_label.text = f'{self.currency_type}{abs(self.bankroll_amount):,}'
							
	def touch_ended(self, touch):
		self.shuffle_rect.alpha = 1
		self.all_in_btn.scale=0.75
		self.inc_bet.font = (self.button_font, 30)
		self.inc_bet_0.font = (self.button_font, 30)		
		self.dec_bet.font = (self.button_font, 30)
		self.dec_bet_0.font = (self.button_font, 30)
		
	def pause(self):
		sound.stop_all_effects()	
		
	def resume(self):
		bg_music = sound.play_effect('3CardBeat.wav', volume=0.25)
		bg_music.looping = True
		
	def stop(self):
		sound.stop_all_effects()
		
main= Main()
if __name__ == '__main__':
	run(main, LANDSCAPE, show_fps=False)


	





