"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""
import sys
sys.path.append('../')

import unittest

import isolation
import game_agent
import sample_players

from importlib import reload


class IsolationTest(unittest.TestCase):
    """Unit tests for isolation agents"""
    NUMBER_OF_GAMES = 20
    
    def setUp_random_vs_minimax(self):
        reload(game_agent)
        self.player1 = sample_players.RandomPlayer()
        self.player2 = game_agent.MinimaxPlayer(search_depth=10)
        self.game = isolation.Board(self.player1, self.player2,width=5,height=3)
        pass
    
    def test_minimax_init(self):
        self.setUp_random_vs_minimax()
        player = game_agent.MinimaxPlayer(search_depth=10,timeout=5.)
        self.assertTrue(player.search_depth==10)
        self.assertTrue(player.TIMER_THRESHOLD==5.)
        self.assertTrue(player.score==game_agent.min_value)
        pass
        
    def test_minimax_plays(self):
        self.setUp_random_vs_minimax()
        winner,history,reason = self.game.play()
        pass
    
    def test_minimax_vs_random(self):
        count=0    
        for _ in range(self.NUMBER_OF_GAMES):
            self.setUp_random_vs_minimax()
            winner,history,reason = self.game.play()
            if winner==self.player2:
                count+=1
        self.assertTrue(count==self.NUMBER_OF_GAMES,msg='won : {}/{}'.format(count,self.NUMBER_OF_GAMES))
    
if __name__ == '__main__':
    unittest.main()
