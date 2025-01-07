import pyxel
import math

class App:
    def __init__(self):
        pyxel.init(200,200)
        self.pads = Pad()
        self.mikata = Mikata()
        self.bullet = []
        self.dangan = []
        self.tekia = Tekia()
        self.tekib = Tekib()
        self.score = 10
        self.life = 5
        self.energy = 8
        self.clear = False
        self.gameover = False
        self.fire = []
        pyxel.load('保存するファイルパス.pyxres')
        pyxel.sounds[0].set(notes='B2C2', tones='PS', volumes='36', effects='SF', speed=10)
        pyxel.sounds[1].set(notes='F2E2F2E2', tones='SSSS', volumes='3333', effects='NNNN', speed=5)
        pyxel.sounds[2].set(notes='F1E1D1C1', tones='SSSS', volumes='3333', effects='NNNN', speed=8)
        pyxel.sounds[3].set(notes='F1E1D1C1F1E1D1C1F1E1D1C1F1E1D1C1', tones='SSSSSSSSSSSSSSSS', volumes='3333333333333333', effects='NNNNNNNNNNNNNNNN', speed=8)
        pyxel.run(self.update, self.draw)
    
    def update(self):
        self.pads.x = pyxel.mouse_x
        self.pads.y = pyxel.mouse_y
        self.pads.update(self.bullet)
        self.mikata.update(self.dangan)
        self.tekia.move()
        self.tekib.move()
        self.mikata.move()

        for i in reversed(range(len(self.bullet))):
            if not self.bullet[i].move():
                del self.bullet[i]
        
        for i in reversed(range(len(self.dangan))):
            if not self.dangan[i].move():
                del self.dangan[i]

        for bullet in self.bullet:
            bullet.move()

            if self.tekia.catcha(bullet):
                pyxel.play(0, 1)
                bullet.s *= -1.3
            if self.tekib.catcha(bullet):
                pyxel.play(0, 1)
                bullet.s *= -1.3

            if bullet.y <= 86 and 60 <= bullet.x <= 140:
                self.score += -1
                pyxel.play(0, 0)
            if self.score <= 0:
                self.clear = True
                self.fire.append(Fire(pyxel.mouse_x,pyxel.mouse_y))
            for i in range(len(self.fire)-1, -1, -1):
                if not self.fire[i].alive:
                    del self.fire[i]
            for f in self.fire:
                f.update()

            if self.pads.catcha(bullet):
                self.life -= 1
                pyxel.play(0, 2)
            if self.mikata.catcha(bullet):
                self.energy -= 1
        
        for dangan in self.dangan:
            dangan.move()
            if self.tekia.catchb(dangan):
                pyxel.play(0, 1)
                dangan.s *= -1.3
            if self.tekib.catchb(dangan):
                pyxel.play(0, 1)
                dangan.s *= -1.3
            if dangan.y <= 86 and 60 <= dangan.x <= 140:
                self.score += -1
                pyxel.play(0, 0)
            if self.pads.catchb(dangan):
                self.life -= 1
                pyxel.play(0, 2)
            if self.mikata.catchb(dangan):
                self.energy -= 1
            if self.energy <= 0:
                dangan.muhon()
                if dangan.y >= 200:
                    dangan.x = self.mikata.x
                    dangan.y = self.mikata.y
        if self.life == 0:
                self.gameover = True
                pyxel.play(0, 3)



    def draw(self):
        if self.clear:
            pyxel.text(100, 100, "GAME CLEAR", 4)
            for f in self.fire:
                f.draw()
        elif self.gameover:
            pyxel.text(100, 100, "GAME OVER", 2)
        else:
            pyxel.cls(0)
            pyxel.rect(0, 106, 200, 100, 11)
            pyxel.circ(200, 0, 30, 10)
            pyxel.bltm(37, 2, 0, 0, 0, 128, 128)
            pyxel.text(10, 10, "HP: " + str(self.score), 7)
            pyxel.text(160, 170, "LIFE: " + str(self.life), 0)
            pyxel.text(160, 150, "ENERGY: " + str(self.energy), 0)
            self.mikata.draw()
            self.pads.draw()
            self.tekia.draw()
            self.tekib.draw()
            for b in self.bullet:
                b.draw()
            for b in self.dangan:
                b.draw()
            

class Bullet:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.s = 1.2
    def draw(self):
        pyxel.rect(self.x, self.y-20, 5, 5, 7)

    def move(self):
        self.y -= self.s
        if self.y < 86:
            return False
        else:
            return True


class Pad:

    def __init__(self):
        self.x = 100
        self.y = 100
        self.w = 40
        self.h = 13
        self.c = pyxel.COLOR_PINK
    def draw(self):
        pyxel.rect(self.x-20, self.y-20, self.w, self.h, 14)
    def update(self,b):
        self.x = pyxel.mouse_x
        if pyxel.btnp(pyxel.KEY_SPACE):
            b.append(Bullet(self.x,self.y)) 
    def catcha(self, bullet):
        return self.y + 5 <= bullet.y <= self.y + 8 and self.x - 20 <= bullet.x <= self.x + 20
    def catchb(self, dangan):
        return self.y + 5 <= dangan.y <= self.y + 8 and self.x - 20 <= dangan.x <= self.x + 20

class Dangan:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.s = 1.2
        
    def draw(self):
        pyxel.rect(self.x, self.y-20, 5, 5, 7)

    def move(self):
        self.y -= self.s
        if self.y < 86:
            return False
        else:
            return True
    
    def muhon(self):
        self.y += self.s
        if self.y > 200:
            return False
        else:
            return True



class Mikata:


    def __init__(self):
        self.x = 150
        self.y = 150
        angle = pyxel.rndi(30, 150)
        self.vx = pyxel.cos(angle)
        self.vy = pyxel.sin(angle)
    def move(self):
        self.x -= self.vx 
        self.y -= self.vy 
        if self.x > 180:
            angle = pyxel.rndi(30, 150)
            self.vx = pyxel.cos(angle) * -1
            self.vy = pyxel.sin(angle) 
        if self.x < 20:
            angle = pyxel.rndi(30, 150)
            self.vx = pyxel.cos(angle) * -1
            self.vy = pyxel.sin(angle)
        if self.y < 120:
            angle = pyxel.rndi(30, 150)
            self.vx = pyxel.cos(angle) 
            self.vy = pyxel.sin(angle) * -1
        if self.y > 170:
            angle = pyxel.rndi(30, 150)
            self.vx = pyxel.cos(angle) 
            self.vy = pyxel.sin(angle) * 1

    def draw(self):
        pyxel.rect(self.x-20, self.y-20, 40, 8, 8)

    def update(self,b):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            b.append(Dangan(self.x,self.y)) 

    def catcha(self, bullet):
        return self.y + 7 <= bullet.y <= self.y + 8 and self.x - 20 <= bullet.x <= self.x + 20
    def catchb(self, dangan):
        return self.y + 7 <= dangan.y <= self.y + 8 and self.x - 20 <= dangan.x <= self.x + 20

class Tekia:

    def __init__(self):
        self.x = 0
        self.w = 65
        self.h = 5
        self.speed = pyxel.rndi(10, 40)
    def draw(self):
        pyxel.rect(self.x, 78, self.w, self.h, 12)
    def move(self):
        self.x += self.speed*0.1
        if self.x >= 80:
            self.speed *= -1
        if self.x <= 0:
            self.speed = pyxel.rndi(10, 40)
            self.x += self.speed*0.1
    def catcha(self, bullet):
        return 95 <= bullet.y <= 100 and self.x <= bullet.x <= self.x + 65
    def catchb(self, dangan):
        return 95 <= dangan.y <= 100 and self.x <= dangan.x <= self.x + 65

class Tekib:

    def __init__(self):
        self.x = 135
        self.w = 65
        self.h = 5
        self.speed = pyxel.rndi(10, 40)
    def draw(self):
        pyxel.rect(self.x, 78, self.w, self.h, 12)
    def move(self):
        self.x -= self.speed*0.1
        if self.x <= 80:
            self.speed *= -1
        if self.x >= 135:
            self.speed = pyxel.rndi(10, 40)
            self.x -= self.speed*0.1
    def catcha(self, bullet):
        return 95 <= bullet.y <= 100 and self.x <= bullet.x <= self.x + 65
    def catchb(self, dangan):
        return 95 <= dangan.y <= 100 and self.x <= dangan.x <= self.x + 65
    
class Fire:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.start = pyxel.frame_count
        self.dot = [(x,y)]
        self.r = 5
        self.s = 0
        self.alive = True
    
    def update(self):
        if pyxel.frame_count > self.start + 30*(self.s + 1):
            for angle in range(0,360,45):
                self.dot.append( (self.x+ math.cos(math.radians(angle))*self.r, self.y+math.sin(math.radians(angle))*self.r) )
            self.s += 1
            self.r += 5
        if self.s > 5:
            self.alive = False

    def draw(self):
        for d in self.dot:
            pyxel.pset(d[0], d[1], pyxel.COLOR_ORANGE)



App()