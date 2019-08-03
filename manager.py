from string import ascii_lowercase as alphabet
from random import shuffle
from random import randint
from tkinter import *
import json


class Word:
    ''' Class format for a word type '''
    def __init__(self, word):
        self.word = word
        self.length = len(word)

    def set_word(self, new_word):
        self.word = new_word

    def __str__(self):
        return self.word

class Container:
    ''' Container for word list
        min_length -  integer - minimum word length
        banned     -  array   - banned letters
    '''

    def __init__(self):
        self.contents = []
        self.index = 0

    def add_content(self, new_element):
        self.contents.append(new_element)

    def remove_content(self, element):
        self.contents.remove(element)

    def clear_content(self):
        self.contents = []

    def generate_content(self, min_length=5, max_length=12, banned=None):
        ''' Generates a word-list based on minimum word length and banned letters '''
        for letter in alphabet:
            directory = f'words/{letter}.json'
            with open(directory, 'r+') as file:
                contents = json.load(file)  # Obtain words list from json file
                shuffle(contents)  # Shuffle contents 
                for word in contents:
                    if len(word) in range (min_length, max_length+1):
                        if banned:
                            if not any((letter in word) for letter in banned):
                                self.add_content(word)
                                break
                        else:
                            self.add_content(word)
                            break

    def __str__(self):
        return str(self.contents)

    def __len__(self):
        return len(self.contents)

    def __iter__(self):
        return self

    def __next__(self):
        try:
            result = self.contents[self.index]
        except IndexError:
            raise StopIteration
        self.index += 1
        return result

class Window:
    def __init__(self, master):
        self.master = master
        self.draw_elements()

    def generate_words(self):
        self.text_words.delete('1.0', END)  # Clear text widget

        # Get banned letters
        banned_array = list(self.banned_letters.get())

        # Generate
        word_list = Container()
        try:
            minimum = self.min_length.get()
            maximum = self.max_length.get()
        except:
            # Small validation
            self.text_words.insert(END, 'Set min/max lengths!')
        word_list.generate_content(minimum, maximum, banned_array)

        header = f'[No] [*] [{"Word":^{maximum}}] [Length]\n'
        self.text_words.insert(END, header)
        for index, word in enumerate(word_list, 1):
            output = f'[{index:02}] [{word[0].upper()}]  {word:{maximum}}  [  {len(word)}  ]\n'
            self.text_words.insert(END, output)

    def draw_elements(self):
        self.banned_letters = StringVar()
        self.min_length = IntVar()
        self.min_length.set(10)
        self.max_length = IntVar()
        self.max_length.set(15)

        # Title
        panel_title = Frame(self.master, bg='#4C5961', height=100)
        panel_title.pack(side='top', fill='both')
        label_title = Label(panel_title, text='BattleText Assistant',
                            bg='#4C5961', fg='white',
                            font=('Arial Bold', 24, 'bold'))
        label_title.pack()

        # Entry
        panel_entry = Frame(self.master, bg='#768C98', height=100)
        panel_entry.pack(side='top', fill='both')
        
        label_instruction = Label(panel_entry, bg='#768C98',
                                  fg='white', font=('Helvetica', 12, 'bold'),
                                  text='Banned Letters')
        label_instruction.pack(side='left', fill='both')
        
        entry_banned = Entry(panel_entry, textvariable=self.banned_letters,
                             font=('Arial', 12, 'bold'))
        entry_banned.pack(side='left', expand=1, fill='both', padx=3)

        # Length
        panel_size = Frame(self.master, bg='#768C98', height=100)
        panel_size.pack(side='top', fill='both')

        # Min
        label_len = Label(panel_size, bg='#768C98',
                                  fg='white', font=('Helvetica', 12, 'bold'),
                                  text='Minimum Length')
        label_len.pack(side='left', fill='both')
        
        entry_min = Entry(panel_size, textvariable=self.min_length,
                             font=('Arial', 12, 'bold'),width=3)
        entry_min.pack(side='left')
        
        # Max
        panel_size2 = Frame(self.master, bg='#768C98', height=100)
        panel_size2.pack(side='top', fill='both')
        
        label_len2 = Label(panel_size2, bg='#768C98',
                                  fg='white', font=('Helvetica', 12, 'bold'),
                                  text='Maximum Length')
        label_len2.pack(side='left', fill='both')
        
        entry_max = Entry(panel_size2, textvariable=self.max_length,
                             font=('Arial', 12, 'bold'),width=3)
        entry_max.pack(side='left')

        
        # Generation
        panel_wordlist = Frame(self.master, bg='#98ACB5')
        panel_wordlist.pack_propagate(0)
        panel_wordlist.pack(expand=True, fill='both')
        
        self.text_words = Text(panel_wordlist, bg='#E3E6E7',
                               font=('Consolas', 12, 'bold')
                               )
        self.text_words.pack(expand=True, fill='both', padx=40)

        button_generate = Button(panel_wordlist, text='Generate List',bg='gray',
                                 command=self.generate_words,
                                 font=('Arial', 12, 'bold'), relief='groove',
                                 width=20, height=2)
        button_generate.pack()
        
def main():
    # Window Configuration
    root = Tk()
    root.title('BattleText-Assistant')
    root.geometry('500x700')
    root.resizable(width=False, height=False)
    root['bg'] = '#98ACB5'
    Window(root)
    root.mainloop()
    
main()

# Made by Juris-S
# Found on github.com/Juris-S/BattleText-Assistant/
