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
    'helge': [True],
    'ilija': [True],
    'jan': [True],
    'jens': [True],
    'jesko': [True],
    'julia': [True],
    'jutta': [True],
    'kevin': [True],
    'kevind': [True],
    'manolo': [True],
    'marcel': [True],
    'marcelk': [True],
    'marian': [True],
    'markus': [True],
    'matthias': [True],
    'michael': [True],
    'rene': [True],
    'ronnie': [True],
    'simon': [True],
    'simone': [True],

    # declined
    'tobias': [False],

    # incomplete
    'jogi': [None],
    'justus': [None],
    'frank': [None],
    'hilde': [None],
    'lennard': [None],
    'lux': [None],
    'marcelr': [None],
    'mario': [None],
    'markuss': [None],
    'paul': [None],
    'ralf': [None],
    'ralfw': [None],
    'sven': [None],
    'tana': [None],
    'uli': [None],

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
