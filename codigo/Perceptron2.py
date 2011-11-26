#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Rodrigo Lira v2.0

from random import randint,choice


class RedeException(Exception):
    def __init__(self,msg):
        Exception.__init__(self,msg)


class Neuronio():
    def __init__(self,identificador,entrada=0,peso=[]):
        self.pesos = peso
        self.entrada = entrada
        self.identificador = identificador

    def calcular(self,posicao):
        return self.pesos[posicao]*self.entrada

    def __str__(self):
        return (u"%02d | Entrada: %2d | Peso: %s" %(self.identificador,self.entrada,','.join(str(x) for x in self.pesos)))

class RedeNeural():
    def __init__(self,quantidade_neuronios,pesos_iniciais,bias,alfa,numero_ciclos=0,quantidade_saidas=1):
        self.rede = []
        self.alfa = alfa
        self.bias = bias
        self.quantidade_saida = quantidade_saidas
        self.ciclos = numero_ciclos
        self.pesos_iniciais = pesos_iniciais
        self._inserir_neuronios(quantidade_neuronios)

    def _get_pesos(self,posicao):
        """
        FUNC: _get_pesos
        @posicao
        
        Pega no vetor pesos o pesos da posicao do Neurônio.
        """
        return [vetor[posicao] for vetor in self.pesos_iniciais]
    
    def _inserir_neuronios(self,quantidade_neuronios):
        """
        FUNC: _inserir_neuronios
        @quantidade_neuronios

        Inseri na rede os Neurônios
        """

        self.rede.append(Neuronio(identificador=0,entrada=self.bias,peso=self._get_pesos(0)))

        if quantidade_neuronios>0:
            cont=0
            while cont<quantidade_neuronios:
                self.rede.append(Neuronio(identificador=cont+1,peso=self._get_pesos(cont+1)))
                cont+=1
        else:
            raise (u'Valor de neurônios inválidos')


    def _preencher_ordem(self,exemplos,ordem_exemplos):
        
        if not ordem_exemplos:
            ordem_exemplos = map(lambda _: [],range(self.ciclos))

        cont=0
        while cont<self.ciclos:
            ordem = ordem_exemplos[cont]

            if not ordem:
                ordem_exemplos[cont] = range(len(exemplos))

            elif len(ordem) != len(exemplos):
                raise RedeException('Quantidade incorreta de valores na ordem do ciclo %d' %cont+1)
            cont+=1
        return ordem_exemplos

    def degrau(self,valor):
        return 1 if valor>=0 else 0

    def soma_funcoes(self,posicao,verbose=False):
        net = 0
        for neuronio in self.rede:
            if verbose:
                print neuronio
            net+=neuronio.calcular(posicao)
        return net

    def treinar(self,exemplos,saida,ordem_exemplos=[]):

        print ''.center(50,'-'),'\n'
        print ' INICIO DA ETAPA DE TREINAMENTO '.center(50),'\n'
        print ''.center(50,'-'),'\n'

        ordem_exemplos = self._preencher_ordem(exemplos,ordem_exemplos)

        contCiclos = 0
        
        while contCiclos<self.ciclos:

            print ('Ciclo: %d\n' %(contCiclos+1)).center(50)
            contExemplos = 0
            acertos = 0
            while contExemplos<len(exemplos):
                exemplo = ordem_exemplos[contCiclos][contExemplos]

                print 'Exemplo:', exemplo+1,'\n'

                contSaida = 0
                numero_neuronio = 0

                #Setar as entradas nos neurônios
                while numero_neuronio<len(self.rede):
                    neuronio = self.rede[numero_neuronio]
                    if numero_neuronio != 0:
                        neuronio.entrada = entrada[exemplo][numero_neuronio-1]
                    numero_neuronio+=1

                while contSaida<self.quantidade_saida:

                    print ('Saida %d' % (contSaida+1))                    
                    
                    resposta = 0
                    resposta_saida = 0

                    net = self.soma_funcoes(contSaida,True)
                    print 'net: %d' %(net)

                    #Função degrau
                    resposta = self.degrau(net)
                    resposta_saida = saida[exemplo][contSaida]

                    print 'Resposta conseguida: %d | Resposta Esperada: %d |' %(resposta,resposta_saida),                    

                    if resposta == resposta_saida:
                        print 'Ok\n'
                        acertos+=1
                    else:
                        print 'Recalcular os pesos\n'

                        numero_neuronio = 0

                        while numero_neuronio < len(self.rede):
                            neuronio = self.rede[numero_neuronio]
                            neuronio.pesos[contSaida] = neuronio.pesos[contSaida] + self.alfa*(resposta_saida - resposta) * neuronio.entrada
                            numero_neuronio += 1

                    
                    contSaida+=1
                print ''.center(50,'-'),'\n'
                contExemplos+=1
            contCiclos+=1
        print 'FIM DA ETAPA DE TREINAMENTO'.center(50),'\n'
        print ''.center(50,'-'),'\n'
        return acertos

    def execultar(self,entrada,verbose=True):

        contSaida = 0
        numero_neuronio = 0
        respostas = []
        while numero_neuronio<len(self.rede):
            neuronio = self.rede[numero_neuronio]
            if numero_neuronio !=0:
                neuronio.entrada = entrada[numero_neuronio-1]
            numero_neuronio+=1

        while contSaida < self.quantidade_saida:

            if verbose:
                print 'Saida %d' % (contSaida+1)

            resposta = 0
            net = self.soma_funcoes(contSaida,verbose)

            if verbose:
                print 'net: %d' % net
            
            resposta = self.degrau(net)
            #print 'Resposta conseguida: %d' %(reposta)
            respostas.append(resposta)
            contSaida+=1
        return tuple(respostas)



            

    def __str__(self):
        
       temp=''
       for neuronio in self.rede:
           temp+=str(neuronio)+'\n'
       return temp
        
        
       
if __name__ == '__main__':

# ct fidelidade | compra > 50 | Pagamento dinheiro
# 00 - diamante
# 01 - ouro
# 10 - prata
# 11 - bronze

    entrada = [
                [1,0,1,1,0,0,0,1,1],
                [0,1,0,1,1,1,0,1,0],
                [1,1,1,0,0,0,1,0,0],
                [1,1,1,1,1,1,1,0,0],
                [1,0,0,1,1,1,0,0,0],
                [0,0,1,0,0,0,1,1,1],
              ]

    saidas = [
              [0],
              [0],
              [0],
              [1],
              [1],
              [1],
              ]
    
    ordem = [[]]

    pesos  = [[1,
               1,
               -1,
               1,
               1,
               1,
               1,
               1,
               0,
               0]]

    try:
        cont=0
        
        acertos=0
        ciclos = 1

        
        rede = RedeNeural(9,pesos,bias=1,numero_ciclos=8,alfa=1)
        acertos = rede.treinar(entrada,saidas)
        print acertos
        resposta = rede.execultar([0,0,0,0,0,1,0,0,0])
        print resposta
        

        
#        a = rede.execultar([-1,-1,-1])
#        print a

    except RedeException: # Ver isso
        print RedeException.message
        
    #print rede
