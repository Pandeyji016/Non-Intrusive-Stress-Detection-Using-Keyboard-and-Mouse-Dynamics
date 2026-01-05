from pynput import keyboard, mouse
import time, math

def extract_features(duration=30):
    key_times = []
    mouse_positions = []
    mouse_clicks = 0
    last_key_time = None

    def on_press(key):
        nonlocal last_key_time
        now = time.time()
        if last_key_time:
            key_times.append(now - last_key_time)
        last_key_time = now

    def on_move(x, y):
        mouse_positions.append((x, y))

    def on_click(x, y, button, pressed):
        nonlocal mouse_clicks
        if pressed:
            mouse_clicks += 1

    kb = keyboard.Listener(on_press=on_press)
    ms = mouse.Listener(on_move=on_move, on_click=on_click)

    kb.start()
    ms.start()
    time.sleep(duration)
    kb.stop()
    ms.stop()

    typing_speed = len(key_times) / duration
    avg_key_delay = sum(key_times)/len(key_times) if key_times else 0

    mouse_speed = 0
    for i in range(1, len(mouse_positions)):
        x1,y1 = mouse_positions[i-1]
        x2,y2 = mouse_positions[i]
        mouse_speed += math.sqrt((x2-x1)**2 + (y2-y1)**2)
    mouse_speed /= duration if mouse_positions else 1

    mouse_jitter = len(mouse_positions) / duration
    click_rate = mouse_clicks / duration
    idle_time = 0

    return [
        typing_speed,
        avg_key_delay,
        mouse_speed,
        mouse_jitter,
        click_rate,
        idle_time
    ]
