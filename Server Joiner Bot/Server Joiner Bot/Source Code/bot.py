import os
import signal
import sys
import time
import discord
import discum
import config


bot = discum.Client(token=sys.argv[1], log={"console": False, "file": False})
users = {}
total_users = []
total_dmed = 0


@bot.gateway.command
def on_event(resp):
    try:
        if resp.event.ready_supplemental:
            user = bot.gateway.session.user
            for server in config.target_servers_invites:
                try:
                    bot.joinGuild(server.split('/')[-1])
                    print(f"{user['username']}#{user['discriminator']}: Joined '{server}'")
                except Exception as e:
                    print(f"{user['username']}#{user['discriminator']}: Could not join '{server}'")
                time.sleep(config.delay_between_token_joins)
    except Exception as e:
        pass


# Start Server Joiner Bot
try:
    bot.gateway.run()
except Exception as e:
    os.kill(os.getppid(), signal.SIGINT)
