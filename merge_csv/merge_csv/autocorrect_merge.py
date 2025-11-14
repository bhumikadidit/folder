import pandas as pd
import re
from collections import Counter

# Function to extract words 
def words(text): 
    return re.findall(r'\w+', text.lower())

# Load correct districts as the dictionary for spell correction
with open('correct_districts.txt', 'r') as f:
    big_text = f.read()
WORDS = Counter(words(big_text))  # Frequency counter; if no corpus, all have count 1
N = sum(WORDS.values())

# Probability function 
def P(word): 
   return WORDS[word] / N

# Generate 1-edit candidates 
def edits1(word):
   letters = 'abcdefghijklmnopqrstuvwxyz'  
   splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
   deletes = [a + b[1:] for a, b in splits if b]
   transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
   replaces = [a + c + b[1:] for a, b in splits if b for c in letters]
   inserts = [a + c + b for a, b in splits for c in letters]
   return set(deletes + transposes + replaces + inserts)

# Find known words from candidates
def known(words): 
   return set(w for w in words if w in WORDS)

# Generate candidates 
def candidates(word):
   return known([word]) or known(edits1(word)) or [word]  

# Correction function 
def correction(word):
   return max(candidates(word), key=P)  

# Process kpi_1.csv in chunks
chunk_size = 1000 
cleaned_chunks = []

for chunk in pd.read_csv('kpi_1.csv', chunksize=chunk_size):
   chunk['District'] = chunk['District'].apply(
       lambda x: correction(str(x).lower()) if pd.notna(x) else x
   )
   cleaned_chunks.append(chunk)

df1_cleaned = pd.concat(cleaned_chunks, ignore_index=True)
df1_cleaned.to_csv('kpi_1_cleaned.csv', index=False)

# Repeat for kpi_2.csv
cleaned_chunks = []
for chunk in pd.read_csv('kpi_2.csv', chunksize=chunk_size):
   chunk['District'] = chunk['District'].apply(
       lambda x: correction(str(x).lower()) if pd.notna(x) else x
   )
   cleaned_chunks.append(chunk)

df2_cleaned = pd.concat(cleaned_chunks, ignore_index=True)
df2_cleaned.to_csv('kpi_2_cleaned.csv', index=False)

# Merge cleaned files
merged = pd.merge(df1_cleaned, df2_cleaned, on='District', how='outer')
merged.to_csv('merged_kpi.csv', index=False)
   