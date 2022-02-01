from aitextgen import aitextgen
from config import *


# With your trained model, you can reload the model at any time by
# providing the folder containing the pytorch_model.bin model weights + the config, and providing the tokenizer.
ai = aitextgen(model_folder=model_folder, tokenizer_file=tokenizer_file)

# ai.generate(10, prompt="log4j is")
ai.generate(10)
