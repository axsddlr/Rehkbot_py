#!/usr/bin/env bash

###############################################################
###  Rehkbot Install Script
###
### Copyright (C) 2020 Andre Saddler
###
### By: Andre Saddler (Rehkloos)
### Email: contact@rehkloos.com
### Webpage: https://rehkloos.com
###
### Licensed under the Apache License, Version 2.0 (the "License");
### you may not use this file except in compliance with the License.
### You may obtain a copy of the License at
###
###    http://www.apache.org/licenses/LICENSE-2.0
###
### Unless required by applicable law or agreed to in writing, software
### distributed under the License is distributed on an "AS IS" BASIS,
### WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
### See the License for the specific language governing permissions and
### limitations under the License.
################################################################

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

color(){
  RED=`tput setaf 1`
  GRN=`tput setaf 2`
  YLLW=`tput setaf 3`
  NC=`tput sgr0` # No Color
}

unameOut="$(uname -s)"

# Help menu
help(){
  echo "-h | --help                   : this screen"
  echo "-i | --install                : install"
  echo "-d | --download               : download latest TrovoBot build"
  echo "-m | --mac                    : macOS install"
  echo "no args                       : start installer w/ menu"
}

# Check OS
function checkos(){
if [[ "$(uname)" == "$1" ]]; then
    echo true
  else
    echo false
  fi
}

# IS_MAC=$(checkos "Darwin")
IS_LINUX=$(checkos "Linux")

# Full environment install
install(){

tput reset

color

tput cup 3 19
tput setaf 3
echo "Enter System Password Below to Continue"
tput sgr0

sudo -v; sudo apt-get update

 REQPKGS=("ffmpeg" "python3-psutil" "python3-dbus")

for pkg in "${REQPKGS[@]}"; do
    if [[ $(dpkg-query -f'${Status}' --show $pkg 2>/dev/null) = *\ installed ]];
then
   echo "${GRN} $pkg already installed.  Skipping. ${NC}"
else
   echo "${RED} $pkg was not found, installing... ${NC}" 2>&1
   sudo -v; sudo apt-get --allow -y install $pkg 2>/dev/null
fi
done

if [[ -d "$DIR/rehkbot_py" ]];
then
# cd $DIR/rehkbot_py
echo "${YLLW} Installing dependencies ${NC}"
yarn install > /dev/null 2>&1 &
while kill -0 $! 2> /dev/null; do
    echo -n '.'
    sleep 1
done
elif [[ ! -d "$DIR"  ]]; then
  echo "${RED} 'rehkbot_py' directory does not exist ${NC}"
  exit 0
fi
}


checkos
if [[ "$IS_LINUX" = true ]]; then
# non-gui arguments
while (( "$#" )); do
  case $1 in
    -h|--help) help
               exit 0;;
    -i|--install) install
                  exit 0;;
  esac
  shift
done

elif [[ "$IS_LINUX" = false ]]; then
  echo "Unsupported OS"
  exit 1
fi
