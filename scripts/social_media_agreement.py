from scripts.update_friend_fields import update_friend_fields

fields = ['social_media_agreement']
friends = {

    # accepted
    'alex': [True],
    'angela': [True],
    'armin': [True],
    'basti': [True],
    'bjoern': [True],
    'chris': [True],
    'david': [True],
    'davidb': [True],
    'fede': [True],
    'frank': [True],
    'helge': [],
    'hilde': [True],
    'ilija': [True],
    'jan': [True],
    'jens': [True],
    'jesko': [True],
    'julia': [True],
    'jutta': [True],
    'justus': [True],
    'kevin': [True],
    'kevind': [True],
    'lennard': [True],
    'manolo': [True],
    'marcel': [],
    'marcelk': [True],
    'marian': [True],
    'mario': [True],
    'markus': [True],
    'markuss': [True],
    'matthias': [True],
    'michael': [True],
    'ralfw': [True],
    'rene': [True],
    'ronnie': [True],
    'simon': [True],
    'simone': [True],
    'tana': [True],

    # declined
    'tobias': [False],
    'uli': [False],

    # incomplete
    'jogi': [None],
    'lux': [None],
    'marcelr': [None],
    'paul': [None],
    'ralf': [None],
    'sven': [None],

    # supporting
    'antonia': [None],
    'babara': [None],
    'bettina': [None],
    'conni': [None],
    'dorina': [None],
    'julia-sophie': [None],
    'louis': [None],
    'nikola': [None],
    'oma': [None],
    'stefanie': [None],
    'stephan': [None],
    'uwe': [None],
    'wolfgang': [None],
    'zinnia': [None],
}

update_friend_fields(fields, friends)
