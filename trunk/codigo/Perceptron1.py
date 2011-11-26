#-*- coding: utf-8 -*-

from random import randint

class Neuronio():
    def __init__(self,seq,peso=randint(1,10),entrada=1):
            self.peso=peso
            self.seq = seq
            self.entrada=entrada

    def calcular(self):
            return self.peso*self.entrada

    def __str__(self):
        return u"%02d | Entrada: %d | Peso: %d" %(self.seq,self.entrada,self.peso)
        
class RedeNeural():
        def __init__(self,numeroNeuronios,pesos_iniciais,bias,alfa,ciclos=0):

            self.rede = []
            self.bias = bias
            self._inserir_neuronios(pesos_iniciais,numeroNeuronios)
            self.alfa = alfa
            self.ciclos = ciclos
            
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
            
            print ''.center(50,'-'),'\n'
            print ' INICIO DA ETAPA DE TREINAMENTO '.center(50),'\n'
            print ''.center(50,'-'),'\n'
            
            ordem_exemplos = self._preencher_ordem(entrada,ordem_exemplos)
            resposta = 0
            contCiclos = 0
            resposta_saida = 0
            print ordem_exemplos
            while contCiclos<self.ciclos:
                print ('Ciclo: %d\n' % (contCiclos+1)).center(50)
                contExemplos = 0
               
                while contExemplos<len(entrada): # Quantidade de exemplos de resposta
                    exemplo = ordem_exemplos[contCiclos][contExemplos]
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
                        print neuronio
                        net += neuronio.calcular()

                    print 'net: %d' % (net)

                    # Função Degrau 
                    if net>=0:
                        resposta = 1
                    else:
                        resposta = 0
            
                    resposta_saida = saida[exemplo]
                    print 'Resposta conseguida: %d | Resposta Esperada: %d |' %(resposta,resposta_saida),
                    if resposta == resposta_saida:
                        print 'Ok!\n'
                    else:
                        print 'Recalcular os pesos\n'

                        numero_neuronio = 0
                        while numero_neuronio < len(self.rede):
                            neuronio = self.rede[numero_neuronio]
                            neuronio.peso = neuronio.peso + self.alfa*(resposta_saida - resposta)*neuronio.entrada
                            numero_neuronio+=1
                    
                    print ''.center(50,'-'),'\n'    
                    contExemplos += 1
                contCiclos+=1
            print 'FIM DA ETAPA DE TREINAMENTO'.center(50),'\n'
            print ''.center(50,'-'),'\n'

        def execultar(self,entrada):
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

            print 'net: %d' % (net)

            if net>=0:
                resposta = 1
            else:
                resposta = 0

            return resposta
         

            
if __name__ == '__main__':
    #exemplo1
    #entrada = [ [0,0], [0,1], [1,0], [1,1]  ]
    #saida = [0,0,0,1]
    #pesos = [0,3,3]

    entrada = [ [-1,-1,1], # Galinha
                [1,-1,1], # Elefante
                [-1,-1,-1], # Peixe
                [1,1,-1], # Ornitorrinco
                [-1,1,1], # Escorpiao
                [1,-1,-1]] # baleia

    saida = [0,1,0,1,0,1]
    pesos0 = [-1,-1,-1,-1]
    rede = RedeNeural(3,pesos0,1,1,2)

    
    rede.treinamento(entrada,saida,[[],[2,5,4,1,0,3]])


    resultado = rede.execultar([1,1,1])
    print 'Equidina: ',resultado

    resultado = rede.execultar([0,1,0])
    print 'Anaconda: ',resultado
    
    
    """
    entrada = [[1,1,1,0,1,0,0,1,0],[1,0,1,1,1,1,1,0,1]]
    entrada = [[1,1,1,0,1,0,0,1,0],[0,1,0,0,1,0,0,1,0]]
    saida = [1,0,1]
    pesos = [0]*10
    rede  = RedeNeural(9,pesos,1,1,3)
    rede.treinamento(entrada,saida)

    resultado = rede.comparar([1,1,1,1,1,1,0,1,0])
    print 'T modifificado: %d \n'%resultado
    resultado = rede.comparar([1,0,0,1,1,1,1,0,1])
    print 'H modificado: ',resultado

    resultado = rede.comparar([1]*9)
    print 'Matriz completa: ',resultado

    resultado = rede.comparar([0,1,0,0,1,0,1,1,1])
    print 'T invertido 180: ',resultado
    """

#    for neuronio in rede.rede:
#        print neuronio

