# MusicalBalls
Final project for MUS277

Set up:
First make sure the external web cam and arduino with ir sensor and FSR sensor are plugged into the computer. Next, run main.py using python3 and make sure the correct web cam is being used to look at the tray of balls. Finally, open the Max patch and activate the arduino serial port within the readArduinoData subpatch. Also, make sure that the toggle at the top of the patch is activated which updates the color of the balls in real time every second. 

![Alt text](images/structure_v1.JPG?raw=true "Structure v1")

The above structure was laser cut out of 1/4 inch hardboard after being CAD in Solidworks. For future iterations, I had hoped to improve the structure and laser cut using 1/4 inch acrylic sheets. 

Using a Logitech C270 Widescreen HD Webcam to look at a tray of balls, the python 3.7 script called main.py sends messages to a Max 8 patch on the order and color of the balls in the tray. Each colored ball represents a unique sound and pressing a FSR sensor determines how long each sound is played. The IR sensor determines volume but if it is not being used, it defaults to the last saved volume. 

Note: To help with the consistency of the lighting I attached a [wireless LED light](https://www.amazon.com/gp/product/B073WK7CFN/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1) next to the camera. The min/max values of the color balls may still need to be adjusted in main.py which is what the hsv_finder.py script is used for. In the future, using less transparent ping pong balls may help with the lighting inconsistencies. 

With the maxpatch v2, the sounds that are being played are part of an original composition that was split up into 8 different sections within the folder called "Sounds". 

Future work:
Add visual indicator (LEDs) to the structure to let the user know which ball is being played. To do this, I will have to figure out how to send and recieve serial data within the same Max patch. 

To make the interaction more interesting, I was considering making this into a drum machine where each ball represents a different drum sound (snare, bass, high-hat, etc..). However, I would need to incorporate some sort of looping mechanism (possibly a mechanical button) that saves the sounds and plays them back because hearing individual drum sounds on their own is not particularly interesting. 

Another alternative I was considering was making each ball represent a simple sine wave with an associated pitch and every time the FSR sensor was pressed, a whole row/column would play. In this manner, the user could create chords of four notes at a time. 