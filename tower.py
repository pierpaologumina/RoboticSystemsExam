import math

from block import *
from pose import Pose

from PyQt5.QtGui import QColor, QPen, QBrush, QPixmap
from PyQt5.QtCore import Qt

class Tower:

    def __init__(self, ui, _tower_pos):
        self.blocks = list()
        self.tower_pos = Pose(ui)
        self.tower_pos.set_pose(_tower_pos[0],_tower_pos[1],0)
        self.qt_color = Qt.magenta
        self.ui = ui

    def add_block_to_tower(self, block):
        if len(self.blocks) >= 3:
            print("Maximum tower size reached")
            return
        tower_x, tower_z = self.tower_pos.get_pose()

        block.set_pose(tower_x, tower_z)
        self.blocks.append(block)
        print("Numero blocchi inseriti: ",len(self.blocks))

    def get_tower_length(self):
        return len(self.blocks)
    
    def get_height(self):
        _, tower_z = self.tower_pos.get_pose()
        return tower_z + (self.get_tower_length() + 1) * Block.HEIGHT + Block.HEIGHT

    def release_tower(self):
        self.blocks.clear()

    def paint(self, qp, window_width, window_height):
        
        # Draw tower base
        qp.setPen(QPen(self.qt_color, 5, Qt.SolidLine))
        qp.setBrush(QColor(QBrush(self.qt_color, Qt.SolidPattern)))

        tower_pixel_x, tower_pixel_z = self.tower_pos.get_pose()

        qp.drawRect(tower_pixel_x,tower_pixel_z,100,10)
        qp.drawRect(tower_pixel_x+45,tower_pixel_z,10,500)

        # Draw tower blocks
        for b in self.blocks:
            b.paint(qp)
