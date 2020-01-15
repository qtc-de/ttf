import re
import sys
import textwrap
import itertools
from pyparsing import *
from io import StringIO
from termcolor import colored
from .Lock import Lock

def coloredWrapper(string, color):
    """The termcolor.colored function has the downside that color codes and attributes have to
       be specified seperatly. Thefore, we would require additional parameters to allow body or
       blink text. Instead we use this helper function, which lets you specify attributes by using
       a # as a seperator behind the color name. Furthermore, we add support for the color code 'none'.

    Parameters:
        string                  (string)                    The string that should be highlighted
        color                   (string)                    The color that should be used. E.g. 'blue#bold'

    Returns:
        array(str)              List of padded strings. Probably with incresed length.
    """
    #the color strings supported by ttf contain attributes seperated by #. First step is to split these
    #and inspect of the string needs colorization at all
    colorComponents = color.split("#")
    if colorComponents[0] == "none":
        return string

    #termcolor does not support nested colors. Therefore we simply colorize a dummy string and split
    #at the dummy signature to get the color code of the desired color. All reset markes (\x1b[...)
    #are then replaced by that color code
    splitDummy = "dkjashdqi8vip1238zhr"
    colorPrefix = colored(splitDummy, colorComponents[0], attrs=colorComponents[1:]).split(splitDummy)[0]
    coloredString = string.replace('\x1b[0m', '\x1b[0m{}'.format(colorPrefix))

    #finally we can just colorize the string and return it back to the user
    coloredString = colored(coloredString, colorComponents[0], attrs=colorComponents[1:])
    return coloredString



class Block: 
    """Blocks are structured output components. It has a fixed size, padding, headline and body and can contain
       neighbourship relation ships. If a Block is printed, it will wrap the text inside to the approtiate size
       and print neigthbours accordingly like they were defined. A typical output structure would look like this:

                              ------------     ----------      ----------
                             |   Block0   |---|  Block1  |    |  Block2  |
                             |            |   |          |----|          |
                             |            |   |  ######  |    |  ######  |
                             |            |   | ----------    |  ######  |
                             |            |         |          ----------
                             |            |    ----------          |
                             |            |   |  Block3  |     ----------
                             |            |   |          |    |  Block4  |
                             |            |   |  ######  |    |          |
                             |            |    ----------     |  ######  |
                             |____________|                    ----------

        Notice that the Block class was only tested on well defined block compositions. If you are going crazy
        with relationships between blocks, the layout could brake.

    Parameters:
        None

    Returns:
        None
    """


    def __init__(self, size=90, padding=[0,0,0,0], head=["", "", ""], body=["", "", 0], right=None, bottom=None, unlocked=False, printMaster=None, vanishMaster=None):
        """Creates a new Block object. 

        Parameters:
            size             (int)                       The horizontal size that the block takes on the screen
            padding          (array[int,int,int,int])    The padding for text contained in block [upper, right, lower, left]
            head             (array[str,str,bool])       An optional heading for the block [content, color, separator]
            body             (array[str,str,int])        The body of the block [content, color, indent]
            right            (Block)                     The right neighbour of the block
            bottom           (Block)                     The bottom neigbor of this block
            unlocked         (Boolean)                   Determines if the corresponding Block is unlocked
            printMaster      (Lock)                      Assigns the current Block a printMaster to keep it aligned in a row

        Returns:
            Block:  An object that can be placed beside other blocks that are formatted nicly when printed
        """
        self.size = size
        self.padding = padding

        #we could put the optional newline at the end of the block into head[0]
        #instead of using head[2]. However, this would need quite some changes
        self.headContent = head[0]
        self.headColor = head[1]
        self.headNewline = head[2]

        self.bodyContent = body[0]
        self.bodyColor = body[1]
        self.bodyIndent = body[2]

        self.keywords = {}

        self.right = right
        self.bottom = bottom
        
        self.lock = Lock(unlocked, printMaster)

        self.vanishLock = None
        if vanishMaster:
            self.vanishLock = Lock(False, vanishMaster)

        self.content = None
        self.generator = None


    def __str__(self):
        """Helper function to print a plain block. This should only be used for debugging and testing because it does
           not care about neighbors and other blocks. 

        Parameters:
            None

        Returns:
            None
        """
        return "\n".join(self.content)



    def addKeyword(self, keyword, color):
        """This function can be used to add keywords after creation of a Block object. Keywords are seperatly highlighted
           inside Blocks.

        Parameters:
            keyword                     (string)            Keyword to highlight. Should be a valid regular expression
            color                       (string)            Color which is used to highlight the keyword

        Returns:
            None
        """
        try:
            keyword = "({})".format(keyword)
            regex = re.compile(keyword)
            self.keywords[regex] = color
        except:
            pass


    def highlightKeywords(self, string):
        """Iterates over the dictionary of self.keywords and applies the corresponding colorization to them. 

        Parameters:
            string                      (string)            String in which the keywords should be highlighted

        Returns:
            None
        """
        for keyword, color in self.keywords.items():
            #here we apply a dirty hack. Since the algorithm that colors the whole block will search for the signature
            #\x1b[0m and append the ANSI block color code behind it. This needs to be done, since nested colors would
            #otherwise leave the contents behind them uncolored. However, it leads to a problem with bold text, since
            #the termcolor library does not tell a non bold ANSI color to be explictly not bold. Instead, it will just use
            #the default settings for boldness, which was may modified by another ANSI color before. Thefore, we need to
            #reset every ANSI change in front of a nested color, but this would get replaced by the body highlighter. 
            #To avoid this, we use the signature '\x1b[00m', which has the same effect as '\x1b[0m', but is not replaced
            #by the body highlighter.
            string = keyword.sub('\x1b[00m{}'.format(coloredWrapper(r'\1', color)), string)
        return string
            

    def clone(self, withNeighbors=False, withLocks=False):
        """Returns a copy of self. Notice that only basic attributes are copied. Neighbors and Locks have to be added
           manually

        Parameters:
            None

        Returns:
            copiedBlock                 (Block)             A copy of the Block represented by self
        """
        copiedPadding = self.padding
        copiedHeadline = [self.headContent, self.headColor, self.headNewline]
        copiedBody = [self.bodyContent, self.bodyColor, self.bodyIndent]
        copiedBlock = Block(self.size, copiedPadding, copiedHeadline, copiedBody)
        if withNeighbors:
            copiedBlock.right = self.right
            copiedBlock.bottom = self.bottom
        if withLocks:
            copiedBlock.lock = self.lock.clone()
            if self.vanishLock:
                copiedBlock.vanishLock = self.vanishLock.clone()
        return copiedBlock


    def addPrintMaster(self, printMaster):
        """Add a printMaster Lock after the Block was already created

        Parameters:
            printMaster                 (Lock)              Lock object that will be used for the printMaster property of self

        Returns:
            None       
        """
        self.lock.master = printMaster
        self.lock.makeSlave(printMaster)


    def addVanishMaster(self, vanishMaster):
        """Add a vanishMaster Lock after the Block was already created

        Parameters:
            vanishMaster                (Lock)              Lock object that will be used for the vanishMaster property of self

        Returns:
            None       
        """
        if self.vanishLock:
            self.vanishLock.master = vanishMaster
            self.vanishLock.makeSlave(vanishMaster)
        else:
            self.vanishLock = Lock(False, vanishMaster)


    def createEmptyBlock(size):
        """Emtpy Blocks are often required for padding purposes. This function just creaes an empty block.

        Parameters:
            None

        Returns:
            emptyBlock              (Block)             A block with no contents
        """
        emptyPadding = [0,0,0,0]
        emptyHead = ["", "none", False]
        emptyBody = ["", "none", 0]
        emptyBlock = Block(size, padding=emptyPadding, head=emptyHead, body=emptyBody)
        return emptyBlock
        

    def buildContent(self):
        """Creates an array of formatted lines that are stored inside of self.content

        Parameters:
            None

        Returns:
            None
        """
        #if indent is set to auto, the body will indent with size of the headline
        #since the headline can be longer than the block size, we need to take the modulus
        if self.bodyIndent == "auto": 
            self.bodyIndent = len(self.headContent) % self.size
        if self.bodyColor == "":
            self.bodyColor = "none"
        if self.headColor == "":
            self.headColor = "none"

        #if we put the raw input into textwrap, the output becomes wired if there are newlines 
        #present, since textwrapper counts them to the string length instead of a break.
        #therefore we split the input into lines first and invoke textwrap over all of them.
        headLines = self.headContent.splitlines()
        bodyLines = self.bodyContent.splitlines()

        #Step 1: We wrap each line inside the headline of the block. This is probably always the
        #case, but who knows :)
        textWrapper1 = self.createTextWrapper(initial=False)
        wrappedHead = list(map(lambda x: textWrapper1.wrap(x), headLines))
        headLines =  itertools.chain(*wrappedHead)
        if headLines != []:
            #applying color at this point is kind of dumb, since textwrap will count color codes
            #to the string length. However, it seems to me the best way of color implementation, 
            #because it leads to a clean cut between headline and body of the block
            headLines = list(map(lambda x: coloredWrapper(x, self.headColor), headLines))

            #if the headline is seperated from the body by a newline, we only have to join the
            #headline output and the body output. If there is no newline between headline and
            #body we need to more work to get a nice formatted output
            if not self.headNewline and bodyLines != []:
                #we have to determine if there are spaces for body indentation left and append them
                try:
                    indentLeft = self.bodyIndent - Block.realLength(headLines[-1])
                    headLines[-1] += ' ' * indentLeft
                except IndexError:
                    #cases where the hadnline was empty has to be handeled seperatly
                    indentLeft = self.bodyIndent
                    headLines.append(' ' * indentLeft)
                #we have to determine how many characters the body text beside the headline can take.
                #then we create a textwrap object for that size
                charactersLeft = self.size - Block.realLength(headLines[-1]) - self.padding[1] - self.padding[3]
                tmpTextWrapper = textwrap.TextWrapper();
                tmpTextWrapper.replace_whitespace = False
                tmpTextWrapper.width = charactersLeft
                wrappedBody = tmpTextWrapper.wrap(bodyLines[0])
                #we append the colored and wrapped first body line to the headline and remove it from
                #the rest of the body
                keywordsColored = self.highlightKeywords(wrappedBody[0])
                headLines[-1] = headLines[-1] + coloredWrapper(keywordsColored, self.bodyColor)
                if len(wrappedBody) > 1:
                    bodyLines[0] = " ".join(wrappedBody[1:])
                else:
                    bodyLines.pop(0)


        #wrapping and coloring the body is straight forward
        textWrapper2 = self.createTextWrapper(initial=True)
        wrappedBody = list(map(lambda x: textWrapper2.wrap(x), bodyLines))
        bodyLines = itertools.chain(*wrappedBody)
        bodyLines = list(map(lambda x: self.highlightKeywords(x), bodyLines))
        bodyLines = list(map(lambda x: coloredWrapper(x, self.bodyColor), bodyLines))

        content = headLines + bodyLines
        #if head and body were empty, the print function will break. Therefore we insert an empty string in that case
        if content == []:
            content = [""]
        return self.applyPadding(content)


    def buildBlockChain(self):
        """The content of block objects is not initialized until the buildContent() function is called. This function
           is a helper function which iterates over each Block object in the chain and calls builtContent() on them

        Parameters:
            None

        Returns:
            None
        """
        self.content = self.buildContent()
        self.generator = self.buildGenerator()
        if self.right: 
            self.right.buildBlockChain()
        if self.bottom:
            self.bottom.buildBlockChain()


    def realLength(string):
        """Returns the length of the string after stripping ANSI color codes. This is required for correct wrapping of 
           text, since textwrap will count ANSI color codes to the string length per default.

        Parameters:
            string                  (string)            The string of which the length is computed

        Returns:
            length                  (int)               Length of the uncolored string.
        """
        ESC = Literal('\x1b')
        integer = Word(nums)
        escapeSeq = Combine(ESC + '[' + Optional(delimitedList(integer,';')) + oneOf(list(alphas)))
        nonAnsiString = lambda s : Suppress(escapeSeq).transformString(s)
        uncoloredString = Suppress(escapeSeq).transformString(string)
        return len(uncoloredString)


    def applyPadding(self, lines):
        """Takes a list of strings and applies padding to them.

        Parameters:
            lines                   (array[str,...])            Strings that need to be padded

        Returns:
            array(str)              List of padded strings. Probably with incresed length.
        """
        #apply upper padding by simply insertig the lines to the top
        for ctr in range(0, self.padding[0]):
            lines.insert(0, "")
        #apply lower padding by simply appending the lines to the bottom
        for ctr in range(0, self.padding[2]):
            lines.append("")
        #insert padding infront of each lines
        lines = list(map(lambda x: " " * self.padding[3] + x, lines))
        #padding of the left site was alrady done by adjusting the wrapper size, but we may have to fill up!
        lines = list(map(lambda x: x + " " * (self.size - Block.realLength(x)), lines))
        return lines


    def masquaradeBottom(self, block):

        self.size = block.size
        self.padding = block.padding
        self.bottom = block.bottom
        self.lock = block.lock
        self.content = block.content
        self.generator = block.generator

        block.addRightNeighbor(self.right)
        self.right = block.right


    def printLine(self):
        """Print the next line of the current and all connected blocks. The algorithm is quite complicated because of possible neighbours
           and probably contained Locks between them. However, this is the core to understand and define how blocks are aligned inside 
           the output.

        Parameters:
            None

        Returns:
            None
        """
        #this parameter is an indicator for the while loop. If some block in the chain has
        #still lines to print after printing the current row, it will set the parameter to true
        #before the function complete. If it stays false till we end, all blocks should be empty
        returnBool = False

        #the self.generator object stores all lines of the block in a generator, aligned with the
        #information if the line was the last one inside the generator
        (line, last) = next(self.generator)
        print(line, end="")

        #if we have printed the last line of the block, we unlock the lock of our bottom neighbour
        if last and self.bottom and self.bottom.lock:
            self.bottom.lock.unlock()
        if last and self.vanishLock:
            self.vanishLock.unlock()


        #if there are right neighbours, print their current row.
        #if no right neigbour exists, print a newline
        if self.right and self.right.vanishLock and self.right.vanishLock.isUnlocked():
            self.right = self.right.right if self.right.right else None
        if self.right:
            returnBool = self.right.printLine() or returnBool
        else:
            print("")

        #if the printed line is the last one...
        if last:
            #and there is a bottom block
            if self.bottom:
                #chek if the master lock of the bottom neighbour is unlocked
                if self.bottom.lock.master == None or self.bottom.lock.master.isUnlocked():
                    #at this point our block is empty and our bottom is unlocked.
                    #we just replace ourself with out bottom neighbor and inherint
                    #our right neighbor to him. Now we have a fresh block and can 
                    #continue with printing
                    self.masquaradeBottom(self.bottom)
                    returnBool = True
                #if our bottom is still locked, create a generator with a single newline.
                #this generator will be empty on next printLine and we check if our bottom
                #is then unlocked again
                else:
                    blackMagic = lambda: [(yield( (" " * self.size, True)))]
                    self.generator = blackMagic()
                    returnBool = True
            #if no bottom is there, generate a generator with an empty line.
            #this is required if other Blocks still have stuff to print.
            #we set returnBool to false, since we have nothing more to say
            else:
                blackMagic = lambda: [(yield( (" " * self.size, True)))]
                self.generator = blackMagic()
                returnBool = False or returnBool
        
        #if we have not printed the last line, we want to continue and set returnBool to True
        else:
            returnBool = True
        return returnBool


    def printBlockChain(self):
        """Printing all rows from the current block and all his neighbours

        Parameters:
            None

        Returns:
            None
        """
        if not self.content:
            self.buildBlockChain()
        #just iterate over the block and print the lines
        while self.printLine():
            pass


    def getBlockChain(self):
        """Same as printBlockChain but instead of printing the blockChain it is returned
           as a string. 

        Parameters:
            None

        Returns:
            blockChain          (string)             String representation of the blockChain
        """
        sys.stdout = blockChain = StringIO()
        self.printBlockChain()
        sys.stdout = sys.__stdout__
        return blockChain.getvalue()


    def buildGenerator(self):
        """It turns out that for the print algorithm a generator of the Block contents is far
           more useful than a list. However, generators do not provide a check function if 
           they have elements in them, but throw an exception instead. This is not acceptable
           inside the print algorithm and therefore the generator build here contains the content 
           of the block along with a boolean which indicates if the current line is the last one.

        Parameters:
            None

        Returns:
            Generator           (str, bool)          The generator contains the different lines form self.contents
                                                     along with a bool, which is true if it is the last line
        """
        booleanArray = [False] * (len(self.content) -  1)
        booleanArray.append(True)
        iterateOver = zip(self.content, booleanArray)
        for line in iterateOver:
            yield(line)


    def createTextWrapper(self, initial=False):
        """Creates a TextWrapper object that is adjusted to the needs of the block

        Parameters:
            initial             (bool)                  specify if the wrapper uses initial indent

        Returns:
            TextWrapper         The TextWrapper fits all the needs of the current block
        """
        textWrapper = textwrap.TextWrapper();
        #we want to allow newlines in the body
        textWrapper.replace_whitespace = False
        #to match the block size, we have to subtract it from the Wrapper size
        textWrapper.width = self.size - (self.padding[1] + self.padding[3])
        #subsequent lines have to have an indent of the specified body-indent
        textWrapper.subsequent_indent = " " * self.bodyIndent
        #we may need initial indent (in case the head-separator contains a newline)
        if initial:
            textWrapper.initial_indent = textWrapper.subsequent_indent
        return textWrapper


    def addRightNeighbor(self, block):
        """Helper function which traverses the right neighbors of a block until it finds the last one.
           Once the last block is reached, it appends the Block from the arguments to this last Block.

        Parameters:
            block             (Block)                  Block which should be appended to the right chain

        Returns:
            None
        """
        mostRight = self
        while mostRight.right:
            mostRight = mostRight.right
        mostRight.right = block


    def addBottomNeighbor(self, block):
        """Helper function which traverses the bottom neighbors of a block until it finds the last one.
           Once the last block is reached, it appends the Block from the arguments to this last Block.

        Parameters:
            block             (Block)                  Block which should be appended to the bottom chain

        Returns:
            None
        """
        mostDown = self
        while mostDown.bottom:
            mostDown = mostDown.bottom
        mostDown.bottom = block
