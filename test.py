import pygame

pygame.init()

canvas = pygame.display.set_mode((500,500))
pygame.display.set_caption("Testing...")

def draw_rect(canvas):
    pygame.draw.rect(canvas, (255,0,0), pygame.Rect(10,0,50,50))
    pygame.display.update()

while True:
    draw_rect(canvas)
