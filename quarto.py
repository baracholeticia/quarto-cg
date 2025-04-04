from OpenGL.GL import *
from textura import Textura
from skybox import Skybox
from ventilador import Ventilador

class Quarto:
    def __init__(self):
        self.width = 8.0
        self.height = 3.0
        self.depth = 8.0

        self.door_width = 1.0
        self.door_height = 2.25
        self.door_thickness = 0.05
        self.door_pos_x = -self.door_width/2
        self.wall_thickness = 0.2

        self.floor_color = (0.5, 0.4, 0.3)
        self.ceiling_color = (0.6,0.6,0.6)
        self.wall_color = (0.7, 0.7, 0.7)
        self.door_color = (0.4,0.3,0.2)

        self.textures = {
            'floor': Textura.load_texture("textures/piso.png"),
            'wall': Textura.load_texture("textures/parede.jpg"),
            'door': Textura.load_texture("textures/porta.jpg")
        }

        self.skybox = Skybox()
        self.skybox.load_texture("textures/skybox.jpg")

        self.door_angle = 0
        self.door_opening = False
        self.door_target_angle = 0

        self.fan = Ventilador()

    def draw_textured(self, texture_key, vertices, tex_coords, color):
        if self.textures.get(texture_key):
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.textures[texture_key])
            glColor3f(1, 1, 1)
        else:
            glDisable(GL_TEXTURE_2D)
            glColor3f(*color)

        glBegin(GL_QUADS)
        for i in range(4):
            glTexCoord2f(*tex_coords[i])
            glVertex3f(*vertices[i])
        glEnd()
        glDisable(GL_TEXTURE_2D)

    def draw_floor(self):
        vertices = [
            (-self.width / 2, 0.0, -self.depth / 2),
            (self.width / 2, 0.0, -self.depth / 2),
            (self.width / 2, 0.0, self.depth / 2),
            (-self.width / 2, 0.0, self.depth / 2)
        ]
        tex_coords = [(0, 0), (1, 0), (1, 1), (0, 1)]
        self.draw_textured('floor', vertices, tex_coords, self.floor_color)

    def draw_ceiling(self):
        vertices = [
            (-self.width / 2, self.height, -self.depth / 2),
            (self.width / 2, self.height, -self.depth / 2),
            (self.width / 2, self.height, self.depth / 2),
            (-self.width / 2, self.height, self.depth / 2)
        ]
        tex_coords = [(0, 0), (1, 0), (1, 1), (0, 1)]
        self.draw_textured('ceiling', vertices, tex_coords, self.ceiling_color)

    def draw_walls(self):
        tex_coords = [(0, 0), (1, 0), (1, 1), (0, 1)]

        # parede de tras
        vertices_back_left = [
            (-self.width / 2, 0.0, self.depth / 2),
            (self.door_pos_x, 0.0, self.depth / 2),
            (self.door_pos_x, self.height, self.depth / 2),
            (-self.width / 2, self.height, self.depth / 2)
        ]
        self.draw_textured('wall', vertices_back_left, tex_coords, self.wall_color)

        vertices_back_right = [
            (self.door_pos_x + self.door_width, 0.0, self.depth / 2),
            (self.width / 2, 0.0, self.depth / 2),
            (self.width / 2, self.height, self.depth / 2),
            (self.door_pos_x + self.door_width, self.height, self.depth / 2)
        ]
        self.draw_textured('wall', vertices_back_right, tex_coords, self.wall_color)

        vertices_back_top = [
            (self.door_pos_x, self.door_height, self.depth / 2),
            (self.door_pos_x + self.door_width, self.door_height, self.depth / 2),
            (self.door_pos_x + self.door_width, self.height, self.depth / 2),
            (self.door_pos_x, self.height, self.depth / 2)
        ]
        self.draw_textured('wall', vertices_back_top, tex_coords, self.wall_color)

        # parede da frente
        vertices_front = [
            (-self.width / 2, 0.0, -self.depth / 2),
            (self.width / 2, 0.0, -self.depth / 2),
            (self.width / 2, self.height, -self.depth / 2),
            (-self.width / 2, self.height, -self.depth / 2)
        ]
        self.draw_textured('wall', vertices_front, tex_coords, self.wall_color)

        # parede esquerda
        vertices_left = [
            (-self.width / 2, 0.0, -self.depth / 2),
            (-self.width / 2, 0.0, self.depth / 2),
            (-self.width / 2, self.height, self.depth / 2),
            (-self.width / 2, self.height, -self.depth / 2)
        ]
        self.draw_textured('wall', vertices_left, tex_coords, self.wall_color)

        # parede direita
        vertices_right = [
            (self.width / 2, 0.0, -self.depth / 2),
            (self.width / 2, 0.0, self.depth / 2),
            (self.width / 2, self.height, self.depth / 2),
            (self.width / 2, self.height, -self.depth / 2)
        ]
        self.draw_textured('wall', vertices_right, tex_coords, self.wall_color)

    def draw_door(self):
        glPushMatrix()

        glTranslatef(self.door_pos_x + self.door_width, 0, self.depth / 2 - self.door_thickness)
        glRotatef(-self.door_angle, 0, 1, 0)
        glTranslate(-self.door_width, 0, 0)

        if self.textures.get('door'):
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.textures['door'])
            glColor3f(1, 1, 1)
        else:
            glDisable(GL_TEXTURE_2D)
            glColor3f(*self.door_color)

        glBegin(GL_QUADS)

        # frente
        glTexCoord2f(0, 0); glVertex3f(0, 0, 0)
        glTexCoord2f(1, 0); glVertex3f(self.door_width, 0, 0)
        glTexCoord2f(1, 1); glVertex3f(self.door_width, self.door_height, 0)
        glTexCoord2f(0, 1); glVertex3f(0, self.door_height, 0)

        # tras
        glTexCoord2f(0, 0); glVertex3f(0, 0, -self.door_thickness)
        glTexCoord2f(1, 0); glVertex3f(self.door_width, 0, -self.door_thickness)
        glTexCoord2f(1, 1); glVertex3f(self.door_width, self.door_height, -self.door_thickness)
        glTexCoord2f(0, 1); glVertex3f(0, self.door_height, -self.door_thickness)

        glColor3f(0.3, 0.2, 0.1)
        # lado direito
        glVertex3f(self.door_width, 0, 0)
        glVertex3f(self.door_width, self.door_height, 0)
        glVertex3f(self.door_width, self.door_height, -self.door_thickness)
        glVertex3f(self.door_width, 0, -self.door_thickness)
        # lado esquerdo
        glVertex3f(0, 0, 0)
        glVertex3f(0, self.door_height, 0)
        glVertex3f(0, self.door_height, -self.door_thickness)
        glVertex3f(0, 0, -self.door_thickness)
        # cima
        glVertex3f(0, self.door_height, 0)
        glVertex3f(self.door_width, self.door_height, 0)
        glVertex3f(self.door_width, self.door_height, -self.door_thickness)
        glVertex3f(0, self.door_height, -self.door_thickness)

        glEnd()
        glDisable(GL_TEXTURE_2D)
        glPopMatrix()

    def update_door(self, delta_time):
        if self.door_opening:
            speed = 90.0 * delta_time
            if self.door_angle < self.door_target_angle:
                self.door_angle = min(self.door_angle + speed, self.door_target_angle)
            else:
                self.door_angle = max(self.door_angle - speed, self.door_target_angle)

            if abs(self.door_angle - self.door_target_angle) < 0.1:
                self.door_opening = False

    def toggle_door(self):
        if self.door_target_angle == 0:
            self.door_target_angle = 90
        else:
            self.door_target_angle = 0
        self.door_opening = True

    def draw(self):
        self.draw_floor()
        self.draw_ceiling()
        self.draw_walls()
        self.draw_door()
        self.fan.draw()
        self.skybox.draw()

    def update(self, delta_time):
        self.update_door(delta_time)
        self.fan.update(delta_time)