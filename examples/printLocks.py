#              Block Layout:                     
#                                                         
#   __________    __________    __________ 
#  |          |--|          |--|          |
#  |  Block1  |  |  Block2  |  |  Block3  |
#  |          |  |__________|  |__________|
#  |          |   |             |          
#  |          |   __________    __________ 
#  |          |  |          |  |          |
#  |          |  |  Block4  |XX|  Block5  |
#  |__________|  |__________|  |__________|
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
Block1Body = [body * 10, bodyColor, bodyIndent]
Block1 = Block(blocksize, defaultPadding, Block1Headline, Block1Body)

Block2Headline = [headline, headlineColor, headlineNewline]
Block2Body = [body * 3, bodyColor, bodyIndent]
Block2 = Block(blocksize, defaultPadding, Block2Headline, Block2Body)

Block3Headline = [headline, headlineColor, headlineNewline]
Block3Body = [body * 5, bodyColor, bodyIndent]
Block3 = Block(blocksize, defaultPadding, Block3Headline, Block3Body)

Block4 = Block2.clone()
Block4.addPrintMaster(lock)
Block5 = Block4.clone(withLocks=True)

Block1.right = Block2
Block2.right = Block3
Block2.bottom = Block4
Block3.bottom = Block5

print()
Block1.buildBlockChain()
Block1.printBlockChain()
