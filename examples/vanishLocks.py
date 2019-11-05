#                       Block Layout:                     
#                                                         
#   __________    __________    __________     __________ 
#  |          |--|          |--|          |- -|          |
#  |  Block1  |  |  Block2  |  |  Block3  |   |  Block4  |
#  |          |  |__________|  |__________|   |          |
#  |          |   |                           |          |
#  |          |   _________________________   |          |
#  |          |  |                         |  |          |
#  |          |  |         Block5          |  |          |
#  |          |  |_________________________|  |          |
#  |          |   |                           |          |
#  |          |   __________    __________    |          |
#  |          |  |          |--|          |   |          |
#  |          |  |  Block6  |  |  Block7  |   |          |
#  |__________|  |__________|  |__________|   |__________|
#                                                        
from ttf import Block, Lock

blocksize = 40
defaultPadding = [0, 5, 1, 0]

headline = "Example Block: "
headlineColor = "yellow#bold"
headlineNewline = False

body = "oooooooooooooooooooooooooo"
bodyColor = "blue#bold"
bodyIndent = "auto"

lock = Lock()


Block1Headline = [headline, headlineColor, headlineNewline]
Block1Body = [body * 15, bodyColor, bodyIndent]
Block1 = Block(blocksize, defaultPadding, Block1Headline, Block1Body)

Block2Headline = [headline, headlineColor, headlineNewline]
Block2Body = [body * 4, bodyColor, bodyIndent]
Block2 = Block(blocksize, defaultPadding, Block2Headline, Block2Body)

Block3 = Block2.clone()
Block3.addVanishMaster(lock)

Block4 = Block1.clone()

Block5Headline = [headline, headlineColor, headlineNewline]
Block5Body = [body * 15, bodyColor, bodyIndent]
Block5 = Block(blocksize * 2, defaultPadding, Block5Headline, Block5Body, printMaster=lock)

Block6 = Block2.clone()
Block7 = Block2.clone()

Block1.right = Block2
Block2.right = Block3
Block3.right = Block4

Block2.bottom = Block5
Block5.bottom = Block6
Block6.right = Block7

print()
Block1.buildBlockChain()
Block1.printBlockChain()
