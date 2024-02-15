##
import numpy as np
import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import BertTokenizer, BertModel, BertPreTrainedModel, AdamW
import torch.nn as nn
from sklearn.model_selection import train_test_split
from tqdm import tqdm


tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')


apt_rent = pd.read_csv(
    '/data/data_step_3/apartment_rent/2023-10-21_apartments_rent_full_history_step3.csv'
)


class RealEstateDataset(Dataset):
    def __init__(self, descriptions, prices, tokenizer, max_len):
        self.descriptions = list(descriptions)
        self.prices = list(prices)
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.descriptions)

    def __getitem__(self, idx):
        description = self.descriptions[idx]
        price = self.prices[idx]

        encoding = self.tokenizer.encode_plus(
            description,
            add_special_tokens=True,
            max_length=self.max_len,
            return_token_type_ids=False,
            padding='max_length',
            truncation=True,
            return_attention_mask=True,
            return_tensors='pt',
        )

        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'price': torch.tensor(price, dtype=torch.float),
        }


text_translated = apt_rent['text_translated']
price = apt_rent['price']
train_descriptions, val_descriptions, train_prices, val_prices = train_test_split(text_translated, price, test_size=0.1)
train_dataset = RealEstateDataset(train_descriptions, train_prices, tokenizer, max_len=128)
val_dataset = RealEstateDataset(val_descriptions, val_prices, tokenizer, max_len=128)
train_dataloader = DataLoader(train_dataset, batch_size=32, shuffle=True)
val_dataloader = DataLoader(val_dataset, batch_size=32)


class BertRegressor(BertPreTrainedModel):
    def __init__(self, config):
        super().__init__(config)
        self.bert = BertModel(config)
        self.regressor = nn.Linear(config.hidden_size, 1)

    def forward(self, input_ids, attention_mask):
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        pooled_output = outputs[1]
        return self.regressor(pooled_output)


model = BertRegressor.from_pretrained('bert-base-uncased')
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
optimizer = AdamW(model.parameters(), lr=3e-5)
loss_fn = nn.MSELoss()
num_epochs = 2


for epoch in range(num_epochs):
    model.train()
    train_losses = []
    for batch in tqdm(train_dataloader, desc=f"Training Epoch {epoch + 1}/{num_epochs}"):
        input_ids = batch["input_ids"].to(device)
        attention_mask = batch["attention_mask"].to(device)
        prices = batch["price"].to(device)

        optimizer.zero_grad()

        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        loss = loss_fn(outputs.squeeze(), prices)

        loss.backward()
        optimizer.step()

        train_losses.append(loss.item())

    model.eval()
    val_losses = []
    for batch in tqdm(val_dataloader, desc=f"Validation Epoch {epoch + 1}/{num_epochs}"):
        input_ids = batch["input_ids"].to(device)
        attention_mask = batch["attention_mask"].to(device)
        prices = batch["price"].to(device)

        with torch.no_grad():
            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
            loss = loss_fn(outputs.squeeze(), prices)
            val_losses.append(loss.item())

    print(
        f"Epoch {epoch + 1}/{num_epochs}, "
        f"Training Loss: {np.mean(train_losses):.4f}, "
        f"Validation Loss: {np.mean(val_losses):.4f}"
    )


def create_finetuned_embedding(text, model, tokenizer):
    inputs = tokenizer(text, return_tensors="pt").to(device)

    with torch.no_grad():
        outputs = model.bert(**inputs)
    embeddings = outputs.last_hidden_state[:, 0, :].cpu().numpy()

    return embeddings


dataset_embeddings = [create_finetuned_embedding(description, model, tokenizer) for description in text_translated]
