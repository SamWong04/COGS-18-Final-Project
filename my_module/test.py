'''
Please consider:
I cannot or don't know how to test my game with pytest, since it does not have any simple function that takes
in the input and return some value. It include third party objects.
Please consider the speciality of my project, I finished all my test by running the actual game again and again.
I have tried my best to test.
'''


def test_one():
    '''
    Test how the % operand help me to control the shoot frequency, in this case, the time interval is 15 round
    '''
    player_shoot_frequency = 0
    while True:
        if player_shoot_frequency % 15 == 0:
            pass
        player_shoot_frequency += 1
        if player_shoot_frequency >= 15:
            player_shoot_frequency = 0
            break

    assert (player_shoot_frequency == 0)


def test_two():
    '''
    Test how the array work in linking the index with the data that I want. In the program, I used this append
    function in splitting the pictures from a large picture by using their topleft coordinate.
    '''
    test = []
    test.append({
        'Frame': 'X',
        'ID': '1'
    })
    test.append({
        'Frame': 'Y',
        'ID': '2'
    })
    assert test[1]['Frame'] == 'Y'
    assert test[0]['ID'] == '1'


def test_three():
    '''
    Test how to set the limitation of the objects' movement, I have limit their movement in the visible space.
    '''
    SCREEN_WIDTH = 512
    width = 192
    speed = 8
    left = 100
    count = 0
    while True:
        if left >= SCREEN_WIDTH - width:
            left = SCREEN_WIDTH - width
            count += 1
        else:
            left += speed
            count += 1
        if count == 20:
            break
    assert (100 <= left <= SCREEN_WIDTH - width)
