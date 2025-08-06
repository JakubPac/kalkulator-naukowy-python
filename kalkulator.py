# -*- coding: utf-8 -*-
"""
Created on Sun Aug  3 19:56:35 2025

@author: jakub
"""
import tkinter as tk
import math
from py_expression_eval import Parser


class Dzialania:
    
    def __init__(self, *args):
        self.args = args
        
    def add(self):
        return sum(self.args)
    
    def sub(self):
        if not self.args:
            return 0
        wynik = self.args[0]
        for arg in self.args[1:]:
            wynik -= arg
        return wynik
    
    def mul(self):
        wynik = 1
        for arg in self.args:
            wynik *= arg
        return wynik

    def div(self):
        if not self.args:
            return None
        wynik = self.args[0]
        try:
            for arg in self.args[1:]:
                wynik /= arg
        except ZeroDivisionError:
            return 'Nie dzielimy przez 0!'
        return wynik
    
    def sinus(self):
        if len(self.args) != 1:
            return 'Sin przyjmuje 1 wartosc'
        else:
            radiany = math.radians(self.args[0])
            return math.sin(radiany)
    
    def cosinus(self):
        if len(self.args) != 1:
            return 'Cos przyjmuje 1 wartosc'
        else:
            radiany = math.radians(self.args[0])
            return math.cos(radiany)
    
    def tangens(self):
        if len(self.args) != 1:
            return 'Tan przyjmuje 1 wartosc'
        else:
            radiany = math.radians(self.args[0])
            try:
                wynik = math.tan(radiany)
                if abs(wynik) > 1e10:
                    return 'Tan nieokreślony'
                return wynik
            except:
                return 'Błąd w Tangensie!'
    
    def cotangens(self):
        if len(self.args) != 1:
            return 'Ctg przyjmuje 1 wartosc'
        else:
            radiany = math.radians(self.args[0])
            if abs(math.tan(radiany)) < 1e-15:  # wartość bliska zeru
                return 'Ctg nieokreślony (dzielenie przez zero)'
            return 1 / math.tan(radiany)
    
    @staticmethod
    def obliczenie_trygonometrii(wyrazenie, funkcja):
        try:
            if wyrazenie.endswith(')'):
                liczba = float(wyrazenie[4:-1])
            else:
                liczba = float(wyrazenie[4:])
            dz = Dzialania(liczba)
            if funkcja == 'sin':
                return dz.sinus()
            elif funkcja == 'cos':
                return dz.cosinus()
            elif funkcja == 'tan':
                return dz.tangens()
            elif funkcja == 'ctg':
                return dz.cotangens()
        except:
            return 'Błąd: niepoprawny argument!'
        

class Kalkulator(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.title('Kalkulator naukowy.')
        self.wejscie = tk.Entry(self, width = 30, borderwidth = 3, justify = 'right', font = ('Arial', 16))
        self.wejscie.grid(row = 0, column = 0, columnspan = 4, pady = 10)    

        self.przyciski = [('sin(', 1, 0), ('cos(', 1, 1), ('tan(', 1, 2), ('ctg(', 1, 3),
                     ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('/', 2, 3),
                     ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('*', 3, 3),
                     ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('-', 4, 3),
                     ('0', 5, 0), ('.', 5, 1), ('+', 5, 2)]
        
        for (text, row, col) in self.przyciski:
            b = tk.Button(self, text = text, width = 5, height = 2, font = ('Arial', 14),
                        command = lambda t = text: self.dodaj_znak(t))
            b.grid(row = row, column = col, padx = 2, pady =2)
        
        b_c = tk.Button(self, text = 'C', width = 5, height = 2, font = ('Arial', 14), command = self.wyczysc)
        b_c.grid(row = 5, column = 3, padx = 2, pady = 2)
        
        b_row = tk.Button(self, text = '=', width = 14, height = 2, font = ('Arial', 14), command = self.oblicz)
        b_row.grid(row = 6, column = 2, columnspan = 2, padx = 2, pady = 2)
        
        brac_b = tk.Button(self, text = '(', width = 5, height = 2, font = ('Arial', 14), command = lambda t = '(': self.dodaj_znak(t))
        brac_b.grid(row = 6, column = 0, padx = 2, pady = 2)
        
        brac2_b = tk.Button(self, text = ')', width = 5, height = 2, font = ('Arial', 14), command = lambda t = ')': self.dodaj_znak(t))
        brac2_b.grid(row = 6, column = 1, padx = 2, pady = 2)


    def dodaj_znak(self, znak):
        if self.wejscie.get() == 'Błąd' or self.wejscie.get() == '':
            self.wejscie.delete(0, tk.END)
            self.wejscie.insert(0, znak)
        elif znak in ['sin(', 'cos(', 'tan(', 'ctg(']:
            self.wejscie.delete(0, tk.END)
            self.wejscie.insert(0, znak)
        else:
            self.wejscie.insert(tk.END, znak)
    
    def wyczysc(self):
        self.wejscie.delete(0, tk.END)
    
    def oblicz(self):
        try:
            wyrazenie = self.wejscie.get()
            if wyrazenie.startswith('sin('):
                wynik = Dzialania.obliczenie_trygonometrii(wyrazenie, 'sin')
            elif wyrazenie.startswith('cos('):
                wynik = Dzialania.obliczenie_trygonometrii(wyrazenie, 'cos')
            elif wyrazenie.startswith('tan('):
                wynik = Dzialania.obliczenie_trygonometrii(wyrazenie, 'tan')
            elif wyrazenie.startswith('ctg('):
                wynik = Dzialania.obliczenie_trygonometrii(wyrazenie, 'ctg')
            else:
                try:
                    parser = Parser()
                    wynik = parser.evaluate(wyrazenie, {})
                except:
                    wynik = 'Błąd parsera'
            self.wejscie.delete(0, tk.END)
            self.wejscie.insert(0, str(wynik))
        except Exception as e:
            self.wejscie.delete(0, tk.END)
            self.wejscie.insert(0, 'Błąd')
            print("Błąd:", e)
        
        
if __name__ == '__main__':
    app = Kalkulator()
    app.mainloop()