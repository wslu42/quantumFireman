Hey I wrote a games (qFire.ipynb) based on the idea of https://github.com/HuangJunye/QPong by Qiskit advocate Junye Huang!

In this game, I tried to force users to use quantum gates to perform something cannot be done by using binary operation along.

There are three modes in the game: sandbox, training, and challenger. Once you load the game by running all the cells in one of the jupyter notebooks (qFire or qShooter), you immediately enter the sandbox mode. In this mode you can first familiar yourself with the control and check how quantum gates work with the list of controls on the right as a reference. Once you feel comfortable with the interface hit 2 to enter the next stage.

The next stage starts with training mode. In this mode we will generate states from easy ones to advanced ones such as Bell states and GHZ states. You mission is to use quantum gates to assemble a quantum circuit which gives a set of possible states after measurement matching to the falling humanoid blocks. In the training mode we drop 5 blocks in each category (binary/superposition/Bell/GHZ), and after 20 blocks you will enter the challenger mode and the game statistics will be reset. Try to collect as many blocks as you can before missing 10 blocks in the challenger mode!

Before you start, you should know a bit about how the measurement works in this game. Since we don’t have unlimited resources we only use 16 shots in each step while you press space to load the circuit, and only the states with counts more than 3 will be considered when we map the states to the position of buckets. As a result, there are two consequences:
1.	It is highly unlikely to catch the blocks by trivially putting Hadamard gates to each qubit. Yes potentially we generate all possible states, but due to the lower limit of counts it results in uncontrollable collapse of states and most of the time you will end up with no bucket after mapping!
2.	To maximize the chance of getting desired states, try to match the exact state set by putting together the right quantum circuit! Also prepare for the possibility of missing some expected states since we have limited measurement shots. Hey it is supposed to be a quantum game!

Finally, the difference between qFire and qShooter is about how familiar yourself to this game. If you are new to the UI I would suggest start with qFire, but if you are looking for a quick practice just hop on to the qShooter. Enjoy and let me know your thoughts to make it better!

Personal high-score on qShooter. Enjoy the game!

![image](https://github.com/wslu42/quantumFireman/blob/master/hc.png)

///

Here are the game controls:

Use arrow to move paddle between 3 qubits

1. Use c(v)/x/z(h) to add one CX/X/H gate to the qubit where paddle stays. 

2. Noticed that c(CX) operate like this: set current location where paddle is to be the control and the right one next to the current qubit to be control. Noticed that v(CX) operate like this: set current location where paddle is to be the control and the left one next to the current qubit to be control. Noticed that h works like z.

3. Hit space to load the quantum circuit and move bucket to "catch" the falling humanoid blocks

4. If you missed 10 times it will be game over in the challenger mode! Press 2 again can reset game statistics in challenger mode.

5. Check out the availble PNG files under folder "ref" for circuit examples and the outputs! The green ones are all CX gate created by c.

hey我寫了一個量子小遊戲 如果有興趣的話可以幫我試玩一下XD 不過我都只有周末會寫 然後看缺什麼package就裝什麼，應該只需要裝qiskit跟pygame

遊戲裡面左右可以移動游標，cxz可以添加量子閘在三個qubit上，添加完後把這組量子電路按空白鍵輸出，會得到000,001,010,011,100,101,110,111這八種可能性的其中幾種(古典狀態只會有一種)，"bucket"就會移動到對應的位置 遊戲的任務就是用bucket接到所有下落中的磚塊小人

x gate的作用跟古典的not gate一樣，把0翻到1或1翻到0。所以比方說我們想把bucket移到010這個位置上，就把paddle游標移到中間的qubit按下x，然後按空白鍵，就會看到bucket移到010的位置

要注意的是一個qubit最多允許三個閘，所以剛剛這個例子如果在空白鍵之前再按一次x就會看到兩個紅色方塊，按空白鍵後會得到000(中間又翻回0了)，同理如果按三次x才按空白鍵，就會回到010

h gate (按z)比較複雜，他會允許這個qubit最後量測出現在0與1的位置，也就是說如果paddle在最左邊的qubit上按z添加藍色的h gate後按空白鍵的話，bucket會出現在100與000這兩個位置，這就是所謂的量子疊加(superposition)

cx gate則是完成所謂量子糾纏的閘(entanglement)，實際的作用有點難用文字解釋，實際操作可能比較好懂

基本上遊戲中會遇到一些只靠x跟h無法處理的落磚(磚頭一次掉落1-2個)，比方說000&011

000&011這組狀態看似可以靠[0,h,h]這組電路，但實際給出的組合為000&010&001&011，所以不合

000&011的解法是在右邊的qubit按z再按c。c的功能是針對c所在的位置去動左邊一個qubit的態

右邊的qubit按h後會出現0與1這兩種可能，而c的功能是當當前qubit為1時就去把左邊一個qubit翻動(自動加上x)，當前為0時則不動，稱為control-not

也就是說0?1時中間會是1，0?0時中間會是0

https://www.youtube.com/watch?v=_MzocuKu18A 忘了說我打算把它改成跟這個遊戲致敬！

Consultants: Junye Huang, Dimo Tsai, LiLo Wang
