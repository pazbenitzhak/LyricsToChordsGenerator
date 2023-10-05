import torch.nn as nn

class BERT_For_Chords(nn.Module):
    def __init__(self, bert, output_dim, dropout=0, dim=1, hidden_layer_size=300, activation=nn.ReLU()):

        super().__init__()

        self.bert = bert

        embedding_dim = bert.config.to_dict()['hidden_size']

        self.fc1 =  nn.Sequential(nn.Linear(embedding_dim, hidden_layer_size), activation)

        self.hidden_layers = nn.Sequential(*[nn.Linear(hidden_layer_size, hidden_layer_size), activation]*dim)

        self.fc2 = nn.Linear(hidden_layer_size, output_dim)

        self.dropout = nn.Dropout(dropout)

    def forward(self, text):

        #text = [sent len, batch size]

        text = text.permute(1, 0)

        #text = [batch size, sent len]

        embedded = self.dropout(self.bert(text)[0])

        #embedded = [batch size, seq len, emb dim]

        embedded = embedded.permute(1, 0, 2)

        #embedded = [sent len, batch size, emb dim]

        predictions = self.fc1(self.dropout(embedded))

        predictions = self.hidden_layers(self.dropout(predictions))

        predictions = self.fc2(self.dropout(predictions))

        #predictions = [sent len, batch size, output dim]

        return predictions