import struct

from obj import  Obj

def char(c):
    # 1 byte
    return struct.pack('=c', c.encode('ascii'))

def word(w):
    # 2 bytes
    return struct.pack('=h',w)

def dword(d):
    # 4 bytes
    return struct.pack('=l',d)

def color(r, g, b):
    return bytes([b, g, r])

def decimalToRgb(decimal_array):
    rgb_array = []
    for i in range(3):
        rgb_array.append(int(round(decimal_array[i]*255)))
    return rgb_array


BLACK = color(0,0,0)
WHITE = color(255,255,255)

class Render(object):
    def __init__(self, width, height):
        self.curr_color = WHITE
        self.clear_color = BLACK
        self.glCreateWindow(width, height)

    def glCreateWindow(self, width, height):
        self.width = width
        self.height = height
        self.glClear()
        self.glViewport(0,0, width, height)

    def glClear(self):
        self.pixels = [ [ self.clear_color for x in range(self.width)] for y in range(self.height) ]

    def glViewport(self, x, y, width, height):
        self.viewport_initial_x = x
        self.viewport_initial_y = y
        self.viewport_width = width
        self.viewport_height = height
        self.viewport_final_x = x + width
        self.viewport_final_y = x + height
        
    def glVertextInViewport(self, x,y):
        return (x >= self.viewport_initial_x and
            x <= self.viewport_final_x) and (
            y >= self.viewport_initial_y and
            y <= self.viewport_final_y)

    def glClearColor(self, r,g,b):
        rgb_array = decimalToRgb([r,g,b])
        self.clear_color = color(rgb_array[0], rgb_array[1], rgb_array[2])

    def glVertex(self, x, y):
        if(x >= 0 or x < 0):
            pixelX = int(( x + 1 ) * ( self.viewport_width / 2 ) + self.viewport_initial_x)
        if(y >= 0 or y < 0):
            pixelY = int(( y + 1 ) * (self.viewport_height /2 ) + self.viewport_initial_y)
        if(self.glVertextInViewport(pixelX,pixelY) == True):
            self.pixels[pixelY][pixelX] = self.curr_color
    
    def glPoint(self, x, y):
        try:
            self.pixels[y][x] = self.curr_color
        except:
            pass
    
    def glColor(self, r,g,b):
        rgb_array = decimalToRgb([r,g,b])
        self.curr_color = color(rgb_array[0], rgb_array[1], rgb_array[2])

    def glFixCoordinate(self, value, main_axis):
        fixed_coordinate = 0
        if main_axis:
            fixed_coordinate = (value+1) * (self.viewport_width/2) + self.viewport_initial_x
        else:
            fixed_coordinate = (value+1) * (self.viewport_height/2) + self.viewport_initial_y
        return round(fixed_coordinate)
    

    def glLine(self, x0, y0, x1, y1) :
        x0 = self.glFixCoordinate(x0, True)
        x1 = self.glFixCoordinate(x1, True)
        y0 = self.glFixCoordinate(y0, False)
        y1 = self.glFixCoordinate(y1, False)

        steep = abs(y1 - y0) > abs(x1 - x0)

        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dx, dy = abs(x1 - x0), abs(y1 - y0)      
        
        offset = 0
        limit =  0.5
        y = y0

        for x in range(x0, x1+1):
            self.glPoint(y, x) if steep else self.glPoint(x, y)
            
            offset += 2*dy

            if offset >= limit:
                y += 1 if y0 < y1 else -1
                limit += 2*dx
    
    def glFinish(self, filename):
        archivo = open(filename, 'wb')

        # File header 14 bytes
        #archivo.write(char('B'))
        #archivo.write(char('M'))

        archivo.write(bytes('B'.encode('ascii')))
        archivo.write(bytes('M'.encode('ascii')))

        archivo.write(dword(14 + 40 + self.width * self.height * 3))
        archivo.write(dword(0))
        archivo.write(dword(14 + 40))

        # Image Header 40 bytes
        archivo.write(dword(40))
        archivo.write(dword(self.width))
        archivo.write(dword(self.height))
        archivo.write(word(1))
        archivo.write(word(24))
        archivo.write(dword(0))
        archivo.write(dword(self.width * self.height * 3))
        archivo.write(dword(0))
        archivo.write(dword(0))
        archivo.write(dword(0))
        archivo.write(dword(0))
        
        # Pixeles, 3 bytes cada uno

        for x in range(self.height):
            for y in range(self.width):
                archivo.write(self.pixels[x][y])

        archivo.close()

    def glLine_coord(self, x0, y0, x1, y1):

        steep = abs(y1 - y0) > abs(x1 - x0)

        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dx, dy = abs(x1 - x0), abs(y1 - y0)      
        
        offset = 0
        limit =  0.5
        y = y0
    
        try:
            m = dy/dx
        except ZeroDivisionError:
            pass
            
        

        for x in range(x0, x1+1):
            self.glPoint(y, x) if steep else self.glPoint(x, y)
            
            offset += 2*dy

            if offset >= limit:
                y += 1 if y0 < y1 else -1
                limit += 2*dx        
    
    def glDrawPolygon(self, vertices):
        count = len(vertices)

        for limit in range(count):
            v0 = vertices[limit]
            v1 = vertices[(limit + 1) % count]
            self.glLine_coord(v0[0], v0[1], v1[0], v1[1])

    def is_point_in_path(self, x, y, poly):
        # Args:
        #   x -- The x coordinates of point.
        #   y -- The y coordinates of point.
        #   poly -- a list of tuples [(x, y), (x, y), ...]

        # Returns:
        #   True if the point is in the path.
        num = len(poly)
        i = 0
        j = num - 1
        c = False
        for i in range(num):
            if ((poly[i][1] > y) != (poly[j][1] > y)) and \
                    (x < poly[i][0] + (poly[j][0] - poly[i][0]) * (y - poly[i][1]) /
                                    (poly[j][1] - poly[i][1])):
                c = not c
            j = i
        return c

    def scan(self, poly):
        minX, maxX, minY, maxY = 0,0,0,0
        for i in range(len(poly)):
            if(poly[i][0] < minX):
                minX = poly[i][0]
            elif(poly[i][0] > maxX):
                maxX = poly[i][0]
            if(poly[i][1] < minY):
                minY = poly[i][1]
            elif(poly[i][1] > maxY):
                maxY = poly[i][1]

        for y in range(minY, maxY):
            for x in range(minX, maxX):
                if (self.is_point_in_path(x,y, poly)):
                    #print(str(self.is_point_in_path(y,x, poly)) + " cords " + str(x) + "," + str(y))
                    self.glPoint(x, y)
    
    def loadModel(self, filename, translate, scale):
        model = Obj(filename)

        for face in model.faces:

            vertCount = len(face)

            for vert in range(vertCount):
                
                v0 = model.vertices[ face[vert][0] - 1 ]
                v1 = model.vertices[ face[(vert + 1) % vertCount][0] - 1]

                x0 = round((v0[0] * scale[0])  + translate[0])
                y0 = round((v0[1] * scale[1])  + translate[1])
                x1 = round((v1[0] * scale[0])  + translate[0])
                y1 = round((v1[1] * scale[1])  + translate[1])

                self.glLine_coord(x0, y0, x1, y1)








