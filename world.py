import math

from block import *
from tower import *
from utilities import *

from PyQt5.QtGui import QColor, QPen, QBrush, QPixmap
from PyQt5.QtCore import Qt

class World:

    def paintObstacles(self,painter,obstacle):
        painter.drawPixmap(90,350,80,80,obstacle)        
        painter.drawPixmap(400,250,80,80,obstacle)
        #painter.drawPixmap(550,150,80,80,obstacle)
        painter.drawPixmap(850,80,80,80,obstacle)        
        painter.drawPixmap(750,450,80,80,obstacle)

    def __init__(self, ui):
        self.__blocks = dict()
        self.block_slot_busy = dict()
        
       
       
        self.block_slot_nodes =	{
            #sotto
            "nodo_slot_A": (470,690),
            "nodo_slot_B": (370,690),
            "nodo_slot_C": (270,690),
            "nodo_slot_D": (170,690),
            "nodo_slot_E": (70,690),
            #sopra
            "nodo_slot_F": (470,180),
            "nodo_slot_G": (370,180),
            "nodo_slot_H": (270,180),
            "nodo_slot_I": (170,180),
            "nodo_slot_J": (70,180)
        }

        self.nodi =	{
            #sotto
            "nodo_slot_A": (470,630),
            "nodo_slot_B": (370,630),
            "nodo_slot_C": (270,630),
            "nodo_slot_D": (170,630),
            "nodo_slot_E": (70,630),
            #sopra
            "nodo_slot_F": (470,120),
            "nodo_slot_G": (370,120),
            "nodo_slot_H": (270,120),
            "nodo_slot_I": (170,120),
            "nodo_slot_J": (70,120),
            #altri
            "nodo_A": (580,70),
            "nodo_B": (730,120),
            "nodo_C": (700,330),
            "nodo_D": (900,330),
            "nodo_E": (470,500),
            "nodo_F": (600,530),
            "nodo_G": (900,600),
            "nodo_H": (1145,330),
            "nodo_target": (1145,450),
            "nodo_start": (640,655)
        }

        self.edge =	[]
        #archi del nodo "nodo_slot_A"
        self.edge.append(("nodo_slot_A","nodo_slot_B",int(math.ceil(distanceCouple(self.nodi["nodo_slot_A"],self.nodi["nodo_slot_B"])))))
        self.edge.append(("nodo_slot_A","nodo_E",int(math.ceil(distanceCouple(self.nodi["nodo_slot_A"],self.nodi["nodo_E"])))))
        #archi del nodo "nodo_slot_B"
        self.edge.append(("nodo_slot_B","nodo_slot_A",int(math.ceil(distanceCouple(self.nodi["nodo_slot_B"],self.nodi["nodo_slot_A"])))))
        self.edge.append(("nodo_slot_B","nodo_slot_C",int(math.ceil(distanceCouple(self.nodi["nodo_slot_B"],self.nodi["nodo_slot_C"])))))
        self.edge.append(("nodo_slot_B","nodo_E",int(math.ceil(distanceCouple(self.nodi["nodo_slot_B"],self.nodi["nodo_E"])))))
        #archi del nodo "nodo_slot_C"
        self.edge.append(("nodo_slot_C","nodo_slot_B",int(math.ceil(distanceCouple(self.nodi["nodo_slot_C"],self.nodi["nodo_slot_B"])))))
        self.edge.append(("nodo_slot_C","nodo_slot_D",int(math.ceil(distanceCouple(self.nodi["nodo_slot_C"],self.nodi["nodo_slot_D"])))))
        self.edge.append(("nodo_slot_C","nodo_E",int(math.ceil(distanceCouple(self.nodi["nodo_slot_C"],self.nodi["nodo_E"])))))
        #archi del nodo "nodo_slot_D"
        self.edge.append(("nodo_slot_D","nodo_slot_C",int(math.ceil(distanceCouple(self.nodi["nodo_slot_D"],self.nodi["nodo_slot_C"])))))
        self.edge.append(("nodo_slot_D","nodo_slot_E",int(math.ceil(distanceCouple(self.nodi["nodo_slot_D"],self.nodi["nodo_slot_E"])))))
        self.edge.append(("nodo_slot_D","nodo_E",int(math.ceil(distanceCouple(self.nodi["nodo_slot_D"],self.nodi["nodo_E"])))))
        #archi del nodo "nodo_slot_E"
        self.edge.append(("nodo_slot_E","nodo_slot_D",int(math.ceil(distanceCouple(self.nodi["nodo_slot_E"],self.nodi["nodo_slot_D"])))))
        self.edge.append(("nodo_slot_E","nodo_E",int(math.ceil(distanceCouple(self.nodi["nodo_slot_E"],self.nodi["nodo_E"])))))
        #archi del nodo "nodo_slot_F"
        self.edge.append(("nodo_slot_F","nodo_slot_G",int(math.ceil(distanceCouple(self.nodi["nodo_slot_F"],self.nodi["nodo_slot_G"])))))
        self.edge.append(("nodo_slot_F","nodo_A",int(math.ceil(distanceCouple(self.nodi["nodo_slot_F"],self.nodi["nodo_A"])))))
        #archi del nodo "nodo_slot_G"
        self.edge.append(("nodo_slot_G","nodo_slot_F",int(math.ceil(distanceCouple(self.nodi["nodo_slot_G"],self.nodi["nodo_slot_F"])))))
        self.edge.append(("nodo_slot_G","nodo_slot_H",int(math.ceil(distanceCouple(self.nodi["nodo_slot_G"],self.nodi["nodo_slot_H"])))))
        self.edge.append(("nodo_slot_G","nodo_A",int(math.ceil(distanceCouple(self.nodi["nodo_slot_G"],self.nodi["nodo_A"])))))
        #archi del nodo "nodo_slot_H"
        self.edge.append(("nodo_slot_H","nodo_slot_G",int(math.ceil(distanceCouple(self.nodi["nodo_slot_H"],self.nodi["nodo_slot_G"])))))
        self.edge.append(("nodo_slot_H","nodo_slot_I",int(math.ceil(distanceCouple(self.nodi["nodo_slot_H"],self.nodi["nodo_slot_I"])))))
        self.edge.append(("nodo_slot_H","nodo_A",int(math.ceil(distanceCouple(self.nodi["nodo_slot_H"],self.nodi["nodo_A"])))))
        #archi del nodo "nodo_slot_I"
        self.edge.append(("nodo_slot_I","nodo_slot_H",int(math.ceil(distanceCouple(self.nodi["nodo_slot_I"],self.nodi["nodo_slot_H"])))))
        self.edge.append(("nodo_slot_I","nodo_slot_J",int(math.ceil(distanceCouple(self.nodi["nodo_slot_I"],self.nodi["nodo_slot_J"])))))
        self.edge.append(("nodo_slot_I","nodo_A",int(math.ceil(distanceCouple(self.nodi["nodo_slot_I"],self.nodi["nodo_A"])))))
        #archi del nodo "nodo_slot_J"
        self.edge.append(("nodo_slot_J","nodo_slot_I",int(math.ceil(distanceCouple(self.nodi["nodo_slot_J"],self.nodi["nodo_slot_I"])))))
        self.edge.append(("nodo_slot_J","nodo_A",int(math.ceil(distanceCouple(self.nodi["nodo_slot_J"],self.nodi["nodo_A"])))))
        
        
        #archi del nodo "nodo_A"
        self.edge.append(("nodo_A","nodo_slot_F",int(math.ceil(distanceCouple(self.nodi["nodo_A"],self.nodi["nodo_slot_F"])))))
        self.edge.append(("nodo_A","nodo_slot_G",int(math.ceil(distanceCouple(self.nodi["nodo_A"],self.nodi["nodo_slot_G"])))))
        self.edge.append(("nodo_A","nodo_slot_H",int(math.ceil(distanceCouple(self.nodi["nodo_A"],self.nodi["nodo_slot_H"])))))
        self.edge.append(("nodo_A","nodo_slot_I",int(math.ceil(distanceCouple(self.nodi["nodo_A"],self.nodi["nodo_slot_I"])))))
        self.edge.append(("nodo_A","nodo_slot_J",int(math.ceil(distanceCouple(self.nodi["nodo_A"],self.nodi["nodo_slot_J"])))))
        self.edge.append(("nodo_A","nodo_B",int(math.ceil(distanceCouple(self.nodi["nodo_A"],self.nodi["nodo_B"])))))
        #archi del nodo "nodo_B"
        self.edge.append(("nodo_B","nodo_A",int(math.ceil(distanceCouple(self.nodi["nodo_B"],self.nodi["nodo_A"])))))
        self.edge.append(("nodo_B","nodo_C",int(math.ceil(distanceCouple(self.nodi["nodo_B"],self.nodi["nodo_C"])))))
        #archi del nodo "nodo_C"
        self.edge.append(("nodo_C","nodo_B",int(math.ceil(distanceCouple(self.nodi["nodo_C"],self.nodi["nodo_B"])))))
        self.edge.append(("nodo_C","nodo_D",int(math.ceil(distanceCouple(self.nodi["nodo_C"],self.nodi["nodo_D"])))))
        self.edge.append(("nodo_C","nodo_E",int(math.ceil(distanceCouple(self.nodi["nodo_C"],self.nodi["nodo_E"])))))
        self.edge.append(("nodo_C","nodo_F",int(math.ceil(distanceCouple(self.nodi["nodo_C"],self.nodi["nodo_F"])))))
        #archi del nodo "nodo_D"
        self.edge.append(("nodo_D","nodo_C",int(math.ceil(distanceCouple(self.nodi["nodo_D"],self.nodi["nodo_C"])))))
        self.edge.append(("nodo_D","nodo_G",int(math.ceil(distanceCouple(self.nodi["nodo_D"],self.nodi["nodo_G"])))))
        self.edge.append(("nodo_D","nodo_H",int(math.ceil(distanceCouple(self.nodi["nodo_D"],self.nodi["nodo_H"])))))
        #archi del nodo "nodo_E"
        self.edge.append(("nodo_E","nodo_slot_A",int(math.ceil(distanceCouple(self.nodi["nodo_E"],self.nodi["nodo_slot_A"])))))
        self.edge.append(("nodo_E","nodo_slot_B",int(math.ceil(distanceCouple(self.nodi["nodo_E"],self.nodi["nodo_slot_B"])))))
        self.edge.append(("nodo_E","nodo_slot_C",int(math.ceil(distanceCouple(self.nodi["nodo_E"],self.nodi["nodo_slot_C"])))))
        self.edge.append(("nodo_E","nodo_slot_D",int(math.ceil(distanceCouple(self.nodi["nodo_E"],self.nodi["nodo_slot_D"])))))
        self.edge.append(("nodo_E","nodo_slot_E",int(math.ceil(distanceCouple(self.nodi["nodo_E"],self.nodi["nodo_slot_E"])))))
        self.edge.append(("nodo_E","nodo_F",int(math.ceil(distanceCouple(self.nodi["nodo_E"],self.nodi["nodo_F"])))))
        self.edge.append(("nodo_E","nodo_C",int(math.ceil(distanceCouple(self.nodi["nodo_E"],self.nodi["nodo_C"])))))
        #archi del nodo "nodo_F"
        self.edge.append(("nodo_F","nodo_start",int(math.ceil(distanceCouple(self.nodi["nodo_F"],self.nodi["nodo_start"])))))
        self.edge.append(("nodo_F","nodo_E",int(math.ceil(distanceCouple(self.nodi["nodo_F"],self.nodi["nodo_E"])))))
        self.edge.append(("nodo_F","nodo_C",int(math.ceil(distanceCouple(self.nodi["nodo_F"],self.nodi["nodo_C"])))))
        #archi del nodo "nodo_G"
        self.edge.append(("nodo_G","nodo_start",int(math.ceil(distanceCouple(self.nodi["nodo_G"],self.nodi["nodo_start"])))))
        self.edge.append(("nodo_G","nodo_D",int(math.ceil(distanceCouple(self.nodi["nodo_G"],self.nodi["nodo_D"])))))
        #archi del nodo "nodo_H"
        self.edge.append(("nodo_H","nodo_target",int(math.ceil(distanceCouple(self.nodi["nodo_H"],self.nodi["nodo_target"])))))
        self.edge.append(("nodo_H","nodo_D",int(math.ceil(distanceCouple(self.nodi["nodo_H"],self.nodi["nodo_D"])))))
        #archi del nodo "nodo_start"
        self.edge.append(("nodo_start","nodo_G",int(math.ceil(distanceCouple(self.nodi["nodo_start"],self.nodi["nodo_G"])))))
        self.edge.append(("nodo_start","nodo_F",int(math.ceil(distanceCouple(self.nodi["nodo_start"],self.nodi["nodo_F"])))))
        #archi del nodo "nodo_target"
        self.edge.append(("nodo_target","nodo_H",int(math.ceil(distanceCouple(self.nodi["nodo_target"],self.nodi["nodo_H"])))))  

        for slot in self.block_slot_nodes:
            self.block_slot_busy[slot] = False
        self.ui = ui
        self.gordo = QPixmap("bomb.png")  # obstacle image
        self.start = QPixmap("start.png")  # start image
        self.towers = []
       
        # Initialize tower
        self.tower=Tower(ui, (1100,500))

    # Add block to world
    def new_block(self, uColor, node_slot):
        b = Block(uColor,self.ui)
        uXtmp, uZtmp = self.block_slot_nodes[node_slot]
        uX , uZ = pixel_to_meter(uXtmp, uZtmp,self.ui.width(),self.ui.height(),self.ui.autopilot.quadrotor.dronePix.height())
        b.set_pose(uX, uZ, 0)
        self.block_slot_busy[node_slot] = True
        self.__blocks[node_slot] = b
    
    def get_block(self,node_name):
        return self.__blocks[node_name]
    
    # Remove block from world
    def pop_block(self,node_name):
        self.block_slot_busy[node_name] = False
        out_block = self.__blocks.pop(node_name)
        return out_block

    def count_blocks(self):
        return len(self.__blocks)



    # Compute color of closest block
    def sense_color(self):
        robot_pose = self.ui.autopilot.quadrotor.get_pose_xz()
        min_dist = 1
        b_color = None
        for b in self.__blocks.values():
            b_pose = b.get_pose()
            dist = distanceCouple(b_pose, robot_pose)
            if dist < min_dist:
                min_dist = dist
                b_color = b.get_color()
        return b_color

    def paint(self, qp, window_width, window_height):
        qp.setPen(QPen(Qt.gray, 5, Qt.SolidLine))
        qp.setBrush(QColor(QBrush(Qt.red, Qt.SolidPattern)))
        
        qp.setBrush(QColor(QBrush(Qt.gray, Qt.SolidPattern))) 
        qp.drawRect(0,200,500,20)                       #mensola 1
        qp.drawRect(window_width - 300,450,20,500)      #barriera 1
        qp.drawRect(window_width - 300,0,20,250)        #barriera 2
       
        self.tower.paint(qp, window_width, window_height)
        for nodo in self.nodi:
            self.xx, self.zz = self.nodi[nodo]
            qp.drawEllipse(self.xx, self.zz, 10, 10)
        
        qp.setPen(QPen(Qt.gray, 5, Qt.SolidLine))
        qp.setBrush(QColor(QBrush(Qt.gray, Qt.SolidPattern)))       #pavimento
        qp.drawRect(0,window_height-10,window_width,10)
        for b in self.__blocks.values():
            b.paint(qp)
        self.paintObstacles(qp, self.gordo)
        qp.drawPixmap(window_width/2-self.start.width()/20,window_height - self.start.height()/8,self.start.width()/10,self.start.height()/10,self.start)  


