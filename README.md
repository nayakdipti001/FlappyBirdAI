🐦 Flappy Bird AI using NEAT
This project utilizes NeuroEvolution of Augmenting Topologies (NEAT) to train an AI agent to play the classic game Flappy Bird. Through evolutionary algorithms, the AI learns to navigate through pipes by evolving over generations without any prior knowledge of the game mechanics.

🚀 Features
Python & Pygame: Built using Python and the Pygame library for game rendering.

NEAT Integration: Implements the NEAT algorithm to evolve neural networks.

Visual Feedback: Displays generation count, score, and number of alive birds during training.

Performance Tracking: Includes fitness plots to monitor AI performance over generations.

Replay Functionality: Ability to replay the best-performing bird's gameplay.

📁 Project Structure

FlappyBirdAI/
├── build/                 # Build files
├── dist/                  # Distribution files
├── images/                # Game assets (e.g., bird, pipes, background)
├── sounds/                # Sound assets
├── .idea/                 # IDE configuration files
├── best_bird.pkl          # Serialized best-performing neural network
├── config-feedforward.txt # NEAT configuration file
├── fitness_plot.png       # Fitness over generations plot
├── flappy.py              # Core game logic
├── flappy.spec            # PyInstaller spec file
├── main.py                # Entry point for training the AI
├── replay.py              # Replay the best-performing bird
├── visualize.py           # Visualize the neural network
├── winner_net/            # Directory for storing the winning network
├── winner_net.png         # Visualization of the winning network
└── README.md              # Project documentation


🧠 How the AI Works
Inputs to the Neural Network:

Bird's vertical position (y)

Distance to the next pipe

Height of the pipe gap

Output:

Decision to flap or not

Fitness Function:

Rewards the bird for staying alive and successfully passing through pipes.

Evolution Process:

The NEAT algorithm evolves the population of neural networks over generations, selecting for higher fitness scores.

⚙️ Requirements
Ensure you have Python installed. Then, install the necessary dependencies:


pip install pygame neat-python
📝 How to Run
Train the AI:


python main.py
This will start the training process, where multiple birds will learn to play the game over generations.

Replay the Best Bird:

After training, you can watch the best-performing bird:


python replay.py
📊 Visualizations
Fitness Plot: fitness_plot.png shows the fitness score progression over generations.

Neural Network Visualization: winner_net.png provides a graphical representation of the best-performing neural network.



📚 References
NEAT-Python Documentation

Inspired by various Flappy Bird AI projects and tutorials.

📜 License
This project is open-source and available under the MIT License.








