from aitextgen.TokenDataset import TokenDataset
from aitextgen.tokenizers import train_tokenizer
from aitextgen.utils import build_gpt2_config
from aitextgen import aitextgen
from config import *

# Train a custom BPE Tokenizer on the downloaded text
# This will save one file: `aitextgen.tokenizer.json`, which contains the
# information needed to rebuild the tokenizer.
train_tokenizer(file_name, vocab_size=dc_vocab_size)

# Set up custom configuration for GPT2
config = build_gpt2_config(
    vocab_size=dc_vocab_size,
    max_length=dc_max_length,
    dropout=dc_dropout,
    n_embd=dc_n_embd,
    n_layer=dc_n_layer,
    n_head=dc_n_head,
)

# Instantiate aitextgen using the created tokenizer and config
ai = aitextgen(model=dc_train_from, tokenizer_file=tokenizer_file, config=config)

# You can build datasets for training by creating TokenDatasets,
# which automatically processes the dataset with the appropriate size.
data = TokenDataset(file_name, tokenizer_file=tokenizer_file, block_size=dc_block_size)

# Train the model! It will save pytorch_model.bin periodically and after completion to the `trained_model` folder.
ai.train(
    data,
    batch_size=dc_batch_size,
    num_steps=dc_num_steps,
    generate_every=dc_generate_every,
    save_every=dc_save_every,
)
