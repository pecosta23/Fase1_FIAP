from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score

acao1 = [1,0,1] #AAPL
acao2 = [0,1,0] #GOOGL
acao3 = [1,1,1] #MSFT
acao4 = [0,0,1] #AMZN
acao5 = [1,1,0] #TSLA
acao6 = [0,1,1] #FB

dados_treino = [acao1, acao2, acao3, acao4, acao5, acao6]
rotulos_treino = [1,1,1,0,0,0] # 1 = alta, 0 = baixa

#iniciando modelo SVC
modelo = LinearSVC()
modelo.fit(dados_treino, rotulos_treino)

#conjunto de teste
teste1 = [1,0,0]
teste2 = [0,1,1]
teste3 = [1,1,0]

dados_teste = [teste1, teste2, teste3]
rotulos_teste = [1,0,1]

#fazendo previsões
previsoes = modelo.predict(dados_teste)

#Avaliar a precisao do modelo
taxa_acerto = accuracy_score(rotulos_teste, previsoes)
print("Taxa de acerto %.2f%%" % (taxa_acerto * 100))

