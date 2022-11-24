import chess
import chess.engine
import random

brd = chess.Board()


def last_move_player():
    moves = []
    for c in brd.legal_moves:
        moves.append(str(c))
    brd.push_san(moves[-1])


def random_move_player():
    moves = []
    for c in brd.legal_moves:
        moves.append(str(c))
    brd.push_san(moves[random.randint(0, len(moves) - 1)])


engine = chess.engine.SimpleEngine.popen_uci("/usr/games/stockfish")


def evaluate_position_stockfish(board) -> int:
    result = engine.analyse(board, chess.engine.Limit(time=0.01))
    print(result["score"])
    m = result["score"].relative.score().real
    print(m)
    return int(str(m))


def evaluate_position(board) -> float:
    white = board.occupied_co[chess.WHITE]
    black = board.occupied_co[chess.BLACK]
    return (
            chess.popcount(white & board.pawns) - chess.popcount(black & board.pawns) +
            3 * (chess.popcount(white & board.knights) - chess.popcount(black & board.knights)) +
            3 * (chess.popcount(white & board.bishops) - chess.popcount(black & board.bishops)) +
            5 * (chess.popcount(white & board.rooks) - chess.popcount(black & board.rooks)) +
            9 * (chess.popcount(white & board.queens) - chess.popcount(black & board.queens))
    ) + 0.001 * random.random()


def negamax_move_player(brd):
    moves = []
    for c in brd.legal_moves:
        moves.append(str(c))

    values = []
    for move in moves:
        copy_board = brd.copy()
        copy_board.push_san(move)
        value = nega_max(copy_board, 1, True)
        values.append(value)

    index = values.index(max(values))
    brd.push_san(moves[index])


def nega_max(board, depth, is_maximizer):  # let black is maximizer
    if depth == 0:
        if is_maximizer:
            return -evaluate_position(board)
        return evaluate_position(board)

    max = -999999
    for c in board.legal_moves:
        move = str(c)
        copy_board = board.copy()
        copy_board.push_san(move)
        next = -nega_max(copy_board, depth - 1, not is_maximizer)
        if next > max:
            max = next
    return max


def monte_carlo_move_player():
    moves = []
    for c in brd.legal_moves:
        moves.append(str(c))

    values = []
    for move in moves:
        copy_board = brd.copy()
        copy_board.push_san(move)
        value = monte_carlo(copy_board)
        values.append(value)

    index = values.index(max(values))
    brd.push_san(moves[index])


def monte_carlo(board):
    def simulate_times(moves):
        for i in range(moves):
            negamax_move_player(board)

    simulate_times(2)
    return evaluate_position(board)


def negascout_move_player():
    moves = []
    for c in brd.legal_moves:
        moves.append(str(c))

    values = []
    for move in moves:
        copy_board = brd.copy()
        copy_board.push_san(move)
        value = nega_scout(copy_board, 3, 1, 3)
        values.append(value)

    index = values.index(max(values))
    brd.push_san(moves[index])


def nega_scout(board, depth, alpha, beta):
    if depth == 0:
        return evaluate_position(board)

    bestValue = -999999
    for move in board.legal_moves:
        copy_board = board.copy()
        copy_board.push(move)
        result = nega_scout(copy_board, depth - 1, -(alpha + 1), -alpha)
        board_value = -result
        if (board_value > alpha and board_value < beta and depth > 1):
            result2 = nega_scout(copy_board, depth - 1, -beta, -board_value)
            board_value = max(board_value, -result2)
        if board_value > bestValue:
            bestValue = board_value
    return bestValue


def pvs_move_player():
    moves = []
    for c in brd.legal_moves:
        moves.append(str(c))

    values = []
    for move in moves:
        copy_board = brd.copy()
        copy_board.push_san(move)
        value = pvs(copy_board, 3, 1, 3)
        values.append(value)

    index = values.index(max(values))
    brd.push_san(moves[index])


def pvs(board, depth, alpha, beta):
    if depth == 0:
        return evaluate_position(board)

    bestValue = -999999
    for move in board.legal_moves:
        copy_board = board.copy()
        copy_board.push(move)
        result = pvs(copy_board, depth - 1, -(alpha + 1), -alpha)
        board_value = -result
        if (board_value > alpha and board_value < beta):
            result2 = nega_scout(copy_board, depth - 1, -beta, -alpha)
            board_value = -result2
        if board_value > bestValue:
            bestValue = board_value
    return bestValue


while True:
    # white player
    random_move_player()
    print(brd)

    # black player
    # negamax_move_player(board)
    # negascout_move_player()
    # pvs_move_player()
    monte_carlo_move_player()

    print("~")
    print("~")
    print("~")
    print(brd)

    command = input("command:")
    if command == "exit":
        break