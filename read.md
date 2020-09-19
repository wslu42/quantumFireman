Hey I wrote a games based on the idea of https://github.com/HuangJunye/QPong by Qiskit advocate Junye Huang!

In this game, I tried to redefine the mechanism such that we forced user to use quantum gates to perform something cannot be achieved by using binary operation, which is essentially using X gate along.

Here are the game controls:

1. Use arrow to move paddle between 3 qubits

2. Use c/x/z to add one CX/X/H gate to the qubit where paddle stays.
2.1. Noticed that c(CX) operate like this: set current location where paddle is to be the control and the right one next to the current qubit to be control.
2.2. Noticed that v(CX) operate like this: set current location where paddle is to be the control and the left one next to the current qubit to be control.
2.3. Noticed that h works like z.

3. Hit space to load the quantum circuit and move bucket to "catch" the falling humanoid blocks

4. If you missed 10 times it will be game over!

5. check out the availble PNG files for circuit examples and the outputs! The green ones are all CX gate created by c.

hey我寫了一個量子小遊戲
如果有興趣的話可以幫我試玩一下XD  不過我都只有周末會寫
然後看缺什麼package就裝什麼，應該只需要裝qiskit跟pygame

遊戲裡面左右可以移動游標，cxz可以添加量子閘在三個qubit上，添加完後把這組量子電路按空白鍵輸出，會得到000,001,010,011,100,101,110,111這八種可能性的其中幾種(古典狀態只會有一種)，"bucket"就會移動到對應的位置
遊戲的任務就是用bucket接到所有下落中的磚塊小人

x gate的作用跟古典的not gate一樣，把0翻到1或1翻到0。所以比方說我們想把bucket移到010這個位置上，就把paddle游標移到中間的qubit按下x，然後按空白鍵，就會看到bucket移到010的位置

要注意的是一個qubit最多允許三個閘，所以剛剛這個例子如果在空白鍵之前再按一次x就會看到兩個紅色方塊，按空白鍵後會得到000(中間又翻回0了)，同理如果按三次x才按空白鍵，就會回到010

h gate (按z)比較複雜，他會允許這個qubit最後量測出現在0與1的位置，也就是說如果paddle在最左邊的qubit上按z添加藍色的h gate後按空白鍵的話，bucket會出現在100與000這兩個位置，這就是所謂的量子疊加(superposition)

cx gate則是完成所謂量子糾纏的閘(entanglement)，實際的作用有點難用文字解釋，實際操作可能比較好懂

基本上遊戲中會遇到一些只靠x跟h無法處理的落磚(磚頭一次掉落1-2個)，比方說000&011

000&011這組狀態看似可以靠[0,h,h]這組電路，但實際給出的組合為000&010&001&011，所以不合

000&011的解法是在右邊的qubit按z再按c。c的功能是針對c所在的位置去動左邊一個qubit的態

右邊的qubit按h後會出現0與1這兩種可能，而c的功能是當當前qubit為1時就去把左邊一個qubit翻動(自動加上x)，當前為0時則不動，稱為control-not

也就是說0?1時中間會是1，0?0時中間會是0

https://www.youtube.com/watch?v=_MzocuKu18A
忘了說我打算把它改成跟這個遊戲致敬！

Consultants:
Junye Huang, Dimo Tsai, LiLo Wang 
