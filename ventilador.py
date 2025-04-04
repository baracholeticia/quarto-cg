from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np


class Ventilador:
    def __init__(self):
        self.rotation_angle = 0.0
        self.rotation_speed = 2.0
        self.is_running = False
        self.light_on = True

        self.position = np.array([0.0, 3.0, 0.0])  # y=3.0 (altura do teto)

        self.light_id = GL_LIGHT1
        self.light_position = [0.0, 2.7, 0.0, 1.0]  # Posição ligeiramente abaixo
        self.light_diffuse = [1.0, 1.0, 1.0, 1.0]
        self.light_direction = [0.0, -1.0, 0.0]  # Apontando para baixo
        self.light_cutoff = 30.0  # Ângulo de abertura

        # Dimensões do ventilador
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

        # Substitui o cilindro por duas esferas como suporte
        glColor3f(0.3, 0.3, 0.3)
        # Esfera superior
        glPushMatrix()
        glTranslatef(0, -0.1, 0)
        self.draw_sphere(0.15, 20, 20)
        glPopMatrix()

        # Esfera inferior
        glPushMatrix()
        glTranslatef(0, -0.3, 0)
        self.draw_sphere(0.15, 20, 20)
        glPopMatrix()

        # Motor
        glPushMatrix()
        glTranslatef(0, -0.4, 0)
        glColor3f(0.5, 0.5, 0.5)
        self.draw_sphere(0.15, 20, 20)

        # Hélices
        glRotatef(self.rotation_angle, 0, 1, 0)
        glColor3f(0.7, 0.7, 0.7)

        # Ângulos das hélices usando numpy
        angles = np.arange(0, 360, 90)
        for angle in angles:
            glPushMatrix()
            glRotatef(angle, 0, 1, 0)
            self.draw_blade()
            glPopMatrix()

        # Lâmpada
        glPushMatrix()
        glTranslatef(0, -0.2, 0)
        glColor3f(1.0, 1.0, 0.8)
        self.draw_light_bulb()
        glPopMatrix()

        glPopMatrix()
        glPopMatrix()

        # Configura luz
        if self.light_on:
            glEnable(self.light_id)
            glLightfv(self.light_id, GL_POSITION, self.light_position)
            glLightfv(self.light_id, GL_DIFFUSE, self.light_diffuse)

            # Configura a luz como um spot
            glLightf(self.light_id, GL_SPOT_CUTOFF, self.light_cutoff)
            glLightfv(self.light_id, GL_SPOT_DIRECTION, self.light_direction)
            glLightf(self.light_id, GL_SPOT_EXPONENT, 2.0)

            # Atenuação
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
        # Vertices usando numpy
        vertices = np.array([
            # Face frontal
            [-0.75, -0.025, -0.05],
            [0.75, -0.025, -0.05],
            [0.75, 0.025, -0.05],
            [-0.75, 0.025, -0.05],
            # Face traseira
            [-0.75, -0.025, 0.05],
            [0.75, -0.025, 0.05],
            [0.75, 0.025, 0.05],
            [-0.75, 0.025, 0.05]
        ], dtype=np.float32)

        # Índices para desenhar quadrados
        indices = [
            [0, 1, 2, 3],  # Frente
            [4, 5, 6, 7],  # Trás
            [0, 3, 7, 4],  # Esquerda
            [1, 2, 6, 5],  # Direita
            [0, 1, 5, 4],  # Inferior
            [2, 3, 7, 6]  # Superior
        ]

        glBegin(GL_QUADS)
        for face in indices:
            for vertex in face:
                glVertex3fv(vertices[vertex])
        glEnd()

    def draw_light_bulb(self):
        # Usando gluSphere com escala para elipsoide
        glScalef(self.light_bulb_radius, self.light_bulb_height, self.light_bulb_radius)
        quadric = gluNewQuadric()
        gluSphere(quadric, 0.5, 20, 20)
        gluDeleteQuadric(quadric)