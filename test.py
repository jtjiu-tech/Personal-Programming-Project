import random, time, sys

##CLASSES     
   
    
class PlayerInfo:
    """An object containing player information. Pass in when modifying player libraries or info"""
    def __init__(self, game_bank, quick_key, player_dicts):
        self.game_bank = game_bank
        self.quick_key = quick_key
        self.player_dicts = player_dicts
        self.player_turn = 1
        self.game_stage = 1
        self.longest_road = [0, 0]
        self.largest_army = [0, 0]


class Grid:
    """An object to contain all the important information needed to render the grid or access its variables"""
    def __init__(self, robber, tiles, settlement_locs, roads, biomes):
        self.robber = robber
        self.tiles = tiles
        self.settlement_locs = settlement_locs
        self.roads = roads
        self.biomes = biomes
    

##CONSTANTS


INFO_MESSAGE = """List of omissions:
> Player-player trades not implemented
> You won't obtain the resources from your second settlement
> Longest road and largest army haven't been coded yet
> Your second road can also be attached to an existing road (it's more fun like that)
> You can build past someone else's settlement as long as you have a road connected to it (I didn't have time to code against that)
> Cities aren't explicitly shown, so please use your imagination :D - however they'll still be displayed in terms of victory points.
> Cities will not get double the resources. I forgot about that rule.
> There are probably more - please let me know if you see any when testing!"""

COSTS = """The costs for actions as follows:
ROAD: 1x brick, 1x wood
SETTLEMENT: 1x brick, 1x wood, 1x grain, 1x sheep
CITY (upgrades from settlement): 2x grain, 3x ores
DEVELOPMENT CARD (type 'draw'): 1x sheep, 1x grain, 1x ores
Development cards can include:
- victory point cards (secret victory points)
- year of plenty (get 2 free cards from bank)
- monopoly (get all copies of a specific card from players)
- knight cards (move robber)
- build road cards (place 2 free roads).
Is this information too long? Type 'cls' to clear :)"""

COMMANDS = """These are the commands available to you:
'et' ends your turn - you have to roll first. This is password protected!
'b' allows you to build, should you have enough resources!
't' allows you to trade with a player or port.
'r' lets you roll for resources- you can do this once a turn.
'cls' clears some text in case you have too much on your screen
'd' allows you to draw a development card.
'i' prints out the adaptations made here from the original game of Catan.
'pod' or 'deck' allows you to see your deck. This is under password protection.
'costs' lets you see how much each action will cost."""

ERROR_MESSAGE = "That action doesn't exist. Type 'cmds' or 'c' if you're confused on what commands you can use here!"
    
RESOURCES = ["ores", "grain", "wood", "brick", "sheep"]
    
CARDS = {'knight': 14, 'year of plenty': 2, 'build road': 2, 'monopoly': 2, 'VP card': 5}

ASSOCIATED_SETTLEMENTS = {
    "S1": ["A", "B", "E", "I", "H", "D"],
    "S2": ["C", "D", "H", "N", "M", "G"],
    "S3": ["E", "F", "J", "P", "O", "I"],
    "S4": ["$", "G", "M", "S", "R", "L"],
    "S5": ["H", "I", "O", "U", "T", "N"],
    "S6": ["J", "K", "Q", "W", "V", "P"],
    "S7": ["M", "N", "T", "Z", "Y", "S"],
    "S8": ["O", "P", "V", "b", "a", "U"],
    "S9": ["R", "S", "Y", "e", "d", "X"],
    "S10": ["T", "U", "a", "g", "f", "Z"],
    "S11": ["V", "W", "c", "i", "h", "b"],
    "S12": ["Y", "Z", "f", "l", "k", "e"],
    "S13": ["a", "b", "h", "n", "m", "g"],
    "S14": ["d", "e", "k", "q", "p", "j"],
    "S15": ["f", "g", "m", "s", "r", "l"],
    "S16": ["h", "i", "o", "u", "t", "n"],
    "S17": ["k", "l", "r", "w", "v", "q"],
    "S18": ["m", "n", "t", "y", "x", "s"],
    "S19": ["r", "s", "x", "+", "z", "w"]
    }

KAOMOJIS = {
        "ores": "‧₊˚🗻`",
        "brick": "↟↟↟↟↟↟",
        "grain": "˚ʚ🌱₊˚",
        "wood": " ݁˖𓂃.𖠰.",
        "sheep": ":3 ^^~", 
        "desert": " ⛰︎ ོ ༄-"}

COLOUR_CODES = {"red" : [255, 0, 0], "green" : [0, 255, 0], "blue" : [0, 0, 255]}

CONSTRUCT_COSTS =  {'road' : {'brick' : 1, 'wood' : 1},
                         'settlement' : {'brick' : 1, 'wood' : 1, 'grain' : 1, 'sheep' : 1},
                         'city' : {'grain' : 2, 'ores' : 3},
                         'dev card': {'sheep' : 1, 'grain' : 1, 'ores' : 1}}

##DISPLAY-RELATED


def clear_screen():
    """Clears the screen with ansi code"""
    print("\033c", end="")
    
    
def print_grid(grid : Grid):##this is a very long function so keep it closed.
    """Prints out the grid. KEEP THIS SUBROUTINE FOLDED OR IT WILL BE A GIANT BLOCK OF TEXT"""

    grid_part_1 = (
#line 1
(" " * 65) + "3: 1 port" + "\n" +
#line 2
(" " * 65) + "/      \\" + "\n" +
#line 3
(" " * 64) + "/        \\" + "\n" +
#line 4
(" " * 20) + "sea" + (" " * 38) + grid.settlement_locs["A"]["display"] + " " + (grid.roads["AB"]["display"] + " ") * 4 + grid.settlement_locs["B"]["display"] + (" " * 38) + "sea" + "\n" +
#line 5
(" " * 61) + grid.roads["AD"]["display"] + "              " + grid.roads["BE"]['display'] + "\n" +
#line 6 & 7
(" " * 60) + grid.roads["AD"]['display'] + "                " + grid.roads["BE"]['display'] + "\n\n" +
#line 8
(" " * 35) + ("2:1 grain port") + (" " * 9) + grid.roads["AD"]['display'] + (" " * 7) + KAOMOJIS[grid.tiles["S1"]["biome"]] + (" "* 7) + grid.roads["BE"]['display'] + (" " * 16) + "3:1 port" + "\n" +
#line 9
(" " * 36) + "|    " + "\\" + "   " + (grid.roads["CD"]['display'] + " ") * 4 + grid.roads["AD"]['display'] + (" " * 10) + str(grid.tiles["S1"]["number"]) 
+ (" " * 11 if len(str(grid.tiles["S1"]["number"])) == 1 else " " * 10) + grid.roads["BE"]['display'] + " " + (grid.roads["EF"]['display'] + " ") * 4 + "   /  |\n" +
#line 10
(" " * 36) + "|" + (" " * 3) + grid.settlement_locs["C"]["display"] + " " + grid.roads["CG"]['display'] + (" " * 11) + grid.settlement_locs["D"]["display"] + "  " + grid.roads["DH"]['display']
+ (" " * ((22 - len(str(grid.tiles["S1"]["biome"])))//2)) + grid.tiles["S1"]["biome"] +
(" " * (((22-len(str(grid.tiles["S1"]["biome"])))//2)+ (1 if len(str(grid.tiles["S1"]["biome"]))%2 != 0 else 0)))
+ grid.roads["EI"]['display'] + " " + grid.settlement_locs["E"]["display"] + (" " * 8) + grid.settlement_locs["F"]["display"] + "  " + grid.roads["FJ"]['display'] + "     |\n" +
#line 11
(" " * 36) + "|" + "    " + grid.roads["CG"]['display'] +  (" " * 16) + grid.roads["DH"]['display'] + (" " * 9) + "S1" + (" " * 9) + grid.roads["EI"]['display'] + (" " * 15) + 
grid.roads["FJ"]['display'] + "    |" + "\n" +
#line 12
(" " * 36) + "|" + (" " * 63) + "|" + "\n" +
#line 13
(" " * 36) + "|" + "  " + grid.roads["CG"]['display'] + (" " * 7) + KAOMOJIS[grid.tiles["S2"]["biome"]] + (" " * 7) + grid.roads["DH"]['display'] 
+ (" " * 16) + grid.roads["EI"]['display'] + " "  + (" " * 6) + (KAOMOJIS[grid.tiles["S3"]["biome"]]) 
+ (" " * 6) + grid.roads["FJ"]['display'] +"  |\n" +
#line 14
(" " * 21) + grid.settlement_locs["$"]["display"] + " " + (grid.roads[quick_reorder("G$")]['display'] + " ") * 4 + grid.settlement_locs["G"]["display"] + "  " + grid.roads["CG"]['display'] + (" " * 10) + str(grid.tiles["S2"]["number"]) + 
(" " * 9 if len(str(grid.tiles["S2"]["number"])) == 1 else " " * 8) + grid.settlement_locs["H"]["display"] + " " + grid.roads["DH"]['display'] + " " + (grid.roads["HI"]['display'] + " ") * 4 + " " + grid.roads["EI"]['display'] + " " + grid.settlement_locs["I"]["display"] +
(" " * 8) + str(grid.tiles["S3"]["number"]) + (" " * 8 if len(str(grid.tiles["S3"]["number"])) == 1 else " " * 7) + grid.settlement_locs["J"]["display"] + " " + grid.roads["FJ"]['display'] + " | " + (grid.roads["JK"]['display'] + " ") * 4 
+ grid.settlement_locs["K"]["display"] + "\n" +
#line 15
(" " * 21) + grid.roads[quick_reorder("L$")]['display'] + (" " * 16) + grid.roads["GM"]['display'] + (" " * ((22 - len(str(grid.tiles["S2"]["biome"])))//2)) + grid.tiles["S2"]["biome"] + (" " * 9 if grid.tiles["S2"]["biome"] != "desert" else " " * 8)
+ grid.roads["HN"]['display'] + (" " * 14) + grid.roads["IO"]['display'] + (" " * ((21 - len(str(grid.tiles["S3"]["biome"])))//2)) + grid.tiles["S3"]["biome"] + (" " * ( (21 - len(grid.tiles["S3"]["biome"])) //2   ) ) + 
(" " * (1 if len(grid.tiles["S3"]["biome"]) % 2 != 1 else 0)) + grid.roads["JP"]['display'] + (" " * 14) + grid.roads["KQ"]['display'] + "\n" +
#line 16 & 17 
(" " * 20) + grid.roads[quick_reorder("L$")]['display'] + (" " * 18) + grid.roads["GM"]['display'] + (" " * 9) + "S2" + (" " * 9) + grid.roads["HN"]['display'] + (" " * 16) + grid.roads["IO"]['display'] + (" " * 8) + "S3" + (" " * 9) + grid.roads["JP"]['display'] + 
(" " * 16) + grid.roads["KQ"]['display'] + "\n\n" +
#line 18
(" " * 18) + grid.roads[quick_reorder("L$")]['display'] + (" " * 8) + KAOMOJIS[grid.tiles["S4"]["biome"]] + (" " * 8) + grid.roads["GM"]['display'] + (" " * 16) + grid.roads["HN"]['display'] + (" " * 7) + 
KAOMOJIS[grid.tiles["S5"]["biome"]] + (" " * 7) + grid.roads["IO"]['display']
+ (" " * 15) + grid.roads["JP"]['display'] + (" " * 7) + KAOMOJIS[grid.tiles["S6"]["biome"]] + (" " * 7) + grid.roads["KQ"]['display'] + "\n" + 
#line 19
(" " * 15) + grid.settlement_locs["L"]["display"] + " " + grid.roads[quick_reorder("L$")]['display'] + (" " * 11) + str(grid.tiles["S4"]["number"]) + (" " * (10 if len(str(grid.tiles["S4"]["number"])) == 1 else 9)) + grid.settlement_locs["M"]["display"] +
" " + grid.roads["GM"]['display'] + "  " + (grid.roads["MN"]['display'] + " ") * 4 + grid.roads["HN"]['display'] + grid.settlement_locs["N"]["display"] + (" " * 9) + str(grid.tiles["S5"]["number"]) + (" " * 9 if len(str(grid.tiles["S5"]["number"])) == 1 else " " * 8) + grid.settlement_locs["O"]["display"] +
" " + grid.roads["IO"]['display'] + " " + (grid.roads["OP"]['display'] + " ") * 4 + grid.roads["JP"]['display'] + " " + grid.settlement_locs["P"]["display"] + (" " * 8) + str(grid.tiles["S6"]["number"]) + (" " * 11 if len(str(grid.tiles["S6"]["number"])) == 1 else " " * 10) + grid.roads["KQ"]['display']
+ " " + grid.settlement_locs["Q"]["display"] + "\n"
)

    grid_part_2 = (
#line 20
(" " * 17) + grid.roads["LR"]['display'] + (" " * ((24 - len(str(grid.tiles["S4"]["biome"])))//2)) + grid.tiles["S4"]["biome"] + (" " * 10 if grid.tiles["S4"]["biome"] != "desert" else " " * 9) + grid.roads["MS"]['display'] + (" " * 14) + grid.roads["NT"]['display'] +
(" " * ((22 - len(str(grid.tiles["S5"]["biome"])))//2)) + grid.tiles["S5"]["biome"] + (" " * 9 if grid.tiles["S5"]["biome"] != "desert" else " " * 8) + grid.roads["OU"]['display'] + (" " * 13) + grid.roads["PV"]['display'] +
(" " * ((22 - len(str(grid.tiles["S6"]["biome"])))//2)) + grid.tiles["S6"]["biome"] + (" " * 9 if grid.tiles["S6"]["biome"] != "desert" else " " * 8) + grid.roads["QW"]['display'] + "\n" +
#line 21 & 22
(" " * 18) + grid.roads["LR"]['display'] + (" " * 10) + "S4" + (" " * 10) + grid.roads["MS"]['display'] + (" " * 16) + grid.roads["NT"]['display'] + (" " * 9) + "S5" + (" " * 9) + grid.roads["OU"]['display'] + (" " * 15) + grid.roads["PV"]['display'] 
+ (" " * 9) + "S6" + (" " * 9) + grid.roads["QW"]['display'] + "\n\n" +
#line 23
(" " * 20) + grid.roads["LR"]['display'] + (" " * 18) + grid.roads["MS"]['display'] + (" " * 7) + KAOMOJIS[grid.tiles["S7"]["biome"]] + (" " * 7) + grid.roads["NT"]['display'] + (" " * 16) + grid.roads["OU"]['display'] + (" " * 7) + KAOMOJIS[grid.tiles["S8"]["biome"]]  + (" " * 6) + grid.roads["PV"]['display'] +
(" " * 16) + grid.roads["QW"]['display'] + "\n" +
#line 24
(" " * 3) + "2:1 wood port - " + grid.settlement_locs["R"]["display"] + " " + grid.roads["LR"]['display'] + "  " + (grid.roads["RS"]['display'] + " ") * 4 + grid.settlement_locs["S"]["display"] + " " + grid.roads["MS"]['display'] + (" " * 10) + str(grid.tiles["S7"]["number"]) + 
(" " * 8 if len(str(grid.tiles["S7"]["number"])) == 1 else " " * 7) + grid.settlement_locs["T"]["display"] + "  " + grid.roads["NT"]['display'] + "  " + (grid.roads["TU"]['display'] + " ") * 4 + grid.roads["OU"]['display'] + " " + grid.settlement_locs["U"]["display"] +
(" " * 8) + str(grid.tiles["S8"]["number"]) + (" " * 8 if len(str(grid.tiles["S8"]["number"])) == 1 else " " * 7) + grid.settlement_locs["V"]["display"] + " " + grid.roads["PV"]['display'] + " " + (grid.roads["VW"]['display'] + " ") * 4 + " " + grid.roads["QW"]['display'] + 
grid.settlement_locs["W"]["display"] +  " _ _ _  2:1 sheep port" + "\n" +
#line 25
(" " * 8) + "\\" + (" " * 12) + grid.roads["RX"]['display'] + (" " * 16) + grid.roads["SY"]['display'] + (" " * ((22 - len(str(grid.tiles["S7"]["biome"])))//2)) + grid.tiles["S7"]["biome"] + 
(" " * (((22-len(str(grid.tiles["S7"]["biome"])))//2) + (1 if len(str(grid.tiles["S7"]["biome"]))%2 != 0 else 0))) + grid.roads["TZ"]['display'] + (" " * 14) + grid.roads["Ua"]['display'] +
(" " * ((21 - len(str(grid.tiles["S8"]["biome"])))//2)) + grid.tiles["S8"]["biome"] + 
(" " * (((21-len(str(grid.tiles["S8"]["biome"])))//2) + (1 if len(str(grid.tiles["S8"]["biome"]))%2 != 1 else 0))) + grid.roads["Vb"]['display'] + (" " * 14) + grid.roads["Wc"]['display'] + "         /\n" +
#line 26
(" " * 9) + "\\" + (" " * 10) + grid.roads["RX"]['display'] + (" " * 18) + grid.roads["SY"]['display'] + (" " * 9) + "S7" + (" " * 9) + grid.roads["TZ"]['display'] + (" " * 16) + grid.roads["Ua"]['display'] + (" " * 8) + "S8" + (" " * 9) + 
grid.roads["Vb"]['display'] + (" " * 16) + grid.roads["Wc"]['display'] + "       /" + "\n" +
#line 27
(" " * 10) + "\\" + (" " * 110) + "/" + "\n" +
#line 28
(" " * 11) + "\\" + (" " * 6) + grid.roads["RX"]['display'] + (" " * 8) + KAOMOJIS[grid.tiles["S9"]["biome"]] + (" " * 8) + grid.roads["SY"]['display'] + (" " * 16) + 
grid.roads["TZ"]['display'] + (" " * 6) + KAOMOJIS[grid.tiles["S10"]["biome"]] + (" " * 8) + grid.roads["Ua"]['display']
+ (" " * 15) + grid.roads["Vb"]['display'] + (" " * 7) + KAOMOJIS[grid.tiles["S11"]["biome"]] + (" " * 7) + grid.roads["Wc"]['display'] + "   /" + "\n" +
#line 29
(" " * 12) + "\\  " + grid.settlement_locs["X"]["display"] + " " + grid.roads["RX"]['display'] + (" " * 12) + str(grid.tiles["S9"]["number"]) + 
(" " * 9 if len(str(grid.tiles["S9"]["number"])) == 1 else " " * 8) 
+ grid.settlement_locs["Y"]["display"] + " " + grid.roads["SY"]['display'] + " " + (grid.roads["YZ"]['display'] + " ") * 4 + grid.settlement_locs["Z"]["display"] + 
grid.roads["TZ"]['display'] + (" " * 10) + str(grid.tiles["S10"]["number"]) + (" " * 9 if len(str(grid.tiles["S10"]["number"])) == 1 else " " * 8) + 
grid.settlement_locs["a"]["display"] + " " + grid.roads["Ua"]['display'] + (" " + grid.roads["ab"]['display']) * 4 + grid.settlement_locs["b"]["display"] + grid.roads["Vb"]['display'] +
(" " * 10) + str(grid.tiles["S11"]["number"]) + (" " * 11 if len(str(grid.tiles["S11"]["number"])) == 1 else " " * 10) + grid.roads["Wc"]['display'] + " " + grid.settlement_locs["c"]["display"] + "\n" +
#line 30
(" " * 17) + grid.roads["Xd"]['display'] + (" " * ((24 - len(str(grid.tiles["S9"]["biome"])))//2)) + grid.tiles["S9"]["biome"] + (" " * (((24-len(str(grid.tiles["S9"]["biome"])))//2) + (1 if len(str(grid.tiles["S9"]["biome"]))%2 != 0 else 0))) 
+ grid.roads["Ye"]['display'] + (" " * 14) + grid.roads["Zf"]['display'] + (" " * ((22 - len(str(grid.tiles["S10"]["biome"])))//2)) + grid.tiles["S10"]["biome"] + 
(" " * (((22-len(str(grid.tiles["S10"]["biome"])))//2) + (1 if len(str(grid.tiles["S10"]["biome"]))%2 != 0 else 0))) + grid.roads["ag"]['display'] + (" " * 13) + grid.roads["bh"]['display'] +
(" " * ((22 - len(str(grid.tiles["S11"]["biome"])))//2)) + grid.tiles["S11"]["biome"] + 
(" " * (((22-len(str(grid.tiles["S11"]["biome"])))//2) + (1 if len(str(grid.tiles["S11"]["biome"]))%2 != 0 else 0))) + grid.roads["ci"]['display'] + "\n"
    
    )

    grid_part_3 = (
#line 31 & 32
(" " * 18) + grid.roads["Xd"]['display'] + (" " * 10) + "S9" + (" " * 10) + grid.roads["Ye"]['display'] + (" " * 16) + grid.roads["Zf"]['display'] + (" " * 8) + "S10" + (" " * 9) + grid.roads["ag"]['display'] + (" " * 15) + grid.roads["bh"]['display'] + (" " * 8) + "S11" + (" " * 9) + grid.roads["ci"]['display'] + "\n\n" +
#line 33
(" " * 20) + grid.roads["Xd"]['display'] + (" " * 18) + grid.roads["Ye"]['display'] + (" " * 7) + KAOMOJIS[grid.tiles["S12"]["biome"]] + (" " * 7) + grid.roads["Zf"]['display'] + (" " * 16) + grid.roads["ag"]['display'] + (" " * 6) + KAOMOJIS[grid.tiles["S13"]["biome"]] + (" " * 7) + 
grid.roads["bh"]['display'] + (" " * 16) + grid.roads["ci"]['display']
+ "\n" +
#line 34
(" " * 19) + grid.settlement_locs["d"]["display"] + " " + grid.roads["Xd"]['display'] + "  " + (grid.roads["de"]['display'] + " ") * 4 + grid.settlement_locs["e"]["display"] + " " + grid.roads["Ye"]['display'] + (" " * 10) + 
str(grid.tiles["S12"]["number"]) + (" " * 9 if len(str(grid.tiles["S12"]["number"])) == 1 else " " * 8) + grid.settlement_locs["f"]["display"] + " " + grid.roads["Zf"]['display'] + " " + (grid.roads["fg"]['display'] + " ") * 4 + grid.settlement_locs["g"]["display"] + grid.roads["ag"]['display'] +
(" " * 10) + str(grid.tiles["S13"]["number"]) + (" " * 8 if len(str(grid.tiles["S13"]["number"])) == 1 else " " * 7) + grid.settlement_locs["h"]["display"] + " " + grid.roads["bh"]['display'] + " " + (grid.roads["hi"]['display'] + " ") * 4 + " " + grid.roads["ci"]['display'] + " " 
+ grid.settlement_locs["i"]["display"] + "\n" +
#line 35
(" " * 21) + grid.roads["dj"]['display'] + (" " * 16) + grid.roads["ek"]['display'] + (" " * ((23 - len(str(grid.tiles["S12"]["biome"])))//2)) + grid.tiles["S12"]["biome"] + 
(" " * (((21-len(str(grid.tiles["S12"]["biome"])))//2) + (1 if len(str(grid.tiles["S12"]["biome"]))%2 != 1 else 0))) + grid.roads["fl"]['display'] + (" " * 14) + grid.roads["gm"]['display']
+ (" " * ((21 - len(str(grid.tiles["S13"]["biome"])))//2)) + grid.tiles["S13"]["biome"] + 
(" " * (((21-len(str(grid.tiles["S13"]["biome"])))//2) + (1 if len(str(grid.tiles["S13"]["biome"]))%2 != 1 else 0))) + grid.roads["hn"]['display'] + (" " * 14) + grid.roads["io"]['display'] + "\n" +
#line 36 & 37
(" " * 20) + grid.roads["dj"]['display'] + (" " * 18) + grid.roads['ek']['display'] + (" " * 8) + "S12" + (" " * 9) + grid.roads['fl']['display'] + (" " * 16) + grid.roads['gm']['display'] + (" " * 8) + "S13" + (" " * 8) + grid.roads['hn']['display'] + (" " * 16) + grid.roads['io']['display'] + "\n\n" +
#line 38 
(" " * 18) + grid.roads['dj']['display'] + (" " * 8) + KAOMOJIS[grid.tiles["S14"]["biome"]] + (" " * 8) + grid.roads['ek']['display'] + (" " * 16) + grid.roads['fl']['display'] + 
(" " * 7) + KAOMOJIS[grid.tiles["S15"]["biome"]] + (" " * 7) + grid.roads['gm']['display'] + (" " * 15) + grid.roads['hn']['display'] + (" " * 7) + KAOMOJIS[grid.tiles["S16"]["biome"]] + (" " * 7)
+ grid.roads['io']['display'] + "\n" +
#line 39
(" " * 15) + grid.settlement_locs["j"]["display"] + " " + grid.roads['dj']['display'] + (" " * 11) + str(grid.tiles["S14"]["number"]) + (" " * 10 if len(str(grid.tiles["S14"]["number"])) == 1 else " " * 9) + grid.settlement_locs["k"]["display"]
+ " " + grid.roads['ek']['display'] + " " + (grid.roads["kl"]['display'] + " ") * 4 + grid.settlement_locs["l"]["display"] + grid.roads['fl']['display'] + (" " * 10) + str(grid.tiles["S15"]["number"]) + (" " * 9 if len(str(grid.tiles["S15"]["number"])) == 1 else " " * 8)
+ grid.settlement_locs["m"]["display"] + " " + grid.roads['gm']['display'] + " " + (grid.roads["mn"]['display'] + " ") * 4 + grid.roads['hn']['display'] + grid.settlement_locs["n"]["display"] + (" " * 9) + str(grid.tiles["S16"]["number"]) + 
(" " * 11 if len(str(grid.tiles["S16"]["number"])) == 1 else " " * 10) + grid.roads['io']['display'] + " " + grid.settlement_locs["o"]["display"] + "\n" +
#line 40
(" " * 17) + grid.roads['jp']['display'] + (" " * ((24 - len(str(grid.tiles["S14"]["biome"])))//2)) + grid.tiles["S14"]["biome"] +
(" " * (((24-len(str(grid.tiles["S14"]["biome"])))//2) + (1 if len(str(grid.tiles["S14"]["biome"]))%2 != 0 else 0))) + grid.roads['kq']['display'] + (" " * 14) + grid.roads['lr']['display'] +
(" " * ((22 - len(str(grid.tiles["S15"]["biome"])))//2)) + grid.tiles["S15"]["biome"] + 
(" " * (((22-len(str(grid.tiles["S15"]["biome"])))//2) + (1 if len(str(grid.tiles["S15"]["biome"]))%2 != 0 else 0))) + grid.roads['ms']['display'] + (" " * 13) + grid.roads['nt']['display'] +
(" " * ((22 - len(str(grid.tiles["S16"]["biome"])))//2)) + grid.tiles["S16"]["biome"] + 
(" " * (((22 - len(str(grid.tiles["S16"]["biome"])))//2) + (1 if len(str(grid.tiles["S16"]["biome"]))%2 != 0 else 0))) + grid.roads['ou']['display'] + "\n" +
#line 41 
(" " * 14) + "/" + (" " * 3) + grid.roads['jp']['display'] + (" " * 9) + "S14"  + (" " * 10) + grid.roads['kq']['display'] + (" " * 16) + grid.roads['lr']['display'] + (" " * 8) + "S15" + (" " * 9) + grid.roads['ms']['display'] 
+ (" " * 15) + grid.roads['nt']['display'] + (" " * 8) + "S16" + (" " * 9) + grid.roads['ou']['display'] + 
(" " * 3) + "\\" + "\n" +
#line 42
(" " * 13) + "/" + (" " * 107) + "\\" + "\n" 
            )

    grid_part_4 = (
#line 43
(" " * 12) + "/" + (" " * 7) + grid.roads['jp']['display'] + (" " * 18) + grid.roads['kq']['display'] + (" " * 7) + KAOMOJIS[grid.tiles["S17"]["biome"]] + 
(" " * 7) + grid.roads['lr']['display'] + (" " * 16) + grid.roads['ms']['display'] + (" " * 6) + KAOMOJIS[grid.tiles["S18"]["biome"]] + (" " * 7)
+ grid.roads['nt']['display'] + (" " * 16) + grid.roads['ou']['display'] + (" " * 7) + "\\" + "\n" +
#line 44
" 2:1 brick port _  " + grid.settlement_locs["p"]["display"] + " " + grid.roads['jp']['display'] + " " + (grid.roads["pq"]['display'] + " ") * 4 + " " 
+ grid.settlement_locs["q"]["display"] + " " + grid.roads['kq']['display'] + (" " * 11) + str(grid.tiles["S17"]["number"]) +
(" " * 8 if len(str(grid.tiles["S17"]["number"])) == 1 else " " * 7) + grid.settlement_locs["r"]["display"] + " " + grid.roads['lr']['display'] + " " + 
(grid.roads["rs"]['display'] + " ") * 4 + grid.settlement_locs["s"]["display"] + grid.roads['ms']['display'] + (" " * 10) + 
str(grid.tiles["S18"]["number"]) + (" " * 8 if len(str(grid.tiles["S18"]["number"])) == 1 else " " * 7) + grid.settlement_locs["t"]["display"] + " " + grid.roads['nt']['display'] + 
" " + (grid.roads["tu"]['display'] + " ") * 4 + " " + grid.roads['ou']['display'] +
grid.settlement_locs["u"]["display"] + "  _ _ 3:1 port" + "\n" +
#line 45
(" " * 38) + grid.roads['qv']['display'] + (" " * ((22 - len(str(grid.tiles["S17"]["biome"])))//2)) + grid.tiles["S17"]["biome"] + 
(" " * (((22 - len(str(grid.tiles["S17"]["biome"])))//2) + (1 if len(str(grid.tiles["S17"]["biome"]))%2 != 0 else 0))) + grid.roads['rw']['display'] + (" " * 14) + grid.roads['sx']['display'] +
(" " * ((21 - len(str(grid.tiles["S18"]["biome"])))//2)) + grid.tiles["S18"]["biome"] + (" " * (((21 - len(str(grid.tiles["S18"]["biome"])))//2) 
+ (1 if len(str(grid.tiles["S18"]["biome"]))%2 != 1 else 0))) + grid.roads['ty']['display'] + "\n" +
#line 46 & 47
(" " * 39) + grid.roads['qv']['display'] + (" " * 8)  + "S17" + (" " * 9) + grid.roads['rw']['display'] + (" " * 16) + grid.roads['sx']['display'] + 
(" " * 8) + "S18" + (" " * 8) + grid.roads['ty']['display'] + "\n\n" +
#line 48
(" " * 41) + grid.roads['qv']['display'] + (" " * 16) + grid.roads['rw']['display'] + (" " * 7) + KAOMOJIS[grid.tiles["S19"]["biome"]] + (" " * 7) + 
grid.roads['sx']['display'] + (" " * 15) + grid.roads['ty']['display'] + "\n" +
#line 49
(" " * 42) + grid.roads['qv']['display'] + grid.settlement_locs["v"]["display"] + " " + (grid.roads["vw"]['display'] + " ") * 4 + grid.settlement_locs["w"]["display"] + 
(" " * 10) + str(grid.tiles["S19"]["number"]) + (" " * 9 if len(str(grid.tiles["S19"]["number"])) == 1 else " " * 8) + grid.settlement_locs["x"]["display"] + " " + 
grid.roads['sx']['display'] + " " + (grid.roads["xy"]['display'] + " ") * 4 + grid.roads['ty']['display'] + " " 
+ grid.settlement_locs["y"]["display"] + "\n" +
#line 50
(" " * 58) + grid.roads['wz']['display'] +(" " * ((21 - len(str(grid.tiles["S19"]["biome"])))//2)) + grid.tiles["S19"]["biome"] + 
(" " * (((21 - len(str(grid.tiles["S19"]["biome"])))//2) + (1 if len(str(grid.tiles["S19"]["biome"]))%2 != 1 else 0))) + grid.roads[quick_reorder("x+")]['display'] + "\n" +
#line 51
(" " * 44) + "\\" + (" " * 11) + "/  " + grid.roads['wz']['display'] + (" " * 8) + "S19" + (" " * 8) + grid.roads[quick_reorder("x+")]['display'] + "  \\          /" + "\n" +
#line 52
(" " * 45) + "\\         /" + (" " * 27) + "\\" + "        " + "/" + "\n" +
#line 53
(" " * 46) + "\\       /      " + grid.roads['wz']['display'] + "               " + grid.roads[quick_reorder("x+")]['display'] + "      " + "\\" + "      " + "/" + "\n" +
#line 54
(" " * 45) + "2:1 ore port     " + grid.roads['wz']['display'] + grid.settlement_locs["z"]["display"] + " " + (grid.roads["+z"]['display'] + " ") * 4 + grid.settlement_locs["+"]["display"] 
+ "      3:1 port"

    )

    quick_grid_access = [grid_part_1, grid_part_2, grid_part_3, grid_part_4]

    for grid in quick_grid_access:
        print(grid, end="")
    print("\n")
  
        
def print_board(player_info : PlayerInfo, grid : Grid):
    """Prints out basic information (visual display for what players need to see during their turns)"""

    print("________ WELCOME TO THE WORLD OF CATAN. WHERE WILL YOU SETTLE TODAY? ________\n")
    print(f"˗ˋˏ$ˎˊ˗ GAME BANK ˗ˋˏ$ˎˊ˗")
    game_bank = player_info.game_bank
    for resource in game_bank["resources"]:
        print(f'{resource} : {game_bank["resources"][resource]}', end="  ||  ")
    print("\n")
    for card in CARDS:
        print(f'{card} : {game_bank["cards"].count(card)}', end="  ||  ")
    print("\n")
    for player in player_info.quick_key:
        print(ansi_stitching(player_info.player_dicts[player]['colour'], 
f"Player {player} ({player_info.player_dicts[player]['name']}) : {calculate_points(player_info, player, 1)} public VPs, {calculate_hand_size(player_info, player)} resource cards"), end="  ||  ")
    print("\n")

    print_grid(grid)

    print(f"The robber is currently pillaging the citizens of {grid.robber} and stealing all their {grid.tiles[grid.robber]['biome']}...")


##COLOURS


def ansi_stitching(colour : list, text : str) -> str:
	"""Edits the string's value with an ANSI code that imbues it with pretty colours :3"""
	
	coloured_ver = "\x1b[38;2;"
	reps = 0
	for value in colour:
		coloured_ver += str(value)
		reps += 1
		if reps < 3:
			coloured_ver += ";"
	
	coloured_ver += "m" + text + "\x1b[0m"

	return coloured_ver
    
    
def add_colours(player_info) -> tuple[list, dict]:
        """Calls all the functions initially needed for the initialising of player dictionaries"""
        quick_key, player_dicts = player_info.quick_key, player_info.player_dicts
        
        player_colours = assign_player_colours(quick_key)
        for player, colour in zip(player_dicts, player_colours):
                player_dicts[player]["colour"] = colour
        
        return player_dicts
    
    
def assign_player_colours(quick_key : list) -> list:
    """Iterates through each player and makes sure they have a colour assigned"""
    
    preset_colours = [[1, 201, 184], [252, 210, 1], [252, 84, 1], [210, 1, 252]]#this variable only needs to be temporary
    player_colours = []
    new_colour = False
    for player in quick_key:#iterates through players
        action = ""
        while not action in ["y", "n"]:#indefinite iteration
            print(' We strongly recommend making your own, since the default may be similar to the colour someone else has chosen.' if new_colour else '')
            action = input("Would you like to customise your own colour? (If not, you'll get a premade one!)" + 
" Type 'Y' for yes and 'N' for no.\n˚₊ · »-♡→ ").strip().lower()#a prompt, as the default may be too similar and undifferentiable from a pre-chosen colour
            if action == "y":
                player_colours.append(choose_colour())
                new_colour = True
            elif action == "n":
                print(ansi_stitching(preset_colours[player - 1], "This is your assigned colour!"))
                player_colours.append(preset_colours[player - 1])
                time.sleep(0.3)
            else:
                print("Sorry, please either type 'y' or 'n'.")
        clear_screen()
                            
    print_player_colours(quick_key, player_colours)
    return player_colours   
    
    
def choose_colour() -> list:
    """Get a player's colours by iterating through red, blue, and green."""
    
    player_colour = []
    satisfied = False
    while not satisfied:
        get_colour(player_colour)   
                                
        confirmed = False
        while not confirmed:
            confirmed, satisfied = confirm_colour(player_colour, satisfied, confirmed)

    clear_screen()
    return player_colour
    
    
def confirm_colour(player_colour, satisfied, confirmed) -> tuple[bool, bool]:
        confirm = input(ansi_stitching(player_colour, """This is what your colour looks like - are you sure you want it? 
Type 'Y' for yes and 'N' for no. 
Please make sure all other players can see this colour.\n""") + "> ").strip()
        if confirm == "N":
                player_colour = []
                confirmed = True
        elif confirm == "Y":
                satisfied = True
                confirmed = True
        else:
                print("Please type either 'Y' or 'N'. This is case sensitive.")
                
        return confirmed, satisfied
    
    
def print_player_colours(quick_key, player_colours):
        """Prints the colour for each player"""
        
        for player in quick_key:
                print(ansi_stitching(player_colours[player - 1], f"Player {player}, this is your colour."))
                time.sleep(0.3)
                
                
def get_colour(player_colour : list) -> list:
    for colour in COLOUR_CODES:#iterate through colours               
        valid_input = False
        while not valid_input:#makes sure that it doesn't end without getting the right colour
            action = input(ansi_stitching(COLOUR_CODES[colour], f"‧₊˚♪ 𝄞₊˚⊹ What value would you like to use for {colour}? ‧₊˚♪ 𝄞₊˚⊹\n˚₊ · »-♡→ ")).strip().lower()
            try:
                if int(action) <= 255:
                    player_colour.append(int(action))
                    valid_input = True
                else:
                    print("Sorry; RGB values only go up to 255.")
                    
            except ValueError:
                print("Please input a valid integer, in arabic numerals, within the range of 0 to 255.")
                                    
    return player_colour
    

##PLAYER INFORMATION/DICTIONARIES
  
  
def create_player_info() -> tuple[list, dict]:
    """Obtains player information needed to initialise variables"""
    
    quick_key = create_player_key(get_player_number())
    player_dicts = {}#the player dictionaries are also stored in dictionaries
    player_names = []
    for player in quick_key:
        player_dicts[player] = {}
        name = get_player_name(player, player_names)
        player_dicts[player]['name'] = name
        player_names.append(name)
        player_dicts[player]['password'] = get_player_password()
    return quick_key, player_dicts
    
    
def create_player_key(player_number : int) -> list:
    """Creates a key which can be used to iterate through players or find player number"""
    
    #iterates through each player and appends their ID to the quick key
    quick_key = []
    for player in range(player_number):
        quick_key.append(player + 1)
        
    return quick_key


def get_player_number() -> int:
    """Gets the number of players, repeats until valid"""
    
    player_number = 0
    while not player_number in [3, 4]:#only 3 and 4 players are accepted so I simply created a list to make the conditional shorter.
        try:
            player_number = int(input("How many people are playing? ⋆˚✿🍒𐙚⋆˚\n˚₊ · »-♡→ ").strip()) 
            if not player_number in [3, 4]:
                print("You can only play with 3 or 4 people.")
                
        except ValueError:#as not entering an integer would lead the 'int' to return a value error (the types do not align)
            print("Enter an integer (3 or 4) please.")
            
    return player_number


def get_player_name(player : int, player_names : list) -> str:
    """Gets the name of the current player and checks the length and if it is composed of numbers."""
    blacklist = ['cancel', 'x', '1', '2', '3', '4', '0', 'esc', 'g', 'b', 'bank', 'game bank']
    valid_name = False
    while not valid_name:
        player_name = input(f"Player {player}, enter your name!\n˚₊ · »-♡→ ").strip().lower()
        if player_name in player_names:
            #checks if name has already been created by accessing past names
            print("... That name's already owned. Choose something else.")
        elif player_name.isdigit():
            print("Sorry, you're not allowed a name consisting of only numbers, as this will cause problems later.")
        elif len(player_name) > 8:
            print("Please set a shorter name. Sorry if your name is really that long, but it's hard to display.")
        else:
            if player_name in blacklist:
                print("That name is blacklisted.")
            else:
                valid_name = True
            
    return player_name   


def add_keys(player_info : PlayerInfo) -> dict:
    """Adds keys to each existing player dictionary"""
    
    player_dicts = player_info.player_dicts

    for player in player_info.quick_key:
        player_dicts[player]['constructs'] = {"settlement": 3, "city": 4, "road": 13, "settlement list" : [], "city list" : [], "road list" : []}#technically they have more but they use it up initially - so it's easier to do this
        
        player_dicts[player]['resources'] = {}
        for resource in RESOURCES:
            player_dicts[player]['resources'][resource] = 0
            
        player_dicts[player]['cards'] = {}
        for dev_card in CARDS:
            player_dicts[player]['cards'][dev_card] = 0
        player_dicts[player]['army'] = 0
            
    return player_dicts
    

def get_player_password() -> str:
    """Gets a password and checks if it's valid."""
    
    while True:
        password = input("Please enter a password; it'll be used to check for your consent later. Keep it short but memorable," + 
                            "and make sure it's not a password you use for important sites.\n˚₊ · »-♡→ ")
        
        if len(password) > 7:
            print("That password is way too long. Keep it to 7 or below characters.")
        else:
            print("Okay. At all costs, do NOT forget your password!")
            time.sleep(1)
            break
            
    clear_screen()#Clears screen for privacy
    
    return password
    
    
def print_deck(player_info, player=0):
    """Prints the player's deck."""
    
    printee = player_info.player_turn if not player else player
    force_password(player_info, printee)
    
    print("---RESOURCE CARDS---")
    for resource in player_info.player_dicts[printee]['resources']:
        print(f"{resource} : {player_info.player_dicts[printee]['resources'][resource]}")
    print("\n---DEVELOPMENT CARDS---")
    for card in player_info.player_dicts[printee]['cards']:
        print(f"{card} : {player_info.player_dicts[printee]['cards'][card]}")
    

##DEVELOPMENT CARDS


def draw_development_card(player_info) -> tuple[PlayerInfo, bool]:
    """Draws a development card from the game bank with a simple pop method"""
    
    force_password(player_info)
    print("Make everyone else look away.")
    cards = player_info.game_bank['cards']
    if cards == []:
        print("The game bank has no more development cards. Sorry, you can't buy any!")
        return player_info, False
    random.shuffle(cards)
    card = cards.pop()
    print(f"You've drawn a {card} card!")
    player_info.player_dicts[player_info.player_turn]['cards'][card] += 1
    if card == 'VP card':
        print("You gained one secret VP.")
    
    return player_info, True


def execute_development_card(card, grid, player_info) -> tuple[PlayerInfo, Grid]:
    """Executes development card based on the card chosen"""
    
    if card == 'knight':
        grid.robber = place_robber(grid)
        player_info = steal_card(player_info, grid)
        player_info.player_dicts[player_info.player_turn]['army'] += 1
        print("Your army has grown. Congratulations, settler!")
    elif card == 'build road':
        for i in range(2):
            print(f"Free road no.{i}:")
            player_info, grid, trade = place_road(player_info, grid)
    elif card == 'year of plenty':
        player_info = year_of_plenty(player_info)
    elif card == 'monopoly':
        player_info = monopoly(player_info)
    elif card == 'VP card':
        print("VP cards cannot be played.")
        
    if card != 'VP card':
        player_info.player_dicts[player_info.player_turn]['cards'][card] -=1
    
    return player_info, grid


def choose_development_card(player_info) -> str:
    """Allows player to choose a development card"""
    
    player = player_info.player_turn
    force_password(player_info)
    player_cards = []
    for card in player_info.player_dicts[player]['cards']:
        if player_info.player_dicts[player]['cards'][card] >= 1:
            player_cards.append(card)
    if player_cards == []:
        print("You actually don't have any development cards, lols")
        return ""
    while True:
        action = input("Would you like to play one? Warning: once you confirm you CANNOT go back. These are the cards you can play: " + str(player_cards)[1:-1] + ".\n˚₊ · »-♡→ ")
        if action in ['y', 'yes', 'confirm']:
            break
        elif action in ['n', 'no', 'nope', 'x', 'cancel']:
            print("Good choice.")
            return ""
        else:
            print("You seem to be a bit mentally challenged right now. Type 'x' to leave or 'y' to continue ^^")
    
    card = choose_resource("Choose the card you'll play:\n˚₊ · »-♡→ ", player_cards)
    return card


def year_of_plenty(player_info) -> PlayerInfo:
    """This mechanic allows a player to take any 2 resource cards from the bank"""
    
    for i in range(2):
        possible_resources = []
        for resource in player_info.game_bank['resources']:
            if player_info.game_bank['resources'][resource] != 0:
                possible_resources.append(resource)
        if possible_resources == []:
            print("Sorry, the bank is kinda broke so you can't take a resource")
            return player_info
        while True:
            action = input("Which resource would you like to take from the bank?\n˚₊ · »-♡→ ").strip().lower()
            if action in possible_resources:
                print("Alright - you will now obtain 1 free card from the bank!")
                player_info = transfer_resources(player_info, {action : 1}, 0, 1)
                break
            elif action.isdigit():
                if int(action) >= 1 and int(action) <= len(possible_resources):
                    player_info = transfer_resources(player_info, {possible_resources[int(action) - 1] : 1}, 0, 1)
                    break
                else:
                    print("Not a valid number. Try entering the name of the resource.")
            elif action == 'l':
                for resource in possible_resources:
                    print(f"{possible_resources.index(resource) + 1}. {resource} : {player_info.game_bank['resources'][resource]}")
            else:
                print("Invalid entry. You can either enter the number on the list or the name of the resource you want. Type 'l' to see the possible trades.")
        
    return player_info


def monopoly(player_info) -> PlayerInfo:
    """Forcibly steals all of a chosen resource card from all players"""
    
    print("You've just stumbled on one of the most powerful cards in the game! Announce 1 of any resource to steal all copies of it from all players!")
    resource = choose_resource("Choose the resource you'd like to monopolise! (PS enter either the name of the resource or its number)\n˚₊ · »-♡→ ")
    tax_resources(player_info, resource)
    print("Forced collection complete. Returning now :)")
    
    return player_info
    
            
def choose_resource(message, list=[]) -> str:
    list = RESOURCES if list==[] else list
    while True:
        print("Here are the cards you can choose:")
        for resource in list:
            print(f"{list.index(resource) + 1}. {resource}")
        action = input(message).strip().lower()
        if action.isdigit():
            if int(action) >= 1 and int(action) <= len(list):
                return list[int(action) - 1]
            else:
                print("Not a valid integer selection")
        elif action in list:
            return action
        else:
            print("Oops, not a valid resource!")


def tax_resources(player_info, resource) -> PlayerInfo:
    """Goes through each player and forcibly hands all of the specified resource to the current player"""
    
    for player in player_info.quick_key:
        if player_info.player_dicts[player]['resources'][resource] == 0:
            print(f"Player {player} was unable to concede their {resource}.")
        else:
            player_info = trade_resources(player_info, {resource : player_info.player_dicts[player]['resources'][resource]}, player_info.player_turn, player)
            
    return player_info


##CARD TRANSFERS (RESOURCE CARDS)/TRADES
    

def discard_resource(player_info, player) -> PlayerInfo:
    """Lets player choose a resource to discard"""
    
    while True:
        action = input("Choose the resource you'd like to discard!\n˚₊ · »-♡→ ").strip().lower()
        resources = list(player_info.player_dicts[player]['resources'])
        try:
            action = int(action)
            if action <=5 and action > 0:
                print(f"You have chosen to discard {resources[action]}.")
            else:
                print("Yes, you are allowed to enter a number - but it must correspond to the relevant resource. (Number between 1 and 5.)")
        except ValueError:
            if action in resources:
                print(f"You have chosen to discard {action}.")
            elif action == 'check':
                print_deck(player_info, player)
            elif action == 'cls':
                clear_screen()
            else:
                print("That resource doesn't exist.")
        owned = player_info.player_dicts[player]['resources'][action]
        if owned > 0:
            while True:
                discard_num = input(f"How many would you like to discard?\n˚₊ · »-♡→ ").strip()
                if not discard_num.isdigit():
                    print("Write your POSITIVE number in arabic numerals.")
                else:
                    if int(discard_num) > owned:
                        print("That number's too large!")
                    else:
                        break
        
        print("Confirmed. Transferring resources to the bank...")
        resources = {action : discard_num}
        player_info = transfer_resources(player_info, resources, player)
        break
                                    
    return player_info


def transfer_resources(player_info : PlayerInfo, resources : dict, player=0, add=0) -> PlayerInfo:
    """Gives/takes resources to/from players to game bank. Pass the resources into this function as follows: {Resource : number}. Automatically assumes that you are subtracting if nothing is passed into the function."""
    
    player=player_info.player_turn if not player else player
    for resource in resources:
        if add:
            player_info.player_dicts[player]['resources'][resource] += resources[resource]
            player_info.game_bank['resources'][resource] -= resources[resource]
        else:
            player_info.player_dicts[player]['resources'][resource] -= resources[resource]
            player_info.game_bank['resources'][resource] += resources[resource]
            
    return player_info


def trade_resources(player_info : PlayerInfo, resources : dict, recipient, donor=0) -> PlayerInfo:
    """This subroutine facilitates trade but doesn't check if the trade is possible - so check before calling"""
    
    donor = player_info.player_turn if donor == 0 else donor
    
    for resource in resources:
        player_info.player_dicts[donor]['resources'][resource] -= resources[resource]
        player_info.player_dicts[recipient]['resources'][resource] += resources[resource]
        print(f"{resources[resource]} {'has' if resources[resource] == 1 else 'have'} been transferred to player {recipient} from player {donor}'s account!")
    print("Thanks for using Catan's trade service. See you again soon!")
    
    return player_info
    
    
def steal_one(player_info, victim) -> str:
    """Randomises the victim's hand and forces the player to select one."""
    
    hand_list = []
    for resource in player_info.player_dicts[victim]['resources']:
        hand_list.extend([resource] * player_info.player_dicts[victim]['resources'][resource])
    if hand_list == []:
        print("The victim you've chosen has an empty hand!")
        return ""
    else:
        random.shuffle(hand_list)
        while True:
            action = input(f"Pick a number from 1 to {len(hand_list)}.\n˚₊ · »-♡→ ").strip().lower()
            try:
                if int(action) >= 1 and int(action) <= len(hand_list):
                    return hand_list[int(action) - 1]
                else:
                    print("Not a valid number. Follow the prompt please.")
            except ValueError:
                print("Please enter your chosen number in arabic numerals.")
                
                
def choose_trade(player_info, grid) -> PlayerInfo:
    """Calls a trade. Only works on the game bank"""
    
    print("Looks like you want to make a trade?")
    force_password(player_info)
    while True:
        for player in player_info.quick_key:
            if player != player_info.player_turn:
                print(f"Player {player} (aka '{player_info.player_dicts[player]['name']}')")
        print("Or type 'g' for the game bank.")
        names_list = []
        for player in player_info.quick_key:
            if player != player_info.player_turn:
                names_list.append(player_info.player_dicts[player]['name'])
        names_list.append('g')
        action = input("˚₊ · »-♡→ ")
        if action.isdigit():
            if int(action) in player_info.quick_key:
                print("Ummmmmmm I scrapped the player player thing so if you want to do a trade do it with the bank sry")
            else:
                print("Invalid player")
        elif action in names_list:
            if action == 'g':
                player_info = trade_bank(player_info, grid)
            else:
                print("In all honesty, I don't have time to make a player-player trade function before tomorrow." +
"\nBut nobody ever accepts trades anyways, so... just type cancel please TwT")
                """for player in player_info.quick_key:
                    if player_info.player_dicts[player]['name'] == action:
                        trader = player"""
        elif action == 'cancel':
            return player_info
        else:
            print("Not eligible. Try again.")
            
        return player_info


def trade_bank(player_info, grid) -> PlayerInfo:
    
    port_claims = []
    player = player_info.player_turn
    for settlement in player_info.player_dicts[player]['constructs']['settlement list']:
        if grid.settlement_locs[settlement]['port']:
            port_claims.append(grid.settlement_locs[settlement]['port'])
    port_claims = list(set(port_claims))
    port_claims.append("4:1 trade")
    while True:
        for port in port_claims:
            print(f"{port_claims.index(port) + 1}. {port}")
        action = input("Select a port:\n˚₊ · »-♡→ ")
        if action.isdigit():
            if int(action) > 0 and int(action) <= len(port_claims):
                port = port_claims[int(action) - 1]
                break
            else:
                print("Invalid integer selection.")
        elif action in port_claims:
            port = action
            break
        elif action in ['x', 'cancel']:
            return player_info
        else:
            print("That's not a valid input. Either type the number of the port you want to select, its name, or 'x' to leave.")
    if port[0] == '4':
        player_info = default_trade(player_info, 4)
    elif port[0] == '3':
        player_info = default_trade(player_info, 3)
    else:
        player_info = specialised_trade(player_info, port)
        
    return player_info
      
        
def default_trade(player_info, num) -> PlayerInfo:
    """Allows 4:1 and 3:1 trades"""
    
    resource_list = []
    for resource in player_info.player_dicts[player_info.player_turn]['resources']:
        if player_info.player_dicts[player_info.player_turn]['resources'][resource] >= num:
            resource_list.append(resource)
    bank = []
    for resource in player_info.game_bank['resources']:
        if player_info.game_bank['resources'][resource] >= 1:
            bank.append(resource)
    if resource_list == []:
        print(f"You don't have enough resource cards to make a default trade. You need {num}.")
        return player_info
    elif bank == []:
        print("The bank is broke and so can't fund anything... Sorry~")
        print("Trade canceled forcibly!")
        return player_info
    else:
        while True:
            print("The resources that you can trade with the bank for are:")
            for resource in resource_list:
                print(resource)
            print("The resources that the bank can reward you with are:")
            for resource in bank:
                print(resource)
            action = input("Would you like to confirm the trade? Warning: you can't leave after you say yes, so be absolutely sure. Type 'y' for yes, and 'n' for no.\n˚₊ · »-♡→ ").strip().lower()
            if action in ['x', 'cancel', 'no', 'n']:
                print("Okay, good choice!")
                return player_info
            elif action in ['y', 'yes', 'continue']:
                break
            else:
                print("Invalid input. Check for spelling errors?")
        give = choose_resource("Choose the resource you'd like to give away.\n˚₊ · »-♡→ ", resource_list)
        
        obtain = choose_resource("Choose the resource the bank will reward you with:\n˚₊ · »-♡→ ", bank)
        player_info.player_dicts[player_info.player_turn]['resources'][give] -= num
        player_info.game_bank['resources'][give] += num
        player_info.player_dicts[player_info.player_turn]['resources'][obtain] += 1
        player_info.game_bank['resources'][obtain] -= 1
        
        return player_info


def specialised_trade(player_info, port) -> PlayerInfo:
    """Facilitates 2:1 trade"""
    
    for resource in RESOURCES:
        if resource[:3] in port:
            give = resource
    available_resources = []
    for resource in player_info.game_bank['resources']:
        if player_info.game_bank['resources'][resource] >= 1:
            available_resources.append(resource)
    if give in available_resources:
        available_resources.remove(give)
    if available_resources == []:
        print("The bank is broke and so can't fund anything... Sorry~")
        print("Trade canceled forcibly!")
        return player_info
    trader = player_info.player_turn
            
    if player_info.player_dicts[trader]['resources'][give] < 2:
        print(f"You actually don't have enough {give}; you have {player_info.player_dicts[trader]['resources'][give]} only.")
        print("Trade unsuccessful - better luck next time~")
        return player_info
    obtain = choose_resource("Choose the resource the bank will reward you with:\n˚₊ · »-♡→ ", available_resources)
    
    player_info.player_dicts[trader]['resources'][give] -= 2
    player_info.game_bank['resources'][give] += 2
    player_info.player_dicts[trader]['resources'][obtain] += 1
    player_info.game_bank['resources'][obtain] -= 1
    
    return player_info


##GRID GENERATION/DYNAMIC BOARD


def create_tiles() -> dict:
    """Creates one of each tile in a dictionary of tiles"""
        
    tiles = {}
    for i in range(19):#there are 19 total tiles.
        tiles[("S"+str(i+1))] = {}
                
    return tiles


def place_desert(tiles : dict) -> tuple[dict, str]:
    """The desert and robber are placed on the same random tile"""
        
    print("Spawning your desert...")
    desert = random.randint(1, 19)#the parameters for possible tiles (there are 19)
    tiles[("S"+str(desert))]["biome"] = "desert"
    tiles[("S"+str(desert))]["number"] = "NA"
    robber = "S"+str(desert)

    return tiles, robber


def make_token_list() -> list:
    """These are the possible tokens that can be assigned onto hexes."""
        
    number_tokens = []
    for i in range(3,12): #the range is between 2 and 11 inclusive as 1 and 12 only appear once.
        for x in range(2): #need to repeat this twice as these tokens appear twice.
            number_tokens.append(i)
    
    for i in range(2):
        number_tokens.remove(7)
        number_tokens.append(2)
    number_tokens.append(12)
        
    return number_tokens


def create_roads() -> dict:
	"""Creates a dictionary for roads and adds roads into it"""
	
	print("Paving your roads...")
	counter = 0
	quick_dict = dict(zip(["__", "/", "\\"], ["ABCDEF$GHIJKMNOPRSTUVWYZabdefghiklmnpqrstuvwxyz+", 
					"ADCG$LRXMSHNEIJPQWVbcihnoutyx+rwmsflagOUTZYedjkq",
					"BEFJDHIOGMLRSYNTXdekjpqvwzsxntiobhWcKQPVUaZfgmlr"]))
	roads = {}
	for road_type in ["__", "/", "\\"]:
		for i in range(len(quick_dict[road_type])//2):
			road = ""
			for x in range(2): 
				road += quick_dict[road_type][counter]
				counter += 1

			road = quick_reorder(road)
			roads[road] = {'display' : road_type, 'owner' : 0}
		counter = 0#resets the counter
			
	return roads


def make_grid(biomes : list, number_tokens : list, associated_settlements : dict) -> tuple[dict, str, dict, dict]:
        """Creates variables used in the grid"""
        
        settlement_locations = "abcdefghijklmnopqrstuvwxyz".upper()
        settlement_locations += settlement_locations.lower() + "+" + "$"
        #duplicates it in lowercase as the settlements are denoted alphabetically
        
        tiles = create_tiles()
        tiles, robber = place_desert(tiles)
        number_tokens = make_token_list()
        
        tiles = assign_tile_variables(tiles, biomes, number_tokens, associated_settlements)
        settlement_locs = assign_ports(settlement_locations)
        roads = create_roads()
        
        return tiles, robber, settlement_locs, roads


def assign_ports(settlement_locations : str) -> dict:
    """Assigns ports to relevant tiles"""
        
    ports = ["wood", "grain", "sheep", "ore", "brick"]
    settlement_locs = {}
    for loc in settlement_locations:
        settlement_locs[loc] = {"display": loc}#the display is the string that will be directly accessed for colouring later
        settlement_locs[loc]["port"] = ""
        settlement_locs[loc]["owner"] = 0
        
    for loc in "ABFJouxy":#these settlements can access the ports
        settlement_locs[loc]["port"] = "3:1 port"
        
    i = 0
    reps = 0
    for loc in "RQCGWcvwjp":
        reps += 1
        port_to_place = f"2:1 {ports[i]} port"
        settlement_locs[loc]["port"] = port_to_place
        if reps % 2 == 0:
            i += 1#it just makes sure that we iterate through the possible ports every 2 repetitions

    return settlement_locs


def assign_tile_variables(tiles : dict, biomes : list, number_tokens : list, associated_settlements):
    """Assigns variables to each tile"""
         
    for i in range(19):
        try:
            tiles[("S"+str(i+1))]["biome"]#the desert currently has no biome tag so simply calling it will return error
        except KeyError:
            #shuffle the biomes; pop is fast
            random.shuffle(biomes)
            chosen_biome = biomes.pop()
            #adds the chosen variables to the biome.
            tiles[("S"+str(i+1))]["biome"] = chosen_biome
            #shuffles the tokens too
            random.shuffle(number_tokens)
            chosen_number = number_tokens.pop()
            tiles[("S"+str(i+1))]["number"] = chosen_number
        
        tiles["S"+str(i+1)]["attached_settlements"] = associated_settlements["S"+str(i+1)]

    return tiles


def make_biomes() -> list:
        """Creates a list of biomes"""
        
        biomes = []
        for i in range(3):
                biomes.append("ores")
                biomes.append("brick")

        for i in range(4):
                biomes.append("grain")
                biomes.append("wood")
                biomes.append("sheep")
        
        return biomes
    
    
def place_robber(grid : Grid) -> str:
    """Forces a valid placement of the robber according to the player's choosing (activated upon rolling a 7)"""
    
    error_message = "That tile doesn't exist. Please input as either the arabic numerals following the S or with the S."
    
    while True:
        placement = input("Where would you like to place the robber?\n˚₊ · »-♡→ ")
        if placement in grid.tiles.keys():
            tile = placement
            proceed = True
        elif placement.isdigit():
            if int(placement) <= 19:
                    tile = "S" + str(placement)
                    proceed = True
            else:
                    print(error_message)
                    proceed = False
        else:
            print(error_message)
            proceed = False
                        
        if proceed:
            if grid.robber == tile:
                print("You can't choose not to move it!")
                    
            else:
                grid.robber = tile
                break
                                
    return grid.robber
    
    
##INITIALISING GAME ASSETS


def create_game_bank(player_info : PlayerInfo):
    """Calls the functions needed to set up the game bank"""
    
    game_bank = {}
    #adds the dictionaries for asset values into the game bank
    resources, dev_bank = initialise_resource_cards()
    game_bank['resources'] = resources
    game_bank['cards'] = dev_bank
    
    #creates a bank of building costs that the game can directly access
    
    return game_bank

 
def initialise_resource_cards() -> tuple[dict, list]:
    """Initialises the dictionary for each resource to be passed into the game bank"""
    
    #Initialises 19 of each resource
    resources = {}
    for resource in RESOURCES:
        resources[resource] = 19
        
    #creates the development card bank
    cards = []
    for card in CARDS:
        cards.extend([card] * CARDS[card])
    
    return resources, cards


##ROLL MECHANICS


def dice_roll(player_info : PlayerInfo, grid : Grid) -> tuple[PlayerInfo, Grid]:
    """Rolls the die"""
    
    dice_1 = random.randint(1, 6)
    dice_2 = random.randint(1, 6)
    roll = dice_1 + dice_2
    print(f"As everyone watches with bated breath, you roll the die. You pray for a good result. They land as follows: |{dice_1}| |{dice_2}| ... {dice_1} + {dice_2} = {roll}. You've rolled a {roll}.")
    
    if roll == 7:
        return rolled_a_seven(player_info, grid)
            
    for tile in grid.tiles:
        
        if grid.tiles[tile]['number'] == roll:
            
            print(f"Tile {tile} has number {roll}!")

            if grid.robber != tile:
                for player in player_info.quick_key:
                    for building in ['settlement', 'city']:
                    
                        for settlement in player_info.player_dicts[player]['constructs'][f'{building} list']:
                            if settlement in grid.tiles[tile][f'attached_{building + "s" if building == "settlement" else ""}']:
                                if settlement in player_info.player_dicts[player]['constructs']['settlement list']:
                                    player_info = give_resources(grid.tiles[tile]['biome'], player_info, player, settlement)
                                else:
                                    player_info = give_resources(grid.tiles[tile]['biome'], player_info, player, settlement, 2)
            else:
                print(f"The robber has prevented anyone from obtaining resources on {tile}")
    
    return player_info, grid
 
 
def roll_die(roll_allowed, player_info, grid) -> tuple[bool, PlayerInfo, Grid]:
    """Roll die if roll is allowed"""
    
    if roll_allowed:
        player_info, grid = dice_roll(player_info, grid)
        roll_allowed = False
    else:
        print("You've already rolled this turn. You can only roll once per turn.") 
            
    return roll_allowed, player_info, grid
 
 
def give_resources(resource : str, player_info : PlayerInfo, player, settlement='', num=1) -> PlayerInfo:
    """Transfers resources from bank to players based on rolls"""
    
    game_bank = player_info.game_bank
    if game_bank['resources'][resource] != 0:
        if settlement != "":
            print(f"P{player} has obtained {resource} from '{settlement}.'")
                
        game_bank['resources'][resource] -= 1
        player_info.player_dicts[player]['resources'][resource] += 1
    else:
        print(f"The bank has run out of {resource}! P{player} is unable to obtain {resource}{f' from {settlement}' if settlement != '' else ''}")
        
    player_info.game_bank = game_bank
    return player_info
    
    
def halve_decks(player_info : PlayerInfo) -> PlayerInfo:
    """Identifies players that must halve their hands and forces said halving"""
    #Players that have more than 7 cards after rolling a 7 must discard half their cards
    
    for player in player_info.quick_key:
        hand_size = calculate_hand_size(player_info, player)
        if hand_size > 7:
            print(f"Pass the laptop to player {player}. \nYou currently have {hand_size} cards. You must discard your hand until you have {required_size} cards left.")
            force_password(player_info, player)#ensure privacy
            required_size = hand_size//2
        else:
            required_size = hand_size
            print(f"Player {player} has a satisfactory hand size.")
            
        while hand_size > required_size:
            player_info = discard_resource(player_info, player)
            hand_size = calculate_hand_size(player_info, player)
            
    return player_info


def rolled_a_seven(player_info, grid) -> tuple[PlayerInfo, Grid]:
    """Moves the robber and halves the decks."""
    
    print(f"Player {player_info.player_turn}, you must place the robber.")
    grid.robber = place_robber(grid)
    print("Now everyone look away apart from the current player.")
    force_password(player_info)
    player_info = steal_card(player_info, grid)
    player_info = halve_decks(player_info)
    print("Type 'cls' and then tell everyone to look back at the screen.")
    
    return player_info, grid


##BUILDING-RELATED


def build(player_info : PlayerInfo, grid: Grid) -> tuple[PlayerInfo, Grid]:
    """Asks the player what they would like to build, then builds it"""
    
    while True:
        action = input("What would you like to build? Hint: type 'check' to see the input format.\n˚₊ · »-♡→ ").strip().lower()
        
        if action in ['x', 'cancel']:
            break
        elif action == 'check':
            print("""Enter:
> 'x' or 'cancel' to escape the building site
> 'road', '1', or 'r' to build a road
> 'settlement', '2', or 's' to build a settlement
> 'city', '3', or 'c' to upgrade to a settlement
Happy building!""")
        elif action in ['road', '1', 'r']:
            if proceed('road', player_info):
                player_info, grid, trade = place_road(player_info, grid)
                if trade:
                    transfer_resources(player_info, CONSTRUCT_COSTS['road'])
                    player_info.player_dicts[player_info.player_turn]['constructs']['road'] -=1
                
        elif action in ['settlement', '2', 's']:
            if proceed('settlement', player_info):
                player_info, grid, trade = place_settlement(player_info, grid)
                if trade:
                    transfer_resources(player_info, CONSTRUCT_COSTS['settlement'])
                    player_info.player_dicts[player_info.player_turn]['constructs']['settlement'] -=1
                    
        elif action in ['city', '3', 'c']:
            if proceed('city', player_info):
                player_info, grid, trade = upgrade_to_city(player_info, grid)
                if trade:
                    transfer_resources(player_info, CONSTRUCT_COSTS['city'])
                    player_info.player_dicts[player_info.player_turn]['constructs']['city'] -=1
        else:
            print("Looks like that's not a valid command. If you're confused, try using 'check' to see what you're allowed to enter here :)")
            
    clear_screen()
    print_board(player_info, grid)
                    
    return player_info, grid

    
def place_road(player_info : PlayerInfo, grid : Grid) -> tuple[PlayerInfo, Grid, bool]:
    """Places down a road and changes player information accordingly, as well as the grid. Does not take resources from the player in the process."""
    
    player = player_info.player_turn
    if player_info.player_dicts[player]['constructs']['road'] < 1:
        print("You've used up all your possible roads. Sorry.")
        return player_info, grid, False
    
    valid = False
    while not valid:
        text = input(ansi_stitching(player_info.player_dicts[player]['colour'], f"Player {player}, where are you placing your road?") + "\n˚₊ · »-♡→ ").strip()
        valid = check_road(text, grid, player_info)
        if text == 'cls':#allows player to clear their screen
            clear_screen()
            print_board(player_info, grid)
            
    player_info.player_dicts[player]['constructs']['road list'].append(text)
    grid.roads[quick_reorder(text)]['display'] = ansi_stitching(player_info.player_dicts[player]['colour'], grid.roads[quick_reorder(text)]['display'])
    grid.roads[quick_reorder(text)]['owner'] = player
    #clear_screen()
    print_board(player_info, grid)
    
    player_info.player_dicts[player_info.player_turn]['constructs']['road'] -= 1
    return player_info, grid, True


def place_settlement(player_info : PlayerInfo, grid) -> tuple[PlayerInfo, Grid, bool]:
    """Places down a settlement. Does not deduct any resources from the player, do this separately"""

    player = player_info.player_turn
    if player_info.player_dicts[player]['constructs']['settlement'] < 1:
        print("You have no more settlements! Sorry.")
        return player_info, grid, False#ends the subroutine early
    
    valid = False
    while not valid:
        text = input(ansi_stitching(player_info.player_dicts[player]['colour'], f"Player {player}, where would you like to place your settlement?") + "\n˚₊ · »-♡→ ").strip()
        valid = check_settlement(text, grid, player_info, 1)
        if text == 'cls':
            clear_screen()
            print_board(player_info, grid)
            
    player_info.player_dicts[player]['constructs']['settlement list'].append(text)#adds the new settlement to the player's list of settlements
    grid.settlement_locs[text]['display'] = ansi_stitching(player_info.player_dicts[player]['colour'], grid.settlement_locs[text]['display'])
    grid.settlement_locs[text]['owner'] = player
    clear_screen()
    print_board(player_info, grid)
    
    player_info.player_dicts[player]['constructs']['settlement'] -= 1
    return player_info, grid, True
    

def change_construct_number(player_info : PlayerInfo, construct, add=0) -> PlayerInfo:
    """Adds or subtracts the construct from the player's bank when they place something down"""
    
    player = player_info.player_turn
    if add:
        player_info.player_dicts[player]['constructs'][construct] +=1
    else:
        player_info.player_dicts[player]['constructs'][construct] -= 1
        
    return player_info


def steal_card(player_info, grid) -> PlayerInfo:
    """Sets up the steal 1 card mechanic"""
    
    steal_list, steal_names = find_steal_victims(player_info, grid)
    
    if steal_list == []:
        print("'You didn't place the robber next to anybody else's settlement, so you can't steal anything.")
        return player_info
    victim = identify_victim(steal_list, steal_names, player_info)
    resource_to_steal = steal_one(player_info, victim)
    if resource_to_steal == '':
        return player_info
    player_info = trade_resources(player_info, {resource_to_steal : 1}, player_info.player_turn, victim)
    print(f"You have stolen one of player {victim}'s {resource_to_steal}. Returning to the mainframe now...")
    
    return player_info
            
            
def find_steal_victims(player_info, grid) -> tuple[list, list]:
    steal_list = []
    for settlement in grid.tiles[grid.robber]['attached_settlements']:
        if grid.settlement_locs[settlement]['owner'] != 0 and grid.settlement_locs[settlement]['owner'] != player_info.player_turn:
            steal_list.append(grid.settlement_locs[settlement]['owner'])
    steal_set = set(sorted(steal_list))
    steal_list = list(steal_set)
    steal_names = []
    for player in steal_list:
        steal_names.append(player_info.player_dicts[player]['name'])
    return steal_list, steal_names


def identify_victim(steal_list, steal_names, player_info) -> int:
    """Forces a loop to identify a player to steal from"""
    
    while True:
        print("These are the players that you can steal from:")
        for player in steal_list:
            print(f"Player {player} (aka '{player_info.player_dicts[player]['name']}')")
        action = input("Please select a player to steal from.\n˚₊ · »-♡→ ").strip().lower()
        if action.isdigit():
            if int(action) in steal_list:
                return int(action)
            else:
                print("Invalid player")
        elif action in steal_names:
            return steal_list[steal_names.index(action)] 
        else:
            print("Not eligible. Try again.")


def upgrade_to_city(player_info, grid):
    settlements = player_info.player_dicts[player_info.player_turn]['constructs']['settlement list']
    if settlements == []:
        print("You don't have any settlements to upgrade.")
        return player_info, grid, False
    if player_info.player_dicts[player_info.player_turn]['constructs']['city'] < 1:
        return player_info, grid, False
    
    while True:
        action = input("Select a settlement. It's case sensitive, by the way!\n˚₊ · »-♡→ ")
        for settlement in settlements:
            print(f"The settlement{'s' if len(settlements) > 1 else ''} you have available to you are: ")
            print(settlement, end=(", " if settlement != settlements[-1] else "."))
        if action in ['esc', 'cancel']:
            print("Okay, escaping the city upgrade site...")
            return player_info, grid, False
        elif action in settlements:
            player_info.player_dicts[player_info.player_turn]['constructs']['city list'].append(action)
            player_info.player_dicts[player_info.player_turn]['constructs']['city'] -= 1
            settlements.remove(action)
            print("Congrats on upgrading to a settlement!")
            return player_info, grid, True
        else:
            print("That's not a valid settlement. If you want to leave, please type 'esc' or 'cancel'! (x will place something at x so...)")
                
 
##PROCESSING


def check_password(player_info, player=0) -> bool:
    """Checks the player's password"""
    
    victim = player_info.player_turn if not player else player
    attempt = input("Enter your password. (Turn your screen away from the other players).\n˚₊ · »-♡→ ")
    if attempt == player_info.player_dicts[victim]['password']:
        return True
    else:
        print("Wrong password.")
        return False


def force_password(player_info : PlayerInfo, player=0):
    """Forces the player to input their password. The game breaks if they forget it. So it's very important for them to remember their password."""
    
    victim = player_info.player_turn if not player else player
    
    correct_password = False
    while not correct_password:
        correct_password = check_password(player_info, victim)
        if not correct_password:
            print("This is bad. You're stuck in an infinite loop now :P")
        

def quick_reorder(road : str):
    """Reorders a 2-letter string based on ascii values (alphabetical order I suppose). 
        This allows me to standardise the way in which roads are called from the dictionary."""

    if road[0] > road[1]:
        road = road[1] + road[0]

    return road


def check_settlement(text : str, grid : Grid, player_info : PlayerInfo, initial : int=0):
    if not text in grid.settlement_locs:
        print("That settlement doesn't exist.")
        return False
    owner = grid.settlement_locs[text]['owner']
    if owner != 0:#Checks if it's already owned. If so, then the players should not be allowed to obtain it.
        if owner == player_info.player_turn:
            print("You already own it!")
        else:
            print(f"This road is already owned by player {owner}. Pro tip: if it's coloured, it's not up for grabs.")
        return False#Both statements will obtain false.
    related_roads = []
    for road in grid.roads:
        if text in road:
            related_roads.append(road)
    for road in related_roads:
        adjacent_settlement = road.replace(text, '')
        if grid.settlement_locs[adjacent_settlement]['owner']:
            print(f"The adjacent settlement, '{adjacent_settlement}', is already owned. You can't build directly next to it.")
            return False
    for road in related_roads:
        if grid.roads[road]['owner'] == player_info.player_turn:
            print("Congratulations on building a new settlement!")
            return True
    if initial:
        print("Congratulations on obtaining your free settlement!!")
        return True
    else:
        print("You don't own a connected road - you must have a claim to the settlement. Sorry.")
        return False


def check_road(text : str, grid : Grid, player_info : PlayerInfo) -> bool:
    try:
        text = quick_reorder(text)
    except IndexError:
        print("Roads are two letters long. Please enter the settlements that you are stringing together!")
        return False
    
    if text not in grid.roads:
        print("That road doesn't exist.")
        return False
    
    owner = grid.roads[text]['owner']
    if owner != 0:#checks if a player that's not the current one owns it
        if owner != player_info.player_turn:
            print(f"That road already belongs to player {owner}. Better luck next time.")
        else:
            print("You already own that road.")
        return False
    
    settlement_rights = []
    for road in player_info.player_dicts[player_info.player_turn]['constructs']['road list']:
        for settlement in road:
            settlement_rights.append(settlement)
    for settlement in player_info.player_dicts[player_info.player_turn]['constructs']['settlement list']:
        settlement_rights.append(settlement)
    print(settlement_rights)
    
    for claim in set(settlement_rights):
        print(claim)
        if claim in text:
            print("Congratulations on paving your new road!")
            return True
    
    print("You don't own any settlements/roads next to that road, so you don't have ownership rights. Sorry.")
    return False


def create_classes() -> tuple[Grid, PlayerInfo]:
    """Sets up class variables for later use"""
    
    number_tokens = make_token_list()
    biomes = make_biomes()
    quick_key, player_dicts = create_player_info()
    player_info = PlayerInfo({}, quick_key, player_dicts)
    game_bank = create_game_bank(player_info)
    player_info.game_bank = game_bank
    tiles, robber, settlement_locs, roads = make_grid(biomes, number_tokens, ASSOCIATED_SETTLEMENTS)
    
    grid = Grid(robber, tiles, settlement_locs, roads, biomes)
    
    clear_screen()
    
    return grid, player_info


def allow_turn_end(roll_allowed : bool, player_info : PlayerInfo) -> bool:
    """Checks if the turn can end and returns the turn"""
    
    if not roll_allowed:
        if check_password(player_info):
            print("Your turn has ended.")
            turn = False
        else:
            turn = True
    else:
        print("You must roll before you can end your turn.")
        turn = True
            
    return turn
  
    
def proceed(construct : str, player_info : PlayerInfo) -> bool:
    """Checks if the player has enough of the resource, then asks the player if they'd like to continue the trade"""
    
    materials_needed = CONSTRUCT_COSTS[construct]
    
    force_password(player_info)
    for resource in materials_needed:
        owned = player_info.player_dicts[player_info.player_turn]['resources'][resource]
        if owned < materials_needed[resource]:
            print(f"You don't have enough {resource}. Trade unsuccessful. You need {materials_needed[resource]} but only have {owned}.")
            return False
        else:
            print(f"You have enough {resource} for the trade. (You have {owned}, {materials_needed[resource]} are required)")
        time.sleep(0.1)
        if construct != 'dev card':
            if player_info.player_dicts[player_info.player_turn]['constructs'][construct] < 1:
                print("You don't have enough constructs to build anything!")
                return False
            
    while True:
        action = input("You have enough of every resource. Would you like to proceed with the trade?\n˚₊ · »-♡→ ").strip().lower()
        if action in ['no', 'x', 'cancel']:
            print("OK, the trade is canceled.")
            return False
        elif action in ['yes', 'y', 'continue', 'proceed']:
            print("OK, we will proceed to the checking stage to make sure you are eligible.")
            return True
        elif action == 'check':
            print("""The possible commands you can use here are:
> 'yes' to confirm the trade 
> 'no' to end the trade
> 'cls' to clear the screen
> 'check' to check commands.
Have fun trading~""")
        elif action == 'cls':
            clear_screen()
        else:
            print("Unsure of the commands? Use 'check' to see what you can input here.")


def calculate_hand_size(player_info : PlayerInfo, player : int) -> int:
    """Calculates the hand size of a specified player"""
    
    hand_size = 0
    for resource in player_info.player_dicts[player]['resources']:
        hand_size += player_info.player_dicts[player]['resources'][resource]
        
    return hand_size


def evaluate_game(player_info : PlayerInfo) -> bool:
    """Calculates victory points and determines if the game is still ongoing or if someone has won"""
    
    if calculate_points(player_info, player_info.player_turn) >= 10:
        winner = player_info.player_turn
        print(ansi_stitching(player_info.player_dicts[winner]['colour'], f"The game has ended!! Player {winner} IS VICTORIOUS!!"))
        return False
    
    else:
        return True


def calculate_points(player_info, player, public=0) -> int:
    """Calculates the given player's victory points"""
    
    victory_points = 0
    victory_points += len(player_info.player_dicts[player]['constructs']['settlement list'])
    victory_points += len(player_info.player_dicts[player]['constructs']['city list']) * 2#every city is worth 2VPs
    if not public:
        victory_points += player_info.player_dicts[player]['cards']['VP card']
    if player_info.longest_road[0] == player:
        victory_points += 2
    if player_info.largest_army[0] == player:
        victory_points += 2
        
    return victory_points


##PROGRAM STAGES


def get_initial_inputs():
    print("""WELCOME TO MY TEXT-BASED CATAN.
Before we start, make sure \x1b[38;2;142;194;21mthis text\x1b[0m is green!
CREDITS: Vivienne, CATAN game studio. To start the game, type 'start', or type 'rng' to gamble!
To see the available commands, type 'cmds'.
ENTER YOUR COMMAND TO BEGIN""")#the welcome message
    
    while True:
        action = input("What would you like to do? :)\n˚₊ · »-♡→ ").lower()  
        if action == 'start':
            print("Starting your game now!")
            #aesthetics for a loading/clearing screen
            time.sleep(1)
            clear_screen()
            break
        elif action == 'rng':
            print("Sorry, that's been removed from the program now.")#currently under work. i might add it back but there were some fishy calculations
        elif action == 'cls':
            clear_screen()
        elif action == 'cmds':
            print("""The available commands are:
> 'cls' clears your screen
> 'start' starts your game
> 'rng' begins rng
'cmds' allows you to view current commands.""")
        else:
            print("That's not currently a valid command.")
      

def initial_loop(player_info : PlayerInfo, grid : Grid) -> tuple[PlayerInfo, Grid]:
    """Carries out the initial loop for the players to place down their settlements and roads FOR FREE."""
    
    game_bank = player_info.game_bank

    print_board(player_info, grid)
    print(f"We'll go from player 1 to player {len(player_info.quick_key)}; you can place two settlements and two roads for free. Please choose wisely.")

    
    for player in player_info.quick_key:
        player_info.player_turn = player
        player_info, grid, trade = place_settlement(player_info, grid)
        player_info, grid, trade = place_road(player_info, grid)
    for player in reversed(player_info.quick_key):
        player_info.player_turn = player
        player_info, grid, trade = place_settlement(player_info, grid)
        player_info, grid, trade = place_road(player_info, grid)
                    
    player_info.player_turn = 1
    player_info.game_bank = game_bank
                    
    return player_info, grid


def main_game(player_info, grid):
    """The very time consuming main stage of the game"""

    game = True
    player_info.game_stage = 2
    
    while game:
        for player in player_info.quick_key:
            
            turn = True
            player_info.player_turn = player
            roll_allowed = True
            
            while turn and game:
                action = input(ansi_stitching(player_info.player_dicts[player]['colour'], f"Player {player}, what's your move?") + "\n˚₊ · »-♡→ ").strip().lower()
                if action in ['et', 'end turn']:
                    turn = allow_turn_end(roll_allowed, player_info)
                    
                elif action in ['b', 'build']:
                    player_info, grid = build(player_info, grid)
                    game = evaluate_game(player_info)
                    
                elif action in ['t', 'trade']:
                    player_info = choose_trade(player_info, grid)
                
                elif action in ['r', 'roll']:
                    roll_allowed, player_info, grid = roll_die(roll_allowed, player_info, grid)
                    
                elif action in ['cls', 'clear screen']:
                    clear_screen()
                    print_board(player_info, grid)
                    
                elif action in ['c', 'cmds']:
                    print(COMMANDS)
                    
                elif action in ['d', 'draw']:
                    if proceed('dev card', player_info):
                        player_info, bought = draw_development_card(player_info)
                        if bought:
                            transfer_resources(player_info, CONSTRUCT_COSTS['dev card'])
                    print("Type 'cls', then turn the screen back so everyone can see.")
                    game = evaluate_game(player_info)
                
                elif action in ['i', 'info']:
                    print(INFO_MESSAGE)
                
                elif action in ['pod', 'print deck', 'deck']:
                    print_deck(player_info)
                    
                elif action in ['play', 'p']:
                    card = choose_development_card(player_info)
                    if card != "":
                        player_info, grid = execute_development_card(card, grid, player_info)
                    
                elif action == 'costs':
                    print(COSTS)
                    
                else:
                    print(ERROR_MESSAGE)
                    
            clear_screen()
            print_board(player_info, grid)          
        
    
def main():
    """Main code for the game, initially called"""
    while True:
        print("If you're playing the game, remove the line with sys.exit (use command F or smth idk)")
        sys.exit()########remove this line if playing
        get_initial_inputs()#the initial input loop ends as soon as the game starts
        grid, player_info = create_classes()#assigns variables to the classes and makes them direct objects to call
        player_info.player_dicts = add_colours(player_info)#gives each player colours
        player_info.player_dicts = add_keys(player_info)#adds further keys to player dictionaries
        player_info, grid = initial_loop(player_info, grid)#go through the initial loop for the game
        main_game(player_info, grid)
    
    
##DO NOT TOUCH
    
if __name__ == "__main__":
    main()