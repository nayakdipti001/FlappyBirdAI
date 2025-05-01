🐦 Flappy Bird AI using NEAT
This project uses NeuroEvolution of Augmenting Topologies (NEAT) to train an AI agent to play the popular game Flappy Bird. The AI learns to navigate through pipes by evolving over generations without any prior knowledge of the game.

🚀 Features
Built using Python and Pygame

Implements NEAT algorithm for evolving neural networks

Visual representation of AI-controlled birds

Displays generation count, score, and alive birds

🧠 How the AI Works
The bird is controlled by a neural network.

Input to the neural net: bird's y-position, distance to next pipe, height of pipe gap.

Output: whether the bird should jump or not.

NEAT evolves a population of neural networks over generations based on fitness (score)


⚙️ Requirements
Install dependencies using pip:

pip install pygame neat-python
