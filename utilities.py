import math

# Convert pixel coordinates to meter quadrotor coordinates
def pixel_to_meter(x,z,window_width,window_height,drone_height):
    x_meter = -(window_width/2 -x)/100
    z_meter = (window_height - drone_height -z)/100
    return x_meter, z_meter 

# Convert meter quadrotor coordinates to pixel coordinates
def meter_to_pixel(x,z,window_width,window_height,drone_height):
    x_pixel = x*100 + window_width/2
    z_pixel = - z*100 + window_height - drone_height
    return x_pixel, z_pixel 

# Compute euclidean distance between two couples
def distanceCouple(tuple1,tuple2):
    return math.sqrt((tuple1[0]-tuple2[0])**2 + (tuple1[1]-tuple2[1])**2)

def rotate_point(cx, cy, px , py, angle):
     return math.cos(angle) * (px - cx) - math.sin(angle) * (py - cy) + cx, math.sin(angle) * (px - cx) + math.cos(angle) * (py - cy) + cy
