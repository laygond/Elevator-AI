# Elevator-AI
Intelligent Elevator using OpenHAB, OpenCV, and TensorFlow for creating Automation Rules

# Directory Structure
```
.Elevator-AI
├── README.md
├── README_images            # Images used by README.md
│   └── ...
├── firmware                 # Custom ESP8266/32 IoT firmware
│   ├── custom-motion-sensor # detects motion inside elevator
│   └── custom-servo-switch  # turns elevator ON/OFF
├── openhab2                 # soft link to openhab's directory
│   ├── items
│   ├── rules
│   ├── sitemaps
│   ├── things
│   └── ...
├── no_signal.png
└── simple_cam_monitor.py
```
# Web/Mobile App Sitemap
<p align="center"> <img src="README_images/app.png"> </p>
<p align="center"> Fig: Elevator currently ON and set to work automatically. There are currently people inside and switch is currently out of range of elevator cabin. </p>

# Implemented Rules/Features
- Turn elevator ON/OFF manually 
- Schedule to turn elevator ON at 8AM
- Schedule to turn elevator OFF repetively every 10 min for about an hour starting at 8PM until there is no motion inside elevator (there are no people) 
- More later ...

# References
### Hardware


### Load Code to IoT Devices

- [Install Arduino in Linux](https://www.arduino.cc/en/guide/linux)
- [Add ESP8266 to Arduino Board Manager](https://randomnerdtutorials.com/how-to-install-esp8266-board-arduino-ide/)
- [Discussion of QIO DIO QOUT DOUT flash modes](https://www.esp32.com/viewtopic.php?t=1250)
- [Flash Firmware to Tuya Devices Over the Air](https://www.youtube.com/watch?v=O5GYh470m5k&ab_channel=digiblurDIY)
- [Figuring out generic tuya devices control pins](https://www.youtube.com/watch?v=m_O24tTzv8g&ab_channel=digiblurDIY)
