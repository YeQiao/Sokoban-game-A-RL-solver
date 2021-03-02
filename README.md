# Sokoban-game-A-RL-solver

All level.txt should stay under sokobanLevels folder. Benchmark levels are already inside.
How to run:
python sokoban.py level.txt


FOR Q-learning
Frst: install gym toolkit
	git clone https://github.com/openai/gym
	cd gym
	pip install -e .
	
Seond: install gym-sokoban extension
	git clone git@github.com:mpSchrader/gym-sokoban.git
	cd gym-sokoban
	pip install -e .
	
third: replace the sokoban_env.py with the our version.

Aaliable map setup: under the file gym_sokoban/envs/available_envs.json
Trained Q-table named Array.txt
