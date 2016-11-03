# Imagemap

`imagemap` is a tool to generate a big grid image from a folder of images.

This can be all done without using the command line.
`imagemap` relies on conventions for this.
It's shipped with an empty `images` folder.
All images should be put in there. Nothing else.
By double-clicking the app an image will be generated.
Tile and grid sizes are hard coded. All images will be cut appropriately.
Mac OS and Linux version of this tool can be build. There are no external dependencies.

This project was done as a quick solution to be usable without needing to open a terminal. It can be given to anyone and should just work with one click.

## Build

Run `./build.sh darwin` or `./build.sh linux` to get a ZIP file ready to ship.

For building and development a UNIX system and [Go](https://golang.org/) are required.