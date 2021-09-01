import random
import math
import csv

with open('iris.data.txt', "r") as csvfile:
    lines = csv.reader(csvfile)
    # for row in lines:


def dadosCsv(nome, share, treinamento=[], teste=[]):
    with open(nome, "r") as csvfile:
        lines = csv.reader(csvfile)
        dataset = list(lines)
        print(dataset)
       # dataset = normalize(dataset)

       # dataset = binarylist(dataset)

        for x in range(len(dataset) - 1):
            # print(x, "(x)", dataset[x])
            # caso aleatório
            if random.random() < share:
                treinamento.append(dataset[x])
            else:
                teste.append(dataset[x])

            # caso padrão, 15 no conjunto de teste, 35 no treinamento para 50 amostras de cada classe
            # if x % 50 > 15:
            #     treinamento.append(dataset[x])
            # else:
            #     teste.append(dataset[x])
        print(len(treinamento), " treinamento", len(teste), " teste")

def subset(elementos, train=[]):
    #retorna subconjunto do conjunto original de treinamento com numero especifico de elementos
    resp = []
    for x in range(elementos):
        resp.append(train[x])

    return resp

def rangeSelector(ranges, data=[]):
    #método que gera os intervalos da árvore de decisão.
    # Por exemplo, pra um atributo X que varia entre 1 e 7 e queremos classificar em 3 classes diferentes,
    # a classe 1 pode ser com valores de X entre 1 e 3, a classe 2, com valores entre 3 e 5 e a classe 3 com valores entre 5 e 7
    # [1 -3 | 3 -5 | 5 -7 ] faixa de classificação
    #   [ C1 | C2 | C3 ] respectivas classes

    # se for normalizar, deve-se normalizar o dataset inteiro pra evitar erros

    max = [0, 0, 0, 0]
    min = [0, 0, 0, 0]
    # valores inciais assumidos como todos 0. Fazem sentido pro iris,
    # mas o correto seria pegar valores do primeiro exemplo e tratar a partir dele
    resp = data

    for x in range(len(data) - 1):
        #seleciona o maior e o menor exemplo dentre os valores do dataset.
        # A ideia é obter os valores máximo e mínimo pra todos os parametros
        for y in range(4):
            #4 pq é o tamanho da lista de parametros
            # print(x, "(x)", y, "(y)", matriz[x][y], "(cell)")
            #se = 0 recebe (funciona pq todos os valores são positivos)
            #se maior que o atual, atualiza

            if x == 0:

                max[y] = float(data[x][y])
                min[y] = float(data[x][y])

            else:

                if float(data[x][y]) > max[y]:
                    max[y] = float(data[x][y])
                if float(data[x][y]) < min[y]:
                    min[y] = float(data[x][y])

    # print(max)
    # print(min)


    delta = []
    for x in range(4):
        a = []
        delta.append(a)
    #inicializa uma matriz de 4 linhas

    #print(delta)

    for x in range(4):
        for y in range(ranges-1):
            a = min[x] + (y+1)*((max[x]-min[x])/ranges)
            delta[x].append(a)

    # print("delta array:", delta)
    # cria os intervalos

    #este último loop pega os dados e converte eles para sua posição dentro de cada intervalo
    #por exemplo, seja um exemplo E = [2.8, 3.5, 4.7]
    # e as ranges pra cada atributo forem: X = [0-2|2-4|4-6], Y =[0-1.5|1.5-3|3-4.5] e Z = [0-3|3-6|6-9]
    # o valor exemplo E dentro dos intervalos de classificação sera E' = [1, 2, 1]
    #a lista resp entrega todos os valores já dentro de seus intervalos
    for x in range(len(data)):
        for y in range(4):
            for i in range(ranges-1):
                if i == 0:
                    if float(data[x][y]) <= delta[y][i]:
                        resp[x][y] = 0
                    elif ranges == 2:
                        resp[x][y] = 1

                else:
                    if float(data[x][y]) > delta[y][i]:
                        resp[x][y] = ranges-1
                    elif float(data[x][y]) > delta[y][i - 1] and float(data[x][y]) <= delta[y][i]:
                        resp[x][y] = i

    return resp

def entropia(data=[]):

    #calcula o valor de entropia que mede a homogeneidade dos exemplos
    s = [0 for i in range(len(data))]
    sum = [0 for i in range(len(data))]

    # print("enries", s, "somas: ", sum)

    for x in range(len(data)):

        for y in range(len(data[0])):
            sum[x] += data[x][y]

    # print("somas: ", sum)

    for a in range(len(data)):
        for b in range(len(data[0])):
            # print(a, " a, b", b)
            # print(data[a][b], " number/sum ", sum[a])
            if sum[a] == 0:
                s[a] = 0
                break

            c = data[a][b]/sum[a]
            if c != 0:
                s[a] += -1 * c * math.log(c, 2)

    # print(s)
    return s

def countSort(ranges, data=[], padrao=[]):
    #admitindo padrão = [setosa, versicolor, virginica]
    # conta como é a distribuição os casos de teste por classe para cada amostra
    attributes = len(padrao)

    sortedmatrix = [0 for i in range(len(padrao))]

    for x in range(len(data)):
        # print(data[x])
        # print(map)

        for y in range(len(padrao)):
            if data[x][-1] == padrao[y]:
                sortedmatrix[y] += 1

    sort = []
    sort.append(sortedmatrix)
    # print(sort)
    return sort

def countAttribute(ranges, data=[], padrao=[]):
    #divide os resultados entre os diferentes valores para cada atributo
    # por exemplo, sepal length pode estar dentro de tres faixas de comprimento
    # e cada faixa pode estar dividida entre diferentes espécies da íris
    #já recebe os dados nos ranges discretos

    attributes = len(data[0]) - 1

    resp = [[[0 for i in range(len(padrao))] for j in range(ranges)] for k in range(attributes)]
    # print(resp)

    for x in range(attributes):
        # print(attributes)
    #esse loop poderia ser consertado na corrdenada j da matriz resposta na ordem data > attributes > ranges ficaria teoricamente mais rápido
        for y in range(len(data)):
            # print(data[y])
            if data[y][-1] == padrao[0]:
                resp[x][data[y][x]][0] += 1
            elif data[y][-1] == padrao[1]:
                resp[x][data[y][x]][1] += 1
            elif data[y][-1] == padrao[2]:
                resp[x][data[y][x]][2] += 1
            # print(resp[x])

    # print(resp)
    return resp

def gain(ranges, data=[], sort =[], valuesort=[], padrao=[]):
    #calcula o ganho que um atributo,
    # o parametro indica as mudanças na entropia (no balanço entre quantidades de exemplos com a mesma classe)
    # quando se particiona a classificação através de um atributo

    # print("-------- gain -------------")
    attributes = len(data[0]) - 1
    eSort = entropia(sort)
    # print("esort: ", eSort)
    eAtt = [0 for i in range(attributes)]
    eAux = [0 for i in range(attributes)]
    # print("eaux ", eAux)
    sum = 0
    sortsum = 0

    for x in range(attributes):
        for y in range(ranges):
            sum = 0
            sortsum = 0
            # print("vs", valuesort[x][y])
            for z in range(len(padrao)):
                sum += valuesort[x][y][z]
                sortsum += sort[0][z]
                # print("sum: ", sum, "; sortsum: ", sortsum)

            # print("value sort", valuesort[x][y])
            v = [valuesort[x][y]]
            ent = entropia(v)
            eAux[y] = ent[0]*sum/sortsum
            # print(eAux)

        for w in range(attributes):
            eAtt[x] -= eAux[w]

        eAtt[x] += eSort[0]

    # print(eAtt)
    return eAtt

def subdata(propriedade, faixa, data =[]):
    #busca apenas as instancias de um atributo
    resp = []
    for x in range(len(data)):
        if data[x][propriedade] == faixa:
            resp.append(data[x])
    # print("look at the subdata")
    # print(propriedade," prop, faixa ",faixa)
    # print(resp)
    return resp

def treeWriter(ranges, order=[], data=[], padrao=[]):
    #calcula e escreve a árvore! printamos na tela também
    # mas numa notação específca e não muito amigável, confesso
    attname = ['sepal length', "sepal width", "petal length", "petal width"] #mais uma parte específica pra este problema que poderia ser generalista
    # print("treewriting!")
    # print(order)

    # exceptionControl
    if min(order) == 0:
        print("EXCEPTION!") #ace attorney neles
        return
    #recursion control
    if order[0] == -2:
        #primeira ocorrencia da recursao
        rangedata = rangeSelector(ranges, data)
        order.pop()
        order = [-1 for x in range(len(attname))]
    else:
        rangedata = data

    sort = countSort(ranges, rangedata, padrao)
    # print("sort", sort)
    valuesort = countAttribute(ranges, rangedata, padrao)
    # print("valuesort", valuesort)

    ganho = gain(ranges, rangedata, sort, valuesort, padrao)
    selprop = max(ganho)  # propriedade de ganho máximo, selecionada

    # precisa tratar loop e pegar sempre a mesma propriedade na recursão.
    # Guardar propriedades já pegas pra recursão garantir distribuição? order = vetor?

    ind = ganho.index(selprop)  # identificador da propriedade, índice do vetor ganho

    if order[ind] < 0:
        # print("nova propriedade")
        #primeira ocorrencia da recursão
        # print(order)
        order[ind] = ind
    else:
        # print(order)
        while order[ind] == ind:
            # print("não podemos usar a mesma prop duas vezes")
            if order[ind] == ind:
                ganho[ind] = -1
                selprop = max(ganho)
                ind = ganho.index(selprop)
                # print(ganho)

        order[ind] = ind

    # print("after loop", order)
    # sol = [attname[ind]] #para uma arvore gráfica
    sol = []
    # print(selprop, " (prop)", ind, " (indice de)", attname[ind])
    # print("sol: ", sol)
    tree = [ind]

    for x in range(ranges):
        #x indica qual dos ranges
        # print("in x: ", x, ": ", valuesort[ind][x])
        eAux = entropia([valuesort[ind][x]])
        # print(" e sua entropia: ", eAux)
        if eAux[0] == 0 or (min(order) == 0 and eAux[0] == 1):
            for y in range(ranges):
                # print("folha!")
                #y indica qual das classes
                if valuesort[ind][x][y] != 0:
                    sol.append(padrao[y])
                    # print(sol)
                    break
                if max(valuesort[ind][x]) == 0:
                    sol.append("*")
                    # print(sol)
                    break
        else:
            # print("galho")
            dataux = subdata(ind, x, rangedata)
            dfsol = treeWriter(ranges, order, dataux, padrao)
            sol.append(dfsol)
            # print(sol)

    tree.append(sol)
    # print(tree)
    return tree

def classify (index, tree=[], testcase = []):
    #o real classificador que percorre a árvore e faz seu trabalho e forma eficiente
    answer = 0
    # print(index, " at tree: ", tree)
    # print("case: ", testcase)
    if isinstance(tree[0], int):
       answer = classify(tree[0], tree[1], testcase)

    else:
        for x in range(len(tree)):
            # print("at ", x)
            if isinstance(tree[x], str):
                # print(tree[x])
                if testcase[index] == x:
                    # print(testcase[index])
                    if testcase[-1] == tree[x]:
                        # print(testcase[-1])
                        answer += 1
                        # print("ohmigod, ", answer)
                        return answer

            elif isinstance(tree[x], list):
               answer = classify(x, tree[x], testcase)
               break

    return answer

def gini(order = [], tree =[]):
    #initial order must be = [0,0,0,0,0]
    #método para impureza de gini que indica erros na classificação
    for x in range(len(tree)):
        if isinstance(tree[x], list):
            gini(order, tree[x])
        else:
            if isinstance(tree[x], int):
                order[tree[x]] += 1
                order[-1] += 1

#-----------execute--------------

treinamento = []
test = []
dadosCsv("iris.data.txt", 0.66, treinamento, test)
padrao = ['Iris-setosa', 'Iris-versicolor', 'Iris-virginica']
# print(test)
faixa = 3
testa = rangeSelector(faixa, test)
# print("testa", testa)
# print(" random ")
# random.shuffle(treinamento)
# treinamento = subset(50, treinamento)
# print(treinamento)

#samples
training = [['5.7', '2.9', '4.2', '1.3', 'Iris-versicolor'], ['6.1', '3.0', '4.9', '1.8', 'Iris-virginica'], ['6.1', '2.6', '5.6', '1.4', 'Iris-virginica'], ['5.4', '3.0', '4.5', '1.5', 'Iris-versicolor'], ['6.5', '3.0', '5.5', '1.8', 'Iris-virginica'], ['5.5', '4.2', '1.4', '0.2', 'Iris-setosa'], ['6.7', '3.0', '5.2', '2.3', 'Iris-virginica'], ['4.6', '3.2', '1.4', '0.2', 'Iris-setosa'], ['6.1', '2.8', '4.7', '1.2', 'Iris-versicolor'], ['5.1', '3.8', '1.6', '0.2', 'Iris-setosa']]
# training = [['5.7', '2.5', '5.0', '2.0', 'Iris-virginica'], ['5.2', '2.7', '3.9', '1.4', 'Iris-versicolor'], ['6.7', '3.1', '4.4', '1.4', 'Iris-versicolor'], ['4.8', '3.0', '1.4', '0.1', 'Iris-setosa'], ['6.3', '2.9', '5.6', '1.8', 'Iris-virginica'], ['7.7', '2.8', '6.7', '2.0', 'Iris-virginica'], ['5.4', '3.0', '4.5', '1.5', 'Iris-versicolor'], ['4.5', '2.3', '1.3', '0.3', 'Iris-setosa'], ['5.0', '3.4', '1.5', '0.2', 'Iris-setosa'], ['7.7', '3.0', '6.1', '2.3', 'Iris-virginica']]
# training = [['6.5', '3.0', '5.8', '2.2', 'Iris-virginica'], ['4.4', '3.2', '1.3', '0.2', 'Iris-setosa'], ['6.7', '3.1', '4.4', '1.4', 'Iris-versicolor'], ['7.7', '2.6', '6.9', '2.3', 'Iris-virginica'], ['6.3', '2.7', '4.9', '1.8', 'Iris-virginica'], ['6.4', '3.1', '5.5', '1.8', 'Iris-virginica'], ['5.1', '3.3', '1.7', '0.5', 'Iris-setosa'], ['5.0', '3.4', '1.5', '0.2', 'Iris-setosa'], ['6.2', '2.8', '4.8', '1.8', 'Iris-virginica'], ['6.2', '2.2', '4.5', '1.5', 'Iris-versicolor'], ['6.3', '2.5', '5.0', '1.9', 'Iris-virginica'], ['4.8', '3.4', '1.9', '0.2', 'Iris-setosa'], ['6.8', '2.8', '4.8', '1.4', 'Iris-versicolor'], ['5.1', '3.8', '1.6', '0.2', 'Iris-setosa'], ['7.7', '3.8', '6.7', '2.2', 'Iris-virginica'], ['5.6', '3.0', '4.1', '1.3', 'Iris-versicolor'], ['5.2', '2.7', '3.9', '1.4', 'Iris-versicolor'], ['6.5', '3.2', '5.1', '2.0', 'Iris-virginica'], ['6.0', '2.7', '5.1', '1.6', 'Iris-versicolor'], ['4.8', '3.4', '1.6', '0.2', 'Iris-setosa']]
training = rangeSelector(faixa, training)
# print("ranged training", training)
# print("sort")

#1 sample
test1 = [[0, 1, 0, 0, 'Iris-setosa'], [0, 1, 0, 0, 'Iris-setosa'], [0, 1, 0, 0, 'Iris-setosa'], [0, 1, 0, 0, 'Iris-setosa'], [0, 1, 0, 0, 'Iris-setosa'], [1, 2, 0, 0, 'Iris-setosa'], [0, 1, 0, 0, 'Iris-setosa'], [0, 1, 0, 0, 'Iris-setosa'], [0, 1, 0, 0, 'Iris-setosa'], [0, 1, 0, 0, 'Iris-setosa'], [1, 2, 0, 0, 'Iris-setosa'], [0, 1, 0, 0, 'Iris-setosa'], [0, 1, 0, 0, 'Iris-setosa'], [0, 1, 0, 0, 'Iris-setosa'], [1, 2, 0, 0, 'Iris-setosa'], [1, 2, 0, 0, 'Iris-setosa'], [2, 1, 1, 1, 'Iris-versicolor'], [1, 1, 1, 1, 'Iris-versicolor'], [2, 1, 2, 1, 'Iris-versicolor'], [1, 0, 1, 1, 'Iris-versicolor'], [1, 0, 1, 1, 'Iris-versicolor'], [1, 0, 1, 1, 'Iris-versicolor'], [1, 1, 1, 1, 'Iris-versicolor'], [0, 0, 1, 1, 'Iris-versicolor'], [2, 1, 1, 1, 'Iris-versicolor'], [0, 0, 1, 1, 'Iris-versicolor'], [0, 0, 1, 1, 'Iris-versicolor'], [1, 1, 1, 1, 'Iris-versicolor'], [1, 0, 1, 1, 'Iris-versicolor'], [1, 1, 1, 1, 'Iris-versicolor'], [1, 1, 1, 1, 'Iris-versicolor'], [2, 1, 1, 1, 'Iris-versicolor'], [1, 1, 2, 2, 'Iris-virginica'], [1, 0, 2, 2, 'Iris-virginica'], [2, 1, 2, 2, 'Iris-virginica'], [1, 1, 2, 2, 'Iris-virginica'], [1, 1, 2, 2, 'Iris-virginica'], [2, 1, 2, 2, 'Iris-virginica'], [0, 0, 1, 1, 'Iris-virginica'], [2, 1, 2, 2, 'Iris-virginica'], [2, 0, 2, 2, 'Iris-virginica'], [2, 1, 2, 2, 'Iris-virginica'], [1, 1, 2, 2, 'Iris-virginica'], [1, 0, 2, 2, 'Iris-virginica'], [2, 1, 2, 2, 'Iris-virginica'], [1, 0, 2, 2, 'Iris-virginica'], [1, 0, 2, 2, 'Iris-virginica'], [1, 1, 2, 2, 'Iris-virginica']]
# #3 sample
test3 = [[0, 1, 0, 0, 'Iris-setosa'], [0, 2, 0, 0, 'Iris-setosa'], [0, 2, 0, 0, 'Iris-setosa'], [0, 2, 0, 0, 'Iris-setosa'], [0, 1, 0, 0, 'Iris-setosa'], [1, 2, 0, 0, 'Iris-setosa'], [0, 2, 0, 0, 'Iris-setosa'], [0, 2, 0, 0, 'Iris-setosa'], [0, 2, 0, 0, 'Iris-setosa'], [0, 1, 0, 0, 'Iris-setosa'], [0, 2, 0, 0, 'Iris-setosa'], [0, 0, 0, 0, 'Iris-setosa'], [0, 2, 0, 0, 'Iris-setosa'], [0, 1, 0, 0, 'Iris-setosa'], [1, 1, 1, 1, 'Iris-versicolor'], [2, 1, 2, 1, 'Iris-versicolor'], [0, 0, 1, 1, 'Iris-versicolor'], [1, 1, 1, 1, 'Iris-versicolor'], [0, 1, 1, 1, 'Iris-versicolor'], [0, 0, 1, 1, 'Iris-versicolor'], [1, 1, 1, 1, 'Iris-versicolor'], [1, 0, 1, 1, 'Iris-versicolor'], [1, 1, 1, 1, 'Iris-versicolor'], [1, 1, 1, 1, 'Iris-versicolor'], [1, 1, 1, 1, 'Iris-versicolor'], [2, 1, 2, 1, 'Iris-versicolor'], [1, 1, 2, 1, 'Iris-versicolor'], [1, 1, 1, 1, 'Iris-versicolor'], [1, 1, 1, 1, 'Iris-versicolor'], [0, 1, 1, 1, 'Iris-versicolor'], [1, 0, 1, 1, 'Iris-versicolor'], [1, 1, 1, 1, 'Iris-versicolor'], [0, 0, 1, 1, 'Iris-versicolor'], [1, 1, 1, 1, 'Iris-versicolor'], [1, 1, 1, 1, 'Iris-versicolor'], [1, 1, 1, 1, 'Iris-versicolor'], [1, 2, 2, 2, 'Iris-virginica'], [1, 1, 2, 2, 'Iris-virginica'], [2, 1, 2, 2, 'Iris-virginica'], [0, 0, 1, 1, 'Iris-virginica'], [1, 0, 2, 2, 'Iris-virginica'], [1, 0, 2, 1, 'Iris-virginica'], [1, 1, 2, 2, 'Iris-virginica'], [1, 1, 2, 2, 'Iris-virginica'], [1, 1, 2, 2, 'Iris-virginica'], [2, 2, 2, 2, 'Iris-virginica'], [2, 1, 2, 2, 'Iris-virginica'], [1, 1, 2, 2, 'Iris-virginica'], [2, 1, 2, 2, 'Iris-virginica'], [1, 1, 2, 2, 'Iris-virginica'], [1, 2, 2, 2, 'Iris-virginica']]
# #2 sample
test2 = [[0, 1, 0, 0, 'Iris-setosa'], [0, 0, 0, 0, 'Iris-setosa'], [0, 1, 0, 0, 'Iris-setosa'], [1, 2, 0, 0, 'Iris-setosa'], [0, 2, 0, 0, 'Iris-setosa'], [0, 1, 0, 0, 'Iris-setosa'], [0, 1, 0, 0, 'Iris-setosa'], [0, 1, 0, 0, 'Iris-setosa'], [0, 2, 0, 0, 'Iris-setosa'], [0, 1, 0, 0, 'Iris-setosa'], [0, 1, 0, 0, 'Iris-setosa'], [0, 1, 0, 0, 'Iris-setosa'], [0, 1, 0, 0, 'Iris-setosa'], [0, 1, 0, 0, 'Iris-setosa'], [1, 1, 1, 1, 'Iris-versicolor'], [2, 1, 1, 1, 'Iris-versicolor'], [0, 0, 1, 1, 'Iris-versicolor'], [1, 1, 1, 1, 'Iris-versicolor'], [1, 0, 1, 1, 'Iris-versicolor'], [2, 1, 1, 1, 'Iris-versicolor'], [1, 0, 1, 1, 'Iris-versicolor'], [1, 0, 1, 1, 'Iris-versicolor'], [1, 1, 1, 1, 'Iris-versicolor'], [1, 0, 1, 1, 'Iris-versicolor'], [1, 0, 1, 1, 'Iris-versicolor'], [0, 0, 1, 1, 'Iris-versicolor'], [1, 0, 2, 1, 'Iris-versicolor'], [0, 1, 1, 1, 'Iris-versicolor'], [0, 0, 1, 1, 'Iris-versicolor'], [1, 1, 1, 1, 'Iris-versicolor'], [1, 0, 1, 1, 'Iris-versicolor'], [0, 0, 0, 1, 'Iris-versicolor'], [1, 0, 2, 2, 'Iris-virginica'], [2, 1, 2, 2, 'Iris-virginica'], [1, 1, 2, 2, 'Iris-virginica'], [2, 1, 2, 2, 'Iris-virginica'], [2, 0, 2, 2, 'Iris-virginica'], [1, 0, 2, 2, 'Iris-virginica'], [1, 1, 2, 2, 'Iris-virginica'], [2, 2, 2, 2, 'Iris-virginica'], [2, 0, 2, 2, 'Iris-virginica'], [1, 0, 1, 1, 'Iris-virginica'], [1, 0, 1, 2, 'Iris-virginica'], [2, 0, 2, 2, 'Iris-virginica'], [2, 1, 2, 2, 'Iris-virginica'], [1, 0, 2, 2, 'Iris-virginica'], [2, 0, 2, 2, 'Iris-virginica'], [1, 0, 2, 1, 'Iris-virginica'], [1, 1, 2, 2, 'Iris-virginica'], [1, 1, 2, 2, 'Iris-virginica'], [2, 1, 2, 2, 'Iris-virginica'], [1, 0, 2, 2, 'Iris-virginica'], [2, 1, 2, 2, 'Iris-virginica'], [2, 1, 2, 2, 'Iris-virginica'], [1, 1, 2, 2, 'Iris-virginica'], [1, 1, 2, 2, 'Iris-virginica'], [1, 1, 2, 2, 'Iris-virginica']]


#dados
# sortidos = countSort(faixa, treinamento, padrao)

# print(sortidos)
sortidos = countSort(3, training, padrao)

# print("training: ", sortidos)
sortudos = countSort(faixa, test, padrao)
# print("testes", sortudos)

# print("attribute sort")
atributos = countAttribute(3, training, padrao)
# print(atributos)

#resultados
print("----------------------")
#
# tree = treeWriter(faixa, [-2], treinamento, padrao)
tree = treeWriter(3, [-2], training, padrao)
print(tree)

# order = [0,0,0,0,0]
# gini(order, tree)
# print(order)

#casos de teste
#caso 1

print("teste 1 casos [16.16.16]")
acertos = 0
vetorAcertos = [0, 0, 0]

for x in range(len(test1)):
    # print(test1[x])
    ponto = classify(-1, tree, test1[x])

    if ponto != 0:
        if test1[x][-1] == padrao[0]:
            vetorAcertos[0]+=1
        if test1[x][-1] == padrao[1]:
            vetorAcertos[1]+=1
        if test1[x][-1] == padrao[2]:
            vetorAcertos[2]+=1

    acertos += ponto

print("a taxa de acerto é: ", 100 * acertos/len(test1), "%")
print(vetorAcertos)

# #caso2
# print("teste 2:casos  [[14, 18, 25]]")
# acertos = 0
# vetorAcertos = [0, 0, 0]
#
# for x in range(len(test2)):
#     # print(test[x])
#     ponto = classify(-1, tree, test2[x])
#
#     if ponto != 0:
#         if test2[x][-1] == padrao[0]:
#             vetorAcertos[0]+=1
#         if test2[x][-1] == padrao[1]:
#             vetorAcertos[1]+=1
#         if test2[x][-1] == padrao[2]:
#             vetorAcertos[2]+=1
#
#     acertos += classify(-1, tree, test2[x])
#
# print("a taxa de acerto é: ", 100 * acertos/len(test2), "%")
# print(vetorAcertos)
#
# #caso3
# print("teste 3: casos  [[14, 22, 15]]")
# acertos = 0
# vetorAcertos = [0, 0, 0]
#
# for x in range(len(test3)):
#     # print(test[x])
#     ponto = classify(-1, tree, test3[x])
#
#     if ponto != 0:
#         if test3[x][-1] == padrao[0]:
#             vetorAcertos[0]+=1
#         if test3[x][-1] == padrao[1]:
#             vetorAcertos[1]+=1
#         if test3[x][-1] == padrao[2]:
#             vetorAcertos[2]+=1
#
#     acertos += classify(-1, tree, test3[x])
#
# print("a taxa de acerto é: ", 100 * acertos/len(test3), "%")
# print(vetorAcertos)
#
# print("teste aleatório: casos", sortudos)
# acertos = 0
# vetorAcertos = [0, 0, 0]
#
# for x in range(len(test)):
#     # print(test[x])
#     ponto = classify(-1, tree, test[x])
#
#     if ponto != 0:
#         if test[x][-1] == padrao[0]:
#             vetorAcertos[0]+=1
#         if test[x][-1] == padrao[1]:
#             vetorAcertos[1]+=1
#         if test[x][-1] == padrao[2]:
#             vetorAcertos[2]+=1
#
#     acertos += classify(-1, tree, test[x])
#
# print("a taxa de acerto é: ", 100 * acertos/len(test), "%")
# print(vetorAcertos)
