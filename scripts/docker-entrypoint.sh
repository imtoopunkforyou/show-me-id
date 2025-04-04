#!/bin/bash
echo '============================'
echo 'Launching the bot...'
echo '============================'
date
echo '============================'
uv sync && uv run $PROJECT_PATH/smid/__main__.py