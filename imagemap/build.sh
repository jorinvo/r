#!/usr/bin/env sh
set -e


export GOOS=$1
export GOARCH=amd64

if [ ! $GOOS ]
then
  echo "Usage: ./build.sh darwin|linux"
  exit
fi

if [ "$GOOS" = "darwin" ]
then
  BIN_DIR="imagemap/imagemap.app/Contents/MacOS"
else
  BIN_DIR="imagemap"
fi

echo "Create directory structure"
mkdir -p $BIN_DIR imagemap/images

if [ "$GOOS" = "darwin" ]
then
  echo "Add app icon"
  cp $GOPATH/src/github.com/jorinvo/imagemap/Icon imagemap/imagemap.app
fi

echo "Create binary:"
go build -v -ldflags="-s -w" -o $BIN_DIR/imagemap github.com/jorinvo/imagemap
echo "Package binary:"
upx --brute -q $BIN_DIR/imagemap

echo "Move files into zip:"
rm -f imagemap.zip
zip -rm imagemap.zip imagemap

