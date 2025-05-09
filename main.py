Snowboard Rush - A 3D OpenGL Endless Runner Game 🏂
Snowboard Rush is a 3D endless runner game built entirely using OpenGL (PyOpenGL), with custom drawing done via GL_POINTS, GL_LINES, and GL_QUADS. The game uses no external assets — everything is rendered using raw OpenGL calls. Designed to demonstrate low-level graphics programming and algorithmic rendering in Python.
Gameplay Overview 🎮

Endless Terrain Navigation: Move through an infinite snowy landscape.
Shoot Obstacles (Avoid): Dodge trees, snowmen, rocks, turrets, and birds by moving or jumping.
Rotate Player to Aim: Adjust direction with jumps and spins.
Avoid Obstacles and Keep Health Up: Collect life boxes to maintain lives.
Blood Splatter Effects and Scoring System: Earn points over time, boosted by gold stars and power-ups.
Multiple Difficulty Levels and Pause Menu: Difficulty increases with progress, with a pause option.

Features ✨

Shooting Mechanics with Rotation-based Aim: Jump and spin to navigate obstacles.
Randomly Spawning Obstacles with AI Movement: Birds move unpredictably in the air.
Collision Detection (Player, Obstacles): Detect hits with obstacles and collectibles.
Dynamic Track Effects: Snowboard tracks appear and fade behind the player.
No Textures — All Visuals Created Using Midpoint Line/Circle Algorithms: Rendered with OpenGL primitives.
Pause Menu with Difficulty Toggle: Pause and adjust gameplay pace.
Main Menu and Game Over Screens: Start screen and end-game summary.

Controls ⌨️



Action
Key / Mouse



Move Up
Spacebar (Jump)


Move Down
N/A


Move Left
Left Arrow


Move Right
Right Arrow


Rotate Gun CCW
N/A


Rotate Gun CW
N/A


Fire Bullet
N/A


Toggle Camera
C


Zoom Out
Q


Zoom In
E


Activate Boost
B


Restart
R


Pause/Resume
Center Button


Exit
ESC or Right Button


Install Dependencies 📦
pip install PyOpenGL PyOpenGL_accelerate numpy

Run the Game 🚀
python snowboard_rush.py

Project Structure 📂
your-folder/
├── snowboard_rush.py  # Main game code
└── gameplay.png       # Screenshot (add yourself)

Algorithms Used 🧠

Midpoint Line Drawing Algorithm: Used for UI elements and tracks.
Midpoint Circle Drawing Algorithm: Applied for rendering stars and life boxes.
Zone-based Line Conversion: Ensures consistent rendering of 3D lines.
Basic Vector Math for Rotation and Collision: Handles player movement and obstacle detection.

Notes 📝

Built with educational purposes in mind.
Ensure OpenGL and GLUT are supported on your system (e.g., install freeglut3-dev on Ubuntu).

