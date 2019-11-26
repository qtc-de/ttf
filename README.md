## ttf - Terminal Text Formater

*ttf* is a pyhton library that makes design of component based console output very easy. It uses Block objects to align different compoents with each other to create a structured and flexible console based output.


### Installation

-----

**Via setup.py**

To install it, make sure you have Python 3.6 or greater installed.  Then run these command from the command prompt:

```
$ pip3 install -r requirements.txt --user
$ python3 setup.py install --user
```

**As pip package**

If you want to generate a pip package instead, run the following command from
the command prompt:

```
$ python3 setup.py sdist
```

You can then install the library via pip using:

```
$ pip3 install dist/ttf-1.1.0.tar.gz --user
```


### Description 

-----

Instead of giving a high level description of *ttf*, we will examine three simple examples that show you basically everything that you need to know about *ttf*. Although the complexity of the examples will be increasing, you should be able to follow and the time to read this should not take more than 10 minutes. So lets jump in!


**Example 1**

-----

Consider you develop a console application written in python. The idea of your application is to read in some data from files or a database and to display the contents into a well structured format on console. Furthermore, consider the data to be structured into logical units that need to be displayed blockwise on console. After making some notes on your scratchpad, your first draft for the layout of the output looks like this:

```
#              Block Layout:                     
#                                                         
#   __________    __________    __________ 
#  |          |  |          |  |          |
#  |  Block1  |  |  Block2  |  |  Block3  |
#  |          |  |__________|  |__________|
#  |          |                            
#  |          |   __________    __________ 
#  |          |  |          |  |          |
#  |          |  |  Block4  |  |  Block5  |
#  |__________|  |__________|  |__________|
#                                                                                                    
```
Each block forms one component of your output and contains most likely related data. E.g. if your application is used to fetch information of the employees database, Block1 could contain the name and a description of the employee. Block2 could contain his current position and salary. Block3 could store information about team memberships and so on...

Such a situation is the ideal use case for *ttf* and exactly the purpose it was written for. Imagine you would have to write a structure as the above one just by using **print** functions. It would be an absolutly pain because you cannot know in advance how many data each block contains. On your scratchpad the blocks are of course well aligned, but block2 could contain more rows than block3, destroing the well aligned layout. 

With *ttf*, implementing such a block structure is very easy. You do it by defining an object for each block and just define neighborship relationships between the different blocks. Here is the source code for creating the above mentioned block structure:

```python
from ttf import Block, Lock
 
blocksize = 40
defaultPadding = [0, 5, 1, 0]

headline = "Example Block: "
headlineColor = "yellow#bold"
headlineNewline = False

body = "oooooooooooooooooooooooooo"
bodyColor = "blue#bold"
bodyIndent = "auto"

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
Block5 = Block2.clone()

Block1.right = Block2
Block2.right = Block3
Block2.bottom = Block4
Block3.bottom = Block5

print()
Block1.printBlockChain()
```
As you can see we simply create one Block object for each block that we want to see in our output. Then we are connecting the different blocks by using neighborship relationships. Specifying the correct neighborships make take a little bit of practice, but once you get used to it should be pretty self evident. Here is an updated version of our scratchpad, after adding neighborship relationships:

```
#              Block Layout:                     
#                                                         
#   __________    __________    __________ 
#  |          |--|          |--|          |
#  |  Block1  |  |  Block2  |  |  Block3  |
#  |          |  |__________|  |__________|
#  |          |   |             |          
#  |          |   __________    __________ 
#  |          |  |          |  |          |
#  |          |  |  Block4  |  |  Block5  |
#  |__________|  |__________|  |__________|
#                                                                                                    
```
Now it is time to view the output of our code. Notice that we did used just some placeholder text for the blocks and that the contents of our output are not that interisting. That matters is that the structure of the different blocks!

```
$ python3 basic.py 

Example Block: oooooooooooooooooooo     Example Block: oooooooooooooooooooo     Example Block: oooooooooooooooooooo     
               oooooooooooooooooooo                    oooooooooooooooooooo                    oooooooooooooooooooo     
               oooooooooooooooooooo                    oooooooooooooooooooo                    oooooooooooooooooooo     
               oooooooooooooooooooo                    oooooooooooooooooo                      oooooooooooooooooooo     
               oooooooooooooooooooo                                                            oooooooooooooooooooo     
               oooooooooooooooooooo     Example Block: oooooooooooooooooooo                    oooooooooooooooooooo     
               oooooooooooooooooooo                    oooooooooooooooooooo                    oooooooooo               
               oooooooooooooooooooo                    oooooooooooooooooooo                                             
               oooooooooooooooooooo                    oooooooooooooooooo       Example Block: oooooooooooooooooooo     
               oooooooooooooooooooo                                                            oooooooooooooooooooo     
               oooooooooooooooooooo                                                            oooooooooooooooooooo     
               oooooooooooooooooooo                                                            oooooooooooooooooo       
               oooooooooooooooooooo                                                                               
```
Nice! That looks almost like the structure we did draw on our scratchpad. However, as you can see *Block4* and *Block5* are not well aligned. This problem will be fixed in Example 2! If you look back on the sourcecode we used to generate this example, you may think that it is a little bit verbose and lengthy. However, in the other examples you will see that once you have written the initial code, the management of Blocks and their contents becomes amazingly scalable and easy to handle. So lets go over to the other examples!

**Example 2**

-----

In example 1 we saw how simple it is to create a component based output with *ttf*. However, we also saw that blocks with different lengths are not that well aligned now. To fix this problem, we introduce new objects that are called **Locks**. Locks are usually used in *ttf* to align a certain block-row of your output. In the code from example 1 we would assign Block4 and Block5 to the same Lock object in order to align them. Locks are closed as long as a parent block of the corresponding block-row has something to print. In our case the parent blocks are Block2 and Block3. As soon as both of them are empty, the Lock object for the next block-row gets unlocked and the blocks assigned to this Lock start to print. 

Here is how that looks like in code:
```python
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
Block1.printBlockChain()
```
You can add locks to existing Blocks using **addPrintMaster** or define them already in the consturctor by using ``printMaster=...`` as a function parameter. When cloning a Block, Locks are normally not inherited. Therfore you need to specify the variable ``withLocks=True``. 

With out new modifications our output now matches exactly the desired block structure from our scratchpad:

```
$ python3 printLocks.py 

Example Block: oooooooooooooooooooo     Example Block: oooooooooooooooooooo     Example Block: oooooooooooooooooooo     
               oooooooooooooooooooo                    oooooooooooooooooooo                    oooooooooooooooooooo     
               oooooooooooooooooooo                    oooooooooooooooooooo                    oooooooooooooooooooo     
               oooooooooooooooooooo                    oooooooooooooooooo                      oooooooooooooooooooo     
               oooooooooooooooooooo                                                            oooooooooooooooooooo     
               oooooooooooooooooooo                                                            oooooooooooooooooooo     
               oooooooooooooooooooo                                                            oooooooooo               
               oooooooooooooooooooo                                                                                     
               oooooooooooooooooooo     Example Block: oooooooooooooooooooo     Example Block: oooooooooooooooooooo     
               oooooooooooooooooooo                    oooooooooooooooooooo                    oooooooooooooooooooo     
               oooooooooooooooooooo                    oooooooooooooooooooo                    oooooooooooooooooooo     
               oooooooooooooooooooo                    oooooooooooooooooo                      oooooooooooooooooo       
               oooooooooooooooooooo                                                                                     
```
Nice! However, this example was just a slight modification of example 1 and does not show how scalable and easy managble the *ttf* library makes your code. So lets look at the more complex example 3 to get a feeling for that.

**Example 3**

-----

After you have created the block layout from your scratchpad, you notice that the structure is not ideal to represent your data. You decide to switch the block structure and create a second draft on your scratchpad:

```
#                       Block Layout:                     
#                                                         
#   __________    __________    __________     __________ 
#  |          |  |          |  |          |   |          |
#  |  Block1  |  |  Block2  |  |  Block3  |   |  Block4  |
#  |          |  |__________|  |__________|   |          |
#  |          |                               |          |
#  |          |   _________________________   |          |
#  |          |  |                         |  |          |
#  |          |  |         Block5          |  |          |
#  |          |  |_________________________|  |          |
#  |          |                               |          |
#  |          |   __________    __________    |          |
#  |          |  |          |  |          |   |          |
#  |          |  |  Block6  |  |  Block7  |   |          |
#  |__________|  |__________|  |__________|   |__________|
#                                                                                                    
```
If you would have created your first layout with **print** functions, this would be the moment you would have to delete your complete code and write everything again for the new layout. However, with ttf such a change becomes easy managble. 

The first thing we should do is to think about neighborship relationships. This is not that easy as before, since we have some new concepts here. From block-row 1 to block-row 2 for example, we have to reduce the number of blocks and from block-row 2 to block-row 3, there is one additional block to add. 

Well, for the second case we do not need to introduce new concepts at all. We simply define Block6 to be the bottom neighbor of Block5 and then choose Block7 to be the right neighbor of Block6. tff is smart enough to handle the transition from one to two blocks on its own. However, for the transition from two blocks to one, like from block-row 1 to block-row 2 we need to introduce a new concept. 

To understand this new concept I will first of all show the final neighborship relationships that are used for the desired block layout:

```
#                       Block Layout:                     
#                                                         
#   __________    __________    __________     __________ 
#  |          |--|          |--|          |- -|          |
#  |  Block1  |  |  Block2  |  |  Block3  |   |  Block4  |
#  |          |  |__________|  |__________|   |          |
#  |          |   |                 V         |          |
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
```
Okay, as you can see Block3 was marked by a **V** which means that this block will vanish after it has printed all its contents. When a block vanishes, its right neighbor simply becomes the right neighbor of the previous block (Block2 in our example). However, this leads to a problem. If Block3 just vanishes after it printed all its contents, while Block2 has still stuff to print, Block4 will print some of his contents into the gap there Block3 was previously. Or to put in mroe easily: Block3 should not vanish directly after it got empty, but should vanish then Block5 starts to print. 

Fortunately we have already the concept of Locks, that prevent bottom neighbors from beeing printed while parent blocks have still content. We can take advantage of this concept for vanishing blocks and introduce a new object property called **vanishMaster**. The vanishMaster property expects a Lock object as value. Once a lock was assigned, the corresponding block will vanish after it is empty **and** after the assigned lock gets unlocked.

To solve our problem we simply assign Block5 and Block3 to the same Lock object. In Block5 we set the Lock to be the **printMaster**, preventing the block from beeing printed until Block2 and Block3 have finished with their content. In Block3 we will set the lock as the **vanishMaster**, preventing the block from beeing vanished until Block2 and Block3 have finsihed with thrie contents. 

Here is now finally the code to produce the above layout:

```
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
Block1.printBlockChain()
```
This is now the moment you should realize how amazing the *ttf* library is. Using the already excisting code from example 2, getting to this new code can be done in a minimum of time. You basically just need to copy some stuff and to update the neighborship relationships.
Here is the corresponding output:

```

$ python3 vanishLocks.py 

Example Block: oooooooooooooooooooo     Example Block: oooooooooooooooooooo     Example Block: oooooooooooooooooooo     Example Block: oooooooooooooooooooo     
               oooooooooooooooooooo                    oooooooooooooooooooo                    oooooooooooooooooooo                    oooooooooooooooooooo     
               oooooooooooooooooooo                    oooooooooooooooooooo                    oooooooooooooooooooo                    oooooooooooooooooooo     
               oooooooooooooooooooo                    oooooooooooooooooooo                    oooooooooooooooooooo                    oooooooooooooooooooo     
               oooooooooooooooooooo                    oooooooooooooooooooo                    oooooooooooooooooooo                    oooooooooooooooooooo     
               oooooooooooooooooooo                    oooo                                    oooo                                    oooooooooooooooooooo     
               oooooooooooooooooooo                                                                                                    oooooooooooooooooooo     
               oooooooooooooooooooo     Example Block: oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo                    oooooooooooooooooooo     
               oooooooooooooooooooo                    oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo                    oooooooooooooooooooo     
               oooooooooooooooooooo                    oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo                    oooooooooooooooooooo     
               oooooooooooooooooooo                    oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo                    oooooooooooooooooooo     
               oooooooooooooooooooo                    oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo                    oooooooooooooooooooo     
               oooooooooooooooooooo                    oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo                    oooooooooooooooooooo     
               oooooooooooooooooooo                    oooooooooooooooooooooooooooooo                                                  oooooooooooooooooooo     
               oooooooooooooooooooo                                                                                                    oooooooooooooooooooo     
               oooooooooooooooooooo     Example Block: oooooooooooooooooooo     Example Block: oooooooooooooooooooo                    oooooooooooooooooooo     
               oooooooooooooooooooo                    oooooooooooooooooooo                    oooooooooooooooooooo                    oooooooooooooooooooo     
               oooooooooooooooooooo                    oooooooooooooooooooo                    oooooooooooooooooooo                    oooooooooooooooooooo     
               oooooooooooooooooooo                    oooooooooooooooooooo                    oooooooooooooooooooo                    oooooooooooooooooooo     
               oooooooooo                              oooooooooooooooooooo                    oooooooooooooooooooo                    oooooooooo               
                                                       oooo                                    oooo   
```
If you were able to follow the above description you should have a pretty solid understanding of the *ttf* library and be able to use it inside your own programs. If I find time for it I will also document the different classes and functions inside the Wiki-Pages. However, for now you will find detailed documentation inside the sourcecode. 


### Warning

-----

It should be noticed that this library was not an intended project. It was only a by-product of other projects and was only tested in the context of these other projects. 
There is no gurantee that there are no bugs or other problems with the project. If you encounter any problems, please report them by submitting an issue.


*Copyright 2019, Tobias Neitzel and the ttf contributors.*
