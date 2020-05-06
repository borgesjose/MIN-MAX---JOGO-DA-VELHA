#######################################################  
# Universidade Federal do Piauí                       #
# Campus ministro petronio Portela                    #                                       
# Copyright 2018 -José Borges do Carmo Neto-           #
# @author José Brges do Carmo Neto                    #
# @email jose.borges90@hotmil.com                     #
#  -- Minimax Aplicado ao jogo da Velha               #
#  -- Version: 1.5  - 17/09/2018                      #
#######################################################    

###########################################################################################################
#                                          Definições
import turtle 

Casa_X = 'X' # É o MAX
Casa_O = 'O' # É o MIN
Casa_vazia = ' '

X_Vence = 'X Venceu!'
O_Vence = 'O Venceu!'
Empate = 'Empate'

#Lista com o estado atual do tabuleiro
estado_atual =    [[' ', ' ', ' '],[' ', ' ', ' '],[' ', ' ', ' ']]

#############################################################################################
#                                 Minimax
#As funções dentro deste bloco são otimizadas para funcionar em recursão
#...O famigerado codigo do minimax...
#
#

from math import inf as infinito
from random import choice

Humano = -1
Computador = +1
tabuleiro_minimax = [[0, 0, 0],[0, 0, 0],[0, 0, 0]]


def tabuleiro_to_estado(tabuleiro):
    estado = [[None,None,None],[None,None,None],[None,None,None]]    
    for i in range(3):
        for j in range(3):
            if tabuleiro[i][j] == 0:
                estado[i][j] = ' '
            if tabuleiro[i][j] == -1:
                estado[i][j] = 'X'
            if tabuleiro[i][j] == 1:
                estado[i][j] = 'O'
    return estado

def estado_to_tabuleiro(estado):
    tabuleiro = [[None,None,None],[None,None,None],[None,None,None]]    
    for i in range(3):
        for j in range(3):
            if estado[i][j] == ' ':
                tabuleiro[i][j] = 0
            if estado[i][j] == 'X':
                tabuleiro[i][j] = -1
            if estado[i][j] == 'O':
                tabuleiro[i][j] = 1

    return tabuleiro


def avaliar_tabuleiro(tab):
  
    if verificar_vencedor(tab, Computador):
        score = +1
    elif verificar_vencedor(tab, Humano):
        score = -1
    else:
        score = 0

    return score


# esta função pode parecer muito com a avaliar_estado, mas ela tem um papel importante na avaliação 
# das jogadas dentro da execução recursiva do algoritmo minimax, sendo mais direta e custando menos 
# a maquina alem de atuar sobre o tabuleiro, e não sobre o estado.
def verificar_vencedor(tabuleiro, jogador):

    tabuleiro_vencedor = [
        [tabuleiro[0][0], tabuleiro[0][1], tabuleiro[0][2]],[tabuleiro[1][0], tabuleiro[1][1], tabuleiro[1][2]],
        [tabuleiro[2][0], tabuleiro[2][1], tabuleiro[2][2]],[tabuleiro[0][0], tabuleiro[1][0], tabuleiro[2][0]],
        [tabuleiro[0][1], tabuleiro[1][1], tabuleiro[2][1]],[tabuleiro[0][2], tabuleiro[1][2], tabuleiro[2][2]],
        [tabuleiro[0][0], tabuleiro[1][1], tabuleiro[2][2]],[tabuleiro[2][0], tabuleiro[1][1], tabuleiro[0][2]]]
    if [jogador, jogador, jogador] in tabuleiro_vencedor:
        return True
    else:
        return False

def casas_vazias(estado):
    coordenadas = []
    for i in range(3):
        for j in range(3):
            if estado[i][j] == 0:
                coordenadas.append([i,j])
    return coordenadas

#Retorna um booleano indicando se a vitoria ou não:
def game_over(estado):
    return verificar_vencedor(estado, Humano) or verificar_vencedor(estado, Computador)

def minimax(estado, depth, jogador):
    
    if jogador == Computador:
        best = [-1, -1, -infinito]
    else:
        best = [-1, -1, +infinito]

    if depth == 0 or game_over(estado):
        score = avaliar_tabuleiro(estado)
        return [-1, -1, score]

    for elemento in casas_vazias(estado):
        x, y = elemento[0], elemento[1]
        estado[x][y] = jogador
        score = minimax(estado, depth - 1, -jogador)
        estado[x][y] = 0
        score[0], score[1] = x, y

        if jogador == Computador:
            if score[2] > best[2]:
                best = score  # max value
        else:
            if score[2] < best[2]:
                best = score  # min value

    return best
#############################################################################################
#                        Funções de suporte

def tabuleiro_cheio (estado):
		for row in estado:
			if Casa_vazia in row:
				return False
		return True

def de_quem_e_a_vez(estado):
	cont =0
	for row in estado:
		cont += row.count(Casa_X)
		cont -= row.count(Casa_O)
	return cont

def inserir_jogada(estado,x,y):
	global estado_atual
	if de_quem_e_a_vez(estado) and estado[x][y]==' ':
		estado_atual[x][y] =  Casa_O 	
	elif estado[x][y]==' ':
		estado_atual[x][y] = Casa_X

def avaliacao_do_estado(estado):
	provavel_vencedor = []
	
	for row in estado:
		provavel_vencedor.append(set(row))

	for i in range(3):
		provavel_vencedor.append(set([estado[k][i] for k in range(3)]))

	provavel_vencedor.append(set([estado[i][i] for i in range(3)]))
	provavel_vencedor.append(set([estado[i][2-i] for i in range(3)]))

	for trio in provavel_vencedor:
		if trio == set([Casa_X]):
			return X_Vence
		elif trio == set([Casa_O]):
			return O_Vence

	return Empate
 
def existe_vencedor(estado):
	if avaliacao_do_estado(estado) != Empate: 
		return True
	else:
		return False

#print(avaliacao_do_estado(estado_atual))
##########################################################################################
#                               Funções gráficas

largura_tela = 700
altura_tela = 700

cor_fundo = "gray"

def xis(x,y):
	turtle.pencolor("red")
	turtle.up()
	turtle.speed(20)
	turtle.goto(x+20, y-20)
	turtle.setheading(-45)
	turtle.down()
	turtle.forward(226)
	turtle.up()
	turtle.goto(x+180, y-20)
	turtle.setheading(-135)
	turtle.down()
	turtle.forward(226)
	turtle.up()

def bola(x,y):
	turtle.pencolor("black")
	turtle.up()
	turtle.goto(x+100,y-180)
	turtle.setheading(0)
	turtle.down()
	turtle.circle(80)
	turtle.up()

def texto(text):

	turtle.pencolor("black")
	turtle.goto(-315,320)
	turtle.write(text, True, align="left",font=("Comic Sans MS", 20, "normal"))
	turtle.up()

def apagar_texto(text):
	turtle.pencolor(cor_fundo)
	turtle.goto(-315,320)
	turtle.write(text, True, align="left",font=("Comic Sans MS", 20, "normal"))
	turtle.up()


def imprimir_jogada(i,j):
	global estado_atual
	x = 200*j - 300
	y = -200*i + 300
	if estado_atual[i][j]=='X':
		xis(x,y)
		apagar_texto('Is X turn') 
		texto('Is O turn')	
	elif estado_atual[i][j]=='O':
		bola(x,y)
		apagar_texto('Is O turn')
		texto('Is X turn')
	

def tabuleiro():
	turtle.bgcolor(cor_fundo)
	turtle.pencolor("white")
	turtle.title("The Old Woman Game")
	turtle.setup(largura_tela,altura_tela)
	turtle.up()
	turtle.pensize(10)
	turtle.hideturtle()
	turtle.speed(80)

	turtle.goto(-300,100)
	turtle.down()
	turtle.forward(600)
	turtle.up()
	turtle.goto(-300,-100)
	turtle.down()
	turtle.forward(600)

	turtle.up()
	turtle.goto(-100,300)
	turtle.setheading(-90)
	turtle.down()
	turtle.forward(600)
	turtle.up()
	turtle.goto(100,300)
	turtle.down()
	turtle.forward(600)
	turtle.up()

######################################################################################################
#                                    jogadas

def jogada_humana(x,y):
	global estado_atual
	x=x+300
	y=-y+300
	if (x<=0 or x>=600 or y<=0 or y>=600):
			pass
	else:
		i =int( y//200)
		j= int (x//200)
		inserir_jogada(estado_atual,i,j)
		imprimir_jogada(i,j)
		print(avaliacao_do_estado(estado_atual))


def jogada_da_ia(estado):
	
	tabuleiro = estado_to_tabuleiro(estado)
	
	depth = len(casas_vazias(tabuleiro))
	
	if depth == 0 or game_over(estado):
		print(avaliacao_do_estado(estado))
		return 
	if depth == 9:
		i = choice([0, 1, 2])
		j = choice([0, 1, 2])
	else:
   		tabuleiro = estado_to_tabuleiro(estado)
   		t = minimax(tabuleiro,depth,Computador)
   		i = t[0]
   		j = t[1]
   		inserir_jogada(estado,i,j)
   		imprimir_jogada(i,j)
   		print(avaliacao_do_estado(estado_atual))		


def main():
	global estado_atual
	

	tabuleiro()
	while not tabuleiro_cheio(estado_atual) and not existe_vencedor(estado_atual):
		
		if de_quem_e_a_vez(estado_atual):
			jogada_da_ia(estado_atual)
			
		else:
			turtle.onscreenclick(jogada_humana)
			texto(" ")




if __name__ == '__main__':
    main()
