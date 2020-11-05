NAUGHTY_CORRECT = ('You were correct! {creature_name} hangs their head in shame... '
                   'Hoping to change fate,'
                    '{creature_pronoun} bribes you with '
                    '{item_pronoun} {item_name}. Only a {item_rarity} item? '
                    '"Silly {creature_name}, that won\'t get you on the nice list", you think, as you '
                    'chuckle and add it to your inventory.')

NICE_CORRECT = ('You were correct! It was a nice {creature_name}! {caps_creature_pronoun} beams with pride. '
                'As a thanks'
                    ' for your good news, {creature_pronoun} gives you '
                    '{item_pronoun} {item_name}. Wow! A {item_rarity} item! '
                    'You check the "extra nice" box on your list and add the item to your inventory.')

NAUGHTY_INCORRECT = ('You were wrong! It was a nice {creature_name}! {caps_creature_pronoun} can\'t'
                  'let you down, so they chose to act the part.'
                  '{creature_pronoun) replaces'
                  'your {replaced_item} with coal! The guilt is immense, but it\'s better than letting you'
                  'be wrong ')

NICE_INCORRECT = ('You were wrong! It was a naughty {creature_name}, and {creature_pronoun}'
                  'thinks you were trying to deceive them! In spite, {creature_pronoun) replaces'
                  'your {replaced_item} with coal! Serves you right. ')

HELP = ('NEED SOME HELP??? HERE ARE OUR COMMANDS:'
        
        'CONFIG/ADMIN:\n\n'
        'x!config enable <channels>\n'
        'Request: parameters = <channels> (array of strings)\n'
        'Response: string\n\n'
        
        'x!config disable <channels>\n'
        'Request: parameters = <channels> (array of strings)\n'
        'Response: string\n\n'
        
        'x!config role '
        '\nRequest: parameters = <channels> (array of strings)'
        '\nResponse: string'
        '\n\nx!time <time>'
        '\nRequest: parameters = <time> in seconds before ornaments despawn (int)'
        '\nResponse: string'

        '\nx!setchance <probability> '
        '\nRequest: parameters = <probability> in % for bot to appear on a given message (int)'
        '\nResponse: string'

        '\n\nUSER COMMANDS:'
        '\n\nx!leaderboard'
        '\nRequest: no explicit parameters (implicit—> user object)'
        '\nResponse: array of string'
        '\n\nx!inventory <user>'
        '\nRequest: parameters = <user>, default to user who typed (string) (implicit —> user object)'
        '\nResponse: array of strings'
        '\n\nx!tree'
        '\nRequest: no explicit parameters (implicit —> tree object)'
        '\nResponse: image and string'
        '\n\nx!nice or x!naughty'
        '\nRequest: parameters = <user> who wrote command (string)'
        '\nResponse: image and string'
        )
