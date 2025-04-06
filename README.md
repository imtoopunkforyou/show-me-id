# SMID 👮
A simple [Telegram](https://telegram.org/) bot that provides a brief summary of the user.
You can find out information about yourself or forward a message from another user or channel.  
Available at the link: [@show_me_id_bot](https://t.me/show_me_id_bot)

## Self hosted
You can deploy the bot on your server.
To do this, you first need to [register the bot and get its token](https://core.telegram.org/bots/tutorial#obtain-your-bot-token).  

You will also need to install [Docker](https://docs.docker.com/get-started/).  
Once you install Docker, you need to run three commands and your bot will be available.
```bash
git clone --depth 1 --branch 0.1.3 https://github.com/imtoopunkforyou/show-me-id.git
```
```bash
echo "BOT_TOKEN=<your_bot_token>" >> ./show-me-id/.env  
```
```bash
docker compose -f ./show-me-id/compose.yml up --build -d
```

## TODO
- [x] Readme.md
- [ ] Tests
