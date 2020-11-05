# CHRISTMAS_BOT

It’s a frosty winter night. As you warm up by the fire, you hear a faint jingle in the distance. You look out your window and see a strange silhouette over the moon. Is that… Santa Claus? But it’s not Christmas yet! Apparently, Santa is taking a vacation this year, and he needs your help to determine who’s naughty and who’s nice!

## Setting Up

- Make sure your Python version is 3.8 or higher.
- If you don't have Poetry already install Poetry
- Run `poetry install`
- Run `poetry run python src/main.py` (if this doesn't work try replacing 
  `python` with `python3`)
  
## Packages
###### api
- API response handlers
- admin contains admin commands
- user contains user commands
- spawn contains spawn logic and nice/naughty commands

###### constants
- config.py: bot constants + master command list from APIs
- messages.py: naughty/nice format strings, along with error messages if needed

###### helpers
-  response_formatter.py: contains text-formatting functions for response

###### classes.py
- contains custom classes and class methods (Item, helper, Creature, leaderboard)
- Will be replaced with DTOs once we figure out how to handle state
