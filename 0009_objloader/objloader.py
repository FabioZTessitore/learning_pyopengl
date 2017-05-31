import numpy

class ObjLoader:
    def __init__(self):
        self.vert_coords = []
        self.text_coords = []
        self.normals = []

        self.vert_indexes = []
        self.text_indexes = []
        self.normals_indexes = []

        self.model = []

    def load(self, filename):
        file = open(filename, 'r')

        for line in file.readlines():
            if line.startswith('#'):    continue

            values = line.split()
            if not values:  continue

            if values[0] == 'v':
                self.vert_coords.append(values[1:4])
            elif values[0] == 'vt':
                self.text_coords.append(values[1:3])
            elif values[0] == 'vn':
                self.normals.append(values[1:4])
            elif values[0] == 'f':
                face = []
                text = []
                normal = []
                for v in values[1:4]:
                    w = v.split('/')
                    face.append(int(w[0])-1)
                    text.append(int(w[1])-1)
                    normal.append(int(w[2])-1)
                self.vert_indexes.append(face)
                self.text_indexes.append(text)
                self.normals_indexes.append(normal)

        self.vert_indexes = [y for x in self.vert_indexes for y in x]
        self.text_indexes = [y for x in self.text_indexes for y in x]
        self.normals_indexes = [y for x in self.normals_indexes for y in x]

        for i in self.vert_indexes:
            self.model.extend(self.vert_coords[i])
        for i in self.text_indexes:
            self.model.extend(self.text_coords[i])
        #for i in self.normals_indexes:
        #    self.model.extend(self.normals[i])

        self.model = numpy.array(self.model, dtype=numpy.float32)

        print 'vertices (', len(self.vert_coords), ')\n', self.vert_coords
        print 'textures (', len(self.text_coords), ')\n', self.text_coords
        #print 'normals', self.normals
        print 'vert indexes (', len(self.vert_indexes), ')\n', self.vert_indexes
        #print self.text_indexes
        #print self.normals_indexes
        #print self.model

if __name__ == '__main__':
    ol = ObjLoader()
    ol.load('../obj/cube/cube.obj')
