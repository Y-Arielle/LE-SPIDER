import random




score=500
moves=0
cards={'♥️':[1,2,3,4,5,6,7,8,9,10,'J','Q','K'],
      '♦️':[1,2,3,4,5,6,7,8,9,10,'J','Q','K'],
      '♣️':[1,2,3,4,5,6,7,8,9,10,'J','Q','K'],
      '♠️':[1,2,3,4,5,6,7,8,9,10,'J','Q','K']
}


game=[]
for colors,values in cards.items():
   for value in values:
       game.append((colors,value))


# 加倍牌堆并打乱顺序
for i in range(8):
   for j in range(len(game)):  # 将牌堆复制一份,一共复制8份
       game.append(game[j])


random.shuffle(game)  # 随机打乱牌堆


# 将牌分成 10 组，每组 5 张
groups = []  # 用于存储分组的列表


total_groups = 10  # 需要分成 10 组


index = 0  # 用于遍历牌堆的索引
for i in range(total_groups):
   group = []  # 当前组
   if i<4:
       for j in range(6):
           group.append(game[index])  # 添加一张牌到当前组
           index += 1  # 移动到下一张牌
       groups.append(group)  # 把当前组添加到分组列表中
   else:
       for j in range(5):
           group.append(game[index])  # 添加一张牌到当前组
           index += 1  # 移动到下一张牌
       groups.append(group)  # 把当前组添加到分组列表中


chance_cards=[]
for i in range(5):
   group = []
   for j in range(10):
       group.append(game[index])
       index += 1
   chance_cards.append(group)
chance_cards_count = 5
# 显示分组
group_number = 1
for group in groups:
   print("column", group_number, ":",group)  # 打印花色和牌值
   group_number += 1


def print_game():
   group_number = 1
   for group in groups:
       print("column", group_number, ":", group)  # 打印花色和牌值
       group_number += 1


def chanceCards():
   """ 分发特殊牌组 """
   global chance_cards_count
   if chance_cards_count > 0:
       for i in range(10):
           if chance_cards[chance_cards_count - 1]: # 机会牌组列表非空
               groups[i].append(chance_cards[chance_cards_count - 1].pop(0))
       chance_cards_count -= 1
       print("Chance cards have been dealt, "+ str(chance_cards_count)+ " sets of chance cards remain")
       print_game()
   else:
       print("No chance cards have been dealt！")




def get_card_value(card):
   """ 获取牌的值。如果是字母牌，返回一个固定的数值，数字牌返回本身 """
   if isinstance(card[1], int):  # 如果是数字牌，返回它的数字
       return card[1]
   elif card[1] == 'J':  # 如果是J，返回一个较小的值
       return 11
   elif card[1] == 'Q':  # 如果是Q，返回一个中等的值
       return 12
   elif card[1] == 'K':  # 如果是K，返回一个最大的值
       return 13
   else:
       return 0  # 如果是非法的牌，返回0


def move(cbase, cmove, position):
   """
   将一张或一组牌从源列(cbase)移动到目标列(cmove)。


   cbase: 当前的牌堆列表，表示源列
   cmove: 目标列
   position: 要移动的牌的索引位置，可以是单个牌或一组牌
   """
   global score
   # 确保位置合法
   if position < 0 or position >= len(cbase):
       print("Error: position out of range")
       return


   # 提取从指定位置开始的所有牌
   cards_to_move = cbase[position:]


   # 如果是移动多张牌，检查花色是否一致并且数字是否递减
   if len(cards_to_move) > 1:
       for i in range(len(cards_to_move) - 1):
           current_card = cards_to_move[i]
           next_card = cards_to_move[i + 1]
           current_value = get_card_value(current_card)
           next_value = get_card_value(next_card)
           # 确保数字递减
           if current_value - 1 != next_value:
               print("Error: The sequence of cards to be moved is not in decreasing order.")
               return
           # 确保花色一致
           if current_card[0] != next_card[0]:
               print("Error: The cards to be moved do not have the same suit.")
               return


   # 如果目标列为空
   if len(cmove) == 0:
       # 直接将整组牌移动到目标列
       cbase[position:] = []  # 删除源列中的这些牌
       cmove.extend(cards_to_move)  # 添加到目标列
       score -= 1
       print("Successfully moved", cards_to_move, "to target column!")
   else:
       # 检查目标列最后一张牌
       last_card = cmove[-1]
       last_card_value = get_card_value(last_card)


       # 获取要移动的第一张牌
       first_card_to_move = cards_to_move[0]
       first_card_to_move_value = get_card_value(first_card_to_move)


       # 检查与目标列最后一张牌是否递减（不需要花色相同）
       if first_card_to_move_value == last_card_value - 1:
           # 将整组牌移动到目标列
           cbase[position:] = []  # 删除源列中的这些牌
           cmove.extend(cards_to_move)  # 添加到目标列
           score -= 1
           print("Successfully moved", cards_to_move, "to target column!")
       else:
           print("Error: The move does not comply with the rules. The value must be decreasing.")


   return cbase, cmove






def main():
   global score
   global chance_cards_count
   while True:
       print("👉The current score is "+str(score))
       print("🍀Number of remaining chance cards"+str(chance_cards_count))
       action = input("🃏please input your action: 1: move; 2: get chance cards; 3: quit game")
       if action == "1":


           cbase=int(input("please input your columnbase:"))
           cmove=int(input("please input your columnmove:"))
           position=int(input("please input your position:"))
           move(groups[cbase-1], groups[cmove-1], position)
           print_game()


       elif action == "2":
           chanceCards()
       elif action == "3":
           print("Thank you for playing !😀")
           break
       else:
           print("🙅🙅🙅Invalid input!!!🙅🙅🙅")


main()
