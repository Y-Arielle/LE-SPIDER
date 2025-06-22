import random
import json
import os

score=500 # Score de départ -- 初始分数
moves=0 # Nombre de mouvements -- 移动次数
completed_groups = 0  # Nombre de séries complètes -- 已完成排序的牌组数
chance_cards_count = 5 # Nombre de cartes de chance -- 机会牌的数量

# Définir la composition des cartes -- 定义牌的组成
hard_cards={'♥️':['A',2,3,4,5,6,7,8,9,10,'J','Q','K'],
       '♦️':['A',2,3,4,5,6,7,8,9,10,'J','Q','K'],
       '♣️':['A',2,3,4,5,6,7,8,9,10,'J','Q','K'],
       '♠️':['A',2,3,4,5,6,7,8,9,10,'J','Q','K']
}

# Convertir les cartes alphabétiques en chiffres -- 将字母牌转换为数字
# Obtenir la valeur de la carte.
# S'il s'agit d'un nombre, elle renvoie lui-même.
# S'il s'agit d'une lettre, elle renvoie un nombre fixe -- 获取牌的值。如果是字母牌，返回一个固定的数值，数字牌返回本身
def getCardValue(card):

    if isinstance(card[1], int):
        return card[1]
    elif card[1] == 'A':
        return 1
    elif card[1] == 'J':
        return 11
    elif card[1] == 'Q':
        return 12
    elif card[1] == 'K':
        return 13
    else:
        return 0  # Renvoie 0 s'il s'agit d'un caractère illégal. --如果是非法的牌，返回0

# Réglage des différents modes.( Facile, moyen et difficile ) -- 设置不同的游戏模式
def differentModes(mode):
    if mode == 1: # Facile
        easy_cards={}
        easy_cards['♠️']=hard_cards['♠️']
        return easy_cards
    elif mode == 2: # Moyen
        medium_cards={}
        medium_cards['♥️']=hard_cards['♥️']
        medium_cards['♣️']=hard_cards['♣️']
        return medium_cards
    elif mode == 3: # Difficile
        return hard_cards
    else:
        print("🙅🙅🙅Invalid difficulty selected! Defaulting to hard mode.")
        return hard_cards

# Définir l'état au tout début du jeu, en stockant chaque jeu de cartes dans un tableau.
# Compris cards( modes différents ),groups,chance_cards
def setGame():
    game = [] # Pour tout les cards random
    mode = int(input("👾Please input the number to choix the game mode: 1->easy ; 2->medium ; 3->hard "))
    cards = differentModes(mode)

    for colors, values in cards.items():
        for value in values:
            game.append((colors, value))

    # Doublez les piles et séparez l'ordre, pour un total de 8 séries de 104 cartes,
    # 50 cartes de chance et 54 cartes de départ.
    # 加倍牌堆并打乱顺序, 一共8组牌104张，50张机会牌，54张初始牌
    for i in range(8):
        for j in range(len(game)):
            game.append(game[j])

    random.shuffle(game)

    groups = []  # Pour le plateau : Liste de stockage des groupes. -- 用于存储分组的列表

    total_groups = 10  # Il y a 10 séries de cartes. -- 需要分成 10 组

    index = 0
    for i in range(total_groups):
        group = []
        if i < 4:
            for j in range(6):
                group.append(game[index])
                index += 1
            groups.append(group)
        else:
            for j in range(5):
                group.append(game[index])
                index += 1
            groups.append(group)
    chance_cards = []
    for i in range(5):
        group = []
        for j in range(10):
            group.append(game[index])
            index += 1
        chance_cards.append(group)

    return cards,groups,chance_cards

# Enregistrer le jeu. -- 保存游戏
def saveGame(groups, visible_count, score, moves, completed_groups, chance_cards_count, chance_cards):
    save_data = {
        "groups": groups,
        "visible_count": visible_count,
        "score": score,
        "moves": moves,
        "completed_groups": completed_groups,
        "chance_cards_count": chance_cards_count,
        "chance_cards": chance_cards
    }
    with open("game_save.json", "w") as file:
        json.dump(save_data, file)
    print("✅Game state has been saved to 'game_save.json'.")

# Charger le dernier jeu. -- 加载历史游戏
def loadGame():
    if os.path.exists("game_save.json"):
        with open("game_save.json", "r") as file:
            return json.load(file)
    return None

# Initialiser l'état du jeu, -- 初始化游戏状态
# s'il existe un jeu historique, l'utilisateur le sélectionne et reprend le jeu
# sinon un nouveau jeu est lancé.
saved_state = loadGame()
if saved_state:
    load_choice = input("⏰A saved game was found. Would you like to load it? (yes/no): ").strip().lower()
    if load_choice == "yes":
        print("🕷Loading saved game...")
        global groups, visible_count
        groups = saved_state["groups"]
        visible_count = saved_state["visible_count"]
        score = saved_state["score"]
        moves = saved_state["moves"]
        completed_groups = saved_state["completed_groups"]
        chance_cards_count = saved_state["chance_cards_count"]
        chance_cards = saved_state["chance_cards"]
    else:
        print("🆕Starting a new game.")
        cards, groups, chance_cards = setGame()
        visible_count=[]
        for i in range(len(groups)):
            visible_count.append(groups[i])
else:
    print("❗No saved game found. Starting a new game.")
    cards, groups, chance_cards = setGame()
    visible_count = []
    for i in range(len(groups)):
        visible_count.append(groups[i])

# Mise à jour automatique du nombre de cartes visibles dans chaque colonne. -- 动态更新可见牌的数量
# def updateVisibleCount(groups, cbase, cmove, moved_cards_count):
#     # Pour la colonne source :
#     # le nombre actuel de cartes visibles - le nombre de cartes déplacées.
#     if len(groups[cbase]) > 0:
#         if visible_count[cbase] > moved_cards_count :
#             visible_count[cbase] = visible_count[cbase] - moved_cards_count
#         else:
#             visible_count[cbase] = 1
#     elif len(groups[cbase])==0 :
#         visible_count[cbase] = 0
#     # Pour la colonne target :
#     # le nombre de cartes actuellement visibles + le nombre de cartes déplacées.
#     visible_count[cmove] =  visible_count[cmove] + moved_cards_count
#     return visible_count

# Imprimer le plateau
# Tous les jeux (compris les cartes cachées) sont affichés en colonnes, avec la position à l'extrême gauche.
# -- 按列对齐显示所有牌组（包括隐藏牌），并在最左侧显示 Position。
# Tous les affichages ont la même largeur de caractère. -- 所有显示内容的字符宽度一致。
def printGame(groups):

    # Largeur fixe par colonne (avec le contenu de la carte et les espaces). -- 每列固定宽度（包含牌内容和空格）
    column_width = 12

    # Calculer la hauteur maximale des colonnes.( Déterminer le nombre de lignes ou positions à imprimer. ) -- 计算最大列高度
    max_height = 0
    for group in groups:
        if len(group) > max_height:
            max_height = len(group)

    # La première ligne du plateau affiche -- des titres.
    # Construction de titres de colonnes. -- 构造列标题
    column_titles = ["Position".center(column_width)]
    for i in range(len(groups)):
        column_titles.append(("Column " + str(i + 1)).center(column_width))
    print("".join(column_titles))

    # Imprimer le contenu des séries de cartes ligne par ligne. -- 逐行打印牌组内容
    for row in range(max_height):
        row_output = []
        # Ajouter une colonne Position. -- 添加 Position 列
        row_output.append(("P" + str(row + 1)).center(column_width))

        # Ajouter le contenu des cartes. -- 添加牌组内容
        for col in range(len(groups)):
            group = groups[col]
            # hidden = len(group) - visible_count[col]  # Nombre de cartes cachées. -- 隐藏牌数
            if row < len(group):  # S'il y a une carte dans la position actuelle associée à cette colonne. -- 如果这一列对应的当前位置有一张牌
                # if row < hidden:  # Déterminer s'il s'agit d'une carte cachée. -- 判断是不是隐藏牌
                #     card = "*"
                # else:  # Carte visible. -- 可见牌
                card = group[row][0] + str(group[row][1])  # Imprimer la carte. -- 格式化显示牌
                row_output.append(card.center(column_width))  # Centré, largeur fixe. -- 居中对齐，固定宽度
            else:
                row_output.append(" ".center(column_width))  # S'il n'y a pas de carte dans la position actuelle associée à cette colonne, imprimer un espace.
        print("".join(row_output))  # Imprimer la ligne en cours. -- 打印一行

# Délivrance des cartes de chance. -- 发放机会牌
def chanceCards(groups,chance_cards):
    global chance_cards_count, moves
    # S'il y a des cartes de chance.
    if chance_cards_count > 0:
        for i in range(10):
            if chance_cards[chance_cards_count - 1]:
                groups[i].append(chance_cards[chance_cards_count - 1].pop(0))
                visible_count[i] += 1  # Augmenter le nombre de cartes visibles. -- 增加该列的可见牌数，因为机会牌被添加到该列
        chance_cards_count -= 1
        moves += 1
        print("👌Chance cards have been dealt, "+ str(chance_cards_count)+ " sets of chance cards remain")
    else:
        print("🙅No chance cards have been dealt！")

# Déplace une carte ou un groupe de cartes de la colonne source (cbase) vers la colonne cible (cmove).
# Position : l'index de la première carte de la carte à déplacer
def move(groups,cbase, cmove, position,indexbase,indexmove):

    global score,moves,completed_groups
    # Vérifier que la position existe. -- 确保位置合法
    if position < 0 or position >= len(cbase):
        print("🙅🙅🙅Invalid input: position out of range")
        return

    # Sélectionne toutes les cartes à partir de la position spécifiée. -- 提取从指定位置开始的所有牌
    cards_to_move = cbase[position:]

    # Si vous déplacez plusieurs cartes, vérifiez que les couleurs sont de même et que les nombres sont décroissants. -- 如果是移动多张牌，检查花色是否一致并且数字是否递减
    if len(cards_to_move) > 1:
        for i in range(len(cards_to_move) - 1):
            current_card = cards_to_move[i]
            next_card = cards_to_move[i + 1]
            current_value = getCardValue(current_card)
            next_value = getCardValue(next_card)
            # Les nombres sont décroissants. -- 确保数字递减
            if current_value - 1 != next_value:
                print("🙅🙅🙅Invalid move: The sequence of cards to be moved is not in decreasing order.")
                return
            # Les couleurs sont de même. 确保花色一致
            if current_card[0] != next_card[0]:
                print("🙅🙅🙅Invalid move: The cards to be moved do not have the same suit.")
                return

    # Si la colonne target est vide. -- 如果目标列为空
    if len(cmove) == 0:
        # Mouvement direct. -- 直接将整组牌移动到目标列
        cbase[position:] = []  # Supprimer ces cartes de la colonne source. 删除源列中的这些牌
        cmove.extend(cards_to_move)  # Ajouter à la colonne target. -- 添加到目标列
        score -= 1
        moves += 1
        # Mettre à jour le nombre de cartes visibles une fois le déplacement terminé. -- 移动完成后更新可见牌数量
        # updateVisibleCount(groups,indexbase, indexmove, len(cards_to_move))
        print("✅Successfully moved", cards_to_move, "to target column!")
    # Si la colonne target n'est pas vide.
    else:
        # Obtenir la dernière carte de la colonne target. -- 检查目标列最后一张牌
        last_card = cmove[-1]
        last_card_value = getCardValue(last_card)

        # Obtenir la première carte à déplacer. -- 获取要移动的第一张牌
        first_card_to_move = cards_to_move[0]
        first_card_to_move_value = getCardValue(first_card_to_move)

        # Vérifie la décroissance avec la dernière carte de la colonne target
        # (il n'est pas nécessaire qu'il s'agisse de la même couleur). -- 检查与目标列最后一张牌是否递减（不需要花色相同）
        if first_card_to_move_value == last_card_value - 1:
            # Mouvement. -- 将整组牌移动到目标列
            cbase[position:] = []  # Supprimer ces cartes de la colonne source. -- 删除源列中的这些牌
            cmove.extend(cards_to_move)  # Ajouter à la colonne target. -- 添加到目标列
            score -= 1
            moves += 1
            #updateVisibleCount(groups,indexbase, indexmove, len(cards_to_move))   # Mettre à jour le nombre de cartes visibles. -- 更新可见牌数量
            print("✅Successfully moved", cards_to_move, "to target column!")
        else:
            print("🙅🙅🙅Invalid move: The move does not comply with the rules. The value must be decreasing.")
            return
        # Vérifier si la colonne target est complète. 检查目标列是否完成排序
        if checkCompleteGroup(cmove):
            completed_groups += 1
            score += 101
            print("🎉 A group is completed! Total completed groups: "+str(completed_groups))
            remove_completed_group(cmove)
            visible_count[indexmove] = max(1, visible_count[indexmove] - 13) # 更新 visible_count
    return cbase, cmove

# Pour annuler le dernier déplacement, sauvegarder chaque état de jeu
history = []
def saveHistory():
    # Afin de ne pas modifier les données d'origine, nous copions tous les états actuels. -- 将所有状态复制以实现不影响原有数据就能撤销操作
    groups_copy = []
    for group in groups:
        new_group = []
        for card in group:
            new_group.append(card)
        groups_copy.append(new_group)

    chance_cards_copy = []
    for chance_group in chance_cards:
        new_chance_group = []
        for card in chance_group:
            new_chance_group.append(card)
        chance_cards_copy.append(new_chance_group)

    visible_count_copy = []
    for count in visible_count:
        visible_count_copy.append(count)

    history.append({
        "groups": groups_copy,
        "visible_count": visible_count_copy,
        "score": score,
        "moves": moves,
        "completed_groups": completed_groups,
        "chance_cards_count": chance_cards_count,
        "chance_cards": chance_cards_copy
    })

def undoLastMove():

    global groups, visible_count, score, moves, completed_groups, chance_cards_count, chance_cards

    if history:
        last_state = history.pop()  # Retirer le dernier état sauvegardé. -- 取出最后一个保存的状态

        # Remettre les groupes en place. -- 手动还原 groups
        groups = []
        for group in last_state["groups"]:
            new_group = []
            for card in group:
                new_group.append(card)
            groups.append(new_group)

        # Remettre les cartes de chance.
        chance_cards = []
        for chance_group in last_state["chance_cards"]:
            new_chance_group = []
            for card in chance_group:
                new_chance_group.append(card)
            chance_cards.append(new_chance_group)

        # Remettre visible_count.
        visible_count = []
        for count in last_state["visible_count"]:
            visible_count.append(count)

        # Remettre le score et les autres.
        score = last_state["score"]
        moves = last_state["moves"]
        completed_groups = last_state["completed_groups"]
        chance_cards_count = last_state["chance_cards_count"]

        print("🔙 Undo successful! Reverted to the previous state.")
        printGame(groups)
    else:
        print("🙅 No move to undo!")

# C'est pour proposer des déplacements possibles.
# Vérifie si une série de cartes est une séquence décroissante complète :
# Même couleur et séquence décroissante de nombres
def isCompleteSequence(cards):

    if len(cards) < 2:  # Une carte est toujours possible. -- 单张牌总是合法的
        return True

    for i in range(len(cards) - 1):
        if cards[i][0] != cards[i + 1][0]:  # Vérifie s'ils sont de même couleur. -- 检查花色是否一致
            return False
        if getCardValue(cards[i]) - 1 != getCardValue(cards[i + 1]):  # Vérifie s'il est séquence décroissante de nombres. -- 检查数字是否递减
            return False
    return True

def suggestMove(groups, visible_count):

    #Vérifie dans toutes les colonnes actuelles si des cartes peuvent être déplacées et renvoie un guide de déplacement.
    for src_col in range(len(groups)):
        src_group = groups[src_col]
        if len(src_group) > 0:
            visible_cards = src_group[-visible_count[src_col]:]  # Obtenir des cartes visibles. -- 获取可见的牌
            for i in range(len(visible_cards)):
                cards_to_move = visible_cards[i:]  # Obtenir les cartes à partir de la position actuelle. -- 获取从当前位置开始的牌组
                if isCompleteSequence(cards_to_move):  # Traite uniquement les séquences décroissantes complètes qui sont conformes aux règles. -- 仅处理符合规则的完整递减序列
                    for target_col in range(len(groups)):  # Analyse de toutes les colonnes target. -- 遍历所有目标列
                        if src_col != target_col:  # Les colonnes source et target ne peuvent pas être les mêmes. -- 源列和目标列不能相同
                            target_group = groups[target_col]
                            if len(target_group) == 0:  # Si la colonne target est vide, la déplacer directement. -- 如果目标列为空
                                return "Move " + str(cards_to_move) + " from column " + str(src_col + 1) + " to empty column " + str(target_col + 1)
                            # Vérifier que les cartes déplacés sont correctement connectés aux colonnes targets. -- 检查移动的牌组能否正确连接到目标列
                            last_target_card = target_group[-1]  # Obtenir la dernière carte de la colonne target. 获取目标列最后一张牌
                            if (
                                cards_to_move[0][0] == last_target_card[0]  # même couleur -- 花色相同
                                and getCardValue(cards_to_move[0]) == getCardValue(last_target_card) - 1  # décroissant -- 数值递减
                            ):
                                return "Move " + str(cards_to_move) + " from column " + str(src_col + 1) + " to column " + str(target_col + 1)

    return "No moves available at the moment."  # S'il n'y a pas de cartes amovibles. -- 如果没有可移动的牌

# Vérifie si une série de cartes a été trié (de K à A).
def checkCompleteGroup(group):

    # Si le nombre de cartes est inférieur à 13, retour Faux. -- 如果牌组长度不足 13，直接返回 False
    if len(group) < 13:
        return False

    # Déterminer la couleur target. -- 确定目标花色
    suit = group[-13][0]  # 倒数第 13 张牌的花色

    # Vérifiez dans l'ordre à partir de la treizième carte. -- 从倒数第 13 张开始依次检查
    for i in range(13):
        card = group[-13 + i]
        # Si la couleur et l'ordre ne sont pas correctes, retour Faux. -- 如果花色不一致或点数不符合 K 到 A 的顺序，返回 False
        if card[0] != suit or getCardValue(card) != 13 - i:
            return False

    return True

# Si une une série de cartes a été trié, on la supprime.
def remove_completed_group(group):

    del group[-13:]

# Vérifiez si tous les carts ont été trié.
def checkVictory(completed_groups):

    if completed_groups == 8:
        print("🎉🎉 Congratulations! You've sorted all the cards! You win! 🎉🎉")
        return True
    return False

# Fonction principale
def main():
    global score,moves,chance_cards_count,completed_groups,chance_cards

    # Imprimer le plateau
    printGame(groups)

    # Si on ne gagne pas, continuer à répéter la boucle
    while True:
        sum=0
        for i in range(len(groups)):
            sum+=len(groups[i])
        print("🃏Current number of cards on the table: "+str(sum))
        print("👉The current score: "+str(score))
        print("🔢The current moves: "+str(moves))
        print("🎯Completed groups: "+str(completed_groups))
        print("🍀Number of remaining chance cards: "+str(chance_cards_count*10))

        # Vérifier pour la gagne, si oui, break. -- 检查是否胜利
        if checkVictory(completed_groups):
            break

        action = input("🃏please input your action: 1: move; 2: get chance cards; 3: undo last move; 4: suggest move; 5: quit game ")
        # action 1: move
        if action == "1":
            saveHistory()
            user_input = input("🕸Please input 'source column, target column, position' (e.g., 1,2,3): ") # Saisir en une seule fois toutes les données nécessaires au mouvement.
            inputs = user_input.strip().split(",")
            if len(inputs) != 3:
                print("🙅🙅🙅Invalid input! Please enter THREE numbers separated by commas.")
            else:
                valid = True  # En supposant que l'entrée soit valide. -- 假设输入有效
                res = []  # Enregistre le nombre d'entrées. -- 存储转换后的整数
                for i in inputs:
                    i = i.strip()  # Supprimer les espaces avant et après. -- 去除前后的空格
                    if not i.isdigit():  # Vérifier s'il s'agit d'un nombre. -- 检查是否为数字
                        valid = False
                        break
                    res.append(int(i))  # Transforme une chaîne de caractères en un nombre entier et l'ajoute à res. -- 将字符串数字转换为整数并添加到 res 中

                if not valid:
                    print("🙅🙅🙅Invalid input! Input must be NUMBERS separated by commas.")
                else:
                    # Les données converties sont utilisées pour cbase, cmove et position. -- 将转换后的数据赋值给 cbase, cmove, position
                    cbase, cmove, position = res[0], res[1], res[2]
                    # Vérifier que la valeur de la plage d'entrée est valide. -- 检查输入的范围是否合法
                    if not (1 <= cbase <= len(groups)) or not (1 <= cmove <= len(groups)):
                        print("🙅🙅🙅Invalid column numbers! Please try again.")
                    elif not (1 <= position <= len(groups[cbase - 1])):
                        print("🙅🙅🙅Invalid position for the source column! Please try again.")
                    else:
                        # Si tous les données sont valids, movement. 调用 move 函数执行牌的移动操作
                        move(groups, groups[cbase - 1], groups[cmove - 1], position - 1, cbase - 1, cmove - 1)
                        printGame(groups)
        # action 2: get chance cards
        elif action == "2":
            saveHistory()  # 保存当前状态
            chanceCards(groups, chance_cards)
            printGame(groups)
        # action 3: undo last move
        elif action == "3":
            undoLastMove()
        # action 4: suggest move
        elif action == "4":
            suggestion = suggestMove(groups, visible_count)
            print("🔍 Suggested move:", suggestion)
        # action 5: quit game
        elif action == "5":
            save = input("🕷Would you like to save the game state before quitting? (yes/no): ").strip().lower()
            if save == "yes":
                saveGame(groups, visible_count, score, moves, completed_groups, chance_cards_count,chance_cards)
            print("Thank you for playing! 😀")
            break
        else:
            print("🙅🙅🙅Invalid input!Please try again.")

# Commencer le jeu
main()