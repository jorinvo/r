#!/bin/sh
set -e # Exit script on errors

#
# Update ownCloud on Uberspace
#


# WARNING: Please don't use this script as is!
#
# Adjust it to your personal setup.
#
# The script assumes that the data folder
# of your owncloud is not in the application folder.
# You need to install all plugins manually again after updating.
#
# Make sure the script is executable with: chmod +x update-owncloud.sh


OWNCLOUD_VERSION="$1"
TAR_FILE="owncloud-${OWNCLOUD_VERSION}.tar.bz2"
DOWNLOAD_URL="https://download.owncloud.org/community/$TAR_FILE"
URL="your-domain.com" # THIS IS SPECIFIC TO EVERY SETUP
CLOUD="/var/www/virtual/$USER/$URL"
WWW_CLOUD="/var/www/virtual/$USER/www.$URL"

echo checking version
test -z "$OWNCLOUD_VERSION" && echo "No version specified. Try: ./update-owncloud.sh 8.2.2" && exit 1

cd $HOME/tmp

echo downloading
wget $DOWNLOAD_URL

echo extracting
tar -xjvf $TAR_FILE
rm $TAR_FILE

echo copying config
cp $CLOUD/config/config.php owncloud/config/config.php

echo copying new owncloud files
rm -rf $CLOUD/*
cp -r owncloud/* owncloud/.htaccess $CLOUD

echo creating link for www.
rm $WWW_CLOUD
ln -s $CLOUD $WWW_CLOUD

echo cleaning up tmp folder
rm -rf owncloud