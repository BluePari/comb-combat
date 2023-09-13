import random


class Settings:
    def __init__(self):
        self.damage_rate_table = {
            2: {1: 0.51, 4: 0.57, 5: 0.64, 6: 0.71, 7: 0.8, 9: 0.89, 10: 0.99, 11: 1},
            3: {1: 0.61, 4: 0.65, 5: 0.7, 6: 0.76, 7: 0.81, 9: 0.88, 10: 0.94, 11: 1},
            4: {1: 0.72, 4: 0.76, 5: 0.8, 6: 0.85, 7: 0.89, 9: 0.94, 10: 1},
            5: {1: 0.85, 4: 0.88, 5: 0.92, 6: 0.97, 7: 1},
        }

    def get_damage_rate(self, player_num, turn):
        if (
            player_num in self.damage_rate_table
            and turn in self.damage_rate_table[player_num]
        ):
            return self.damage_rate_table[player_num][turn]
        else:
            return None


class Player:
    def __init__(self, username, serial_number):
        self.username = username
        self.serial_number = serial_number
        self.chessboard = [None] * 60
        self.chessboard_to_show = ["___"] * 20
        self.health = 150
        self.score = 0

    def place_piece(self, position, chess):
        piece = [int(num) for num in chess]
        self.chessboard[position] = piece[-3]
        self.chessboard[position + 20] = piece[-2]
        self.chessboard[position + 40] = piece[-1]
        if chess == "1000":
            self.chessboard_to_show[position] = "any"
        else:
            self.chessboard_to_show[position] = str(chess)
        score_delta = self.check_score()
        if score_delta:
            print(f"玩家{self.username}设置成功，获得了{score_delta}点积分")
        else:
            print(f"玩家{self.username}设置成功")

    def check_score(self):
        score = 0

        lines = [
            [8, 13, 17],
            [4, 9, 14, 18],
            [1, 5, 10, 15, 19],
            [2, 6, 11, 16],
            [3, 7, 12],
            [21, 22, 23],
            [24, 25, 26, 27],
            [28, 29, 30, 31, 32],
            [33, 34, 35, 36],
            [37, 38, 39],
            [41, 44, 48],
            [42, 45, 49, 53],
            [43, 46, 50, 54, 57],
            [47, 51, 55, 58],
            [52, 56, 59],
        ]

        for line in lines:
            unique_elements = {self.chessboard[num] for num in line}
            if None in unique_elements:
                continue
            if len(unique_elements) == 1 or (
                len(unique_elements) == 2 and 0 in unique_elements
            ):
                score += sum(len(line) * piece for piece in unique_elements)

        old_score = self.score
        self.score = score
        return score - old_score


class Game:
    def __init__(self, settings):
        self.settings = settings
        self.player_list = []
        self.player_data = []
        self.alive_players = []
        self.inactive_players = []
        self.card_pool1 = [
            num1 + num2 + num3 for num1 in "348" for num2 in "159" for num3 in "267"
        ] * 2
        self.card_pool2 = self.card_pool1[:]
        self.card_pool2.extend(["1000"] * 2)
        self.turn = 0
        self.damage_rate = 1

    def get_command(self):
        return input("请输入控制指令")

    def get_player_input(self):
        player = input("输入指令的玩家是")
        player_input = input("请输入游戏指令")
        return (player, player_input)

    def check_player(self, player):
        if not player.isdigit():
            print("系统错误：接收错误的玩家信息")
            return False
        player = int(player)
        if player >= len(self.player_data):
            print("系统错误：玩家序号超出范围")
            return False
        if self.player_data[player].username not in self.inactive_players:
            print("不要耍赖")
            return False
        return True

    def check_position(self, position):
        if not position.isdigit():
            print("游戏指令输入错误：请输入纯数字")
            return False
        position = int(position)
        if position > 20:
            print("游戏指令输入错误：超出棋盘范围")
            return False
        return True

    def check_card_and_position(self, card_and_position, max_card):
        if len(card_and_position) != 2:
            print("游戏指令输入错误：请输入卡牌序号和位置")
            return False
        if not all(element.isdigit() for element in card_and_position):
            print("游戏指令输入错误：请输入纯数字")
            return False
        card = int(card_and_position[0])
        position = int(card_and_position[1])
        if card >= max_card:
            print("游戏指令输入错误：超出选卡范围")
            return False
        if position > 20:
            print("游戏指令输入错误：超出棋盘范围")
            return False
        return True

    def show_game_status(self):
        for player in self.player_data:
            print(player.serial_number, player.username)
            print("        |{}|".format(player.chessboard_to_show[8]))
            print(
                "    |{}|   |{}|".format(
                    player.chessboard_to_show[4], player.chessboard_to_show[13]
                )
            )
            print(
                "|{}|   |{}|   |{}|".format(
                    player.chessboard_to_show[1],
                    player.chessboard_to_show[9],
                    player.chessboard_to_show[17],
                )
            )
            print(
                "    |{}|   |{}|".format(
                    player.chessboard_to_show[5], player.chessboard_to_show[14]
                )
            )
            print(
                "|{}|   |{}|   |{}|".format(
                    player.chessboard_to_show[2],
                    player.chessboard_to_show[10],
                    player.chessboard_to_show[18],
                )
            )
            print(
                "    |{}|   |{}|".format(
                    player.chessboard_to_show[6], player.chessboard_to_show[15]
                )
            )
            print(
                "|{}|   |{}|   |{}|".format(
                    player.chessboard_to_show[3],
                    player.chessboard_to_show[11],
                    player.chessboard_to_show[19],
                )
            )
            print(
                "    |{}|   |{}|".format(
                    player.chessboard_to_show[7], player.chessboard_to_show[16]
                )
            )
            print("        |{}|".format(player.chessboard_to_show[12]))
            print(f"血量：{player.health}, 得分：{player.score}")

    def check_sum_difference(self, card1, card2):
        if (
            abs(sum(int(num1) for num1 in card1) - sum(int(num2) for num2 in card2))
            <= 4
        ):
            return True
        return False

    def get_cards(self):
        card_list = []
        if self.turn == 1:
            attempted_cards = []
            while not len(card_list) == len(self.alive_players):
                attempted_cards.append(
                    self.card_pool1.pop(random.randint(0, len(self.card_pool1) - 1))
                )
                if (not card_list) or all(
                    self.check_sum_difference(attempted_cards[-1], card)
                    for card in card_list
                ):
                    card_list.append(attempted_cards.pop())
            self.card_pool1.extend(attempted_cards)
        elif self.turn % 7 == 1:
            for i in range(len(self.alive_players) + 1):
                card_list.append(
                    self.card_pool1.pop(random.randint(0, len(self.card_pool1) - 1))
                )
        else:
            card_list.append(
                self.card_pool2.pop(random.randint(0, len(self.card_pool2) - 1))
            )
        return card_list

    def show_card_list(self, card_list):
        for index, card in enumerate(card_list):
            print(index, card, end=";")
        print()

    def card_place_phase(self):
        print(f"第{self.turn}回合开始")
        print(f"伤害倍率：{self.damage_rate}")
        if self.turn == 1:
            self.inactive_players = self.alive_players[:]
            print("初始回合，每个人随机获得一张牌")
            self.show_game_status()
            card_list = self.get_cards()
            self.show_card_list(card_list)
            while self.inactive_players:
                player_input = self.get_player_input()
                player = player_input[0]
                position = player_input[1]
                if self.check_player(player) and self.check_position(position):
                    player = int(player)
                    position = int(position)
                    self.player_data[player].place_piece(position, card_list[player])
                    self.inactive_players.remove(self.player_list[player])
        elif self.turn % 7 == 1:
            print("公共选牌阶段，按照血量顺序选牌")
            card_list = self.get_cards()
            sorted_players = sorted(
                self.alive_players,
                key=lambda username: (
                    self.player_dict[username].health,
                    self.player_dict[username].score,
                    self.player_dict[username].serial_number,
                ),
            )
            for sorted_player in sorted_players:
                self.show_game_status()

                self.inactive_players.append(sorted_player)
                print(f"轮到玩家{sorted_player}选择")
                while self.inactive_players:
                    self.show_card_list(card_list)
                    print()
                    player_input = self.get_player_input()
                    player = player_input[0]
                    card_and_position = player_input[1].split()
                    if self.check_player(player) and self.check_card_and_position(
                        card_and_position, len(card_list)
                    ):
                        player = int(player)
                        card = int(card_and_position[0])
                        position = int(card_and_position[1])
                        self.player_data[player].place_piece(
                            position, card_list.pop(card)
                        )
                        self.inactive_players.pop()
        else:
            self.inactive_players = self.alive_players[:]
            self.show_game_status()
            card_list = self.get_cards()
            self.show_card_list(card_list)
            while self.inactive_players:
                player_input = self.get_player_input()
                player = player_input[0]
                position = player_input[1]
                if self.check_player(player) and self.check_position(position):
                    player = int(player)
                    position = int(position)
                    self.player_data[player].place_piece(position, card_list[0])
                    self.inactive_players.remove(self.player_list[player])

    def is_dead(self, player):
        if self.player_dict[player].health <= 0:
            print(f"{player}已被淘汰")
            self.alive_players.remove(player)

    def battle(self, player1, player2, mirror=False):
        delta = int(
            (self.player_dict[player1].score - self.player_dict[player2].score)
            * self.damage_rate
        )
        player1_info = ""
        player2_info = ""
        if mirror:
            player2_info = "(镜像)"
        else:
            if delta == 0:
                player2_info = "(0)"
            if delta > 0:
                player2_info = "({})".format(-delta)
                self.player_dict[player2].health -= delta
        if delta < 0:
            player1_info = "({})".format(delta)
            self.player_dict[player1].health += delta
        print(("{}{} vs {}{}").format(player1, player1_info, player2, player2_info))
        self.is_dead(player1)
        self.is_dead(player2)

    def battle_phase(self):
        if self.turn % 7 == 1 or self.turn == 2:
            print("本轮不进行玩家对战")
        else:
            pairs = self.alive_players[:]
            random.shuffle(pairs)
            if len(pairs) % 2:
                battle_with_mirror = pairs.pop()
                self.battle(battle_with_mirror, random.choice(pairs), True)
            for i in range(0, len(pairs), 2):
                self.battle(pairs[i], pairs[i + 1])

    def waiting_for_players(self):
        while True:
            command = self.get_command()
            if command.startswith("#join"):
                if len(self.player_list) > 12:
                    print("控制指令输入错误：人满啦")
                else:
                    player = command.split()[1]
                    if player in self.player_list:
                        print("控制指令输入错误：重复的用户名")
                        continue
                    else:
                        self.player_list.append(player)
                        print(f"玩家{player}加入了游戏，目前一共有{len(self.player_list)}人")
            elif command.startswith("#quit"):
                player = command.split()[1]
                if player in self.player_list:
                    self.player_list.remove(player)
                    print(f"玩家{player}退出了游戏，目前一共有{len(self.player_list)}人")
                else:
                    print("控制指令输入错误：这个玩家根本没加入游戏啊")

            elif command.startswith("#start"):
                if len(self.player_list) < 2:
                    print("控制指令输入错误：人数不足，至少需要2人")
                else:
                    break

    def start(self):
        if len(self.player_list) < 2:
            print("人数不足，启动失败")
            return
        random.shuffle(self.player_list)
        for index, username in enumerate(self.player_list):
            self.player_data.append(Player(username, index))
        self.player_dict = {p.username: p for p in self.player_data}
        self.alive_players = self.player_list[:]
        while len(self.alive_players) != 1:
            self.turn += 1
            if self.settings.get_damage_rate(len(self.player_list), self.turn):
                self.damage_rate = self.settings.get_damage_rate(
                    len(self.player_list), self.turn
                )
            self.card_place_phase()
            self.battle_phase()
        print(f"玩家{self.alive_players[0]}获胜")


new_game = Game(Settings())
new_game.waiting_for_players()
new_game.start()
