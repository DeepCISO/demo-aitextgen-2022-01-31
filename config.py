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
model_folder = "trained_model"

# Settings used for how long the model is trained
dc_batch_size = 1  # default was 16?
dc_num_steps = 1000000
dc_generate_every = 500
dc_save_every = 5000
