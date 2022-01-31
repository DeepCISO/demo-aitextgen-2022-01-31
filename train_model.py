from aitextgen.TokenDataset import TokenDataset
from aitextgen.tokenizers import train_tokenizer
from aitextgen.utils import build_gpt2_config
from aitextgen import aitextgen

# Settings used across tokenization and model configuration
# https://docs.aitextgen.io/tutorials/model-from-scratch/
# Remember: model size = vocab_size * embeddings!
dc_train_from = "EleutherAI/gpt-neo-125M"  # gpt3-like
dc_vocab_size = 50000  # gpt2 default is 50k, this is ~2GB RAM usage with 1 batch
dc_max_length = 500
dc_block_size = dc_max_length  # must always be the same, says docs
dc_dropout = 0.0
dc_n_embd = 256
dc_n_layer = 8
dc_n_head = 8
# These all impact speed, and on a GTX 1650 the above == 3.3h/100k steps

# Where to put the files ...
file_name = "model.txt"  # should be more descriptive in the future
tokenizer_file = "aitextgen.tokenizer.json"

# Settings used for how long the model is trained
dc_batch_size = 1  # default was 16?
dc_num_steps = 1000000
dc_generate_every = 1000
dc_save_every = 5000

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
