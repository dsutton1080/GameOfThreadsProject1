import io as io
import data as data


def run_game_procedure():
    """

    """
    numShips = io.prompt_num_ships()
    player1 = data.Player(name=io.prompt_player_name(), ships=io.prompt_fill_ships(), guesses=[])
    player2 = data.Player(name=io.prompt_player_name(), ships=io.prompt_fill_ships(), guesses=[])
    initialState = data.State(player1, player2)
    play_game(initialState)

def play_loop():
    """

    """
    while True:
        run_game_procedure()
        # if !(io.prompt_replay()):
        #     io.close_display()
        #     break

def play_game(initialState):
    """

    :param initialState: 
    """
    lastState = initialState
    curState = initialState
    while True:
        io.display_state(data.to_display_dict(curState))
        guess = io.prompt_guess(curState.player.guesses)
        lastState = curState
        curState = data.update_state(guess, curState)
        io.display_guess_hit_feedback(data.hit_status(guess, lastState))
        io.display_guess_sunk_feedback(data.sunk_status(guess, lastState))
        if(data.is_game_over(curState)):
            winnerName = lastState.currentPlayer.name
            io.display_game_over(winnerName)
            break
        # countdown here?
