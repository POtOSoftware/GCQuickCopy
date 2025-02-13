# GCQuickCopy

This is a lil' automation script I made to quickly copy my GameCube ISOs to a flash drive with a single drag 'n drop :3

I uploaded it here 'cause I figured someone would find it useful

## Usage

Just drag the ISO you wish to copy over the .exe (grab it from Releases), then input the drive letter you wish to copy to!

It's meant to be used on a flash drive with the standard 'ol `X:/games/Game Title/game.iso` file path format

Drag both disc 1 and disc 2 files into the .exe at the same time to copy both discs!

(though in case things go haywire, just drag disc 2 by itself and say Yes at the disc 2 prompt for a sweet lil override)

## Building

First things first, install readline with `pip install pyreadline3`. This is a required module used for modifying the destination folder name.

Second things second, install pyinstaller with `pip install pyinstaller` (if you already have it installed, make sure you are using the latest version).

Third things third, run build.bat