# DeepCISO aitextgen demo, 2022-01-31

Small, portable repository to test aitextgen with GPT Neo 125M which hopefully lowers DeepCISO's dollars-spent-per-user-lolz.

## Requirements

* aitextgen
* numpy
* sqlite3
* tons of tweets

## Usage

#### 1. build_model.py

Inputs: a Twint-created sqlite database of tweets.
Outputs: `model.txt`

Intakes a sqlite database with Tweets in it, builds a per-user engagement minimum, then filters each user's tweets against it to remove some chatting (ex. tweets must be in the 85th percentile or above). Then processes some unwanted garbage out - like @s at the start of a tweet, and links - in a very hacky and low quality way. Dumps remaining data, all lowercase, to `model.txt`. Needs refactoring. Doesn't need to be amazing right now.

#### 2. train_model.py

Inputs: `model.txt`
Outputs: `trained_model/*` and `aitextgen.tokenizer.json`

Finetunes GPT Neo 125M by ElutherAI with pretty lean settings. Should be viable to run on headless systems with 3GB+ of vRAM, or non-headless (headfull?) systems with 4GB+ vRAM. Also should run on CPU, albeit slowly. Messing with these to learn more about accuracy, hence the disposable repository being used here.

#### 3. run_model.py

Inputs: `trained_model/*` and `aitextgen.tokenizer.json`
Outputs: to console

Runs finetuned model - quickly producing memetastic results. Observations to follow.