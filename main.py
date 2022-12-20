from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from itertools import permutations
from time import sleep


class MainApp(MDApp):

    def build(self):
        self.title = 'Jogo da velha'
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        self.theme_cls.theme_text_color: "Custom"
        self.text_color: "white"
        return Builder.load_file('main.kv')

    Window.size = (350, 700)
    turn = 'X'
    jogadas = 0
    winner = False
    inicio = 1
    placar1 = 0
    placar2 = 0
    marcacao = []
    jogador = 1
    computador = False
    lista_jogo = [0, 0, 0, 0, 0, 0, 0, 0, 0]

    @staticmethod
    def listas():
        perm = permutations([1, 1, 1, 1, 1, -1, -1, -1, -1])
        lista = []
        for i in perm:
            a = list(i)
            lista.append(a)
        return lista

    lista2 = listas()
    lista_pc = listas()

    @staticmethod
    def prob(lista):
        num_x = 0
        num_o = 0
        num_e = 0
        prob_x = prob_o = prob_emp = 0
        for linha in lista:
            x_ganhar = []
            x_ganhar.extend([sum(linha[0:3]),
                             sum(linha[3:6]),
                             sum(linha[6:9]),
                             sum(linha[0:7:3]),
                             sum(linha[1:8:3]),
                             sum(linha[2:9:3]),
                             sum(linha[0:9:4]),
                             sum(linha[2:7:2])])
            if 3 not in x_ganhar and -3 not in x_ganhar:
                num_e += 1
            else:
                if 3 in x_ganhar:
                    num_x += 1
                if -3 in x_ganhar:
                    num_o += 1
            total = num_x + num_o + num_e
            prob_x = num_x / total
            prob_o = num_o / total
            prob_emp = num_e / total
        return prob_x, prob_o, prob_emp

    def posicao(self, pos, valor):
        lista3 = []
        for i in self.lista2:
            i[pos - 1] = valor
            if sum(i) == 1 and i not in lista3:
                lista3.append(i)
        self.lista2 = lista3.copy()
        probabilidade_x, probabilidade_y, probabilidade_emp = self.prob(self.lista2)
        return probabilidade_x, probabilidade_y, probabilidade_emp

    @staticmethod
    def prox_pos(lista, valor):
        valor = valor
        x_ganhar = []
        x_ganhar.extend([sum(lista[0:3]),
                         sum(lista[3:6]),
                         sum(lista[6:9]),
                         sum(lista[0:7:3]),
                         sum(lista[1:8:3]),
                         sum(lista[2:9:3]),
                         sum(lista[0:9:4]),
                         sum(lista[2:7:2])])
        if 3*valor in x_ganhar:
            return True
        else:
            return False

    def posicao_pc(self, valor):
        valor = -valor
        lista = []
        probg = 0
        posg = 0
        probnp = 0
        posnp = 0
        proxima = -1
        for posicao in range(0, 9):
            listab = self.lista_jogo.copy()
            listab[posicao] = -valor
            listab2 = self.lista_jogo.copy()
            listab2[posicao] = valor
            if posicao not in self.marcacao:
                for i in self.lista2:
                    a = i.copy()
                    a[posicao] = valor
                    if sum(a) == 1 and i not in lista:
                        lista.append(a)
                if valor == -1:
                    probx, proby, emp = self.prob(lista)
                else:
                    proby, probx, emp = self.prob(lista)
                nperder = 1-probx
                # print('posição',posicao,'-',proby,nperder,probx)
                b = self.prox_pos(listab, -valor)
                b2 = self.prox_pos(listab2,valor)
                if b2 is True:
                    proxima = posicao
                elif proxima <0 and b is True:
                    proxima = posicao
                else:
                    if proby >= probg:
                        posg = posicao
                        probg = proby
                        if nperder >= probnp:
                            posnp = posicao
                            probnp = nperder
            del lista[:]
        if proxima >= 0:
            pos = proxima
        elif probg > 0:
            pos = posg
        else:
            pos = posnp
        return pos

    def pc(self):
        if self.computador is False:
            self.computador = True
        else:
            self.computador = False

    def jogada(self, valor):
        valor = valor
        if self.jogador == 1:
            self.jogador = 2
        else:
            self.jogador = 1
        if self.computador is True and self.jogador == 2:
            b = self.posicao_pc(valor)
            c = f'self.root.ids.btn{b+1}'
            c = eval(c)
            self.press(c, b+1)

    def press(self, btn, pos):
        a = pos
        if self.turn == 'X':
            valor = 1
            self.lista_jogo[pos-1] = valor
            btn.text = 'X'
            self.turn = 'O'
        else:
            valor = -1
            self.lista_jogo[pos-1] = valor
            btn.text = 'O'
            self.turn = 'X'
        if self.jogador == 1:
           vez = 'jogador 2'
        else:
            vez = 'jogador 1'
        probx, probo, empate = self.posicao(a, valor)
        self.root.ids.score.text = f' Vez do {vez}'
        btn.disabled = True
        self.jogadas += 1
        self.win()
        self.root.ids.ganhar.text = f'{probx:.0%}'
        self.root.ids.perder.text = f'{probo:.0%}'
        self.root.ids.empatar.text = f'{empate:.0%}'
        self.marcacao.append(pos-1)
        if self.jogadas < 9:
            self.jogada(valor)

    def disable_all_buttons(self):
        for i in range(1, 10):
            b = f'self.root.ids.btn{i}'
            c = eval(b)
            c.disabled = True

    def end_game(self, a):
        a[0].color = 'red'
        a[1].color = 'red'
        a[2].color = 'red'
        if self.jogador == 1:
            vencedor = 'jogador 1'
        else:
            vencedor = 'jogador 2'
        self.winner = True
        self.root.ids.score.text = f' O vendecedor foi o {vencedor}'
        self.disable_all_buttons()

    def empate(self):
        self.root.ids.score.text = f' O jogo terminou empatado'

    def win(self):
        lista1 = []
        num = []
        for i in range(1, 10):
            variavel = f'self.root.ids.btn{i}'
            func = eval(variavel)
            if func.text == 'X':
                valor = 1
            elif func.text == 'O':
                valor = -1
            else:
                valor = 0
            lista1.append(valor)
            num.append(func)
        l1 = lista1[0:3]
        l2 = lista1[3:6]
        l3 = lista1[6:9]
        c1 = lista1[0:7:3]
        c2 = lista1[1:8:3]
        c3 = lista1[2:9:3]
        d1 = lista1[0:9:4]
        d2 = lista1[2:7:2]
        lista2 = [l1, l2, l3, c1, c2, c3, d1, d2]
        num2 = [num[0:3], num[3:6], num[6:9], num[0:7:3], num[1:8:3], num[2:9:3], num[0:9:4], num[2:7:2]]
        a = False
        for index, item in enumerate(lista2):
            soma = sum(item)
            if soma == 3:
                self.end_game(num2[index])
                a = True
                if self.jogador == 1:
                    self.placar1 += 1
                else:
                    self.placar2 += 1
            elif soma == -3:
                self.end_game(num2[index])
                a = True
                if self.jogador == 1:
                    self.placar1 += 1
                else:
                    self.placar2 += 1

        if self.jogadas == 9 and a is False:
            self.empate()

    def restart(self):
        self.marcacao = []
        self.turn = 'X'
        self.lista_pc = self.listas()
        self.root.ids.jog1.text = str(self.placar1)
        self.root.ids.jog2.text = str(self.placar2)
        self.lista2 = self.listas()
        self.root.ids.ganhar.text = '---'
        self.root.ids.perder.text = '---'
        self.root.ids.empatar.text = '---'
        self.jogadas = 0
        self.lista_jogo = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(1, 10):
            b = f'self.root.ids.btn{i}'
            c = eval(b)
            c.text = ''
            c.disabled = False
            c.color = 'green'
        if self.inicio == 1:
            self.root.ids.score.text = 'Jogador 2 começa'
            self.inicio = 2
            self.jogada(1)
        else:
            self.root.ids.score.text = 'Jogador 1 começa'
            self.inicio = 1


MainApp().run()
