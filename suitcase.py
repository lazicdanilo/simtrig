import time as t
from graphics import GraphWin, Rectangle, Point, color_rgb
import argparse
import math
import re
import classSuitcase

def draw_background(win_x, win_y, win):
    backround = Rectangle(Point(30,30), Point(win_x-30, win_y-30))
    backround.setFill(color_rgb(30,30,30))
    backround.draw(win)


def draw_sensors(win):
    global s1, s2, s3

    s1 = classSuitcase.sensor(300, 400, 5, "Green", "s1", win)
    s2 = classSuitcase.sensor(400, 400, 5, "Red", "s2", win)
    s3 = classSuitcase.sensor(500, 400, 5, "Yellow", "s3", win)


def draw_sensors_with_distance_on_x_axis(x, y, d, win):
    global s1, s2, s3, draw_sensors_with_distance_on_x_axis_flg

    s1 = classSuitcase.sensor(x, y, 5, "Green", "s1", win)
    s2 = classSuitcase.sensor(x+d, y, 5, "Red", "s2", win)
    s3 = classSuitcase.sensor(x+d+d, y, 5, "Yellow", "s3", win)
    draw_sensors_with_distance_on_x_axis_flg = 1

def refresh(win_x, win_y, win):
    #global draw_sensors_with_distance_on_x_axis_flg
    try:
        if (draw_sensors_with_distance_on_x_axis_flg != 1):
            draw_background(win_x, win_y, win)
            draw_sensors(win)
        else:
            draw_background(win_x, win_y, win)
            draw_sensors_with_distance_on_x_axis(args.sensor_start_x, args.sensor_start_y, args.distance, win)
    except NameError:
        draw_background(win_x, win_y, win)
        draw_sensors(win)



def main():
    global args

    parser = argparse.ArgumentParser(description="Quick script")

    parser.add_argument("-d", "--distance", default=None, type=int, help="This is the distance between sensors")
    parser.add_argument("-sx", "--sensor_start_x", default=200, type=int, help="This is starting point for sensors on X axis")
    parser.add_argument("-sy", "--sensor_start_y", default=200, type=int, help="This is starting point for sensors on Y axis")


    parser.add_argument("-tx", "--target_x", default=None, type=int, help="This is target distance in pixels on X axis")
    parser.add_argument("-ty", "--target_y", default=None, type=int, help="This is target distance in pixels on Y axis")
    
    parser.add_argument("-m", "--mouse", default=1, type=int, help="For using mouse to get data")
    parser.add_argument("-s", "--socket", default=0, type=int, help="For using socket to get data")
    parser.add_argument("-f", "--file", default="", type=str, help="For using file to get data")

    parser.add_argument("-wx", "--win_x", default=1000, type=int, help="For defining window size in px on X axis")
    parser.add_argument("-wy", "--win_y", default=700, type=int, help="For defining window size in px on Y axis")

    parser.add_argument("-aw", "--axis_width", default=2, type=int, help="For defining window size in px on Y axis")

    args = parser.parse_args()


    
    win_x = args.win_x
    win_y = args.win_y

    axis_width = args.axis_width


    win = GraphWin("SuitcaseSim", win_x, win_y)
    classSuitcase.start(win_x, win_y, axis_width,win)
    
    draw_background(win_x, win_y, win)

    if(args.distance != None):
        draw_sensors_with_distance_on_x_axis(args.sensor_start_x, args.sensor_start_y, args.distance, win)
    else:
        draw_sensors(win)


    def get_mouse_data():
        while True:
            cp = win.getMouse()

            refresh(win_x, win_y, win)
        
            s1.click_circle(cp.getX(), cp.getY(), cp.getX()+50, cp.getY() - 70)
            s2.click_circle(cp.getX(), cp.getY(), cp.getX()+100, cp.getY() - 70)
            s3.click_circle(cp.getX(), cp.getY(), cp.getX()+150, cp.getY() - 70)

        
    def target_data(x, y):

        s1.click_circle(x, y, x+50, y - 70)
        s2.click_circle(x, y, x+100, y - 70)
        s3.click_circle(x, y, x+150, y - 70)
        
    
        
        

    def socket_data():
        # todo!!!
        pass

    def file_data(file_dir):
        new_speed = 1

        f = open(str(file_dir), "r")
        
        for line in f:
            new_speed_flg = re.match("speed=", line)

            if new_speed_flg:
                speed = re.split("speed=", line)
                new_speed = float(speed[1])
            else:
            
                data = re.split(";", line)

                s1.sensor_radius(int(data[0]))
                s2.sensor_radius(int(data[1]))
                s3.sensor_radius(int(data[2]))
                t.sleep(new_speed)
                refresh(win_x, win_y, win)


    
    if (args.target_x == None) & (args.target_y != None):
        print("Missing target_y argument")

    elif (args.target_x != None) & (args.target_y == None):
         print("Missing target_x argument")

    if (args.socket == 1):
        socket_data()

    elif (args.file != ""):
        file_data(args.file)

    elif (args.target_x != None) & (args.target_y != None):
        target_data(args.target_x, args.target_y)
        get_mouse_data()

    else:
        get_mouse_data()

    pass


main()



    