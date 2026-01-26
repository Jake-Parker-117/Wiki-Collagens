from dotenv import load_dotenv
from pprint import pprint
import requests
import os
import re

load_dotenv()

def fastaread(fasta_file, flattened_fasta):
    """Opens and reads in a Fasta formatted file and flattens it
    """
    open(flattened_fasta, "w")
    with open(fasta_file, 'r') as file:
        with open(flattened_fasta, "w") as output:
            for line in file:
                if line.startswith(">"):
                    line = '\n' + line
                    output.write(line)
                else:
                    line = line.strip()
                    output.write(line)
            return flattened_fasta

def get_cols(flat_fasta, col_txt):
    """Opens flattened fasta file, filters for collagen containing proteins and adds them to a .txt file
    """
    #Using regex to find collagen containing sequences
    header = ''
    pattern = re.compile("(G[A-Z][A-Z]){9,}G[A-Z][A-Z]") #sets a collagen pattern with a minimum length of 27 amino acids
    with open(flat_fasta, 'r') as f:
        with open(col_txt, 'w') as output:
            for line in f:
                if line.startswith(">"):
                    header = line.strip()
                
                else:
                    line = line.strip()
                    regex = pattern.search(line) #searches each non-header line for that pattern
                    if regex:
                        output.write(f"{header} {line} \n\n") #Saves the header and sequence if the pattern is found
            return col_txt


def label_cols(col_file, hfile):
    """ Creates an html file with marked Col regions and interuptions within the given .txt file input
    """
    #Using regex to identify collagen regions, marking them and then finding interuptions and marking those
    with open(col_file) as fin:
        with open(hfile, 'w') as fout:
            text = fin.read()
            
            #Marking uninterrupted Col seqs
            text = re.sub(r'(G[A-Z][A-Z]){2,}G[A-Z][A-Z]', r'</span><span class="COL">\g<0></span><span class="NC">', text)
            
            #Marking G0G interruptions
            text = re.sub(r'G(G.)</span><span class="NC">(.)</span><span class="COL">', r'</span><span class="GXG">G</span><span class="COL">\1\2', text)
            
            #Marking G1G interuptions
            text = re.sub(r'(G.)G</span><span class="NC">(([A-Z]){2}</span><span class="COL">)',r'</span><span class="GXG">\1</span><span class="COL">G\2', text)
            
            #Marking G3-15G interruptions
            text = re.sub(r'(G..)</span><span class="NC">(([A-Z]){1,12}</span><span class="COL">)', r'\1</span><span class="GNG">\2', text)
            
            #Marking GGG interruptions
            text = re.sub(r'GGG(G*)', r'<span class="GGG">\g<0></span>', text)
            
            #Header for html file
            head = """<!DOCTYPE html>
            <html>
            <head>
            <style type="text/css">
                p.p1 {margin: 0.0px 0.0px 0.0px 0.0px; word-wrap: break-word; white-space: pre-wrap; font: 11.0px Menlo; color: #000000; background-color: #ffffff}
                span.NC {font: 12.0px Menlo; word-wrap: break-word; white-space: pre-wrap; color: #000000}
                span.COL {font: 12.0px Menlo; word-wrap: break-word; white-space: pre-wrap; color: #000000; background-color: #ffff00}
                span.GXG {font: 12.0px Menlo; word-wrap: break-word; white-space: pre-wrap; color: #000000; background-color: #00ff00}
                span.GNG {font: 12.0px Menlo; word-wrap: break-word; white-space: pre-wrap; color: #000000; background-color: #00ffff}
                span.GGG {font: 12.0px Menlo; word-wrap: break-word; white-space: pre-wrap; color: #ff0000}
            </style>
            </head>
            <body>
            <span class="NC">"""
            
            #footer for html file
            foot = """
                </span>
                </body>
                </html>"""
            
            html = head
            html += text
            html += foot
            
            fout.write(html)

#if __name__ == "__main__": #This is only for running in terminal
    #print('\n*** Find Collagens ***\n')
    #fasta_seqs = input("Please paste your fasta sequences: ")
    
   # with open("fasta_cols.fasta", "w") as fastafile:
        #fastafile.write(fasta_seqs) #This will cause all lines of fasta to be on 1 line, but rest should be okay. Fix later
        #with open("flat.fasta", "w") as flattened_fasta:
            #fastaread(fastafile, flattened_fasta)
            #with open("col.txt", "w") as col_txt_file:
                #get_cols(flattened_fasta, col_txt_file)
                #with open("col_html.html", "w") as htmlfile:
                    #label_cols(col_txt_file, htmlfile)