#usando o mesmo framework de importação e classificação dos dados da árvore de decisão
import random
from DecisionTree import dadosCsv, treeWriter, rangeSelector, countSort, countAttribute, subset, entropia, subdata, gain, classify, gini

def classifierAdapted (index, tree=[], testcase = []):
    #adaptei o classificador da árvore de decisão
    answer = 0
    padrao = ['Iris-setosa', 'Iris-versicolor', 'Iris-virginica']
    # print(index, " at tree: ", tree)
    # print("case: ", testcase)
    if isinstance(tree[0], int):
       answer = classifierAdapted(tree[0], tree[1], testcase)

    else:
        for x in range(len(tree)):
            # print("at ", x)
            if isinstance(tree[x], str):
                # print(tree[x])
                if testcase[index] == x:
                    if tree[x] in padrao:
                        answer = tree[x]
                        return answer
                    # print(testcase[index])
                    # if testcase[-1] == tree[x]:
                    #     # print(testcase[-1])
                    #     answer += 1
                    #     # print("ohmigod, ", answer)
                    #     return answer

            elif isinstance(tree[x], list):
               answer = classifierAdapted(x, tree[x], testcase)
               break

    return answer

#execute
print("datbuild") #construir os dados
treinamento = []
test = []
dadosCsv("iris.data.txt", 0.66, treinamento, test)
#a ideia vai ser pegar em torno de 120 casos de treinamento e 30 de teste.
# os 120 casos de treinamento vão ser embaralhados e criados subsets de 12 casos para criação de uma árvore de decisão
#a expectativa é que em cada iteração seja criado um subset diferente, com pouquísimas coincidencias
#a floresta criada

padrao = ['Iris-setosa', 'Iris-versicolor', 'Iris-virginica']
# attname = ['sepal length', "sepal width", "petal length", "petal width"]

faixa = 3 #numero de intervalos pra classificação, igual ao numero de valores que queremos classificar
numeroarvores = 500
conjuntotreino=[]
contatreinos=[]
floresta=[]

#gera um numero de arvores para a random forest. para gerar árvores não-aleatórias para a classificação de cada amostra
for numero in range(numeroarvores):
    random.shuffle(treinamento)
    treino = subset(10, treinamento)
    sortx = countSort(faixa, treino, padrao)
    contatreinos.append(sortx)
    conjuntotreino.append(treino)
    trees = treeWriter(faixa, [-2], treino, padrao)
    floresta.append(trees)
    print(sortx, ":", trees)

test = rangeSelector(faixa, test)
#sample
# test = [[0, 1, 0, 0, 'Iris-setosa'], [0, 1, 0, 0, 'Iris-setosa'], [1, 2, 0, 0, 'Iris-setosa'], [0, 1, 0, 0, 'Iris-setosa'],  [1, 2, 0, 0, 'Iris-setosa'], [0, 1, 0, 0, 'Iris-setosa'], [1, 2, 0, 0, 'Iris-setosa'], [1, 2, 0, 0, 'Iris-setosa'], [2, 1, 1, 1, 'Iris-versicolor'], [1, 1, 1, 1, 'Iris-versicolor'], [1, 0, 1, 1, 'Iris-versicolor'], [0, 0, 1, 1, 'Iris-versicolor'], [1, 0, 1, 1, 'Iris-versicolor'], [1, 1, 1, 1, 'Iris-versicolor'], [1, 1, 1, 1, 'Iris-versicolor'], [2, 1, 1, 1, 'Iris-versicolor'], [1, 1, 2, 2, 'Iris-virginica'], [1, 0, 2, 2, 'Iris-virginica'], [2, 1, 2, 2, 'Iris-virginica'], [0, 0, 1, 1, 'Iris-virginica'], [2, 0, 2, 2, 'Iris-virginica'], [2, 1, 2, 2, 'Iris-virginica'], [1, 1, 2, 2, 'Iris-virginica'], [1, 0, 2, 2, 'Iris-virginica'], [1, 0, 2, 2, 'Iris-virginica']]
print("testa", test)
sortudos = countSort(faixa, test, padrao)
print("testes", sortudos)

order = [0,0,0,0,0]
ans = []
score = 0

#tree loop
print("reserva de mata atlantica | entrada somente pessoas autorizadas")

for i in range(len(test)):
    vetorAcerto = [0, 0, 0, 0]
    print("----------------testcase(",i,"):", test[i],"---------------")
    vetorAcerto[-1] = padrao.index(test[i][-1])
    # resultados da classificação splitados. Último termo é o índice da classe correta

    for x in range(numeroarvores):
        tree = floresta[x]
        # print("*** tree(", x, "):", tree)
        gini(order, tree)

        classe = classifierAdapted(-1, tree, test[i])
        # print(" encontrou: ", classe)

        if classe == padrao[0]:
            vetorAcerto[0]+=1
        if classe == padrao[1]:
            vetorAcerto[1]+=1
        if classe == padrao[2]:
            vetorAcerto[2]+=1

        # print(classe, ":", rightbaby, "tree: ", tree)

        # print("-------next-------")
    print("results: ", vetorAcerto)
    ans.append(vetorAcerto)
    n = max(vetorAcerto)
    m = vetorAcerto.index(n)

    if m == vetorAcerto[-1]:
        score+=1

    # print(n, m, score)


print("gini: ", order)
print("taxa de acerto: ",100*score/(len(test)),"%")
print(ans)
