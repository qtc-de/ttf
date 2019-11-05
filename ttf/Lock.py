class Lock: 
    """Locks are used to specify that certain Blocks have to be printed into one row. Consider you have a
       total of five blocks to be printed and you want a structure like:

          ------------     ----------              ----------
         |   Block0   |---|  Block1  |            |  Block2  |
         |            |   |          |------------|          |
         |            |   |  ######  |            |  ######  |
         |            |   |          |            |  ######  |
         |            |    ----------              ----------
         |            |         |                      |
         |            |    ----------              ----------
         |            |   |  Block3  |~~~ Lock ~~~|  Block4  |
         |            |   |          |            |          |
         |            |   |  ######  |            |  ######  |
         |____________|    ----------              ----------

        Notice that block 1 would actually end one line earlier than block 2, destroying the alignment of
        Block 3 and 4. However, if Block3 and Block4 are members of a Lock object which a closed status,
        Block1 would not go over to printing Block3 until the lock was opened. The lock will open automatically
        if the parent of a block containing a Lock prints his last line. 

    Parameters:
        None

    Returns:
        None
    """


    def __init__(self, unlocked=True, master=None):
        """Creates a new Lock object which is open by default. A lock has its own locked status 
           but contains also a list of sublocks. Only if all sublocks are unlocked, the overall
           Lock can be considered as unlocked

        Parameters:
            unlocked            (bool)              Describes if the lock is locked or opened
            master              (Lock)              The master lock the lock is assigned to

        Returns:
            Lock                (Lock)              The new created Lock object
        """
        #sublocks are not added in the consturctor, but by using the makeSlave function
        self.sublocks = []
        self.master = master
        self.unlocked = unlocked
        if self.master:
            self.makeSlave(self.master)


    def clone(self):
        """Clones a Lock object and sets the new Lock object to the same lock state and same master

        Parameters:
            None

        Returns:
            clonedLock          (Lock)              clone from self with same state and master
        """
        clonedLock = Lock(self.unlocked, self.master)
        return clonedLock


    def unlock(self):
        """Changes the state of a Lock from locked to unlocked. This is only true for the lock itself
           and does not affect sublocks. Notice that a Lock is considered locked until all sublocks are
           unlocked

        Parameters:
            None

        Returns:
            None
        """
        self.unlocked = True


    def isUnlocked(self):
        """Checks if a Lock is unlocked by looking a the Lock itself and all the sublocks.

        Parameters:
            None

        Returns:
            returnValue         (bool)              Returns True if unlocked, False otherwise
        """
        returnValue = self.unlocked
        for sublock in self.sublocks:
            returnValue = returnValue and sublock.unlocked
        return returnValue


    def makeSlave(self, printMaster):
        """Helper function that is used to append a Lock to the SubLock list of the corresponding printMaster

        Parameters:
            printMaster          (Lock)              The lock to which self is appended

        Returns:
            None
        """
        if printMaster:
            printMaster.sublocks.append(self)
