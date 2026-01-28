import math

def two_point_angle(point1: tuple[float, float], point2: tuple[float,float]) -> float:
    # accepts 2 arguements, which are two different
    # coordinates
    # this function will calculate and return
    # the angle of two points using the arctan

    # first calculate the change of x and y
    delta_x = point2[0] - point1[0]
    delta_y = point2[1] - point1[1]

    # get the atan2 (which calculates beween two
    # given numbers in contrast to just atan)
    # flip y axis for pygame
    atan2 = math.atan2(delta_y, delta_x)

    # plug in the formula that converts the radians
    # to degrees
    return atan2 * (180 / math.pi)

def two_point_distance(point1: tuple[float, float], point2: tuple[float, float]) -> float:
    # accepts 2 arguments wyhich are two different coordinates
    # this function will calculate and return
    # distance between two points

    # each coord
    x1 = point1[0]
    x2 = point2[0]

    y1 = point1[1]
    y2 = point2[1]

    # plug into the formula
    d = math.sqrt((x2-x1)**2 + (y2-y1)**2)

    return d

def coordinate_range_x(left_x, right_x, target_x) -> bool:
    # left and right x is the range in which you want
    # to check that the target x is in
    # this is for boundary checking and such
    # returns if the target is in the range non-inclusive
    
    if target_x > left_x and target_x < right_x:
        return True

    return False

def calculate_new_xy(old_xy, speed, angle_in_degrees):
    angle_rad = math.radians(angle_in_degrees)
    delta_x = speed * math.cos(angle_rad)
    delta_y = speed * math.sin(angle_rad)
    new_x = old_xy[0] + delta_x
    new_y = old_xy[1] + delta_y
    return new_x, new_y
