# Disco Toilet
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Raspberry Pi](https://img.shields.io/badge/raspberrypi-A22846?style=for-the-badge&logo=raspberrypi&logoColor=white)
![Zigbee](https://img.shields.io/badge/Zigbee-3.0-blue?logo=zigbee)

## Background
The concept is simple: A customer at a bar/restaurant could push a button in the bathroom, and suddenly loud music starts playing, lights start flashing, and disco balls start spinning, creating a immersive, fun, and "instagrammable" toilet experience.

I figured that I could make a simple, cheap to implement, stripped-back, yet highly customisable experience myself in my family's own restaurant. So far, it has been highly popular with customers, and adds a bit of fun to their dining (and toileting) experience.

## Demonstration
Find a YouTube short demonstration [here](https://youtube.com/shorts/kEkEy_Jyqew?feature=share)

## Features
- Trigger a disco sequence at the push of a physical button
- Control multiple smart lights and devices through Zigbee protocol
- Play a random music clip from a folder
- Restore bathroom's default lighting when the sequence finishes
- Cancel sequence with another button press

## How It Works
1. Physical button sends keypress to Python program
2. Program initiates the disco behaviour (Lights dim, begin flashing, etc)
3. Zigbee2MQTT communicates with the Zigbee devices through the Zigbee coordinator and publishes the desired state for each device
4. The connected speaker plays a 30 second snippet of a popular disco song (or any genre). (I just had a folder which stores these snippets as mp3 files, and a random song is played each time)
5. Once the music has finished playing, the disco light is switched off, and the bathroom lights revert back to their default state
6. The button can be pushed again during the disco mode to immediately change the bathroom back to normal, and stop the music playback
7. Hold the button for 5 seconds and it triggers the Pi to shutdown (ensure program has suitable permissions to run this command)

## Required Hardware
- Raspberry Pi
- Speakers
- Zigbee-enabled smart devices (light bulbs, LED strips, ...etc)
- A Disco light/ball + a zigbee-enabled smart plug to connect to it (unless you can find a zigbee-powered disco light of course!)
- Button
  - This could connect directly to the Pi's GPIO pins, or in my case I found a button on [AliExpress](https://www.aliexpress.com/item/1005007358494108.html?aff_fsk=_c4tsNQsv&src=motore&aff_platform=aff_feeds&aff_short_key=_c4tsNQsv&gad_source=1&gad_campaignid=24342048143&gbraid=0AAAAADprV04PDelCsFuK2lfdFhuDJbt0w&cv=a988389207ea41a2b79d593deb9afe05&gclid=CjwKCAjwl4HXBhAjEiwAHlpWhGxQkTKIbsDnDx3CvDbu1yZjo8DZfFMKJNiPqBrATYlV2JLFvEIp8xoCvzEQAvD_BwE) which sends a customisable key event to the Pi via USB

## Implementation
### Flow Diagram
<img width="4127" height="5300" alt="Blank diagram - Page 1" src="https://github.com/user-attachments/assets/59b93b21-c2b0-4c57-a096-47884bc0dbbd" />

### Future Improvements
- Improve reliability and error handling
- Make it so that the same song doesn't appear multiple times in a row (song selected at random from folder)

## Setup
1. Clone the repository
2. Install the required Python dependencies (PyGame), Zigbee2MQTT, and Mosquitto broker
3. Connect and pair your zigbee devices from the Zigbee2MQTT homepage, here on the exposes tab you can see the available functions and publish topics for your specific hardware
4. Run the application on the Raspberry Pi

## Additional Notes And Issues I Had
- Do not cheap out on smart bulbs! A cheap one from AliExpress will **not** do a sufficient job, has very limited "lighting modes" and effects, and can become unresponsive easily. I would recommend Phillips Hue GU10 bulbs that fit perfectly in a ceiling spotlight and are very discrete. You should also always use same brand/model where possible to avoid out of sync issues.
- Speakers must be auto-on or always on so that they are always ready to start playing music on request. I ended up using [these](https://uk.creative.com/p/speakers/creative-pebble-plus) which were surprisingly good for the price point and room size, but if I had the budget would opt for sleeker in-ceiling speakers.
- For the trigger button I used a USB-connected one that can send any customisable key event (I used ENTER). Alternatively, you could utilise the GPIO pins on the Raspberry Pi, or even have a Zigbee wireless smart button.
