print('start of file')
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import DataLoader

from torchtext import data
from torchtext import datasets

print('importing transformers...')
from transformers import BertTokenizer, BertModel

import numpy as np

import time
import random
import functools
print('importing datasets stuff...')
from datasets import load_dataset
from datasets import concatenate_datasets
from datasets import DatasetDict
from datasets import Dataset

from tqdm.notebook import tqdm

import pandas as pd
import itertools
import re
from pprint import pprint

import os

from my_tokenizer import MyTokenizer
from BERT_For_Chords import BERT_For_Chords


def find_ind_word_to_chord_ind(chord_ind, line):
  count = 0
  letter_ind = min(chord_ind, len(line)-1)
  is_space = line[letter_ind].isspace()
  if is_space:
    count +=1
  for i in range(letter_ind,-1,-1):
    if is_space == False and line[i].isspace() == True:
      count +=1
    is_space = line[i].isspace()
  return count



def find_word_in_ind(ind, line):
  last_ind = ind
  for i in range(ind, len(line)):
    if line[i].isspace():
      break
    last_ind = i
  return line[ind:last_ind+1]



def find_word_to_chord_ind(chord_ind, line):
    letter_ind = min(chord_ind, len(line)-1)
    if line[letter_ind].isspace():
      is_found = False
      for i in range(letter_ind,len(line)):
        if not line[i].isspace():
          letter_ind = i
          is_found = True
          break
      if is_found == False:
        for i in range(letter_ind,-1,-1):
          if not line[i].isspace():
            letter_ind = i
            is_found = True
            break
        if is_found == True:
          is_space_found = False
          for i in range(letter_ind,-1,-1):
            if line[i].isspace():
              letter_ind = i
              is_space_found=True
              break
          if is_space_found == True:
            letter_ind = letter_ind+1
          else:
            letter_ind = 0
    else:
      is_space_found = False
      for i in range(letter_ind,-1,-1):
        if line[i].isspace():
          letter_ind = i
          is_space_found=True
          break
      if is_space_found == True:
        letter_ind = letter_ind+1
      else:
        letter_ind = 0
    return find_word_in_ind(letter_ind, line)

if os.path.isfile('dataset/chords_and_lyrics_en.pkl'):
  english_chords = pd.read_pickle('dataset/chords_and_lyrics_en.pkl')
else:
  data = pd.read_pickle('dataset/chords_and_lyrics.pkl')
  english_chords = data[data['lang'] == 'en']
  english_chords.to_pickle('dataset/chords_and_lyrics_en.pkl')
  english_chords.to_csv('dataset/chords_and_lyrics_en.csv')

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True)

init_token = tokenizer.cls_token
pad_token = tokenizer.pad_token
unk_token = tokenizer.unk_token

init_token_idx = tokenizer.convert_tokens_to_ids(init_token)
pad_token_idx = tokenizer.convert_tokens_to_ids(pad_token)
unk_token_idx = tokenizer.convert_tokens_to_ids(unk_token)

max_input_length = tokenizer.max_model_input_sizes['bert-base-uncased']

def cut_and_convert_to_id(tokens, tokenizer, max_input_length):
    tokens = tokens[:max_input_length-1]
    tokens = tokenizer.convert_tokens_to_ids(tokens)
    return tokens

def cut_to_max_length(tokens, max_input_length):
    tokens = tokens[:max_input_length-1]
    return tokens

my_tokenizer_ins = MyTokenizer()


lyrics = english_chords["lyrics"]
chords = english_chords["chords"]
annotated_lyrics = []
annotated_chords = []
annotated_lyrics_input_ids = []
annotated_lyrics_token_type_ids = []
annotated_lyrics_attention_mask = []
annotated_chords_chords_id = []
data = []
for i in range(len(lyrics)):
    row = {}
    if i % 1000 == 0:
        print(i)
    if i not in lyrics or i not in chords:
        continue
    lyric = lyrics[i]
    chord = chords[i]
    text = ""
    for j in range(len(lyric)):
        text += " @ "                 # new line sign
        if 2*j not in lyric:
            continue
        line = lyric[2*j]
        if len(line)==0:
            continue
        line = line.replace('\n', '')
        line = line.replace('\t', '')
        words_in_line = line.split()
        if len(words_in_line) == 0:
            continue
        text += line

    tokenized_text = tokenizer(cut_to_max_length(text, max_input_length), padding='max_length', truncation=True)

    tokenized_chords = list(np.zeros(len(tokenized_text['input_ids']), int))
    annotated_lyrics_input_ids.append(tokenized_text['input_ids'])
    annotated_lyrics_token_type_ids.append(tokenized_text['token_type_ids'])
    annotated_lyrics_attention_mask.append(tokenized_text['attention_mask'])
    row['input_ids'] = tokenized_text['input_ids']
    row['token_type_ids'] = tokenized_text['token_type_ids']
    row['attention_mask'] = tokenized_text['attention_mask']

    words_in_text = text.split()
    start_from_ind = 1
    for j in range(len(lyric)):
        if 2*j not in lyric:
            continue
        line = lyric[2*j]
        if len(line)==0:
            continue
        line = line.replace('\n', '')
        line = line.replace('\t', '')
        words_in_line = line.split()
        tokenized_line = tokenizer(cut_to_max_length(line, max_input_length))
        if len(words_in_line) == 0:
            continue

        if (2*j-1) in chord:
            line_chords = chord[2*j-1]
            line_chords = line_chords.replace('\n', '')
            line_chords = line_chords.replace('\t', '')
            chords_in_line = line_chords.split()

            for chord_in_line in chords_in_line:
                chord_ind = line_chords.find(chord_in_line)
                #word = find_word_to_chord_ind(chord_ind, line)
                #word_ind = words_in_line.index(word)
                word_ind = find_ind_word_to_chord_ind(chord_ind, line)
                ind = start_from_ind + word_ind
                if ind < max_input_length:
                    tokenized_chords[ind] = my_tokenizer.tokenize(chord_in_line)
        start_from_ind += len(tokenized_line['input_ids'])-2 + 1
        #start_from_ind += len(words_in_line) +1
    annotated_lyrics.append(tokenized_text)
    annotated_chords.append(tokenized_chords)
    annotated_chords_chords_id.append(tokenized_chords)
    row['labels'] = tokenized_chords
    data.append(row)



#DATA = load_dataset("csv", "annotated_data")
dataset = Dataset.from_pandas(pd.DataFrame(data=data))
#DATA = Dataset.from_list(annotated_lyrics_input_ids)
dataset = dataset.remove_columns(["token_type_ids"])
dataset.set_format("torch")
dataset = DatasetDict(
    train=dataset.shuffle(seed=1111).select(range(int(0.8*len(dataset)))),
    val=dataset.shuffle(seed=1111).select(range(int(0.8*len(dataset)), len(dataset)))
)


NOTES_NUM = 12
CHORD_TYPES_NUM = 142
OUTPUT_DIM = 1+CHORD_TYPES_NUM*NOTES_NUM**2
DROPOUT = 0.25
dim = 1
hidden_layer_size = 300
activation = nn.ReLU()
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
bert = BertModel.from_pretrained('bert-base-uncased').to(device)


model = BERT_For_Chords(bert, OUTPUT_DIM, DROPOUT, dim, hidden_layer_size, activation)

LEARNING_RATE = 5e-5
N_EPOCHS = 2

optimizer = optim.Adam(model.parameters(), lr = LEARNING_RATE)

TAG_PAD_IDX = 0

criterion = nn.CrossEntropyLoss(ignore_index = TAG_PAD_IDX)

BATCH_SIZE = 16

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)
criterion = criterion.to(device)


train_dataloader = DataLoader(dataset['train'], batch_size=BATCH_SIZE)
eval_dataloader = DataLoader(dataset['val'], batch_size=BATCH_SIZE)
best_val_loss = float("inf")
for epoch in range(N_EPOCHS):
    # training
    model.train()
    for batch_i, batch in enumerate(train_dataloader):
        if batch_i % 1000 == 0:
            print(f'training: epoch {batch_i}')

        text = batch['input_ids']
        tags = batch['labels']

        optimizer.zero_grad()

        #text = [sent len, batch size]

        predictions = model(text.to(device))

        #predictions = [sent len, batch size, output dim]
        #tags = [sent len, batch size]

        predictions = predictions.view(-1, predictions.shape[-1])
        tags = tags.view(-1)

        #predictions = [sent len * batch size, output dim]
        #tags = [sent len * batch size]

        loss = criterion(predictions.to(device), tags.to(device))

        loss.backward()

        optimizer.step()

    # validation
    model.eval()
    loss = 0
    for batch_i, batch in enumerate(eval_dataloader):
        with torch.no_grad():
            output = model(text.to(device))
        loss += criterion(predictions.to(device), tags.to(device))

    avg_val_loss = loss / len(eval_dataloader)
    print("Validation loss:")
    print(avg_val_loss)
    if avg_val_loss < best_val_loss:
        print("Saving checkpoint!")
        best_val_loss = avg_val_loss
        checkpoint = "checkpoints/epoch_" + str(epoch) + ".pt"
        torch.save({
            'epoch': epoch,
            'model_state_dict': model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict(),
            'val_loss': best_val_loss,
            },
            checkpoint
        )

