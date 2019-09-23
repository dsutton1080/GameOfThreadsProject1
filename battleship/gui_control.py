import gui_states


def run():
    """
    The executive procedure that defines the control flow between all the sub-procedures.
    :return: void
    """
    play_again = True
    gui_states.screen.fill((0, 0, 0))
    while play_again:
        gui_states.run_start()
        num = gui_states.run_get_number_ships()
        player1ships = gui_states.run_place_ships(num, "Player 1")
        player2ships = gui_states.run_place_ships(num, "Player 2")
        winnerName = gui_states.run_game_loop(player1ships, player2ships)
        play_again = gui_states.winner_screen_prompt_replay(winnerName)
