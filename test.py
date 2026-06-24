## Personal Programming Project - Vicky. 

import random
import time
from collections import Counter

all_cards = [
    ('h', 3, '🂱'), ('h', 4, '🂲'), ('h', 5, '🂳'), ('h', 6, '🂴'), ('h', 7, '🂵'), ('h', 8, '🂶'), ('h', 9, '🂷'), ('h', 10, '🂸'), ('h', 11, '🂹'), ('h', 12, '🂺'), ('h', 13, '🂻'), ('h', 14, '🂼'), ('h', 15, '🂽'),
    ('s', 3, '🂡'), ('s', 4, '🂢'), ('s', 5, '🂣'), ('s', 6, '🂤'), ('s', 7, '🂥'), ('s', 8, '🂦'), ('s', 9, '🂧'), ('s', 10, '🂨'), ('s', 11, '🂩'), ('s', 12, '🂪'), ('s', 13, '🂫'), ('s', 14, '🂬'), ('s', 15, '🂭'),
    ('d', 3, '🃁'), ('d', 4, '🃂'), ('d', 5, '🃃'), ('d', 6, '🃄'), ('d', 7, '🃅'), ('d', 8, '🃆'), ('d', 9, '🃇'), ('d', 10, '🃈'), ('d', 11, '🃉'), ('d', 12, '🃊'), ('d', 13, '🃋'), ('d', 14, '🃌'), ('d', 15, '🃍'),
    ('c', 3, '🃑'), ('c', 4, '🃒'), ('c', 5, '🃓'), ('c', 6, '🃔'), ('c', 7, '🃕'), ('c', 8, '🃖'), ('c', 9, '🃗'), ('c', 10, '🃘'), ('c', 11, '🃙'), ('c', 12, '🃚'), ('c', 13, '🃛'), ('c', 14, '🃜'), ('c', 15, '🃝'),
    ('BJ', 16, '🃏'), ('RJ', 17, '🃟')
]

# Rank map
def get_card_name(card):
    rank = card[1]
    if rank == 14:
        return f"{card[0]}A"
    elif rank == 15:
        return f"{card[0]}2"
    elif rank == 16:
        return "BJ"
    elif rank == 17:
        return "RJ"
    elif rank == 11:
        return f"{card[0]}J"
    elif rank == 12:
        return f"{card[0]}Q"
    elif rank == 13:
        return f"{card[0]}K"
    else:
        return f"{card[0]}{rank}"

full_deck = [(c[2], get_card_name(c), c) for c in all_cards]

# prints rules
def intro():

    print('''Bot: Hello! Welcome to DouDiZhu aka Landlord
Bot: These are the rules:''')
    print('''RULES:
3 people a game
Whoever gets the flipped card is the landlord
The landlord gets 3 extra cards that is shown to everyone
Card value in ascending: 3 4 5 6 7 8 9 10 J Q K A 2 BJ RJ
Card combinations:
Rocket: BJ and RJ, it is the largest combination
Solo chain: number sequence in ascending order (must at least be 5 cards)
Solo: any solo card
Pairs: a pair of the same number
Bomb: a quad of the same number (the value of each bomb depends on the card value)
Trio with single card : a triad of the same number plus a singular card (the value of the 3+1 depends on the triad)
Trio with pair: a triad of the same number plus a pair (the value of the 3+2 depends on the triad)
Pairs chain: at least three consecutive pairs
Airplane: at least two consecutive trios
Airplane with small wings: at least two consecutive trio and the same number of solo cards
Air plane with large wings: at least two consecutive trios and the same number of pairs
Four with two: four of the same card and two solos
Four with a pair: four of the same card and a pair
          
*** TO PLAY A CARD TYPE THE NUMBER (eg. 13: d3 , you type 13 to play the card) ***
''')
    print('''Betting: Start with $1000. Bombs/Rockets double the bet.
Goal: Bankrupt your opponents!
''')
    start = int(input("Type 1 to [Continue] \n "))
    return start == 1

# me, leanna, oscar :DDDD
def deal_cards():
    deck = full_deck.copy()
    random.shuffle(deck)
    vicky = deck[0:17]
    ossie = deck[17:34]
    lea = deck[34:51]
    extras = deck[51:54]
    return vicky, ossie, lea, extras

#the old landlord thingy too many bugs, program no longer allows player/bots to choose whether they want to be landlord
# new function of being able to bid/gamble
# no landlord extra cards, its causes bugs, 
def determine_landlord_and_bid(hands, extras, names):
    flip_card = random.choice(extras)
    print("Bot: I will shuffle the cards now...")
    print(f"\nBot: The flipped card is: {flip_card[0]}:{flip_card[1]}")
    
    start_index = 0
    #? I don't think this bit works
    for i, hand in enumerate(hands):
        if flip_card[2] in hand:
            start_index = i
            print(f"{names[i]} has the card. Bidding starts with {names[i]}.")
            break
            
    landlord_idx = -1
    highest_bid = 0
    
    bidding_order = [start_index, (start_index + 1) % 3, (start_index + 2) % 3]
    
    for i in bidding_order:
        print(f"\n {names[i]}'s turn to bid")
        print(f"Current highest bid: ${highest_bid}")
        time.sleep(1)
        
        if i == 0:
            try:
                bid_input = input(f"{names[0]}, enter your bid amount (must be > ${highest_bid}) or 0 to pass: ")
                bid_val = int(bid_input)
                if bid_val > highest_bid:
                    highest_bid = bid_val
                    landlord_idx = 0
                    print(f"{names[0]} bids ${highest_bid}.")
                else:
                    print(f"{names[0]} passes.")
            except ValueError:
                print(f"{names[0]} passes.")
        else:
            print(f"{names[i]} is thinking...")
            time.sleep(5)
            if random.randint(1, 10) > 3:
                new_bid = highest_bid + random.randint(10, 50)
                highest_bid = new_bid
                landlord_idx = i
                print(f"{names[i]} bids ${highest_bid}.")
            else:
                print(f"{names[i]} passes.")
    
    if landlord_idx == -1:
        print("No one bid. Redealing...")
        time.sleep(1)
        return None, None, None, None, None

    if landlord_idx == 0:
        hands[0].extend(extras)
    elif landlord_idx == 1:
        hands[1].extend(extras)
    else:
        hands[2].extend(extras)
        
    return hands[0], hands[1], hands[2], landlord_idx, highest_bid

def show_cards(player_cards):
    sorted_hand = sorted(player_cards, key=lambda x: x[2][1])
    print("Your cards: ", end="")
    for i, card in enumerate(sorted_hand):
        print(f"{i+1}:{card[0]}:{card[1]} ", end="")
    print()
    print(f"You currently have: {len(player_cards)} cards")
    print()
    return sorted_hand

# check the combo
def check_combination(cards):
    if not cards:
        return "Pass", 0
    values = [c[2][1] for c in cards]
    value_counts = Counter(values)
    num_cards = len(cards)
    counts = sorted(value_counts.values())
    unique_vals = sorted(value_counts.keys())
    
    # largest bomb
    if set(values) == {16, 17}:
        return "Rocket", 100
    
    if num_cards == 1:
        return "Solo", values[0]
    
    if num_cards == 2 and counts == [2]:
        return "Pair", values[0]
    
    #4 cards w same values
    if num_cards == 4 and counts == [4]:
        return "Bomb", values[0]
    
    if num_cards == 4 and counts == [1, 3]:
        return "Trio with single card", [v for v, c in value_counts.items() if c == 3][0]
    
    if num_cards == 5 and counts == [2, 3]:
        return "Trio with pair", [v for v, c in value_counts.items() if c == 3][0]
    
    # not bomb
    if num_cards == 5 and counts == [1, 4]:
        return "Four with two", [v for v, c in value_counts.items() if c == 4][0]
    
    if num_cards == 6 and counts == [2, 4]:
        return "Four with a pair", [v for v, c in value_counts.items() if c == 4][0]

    # big ones ykyk
    # Solo chain (at least 5 consecutive singles)
    if num_cards >= 5 and counts == [1] * num_cards:
        if all(unique_vals[i] + 1 == unique_vals[i+1] for i in range(len(unique_vals)-1)):
            if 16 not in unique_vals and 15 not in unique_vals:
                return "Solo chain", unique_vals[-1]
            
    # Pairs chain (at least 3 consecutive pairs)
    if num_cards >= 6 and counts == [2] * (num_cards // 2):
        if all(unique_vals[i] + 1 == unique_vals[i+1] for i in range(len(unique_vals)-1)):
            if 16 not in unique_vals and 15 not in unique_vals:
                return "Pairs chain", unique_vals[-1]
    
    # Aeroplane (at least 2 consecutive trios)
    if num_cards >= 6 and num_cards % 3 == 0 and counts == [3] * (num_cards // 3):
        if all(unique_vals[i] + 1 == unique_vals[i+1] for i in range(len(unique_vals)-1)):
            if 16 not in unique_vals and 15 not in unique_vals:
                return "Airplane", unique_vals[-1]

    # Aeroplane with smol wings (trios + same number of solos)       
    if num_cards % 4 == 0 and counts.count(3) == num_cards // 4 and counts.count(1) == num_cards // 4:
         trios = sorted([v for v, c in value_counts.items() if c == 3])
         if all(trios[i] + 1 == trios[i+1] for i in range(len(trios)-1)):
            if 16 not in trios and 15 not in trios:
                return "Airplane with small wings", trios[-1]

    #Aeroplane with big wings (trios + same number of pairs)
    if num_cards % 5 == 0 and counts.count(3) == num_cards // 5 and counts.count(2) == num_cards // 5:
         trios = sorted([v for v, c in value_counts.items() if c == 3])
         if all(trios[i] + 1 == trios[i+1] for i in range(len(trios)-1)):
            if 16 not in trios and 15 not in trios:
                return "Airplane with large wings", trios[-1]

    return "Unknown", 0


#check if the played cards can beat old
def can_beat(new_cards, old_cards, old_type, old_rank):
    new_type, new_rank = check_combination(new_cards)
    if new_type == "Unknown":
        return False
    
    if new_type == "Rocket":
        return True
    
    if old_type == "Rocket":
        return False
        
    if new_type == "Bomb":
        if old_type != "Bomb":
            return True
        else:
            return new_rank > old_rank
            
    if new_type == old_type:
        if len(new_cards) != len(old_cards):
            return False
        if new_type in ["Solo", "Pair", "Bomb"]:
            return new_rank > old_rank
        if "Trio" in new_type or "Airplane" in new_type or "chain" in new_type or "Four" in new_type:
            return new_rank > old_rank
            
    return False


#bots bots absolutely disgustin
def bot_play(bot_cards, last_played, last_type, last_rank, multiplier):
    ranks = Counter([c[2][1] for c in bot_cards])
    sorted_hand = sorted(bot_cards, key=lambda x: x[2][1])
    
    if not last_played:
        if 16 in ranks and 17 in ranks:
            return [c for c in bot_cards if c[2][1] in [16, 17]]
        available_ranks = [r for r in sorted(ranks) if r < 15]
        if len(available_ranks) >= 5:
            for start in range(len(available_ranks)):
                chain = []
                curr = available_ranks[start]
                while curr in ranks and curr < 15:
                    chain.append(curr)
                    if len(chain) == 5:
                        cards = []
                        for r in chain:
                            cards.extend([c for c in bot_cards if c[2][1] == r][:1])
                        return cards
                    curr += 1
        return [sorted_hand[0]]

    candidates = []
    
    if last_type == "Solo":
        for c in sorted_hand:
            if c[2][1] > last_rank:
                candidates = [c]
                break
    elif last_type == "Pair":
        for r in ranks:
            if ranks[r] >= 2 and r > last_rank:
                candidates = [c for c in bot_cards if c[2][1] == r][:2]
                break
    elif last_type == "Trio with single card":
        for r in ranks:
            if ranks[r] >= 3 and r > last_rank:
                trio = [c for c in bot_cards if c[2][1] == r][:3]
                remaining = [c for c in bot_cards if c not in trio]
                if remaining:
                    candidates = trio + [remaining[0]]
                break
    elif last_type == "Trio with pair":
        for r in ranks:
            if ranks[r] >= 3 and r > last_rank:
                trio = [c for c in bot_cards if c[2][1] == r][:3]
                rem_ranks = Counter([c[2][1] for c in bot_cards if c not in trio])
                for rr in rem_ranks:
                    if rem_ranks[rr] >= 2:
                        pair = [c for c in bot_cards if c[2][1] == rr][:2]
                        candidates = trio + pair
                        break
                if candidates: break
    elif last_type == "Solo chain":
        length = len(last_played)
        seq_ranks = [r for r in sorted(ranks) if r < 15]
        for i in range(len(seq_ranks)):
            chain = []
            curr = seq_ranks[i]
            while curr in ranks and curr < 15:
                chain.append(curr)
                if len(chain) == length:
                    if chain[-1] > last_rank:
                        cards = []
                        for r in chain:
                            cards.extend([c for c in bot_cards if c[2][1] == r][:1])
                        return cards
                    break
                curr += 1
    elif last_type == "Pairs chain":
        length = len(last_played) // 2
        pair_ranks = [r for r in sorted(ranks) if ranks[r] >= 2 and r < 15]
        for i in range(len(pair_ranks)):
            chain = []
            curr = pair_ranks[i]
            while curr in ranks and ranks[curr] >= 2 and curr < 15:
                chain.append(curr)
                if len(chain) == length:
                    if chain[-1] > last_rank:
                        cards = []
                        for r in chain:
                            cards.extend([c for c in bot_cards if c[2][1] == r][:2])
                        return cards
                    break
                curr += 1
    elif last_type == "Bomb":
        for r in ranks:
            if ranks[r] == 4 and r > last_rank:
                return [c for c in bot_cards if c[2][1] == r][:4]

    if candidates and can_beat(candidates, last_played, last_type, last_rank):
        return candidates

    if 16 in ranks and 17 in ranks:
        return [c for c in bot_cards if c[2][1] in [16, 17]]
        
    if last_type != "Rocket" and last_type != "Bomb":
        for r in ranks:
            if ranks[r] == 4:
                return [c for c in bot_cards if c[2][1] == r][:4]
                    
    return []

def main():
    if not intro():
        return

#og stuff
    money = [1000, 1000, 1000]
    names = ["Vicky", "Ossie", "Lea"]
    
    while min(money) > 0:
        print(f"\n\n New game  :D")
        print(f"Current Money: Vicky: ${money[0]} | Ossie: ${money[1]} | Lea: ${money[2]}")

        dealt_cards = deal_cards()
        vicky, ossie, lea = dealt_cards[0], dealt_cards[1], dealt_cards[2]
        extras = dealt_cards[3]
        hands = [vicky, ossie, lea]
        
        result = determine_landlord_and_bid(hands, extras, names)
        
        while result is None:
            dealt_cards = deal_cards()
            vicky, ossie, lea = dealt_cards[0], dealt_cards[1], dealt_cards[2]
            extras = dealt_cards[3]
            hands = [vicky, ossie, lea]
            result = determine_landlord_and_bid(hands, extras, names)
            
        vicky, ossie, lea, landlord_idx, base_bid = result
        
        hands = [vicky, ossie, lea]
        current_turn = landlord_idx
        last_played = []
        last_type = None
        last_rank = 0
        passes_in_row = 0
        multiplier = [1] 
        
        print(f"Base Bid: ${base_bid}. Current Multiplier: {multiplier[0]}x")
        time.sleep(1)
        
        while all(len(h) > 0 for h in hands):
            current_player_name = names[current_turn]
            current_hand = hands[current_turn]
            
            print(f"\n{current_player_name}'s Turn:")
            print(f"Pot Multiplier: {multiplier[0]}x")
            if last_played:
                print(f"Last played: {[c[1] for c in last_played]} ({last_type})")
            else:
                print("Table is clear.")
            time.sleep(0.5)
            
            if current_turn == 0:
                show_cards(current_hand)
                user_in = input("Enter card numbers (space separated) or 'pass': ").strip()
                
                if user_in.lower() == 'pass':
                    if not last_played:
                        print("You must play a card.")
                        continue
                    passes_in_row += 1
                    print("Vicky passed.")
                    time.sleep(1)
                else:
                    try:
                        indices = [int(x) - 1 for x in user_in.split()]
                        sorted_display = sorted(current_hand, key=lambda x: x[2][1])
                        potential_play = [sorted_display[i] for i in indices]
                        
                        p_type, p_rank = check_combination(potential_play)
                        
                        if not last_played:
                            if p_type != "Unknown":
                                last_played = potential_play
                                last_type = p_type
                                last_rank = p_rank
                                for c in potential_play:
                                    current_hand.remove(c)
                                passes_in_row = 0
                                if p_type in ["Bomb", "Rocket"]:
                                    multiplier[0] *= 2
                                    print(f"MULTIPLIER DOUBLED! Now {multiplier[0]}x")
                            else:
                                print("Invalid combination.")
                        else:
                            if can_beat(potential_play, last_played, last_type, last_rank):
                                last_played = potential_play
                                last_type, last_rank = check_combination(potential_play)
                                for c in potential_play:
                                    current_hand.remove(c)
                                passes_in_row = 0
                                if p_type in ["Bomb", "Rocket"]:
                                    multiplier[0] *= 2
                                    print(f"MULTIPLIER DOUBLED! Now {multiplier[0]}x")
                            else:
                                print("Cannot beat the current cards.")
                                continue
                    except (ValueError, IndexError):
                        print("Invalid input.")
                        continue
            else:
                print(f"{current_player_name} is thinking...")
                time.sleep(5)
                move = bot_play(current_hand, last_played, last_type, last_rank, multiplier)
                if move:
                    m_type, _ = check_combination(move)
                    print(f"{current_player_name} played: {[c[1] for c in move]} ({m_type})")
                    last_played = move
                    last_type, last_rank = check_combination(move)
                    for c in move:
                        current_hand.remove(c)
                    passes_in_row = 0
                    if m_type in ["Bomb", "Rocket"]:
                        multiplier[0] *= 2
                        print(f"MULTIPLIER DOUBLED! Now {multiplier[0]}x")
                else:
                    print(f"{current_player_name} passed.")
                    passes_in_row += 1
            
            time.sleep(1)
            
            if passes_in_row >= 2:
                last_played = []
                last_type = None
                last_rank = 0
                passes_in_row = 0
                
            winner_idx = -1
            for i, h in enumerate(hands):
                if len(h) == 0:
                    winner_idx = i
                    break
            
            if winner_idx != -1:
                print(f"\n{names[winner_idx]} wins the round!")
                time.sleep(1)
                payout = base_bid * multiplier[0]
                
                if winner_idx == landlord_idx:
                    print(f"Landlord ({names[winner_idx]}) wins! Civilians pay ${payout} each.")
                    money[winner_idx] += payout * 2
                    for i in range(3):
                        if i != winner_idx:
                            money[i] -= payout
                else:
                    print(f"Civilians win! Landlord ({names[landlord_idx]}) pays ${payout} to each civilian.")
                    money[landlord_idx] -= payout * 2
                    for i in range(3):
                        if i != landlord_idx:
                            money[i] += payout
                            
                print(f"Updated Money: Vicky: ${money[0]} | Ossie: ${money[1]} | Lea: ${money[2]}")
                time.sleep(2)
                break
                
            current_turn = (current_turn + 1) % 3

    print("\n\nGame over >:D")
    if money[0] <= 0:
        print("You went bankrupt! Game Over.")
    else:
        print("You bankrupted the bots! You Win! :D")

if __name__ == "__main__":
    main()