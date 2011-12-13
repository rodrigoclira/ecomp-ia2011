#-*- coding: utf-8 -*-

from random import randint
from math import e
from random import choice

LINEAR = 1
SIGMOIDE = 2 

class Neuronio():
    def __init__(self,seq,peso=randint(1,10),entrada=1):
            self.peso=peso
            self.seq = seq
            self.entrada=entrada

    def calcular(self):
            return self.peso*self.entrada

    def __str__(self):
        return u"%02d | Entrada: %f | Peso: %f" %(self.seq,self.entrada,self.peso)
        
class RedeNeural():
        def __init__(self,tipo,numeroNeuronios,pesos_iniciais,bias,alfa,ciclos=0):

            self.rede = []
            self.bias = bias
            self._inserir_neuronios(pesos_iniciais,numeroNeuronios)
            self.alfa = alfa
            self.ciclos = ciclos
            self.tipo = tipo
            self.erros = []
            self.verbose = True
            if tipo == LINEAR:
                self.func = linear
                self.derivada = lambda yi: 1
            elif tipo == SIGMOIDE:
                self.func = sigmoide
                self.derivada = lambda yi : yi*(1-yi)
           

            
        def _inserir_neuronios(self,pesos,numeroNeuronios=1):
            #inserir o bias
            self.rede.append(Neuronio(seq=0,peso = pesos[0], entrada=self.bias))

            if numeroNeuronios>0:
                cont=0
                while cont<numeroNeuronios:
                    self.rede.append(Neuronio(seq=cont+1,peso = pesos[cont+1]))
                    cont+=1
            else:
                raise u"Valor de neurônios inválido"

#        def numero_ciclos(self,numero):
#            self.ciclos = numero

        def _preencher_ordem(self,entrada,ordem_exemplos):

            if not ordem_exemplos:
                ordem_exemplos = map(lambda _: [], range(self.ciclos))

            cont=0                
            while cont<self.ciclos:
                ordem = ordem_exemplos[cont]

                if not ordem:
                    for numero in range(len(entrada)):
                        ordem.append(numero)
                cont+=1

        #    print ordem_exemplos
            return ordem_exemplos
        
        def treinamento(self,entrada,saida,ordem_exemplos=None):

            if self.verbose:
            
                print ''.center(50,'-'),'\n'
                print ' INICIO DA ETAPA DE TREINAMENTO '.center(50),'\n'
                print ''.center(50,'-'),'\n'
            
            ordem_exemplos = self._preencher_ordem(entrada,ordem_exemplos)
            resposta = 0
            contCiclos = 0
            resposta_saida = 0
            
            while contCiclos<self.ciclos:
                if self.verbose:
                    print ('Ciclo: %d\n' % (contCiclos+1)).center(50)
                contExemplos = 0
               
                while contExemplos<len(entrada): # Quantidade de exemplos de resposta
                    exemplo = ordem_exemplos[contCiclos][contExemplos]

                    if self.verbose:
                        print 'Exemplo:',exemplo+1,'\n'

                    resposta = 0            # para treinar a rede
                    resposta_saida = 0
                    numero_neuronio=0
                    
                    while numero_neuronio<len(self.rede):
                        neuronio = self.rede[numero_neuronio]
                        if numero_neuronio != 0:
                            neuronio.entrada = entrada[exemplo][numero_neuronio-1]

                        numero_neuronio+=1

                    net=0
                    for neuronio in self.rede:
                        if self.verbose:
                            print neuronio
                        net += neuronio.calcular()

                    if self.verbose:
                        print 'net: %f' % (net)

                    resposta = self.func(net)            
                    resposta_saida = saida[exemplo]

                    if self.verbose:
                        print 'Resposta conseguida: %f | Resposta Esperada: %f | e2: %f' %(resposta,resposta_saida,self.erro_quadrado(resposta,resposta_saida)),
                    
                    if resposta == resposta_saida:
                        if self.verbose:
                            print '\nOk!\n'
                    else:
                        if self.verbose:
                            print '\nRecalcular os pesos\n'

                        numero_neuronio = 0
                        while numero_neuronio < len(self.rede):
                            neuronio = self.rede[numero_neuronio]
                            neuronio.peso = self.novo_peso(neuronio,resposta,resposta_saida)
#                            neuronio.peso = neuronio.peso + self.alfa*(resposta_saida - resposta)*neuronio.entrada
                            numero_neuronio+=1

                    if self.verbose:
                        print ''.center(50,'-'),'\n'    
                    contExemplos += 1
                if self.verbose:
                    print (u'ERRO MÉDIO DO CICLO: %f\n' % self.erro_quadrado_medio()).center(50)
                self.erros = []
                contCiclos+=1
            if self.verbose:
                print 'FIM DA ETAPA DE TREINAMENTO'.center(50),'\n'
                print ''.center(50,'-'),'\n'

        def erro_quadrado(self,resposta_obtida,resposta_esperada,salvar=True):
            
            e2 = (resposta_esperada-resposta_obtida)**2
            if salvar:
                self.erros.append(e2)
            return e2
                

        def erro_quadrado_medio(self):
            return (reduce(lambda x,y: x+y,self.erros,0)/float(len(self.erros)))
        
        
        def novo_peso(self,neuronio,resposta_obtida,resposta_esperada):
            return neuronio.peso + self.alfa*(resposta_esperada-resposta_obtida)*neuronio.entrada*self.derivada(resposta_obtida)

            
        def executar(self,entrada):
            resposta = 0
            numero_neuronio=0
            while numero_neuronio<len(self.rede):
                neuronio = self.rede[numero_neuronio]
                if numero_neuronio != 0:
                    neuronio.entrada = entrada[numero_neuronio-1]

                numero_neuronio+=1

            net=0
            print ''
            for neuronio in self.rede:
                print neuronio
                net += neuronio.calcular()

            print 'net: %f' % (net)

            resposta = self.func(net)

            return resposta
         
def degrau(numero):
    return 1 if numero>=0 else 0

def linear(numero):
    return numero

def sigmoide(numero):
    return 1/(1+e**-(numero))

            
if __name__ == '__main__':
  

    saida = [  0.19,
               0.11,
               0.60,
               0.31,
               0.52,
               0.39,
            ] 

    entrada = [ 
		[.3,.1,.1],
	        [.03,.02,0],
		[1,1,1],
		[.4,0.15,1],
		[.9,.8,.8],
		[.5,.5,.9]
	      ]
	
               
    # Iniciar os pesos com 0

    pesos0 = [0,0,0,0]
    rede = RedeNeural(LINEAR,3,pesos0,1,0.5,3)

    # Ordem da apresentação dos exemplos	
    ordem = [
                [1,2,3,4,5,6],
                [3,6,5,2,1,4],
                [5,4,1,6,3,2],
                [6,1,2,5,4,3],
                [2,3,4,1,6,5],
                [4,5,6,3,2,1],
                [1,2,3,4,5,6],
                [3,6,5,2,1,4],
                [5,4,1,6,3,2],
                [6,1,2,5,4,3],
                [2,3,4,1,6,5],
                [4,5,6,3,2,1]
            ]

    ordem = map(lambda x: [n-1 for n in x ] , ordem)
    rede.verbose = True

    #Treinar a rede
    rede.treinamento(entrada,saida,ordem) 


    #Calcular o valor do nível de água para os valores  (.7, .6, .85)
    resposta = rede.executar([.7,.6,.85])
    print u'\nNível da água: ',resposta

