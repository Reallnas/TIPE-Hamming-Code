from random import randint
from hammingCode import HammingCode,ExtendedHammingCode,HammingCodeXOR
import numpy as np
import matplotlib.pyplot as plt
import time
import csv
import datetime

def hammingDistance(l1,l2):
    if len(l1) != len(l2):
        raise "Arguments are not the same size"
    counter = 0
    for i in range(0,len(l1)):
        if l1[i] != l2[i] :
            counter += 1
    return counter

def divideLists(l1,l2):
    if len(l1) != len(l2):
        raise "Arguments are not the same size"
    return [l1[i]/l2[i] for i in range(0,len(l1))]

def generateRandomBits(n):
    return [ randint(0,1) for i in range(0,n)]

def changeOneRandomBit(l):
    """chance = randint(0,1000)
    if chance < 10:"""
    pos = randint(0,len(l)-1)
    l[pos] = 1 - l[pos]
    return (l,pos)

def calculateBitRate(times):
    l = [0]*len(times)
    for i in range(0,len(times)):
        k = 2+i
        l[i] = (1/times[i])*(2**k-k-1)
    return l

def saveTimesToCSV(T_enc_norm_gen,T_enc_norm_manual,T_dec_norm,T_enc_ext_gen, T_enc_ext_manual,T_dec_ext,T_enc_xor,T_dec_xor):
    t = datetime.datetime.now()
    file_name = "times/{0}_{1}_{2}_T{3}_{4}.csv".format(t.year,t.month,t.day,t.hour,t.minute)
    puissances = [3+i for i in range(0,len(T_enc_norm_gen))]
    tailles_données = [2**i - i -1 for i in puissances]
    tailles_paquets = [2**i -1for i in puissances]
    with open(file_name, 'w', newline='',encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')

        writer.writerow(["Facteur"] + puissances)
        writer.writerow(["Taille des données (en bits)"] + tailles_données)
        writer.writerow(["Taille des paquets (en bits)"] + tailles_paquets)
        writer.writerow(["Encodage normal (Matrice Génératrice)"] + T_enc_norm_gen)
        writer.writerow(["Encodage normal (Méthode Manuelle)"] + T_enc_norm_manual)
        writer.writerow(["Décodage normal"] + T_dec_norm)
        writer.writerow(["Encodage étendu (Matrice Génératrice)"] + T_enc_ext_gen)
        writer.writerow(["Encodage étendu (Méthode Manuelle)"] + T_enc_ext_manual)
        writer.writerow(["Décodage étendu"] + T_dec_ext)
        writer.writerow(["Encodage (Méthode XOR)"] + T_enc_xor)
        writer.writerow(["Décodage (Méthode XOR)"] + T_dec_xor)

def measureManualMethod(code,nb_test):
    t_enc = 0
    t_dec = 0
    for i in range(0,nb_test):
        if i % 500 == 0:
            print(i)
        data = generateRandomBits(code.data_chunk_size*10)
        chunks = code.cutDataInChunks(data)
        t1 = time.time()
        blocks = code.encodeData(data)
        t2 = time.time()
        for block in blocks:
            changeOneRandomBit(block)
        t3 = time.time()
        corr_data = code.decodeBlocks(blocks)
        t4 = time.time()

        if corr_data != chunks:
            print(corr_data)
            print(chunks)
            raise Exception("Erreur de décryption")

        t_enc += t2-t1
        t_dec += t4-t3
    return (t_enc/(nb_test*10),t_dec/(nb_test*10))

def measureGeneratorMethod(code,nb_test):
    t_enc = 0
    t_dec = 0
    for i in range(0,nb_test):
        if i % 500 == 0:
            print(i)
        data = generateRandomBits(code.data_chunk_size*10)
        chunks = code.cutDataInChunks(data)
        t1 = time.time()
        blocks = code.encodeDataWithGeneratorMatrix(data)
        t2 = time.time()
        for block in blocks:
            changeOneRandomBit(block)
        t3 = time.time()
        corr_data = code.decodeBlocks(blocks)
        t4 = time.time()

        if corr_data != chunks:
            print(corr_data)
            print(chunks)
            raise Exception("Erreur de décryption")

        t_enc += t2-t1
        t_dec += t4-t3
    return (t_enc/(nb_test*10),t_dec/(nb_test*10))

def measureXORMethod(code,nb_test):
    t_enc = 0
    t_dec = 0
    for i in range(0,nb_test):
        if i % 500 == 0:
            print(i)
        data = generateRandomBits(code.data_chunk_size*10)
        chunks = code.cutDataInChunks(data)
        t1 = time.time()
        blocks = code.encodeData(data)
        t2 = time.time()
        for block in blocks:
            changeOneRandomBit(block)
        t3 = time.time()
        corr_data = code.decodeBlocks(blocks)
        t4 = time.time()

        if corr_data != chunks:
            print(corr_data)
            print(chunks)
            raise Exception("Erreur de décryption")

        t_enc += t2-t1
        t_dec += t4-t3
    return (t_enc/(nb_test*10),t_dec/(nb_test*10))

def rawTimesGraphs(Y,T_enc_norm_gen,T_enc_norm_manual,T_dec_norm,T_enc_ext_gen, T_enc_ext_manual,T_dec_ext,T_enc_xor,T_dec_xor):

    plt.figure(1)
    plt.title("Temps en fonction de la taille des paquets (2**k)")
    plt.plot(Y,T_enc_norm_manual,label="Encodage normal",color="red",ls=':')
    plt.plot(Y,T_dec_norm,label="Décodage normal",ls='--',color="red")
    plt.legend(loc='upper left')
    plt.show()

    plt.figure(2)
    plt.title("Temps en fonction de la taille des paquets (2**k)")
    plt.plot(Y,T_enc_norm_manual,label="Encodage normal",color="red",ls=':')
    plt.plot(Y,T_dec_norm,label="Décodage normal",ls='--',color="red")
    plt.plot(Y,T_enc_ext_manual,label="Encodage étendu",color="green",ls=':')
    plt.plot(Y,T_dec_ext,label="Décodage étendu",ls='--',color="green")
    plt.legend(loc='upper left')
    plt.show()

    plt.figure(3)
    plt.title("Temps en fonction de la taille des paquets (2**k)")
    plt.plot(Y,T_enc_norm_gen,label="Encodage normal (Matrice Génératrice)",color="red")
    plt.plot(Y,T_enc_norm_manual,label="Encodage normal (Méthode Manuelle)",color="red",ls=':')
    plt.plot(Y,T_dec_norm,label="Décodage normal",ls='--',color="red")
    plt.plot(Y,T_enc_ext_gen,label="Encodage étendu (Matrice Génératrice)",color="green")
    plt.plot(Y,T_enc_ext_manual,label="Encodage étendu (Méthode Manuelle)",color="green",ls=':')
    plt.plot(Y,T_dec_ext,label="Décodage étendu",ls='--',color="green")
    plt.legend(loc='upper left')
    plt.show()

    plt.figure(4)
    plt.title("Temps en fonction de la taille des paquets (2**k)")
    plt.plot(Y,T_enc_norm_gen,label="Encodage normal (Matrice Génératrice)",color="red")
    plt.plot(Y,T_enc_norm_manual,label="Encodage normal (Méthode Manuelle)",color="red",ls=':')
    plt.plot(Y,T_dec_norm,label="Décodage normal",ls='--',color="red")
    plt.plot(Y,T_enc_ext_gen,label="Encodage étendu (Matrice Génératrice)",color="green")
    plt.plot(Y,T_enc_ext_manual,label="Encodage étendu (Méthode Manuelle)",color="green",ls=':')
    plt.plot(Y,T_dec_ext,label="Décodage étendu",ls='--',color="green")
    plt.plot(Y,T_enc_xor,label="Encodage (Méthode XOR)",color="blue",ls=':')
    plt.plot(Y,T_dec_xor,label="Décodage (Méthode XOR)",color="blue",ls='--')
    plt.legend(loc='upper left')
    plt.show()

def bitRatesGraphs(Y,T_enc_norm_gen,T_enc_norm_manual,T_dec_norm,T_enc_ext_gen, T_enc_ext_manual,T_dec_ext,T_enc_xor,T_dec_xor):
    br_enc_norm_gen = calculateBitRate(T_enc_norm_gen)
    br_enc_norm_manual = calculateBitRate(T_enc_norm_manual)
    br_dec_norm = calculateBitRate(T_dec_norm)
    br_enc_ext_gen = calculateBitRate(T_enc_ext_gen)
    br_enc_ext_manual = calculateBitRate(T_enc_ext_manual)
    br_dec_ext = calculateBitRate(T_dec_ext)
    br_enc_xor = calculateBitRate(T_enc_xor)
    br_dec_xor = calculateBitRate(T_dec_xor)

    plt.figure(11)
    plt.title("Débit en fonction de la taille des paquets (2**k)")
    plt.plot(Y,br_enc_norm_manual,label="Encodage normal",color="red",ls=':')
    plt.plot(Y,br_dec_norm,label="Décodage normal",ls='--',color="red")
    plt.legend(loc='upper left')
    plt.show()

    plt.figure(12)
    plt.title("Débit en fonction de la taille des paquets (2**k)")
    plt.plot(Y,br_enc_norm_manual,label="Encodage normal",color="red",ls=':')
    plt.plot(Y,br_dec_norm,label="Décodage normal",ls='--',color="red")
    plt.plot(Y,br_enc_ext_manual,label="Encodage étendu",color="green",ls=':')
    plt.plot(Y,br_dec_ext,label="Décodage étendu",ls='--',color="green")
    plt.legend(loc='upper left')
    plt.show()

    plt.figure(13)
    plt.title("Débit en fonction de la taille des paquets (2**k)")
    plt.plot(Y,br_enc_norm_gen,label="Encodage normal (Matrice Génératrice)",color="red")
    plt.plot(Y,br_enc_norm_manual,label="Encodage normal (Méthode Manuelle)",color="red",ls=':')
    plt.plot(Y,br_dec_norm,label="Décodage normal",ls='--',color="red")
    plt.plot(Y,br_enc_ext_gen,label="Encodage étendu (Matrice Génératrice)",color="green")
    plt.plot(Y,br_enc_ext_manual,label="Encodage étendu (Méthode Manuelle)",color="green",ls=':')
    plt.plot(Y,br_dec_ext,label="Décodage étendu",ls='--',color="green")
    plt.legend(loc='upper left')
    plt.show()

    plt.figure(14)
    plt.title("Débit en fonction de la taille des paquets (2**k)")
    plt.plot(Y,br_enc_norm_gen,label="Encodage normal (Matrice Génératrice)",color="red")
    plt.plot(Y,br_enc_norm_manual,label="Encodage normal (Méthode Manuelle)",color="red",ls=':')
    plt.plot(Y,br_dec_norm,label="Décodage normal",ls='--',color="red")
    plt.plot(Y,br_enc_ext_gen,label="Encodage étendu (Matrice Génératrice)",color="green")
    plt.plot(Y,br_enc_ext_manual,label="Encodage étendu (Méthode Manuelle)",color="green",ls=':')
    plt.plot(Y,br_dec_ext,label="Décodage étendu",ls='--',color="green")
    plt.plot(Y,br_enc_xor,label="Encodage (Méthode XOR)",color="blue",ls=':')
    plt.plot(Y,br_dec_xor,label="Décodage (Méthode XOR)",color="blue",ls='--')
    plt.legend(loc='upper left')
    plt.show()

def methodRatesGraph(Y,T_enc_norm_gen,T_enc_norm_manual,T_enc_ext_gen,T_enc_ext_manual):
    r_norm = divideLists(T_enc_norm_gen,T_enc_norm_manual)
    r_ext = divideLists(T_enc_ext_gen,T_enc_ext_manual)
    plt.figure(21)
    plt.title("Rapport temporel entre la méthode génératrice et la méthode manuelle")
    plt.plot(Y,r_norm,label="Encodage normal", color="red")
    plt.plot(Y,r_ext,label="Encodage étendu", color="green")
    plt.legend()
    plt.show()

def extendedRatesGraph(Y,T_enc_norm_gen,T_enc_norm_manual,T_dec_norm,T_enc_ext_gen, T_enc_ext_manual,T_dec_ext):
    r_enc_gen = divideLists(T_enc_ext_gen,T_enc_norm_gen)
    r_enc_man = divideLists(T_enc_ext_manual,T_enc_norm_manual)
    r_dec = divideLists(T_dec_ext,T_dec_norm)
    plt.figure(22)
    plt.title("Rapport temporel entre le code étendu et le code classique")
    plt.plot(Y,r_enc_gen,label="Encodage (Matrice Génératrice)", color="red")
    plt.plot(Y,r_enc_man,label="Encodage (Méthode Manuelle)", color="green")
    plt.plot(Y,r_dec,label="Décodage", color="blue")
    plt.legend()
    plt.show()


def Graphs(factor_offset = 1,nb_test = 2000):
    T_enc_norm_manual  =[]
    T_enc_norm_gen  =[]
    T_enc_ext_manual = []
    T_enc_ext_gen  =[]
    T_enc_xor  =[]
    T_dec_xor  =[]
    T_dec_norm  =[]
    T_dec_ext = []
    Y = np.arange(2,2+factor_offset)

    t1 = time.time()
    for k in Y:
        print(k)
        code = HammingCode(k)
        ext_code = ExtendedHammingCode(k)
        xor_code = HammingCodeXOR(k)

        t_manual = measureManualMethod(code,nb_test)
        t_gen = measureGeneratorMethod(code,nb_test)
        t_ext_manual = measureManualMethod(ext_code,nb_test)
        t_ext_gen = measureGeneratorMethod(ext_code,nb_test)
        t_xor = measureXORMethod(xor_code,nb_test)

        T_enc_norm_gen.append(t_gen[0])
        T_enc_norm_manual.append(t_manual[0])
        T_enc_ext_gen.append(t_ext_gen[0])
        T_enc_ext_manual.append(t_ext_manual[0])
        T_enc_xor.append(t_xor[0])
        T_dec_xor.append(t_xor[1])
        T_dec_norm.append(t_manual[1])
        T_dec_ext.append(t_ext_manual[1])

    t2 = time.time()
    print(t2-t1)
    saveTimesToCSV(T_enc_norm_gen,T_enc_norm_manual,T_dec_norm,T_enc_ext_gen,
                    T_enc_ext_manual,T_dec_ext,T_enc_xor,T_dec_xor)

    rawTimesGraphs(Y,T_enc_norm_gen,T_enc_norm_manual,T_dec_norm,T_enc_ext_gen,
                    T_enc_ext_manual,T_dec_ext,T_enc_xor,T_dec_xor)

    bitRatesGraphs(Y,T_enc_norm_gen,T_enc_norm_manual,T_dec_norm,T_enc_ext_gen,
                    T_enc_ext_manual,T_dec_ext,T_enc_xor,T_dec_xor)

    methodRatesGraph(Y,T_enc_norm_gen,T_enc_norm_manual,T_enc_ext_gen,
                    T_enc_ext_manual)
    extendedRatesGraph(Y,T_enc_norm_gen,T_enc_norm_manual,T_dec_norm,
                        T_enc_ext_gen, T_enc_ext_manual,T_dec_ext)


Graphs(8,1500)

def CorrectionUneErreur():
    h = HammingCode(3)
    b = generateRandomBits(4)
    print("Données à encoder: ",b)
    d = h.getEncryptedDataChunk(b)
    print("Bloc encodé: ",d)
    print("Bits ajoutés: [X  X  -  X  -  -  -]")
    err_d,pos = changeOneRandomBit(d)
    print("Bloc encodé erroné: ",err_d)
    print("Erreur en position :",pos)
    corr_b = h.getDecryptedHammingBlock(err_d)
    print("Données récupérées du bloc erroné: ",corr_b)

def DeuxErreursNormal():
    h = HammingCode(3)
    b = generateRandomBits(4)
    print("Données à encoder: ",b)
    d = h.getEncryptedDataChunk(b)
    print("Bloc encodé: ",d)
    print("Bits ajoutés: [X  X  -  X  -  -  -]")
    err_d = d[:]
    err_d[0] = 1 - err_d[0]
    err_d[5] = 1 - err_d[5]
    print("Bloc encodé erroné: ",err_d)
    print("Erreur en position : 0 et 5")
    corr_b = h.getDecryptedHammingBlock(err_d)
    print("Données récupérées du bloc erroné: ",corr_b)

def DetectionDeuxErreursEtendu():
    h = ExtendedHammingCode(3)
    b = generateRandomBits(4)
    print("Données à encoder: ",b)
    d = h.getEncryptedDataChunk(b)
    print("Bloc encodé: ",d)
    print("Bits ajoutés: [X  X  X  -  X  -  -  -]")
    err_d = d[:]
    err_d[0] = 1 - err_d[0]
    err_d[5] = 1 - err_d[5]
    print("Bloc encodé erroné: ",err_d)
    print("Erreur en position : 0 et 5")
    corr_b = h.getDecryptedHammingBlock(err_d)
    print("Données récupérées du bloc erroné: ",corr_b)

CorrectionUneErreur()
DeuxErreursNormal()
DetectionDeuxErreursEtendu()