import os
import pandas as pd
from random import choice

POS = ['Verbs', 'Nouns', 'Other']
LAN = ['English', 'Spanish']

df = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vT6I046wKt5Z3YGh28zQ3k7vYtXXwRw3tZn9ZWgWpM6ydklVk-yDLR0zyw8rMOw3w/pub?gid=1212610006&single=true&output=csv",
                 skiprows=22, header=[0, 1]).iloc[:, 7:13]
df.columns = pd.MultiIndex.from_arrays([['Verbs', 'Verbs', 'Nouns', 'Nouns', 'Other', 'Other'], LAN*3])
for pos in POS:
    df[(pos, 'Prob')] = df[(pos, 'English')].dropna().count()

words = [*['Verbs'] * len(df.Verbs.dropna()),
         *['Nouns'] * len(df.Nouns.dropna()),
         *['Other'] * len(df.Other.dropna())]

while True:
    word = choice(words)
    lang = choice([0, 0, 1])
    c = df[word].dropna().sample(1, weights='Prob')
    
    df[(word, 'Prob')] += 1
    df.at[c.index[0], (word, 'Prob')] = 0
    
    c = c.values.flatten().astype(str)
    print(f"[{word.upper()}] Translate:\t{c[lang]}\n")
    ans = input()
    os.system('cls')
    
    if ans == 'q': break
    print(f"You guessed:\t{ans}\n")
    print(f"Word {c[1].upper()} is a '{word.lower()}' and means {c[0].upper()}\n\n")