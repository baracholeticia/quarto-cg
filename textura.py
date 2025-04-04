from OpenGL.GL import *
from PIL import Image
import numpy as np


class Textura:

    def load_texture(image_path):

        img = Image.open(image_path)
        img = img.convert("RGB")
        img_data = np.array(img, dtype=np.uint8)

        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.width, img.height,0, GL_RGB, GL_UNSIGNED_BYTE, img_data)

        return texture_id