
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time
from math import cos, sin

# Camera setup
camera_pos = (0, 300, 600)
base_camera_pos = list(camera_pos)
camera_shake_duration = 0
camera_shake_intensity = 10
fovY = 60
zoom_level = 1.0
ZOOM_STEP = 0.1
MIN_ZOOM = 0.5
MAX_ZOOM = 2.0
view_mode = 'third_person'
GRID_WIDTH = 400
GRID_LENGTH = 2000
PLAYER_X = 0
PLAYER_Z = 200
PLAYER_Y = 3
player_y_velocity = 0
gravity = -0.5
jump_strength = 10
BASE_STEP_SIZE = 40
STEP_SIZE = BASE_STEP_SIZE
GAME_RUNNING = True
paused = False
width = 1000
height = 800
base_obstacle_speed = 5
obstacle_speed = base_obstacle_speed
points = 0
last_point_time = 0
point_interval = 1.0
gold_stars = []
pink_gold_stars = []
gold_star_collect = 0
boosts_available = 0
player_lives = 1
live_boxes = []
difficulty_multiplier = 1.0
boost_active = False
boost_start_time = 0
BOOST_DURATION = 4.0
BOOST_MULTIPLIER = 3.0
tracks = []
TRACK_WIDTH = 15
TRACK_LENGTH = 40
last_bird_move_time = 0
bird_kill_message_timer = 0.0
player_rotation = 0.0
is_spinning = False
spin_speed = 540.0
is_falling = False
fall_duration = 0.0
MAX_FALL_DURATION = 3.0
is_laid_down = False

obstacles = []

def draw_line(x1, y1, x2, y2):
    glBegin(GL_LINES)
    glVertex3f(x1, y1, 0)
    glVertex3f(x2, y2, 0)
    glEnd()

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_12):
    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(font, ord(char))

def draw_tree(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)
    glColor3f(0.55, 0.27, 0.07)
    glPushMatrix()
    glTranslatef(0, 22.5, 0)
    gluCylinder(gluNewQuadric(), 6, 6, 37.5, 15, 15)
    glPopMatrix()
    glColor3f(0.0, 0.6, 0.0)
    for i in range(3):
        glPushMatrix()
        glTranslatef(0, 52.5 + i * 18, 0)
        glutSolidCone(21 - i * 3, 30, 18, 18)
        glPopMatrix()
    glPopMatrix()

def draw_snowman(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)
    glColor3f(1, 1, 1)
    glTranslatef(0, 15, 0)
    glutSolidSphere(15, 12, 12)
    glTranslatef(0, 20, 0)
    glutSolidSphere(10, 12, 12)
    glTranslatef(0, 16, 0)
    glutSolidSphere(7, 12, 12)
    glColor3f(0, 0, 0)
    glPushMatrix()
    glTranslatef(3, 2, 6)
    glutSolidSphere(1.2, 6, 6)
    glTranslatef(-6, 0, 0)
    glutSolidSphere(1.2, 6, 6)
    glPopMatrix()
    glPopMatrix()

def draw_rock(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)
    glColor3f(0.3, 0.3, 0.3)
    glScalef(1.5, 1.1, 1.3)
    glutSolidSphere(10, 10, 10)
    glPopMatrix()

def draw_turret(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)
    glColor3f(0.3, 0.3, 0.4)
    gluCylinder(gluNewQuadric(), 8, 8, 18, 12, 12)
    glTranslatef(0, 18, 0)
    glColor3f(0.2, 0.2, 0.6)
    glutSolidCone(10, 18, 12, 12)
    glPopMatrix()

def draw_bird(x, y, z, size=5):
    glPushMatrix()
    glTranslatef(x, y, z)
    glColor3f(0.8, 0.5, 0.2)
    glutSolidSphere(size, 15, 15)
    glPushMatrix()
    glTranslatef(0, 0, 0)
    glScalef(2.0, 0.5, 0.5)
    glutSolidCube(size)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(size * 0.8, size * 0.5, 0)
    glutSolidSphere(size * 0.4, 15, 15)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(-size * 0.8, 0, 0)
    glScalef(1.5, 0.3, 0.5)
    glutSolidCube(size)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(size * 0.8, 0, 0)
    glScalef(1.5, 0.3, 0.5)
    glutSolidCube(size)
    glPopMatrix()
    glPopMatrix()

def draw_gold_star(x, y, z):
    glPushMatrix()
    glTranslatef(x, y + 15, z)
    glColor3f(1.0, 0.84, 0.0)
    glBegin(GL_TRIANGLE_FAN)
    glVertex3f(0, 0, 0)
    for i in range(100):
        angle = 2.0 * 3.14159 * i / 100
        glVertex3f(15 * cos(angle), 15 * sin(angle), 0)
    glEnd()
    glBegin(GL_LINES)
    glVertex3f(0, 10, 0)
    glVertex3f(5, 5, 0)
    glVertex3f(5, 5, 0)
    glVertex3f(10, 0, 0)
    glVertex3f(10, 0, 0)
    glVertex3f(5, -5, 0)
    glVertex3f(5, -5, 0)
    glVertex3f(0, -10, 0)
    glVertex3f(0, -10, 0)
    glVertex3f(-5, -5, 0)
    glVertex3f(-5, -5, 0)
    glVertex3f(-10, 0, 0)
    glVertex3f(-10, 0, 0)
    glVertex3f(-5, 5, 0)
    glVertex3f(-5, 5, 0)
    glVertex3f(0, 10, 0)
    glEnd()
    glPopMatrix()

def draw_pink_gold_star(x, y, z):
    glPushMatrix()
    glTranslatef(x, y + 15, z)
    glColor3f(1.0, 0.5, 0.75)
    glBegin(GL_TRIANGLE_FAN)
    glVertex3f(0, 0, 0)
    for i in range(100):
        angle = 2.0 * 3.14159 * i / 100
        glVertex3f(15 * cos(angle), 15 * sin(angle), 0)
    glEnd()
    glBegin(GL_LINES)
    glVertex3f(0, 10, 0)
    glVertex3f(5, 5, 0)
    glVertex3f(5, 5, 0)
    glVertex3f(10, 0, 0)
    glVertex3f(10, 0, 0)
    glVertex3f(5, -5, 0)
    glVertex3f(5, -5, 0)
    glVertex3f(0, -10, 0)
    glVertex3f(0, -10, 0)
    glVertex3f(-5, -5, 0)
    glVertex3f(-5, -5, 0)
    glVertex3f(-10, 0, 0)
    glVertex3f(-10, 0, 0)
    glVertex3f(-5, 5, 0)
    glVertex3f(-5, 5, 0)
    glVertex3f(0, 10, 0)
    glEnd()
    glPopMatrix()

def draw_live_box(x, y, z, size=10):
    glPushMatrix()
    glTranslatef(x, y, z)
    glColor3f(0.0, 1.0, 0.0)
    glutSolidCube(size)
    glPopMatrix()

def draw_snowboarder(x, z, minimal=False):
    global PLAYER_Y, player_rotation, is_laid_down
    glPushMatrix()
    glTranslatef(x, PLAYER_Y, z)
    if is_laid_down:
        glRotatef(90, 1, 0, 0)
    else:
        glRotatef(player_rotation, 0, 1, 0)
    if minimal:
        glPushMatrix()
        glTranslatef(0, -2, 0)
        glColor3f(0.3, 0.3, 0.3)
        glScalef(1.0, 0.1, 3.0)
        glutSolidCube(20)
        glPopMatrix()
    else:
        glPushMatrix()
        glTranslatef(0, -2, 0)
        glColor3f(0.3, 0.3, 0.3)
        glScalef(1.0, 0.1, 3.0)
        glutSolidCube(20)
        glPopMatrix()
        glPushMatrix()
        glTranslatef(5, 8, 0)
        glColor3f(0.0, 0.0, 0.2)
        glScalef(0.5, 1.5, 0.5)
        glutSolidCube(10)
        glPopMatrix()
        glPushMatrix()
        glTranslatef(-5, 8, 0)
        glColor3f(0.0, 0.0, 0.2)
        glScalef(0.5, 1.5, 0.5)
        glutSolidCube(10)
        glPopMatrix()
        glPushMatrix()
        glTranslatef(0, 23, 0)
        glColor3f(0.0, 0.0, 0.2)
        glutSolidCube(20)
        glPopMatrix()
        glPushMatrix()
        glTranslatef(10, 18, 0)
        glColor3f(1.0, 1.0, 0.0)
        glutSolidSphere(5, 12, 12)
        glPopMatrix()
        glPushMatrix()
        glTranslatef(-10, 18, 0)
        glColor3f(1.0, 1.0, 0.0)
        glutSolidSphere(5, 12, 12)
        glPopMatrix()
        glPushMatrix()
        glTranslatef(0, 33, 0)
        glColor3f(0.8, 0.8, 0.8)
        glutSolidSphere(8, 12, 12)
        glPopMatrix()
    glPopMatrix()

def draw_ground():
    glColor3f(0.95, 0.95, 0.98)
    glBegin(GL_QUADS)
    glVertex3f(-GRID_WIDTH, 0, -GRID_LENGTH)
    glVertex3f(GRID_WIDTH, 0, -GRID_LENGTH)
    glVertex3f(GRID_WIDTH, 0, GRID_LENGTH)
    glVertex3f(-GRID_WIDTH, 0, GRID_LENGTH)
    glEnd()
    glColor3f(0.5, 0.7, 0.8)
    glBegin(GL_QUADS)
    glVertex3f(-GRID_WIDTH, 0, -GRID_LENGTH)
    glVertex3f(-GRID_WIDTH - 50, 200, -GRID_LENGTH)
    glVertex3f(-GRID_WIDTH - 50, 200, GRID_LENGTH)
    glVertex3f(-GRID_WIDTH, 0, GRID_LENGTH)
    glEnd()
    glBegin(GL_QUADS)
    glVertex3f(GRID_WIDTH, 0, -GRID_LENGTH)
    glVertex3f(GRID_WIDTH + 50, 200, -GRID_LENGTH)
    glVertex3f(GRID_WIDTH + 50, 200, GRID_LENGTH)
    glVertex3f(GRID_WIDTH, 0, GRID_LENGTH)
    glEnd()

def draw_tracks():
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glColor4f(1.0, 1.0, 1.0, 0.9)
    for track in tracks:
        if track['z'] < GRID_LENGTH:
            glBegin(GL_QUADS)
            glVertex3f(track['x'] - TRACK_WIDTH / 2, 0.1, track['z'] - TRACK_LENGTH / 2)
            glVertex3f(track['x'] + TRACK_WIDTH / 2, 0.1, track['z'] - TRACK_LENGTH / 2)
            glVertex3f(track['x'] + TRACK_WIDTH / 2, 0.1, track['z'] + TRACK_LENGTH / 2)
            glVertex3f(track['x'] - TRACK_WIDTH / 2, 0.1, track['z'] + TRACK_LENGTH / 2)
            glEnd()
    glDisable(GL_BLEND)

def create_obstacles():
    if random.random() < 0.04:  
        type = random.choice(['tree', 'snowman', 'rock', 'turret'])
        x = random.uniform(-GRID_WIDTH / 2, GRID_WIDTH / 2)
        z = random.uniform(-GRID_LENGTH, -GRID_LENGTH / 2)
        y = 0
        obstacles.append({'type': type, 'x': x, 'y': y, 'z': z, 'size': 15})
    elif random.random() < 0.015:  # Increased from 0.01 to 0.015
        x = random.uniform(-GRID_WIDTH / 2, GRID_WIDTH / 2)
        y = random.uniform(20, 100)
        z = random.uniform(-GRID_LENGTH, -GRID_LENGTH / 2)
        obstacles.append({'type': 'bird', 'x': x, 'y': y, 'z': z, 'size': 5})

def create_gold_stars():
    if random.random() < 0.05:
        x = random.uniform(-GRID_WIDTH / 2, GRID_WIDTH / 2)
        z = random.uniform(-GRID_LENGTH, -GRID_LENGTH / 2)
        y = 0
        overlap = False
        for obs in obstacles:
            distance_x = abs(x - obs['x'])
            distance_z = abs(z - obs['z'])
            if distance_x < 30 and distance_z < 30:
                if obs['type'] == 'bird':
                    distance_y = abs(y - obs['y'])
                    if distance_y < (obs['size'] + 15):
                        overlap = True
                        break
                else:
                    overlap = True
                    break
        if not overlap:
            gold_stars.append({'x': x, 'y': y, 'z': z, 'size': 15})

def draw_obstacle(obs):
    if obs['z'] < GRID_LENGTH:
        if obs['type'] == 'tree':
            draw_tree(obs['x'], obs['y'], obs['z'])
        elif obs['type'] == 'snowman':
            draw_snowman(obs['x'], obs['y'], obs['z'])
        elif obs['type'] == 'rock':
            draw_rock(obs['x'], obs['y'], obs['z'])
        elif obs['type'] == 'turret':
            draw_turret(obs['x'], obs['y'], obs['z'])
        elif obs['type'] == 'bird':
            draw_bird(obs['x'], obs['y'], obs['z'], obs['size'])

def draw_gold_star_wrapper(star):
    if star['z'] < GRID_LENGTH:
        draw_gold_star(star['x'], star['y'], star['z'])

def draw_pink_gold_star_wrapper(star):
    if star['z'] < GRID_LENGTH:
        draw_pink_gold_star(star['x'], star['y'], star['z'])

def draw_live_box_wrapper(lbox):
    draw_live_box(lbox['x'], lbox['y'], lbox['z'], lbox['size'])

def draw_buttons():
    glColor3f(0.0, 0.0, 1.0)
    draw_line(70, height - 40, 50, height - 40)
    draw_line(50, height - 40, 60, height - 50)
    draw_line(50, height - 40, 60, height - 30)
    if paused:
        glColor3f(0.0, 0.0, 1.0)
        left = width // 2 - 12
        right = width // 2 + 12
        top = height - 47
        bottom = height - 33
        mid_y = (top + bottom) // 2
        draw_line(left, top, right, mid_y)
        draw_line(right, mid_y, left, bottom)
        draw_line(left, bottom, left, top)
    else:
        glColor3f(0.0, 0.0, 1.0)
        draw_line(width // 2 - 10, height - 45, width // 2 - 10, height - 25)
        glColor3f(0.0, 0.0, 1.0)
        draw_line(width // 2 + 10, height - 45, width // 2 + 10, height - 25)
    glColor3f(1.0, 0.0, 0.0)
    draw_line(width - 70, height - 45, width - 50, height - 25)
    draw_line(width - 70, height - 25, width - 50, height - 45)

def check_collision():
    global GAME_RUNNING, camera_shake_duration, PLAYER_Y, player_lives, PLAYER_X, live_boxes, points, gold_star_collect, bird_kill_message_timer, is_falling, player_y_velocity
    player_size = 25
    collided_with_obstacle = False
    for obs in obstacles:
        distance_x = abs(PLAYER_X - obs['x'])
        distance_z = abs(PLAYER_Z - obs['z'])
        if obs['type'] == 'bird':
            distance_y = abs(PLAYER_Y - obs['y'])
            if distance_x < (player_size + obs['size']) / 2 and \
               distance_z < (player_size + obs['size']) / 2 and \
               distance_y < (player_size + obs['size']) / 2:
                points = max(0, points - 8)
                gold_star_collect = max(0, gold_star_collect - 3)
                bird_kill_message_timer = 2.0
                camera_shake_duration = 0.75
            near_miss_distance = (player_size + obs['size']) * 1.25
            if distance_x < near_miss_distance and \
               distance_z < near_miss_distance and \
               distance_y < near_miss_distance and \
               not (distance_x < (player_size + obs['size']) / 2 and distance_z < (player_size + obs['size']) / 2 and distance_y < (player_size + obs['size']) / 2):
                camera_shake_duration = 0.5
        else:
            distance_y = abs(PLAYER_Y - obs['y'])
            if distance_x < (player_size + obs['size']) / 2 and \
               distance_z < (player_size + obs['size']) / 2 and \
               distance_y < (player_size + obs['size']) / 2:
                collided_with_obstacle = True
                camera_shake_duration = 0.75
                break
            near_miss_distance_horizontal = (player_size + obs['size']) * 0.8
            near_miss_distance_vertical = (player_size + obs['size']) * 0.8
            if distance_x < near_miss_distance_horizontal and \
               distance_z < near_miss_distance_horizontal and \
               distance_y < near_miss_distance_vertical and \
               not (distance_x < (player_size + obs['size']) / 2 and distance_z < (player_size + obs['size']) / 2 and distance_y < (player_size + obs['size']) / 2):
                camera_shake_duration = 0.75
    if collided_with_obstacle:
        player_lives -= 1
        if player_lives <= 0:
            GAME_RUNNING = False
            is_falling = True
            player_y_velocity = 0
        else:
            PLAYER_X = 0
            PLAYER_Y = 3
            player_y_velocity = 0
    new_live_boxes = []
    for lbox in live_boxes:
        distance_x = abs(PLAYER_X - lbox['x'])
        distance_z = abs(PLAYER_Z - lbox['z'])
        distance_y = abs(PLAYER_Y - lbox['y'])
        if distance_x < (player_size + lbox['size']) / 2 and \
           distance_z < (player_size + lbox['size']) / 2 and \
           distance_y < (player_size + lbox['size']) / 2:
            player_lives += 1
        else:
            new_live_boxes.append(lbox)
    live_boxes[:] = new_live_boxes

def check_gold_star_collision():
    global gold_star_collect, PLAYER_Y, difficulty_multiplier, pink_gold_stars, boost_active
    player_size = 25
    new_stars = []
    for star in gold_stars:
        distance_x = abs(PLAYER_X - star['x'])
        distance_z = abs(PLAYER_Z - star['z'])
        distance_y = abs(PLAYER_Y - (star['y'] + 15))
        if distance_x < (player_size + star['size']) / 2 and \
           distance_z < (player_size + star['size']) / 2 and \
           distance_y < (player_size + star['size']) / 2:
            gold_star_collect += 3 if boost_active else 1
            if gold_star_collect > 0 and gold_star_collect % 10 == 0:
                difficulty_multiplier += 0.2
                print(f"Difficulty Increased! Multiplier: {difficulty_multiplier}")
            if gold_star_collect % 5 == 0 and not pink_gold_stars:
                x = random.uniform(-GRID_WIDTH / 2, GRID_WIDTH / 2)
                z = random.uniform(-GRID_LENGTH, -GRID_LENGTH / 2)
                y = random.uniform(20, 30)
                overlap = False
                for obs in obstacles + gold_stars + live_boxes:
                    distance_x = abs(x - obs['x'])
                    distance_z = abs(z - obs['z'])
                    if distance_x < 30 and distance_z < 30:
                        if 'y' in obs and obs.get('type') == 'bird':
                            distance_y = abs(y - obs['y'])
                            if distance_y < (obs['size'] + 15):
                                overlap = True
                                break
                        else:
                            overlap = True
                            break
                if not overlap:
                    pink_gold_stars.append({'x': x, 'y': y, 'z': z, 'size': 15})
        else:
            new_stars.append(star)
    return new_stars

def check_pink_gold_star_collision():
    global boosts_available, PLAYER_Y
    player_size = 25
    new_stars = []
    for star in pink_gold_stars:
        distance_x = abs(PLAYER_X - star['x'])
        distance_z = abs(PLAYER_Z - star['z'])
        distance_y = abs(PLAYER_Y - (star['y'] + 15))
        if distance_x < (player_size + star['size']) / 2 and \
           distance_z < (player_size + star['size']) / 2 and \
           distance_y < (player_size + star['size']) / 2:
            boosts_available += 1
        else:
            new_stars.append(star)
    return new_stars

def update_points(current_time):
    global points, last_point_time
    if current_time - last_point_time >= point_interval:
        points_to_add = min(5, 1 + int(points / 100))
        points_to_add *= BOOST_MULTIPLIER if boost_active else 1
        points += points_to_add
        last_point_time = current_time

def setup_camera():
    global camera_pos, base_camera_pos, camera_shake_duration, camera_shake_intensity, view_mode, zoom_level
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, width / height, 0.1, 3000)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    if view_mode == 'third_person':
        current_camera_pos = [base_camera_pos[0], base_camera_pos[1], base_camera_pos[2] * zoom_level]
        if camera_shake_duration > 0:
            shake_x = random.uniform(-camera_shake_intensity, camera_shake_intensity)
            shake_y = random.uniform(-camera_shake_intensity, camera_shake_intensity)
            shake_z = random.uniform(-camera_shake_intensity, camera_shake_intensity)
            current_camera_pos[0] += shake_x
            current_camera_pos[1] += shake_y
            current_camera_pos[2] += shake_z
        gluLookAt(current_camera_pos[0], current_camera_pos[1], current_camera_pos[2], 0, 0, 0, 0, 1, 0)
    else:
        camera_x = PLAYER_X
        camera_y = PLAYER_Y + 30
        camera_z = PLAYER_Z
        look_x = PLAYER_X
        look_y = PLAYER_Y + 30
        look_z = PLAYER_Z - 100 * zoom_level
        if camera_shake_duration > 0:
            shake_x = random.uniform(-camera_shake_intensity, camera_shake_intensity)
            shake_y = random.uniform(-camera_shake_intensity, camera_shake_intensity)
            shake_z = random.uniform(-camera_shake_intensity, camera_shake_intensity)
            camera_x += shake_x
            camera_y += shake_y
            camera_z += shake_z
        gluLookAt(camera_x, camera_y, camera_z, look_x, look_y, look_z, 0, 1, 0)

def display():
    global is_falling, fall_duration
    glClear(GL_COLOR_BUFFER_BIT)
    glClearColor(0.5, 0.7, 1.0, 1.0)
    setup_camera()
    glEnable(GL_FOG)
    glFogi(GL_FOG_MODE, GL_LINEAR)
    glFogfv(GL_FOG_COLOR, (0.5, 0.7, 1.0, 1.0))
    glFogf(GL_FOG_DENSITY, 0.001)
    glFogf(GL_FOG_START, 500.0)
    glFogf(GL_FOG_END, 1500.0)
    # Collect renderable objects with their z-coordinates
    render_objects = []
    # Ground (render first, farthest)
    render_objects.append({'z': GRID_LENGTH, 'render': lambda: draw_ground(), 'transparent': False})
    # Opaque objects
    for obs in obstacles:
        render_objects.append({'z': obs['z'], 'render': lambda o=obs: draw_obstacle(o), 'transparent': False})
    for star in gold_stars:
        render_objects.append({'z': star['z'], 'render': lambda s=star: draw_gold_star_wrapper(s), 'transparent': False})
    for star in pink_gold_stars:
        render_objects.append({'z': star['z'], 'render': lambda s=star: draw_pink_gold_star_wrapper(s), 'transparent': False})
    for lbox in live_boxes:
        render_objects.append({'z': lbox['z'], 'render': lambda lb=lbox: draw_live_box_wrapper(lb), 'transparent': False})
    if view_mode == 'third_person':
        render_objects.append({'z': PLAYER_Z, 'render': lambda: draw_snowboarder(PLAYER_X, PLAYER_Z, minimal=False), 'transparent': False})
    else:
        render_objects.append({'z': PLAYER_Z, 'render': lambda: draw_snowboarder(PLAYER_X, PLAYER_Z, minimal=True), 'transparent': False})
    # Tracks (transparent, render last)
    for track in tracks:
        render_objects.append({'z': track['z'], 'render': lambda: draw_tracks(), 'transparent': True})
    # Sort objects: opaque first (farthest to nearest), then transparent (farthest to nearest)
    opaque_objects = [obj for obj in render_objects if not obj['transparent']]
    transparent_objects = [obj for obj in render_objects if obj['transparent']]
    opaque_objects.sort(key=lambda x: x['z'], reverse=True)
    transparent_objects.sort(key=lambda x: x['z'], reverse=True)
    sorted_objects = opaque_objects + transparent_objects
    # Render sorted objects
    for obj in sorted_objects:
        obj['render']()
    glDisable(GL_FOG)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, width, 0, height, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    draw_buttons()
    glColor3f(1.0, 1.0, 1.0)
    draw_text(10, height - 70, f"Points: {points}", GLUT_BITMAP_HELVETICA_18)
    draw_text(10, height - 100, f"Stars: {gold_star_collect}", GLUT_BITMAP_HELVETICA_18)
    glColor3f(0.0, 1.0, 0.0)
    draw_text(10, height - 130, f"Lives: {player_lives}", GLUT_BITMAP_HELVETICA_18)
    glColor3f(1.0, 0.5, 0.75)
    draw_text(10, height - 160, f"Boosts: {boosts_available}", GLUT_BITMAP_HELVETICA_18)
    if bird_kill_message_timer > 0:
        glColor3f(1.0, 0.0, 0.0)
        draw_text(width // 2 - 60, height // 2 + 40, "You hit a bird!", GLUT_BITMAP_HELVETICA_18)
    if not GAME_RUNNING and not is_falling:
        glColor3f(1.0, 0.0, 0.0)
        draw_text(width // 2 - 50, height // 2 + 10, "Game Over", GLUT_BITMAP_HELVETICA_18)
        glColor3f(1.0, 0.0, 0.0)
        draw_text(width // 2 - 70, height // 2 - 10, "Press R to Restart", GLUT_BITMAP_HELVETICA_18)
        glColor3f(1.0, 0.5, 0.0)
        draw_text(width // 2 - 80, height // 2 - 40, f"Game Score: {points}", GLUT_BITMAP_HELVETICA_18)
        draw_text(width // 2 - 90, height // 2 - 70, f"Gold Collected: {gold_star_collect}", GLUT_BITMAP_HELVETICA_18)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glutSwapBuffers()

def idle():
    global obstacles, gold_stars, pink_gold_stars, GAME_RUNNING, obstacle_speed, camera_shake_duration, PLAYER_Y, player_y_velocity, gravity, live_boxes, gold_star_collect, STEP_SIZE, difficulty_multiplier, BASE_STEP_SIZE, base_obstacle_speed, boost_active, boost_start_time, tracks, last_bird_move_time, bird_kill_message_timer, player_rotation, is_spinning, is_falling, fall_duration, is_laid_down
    current_time = time.time()
    delta_time = current_time - (idle.last_time if hasattr(idle, 'last_time') else current_time)
    idle.last_time = current_time
    if not GAME_RUNNING and not is_falling and not paused:
        glutPostRedisplay()
        return
    if is_falling:
        fall_duration += delta_time
        player_y_velocity += gravity * delta_time * 60
        PLAYER_Y += player_y_velocity * delta_time * 60
        if PLAYER_Y <= -2 or fall_duration >= MAX_FALL_DURATION:
            is_falling = False
            is_laid_down = True
            PLAYER_Y = -2
            player_y_velocity = 0
            fall_duration = 0.0
            glutPostRedisplay()
        glutPostRedisplay()
        return
    if paused:
        glutPostRedisplay()
        return
    if camera_shake_duration > 0:
        camera_shake_duration -= delta_time
        if camera_shake_duration < 0:
            camera_shake_duration = 0
    if bird_kill_message_timer > 0:
        bird_kill_message_timer -= delta_time
        if bird_kill_message_timer < 0:
            bird_kill_message_timer = 0
    if boost_active and current_time - boost_start_time >= BOOST_DURATION:
        boost_active = False
    player_y_velocity += gravity * delta_time * 60
    PLAYER_Y += player_y_velocity * delta_time * 60
    if PLAYER_Y < 3:
        PLAYER_Y = 3
        player_y_velocity = 0
        if is_spinning:
            is_spinning = False
            player_rotation = 0.0
    if is_spinning:
        player_rotation += spin_speed * delta_time
        player_rotation %= 360
    STEP_SIZE = BASE_STEP_SIZE * difficulty_multiplier
    obstacle_speed = base_obstacle_speed * difficulty_multiplier * (BOOST_MULTIPLIER if boost_active else 1.0)
    new_obstacles = []
    for obs in obstacles:
        obs['z'] += obstacle_speed * delta_time * 60
        if obs['type'] == 'bird' and current_time - last_bird_move_time >= 2.0:
            obs['x'] = random.uniform(-GRID_WIDTH / 2, GRID_WIDTH / 2)
            obs['y'] = random.uniform(20, 100)
            last_bird_move_time = current_time
        if obs['z'] < GRID_LENGTH:
            new_obstacles.append(obs)
    obstacles = new_obstacles
    new_stars = []
    for star in gold_stars:
        star['z'] += obstacle_speed * delta_time * 60
        if star['z'] < GRID_LENGTH:
            new_stars.append(star)
    gold_stars[:] = new_stars
    new_pink_stars = []
    for star in pink_gold_stars:
        star['z'] += obstacle_speed * delta_time * 60
        if star['z'] < GRID_LENGTH:
            new_pink_stars.append(star)
    pink_gold_stars[:] = new_pink_stars
    new_live_boxes = []
    for lbox in live_boxes:
        lbox['z'] += obstacle_speed * delta_time * 60
        if lbox['z'] < GRID_LENGTH:
            new_live_boxes.append(lbox)
    live_boxes[:] = new_live_boxes
    new_tracks = []
    for track in tracks:
        track['z'] += obstacle_speed * delta_time * 60
        if track['z'] < GRID_LENGTH:
            new_tracks.append(track)
    tracks[:] = new_tracks
    if PLAYER_Y == 3:
        tracks.append({'x': PLAYER_X, 'z': PLAYER_Z + 50})
    if gold_star_collect > 0 and gold_star_collect % 10 == 0 and not live_boxes:
        x = random.uniform(-GRID_WIDTH / 2, GRID_WIDTH / 2)
        z = random.uniform(-GRID_LENGTH, -GRID_LENGTH / 2)
        y = 15
        overlap = False
        for obs in obstacles + gold_stars + pink_gold_stars:
            distance_x = abs(x - obs['x'])
            distance_z = abs(z - obs['z'])
            if distance_x < 30 and distance_z < 30:
                overlap = True
                break
        if not overlap:
            live_boxes.append({'type': 'live_box', 'x': x, 'y': y, 'z': z, 'size': 15})
    gold_stars[:] = check_gold_star_collision()
    pink_gold_stars[:] = check_pink_gold_star_collision()
    create_obstacles()
    create_gold_stars()
    check_collision()
    update_points(current_time)
    glutPostRedisplay()

def keyboard(key, x, y):
    global GAME_RUNNING, points, gold_star_collect, boosts_available, PLAYER_X, obstacles, gold_stars, pink_gold_stars, paused, camera_shake_duration, obstacle_speed, PLAYER_Y, player_y_velocity, jump_strength, player_lives, live_boxes, difficulty_multiplier, STEP_SIZE, base_obstacle_speed, BASE_STEP_SIZE, boost_active, boost_start_time, tracks, view_mode, is_spinning, player_rotation, zoom_level, is_falling, fall_duration, is_laid_down
    if key == b'\x1b':
        sys.exit()
    elif key in (b'r', b'R') and not GAME_RUNNING:
        GAME_RUNNING = True
        paused = False
        PLAYER_X = 0
        PLAYER_Y = 3
        player_y_velocity = 0
        points = 0
        gold_star_collect = 0
        boosts_available = 0
        player_lives = 1
        obstacles.clear()
        gold_stars.clear()
        pink_gold_stars.clear()
        live_boxes.clear()
        tracks.clear()
        difficulty_multiplier = 1.0
        STEP_SIZE = BASE_STEP_SIZE
        obstacle_speed = base_obstacle_speed
        camera_shake_duration = 0
        boost_active = False
        boost_start_time = 0
        view_mode = 'third_person'
        player_rotation = 0.0
        is_spinning = False
        zoom_level = 1.0
        is_falling = False
        fall_duration = 0.0
        is_laid_down = False
    elif key == b' ':
        if GAME_RUNNING and not paused and PLAYER_Y < 3.01:
            player_y_velocity = jump_strength
            is_spinning = True
            player_rotation = 0.0
    elif key == b'b' and GAME_RUNNING and not paused and boosts_available >= 1 and not boost_active:
        boost_active = True
        boosts_available -= 1
        boost_start_time = time.time()
    elif key == b'c' and GAME_RUNNING and not paused:
        view_mode = 'first_person' if view_mode == 'third_person' else 'third_person'
    elif key == b'q' and GAME_RUNNING and not paused:
        zoom_level = max(MIN_ZOOM, zoom_level - ZOOM_STEP)
    elif key == b'e' and GAME_RUNNING and not paused:
        zoom_level = min(MAX_ZOOM, zoom_level + ZOOM_STEP)

def special_key_down(key, x, y):
    global PLAYER_X, STEP_SIZE
    if not GAME_RUNNING or paused:
        return
    if key == GLUT_KEY_LEFT:
        PLAYER_X = max(PLAYER_X - STEP_SIZE, -GRID_WIDTH / 2)
    elif key == GLUT_KEY_RIGHT:
        PLAYER_X = min(PLAYER_X + STEP_SIZE, GRID_WIDTH / 2)
    glutPostRedisplay()

def mouse_click(button, state, x, y):
    global GAME_RUNNING, paused, PLAYER_X, points, gold_star_collect, boosts_available, obstacles, gold_stars, pink_gold_stars, camera_shake_duration, obstacle_speed, PLAYER_Y, player_y_velocity, player_lives, live_boxes, difficulty_multiplier, STEP_SIZE, base_obstacle_speed, BASE_STEP_SIZE, boost_active, boost_start_time, tracks, zoom_level, is_falling, fall_duration, is_laid_down
    y = height - y
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if 50 <= x <= 70 and height - 50 <= y <= height - 30:
            GAME_RUNNING = True
            paused = False
            PLAYER_X = 0
            PLAYER_Y = 3
            player_y_velocity = 0
            points = 0
            gold_star_collect = 0
            boosts_available = 0
            player_lives = 1
            obstacles.clear()
            gold_stars.clear()
            pink_gold_stars.clear()
            live_boxes.clear()
            tracks.clear()
            difficulty_multiplier = 1.0
            STEP_SIZE = BASE_STEP_SIZE
            obstacle_speed = base_obstacle_speed
            camera_shake_duration = 0
            boost_active = False
            boost_start_time = 0
            zoom_level = 1.0
            is_falling = False
            fall_duration = 0.0
            is_laid_down = False
        elif width // 2 - 12 <= x <= width // 2 + 12 and height - 47 <= y <= height - 25:
            paused = not paused
        elif width - 70 <= x <= width - 50 and height - 45 <= y <= height - 25:
            glutDestroyWindow(glutGetWindow())
            sys.exit()
    glutPostRedisplay()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Snowboard Rush - Endless Runner")
    glClearColor(0.5, 0.7, 1.0, 1.0)
    glutDisplayFunc(display)
    glutIdleFunc(idle)
    glutSpecialFunc(special_key_down)
    glutKeyboardFunc(keyboard)
    glutMouseFunc(mouse_click)
    glutMainLoop()

if __name__ == "__main__":
    import sys
    main()