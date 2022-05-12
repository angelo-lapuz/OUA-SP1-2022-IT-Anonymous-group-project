import pygame
from player import *
from enemy_class import *
import Spells

font = pygame.freetype.Font(pygame.font.match_font("calibiri"), 26)

battle_status = False
player = object
enemy = object
map_code = int
answer_pos = []
active_spell = None
sucessful_cast = None
answer = None
current_spell = None
spell_pos = []
spells = []
answer_list = []
turn = 'player'


class battle:
    def __init__(self):

        self.player = object
        self.enemy = object
        self.loot = None
        self.turn = 'player'
        self.result = False
        self.keys = pygame.key.get_pressed()

        self.Math_spell = Spells.math_spell()
        self.Spelling_spell = Spells.spelling_spell()
        self.guess_spell = Spells.guess_spell()
        self.gen_spell = Spells.general_spell()

        self.screen = pygame.display.get_surface()
        self.load_img()
        self.question_details = None
        self.question = None
        self.answer_list = [None]
        self.player_answer = None

        self.spells = []

        self.screen = pygame.display.get_surface()

    def set_battle(self, player1, enemy1, map_num):
        global player, enemy, map_code

        player = player1
        enemy = enemy1
        map_code = map_num

    def set_battle_status(self, status):
        global battle_status
        battle_status = status

    def get_battle_status(self):
        global battle_status
        return battle_status

    def end_battle(self):
        global active_spell, sucessful_cast, answer, answer_list, spell_pos, spells, current_spell
        global battle_status

        battle_status = False
        self.question_details = None
        self.question = None
        self.answer_list = [None]
        self.player_answer = None
        active_spell = None
        sucessful_cast = None
        answer = None
        current_spell = None
        spell_pos = []
        spells = []
        answer_list = []

        self.set_battle_loot(enemy.get_loot())
        pygame.sprite.Sprite.kill(enemy)

        self.set_result(True)

        # will shove enemy to 0:0
        enemy.set_enemy_pos()

    def set_battle_loot(self, loot):
        loot_list = list(loot)
        player_known = player.get_player_learned_spells()
        while loot_list[0] in player_known:
            loot_list[0] = random.randrange(0, 9, 1)

        self.loot = loot_list

    def get_battle_loot(self):
        return self.loot

    def get_result(self):
        return self.result

    def set_result(self, result):
        self.result = result

    def reset_question(self):
        self.question_details = None
        self.question = None
        self.answer_list = [None]
        self.player_answer = None
        active_spell = None
        sucessful_cast = None
        answer = None
        current_spell = None
        spell_pos = []
        spells = []
        answer_list = []

    def draw_battle(self):
        global answer_pos, answer, spell_pos, current_spell, turn

        self.x = 400
        self.y = 580
        self.spell_x = 400
        self.spell_y = 580
        self.screen.blit(pygame.image.load('../graphics/maps/' + str(map_code) + '/battle_scene.png').convert_alpha(),
                         (0, 0))
        self.screen.blit(player.get_player_image(), (450, 550))
        self.screen.blit(enemy.get_enemy_image(), (500, 500))

        self.screen.blit(self.battle_ui, (0, 0))
        self.screen.blit(self.spell_button, (20, 400))
        self.screen.blit(self.inven_button, (20, 300))
        self.screen.blit(self.battle_ui_buttom, (5, 480))

        if sucessful_cast:
            text_surface, rect = font.render(str("sucessfully cast " + str(current_spell)), (0, 0, 0))
            self.screen.blit(text_surface, (250, 200))

        if not sucessful_cast:
            if sucessful_cast is None:
                ""
            else:
                text_surface, rect = font.render(str("Failed to cast " + str(current_spell)), (0, 0, 0))
                self.screen.blit(text_surface, (250, 200))

        if turn == 'player':
            if not current_spell:
                self.spells = player.get_player_spells()
                i = 0
                for spell in self.spells:
                    if self.spells[spell]["learnt"]:
                        self.screen.blit(self.spell_slot, (self.spell_x, self.spell_y))
                        self.screen.blit(self.spells[spell]["img"], (self.spell_x + 20, self.spell_y + 15))
                        if len(spell_pos) < len(self.spells):
                            spell_pos.append((self.spell_x, self.spell_y))
                        self.spell_x += 108

            else:
                if self.question_details is None:
                    self.question_details = self.Math_spell.make_question()
                    self.question = self.question_details[0]
                    self.answer_list = self.question_details[1]
                i = 0
                for answer in self.answer_list:

                    text_surface, rect = font.render(str(self.question), (0, 0, 0))
                    self.screen.blit(text_surface, (400, 500))

                    self.screen.blit(self.answer_button, (self.x, self.y))

                    text_surface, rect = font.render(str(answer), (0, 0, 0))
                    self.screen.blit(text_surface, (self.x + 5, self.y + 5))

                    if len(answer_pos) <= len(self.answer_list):
                        answer_rect = self.answer_button.get_rect()
                        answer_pos.append((self.x, self.y))
                        i += 1
                    self.x += 150
            self.player_turn()

    def player_turn(self):
        global sucessful_cast, answer, current_spell
        result = None

        if pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()
            if current_spell is not None:
                user_choice = self.get_user_selection(mouse_pos, 0)

                if user_choice is not None:
                    result = self.check_answer(user_choice)
                    if result:
                        sucessful_cast = True
                        self.reset_question()
                    else:
                        sucessful_cast = False
                        self.reset_question()

                self.enemy_turn()

            elif current_spell is None:
                user_choice = self.get_user_selection(mouse_pos, 1)
                print(user_choice)
                spells_tmp = player.get_player_spells()
                print(spells_tmp)

                for spell in spells_tmp:
                    if spells_tmp[spell]["learnt"]:
                        spells.append(spell)

                current_spell = spells[user_choice]

    def get_question(self):
        global active_spell
        selection = 0

        if selection == 0:
            active_spell = 'math'

            question = self.Math_spell()
        elif selection == 1:
            print("true or false")
        elif selection == 2:
            print("spelling")
        else:
            print("geography")

        return question

    def enemy_turn(self):
        print("AAA")

    def check_answer(self, user_answer):
        global active_spell



        response = self.Math_spell.check_question(user_answer)

        return response

    def get_user_selection(self, mouse_pos, type):

        if type == 0:

            answers_pos = self.get_answer_pos()
        else:

            answers_pos = self.get_spell_pos()

        i = 0
        match = None
        for answer in answers_pos:

            item_pos_x = answers_pos[i][0]
            item_pos_y = answers_pos[i][1]

            if abs((((((item_pos_x + 126) - item_pos_x) / 2) + item_pos_x) - mouse_pos[0])) <= 30 and abs(
                    (((((item_pos_y + 79) - item_pos_y) / 2) + item_pos_y) - mouse_pos[1])) <= 30:
                match = i
            else:
                i += 1
        return match

    def get_answer_pos(self):
        global answer_pos

        return answer_pos

    def get_spell_pos(self):
        global spell_pos

        return spell_pos

    def load_img(self):
        self.answer_button = pygame.image.load('../graphics/battle/question_slot.png').convert_alpha()
        self.spell_button = pygame.image.load('../graphics/battle/spells_button.png').convert_alpha()
        self.inven_button = pygame.image.load('../graphics/battle/inven_button.png').convert_alpha()
        self.battle_ui = pygame.image.load('../graphics/battle/battle_ui.png').convert_alpha()
        self.battle_ui_buttom = pygame.image.load('../graphics/battle/battle_ui_bottom.png').convert_alpha()
        self.spell_slot = pygame.image.load('../graphics/inventory/Spell_box.png').convert_alpha()
