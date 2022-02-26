#!/bin/zsh
docker rm --force banter-bot
docker run --name banter-bot banter-bot-image
