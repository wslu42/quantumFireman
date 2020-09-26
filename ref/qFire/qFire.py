# Import the pygame library and initialise the game engine
import pygame, random, time
import numpy as np
from qiskit import QuantumCircuit, execute, BasicAer, ClassicalRegister, QuantumRegister
from qiskit.visualization import plot_histogram

def randlst(brickMax,brickN):
    lst = []
    for i in range(brickMax):
        if random.randint(0,1) ==1 and len(lst)!=brickN:
            lst += [i]
    return (lst)

def qbitPos(pos, brickswid = 40, scorXpos = 395, brickspit = 45):
    return (1 - (pos + brickswid//2 - scorXpos//2)//brickspit//2)

def fillCounts(counts):
    ctkeys = ['111', '110', '101', '100', '011', '010', '001', '000']
    for i in ctkeys:
        if not (i in counts.keys()):
            counts[i] = 0
    return(counts)

def str2myqc(myqc, GatesPerQubit):
    for i,k in enumerate(GatesPerQubit):
        for v in k:
            if v[0] == 'X':
                myqc.x(i)
            elif v[0] == 'H':
                myqc.h(i)
            elif v[0] == 'C':
                myqc.cx(int(v[1]),int(v[2]))
    return(myqc.copy())

def myqcMeas(myqc, qubitN=3, shots = 16, dev = 'qasm_simulator'):
    myqc.measure(list(range(qubitN)),list(range(qubitN)))
    backend = BasicAer.get_backend(dev)
    counts = execute(myqc, backend, shots=shots).result().get_counts()
    for i in counts:
        if counts[i] < shots//4:
            counts[i] = 0
    cts = {}
    for i in counts:
        if counts[i] != 0:
            cts.update({i:counts[i]})
    return(cts)

def drawGate(qbtPoslst, GatesPerQubit,gateS,all_gate_list):
    for i,k in enumerate(GatesPerQubit):
        for j,v in enumerate(k):
            if v[0] == 'X':
                gate = Gate((255,0,0),gateS,gateS)
                gate.rect.x = qbtPoslst[i][0]
                gate.rect.y = qbtPoslst[i][1] - (j+1)*(gateS +20)
                all_gate_list.add(gate)
            elif v[0] == 'H':
                gate = Gate((0,0,255),gateS,gateS)
                gate.rect.x = qbtPoslst[i][0]
                gate.rect.y = qbtPoslst[i][1] - (j+1)*(gateS +20)
                all_gate_list.add(gate)
            elif v[0] == 'C':
                gate = Gate((0,255,0),gateS,gateS)
                gate.rect.x = qbtPoslst[i][0]
                gate.rect.y = qbtPoslst[i][1] - (j+1)*(gateS +20)
                all_gate_list.add(gate)

class Paddle(pygame.sprite.Sprite):

    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill((1,0,0))
        self.image.set_colorkey((1,0,0))
        
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect()

    def moveLeft(self, pixels, BC):
        self.rect.x -= pixels
        if self.rect.x < BC:
            self.rect.x = BC

    def moveRight(self, pixels, BC):
        self.rect.x += pixels
        if self.rect.x > BC:
            self.rect.x = BC
            
class Gate(pygame.sprite.Sprite):

    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill((1,0,0))
        self.image.set_colorkey((1,0,0))
        
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect()

    def drop(self, pixelsPerFrame, BC):
        self.rect.y += pixelsPerFrame
        if self.rect.y > BC:
            self.rect.y = BC

#======================================================================


#======================================================================

def main():
    pygame.init()

    # Initialize colors and sounds
    BKGND = (1,0,0)
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    LIGHTBLUE = (0,176,240)

    RED = (255,0,0)
    ORANGE = (255,127,0)
    YELLOW = (255,255,0)
    GREEN = (0,255,0)
    BLUE = (0,0,255)
    INDIGO = (46,43,95)
    Violet = (139,0,255)
    colorlst = [Violet,INDIGO,BLUE,GREEN,YELLOW,ORANGE,RED]

    keyiSou = pygame.mixer.Sound('media\keyin.wav')
    spacSou = pygame.mixer.Sound('media\spacein.wav')
    missSou = pygame.mixer.Sound('media\missed.wav')
    catcSou = pygame.mixer.Sound('media\catch.wav')
    pygame.mixer.music.load('media\Chronos.mp3')
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1, 0.0)

    # Initialize game parameters
    score = 0
    lifes = 10 # how many misses allowed before game over
    speed = 1 # how fast the block drops, unit: pixels/sec

    genSpeed = 10 # the time spacing between the generation of each row , unit: sec
    catched = 0 # catched counts
    missed = 0 # missed counts

    brickN = 2
    circDepth = 4
    qubitN = 3
    GatesPerQubit = [[],[],[]]
    bitlst = np.asarray([0,0,0])

    brickRow = 1
    brickRowlst = []        
    binlst = ['111','110','101','100','011','010','001','000']
    xlst = []

    t0 = time.time()
    t00 = t0

    paused = False
    carryOn = True
    BrickGen = False
    clock = pygame.time.Clock()

    # unused parameters
    xQty,hQty,cxQty = 999,999,999
    dly = 0

    # Initialize visuals
    brickMax = 2**qubitN
    bricksdep, brickswid, bricksgap = 40, 40, 5
    brickspit= brickswid+ bricksgap

    brickGroupXShift = 20
    brickGroupYShift = bricksdep + bricksgap + brickGroupXShift
    dockYdep = 80
    dockYpos = brickGroupYShift + 5*(bricksdep + bricksgap) + bricksgap*2
    circYpos = dockYdep + dockYpos
    circYdep = 300
    scorXpos = brickGroupXShift*2+brickMax*brickspit-bricksgap
    scorXwid = 200
    gateS = 40

    qbt0PosX, qbt0PosY = scorXpos//2+brickspit*2, circYpos+circYdep//8
    qbt1PosX, qbt1PosY = scorXpos//2            , circYpos+circYdep//8
    qbt2PosX, qbt2PosY = scorXpos//2-brickspit*2, circYpos+circYdep//8

    qbtPoslst = [[qbt0PosX - brickswid//2, qbt0PosY+circYdep//8*6], 
                 [qbt1PosX - brickswid//2, qbt1PosY+circYdep//8*6],
                 [qbt2PosX - brickswid//2, qbt2PosY+circYdep//8*6]]

    myqc = QuantumCircuit(qubitN,qubitN)

    # Open a new window
    sizeX = scorXpos + scorXwid
    sizeY = circYpos + circYdep + brickGroupXShift
    size = (sizeX, sizeY)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Quantum Fireman Fireman")

    brickImg = pygame.image.load("media\\brick.png").convert()
    brickImg = pygame.transform.scale(brickImg, (gateS, gateS))

    # List all sprites
    all_sprites_list = pygame.sprite.Group()
    all_brick_list = pygame.sprite.Group()
    all_gate_list = pygame.sprite.Group()
    all_bucket_list = pygame.sprite.Group()
    all_list = [all_sprites_list, all_brick_list, all_gate_list, all_bucket_list]

    #Create the Paddles and Buckets
    p=range(brickMax)[-1]
    paddledep = bricksgap*2

    bucket1 = Paddle(YELLOW, brickswid, paddledep)
    bucket1.rect.x = brickGroupXShift + p*brickspit
    bucket1.rect.y = dockYpos - paddledep + dockYdep//4*1
    all_sprites_list.add(bucket1)

    paddle = Paddle(WHITE, brickswid, paddledep)
    paddle.rect.x = qbt1PosX - brickswid//2
    paddle.rect.y = qbt1PosY+circYdep//8*6 
    all_sprites_list.add(paddle)

    rendDict = [['000']]
    for i in rendDict:
        color = (55+200//len(rendDict),55+200//len(rendDict),55+200//len(rendDict))
        p = (2**np.asarray([2,1,0])*[int(j) for j in i]).sum()
        buck = Paddle(color,brickswid,paddledep)
        buck.rect.x = scorXpos - (brickGroupXShift + p*brickspit) - brickswid
        buck.rect.y = dockYpos - paddledep
        xlst += [scorXpos - (brickGroupXShift + p*brickspit) - brickswid]
        all_bucket_list.add(buck)

    class Brick(pygame.sprite.Sprite):

        def __init__(self, color, width, height):
            super().__init__()
            self.image = brickImg
            self.rect = self.image.get_rect()

        def drop(self, pixelsPerFrame, BC):
            self.rect.y += pixelsPerFrame
            if self.rect.y > BC:
                self.rect.y = BC

# -------- Main Program Loop -----------
    while carryOn:
        # --- Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                  carryOn = False

            # detect user input
            if event.type == pygame.KEYUP:

                # paddle movement
                if event.key == pygame.K_LEFT and not paused:
                    paddle.moveLeft (brickspit*2,BC=brickGroupXShift+1.5*brickspit)
                elif event.key == pygame.K_RIGHT and not paused:
                    paddle.moveRight(brickspit*2,BC=brickGroupXShift+5.5*brickspit)

                if event.key == pygame.K_x:
                    keyiSou.play()
                    all_gate_list.empty()

                    GatesPerQubit[qbitPos(paddle.rect.x)] += ['X']
                    if len(GatesPerQubit[qbitPos(paddle.rect.x)]) == circDepth:
                        GatesPerQubit[qbitPos(paddle.rect.x)] = GatesPerQubit[qbitPos(paddle.rect.x)][1:]
                    drawGate(qbtPoslst, GatesPerQubit, gateS, all_gate_list)

                    bitlst[qbitPos(paddle.rect.x)] = 1
                    p = (2**np.asarray([0,1,2])*bitlst).sum()
                    bucket1.rect.x = scorXpos - (brickGroupXShift + p*brickspit) - brickswid

                if event.key == pygame.K_z or event.key == pygame.K_h :
                    keyiSou.play()
                    all_gate_list.empty()

                    GatesPerQubit[qbitPos(paddle.rect.x)] += ['H']
                    if len(GatesPerQubit[qbitPos(paddle.rect.x)]) == circDepth:
                        GatesPerQubit[qbitPos(paddle.rect.x)] = GatesPerQubit[qbitPos(paddle.rect.x)][1:]
                    drawGate(qbtPoslst, GatesPerQubit, gateS, all_gate_list)

                    bitlst[qbitPos(paddle.rect.x)] = 0
                    p = (2**np.asarray([0,1,2])*bitlst).sum()
                    bucket1.rect.x = scorXpos - (brickGroupXShift + p*brickspit) - brickswid

                if event.key == pygame.K_c:
                    keyiSou.play()
                    all_gate_list.empty()

                    ctrl = qbitPos(paddle.rect.x)
                    GatesPerQubit[ctrl] += ['C{}'.format(ctrl)]
                    target = ctrl+1
                    if target == 3:
                        target = 0
                    GatesPerQubit[ctrl][-1] += str(target)
                    if len(GatesPerQubit[qbitPos(paddle.rect.x)]) == circDepth:
                        GatesPerQubit[qbitPos(paddle.rect.x)] = GatesPerQubit[qbitPos(paddle.rect.x)][1:]
                    drawGate(qbtPoslst, GatesPerQubit, gateS, all_gate_list)

                    bitlst[qbitPos(paddle.rect.x)] = 0
                    p = (2**np.asarray([0,1,2])*bitlst).sum()
                    bucket1.rect.x = scorXpos - (brickGroupXShift + p*brickspit) - brickswid

                if event.key == pygame.K_v:
                    keyiSou.play()
                    all_gate_list.empty()

                    ctrl = qbitPos(paddle.rect.x)
                    GatesPerQubit[ctrl] += ['C{}'.format(ctrl)]
                    target = ctrl-1
                    if target == -1:
                        target = 2
                    GatesPerQubit[ctrl][-1] += str(target)
                    if len(GatesPerQubit[qbitPos(paddle.rect.x)]) == circDepth:
                        GatesPerQubit[qbitPos(paddle.rect.x)] = GatesPerQubit[qbitPos(paddle.rect.x)][1:]
                    drawGate(qbtPoslst, GatesPerQubit, gateS, all_gate_list)

                    bitlst[qbitPos(paddle.rect.x)] = 0
                    p = (2**np.asarray([0,1,2])*bitlst).sum()
                    bucket1.rect.x = scorXpos - (brickGroupXShift + p*brickspit) - brickswid

                if event.key == pygame.K_p :
                    paused = not paused
                    pausedcheck = True
                    unpausedcheck = True
                    if paused and pausedcheck :
                        t1 = time.time()
                        pausedcheck = False
                    if (not paused) and unpausedcheck:
                        t2 = time.time()
                        unpausedcheck = False
                    if (not paused):
                        t0 += t2-t1
                        t00 += t2-t1

                if event.key == pygame.K_d:
                    spacSou.play()
                    GatesPerQubit[qbitPos(paddle.rect.x)] = []

                    for i in range(3):
                        gate = Gate(BLACK,gateS,gateS)
                        gate.rect.x = paddle.rect.x
                        gate.rect.y = paddle.rect.y - (i+1)*(gateS + 20)
                        all_gate_list.add(gate)

                    bitlst[qbitPos(paddle.rect.x)] = 0
                    p = (2**np.asarray([0,1,2])*bitlst).sum()
                    bucket1.rect.x = scorXpos - (brickGroupXShift + p*brickspit) - brickswid

                if event.key == pygame.K_SPACE and not paused:
                    spacSou.play()
                    all_gate_list.empty()
                    all_bucket_list.empty()
                    print(GatesPerQubit)

                    myqc_save = str2myqc(myqc, GatesPerQubit)
                    rendDict = myqcMeas(myqc, qubitN=3, shots = 16, dev = 'qasm_simulator')

                    xlst = []
                    for i in rendDict:
                        color = (55+200//len(rendDict),55+200//len(rendDict),55+200//len(rendDict))
                        p = (2**np.asarray([2,1,0])*[int(j) for j in i]).sum()
                        buck = Paddle(color,brickswid,paddledep)
                        buck.rect.x = scorXpos - (brickGroupXShift + p*brickspit) - brickswid
                        buck.rect.y = dockYpos - paddledep
                        xlst += [scorXpos - (brickGroupXShift + p*brickspit) - brickswid]
                        all_bucket_list.add(buck)

                    myqc = QuantumCircuit(qubitN,qubitN)
                    GatesPerQubit = [[],[],[]]
                    bitlst = np.asarray([0,0,0])
                    bucket1.rect.x = scorXpos - (brickGroupXShift + 0*brickspit) - brickswid

        if not paused:
            if time.time()-t0 > genSpeed:
                t0 = time.time()
                bricklst = []
                k=-1
                if random.randint(0,7) ==1: k=-5
                for i in randlst(brickMax, brickN):
                    brick = Brick(colorlst[k],brickswid,bricksdep)
                    brick.rect.x = brickGroupXShift + i* brickspit
                    brick.rect.y = brickGroupYShift + 0*(bricksdep + bricksgap)
                    bricklst += [brick]
                BrickGen = True

            if time.time()-t00 >= 90:
                genSpeed -= 2
                print(genSpeed)
                t00 = time.time()

            if BrickGen:
                all_brick_list.empty()
                brickRowlst += [bricklst]
                for bR in brickRowlst:
                    for b in bR:
                        all_brick_list.add(b)
                BrickGen = False

            if brickRowlst != []:
                for bR in brickRowlst:
                    for b in bR:
                        b.drop(pixelsPerFrame=speed, BC = dockYpos - paddledep)
                b = brickRowlst[0]
                if b[0].rect.y >= dockYpos - paddledep -gateS +2*speed:

                    bxlst = []
                    misslst = []
                    miss = False
                    for i in b:
                        bxlst += [i.rect.x]
                        misslst += [not(i.rect.x in xlst)]
                    for i in xlst:
                        misslst += [not(i in bxlst)]
                    for i in misslst:
                        miss = miss or i
                    if miss:
                        missed -= 1
                        missSou.play()
                    else:
                        catched += 1
                        catcSou.play()
                    [all_brick_list.remove(b) for b in brickRowlst[0]]
                    brickRowlst = brickRowlst[1:]

        [i.update() for i in all_list]


        # --- Drawing code should go here

        screen.fill(BKGND)
        pygame.draw.line(screen, WHITE, [0, brickGroupXShift], [scorXpos, brickGroupXShift], 2)
        pygame.draw.line(screen, WHITE, [0, dockYpos], [scorXpos, dockYpos], 2)
        pygame.draw.line(screen, WHITE, [0, circYpos], [scorXpos, circYpos], 2)
        pygame.draw.line(screen, WHITE, [scorXpos, 0], [scorXpos, sizeY], 2)
        pygame.draw.line(screen, WHITE, [qbt0PosX+brickspit//2-1, qbt0PosY], [qbt0PosX+brickspit//2-1, qbt0PosY+circYdep//8*6], 2)
        pygame.draw.line(screen, WHITE, [qbt0PosX-brickspit//2-1, qbt0PosY], [qbt0PosX-brickspit//2-1, qbt0PosY+circYdep//8*6], 2)
        pygame.draw.line(screen, WHITE, [qbt1PosX+brickspit//2-1, qbt1PosY], [qbt1PosX+brickspit//2-1, qbt1PosY+circYdep//8*6], 2)
        pygame.draw.line(screen, WHITE, [qbt1PosX-brickspit//2-1, qbt1PosY], [qbt1PosX-brickspit//2-1, qbt1PosY+circYdep//8*6], 2)
        pygame.draw.line(screen, WHITE, [qbt2PosX+brickspit//2-1, qbt2PosY], [qbt2PosX+brickspit//2-1, qbt2PosY+circYdep//8*6], 2)
        pygame.draw.line(screen, WHITE, [qbt2PosX-brickspit//2-1, qbt2PosY], [qbt2PosX-brickspit//2-1, qbt2PosY+circYdep//8*6], 2)

        font = pygame.font.Font(None, 18)
        text = font.render("You have MISSED: " + str(missed), 1, WHITE)
        linePos = 10
        screen.blit(text, (scorXpos+20,linePos))
        text = font.render("You have CATCHED: " + str(catched), 1, WHITE)
        linePos += 20
        screen.blit(text, (scorXpos+20,linePos))

    #     text = font.render("x gate available: " + str(xQty), 1, WHITE)
    #     linePos += 40
    #     screen.blit(text, (scorXpos+20,linePos))
    #     text = font.render("h gate available: " + str(hQty), 1, WHITE)
    #     linePos += 20
    #     screen.blit(text, (scorXpos+20,linePos))
    #     text = font.render("cx gate available: " + str(cxQty), 1, WHITE)
    #     linePos += 20
    #     screen.blit(text, (scorXpos+20,linePos))

    #     text = font.render("DISPLAY", 1, WHITE)
    #     linePos += 40
    #     screen.blit(text, (scorXpos+20,linePos))
    #     text = font.render("Red block: X gate", 1, WHITE)
    #     linePos += 30
    #     screen.blit(text, (scorXpos+20,linePos))
    #     text = font.render("Blue block: Hadamard gate", 1, WHITE)
    #     linePos += 30
    #     screen.blit(text, (scorXpos+20,linePos))
    #     text = font.render("Green block: CX gate", 1, WHITE)
    #     linePos += 30
    #     screen.blit(text, (scorXpos+20,linePos))

        text = font.render("CONTROL", 1, WHITE)
        linePos += 40
        screen.blit(text, (scorXpos+20,linePos))
        text = font.render("x: add an X gate.", 1, WHITE)
        linePos += 30
        screen.blit(text, (scorXpos+20,linePos))
        text = font.render("z/h: add an Hadamard gate.", 1, WHITE)
        linePos += 30
        screen.blit(text, (scorXpos+20,linePos))
        text = font.render("c/v: add a CX gate with...", 1, WHITE)
        linePos += 30
        screen.blit(text, (scorXpos+20,linePos))
        text = font.render("control - current paddle", 1, WHITE)
        linePos += 20
        screen.blit(text, (scorXpos+20,linePos))
        text = font.render("target - Left/Right qubit", 1, WHITE)
        linePos += 20
        screen.blit(text, (scorXpos+20,linePos))
        text = font.render("space - load quantum circuit", 1, WHITE)
        linePos += 30
        screen.blit(text, (scorXpos+20,linePos))
        text = font.render("p - paused", 1, WHITE)
        linePos += 30
        screen.blit(text, (scorXpos+20,linePos))

        text = font.render("Developed by Wen-Sen Lu", 1, WHITE)
        linePos += 200
        screen.blit(text, (scorXpos+20,linePos))
        text = font.render("wslu42@gmail.com", 1, WHITE)
        linePos += 20
        screen.blit(text, (scorXpos+20,linePos))
        text = font.render("Consultants: Junye Huang,", 1, WHITE)
        linePos += 30
        screen.blit(text, (scorXpos+20,linePos))
        text = font.render("& Dimo Tsai, Lilo Wang.", 1, WHITE)
        linePos += 20
        screen.blit(text, (scorXpos+20,linePos))

        for i in range(brickMax):
            text = font.render(binlst[i], 1, WHITE)
            screen.blit(text, (brickGroupXShift + i*brickspit +10, dockYpos+dockYdep//6*5))
        qbtLbllst = [(qbt0PosX - brickspit//2-1+8, qbt0PosY), 
                     (qbt1PosX - brickspit//2-1+8, qbt1PosY), 
                     (qbt2PosX - brickspit//2-1+8, qbt2PosY)] 
        for i in range(qubitN):
            text = font.render('qbit'+str(i), 1, WHITE)
            screen.blit(text, qbtLbllst[i])

        #Now let's draw all the sprites in one go. (For now we only have 2 sprites!)
        [i.draw(screen) for i in all_list]


        if missed == -1*lifes:
            #Display Game Over Message for 3 seconds
            font = pygame.font.Font(None, 74)
            text = font.render("GAME OVER", 1, WHITE)
            screen.blit(text, (50,300))
            pygame.display.flip()
            pygame.time.wait(10000)

            #Stop the Game
            carryOn=False

        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # --- Limit to 60 frames per second
        clock.tick(10)

    #Once we have exited the main program loop we can stop the game engine:
    pygame.mixer.music.stop()

if __name__ == '__main__':
    main()
    pygame.quit()