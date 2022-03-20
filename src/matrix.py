import numpy as np

class Matrix:

    mat = [[]]
    nb_line = 0
    nb_column = 0

    def __init__(self,n=1,m=0):
        """Creer une matrice initialisée à 0:

            Paramètres:
            n (int) : nombre de lignes de la matrice
            m (int) : nombre de colonnes de la matrice"""

        self.nb_line = n
        self.nb_column = m
        self.setToNull()

    @staticmethod
    def fromArray(array):
        """Créé une matrice à partir d'un tableau de tableau.
            Les tableaux internes seront les lignes de la matrice,
            ils doivent donc tous avoir la même taille"""
        n = len(array)
        m = len(array[0])
        for line in array:
            if len(line) != m:
                raise Exception("All the lines do not have the same size")
        mat = Matrix(n,m)
        for i,line in enumerate(array):
                mat.changeLine(i,line[:])
        return mat

    def __getitem__(self, key):
        """Surcharge l'opérateur []"""
        return self.mat[key]

    def __str__(self):
        """Surcharge l'opérateur str()
            Utilisé par la fonction print()"""
        return "Nombre de lignes = {}, colonnes={}, \nmatrice={}".format(
        self.nb_line,self.nb_column,self.mat)

    def __eq__(self,M):
        return self.mat == M.mat

    def setToNull(self):
        """Rend la matrice nulle en gardant ses dimensions"""
        self.mat = [[]]*self.nb_line
        line = [0]*self.nb_column
        for i in range(0,self.nb_line):
            self.mat[i] = line[:]

    def getTransposed(self):
        """Renvoie la transposée de la matrice """
        transposed = Matrix(self.nb_column,self.nb_line)
        for i in range(0,self.nb_line):
            for j in range(0,self.nb_column):
                transposed[j][i] = self.mat[i][j]
        return transposed

    def transpose(self):
        """Transpose la matrice """
        self.mat = self.getTransposed().mat
        self.nb_line,self.nb_column = self.nb_column, self.nb_line

    def getHeight(self):
        """Renvoie le nombre de lignes de la matrice"""
        return self.nb_line

    def getWidth(self):
        """Renvoie le nombre de colonne de la matrice"""
        return self.nb_column

    @staticmethod
    def multiply(A,B):
        """Multiplie deux matrices entre elles

            A = Matrix.fromArray([[0,0],[1,0],[0,1],[1,1]])
            B = Matrix.fromArray([[1,1,1,1],[0,0,0,0]])
            print(Matrix.multiply(A,B))
            #print(multiplyMatrixes([[0]],[[0]]))
        """
        n = A.getHeight()
        m = B.getWidth()
        if A.getWidth() != B.getHeight():
            raise Exception("Matrixes have the wrong dimensions: A : l={},c={} B:     l={},c={}".format(A.getHeight(),A.getWidth(),B.getHeight(),B.getWidth()))
        t_B = B.getTransposed()
        q = A.getWidth()
        C = Matrix(n,m)
        for i in range(0,n):
            for j in range(0,m):
                #On traite des matrices de bits, on est donc dans le corps
                #Z/2Z où 1+1 = 0
                C.mat[i][j] = np.dot(A[i],t_B[j]) % 2
        return C

    @staticmethod
    def toColumn(array):
        n = len(array)
        m = Matrix(n,1)
        for i in range(0,n):
            m.mat[i][0] = array[i]
        return  m #Matrix.fromArray([array]).getTransposed()

    def changeLine(self,line_index,new_line):
        self.mat[line_index] = new_line[:]

    def searchColumn(self,column):
        if  self.nb_line != column.getHeight():
            raise Exception("Wrong dimensions, len_column: A={}, B={}".format(self.nb_line,len(column)))
        for i in range(0,self.nb_column):
            same = True
            for j in range(0,self.nb_line):
                if self.mat[j][i] != column.mat[j][0]:
                    same = False
                    break
            if same:
                return i
        return -1

    def multiplyLine(self,line_index,column):
        n = column.getHeight()
        C = 0
        for i in range(0,n):
            C ^= self.mat[line_index][i]*column.mat[i][0]
        return [[C]]

    @staticmethod
    def multiplyLineWithColumn(line,column):
        #On traite des matrices de bits, on est donc dans le corps
        #Z/2Z où 1+1 = 0
        return np.dot(line,column) % 2

def testMatrix():
    m = Matrix(4,5)
    m[0][3] = 1
    t = m.getTransposed()
    print(m)
    print(t)
    c= Matrix.multiply(m,t)

    print(Matrix.toColumn([0,1,2,3,4,5]))
    print(Matrix(2,1) == Matrix.fromArray([[0],[0]]))