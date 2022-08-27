#! /usr/bin/env python3

import os
#import colorama
import re

from rich.console import Console
from rich.theme import Theme
from rich.prompt import Prompt
from rich.table import Table
from rich.padding import Padding

# rich theme definieren < niet meer gebruikt??
custom_theme = Theme({
    "repr.number": "default",
    "my_nr_cyan": "bold not italic cyan",
    })
console = Console(theme=custom_theme)

# colorama initialiseren, anders werkt move_cursor() niet.
#colorama.init()


class BMI_calc():
    def __init__(self, height: float):
        self._height = height # lengt in meters; so for instance 1.89m
        self._weight = 0
        self._bmi = 0
 
    def get_height(self) -> float:
        return self._height
 
    def set_height(self, height: float):
        self._height = height
        self.calc_bmi() # re-calculate bmi based on the new height

    def del_height(self):
        del self._height

    height = property(get_height, set_height, del_height, 'I am the height attribute')

    def get_weight(self) -> float:
        return self._weight
 
    def set_weight(self, weight: float):
        self._weight = weight
        self.calc_bmi() # re-calculate bmi based on the new weight

    def del_weight(self):
        #del self._weight
        self._weight = 0

    weight = property(get_weight, set_weight, del_weight, 'I am the weight attribute')

    def get_bmi(self) -> float:
        return self._bmi

    def set_bmi(self, bmi: float):
        self._bmi = bmi
        self.calc_weight() # re-calculate weight based on the new bmi

    def del_bmi(self):
        #del self._bmi
        self._bmi = 0

    bmi = property(get_bmi, set_bmi, del_bmi, 'I am the bmi attribute')

    def calc_weight(self):
        '''method calc_weight re-calculates and returns the new weight'''
        result = round(self._bmi * self._height**2, 2)
        self._weight = result

    def calc_bmi(self):
        '''method calc_BMI re-calculates and returns the corresponding BMI'''
        result = round(self._weight / self._height**2, 2)
        self._bmi = result


class ProcessInput():
    # geef de input hier en de output is de waarde en of het bmi/height/weight is
    def __init__(self, input: str):
        self._input = input
        self._key = ''
        self._val = 0

    def output(self) -> tuple[str, float]:

        keywords = ['bmi', 'height', 'weight']

        # als een komma voorkomt in de input, vervangen door een punt (NL decimalen -> US decimalen)
        if "," in self._input:
            self._input = self._input.replace(",", ".")

        # wordt er een 'keyword argument' gegeven?
        for k in keywords:
            # kijk of een input wordt gegeven zoals 'bmi = 59'
            if k in self._input:
                m = re.search(r'=(.*)', self._input)
                if m:
                    val_str = (m.group(1)).strip() # eerste groep tussen haakjes + spaties weghalen
                else:
                    val_str = None
                    break
                self._key = k # k gevonden in de input; set de key variable als k (bijv 'bmi')
                self._input = val_str # string -> float >> even niet hier, want anders dubbel doen. Hieronder wel.

        # anders inp variable processen als een nummer
            
        try:
            # als 'inp' iets zinnigs is waar een float van kan worden gemaakt: go ahead.
            self._val = float(self._input)
        except ValueError:
            #als het niks zinnigs is, ga terug naar boven in de while-loop = opnieuw input vragen.
            #return val == None
            return None

        if self._key == '':

            if 0 < self._val <= 2.50:
                # assume input is a (new) height value
                #b.height = inp # new object with new length.
                self._key = 'height'

            elif 2.50 < self._val <= 40:
                # assume input is a BMI value
                #b.bmi = inp
                self._key = 'bmi'

            elif 40 < self._val <= 600:
                # assume input is a weight value
                #b.weight = inp
                self._key = 'weight'

            else:
                # dit komt niet voor, toch? - wel als input == 0 of input > 600
                #continue
                return None

        return (self._key, self._val)


def move_cursor (y:int, x:int):
    print("\033[%d;%dH" % (y, x))


def main():
    b = BMI_calc(1.89) # 1.89 default height. Class BMI_calc sets weight and bmi as zero. For starters.

    quit_strings = ['q', 'quit', 'exit', 'stop', 'ho']
    reset_strings = ['reset']

    while True:

        # user input vragen
        inp = Prompt.ask(f"Please input [bold]weight (kg)[/bold] or [bold]BMI (kg/m2)[/bold]" + 
                         f" or [bold]height (m)[/bold]. (Height = {b.get_height():.2f}m)")

        # als één van de strings in 'quit_strings' wordt getypt, zoals 'quit' dan stoppen we.
        if inp in quit_strings:
            break

        # als één van de strings in 'reset_strings' wordt getypt, zoals 'reset' dan alles weer op default.
        if inp in reset_strings:
            inp = "1.89"
            del b.weight
            del b.bmi
        
        # input 'inp' nu processen: bepalen of het een bmi, height, of weight value betreft.
        pi = ProcessInput(inp)

        # als het onduidelijk is, retourneert pi.output() 'None'
        if pi.output():
            key, val = pi.output()
            # toch even checken of bmi/height/weight (=key) attribute bestaat in instance b. Dan 'setten' met val.
            # kan ook met exec(f"b.{key} = {val}")
            #exec(f"b.{key} = {val}")
            if hasattr(b, key):
                setattr(b, key, val)
        else:
            continue

        # Dit zou toch mooier werken dan die if-elif-elif hierboven: ? -> ja, dus! hasattr / setattr.
        #my_dict = {'bmi': b.bmi, 'height': b.height, 'weight': b.weight, }
        #my_dict[key] = val # b instance van BMI_calc zetten naar 'val'

        table = Table()
        table.add_column("descr")
        table.add_column("value")

        table.add_row(f"Height: ", f"[bold][magenta]{b.height:.2f} m")
        table.add_row(f"Weight: ", f"[bold][magenta]{b.weight:.1f} kg")
        table.add_row(f"BMI: ", f"[bold][magenta]{b.bmi:.1f} kg/m2")

        # Move cursor to top of screen (colorama module required)
#        Niet nodig, aangezien cursor bovenaan komst met 'clear screen' - colorama ook commented-out; zie boven.
#        move_cursor(10, 2)

        # clear screen
        os.system('cls' if os.name == 'nt' else 'clear') # clear screen

        console.print(Padding(table, (1, 14, 1, 14))) # padding: top, right, bottom, left


if __name__ == "__main__":

    main()

