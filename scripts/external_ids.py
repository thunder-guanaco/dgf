from scripts.update_friend_fields import update_friend_fields

fields = ['pdga_number', 'gt_number', 'udisc_username', 'metrix_user_id']
friends = {
    'alex': [126231, 1436, 'alexso', '62515'],
    'angela': [147164, 2129, 'aceangie', '55028'],
    'armin': [147160, 2127, 'putterbomb', '54515'],
    'chris': [194664, 2824, 'chaberno', '112752'],
    'david': [82985, 1711, 'davido', '20851'],
    'fede': [109371, 2106, 'fedejsoren', '39904'],
    'finja': [240384, 2645, 'finjafeldhof', '118472'],
    'frank': [89408, 1704, 'mischke', '25503'],
    'hilde': [56334, 663, 'chrishilde', '25850'],
    'ilija': [104565, 2040, 'ilimiha', '26762'],
    'jan': [239761, 3531, 'disccube', '84435'],
    'jan-daniel': [81405, 1796, 'acker09', '23705'],
    'joerg': [97908, 1794, '2019dobi', '25532'],
    'jogi': [125551, 1847, 'jogi4711', '25547'],
    'julia': [144087, 2237, 'julest', '54522'],
    'justus': [111413, 2118, 'justusfriedrich', '48541'],
    'jutta': [129326, 828, 'juttawenner', '24088'],
    'kevin': [47163, 427, 'kevinkonsorr', '25994'],
    'kevinu': [186521, 4178, 'kevinurb', '125930'],
    'lennard': [203094, 3162, 'Lennardowski', '114206'],
    'manolo': [111828, 1922, 'manologg', '25533'],
    'marcel': [110666, 2119, 'selloh', '44175'],
    'marian': [112270, 2110, 'marian', '39303'],
    'mario': [115250, 2121, 'mariofriedrich', '48542'],
    'mark': [240268, 3899, 'xhomer', '163187'],
    'markus': [94728, 1841, 'markustm', '25538'],
    'matthias': [147730, 2488, 'thias87', '53833'],
    'michael': [47164, 440, 'michael3001', '90199'],
    'paul': [125227, 2327, 'paulgi', '42852'],
    'rene': [183118, 2700, '183118', '98000'],
    'ronnie': [101231, 3266, 'Ronnie77', '53381'],
    'sebastian': [89847, 1873, 'basti09', '25644'],
    'simon': [176326, 2699, 'Simonkk', '194948'],
    'simone': [239411, 3530, 'naduu1', '140240'],
    'sven': [42855, 288, 'svenrippel', '163503'],
    'svenp': [177160, 2835, 'Sven PIP', '115943'],
    'tobias': [127232, 2396, 'nr127232', '68205'],
    'tom': [189326, 2653, 'tombecka', '95829'],
    'uli': [77646, 1769, 'ulrichberg', '23739'],

    # non-PDGA
    'bjoern': [None, 3695, 'björng23', '91927'],
    'davidb': [None, 3681, 'gerbeerserker', '129951'],
    'helge': [None, 3164, 'gmstrott', '28039'],
    'jans': [None, 3381, 'UlfRolf', '85040'],
    'jens': [None, 1716, 'jpsteffen (JP)', '39511'],
    'kevind': [None, 1707, 'kevind', '25520'],
    'markuss': [None, 3277, 'cardenalmendoza', '114204'],
    'renew': [None, 3810, 'renewestermann', '61442'],

    # non-GT
    'jonas': [265307, None, 'microbob', '168361'],

    # non-UDisc
    'janne': [240385, 2497, None, '96672'],

    # non-Metrix

    # incomplete
    'andreas': [None, None, None, '185330'],
    'ann-kathrin': [None, None, None, '170405'],
    'anna': [None, None, None, '114401'],
    'christian': [None, 3911, None, '137742'],
    'gustav': [None, None, 'guddu001', '189094'],
    'jesko': [None, None, 'jeko81', '116360'],
    'lars': [None, 3889, None, '166334'],
    'lukas': [None, None, None, '156575'],
    'marcelr': [None, None, None, '92056'],
    'markusw': [None, None, None, '172865'],
    'thomas': [None, None, None, '133132'],
    'torsten': [None, None, None, '59971'],
    'uwe': [None, None, None, '167484'],
    'valentin': [None, 3884, None, '165185'],

    # supporting
    'antonia': [None, None, None, None],
    'babara': [None, None, None, None],
    'basti': [None, None, None, None],
    'bettina': [None, None, None, None],
    'conni': [None, None, None, None],
    'dorina': [None, None, None, None],
    'louis': [None, None, None, None],
    'martina': [None, None, None, None],
    'nikola': [None, None, None, None],
    'oma': [None, None, None, None],
    'stefanie': [None, None, None, None],
    'stephan': [None, None, None, None],
    'wolfgang': [None, None, None, None],
    'zinnia': [None, None, None, None],

    # old friends
    'julia-sophie': [None, None, None, None],
    'lux': [71666, 1582, 'lux', '54523'],
    'marcelk': [None, 2966, 'marcelge91', '113505'],
    'ralf': [91363, 2038, 'rollerralf', '41591'],
    'ralfw': [104566, 429, 'rallewi', '26806'],
    'tana': [None, 2726, 'tanapat', '101826'],

}

update_friend_fields(fields, friends)
