#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cp -R $DIR ~/.genmake
if [ -f ~/.zshrc ]
then
	if grep -q "alias genmake" ~/.zshrc
	then
		echo "Already install on zshrc"
	else
		echo "Install on zsh.."
		echo "alias genmake='~/.genmake/genmake.py'" >> ~/.zshrc
	fi
fi
if [ -f ~/.bashrc ]
then
        if grep -q "alias genmake" ~/.bashrc
        then
                echo "Already install on bashrc"
        else
                echo "Install on zsh.."
                echo "alias genmake='~/.genmake/genmake.py'" >> ~/.bashrc
        fi
fi
