from hashlib import new
import sys
import bibtexparser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
import string

def compare(s1, s2):
    remove = string.punctuation + string.whitespace
    mapping = {ord(c): None for c in remove}
    return s1.translate(mapping) == s2.translate(mapping)

old_bib = sys.argv[1]
new_bib = sys.argv[2]

with open(old_bib) as old_bib_file:
    old_bib_db = bibtexparser.load(old_bib_file)

with open(new_bib) as new_bib_file:
    new_bib_db = bibtexparser.load(new_bib_file)

unseen_entries = []

for new_entry in new_bib_db.entries:
    is_unseen = True

    for old_entry in old_bib_db.entries:
        if new_entry['title'] == old_entry['title']:
            is_unseen = False 
            break
    
    if is_unseen:
        unseen_entries.append(new_entry)
        # print(new_entry['title'])

print(len(unseen_entries))

db = BibDatabase()
db.entries = unseen_entries

writer = BibTexWriter()
with open('new_entries.bib', 'w') as bibfile:
    bibfile.write(writer.write(db))
