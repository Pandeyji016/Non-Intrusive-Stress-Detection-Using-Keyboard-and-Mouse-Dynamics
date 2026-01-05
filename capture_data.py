from pynput import keyboard, mouse
import time
import csv
import math

key_times = []
mouse_positions = []
mouse_clicks = 0
last_key_time = None

def on_press(key):
    global last_key_time
    now = time.time()
    if last_key_time:
        key_times.append(now - last_key_time)
    last_key_time = now

def on_move(x, y):
    mouse_positions.append((x, y, time.time()))

def on_click(x, y, button, pressed):
    global mouse_clicks
    if pressed:
        mouse_clicks += 1

print("Recording for 30 seconds...")
kb = keyboard.Listener(on_press=on_press)
ms = mouse.Listener(on_move=on_move, on_click=on_click)

kb.start()
ms.start()
time.sleep(30)
kb.stop()
ms.stop()

typing_speed = len(key_times) / 30
avg_key_delay = sum(key_times)/len(key_times) if key_times else 0

mouse_speed = 0
for i in range(1, len(mouse_positions)):
    x1,y1,_ = mouse_positions[i-1]
    x2,y2,_ = mouse_positions[i]
    mouse_speed += math.sqrt((x2-x1)**2 + (y2-y1)**2)

mouse_speed /= 30 if mouse_positions else 1
mouse_jitter = len(mouse_positions)/30
click_rate = mouse_clicks/30
idle_time = 0

stress = int(input("Enter stress (0=Low, 1=Medium, 2=High): "))

with open("data/stress_data.csv","a",newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        round(typing_speed,2),
        round(avg_key_delay,2),
        round(mouse_speed,2),
        round(mouse_jitter,2),
        round(click_rate,2),
        round(idle_time,2),
        stress
    ])

print("Data saved!")
