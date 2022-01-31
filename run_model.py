from aitextgen import aitextgen

# With your trained model, you can reload the model at any time by
# providing the folder containing the pytorch_model.bin model weights + the config, and providing the tokenizer.
ai = aitextgen(model_folder="trained_model", tokenizer_file="aitextgen.tokenizer.json")

# ai.generate(10, prompt="log4j is")
ai.generate(10)
