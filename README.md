# Checkers AI

Checkers gameplay is inspired by [this solution](https://github.com/techwithtim/Python-Checkers),
but with changed rules.

There are three ways to play, user vs user, AI vs AI and user vs AI.

Algorithms - We have used Min-max, Alpha-beta and Depth-limited algorithms to solve checkers game.

Evaluation functions - There is two evaluation functions to evaluate the positions:
- Three stages function 
- Edge function 

Requirements - pygame library.

Python version - our python version was 3.11

Starting the game: First decide in what mode you want to play and open the corresponding .py file. 

If you want to run 'user_vs_user' or 'user_vs_ai', you can provide these values to 'start_game' function:

- `evaluation_functions` - way of evaluation (1 is Three stage function, 2 is Edge function), `1` or `2`; default `1`
- `depth` - any integer; default `3`
- `algorithm` - `'min-max'` or `'alpha-beta'` or `'depth-limited'`; default `'min-max'`
- `color` - if playing against AI, `WHITE` or `RED`; default `WHITE`

If you want to run 'ai_vs_ai' you can provide these values to 'Game' function:

- `mode` - the mode of the game, `ivi` or `pvp` or `pvi`; default `ivi`
- `algorithm_player_one` - name of the algorithm for player one, `'min-max'` or `'alpha-beta'` or `'depth-limited'`; default `'min-max'`
- `algorithm_player_two` - name of the algorithm for player two , `'min-max'` or `'alpha-beta'` or `'depth-limited'`; default `'min-max'`

And this values to 'start_game'

- `evaluation_functions` - way of evaluation (1 is Three stage function, 2 is Edge function), `1` or `2`; default `1`
- `depth` - any integer; default `3`
# Checkers-Using-AI-algorithms
