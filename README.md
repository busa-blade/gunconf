Gunconf
=======

Gunconf is an utility to configure [Aimtrak guns](https://www.ultimarc.com/aimtrak.html) on linux systems

It is tested on ubuntu desktio and retropie. This is a fork of the original code from https://github.com/gunpadawan/gunconf updated to run with python3. Without the code written by this user, this update would not have been possible. My hats off to the original developer.

Written in python on top of pygame, it **does not require an x server.**

![Configuration Panel](https://cloud.githubusercontent.com/assets/26297080/24149019/6d1c3e8c-0e41-11e7-9c4a-487cccceae75.png)
![Sensor View Panel](https://cloud.githubusercontent.com/assets/26297080/24149020/6d1ca76e-0e41-11e7-99a7-039bf5685bf6.png)


# Install
## Prerequisites

`sudo apt install apt-transport-https python3-dev python3-pygame python3-setuptools python3-evdev python3-usb`

## Get the source
`git clone https://github.com/busa-blade/gunconf`

## Install python module
`cd gunconf`

`sudo python setup.py install`

## Udev rules
Application requires access to the aimtrak usb device. It is usually necessary to configure udev to let your specific user access that device.

To let any user access the device, do:

`sudo cp utils/aimtrak.rules /etc/udev/rules.d/99-aimtrak.rules`

`sudo udevadm control --reload-rules`


## Launch
To launch application, you can execute `utils/gunconf.sh`

For retropie users, you can add the app to the retropie menu by simply copying that file:

`sudo cp utils/gunconf.sh /home/pi/RetroPie/retropiemenu/`


# [Advancemame](http://www.advancemame.it/download)

So far advancemame is the only emulator that has been successfully tested.

download advmame >=3.4 (does not work for sure with prior versions)

## Configuration

edit `~/.advance/advmame.rc`

set the following:

`device_mouse none` to disable the support for mouse **even if the gun is configured to report as a mouse**

`device joystick event` to ask advmame to use linux event interface

Next you need to configure the gun itself, especially the different axes.
For player 1 you need to find the right value for `input_map[p1_lightgunx]` and `input_map[p1_lightguny]`

Assuming you have configured the gun to use device ID 0x1601, the configuration is:

`input_map[p1_lightgunx] joystick[d209_1601_2,0,0]`

`input_map[p1_lightguny] joystick[d209_1601_2,0,1]`

* d209 is the usb vendorId of the gun (fixed value)
* 1601 is the usb productId
* 2 is the usb device interface (fixed value)

Then configure the trigger.

`input_map[p1_button1] joystick_button[d209_1601_2,0]`


for more details you can read the [advmame](http://www.advancemame.it/doc-advmame#8.9.5) doc

## Test

From there you should be able to start the emulator and test.

Assuming you own a rom called duckhunt

make sure you have `~/.advance/rom/duckhunt.zip`

launch `advmame duckhunt`

the crosshair should now move on the screen.

Start calibration with the button you have configured for that purpose in gunconf

In the menu, you can configure a key or button to toggle crosshair display

# [Daphne](http://www.daphne-emu.com)

Since my best shooting games run only on daphne, I have added (initial) aimtrak support to that emulator.
It's not that straightforward for now but if you want to give it a try on retropie:

connect to your pi through ssh:

`cd ~/RetroPie-Setup/scriptmodules/emulators`

`mv daphne.sh daphne.sh.bak`

`wget "https://raw.githubusercontent.com/busa-blade/RetroPie-Setup/master/scriptmodules/emulators/daphne.sh"`

launch Retropie-Setup from the retropie menu and install daphne emulator from source

then you need to add a game in `/home/pi/RetroPie/roms/daphne`. 

To be recognized by emulation station, your game needs to be in a directory ending with ".daphne"

at start, daphne.sh will read the content of a file in that directory named \<game\>.commands.

As an example, let's assume we have a game called Last_Bounty_Hunter:

1/ Add your game files in the `/home/pi/RetroPie/roms/daphne/Last_Bounty_Hunter.daphne` directory 

2/ Edit the file named `/home/pi/RetroPie/roms/daphne/Last_Bounty_Hunter.daphne/Last_Bounty_Hunter.daphne`


and add parameters like this: `singe vldp -framefile ./frame-lbh-cdrom.txt -script ./cdrom-lbh.singe`

refer to daphne doc for further information on parameters


# Known limitations
* does not support firmware update (you need a windows host for that...)


