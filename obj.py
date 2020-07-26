# Opens and reads an .obj file saving it's information in four arrays

class Obj(object):
    def __init__(self, filename):
        with open(filename, 'r') as file:
            self.lines = file.read().splitlines()

        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.faces = []

        self.read()

    def read(self):
        for line in self.lines:
            if line and (line[0] == 'v' or line[0] == 'f'):
                prefix, value = line.split(' ', 1)

                # Split the vertices
                if prefix == 'v':
                    self.vertices.append(list(map(float,value.split(' '))))
                # Split the normals
                elif prefix == 'vn':
                    self.normals.append(list(map(float,value.split(' '))))
                # Split the texcoords
                elif prefix == 'vt':
                    self.texcoords.append(list(map(float,value.split(' '))))
                # Split the faces
                elif prefix == 'f':
                    self.faces.append([list(map(int,vert.split('/'))) for vert in value.split(' ')])
