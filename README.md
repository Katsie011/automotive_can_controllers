# CAN Controllers

This project started when I was getting frustrated with the lack of support availible for many of the devices that I was using
when developing off-highway electric vehicles. 

It was taking hours to get started on something that, in the software world, had taken me a quick install. 
Hence, this repo. 


You will find a rough set of CAN Bus controllers that can be used to interface with the devices listed. 


When developing the testbench, I used a raspberry pi with a [waveshare can hat](https://www.waveshare.com/wiki/RS485_CAN_HAT)


More details to follow as this is built out. 
Hope it helps! 🙏


## Installation

1. setup your python environment. 

2. install the requirements

```bash
    pip install requirements.txt
```

3. Clone the repo

```bash
    gh repo clone Katsie011/automotive_can_controllers
```

4. Run the controller you need!
```bash
python controller_applications/bender_ISO175_j1939.py
```
See the examples at the end of each controller application for help.


## Structure of the repo

The repo was mainly intended to host the different CAN bus controllers. 
Internally, this plugged into the another application that I wrote to act as a ECU to run the various Controller Applications (CAs)


## License

This project is licensed under the [Creative Commons Attribution-NonCommercial 4.0 International License](https://creativecommons.org/licenses/by-nc/4.0/).  
You may use, modify, and share this code for non-commercial purposes with attribution.  
For commercial use, please contact me.

