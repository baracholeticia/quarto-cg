import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np


class Camera:
    def __init__(self, width, height):
        self.camera_pos = np.array([0.0, 1.7, 0.0]) #altura 1,70
        self.camera_front = np.array([0.0, 0.0, -1.0])
        self.camera_up = np.array([0.0, 1.0, 0.0])
        self.yaw, self.pitch = -90.0, 0.0

        self.camera_speed = 2.5
        self.mouse_sensitivity = 0.1
        self.keys = {}

        self.standing_height = 1.7
        self.crouching_height = 1.0
        self.is_crouching = False
        self.current_height = self.standing_height

        self.is_jumping = False
        self.jump_velocity = 0.0
        self.gravity = 9.8
        self.jump_strength = 3.5

        self.first_mouse = True
        self.cursor_disabled = True
        self.last_x, self.last_y = width / 2, height / 2
        self.esc_pressed = False

        self.world_limits = {
            'min_x': -3.9, 'max_x': 3.9,
            'min_y': 0.1, 'max_y': 2.9,
            'min_z': -3.9, 'max_z': 3.9
        }

    def update_camera(self):
        glLoadIdentity()
        camera_target = self.camera_pos + self.camera_front
        gluLookAt(self.camera_pos[0], self.camera_pos[1], self.camera_pos[2],camera_target[0], camera_target[1], camera_target[2], self.camera_up[0], self.camera_up[1], self.camera_up[2])

    def key_callback(self, window, key, scancode, action, mods):
        if action == glfw.PRESS:
            self.keys[key] = True

            if key == glfw.KEY_LEFT_SHIFT:
                self.is_crouching = True
                self.current_height = self.crouching_height
                if not self.is_jumping:
                    self.camera_pos[1] = self.current_height

            if key == glfw.KEY_SPACE and not self.is_jumping and not self.is_crouching:
                self.is_jumping = True
                self.jump_velocity = self.jump_strength

        elif action == glfw.RELEASE:
            self.keys[key] = False
            if key == glfw.KEY_LEFT_SHIFT:
                self.is_crouching = False
                self.current_height = self.standing_height
                if not self.is_jumping:
                    self.camera_pos[1] = self.current_height

        elif action == glfw.RELEASE:
            self.keys[key] = False

            if key == glfw.KEY_LEFT_SHIFT:
                self.is_crouching = False
                self.current_height = self.standing_height
                if not self.is_jumping:
                    self.camera_pos[1] = self.current_height

    def process_input(self, window, delta_time):
        velocity = self.camera_speed * delta_time


        if self.keys.get(glfw.KEY_W, False) or self.keys.get(glfw.KEY_S, False) or self.keys.get(glfw.KEY_A, False) or self.keys.get(glfw.KEY_D, False):

            move_direction = np.array([0.0, 0.0, 0.0])

            if self.keys.get(glfw.KEY_W, False):
                front = self.camera_front.copy()
                front[1] = 0
                front = front / np.linalg.norm(front)
                move_direction += front

            if self.keys.get(glfw.KEY_S, False):
                front = self.camera_front.copy()
                front[1] = 0
                front = front / np.linalg.norm(front)
                move_direction -= front

            if self.keys.get(glfw.KEY_A, False):
                right = np.cross(self.camera_front, self.camera_up)
                right[1] = 0
                right = right / np.linalg.norm(right)
                move_direction -= right

            if self.keys.get(glfw.KEY_D, False):
                right = np.cross(self.camera_front, self.camera_up)
                right[1] = 0
                right = right / np.linalg.norm(right)
                move_direction += right

            #anda mais devagar abaixado
            current_speed = velocity * 0.6 if self.is_crouching else velocity

            new_pos = self.camera_pos + current_speed * move_direction
            new_pos[1] = self.camera_pos[1]

            if self.check_bounds(new_pos):
                self.camera_pos[0] = new_pos[0]
                self.camera_pos[2] = new_pos[2]

        #sistema do pulo
        if self.is_jumping:
            self.jump_velocity -= self.gravity * delta_time
            self.camera_pos[1] += self.jump_velocity * delta_time

            if self.camera_pos[1] <= self.current_height:
                self.camera_pos[1] = self.current_height
                self.is_jumping = False
                self.jump_velocity = 0.0

        elif not self.is_crouching and self.camera_pos[1] < self.current_height:
            self.camera_pos[1] += 0.1
            if self.camera_pos[1] > self.current_height:
                self.camera_pos[1] = self.current_height

        #mouse (esc pra mudar)
        if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS and not self.esc_pressed:
            self.cursor_disabled = not self.cursor_disabled
            mode = glfw.CURSOR_DISABLED if self.cursor_disabled else glfw.CURSOR_NORMAL
            glfw.set_input_mode(window, glfw.CURSOR, mode)
            self.esc_pressed = True
            self.first_mouse = self.cursor_disabled
        elif glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.RELEASE:
            self.esc_pressed = False

    def check_bounds(self, position):
        return (self.world_limits['min_x'] <= position[0] <= self.world_limits['max_x'] and
                self.world_limits['min_y'] <= position[1] <= self.world_limits['max_y'] and
                self.world_limits['min_z'] <= position[2] <= self.world_limits['max_z'])

    def mouse_callback(self, window, xpos, ypos):
        if not self.cursor_disabled:
            return

        if self.first_mouse:
            self.last_x = xpos
            self.last_y = ypos
            self.first_mouse = False

        xoffset = xpos - self.last_x
        yoffset = self.last_y - ypos
        self.last_x = xpos
        self.last_y = ypos

        xoffset *= self.mouse_sensitivity
        yoffset *= self.mouse_sensitivity

        self.yaw += xoffset
        self.pitch += yoffset

        if self.pitch > 89.0:
            self.pitch = 89.0
        if self.pitch < -89.0:
            self.pitch = -89.0

        front = np.array([
            np.cos(np.radians(self.yaw)) * np.cos(np.radians(self.pitch)),
            np.sin(np.radians(self.pitch)),
            np.sin(np.radians(self.yaw)) * np.cos(np.radians(self.pitch))
        ])
        self.camera_front = front / np.linalg.norm(front)
