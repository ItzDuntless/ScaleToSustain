from ursina import *
import random

app = Ursina()

home = True

Sky()

camera.position = (900,900,900)

player = Entity(model="cube", color = color.blue, texture = "white_cube", collider = "box")
player.position = (0,2,0)

lava = Entity(model="cube", color = color.yellow, texture = "white_cube", collider = "box")
lava.position = (250,-52,0)
lava.scale = (600,100,0)

home_text = Text(text="Scale to Sustain", color = color.red, origin = (0,0), scale = 2, position = (0,0.4))

home_text2 = Text(text="Climb Up to Save Yourself from the Lava", color = color.black, origin = (0,0), scale = 1.5, position = (0,0.3))

controls_text = Text(text="Controls: Movement- W,A,S,D ; Jump- Space", color = color.black, origin = (0,0), scale = 1, position = (0,-0.4))

play_button = Button(text="Play", text_color = color.black, color = color.lime, scale = (0.3,0.2),position = (0,-0.2), scale_text = 2)
play_button.text_entity.scale = (0.4,0.4)

audio = Audio(sound_file_name="bgmusic.wav",autoplay=True, loop = True)
jump_sfx = Audio(sound_file_name="jump_sfx.mp3", autoplay=False, loop = False)

score = 0

board = Text(text=f"Score:{score}", color = color.black, position = (0,0.1), scale = 2,origin = (0,0,0))
board.position = (900,900)

ypos = -20
xpos = random.randint(-10,10)

dy = 0
gravity = 0.0005

speed_lava = 0

class Platform(Entity):
	def __init__(self, x, y, z):
		super().__init__(
			parent=scene,
			model="cube",
			position=(x,y,z),
			scale=(2,1,1),
			collider="box",
            color = color.red,
            texture = "white_cube"
			)

num=100
platforms=[None]*num
xpos=-5
ypos = -2

def home_exit():
    global home
    home = False
    camera.position = (0,0,0)
    home_text.position = (900,900)
    home_text2.position = (900,900)
    play_button.position = (-900,-900)
    board.position = (0,0.2)
    controls_text.position = (900,900)
    form_platforms()

play_button.on_click = home_exit

def form_platforms():
    global xpos,num,ypos
    for i in range(num):
        xpos += 5
        ypos+=random.randint(1,4)
        platforms[i]=Platform(xpos,ypos,0)

def update():
    global dy,gravity,speed_lava,ypos,score
    if home== False:
        score += 0.1
        board.text = f'Score:{int(score)}'
        for platform in platforms:
            hit_info_1 = player.intersects(platform)
            if hit_info_1.hit and held_keys['space'] and player.y > platform.y:
                jump_sfx.play()
                dy += 1
            elif hit_info_1.hit and player.y > platform:
                dy = 0
                player.y = platform.y+1
            else:
                dy -= gravity
        player.y+=dy
        if held_keys['a']:
            player.x -= 0.08
        if held_keys['d']:
            player.x += 0.08
        lava_hit = player.intersects(lava)
        if lava_hit.hit:
            time.sleep(3)
            score = 0
            board.text = f'Score:{int(score)}'
            player.position = (0,2,0)
            lava.position = (250,-52,0)
            speed_lava = 0
            ypos = -2
            for platform in platforms:
                ypos+=random.randint(1,4)
                platform.y = ypos
        camera.position = (player.x,player.y,-40)
        lava.y += speed_lava
        speed_lava += 0.00003
    

app.run()