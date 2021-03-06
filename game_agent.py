"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass

def center_score(game, player):
    """Outputs a score equal to square of the distance from the center of the
    board to the position of the player.

    This heuristic is only used by the autograder for testing.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : hashable
        One of the objects registered by the game object as a valid player.
        (i.e., `player` should be either game.__player_1__ or
        game.__player_2__).

    Returns
    ----------
    float
        The heuristic value of the current game state
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    w, h = game.width / 2., game.height / 2.
    y, x = game.get_player_location(player)
    return float((h - y)**2 + (w - x)**2)

def open_move_score(game, player):
    """The basic evaluation function described in lecture that outputs a score
    equal to the number of moves open for your computer player on the board.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : hashable
        One of the objects registered by the game object as a valid player.
        (i.e., `player` should be either game.__player_1__ or
        game.__player_2__).

    Returns
    ----------
    float
        The heuristic value of the current game state
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    return float(len(game.get_legal_moves(player)))


def custom_score(game, player):
    # best heuristic / improved score for now
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(own_moves - opp_moves)
    


def custom_score_2(game, player):
    # open move
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    return float(len(game.get_legal_moves(player)))    


def custom_score_3(game, player):
    # improved score
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(own_moves - opp_moves)


# TODO: move depth to function arguments instead of class
# TODO: figure out how to integrate the score function

class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=None, timeout=10.):
        self.search_depth = search_depth
        self.time_left = None
        self.TIMER_THRESHOLD = timeout
    """
    I know this shouldn't be changed but I changed it to integrate the code in
    in the score method. I could override it and make it point to an external
    minimax function in the MinimaxPlayer __init__ but I was having trouble 
    overriding it with a score method in the MinimaxPlayer class so I changed 
    it to a not implemented method
    """
    def score(self):
        raise NotImplementedError

class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """
    
    def __init__(self,search_depth=3,score_fn=None,timeout=10.):
        super().__init__(search_depth=search_depth,timeout=timeout)

    def score(self,game,depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()    
        
        min_value = game.active_player!=self
        
        # check if it's a terminal state first
        legal_moves = game.get_legal_moves()
        if len(legal_moves)==0:
            return float('inf') if min_value else float('-inf')
        
        # check the depth now
        # if it wasn't a terminal state we have to go deeper so we can use a 
        # heuristic function if we're at the depth limit
# =============================================================================
#         loc='{}->({},{}) '.format(depth,game.get_player_location(game._player_1),
#              game.get_player_location(game._player_2))
#         print(loc)
# =============================================================================
        if depth <= 1:
            return custom_score(game,self)
        
        # If depth limit is not reached yet we can go one more level
        if min_value:
            v = float("inf")
            for m in legal_moves:
                v = min(v,self.score(game.forecast_move(m),depth-1))
            return v
        else:
            v = float("-inf")
            for m in legal_moves:
                v = max(v,self.score(game.forecast_move(m),depth-1))
            return v  

    
    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
#        print("\n"+game.to_string())
        
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)
            
        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        
        legal_moves = game.get_legal_moves()
        if len(legal_moves)<1:
            return (-1,-1)        

        move_score = []
        for m in legal_moves:
            new_game=game.forecast_move(m)
            move_score.append(self.score(new_game,depth))
        
        _,best_move = max(zip(move_score,legal_moves))
                
        return best_move
    
        

class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """
    def __init__(self,search_depth=3,score_fn=None,timeout=10.):
        super().__init__(search_depth=search_depth,timeout=timeout)

    def score(self,game,depth,alpha,beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()    
        
        min_value = game.active_player!=self
        
        # check if it's a terminal state first
        legal_moves = game.get_legal_moves()
        if len(legal_moves)==0:
            return float('inf') if min_value else float('-inf')
        
        # check the depth now
        # if it wasn't a terminal state we have to go deeper so we can use a 
        # heuristic function if we're at the depth limit
# =============================================================================
#         loc='{}->({},{}) '.format(depth,game.get_player_location(game._player_1),
#              game.get_player_location(game._player_2))
#         print(loc)
# =============================================================================
        if depth <= 1:
            return custom_score(game,self)
        
        # If depth limit is not reached yet we can go one more level
        if min_value:
            v = float("inf")
            for m in legal_moves:
                v = min(v,self.score(game.forecast_move(m),depth-1,alpha,beta))
                if v <= alpha:
                    return v
                beta = min(beta,v)
            return v
        else:
            v = float("-inf")
            for m in legal_moves:
                v = max(v,self.score(game.forecast_move(m),depth-1,alpha,beta))
                if v>= beta:
                    return v
                alpha = max(alpha,v)
            return v  

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
#        print("\n"+game.to_string())
        
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            d=1
            while True:
                best_move = self.alphabeta(game, d)
                d+=1
                
        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move
    
    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        
        legal_moves = game.get_legal_moves()
        if len(legal_moves)<1:
            return (-1,-1)        

        move_score = []
        for m in legal_moves:
            new_game=game.forecast_move(m)
            move_score.append(self.score(new_game,1,alpha,beta))
        
        _,best_move = max(zip(move_score,legal_moves))
                
        return best_move
