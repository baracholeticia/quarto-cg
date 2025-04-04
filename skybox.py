from OpenGL.GL import *
import numpy as np
from textura import Textura


class Skybox:
    def __init__(self, radius=80.0):
        self.radius = radius
        self.texture_id = None

    #funcao de carregamento porpria com modificacoes
    def load_texture(self, image_path):

        self.texture_id = Textura.load_texture(image_path)
        if self.texture_id:

            glBindTexture(GL_TEXTURE_2D, self.texture_id)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
            return True
        return False

    def draw(self):
        if not self.texture_id:
            return

        glPushMatrix()

        glDisable(GL_LIGHTING)
        glDepthMask(GL_FALSE)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)

        slices = 64
        stacks = 64

        for i in range(stacks):
            lat0 = np.pi * (-0.5 + (i / stacks))
            lat1 = np.pi * (-0.5 + ((i + 1) / stacks))

            glBegin(GL_QUAD_STRIP)
            for j in range(slices + 1):
                lng = 2 * np.pi * (j / slices)

                x0 = np.cos(lng) * np.cos(lat0)
                y0 = np.sin(lat0)
                z0 = np.sin(lng) * np.cos(lat0)

                x1 = np.cos(lng) * np.cos(lat1)
                y1 = np.sin(lat1)
                z1 = np.sin(lng) * np.cos(lat1)

                s = j / slices
                t0 = 1.0 - (i / stacks)
                t1 = 1.0 - ((i + 1) / stacks)

                glTexCoord2f(s, t0)
                glVertex3f(x0 * self.radius, y0 * self.radius, z0 * self.radius)
                glTexCoord2f(s, t1)
                glVertex3f(x1 * self.radius, y1 * self.radius, z1 * self.radius)
            glEnd()

        glDepthMask(GL_TRUE)
        glEnable(GL_LIGHTING)
        glDisable(GL_TEXTURE_2D)

        glPopMatrix()