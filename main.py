#!/usr/bin/env python3

import os, random, pygame, json, time
import sys, subprocess
import paho.mqtt.client as mqtt


SONG_BANK = "./SoundBank/crop/normalised"
COOLDOWN = 4000
BRIGHT = 100

DIM = 20  

#MQTT INIT
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

#DEVICES
LIGHT1 = "bulb1"
LIGHT2 = "bulb2" 
PLUG = "disco-plug"

MQTT_BROKER = "localhost"  
MQTT_PORT = 1883           


global mode 
mode = "standby"

SONG_END_EVENT = pygame.USEREVENT + 1

#MQTT HELPERS
def lights_scene_on():
    client.publish(f"zigbee2mqtt/{LIGHT1}/set",
                   json.dumps({"state": "OFF"}))
    client.publish(f"zigbee2mqtt/{LIGHT2}/set",
                       json.dumps({"state": "OFF"}))
    

def lights_scene_off():
    client.publish(f"zigbee2mqtt/{LIGHT1}/set",
                       json.dumps({"state": "ON"}))
    client.publish(f"zigbee2mqtt/{LIGHT2}/set", json.dumps({"state": "ON"}))

def plug_on():
    client.publish(f"zigbee2mqtt/{PLUG}/set",
                   json.dumps({"state": "ON"}))

def plug_off():
    client.publish(f"zigbee2mqtt/{PLUG}/set",
                   json.dumps({"state": "OFF"}))

def play_disco():
    global song_length_sec
    plug_on()

    song = random.choice(os.listdir(SONG_BANK))
    song_path = os.path.join(SONG_BANK, song)
    pygame.mixer.music.load(song_path)

    sound = pygame.mixer.Sound(song_path)
    song_length_sec = sound.get_length()

    pygame.mixer.music.play(fade_ms=3000)
    lights_scene_on()
    print("playing song: ", song)

def stop_disco():
    lights_scene_off()
    plug_off()

    pygame.mixer.music.fadeout(3000)


def toggle_disco(last_press):
    global mode, fading
    current_time = pygame.time.get_ticks()

    if current_time - last_press < COOLDOWN:
        print("Button is on cooldown. Please wait.")
        return last_press
    
    last_press = current_time

    if mode == "standby":
        mode = "disco"
        fading = False

        client.publish(f"zigbee2mqtt/main-light/set",
            json.dumps({"state": "ON"}))
        
        play_disco()
    elif mode == "disco":

        client.publish(f"zigbee2mqtt/main-light/set",
                                   json.dumps({"state": "OFF"}))
        stop_disco()
        mode = "standby"


    return last_press

def ding_sound():
     for i in range(3):
        pygame.mixer.music.load("./dingsound.mp3")
        pygame.mixer.music.play()
        pygame.time.delay(500)

def on_switch_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        client.subscribe("zigbee2mqtt/switch")

bulbs = ["bulb1", "bulb2"]

def on_switch_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())
    action = data.get("action")

    if action == "on":
        lights_scene_off()
    elif action == "off":
        lights_scene_on()

    elif action == "brightness_move_up":
        for bulb in bulbs:
            client.publish(f"zigbee2mqtt/{bulb}/set", json.dumps({"brightness_move": 20}))
    elif action == "brightness_move_down":
        for bulb in bulbs:
            client.publish(f"zigbee2mqtt/{bulb}/set", json.dumps({"brightness_move": -20}))
    elif action == "brightness_stop":
        for bulb in bulbs:
            client.publish(f"zigbee2mqtt/{bulb}/set", json.dumps({"brightness_move": 0}))

def main():
    global mode, fading, song_length_sec
    print("Finished")

    #PYGAME INIT
    pygame.init()
    pygame.mixer.pre_init(44100, -16, 2, 8192)
    pygame.display.set_mode((200, 200))
  
    #CLOCK INIT
    clock = pygame.time.Clock()

    #BUTTON STATE
    mode = "standby"
    last_press = 0
    hold_press_start = 0

    song_length_sec = -1

    #MQTT INIT
    client.connect("localhost")
    client.on_connect = on_switch_connect
    client.on_message = on_switch_message
    client.loop_start()

    pygame.mixer.music.set_endevent(SONG_END_EVENT)

    ding_sound()


    running = True
    fading = False

    while running:

        #SHUTDOWN DETECTION
        if hold_press_start > 0:
            duration = pygame.time.get_ticks() - hold_press_start
            if duration >= 5000:
                print("Button held for 5 seconds, initiating shutdown...")

                ding_sound()

                pygame.time.delay(3000)  # Wait for the sound effect to finish

    

                subprocess.run(["sudo", "shutdown", "-h", "now"], check=True)
                sys.exit(0)
                hold_press_start = 0

        if mode == "disco" and song_length_sec > 0 and not fading:
            pos_ms = pygame.mixer.music.get_pos()
            if pos_ms != -1:
                remaining_sec = song_length_sec - pos_ms / 1000.0

                if remaining_sec <= 3.0:
                    print("Song entering last 3 seconds. Starting fadeout...")
                    pygame.mixer.music.fadeout(3000)

                    fading = True

        #KEYDOWN LOOP
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                        if hold_press_start == 0:
                            hold_press_start = pygame.time.get_ticks()

            elif event.type == SONG_END_EVENT:
                toggle_disco(last_press)

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    #calculate time held button
                    duration = pygame.time.get_ticks() - hold_press_start

                    if(50 < duration < 1000):
                        last_press = toggle_disco(last_press)

                    #reset timer so we know button released
        
                    hold_press_start = 0

        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
