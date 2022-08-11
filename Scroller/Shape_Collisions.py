#Document used for collisions between shapes:
from cmath import pi
import math

def collision(shape1, shape2, shape1type="circle", shape2type="circle"):
    
    if shape1type == "circle" and shape2type == "circle":
        return(circles(shape1, shape2))
    
    elif shape1type == "circle" or shape2type == "circle":
        if shape1type == "circle":
            if shape2type == "rect": return(circle_rect(shape1, shape2))
            elif shape2type =="triangle": return(circle_tri(shape1, shape2))
        
        else:
            if shape1type == "rect": return(circle_rect(shape2, shape1))
            elif shape1type =="triangle": return(circle_tri(shape2, shape1))

    elif shape1type == shape2type and shape1type == "rect":
        return(rects(shape1, shape2))

    elif shape1type == "rect" or shape2type == "rect":
        if shape1type == "rect":
            if shape2type == "triangle": return(rect_tri(shape1, shape2))
        
        else:
            if shape2type == "triangle": return(rect_tri(shape2, shape1))
    
    elif shape1type == "triangle" and shape2type == "triangle":
        return(triangles(shape1, shape2))
    
    else:
        for i in range(2): print('')
        print("-----COLLISION TYPE CHOICE ERROR-------")
        for i in range(2): print('')
        return(None)




def circles(circle1, circle2):
    distance = (circle1.size+circle2.size)/2
    xdis, ydis = circle1.x - circle2.x, circle1.y-circle2.y
    if math.sqrt(xdis**2 + ydis**2) <= distance: return(True)
    else: return(False)

def rects(rect1, rect2):
    if rect1.x+rect1.size/2 >= rect2.x-rect2.size/2 and rect1.x-rect1.size/2 <= rect2.x+rect2.size/2:
        if rect1.y+rect1.size/2 >= rect2.y-rect2.size/2 and rect1.y-rect1.size/2 <= rect2.y+rect2.size/2:
            return(True)
    return(False)


def triangles(tri1, tri2):
    pass

def circle_rect(circle, rect): #circle and then rect
    if circle.x >= rect.x-rect.size/2 and circle.x <= rect.x+rect.size/2: #if the center of the circle is within the xvalues of the rect
        if circle.y+circle.size/2 >= rect.y-rect.size/2 and circle.y-circle.size/2 <= rect.y+rect.size/2: # if any circle y values are within yvalues of rect
            #print("circle touches top or bottom")
            return(True)

    elif circle.y >= rect.y-rect.size/2 and circle.y <= rect.y+rect.size/2: #if the center of the circle is within the yvalues of the rect
        if circle.x+circle.size/2 >= rect.x-rect.size/2 and circle.x-circle.size/2 <= rect.x+rect.size/2: # if any circle x values are within yvalues of rect
            #print("circle touches left or right")
            return(True)
    
    elif circle.x+circle.size/2 >= rect.x-rect.size/2 and circle.x-circle.size/2 <= rect.x+rect.size/2 and circle.y+circle.size/2 >= rect.y-rect.size/2 and circle.y-circle.size/2 <= rect.y+rect.size/2:
        if circle.x < rect.x:
            if circle.y < rect.y:
                if math.sqrt( (circle.x-(rect.x-rect.size/2))**2 + (circle.y-(rect.y-rect.size/2))**2) <= circle.size/2: 
                    #print("top left corner of rect")
                    return True #top left corner of rect
                    
            else: 
                if math.sqrt( (circle.x-(rect.x-rect.size/2))**2 + (circle.y-(rect.y+rect.size/2))**2) <= circle.size/2: 
                    #print("bottom left corner of rect")
                    return True #bottom left corner of rect
        else:
            if circle.y <rect.y:
                if math.sqrt( (circle.x-(rect.x+rect.size/2))**2 + (circle.y-(rect.y-rect.size/2))**2) <= circle.size/2: 
                    #print("top right corner of rect")
                    return True #top right corner of rect
            else:
                if math.sqrt( (circle.x-(rect.x+rect.size/2))**2 + (circle.y-(rect.y+rect.size/2))**2) <= circle.size/2: 
                    #print("bottom right corner of rect")
                    return True #bottom right corner of rect
    
    return False

def circle_tri(circle, triangle):

    if circle.x < triangle.x: factor = -1
    else:factor = 1

    #check top
    horo_distance, vert_distance = abs(triangle.point1[0]-circle.x), abs(triangle.point1[1]-circle.y)
    if math.sqrt(horo_distance**2 + vert_distance**2) <= circle.size/2:
        return True


    #one side
    perp_slope = -1/((triangle.point1[1]-triangle.point2[1])/(triangle.point1[0]-triangle.point2[0]))
    circle_contact_angle = math.atan(perp_slope)
    px, py = circle.x+ math.cos(circle_contact_angle)*circle.size/2 *-1*factor, circle.y+math.sin(circle_contact_angle)*circle.size/2 *-1
    #if node_visible == True: pygame.draw.ellipse(screen, (255, 0, 0), pygame.Rect(px-5, py-5, 10, 10))
    if point_in_tri(triangle, px, py) == True: return True
    
    # bottom side
    if triangle.point2[1] != triangle.point3[1]:
        perp_slope = -1/((triangle.point2[1]-triangle.point3[1])/(triangle.point2[0]-triangle.point3[0]))
        circle_contact_angle = math.atan(perp_slope)
    else: circle_contact_angle = pi/2*factor

    px, py = circle.x+ math.cos(circle_contact_angle)*circle.size/2 *-1*factor, circle.y+math.sin(circle_contact_angle)*circle.size/2 *-1

    #if node_visible == True: pygame.draw.ellipse(screen, (0, 255, 0), pygame.Rect(px-5, py-5, 10, 10))
    if point_in_tri(triangle, px, py) == True: return True
    
    
    return False




    



    pass
def rect_tri(rect, tri):
    pass


def point_in_tri(tri, px, py, buffer=0):
    point1, point2, point3 = (tri.x+tri.radius*math.cos(tri.angle), tri.y-tri.radius*math.sin(tri.angle)), (tri.x+tri.radius*math.cos(tri.angle-(2*pi/3)), tri.y-tri.radius*math.sin(tri.angle-(2*pi/3))), (tri.x+tri.radius*math.cos(tri.angle+(2*pi/3)), tri.y-tri.radius*math.sin(tri.angle+(2*pi/3)))
    ax, ay = point1[0], point1[1]
    bx, by = point2[0], point2[1]
    cx, cy = point3[0], point3[1]

    w1 = (ax*(cy-ay) + (py-ay)*(cx-ax)-px*(cy-ay))  /  ((by-ay)*(cx-ax) - (bx-ax)*(cy-ay))
    w2 = (py-ay-w1*(by-ay)) / (cy-ay)

    if w1 >= 0-buffer and w2 >= 0-buffer and (w1+w2) <= 1+buffer: return(True)
    return(False)