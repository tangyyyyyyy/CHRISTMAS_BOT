import discord

from constants.globals import ChristmasColor


#creature_name, creature_pronoun, item_pronoun, item_name, item_rarity, creature_name
NAUGHTY_CORRECT = ('Somberly, you were correct... {creature_name} hangs their head in shame... '
       'Hoping to change fate, '
        '{creature_pronoun} bribes you with '
        '{item_pronoun} {item_name}. Only a {item_rarity} item? '
        '"Silly {creature_name}, that won\'t get you on the nice list", you think, as you '
        'chuckle and add it to your inventory.')

#creature_name, caps_creature_pronoun, creature_pronoun, item_pronoun, item_name, item_rarity
NICE_CORRECT = ('Excellent guess! You were correct, it was a nice {creature_name}! {caps_creature_pronoun} beams with pride. '
    'As thanks'
        ' for your good news, {creature_pronoun} gives you '
        '{item_pronoun} {item_name}. Wow! A {item_rarity} item! '
        'You check the "extra nice" box on your list and add the item to your inventory.')

#creature_name, caps_creature_pronoun, creature_pronoun, replaced_item
NAUGHTY_INCORRECT = ('Regretfully, you are wrong... It was a nice {creature_name}! {caps_creature_pronoun} can\'t'
      ' let you down, so {creature_pronoun} chose to act the part. '
      '{caps_creature_pronoun} replaces '
      'your {replaced_item} with coal! The guilt is immense, but it\'s better than letting you '
      'be wrong... ')

#creature_name, caps_creature_pronoun, creature_pronoun, replaced_item
NICE_INCORRECT = ('Wrong, as usual... It was a naughty {creature_name}. Oh no! {caps_creature_pronoun} '
      'thinks your mistake was an act of deception! In spite, {creature_pronoun} replaces '
      'your {replaced_item} with coal! Serves you right. ')

HELP_MESSAGE = discord.Embed(
  title='Christmas Command List',
  description=('After watching the Halloween creatures from afar, the '
                'Christmas creatures have decided to visit and leave presents '
                'behind! Identify whether the creatures are nice or naughty '
                'with the right command when they come and collect items to '
                'become your server\'s Chamption of Christmas!'),
  color=discord.Colour(ChristmasColor.GOLD)
).set_author(
  name='Christmas Bot',
  icon_url='https://i.imgur.com/YZ6v1jw.png',
  url='https://github.com/tangyyyyyyy/CHRISTMAS_BOT'
).set_thumbnail(
  url='https://i.imgur.com/YZ6v1jw.png'
).add_field(
  name='Game',
  value=('`x!nice` \n'
          '`x!naughty`'),
  inline=False
).add_field(
  name='User Commands',
  value=('`x!inventory <user>` - If `<user>` is not provided, defaults to self\n'
          '`x!leaderboard` \n'
          '`x!tree` - Shows a Christmas tree containing all presents!\n'),
  inline=False
).add_field(
  name='Configuration',
  value=('`x!enable` - Enable creature spawns in this channel\n'
          '`x!disable` - Disable creature spawns in this channel\n'
          '`x!setchance <percentage>` - Set creature spawn chance of creatures in % \n'
          '`x!time <seconds>` - Set despawn time of creatures in seconds \n'
          '`x!role` - Refresh the "Champion of Christmas" role'),
  inline=False
)

BAD_COMMAND_MESSAGE = ('Oh no, the elves didn\'t understand your command! '
      'Please check x!help to see what they can do!')

CREATURE_SPAWN_TITLE = ('Someone was impressed by your Christmas spirit and ' 
                        ' has decided to drop by!')

CREATURE_SPAWN_DESCRIPTION = ('Let them in with {creature_command}!')
