#Snake clone for Micropython
#Problems with debouncing rotary encoder

from machine import Pin, I2C
import ssd1306
import time
from rotary_quad_encoder import RotaryQuadEncoder
import urandom

snake=[[10,10],[15,10],[20,10],[25,10],[30,10]]
directions=['e','n','w','s']
snake_dir='w'
apple=[urandom.randrange(18,120),urandom.randrange(18,55)]
score=0


# ESP32 Pin assignment 
i2c = I2C(-1, scl=Pin(22), sda=Pin(21))

# ESP8266 Pin assignment
#i2c = I2C(-1, scl=Pin(5), sda=Pin(4))

oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
r = RotaryQuadEncoder(pin1=12, pin2=13, half_steps=False, pins_pull_up=False,
    track_count=True, reverse=False, range_mode=RotaryQuadEncoder.RANGE_BOUNDED, min=0, max=1) 


push_b=Pin(5, Pin.IN)   

def move_snake(snake_dir):
    global snake
    global apple
    global score
    
    if snake_dir=='e':
        head=snake[0][0]-6
        print(head)
        snake.insert(0,[head,snake[0][1]])
        time.sleep_ms(50)
    
            
    elif snake_dir=='w':
        head=snake[0][0]+6
        snake.insert(0,[head,snake[0][1]])
        time.sleep_ms(50)
        
    elif snake_dir=='n':
        head=snake[0][1]-6
        snake.insert(0,[snake[0][0],head])
        time.sleep_ms(50)
  
        
    elif snake_dir=='s':
        head=snake[0][1]+6
        snake.insert(0,[snake[0][0],head])
        time.sleep_ms(50)

    snake.pop()
    
    if (snake[0][0] > 128) or (snake[0][0] < 0) or (snake[0][1] > 64) or (snake[0][1] < 16):
        print('bump!')
        snake[0]=[64,32]
        snake_dir='w'
    
    if (apple[0] < snake[0][0] + 5) and (apple[0] + 3 > snake[0][0]) and (apple[1] < snake[0][1] + 5) and (apple[1] + 3 > snake[0][1]):
        print('yummy!')
        oled.invert(1)
        time.sleep(0.01)
        oled.invert(0)
        time.sleep(0.01)
        score+=1
        
        #extend body after apple
        snake.insert(0, [snake[0][0],snake[0][1]])
        
        #new apple
        apple=[urandom.randrange(18,120),urandom.randrange(18,55)]
    
    print('--------------')
    #print(snake)
    
    oled.fill(0)
    oled.rect(0,16,128,48,1)
    oled.text('Apples %i' % score, 0,0)
    oled.rect(apple[0],apple[1],3,3,1)
    for segment in snake:
        oled.fill_rect(segment[0],segment[1],5,5,1)
    oled.show()

def rotate(pin):
    global r
    global snake_dir
    global directions
    result = r.process()
    if result != None:
        print(result)
        
        idx = directions.index(snake_dir)
        
        if result==0:
            idx+=1
            if idx>3:
                idx=0
            
        elif result==1:
            idx-=1
            if idx<0:
                idx=3
        
        snake_dir=directions[idx]
        print(snake_dir)


r.pin1.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=rotate)
r.pin2.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=rotate)

#push_b.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=push)


oled.fill(0)

while True:
    move_snake(snake_dir)
    time.sleep_ms(200)
        
