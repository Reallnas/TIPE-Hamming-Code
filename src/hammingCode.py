from matrix import Matrix
from random import randint
from operator import xor

class HammingCodeBase :
    
    def __init__(self,k):
        if k < 2:
            raise Exception("The number of parity bits must at least be 2. k={}".format(k))
        self.k = k
        self.data_chunk_size = 2**k-k-1
        
    @staticmethod
    def getBinaryRepresentation(n,min_nb_of_bit=0):
        """ Renvoie une représentation d'un entier en binaire sur
            au moins min_nb_of_bit bits.
            Les bits de poids faible sont en premier"""
            
        bits = []
        i = n
        while i != 0:
            bits += [i % 2]
            i = i//2
        if len(bits) < min_nb_of_bit:
            bits += [0]*(min_nb_of_bit - len(bits))
        return bits
        
    @staticmethod
    def parityCheck(l):
        """ Renvoie 0 si le nombre de 1 dans la liste passée en argument est pair, 1 sinon
        
            Argument:
            -l (list): Un liste de données binaires"""
        parity = 0
        for elt in l:
            parity ^= elt
        return parity
        
    def cutDataInChunks(self,data):
        """Coupe la liste en morceaux de taille adaptée pour le code de 
            Hamming avec le nombre de bits de parité voulus 
            
            Argument:
            -data (list): Une liste de données binaires"""
            
        chunks, i = [], 0
        #print("k={},data_chunk_size={}".format(self.k,self.data_chunk_size))
        while i*(self.data_chunk_size) < len(data):
            chunk = data[i*(self.data_chunk_size):(i+1)*(self.data_chunk_size)]
            if len(chunk) < self.data_chunk_size:
                chunk += [0]*(self.data_chunk_size-len(chunk))
            chunks.append(chunk)
            i += 1
        return chunks
        
    def calculateGeneratorMatrix(self):
        """Calcule la matrice génératrice associée au code de Hamming voulu"""
        res = []
        for i in range(0,self.data_chunk_size):
            vect = [0]*self.data_chunk_size
            vect[i] = 1
            res.append(self.getEncryptedDataChunk(vect))
        self.generator_matrix = Matrix.fromArray(res).getTransposed()
        
    def calculateParityBitsValue(self,hamming_block):
        """Calcule le produit de la matrice de parité et du 
            bloc de données pour obtenir les valeurs des bits de parité
            
            Argument:
            -hamming_block (list): Un liste de données binaires"""
            
        if len(hamming_block) != self.hamming_block_size:
            raise Exception("Wrong size : {} instead of {}".format(
                len(hamming_block),self.hamming_block_size))
                
        data_column = Matrix.toColumn(hamming_block)
        return Matrix.multiply(self.H,data_column)
        
    def getEncryptedDataChunk(self,data_chunk):
        """Retourne le bloc de donnée encodé selon le code de Hamming 
            avec le nombre de bits de parité voulus
            
            Argument:
            -data_chunk (list): Un liste de données binaires contenant 
                                un bloc de Hamming non valide"""
        if len(data_chunk) != self.data_chunk_size:
            raise Exception("Wrong size : {} instead of {}".format(
                len(data_chunk),self.data_chunk_size))
                
        corr_data_chunk = self.insertParityBits(data_chunk)
        self.correctParityBits(corr_data_chunk)
        return corr_data_chunk
        
    def getEncryptedDataChunkWithGeneratorMatrix(self,data_chunk):
        """Retourne le bloc de donnée encodé selon le code de Hamming 
            avec la matrice génératrice avec le nombre de bits de parité voulus 
            
            Argument:
            -data_chunk (list): Un liste de données binaires contenant 
                                un bloc de Hamming non valide"""
        if len(data_chunk) != self.data_chunk_size:
            raise Exception("Wrong size : {} instead of {}".format(
                len(data_chunk),self.data_chunk_size))
        
        column = Matrix.toColumn(data_chunk)
        #On obtient une matrice colonne contenant le message encodé, 
        #on la transpose pour extraire la liste contenant le message
        return Matrix.multiply(self.generator_matrix,column).getTransposed()[0]
        
    def getDecryptedHammingBlock(self,hamming_block):
        block = hamming_block[:]
        self.ensureValidityAndCorrect(block)
        return self.removeParityBits(block)
        
    def encodeData(self,data):
        chunks = self.cutDataInChunks(data)
        return [self.getEncryptedDataChunk(d) for d in chunks]
        
    def encodeDataWithGeneratorMatrix(self,data):
        chunks = self.cutDataInChunks(data)
        return [self.getEncryptedDataChunkWithGeneratorMatrix(d) for d in chunks]
        
    def decodeBlocks(self,blocks):
        return [self.getDecryptedHammingBlock(block) for block in blocks ]
        
class HammingCode(HammingCodeBase):
    
    empty_parity_bits = None
    
    def __init__(self,k):
        """Regroupe différentes fonctions relatives au code de Hamming
        
            Arguments:
            -k (int) : nombre de bits de parité"""
        HammingCodeBase.__init__(self,k)
        self.parity_bit_number = k
        self.hamming_block_size = self.data_chunk_size + self.parity_bit_number
        
        self.empty_parity_bits = Matrix(self.parity_bit_number,1)
        self.calculateParityMatrix()
        self.calculateGeneratorMatrix()
        
    def calculateParityMatrix(self):
        """ Renvoie une matrice de parité contenant les entiers de 1 à 2**k
            en représentation binaire.
            Les bits de poids faible sont en premier """
            
        self.H = Matrix(self.hamming_block_size,self.parity_bit_number)
        for i in range(1,2**self.k):
            bin_repr = HammingCodeBase.getBinaryRepresentation(i,self.k)
            self.H.changeLine(i-1,bin_repr)
        self.H.transpose()

    
    def insertParityBits(self,data_chunk):
        """Retourne le bloc de données à encoder avec 
            les bits de parité mis à 0
            
            Argument:
            -data_chunk (list): Une liste de données binaires non initialisée"""
            
        if len(data_chunk) != self.data_chunk_size:
            raise Exception("Wrong size : {} instead of {}".format(len(data_chunk),self.data_chunk_size))
            
        res = [0]
        pos = 0
        length = 0
        for i in range(0,self.k-1):
            length += 2**i
            res += [0] + data_chunk[pos:pos+length]
            pos += length
        return res
    
    def removeParityBits(self,hamming_block):
        """Retourne le bloc de données auquel on enlevé les bits de parité
            
            Argument:
            -hamming_block (list): Un liste de données binaires contenant 
                                un bloc de Hamming"""
        res = []
        for i in range(1,self.k):
            res += hamming_block[2**i:2**(i+1)-1]
        return res

    def correctParityBits(self,hamming_block):
        """Retourne le bloc de données avec les bits 
            de parité mis à la bonne valeur.
            
            Argument:
            -hamming_block (list): Un liste de données binaires contenant 
                                un bloc de Hamming"""
                                
        if len(hamming_block) != self.hamming_block_size:
            raise Exception("Wrong size : {} instead of {}".format(
                len(hamming_block),self.hamming_block_size))
                
        #data_column = Matrix.toColumn(hamming_block)
        #parity_bits = Matrix.multiply(self.H,data_column)
        #for i in range(0,self.parity_bit_number):
        #    hamming_block[2**i-1] ^= parity_bits[i][0]
            
        for i in range(0,self.parity_bit_number):
           parity_bit = Matrix.multiplyLineWithColumn(self.H[i],hamming_block)
           hamming_block[2**i-1] ^=  parity_bit

    def ensureValidityAndCorrect(self,hamming_block):
        """Assure la validité du bloc et le corrige si besoin est
        
        Argument:
        -hamming_block (list): Un liste de données binaires contenant 
                            un bloc de Hamming à vérifier"""
        parity_bits = self.calculateParityBitsValue(hamming_block)
        if parity_bits == self.empty_parity_bits:
            return
        column = Matrix.toColumn(hamming_block)
        check_results = Matrix.multiply(self.H,column)
        e = self.H.searchColumn(check_results)
        hamming_block[e] =  1 - hamming_block[e]
        
class ExtendedHammingCode(HammingCodeBase) :
    
    empty_parity_bits = None
    
    def __init__(self,k):
        """Regroupe différentes fonctions relatives au code de Hamming
        
            Arguments:
            -k (int) : nombre de bits de parité
            -extended (bool): utilisation du code de Hamming étendu, ce dernier
                            ajoute un bit de parité final permettant de 
                            détecter jusqu'à 2 erreurs"""
        HammingCodeBase.__init__(self,k)
        self.parity_bit_number = k + 1
        self.hamming_block_size = self.data_chunk_size + self.parity_bit_number
        
        self.empty_parity_bits = Matrix(self.parity_bit_number,1)
        self.calculateParityMatrix()
        self.calculateGeneratorMatrix()
        
    def calculateParityMatrix(self):
        """ Renvoie une matrice de parité contenant les entiers de 1 à 2**k
            en représentation binaire.
            Les bits de poids faible sont en premier """
            
        self.H = Matrix(self.hamming_block_size,self.parity_bit_number)
        for i in range(1,2**self.k):
            bin_repr = [1] + HammingCodeBase.getBinaryRepresentation(i,self.k)
            self.H.changeLine(i,bin_repr)
            first_line =  [1] + [0]*self.k
            self.H.changeLine(0,first_line)
        self.H.transpose()
    
    def insertParityBits(self,data_chunk):
        """Retourne le bloc de données à encoder avec 
            les bits de parité mis à 0
            
            Argument:
            -data_chunk (list): Une liste de données binaires non initialisée"""
            
        if len(data_chunk) != self.data_chunk_size:
            raise Exception("Wrong size : {} instead of {}".format(len(data_chunk),self.data_chunk_size))
            
        res = [0]
        pos = 0
        length = 0
        for i in range(0,self.k-1):
            length += 2**i
            res += [0] + data_chunk[pos:pos+length]
            pos += length
        res = [0] + res
        return res
    
    def removeParityBits(self,hamming_block):
        res = []
        for i in range(1,self.k):
            res += hamming_block[2**i+1:2**(i+1)]
        return res

    def correctParityBits(self,hamming_block):
        """Retourne le bloc de données avec les bits 
            de parité mis à la bonne valeur.
            
            Argument:
            -hamming_block (list): Un liste de données binaires contenant 
                                un bloc de Hamming"""
                                
        if len(hamming_block) != self.hamming_block_size:
            raise Exception("Wrong size : {} instead of {}".format(
                len(hamming_block),self.hamming_block_size))

        for i in range(1,self.parity_bit_number):
            parity_bit = Matrix.multiplyLineWithColumn(self.H[i],hamming_block)
            hamming_block[2**(i-1)] ^=  parity_bit
            
        #Le cas i = 0 est différent car il repose sur les précédentes modifications
        #Il doit donc être traité à part
        parity_bit = Matrix.multiplyLineWithColumn(self.H[0],hamming_block)
        hamming_block[0] ^= parity_bit
        
    def ensureValidityAndCorrect(self,hamming_block):
        """Assure la validité du bloc et le corrige si besoin est
        
        Argument:
        -hamming_block (list): Un liste de données binaires contenant 
                            un bloc de Hamming à vérifier"""
        parity_bits = self.calculateParityBitsValue(hamming_block)
        if parity_bits == self.empty_parity_bits:
            return
        column = Matrix.toColumn(hamming_block)
        check_results = Matrix.multiply(self.H,column)
        if check_results[0][0] == 0:
            raise Exception("Il y a au moins deux erreurs. Bloc impossible à corriger")
        e = self.H.searchColumn(check_results)
        hamming_block[e] =  1 - hamming_block[e]
    
        
class HammingCodeXOR(HammingCodeBase):
    
    def __init__(self,k):
        """Regroupe différentes fonctions relatives au code de Hamming
        
            Arguments:
            -k (int) : nombre de bits de parité
            -extended (bool): utilisation du code de Hamming étendu, ce dernier
                            ajoute un bit de parité final permettant de 
                            détecter jusqu'à 2 erreurs"""
        HammingCodeBase.__init__(self,k)
        self.parity_bit_number = k + 1
        self.hamming_block_size = self.data_chunk_size + self.parity_bit_number
        
    def insertParityBits(self,data_chunk):
        """Retourne le bloc de données à encoder avec 
            les bits de parité mis à 0
            
            Argument:
            -data_chunk (list): Une liste de données binaires non initialisée"""
            
        if len(data_chunk) != self.data_chunk_size:
            raise Exception("Wrong size : {} instead of {}".format(len(data_chunk),self.data_chunk_size))
            
        res = [0]
        pos = 0
        length = 0
        for i in range(0,self.k-1):
            length += 2**i
            res += [0] + data_chunk[pos:pos+length]
            pos += length
        res = [0] + res
        return res
    
    def removeParityBits(self,hamming_block):
        res = []
        for i in range(1,self.k):
            res += hamming_block[2**i+1:2**(i+1)]
        return res
        

    def correctParityBits(self,hamming_block):
        pos = self.binaryListXOR(hamming_block)
        binary = HammingCodeBase.getBinaryRepresentation(pos)
        for i, bit in enumerate(binary):
            hamming_block[2**i] = (hamming_block[2**i] +bit) % 2
            
        hamming_block[0] = HammingCodeBase.parityCheck(hamming_block)
    
    def ensureValidityAndCorrect(self,hamming_block):
        """Assure la validité du bloc et le corrige si besoin est
        
        Argument:
        -hamming_block (list): Un liste de données binaires contenant 
                            un bloc de Hamming à vérifier"""
        pos = self.binaryListXOR(hamming_block)
        
        if pos != 0 and HammingCodeBase.parityCheck(hamming_block) == 0:
            raise Exception("Il y a au moins deux erreurs. Bloc impossible à corriger")
            
        hamming_block[pos] = 1 - hamming_block[pos]
        
    def binaryListXOR(self,l):
        sum = 0
        for i, bit in enumerate(l):
            if bit == 1:
                sum ^= i
        return sum
        
    def getEncryptedDataChunk(self,data_chunk):
        """Retourne le bloc de donnée encodé selon le code de Hamming 
            avec le nombre de bits de parité voulus
            
            Argument:
            -data_chunk (list): Un liste de données binaires contenant 
                                un bloc de Hamming non valide"""
        if len(data_chunk) != self.data_chunk_size:
            raise Exception("Wrong size : {} instead of {}".format(
                len(data_chunk),self.data_chunk_size))
                
        corr_data_chunk = self.insertParityBits(data_chunk)
        self.correctParityBits(corr_data_chunk)
        return corr_data_chunk
        
    def encodeData(self,data):
        chunks = self.cutDataInChunks(data)
        return [self.getEncryptedDataChunk(d) for d in chunks]
        
    def getDecryptedHammingBlock(self,hamming_block):
        block = hamming_block[:]
        self.ensureValidityAndCorrect(block)
        return self.removeParityBits(block)
        
    def decodeBlocks(self,blocks):
        return [self.getDecryptedHammingBlock(block) for block in blocks ]

class HammingCodeTests : 
    
    h = None
    extended_h = None
    h_xor = None
    
    def __init__(self):
        self.h = HammingCode(4)
        self.extended_h = ExtendedHammingCode(4)
        self.h_xor = HammingCodeXOR(4)
        
    def generateRandomBits(self,n):
        return [ randint(0,1) for i in range(0,n)]
        
    def expectEqual(self,a,b):
        if a != b :
            raise Exception("Test Failed: a={}, b={}".format(a,b))
            
    def expectTrue(self,b):
        if not b :
            raise Exception("Test Failed")
    
    def expectFalse(self,b):
        if b :
            raise Exception("Test Failed")
            
    def testAll(self):
        self.testCutDataInChunks()
        self.testParityMatrix()
        self.testGeneratorMatrix()
        self.testInsertParityBits()
        self.testRemoveParityBits()
        self.testCorrectParityBits()
        self.testGetEncryptedDataChunk()
        self.testGetEncryptedDataChunkWithGeneratorMatrix()
        self.testGetDecryptedHammingBlock()
        self.testReversabilityEncryption()
        self.testSimilarityEncryption()
        self.testSimilarityEncryptionData()
        
    def testParityMatrix(self):
        comp = Matrix.fromArray(
                [[1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1], 
                [0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1], 
                [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1], 
                [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1]])
        self.expectEqual(self.h.H, comp)
        
        ext_comp = Matrix.fromArray(
                [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1], 
                [0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1], 
                [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1], 
                [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1], ])
                
        self.expectEqual(self.extended_h.H, ext_comp)
        
    def testGeneratorMatrix(self):
        m = Matrix.multiply(self.h.H,self.h.generator_matrix)
        comp = Matrix(self.h.H.getHeight(),self.h.generator_matrix.getWidth())
        self.expectEqual(comp, m)
        
        ext_m = Matrix.multiply(self.extended_h.H,self.extended_h.generator_matrix)
        ext_comp = Matrix(self.extended_h.H.getHeight(),self.extended_h.generator_matrix.getWidth())
        self.expectEqual(ext_comp, ext_m)
        
    def testCutDataInChunks(self):
        comp = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 
                [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21], 
                [22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32], 
                [33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43], 
                [44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54], 
                [55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65], 
                [66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76], 
                [77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87], 
                [88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98], 
                [99,0,0,0,0,0,0,0,0,0,0]]
        data = [i for i in range(100)]
        data_chunks = self.h.cutDataInChunks(data)
        self.expectEqual(comp, data_chunks)
        
    def testInsertParityBits(self):
        comp = [0, 0, 1, 0, 2, 3, 4, 0, 5, 6, 7, 8, 9, 10, 11]
        d = [1,2,3,4,5,6,7,8,9,10,11]
        self.expectEqual(self.h.insertParityBits(d),comp)
        
        ext_comp = comp = [0, 0, 0, 1, 0, 2, 3, 4, 0, 5, 6, 7, 8, 9, 10, 11]
        self.expectEqual(self.extended_h.insertParityBits(d),ext_comp)
            
    def testRemoveParityBits(self):
        comp = [1,2,3,4,5,6,7,8,9,10,11]
        d = [0, 0, 1, 0, 2, 3, 4, 0, 5, 6, 7, 8, 9, 10, 11]
        self.expectEqual(self.h.removeParityBits(d), comp)
        
        ext_d = [0, 0, 0, 1, 0, 2, 3, 4, 0, 5, 6, 7, 8, 9, 10, 11]
        self.expectEqual(self.extended_h.removeParityBits(ext_d), comp)
        
    def testCorrectParityBits(self):
        comp = [1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1]
        b =    [0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1]
        b2 =    [0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1]
        self.h.correctParityBits(b)
        self.expectEqual(b, comp)
        
        ext_comp = [1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1]
        ext_b = [0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1]
        self.extended_h.correctParityBits(ext_b)
        self.expectEqual(ext_b, ext_comp)
                
    def testGetEncryptedDataChunk(self):
        d = [1,1,1,1,1,1,1,1,1,1,1]
        comp = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        self.expectEqual(self.h.getEncryptedDataChunk([1,1,1,1,1,1,1,1,1,1,1]), comp)
        
        ext_comp = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        self.expectEqual(self.extended_h.getEncryptedDataChunk([1,1,1,1,1,1,1,1,1,1,1]), ext_comp)
        
    def testGetEncryptedDataChunk2(self):
        d = [1,1,1,1,1,1,1,1,1,1,1]
        comp = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        self.expectEqual(self.h.getEncryptedDataChunk(d), comp)
        
        ext_comp = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        self.expectEqual(self.extended_h.getEncryptedDataChunk2(d), ext_comp)
        
    def testGetEncryptedDataChunkWithGeneratorMatrix(self):
        d = [1,1,1,1,1,1,1,1,1,1,1]
        comp = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        self.expectEqual(self.h.getEncryptedDataChunk(d), comp)
        
        ext_comp = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        self.expectEqual(self.extended_h.getEncryptedDataChunkWithGeneratorMatrix(d), ext_comp)
        
    def testGetDecryptedHammingBlock(self):
        comp = [1,1,1,1,1,1,1,1,1,1,1]
        d = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        self.expectEqual(self.h.getDecryptedHammingBlock(d),comp)
        
    def testReversabilityEncryption(self):
        data = [randint(0,1) for i in range (0,90)]
        chunks = self.h.cutDataInChunks(data)
        blocks = self.h.encodeData(data)
        self.expectEqual(chunks, self.h.decodeBlocks(blocks))
        
        ext_blocks = self.extended_h.encodeData(data)
        self.expectEqual(chunks,self.extended_h.decodeBlocks(ext_blocks))
        
        ext_blocks_xor = self.h_xor.encodeData(data)
        self.expectEqual(chunks,self.h_xor.decodeBlocks(ext_blocks_xor))

    def testSimilarityEncryption(self):
        for i in range(0,500):
            data = self.generateRandomBits(self.h.data_chunk_size)
            block = self.h.getEncryptedDataChunk(data)
            block_gen = self.h.getEncryptedDataChunkWithGeneratorMatrix(data)
            self.expectEqual(block,block_gen)
            
            ext_block = self.extended_h.getEncryptedDataChunk(data)
            ext_block_gen = self.extended_h.getEncryptedDataChunkWithGeneratorMatrix(data)
            ext_block_xor = self.h_xor.getEncryptedDataChunk(data)
            self.expectEqual(ext_block,ext_block_gen)
            self.expectEqual(ext_block,ext_block_xor)
            
    def testSimilarityEncryptionData(self):
        for i in range(0,1500):
            data = self.generateRandomBits(self.h.data_chunk_size*10)
            blocks = self.h.encodeData(data)
            blocks_gen = self.h.encodeDataWithGeneratorMatrix(data)
            self.expectEqual(blocks,blocks_gen)
            
            ext_blocks = self.extended_h.encodeData(data)
            ext_blocks_gen = self.extended_h.encodeDataWithGeneratorMatrix(data)
            self.expectEqual(ext_blocks,ext_blocks_gen)
            
HammingCodeTests().testAll()