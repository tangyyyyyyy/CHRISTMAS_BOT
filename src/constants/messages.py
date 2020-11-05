NAUGHTY_CORRECT = ('You were correct! {creature_name} hangs their head in shame... As a bribe,'
                    '{creature_pronoun} gives you '
                    '{item_pronoun} {item_name}. This item is {item_rarity}. '
                    'Silly creature, that won\'t help, you think, as you '
                    'avert your eyes and add it to your inventory.')

NICE_CORRECT = ('You were correct! It was a nice {creature_name}! As a thanks'
                    ' for your expertise, {creature_pronoun} gives you '
                    '{item_pronoun} {item_name}. This item is {item_rarity}. '
                    'You add it to your inventory.')

HELP = ('NEED SOME HELP??? HERE ARE OUR COMMANDS:'
        
        'CONFIG/ADMIN:'
        'x!config enable <channels>'
        'Request: parameters = <channels> (array of strings)'
        'Response: string'
        
        'x!config disable <channels>'
        'Request: parameters = <channels> (array of strings)'
        'Response: string'
        
        'x!config role '
        'Request: parameters = <channels> (array of strings)'
        'Response: string'
        'x!time <time>'
        'Request: parameters = <time> in seconds before ornaments despawn (int)'
        'Response: string'

        'x!setchance <probability> '
        'Request: parameters = <probability> in % for bot to appear on a given message (int)'
        'Response: string'

        'USER COMMANDS:'
        'x!leaderboard'
        'Request: no explicit parameters (implicit—> user object)'
        'Response: array of string'
        'x!inventory <user>'
        'Request: parameters = <user>, default to user who typed (string) (implicit —> user object)'
        'Response: array of strings'
        'x!tree'
        'Request: no explicit parameters (implicit —> tree object)'
        'Response: image and string'
        'x!nice or x!naughty'
        'Request: parameters = <user> who wrote command (string)'
        'Response: image and string'
        )
