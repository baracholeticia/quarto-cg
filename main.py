import glfw
from OpenGL.GL import *
from OpenGL.GLU import *

from camera import Camera
from quarto import Quarto
from ventilador import Ventilador
from textura import Textura


def main():
    if not glfw.init():
        return

    width, height = 1280, 720
    window = glfw.create_window(width, height, "teste cg", None, None)
    if not window:
        glfw.terminate()
        return


    glfw.make_context_current(window)
    camera = Camera(width, height)
    quarto = Quarto()
    glfw.set_key_callback(window, camera.key_callback)
    glfw.set_cursor_pos_callback(window, camera.mouse_callback)

    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)

    glEnable(GL_DEPTH_TEST)

    # Configuração de iluminação como no primeiro código
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_LIGHTING)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_NORMALIZE)

    # Material specular para todos os objetos
    glMaterialfv(GL_FRONT, GL_SPECULAR, [0.1, 0.1, 0.1, 1])

    # Luz ambiente global (mais clara que no segundo código)
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.8, 0.8, 0.8, 1])

    # Luz principal (LIGHT0) - similar ao primeiro código
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_SPECULAR, [0.7, 0.7, 0.7, 1])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.3, 0.3, 0.3, 1])
    glLightfv(GL_LIGHT0, GL_POSITION, [0, 7, 0, 1])  # Posição no teto

    # Configuração de materiais
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)

    # Configura o tempo para cálculo de movimento suave
    last_time = glfw.get_time()

    def framebuffer_size_callback(window, new_width, new_height):
        width, height = new_width, new_height
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, width / height, 0.1, 5000)
        glMatrixMode(GL_MODELVIEW)

    glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.2, 0.3, 0.3, 1.0)

    while not glfw.window_should_close(window):
        current_time = glfw.get_time()
        delta_time = current_time - last_time
        last_time = current_time

        # Verifica tecla P para a porta
        if glfw.get_key(window, glfw.KEY_P) == glfw.PRESS:
            quarto.toggle_door()

        # Verifica tecla V para o ventilador
        if glfw.get_key(window, glfw.KEY_V) == glfw.PRESS:
            quarto.fan.toggle()

        # Verifica tecla L para a luz
        if glfw.get_key(window, glfw.KEY_L) == glfw.PRESS:
            quarto.fan.toggle_light()

        glfw.poll_events()
        camera.process_input(window, delta_time)
        quarto.update(delta_time)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60, width / height, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

        camera.update_camera()
        quarto.draw()

        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == "__main__":
    main()