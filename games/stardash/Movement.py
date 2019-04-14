#class Movement():

#    def __init__(self):
#        pass


def moveMiner(ship, game, player, mineral, taken):
    """Gets passed a ship, the game and the player.

    Moves a Miner towards the nearest asteroid.
    """
    minDist = _distance(0, 0, game.size_x, game.size_y)
    moves = ship.job.moves
    asteroids = game.bodies
    minAst = asteroids[0]
    for astNum in range(4, len(asteroids)):
        if (asteroids[astNum].material_type == mineral):
            dist = _distance(ship.x, ship.y, asteroids[astNum].x, asteroids[astNum].y)
            if dist < minDist:
                minDist = dist
                minAst = asteroids[astNum]
    currDist = minDist
    turns = 1 # to get to the asteroid
    nextX = minAst.next_x(turns)
    nextY = minAst.next_y(turns)
    nextDist = _distance((ship.x + moves * turns) if (ship.x - nextX > 0) else (ship.x - ship.move *turns),
                         (ship.y + moves * turns) if (ship.y - nextY > 0) else (ship.y - ship.move *turns),
                         nextX,
                         nextY)
    while nextDist < currDist:
        currDist = nextDist
        turns += 1
        nextX = minAst.next_x(turns)
        nextY = minAst.next_y(turns)
        nextDist = _distance((ship.x + moves * turns) if (ship.x - nextX > 0) else (ship.x - ship.move * turns),
                             (ship.y + moves * turns) if (ship.y - nextY > 0) else (ship.y - ship.move * turns),
                             nextX,
                             nextY)

    x, y = _moveTo(ship.x, ship.y, nextX, nextY, moves)
    print(x, y)
    ship.move(ship.x + x , ship.y + y)


def _moveTo(shipX, shipY, tarX, tarY, move):
    """Returns the x and y speed to get to target x and y.

    This is to take care of the positives and negatives.
    """
    max_move = int(move / (2**.5)) # in single direction

    x = abs(shipX - tarX)
    y = abs(shipY - tarY)
    print(x, y)


    if tarX < shipX: # Target is to the left
        if (x > max_move):
            x = -1 * max_move
        else:
            x = -1 * x
    else: # Target is to the right
        if (x > max_move):
            x = max_move

    if tarY < shipY: # Target is below
        if (y > max_move):
            y = -1 * max_move
        else:
            y = -1 * y
    else:
        if (y > max_move):
            y = max_move


    return x, y

def _distance(shipX, shipY, tarX, tarY):
    return ((shipX - tarX)**2 + (shipY - tarY)**2) ** .5








