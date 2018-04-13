#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cp -R $DIR ~/.genmake
if [ -f ~/.zshrc ]
then
	if grep -q "alias genmake" ~/.zshrc
	then
		echo "GenMake already install on zshrc"
	else
		echo "Install on zsh.."
		echo "alias genmake='~/.genmake/genmake.py'" >> ~/.zshrc
	fi
	if grep -q "alias 42init" ~/.zshrc
	then
		echo "42init already install on zshrc"
	else
		echo "Install on zsh.."
		echo "alias 42init='~/.genmake/init.py'" >> ~/.zshrc
	fi
fi
if [ -f ~/.bashrc ]
then
        if grep -q "alias genmake" ~/.bashrc
        then
                echo "Already install on bashrc"
        else
                echo "Install genmake on bashrc.."
                echo "alias genmake='~/.genmake/genmake.py'" >> ~/.bashrc
        fi
        if grep -q "alias 42init" ~/.bashrc
        then
                echo "42init Already install on bashrc"
        else
                echo "Install 42init on bashrc.."
                echo "alias 42init='~/.genmake/init.py'" >> ~/.bashrc
        fi
fi
