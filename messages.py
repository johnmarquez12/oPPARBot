# CLIENT MESSAGE CONSTATNTS

def get_points_message(author, pts):
    return f'Points for {author.mention}: {pts}'

def gamble_win_message(author, pts):
    return f'Nice Cock!: {pts} {author.mention}'

def gamble_loss_message(author, pts):
    return f'Nice Try Guy: {pts} {author.mention}'

GAMBLE_LOSS_MESSAGE_0 = '(╯°□°）╯︵ ┻━┻ Points: 0'

GAMBLE_BROKE_MESSAGE = 'u broke af lmao'

GET_POINTS_ERROR = 'Ur not in database yet bitch, sorry havent implemented it ;-; type .play to get points'

INT_CONVERSION_ERROR_MESSAGE = 'not an integer dipshit'

DONATE_TO_SELF_ERROR = 'why are you even trying lmao'

DONATE_BROKE_ERROR = 'lmfao u cant even donate broke bitch'

POINTS_SETUP = 'Ur points have been set up xd'

POINTS_SETUP_ERROR = 'U already have points dipshit'

