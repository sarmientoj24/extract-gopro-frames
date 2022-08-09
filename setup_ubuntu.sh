#!/bin/sh

# Install Go and ffmpeg, uncomment if already done
sudo snap install go --classic
go -version
sudo snap install ffmpeg
ffmpeg -version

curr=$PWD

# Go to GoLang director
cd $1
mkdir -p src/github.com/JuanIrache
cd src/github.com/JuanIrache

wget https://github.com/JuanIrache/gopro-utils/archive/refs/heads/master.zip
unzip master.zip -d .
mv gopro-utils-master gopro-utils
rm master.zip

# Go to gpmd2csv and build artifact
cd gopro-utils/bin/gpmd2csv
go env -w GO111MODULE=off
go build

# Go back to parent dir
cd ${curr}