from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np


class Ventilador:
    def __init__(self):
        self.rotation_angle = 0.0
        self.rotation_speed = 2.0
        self.is_running = False
        self.light_on = True

        self.position = [0.0, 3.0, 0.0]

        self.light_id = GL_LIGHT1
        self.light_position = [0.0, 2.7, 0.0, 1.0]
        self.light_diffuse = [1.0, 1.0, 1.0, 1.0]
        self.light_direction = [0.0, -1.0, 0.0]
        self.light_cutoff = 30.0

        self.light_bulb_radius = 0.3
        self.light_bulb_height = 0.4


    def toggle(self):
        self.is_running = not self.is_running

    def toggle_light(self):
        self.light_on = not self.light_on
        if self.light_on:
            glEnable(self.light_id)
        else:
            glDisable(self.light_id)

    def update(self, delta_time):
        if self.is_running:
            self.rotation_angle += self.rotation_speed * delta_time * 60
            self.rotation_angle %= 360

    def draw(self):
        glPushMatrix()
        glTranslatef(*self.position)

        glColor3f(0.3, 0.3, 0.3)

        glPushMatrix()
        glTranslatef(0, -0.1, 0)
        self.draw_sphere(0.15, 20, 20)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(0, -0.3, 0)
        self.draw_sphere(0.15, 20, 20)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(0, -0.4, 0)
        glColor3f(0.5, 0.5, 0.5)
        self.draw_sphere(0.15, 20, 20)

        #helices
        glRotatef(self.rotation_angle, 0, 1, 0)
        glColor3f(0.7, 0.7, 0.7)

        angles = np.arange(0, 360, 90)
        for angle in angles:
            glPushMatrix()
            glRotatef(angle, 0, 1, 0)
            self.draw_blade()
            glPopMatrix()

        #luz
        glPushMatrix()
        glTranslatef(0, -0.2, 0)
        glColor3f(1.0, 1.0, 0.8)
        self.draw_light_bulb()
        glPopMatrix()

        glPopMatrix()
        glPopMatrix()

        if self.light_on:
            glEnable(self.light_id)
            glLightfv(self.light_id, GL_POSITION, self.light_position)
            glLightfv(self.light_id, GL_DIFFUSE, self.light_diffuse)

            glLightf(self.light_id, GL_SPOT_CUTOFF, self.light_cutoff)
            glLightfv(self.light_id, GL_SPOT_DIRECTION, self.light_direction)
            glLightf(self.light_id, GL_SPOT_EXPONENT, 2.0)

            glLightf(self.light_id, GL_CONSTANT_ATTENUATION, 1.0)
            glLightf(self.light_id, GL_LINEAR_ATTENUATION, 0.05)
            glLightf(self.light_id, GL_QUADRATIC_ATTENUATION, 0.01)
        else:
            glDisable(self.light_id)

    def draw_sphere(self, radius, slices, stacks):
        quadric = gluNewQuadric()
        gluSphere(quadric, radius, slices, stacks)
        gluDeleteQuadric(quadric)

    def draw_blade(self):

        vertices = [
            [-0.75, -0.025, -0.05],
            [0.75, -0.025, -0.05],
            [0.75, 0.025, -0.05],
            [-0.75, 0.025, -0.05],

            [-0.75, -0.025, 0.05],
            [0.75, -0.025, 0.05],
            [0.75, 0.025, 0.05],
            [-0.75, 0.025, 0.05]
        ]

        indices = [
            [0, 1, 2, 3],  # frente
            [4, 5, 6, 7],  # tras
            [0, 3, 7, 4],  # esq
            [1, 2, 6, 5],  # dir
            [0, 1, 5, 4],  # inf
            [2, 3, 7, 6]  # sup
        ]

        glBegin(GL_QUADS)
        for face in indices:
            for vertex in face:
                glVertex3fv(vertices[vertex])
        glEnd()

    def draw_light_bulb(self):

        glScalef(self.light_bulb_radius, self.light_bulb_height, self.light_bulb_radius)
        quadric = gluNewQuadric()
        gluSphere(quadric, 0.5, 20, 20)
        gluDeleteQuadric(quadric)