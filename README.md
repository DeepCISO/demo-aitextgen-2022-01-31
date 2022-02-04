# DeepCISO aitextgen demo, 2022-01-31

Small, portable repository to test aitextgen with GPT Neo 125M which hopefully lowers DeepCISO's dollars-spent-per-user-lolz.

## Requirements

* aitextgen
* numpy
* sqlite3
* tons of tweets

...or skip build_model.py and swap model.txt in with whatever text you like.

## Usage

#### 1. build_model.py (optional)

* Inputs: a Twint-created sqlite database of tweets.
* Outputs: `model.txt`

Intakes a sqlite database with Tweets in it, builds a per-user engagement minimum, then filters each user's tweets against it to remove some chatting (ex. tweets must be in the 85th percentile or above). Then processes some unwanted garbage out - like @s at the start of a tweet, and links - in a very hacky and low quality way. Dumps remaining data, all lowercase, to `model.txt`. Doesn't need to be amazing right now. In the future, will try to have a more intelligent mechanism for selecting and filtering content based on the actual content, not engagement.

#### 2. train_model.py

* Inputs: `model.txt`
* Outputs: `trained_model/*` and `aitextgen.tokenizer.json`

Finetunes GPT Neo 125M by ElutherAI with pretty lean settings. Should be viable to run on headless systems with 3GB+ of vRAM, or non-headless (headfull?) systems with 4GB+ vRAM. Also should run on CPU, albeit slowly. Messing with these to learn more about accuracy, hence the disposable repository being used here.

In the private dataset used (kinda meh, all lowercased, 27MB, only tweets, as above ...) here is the loss at arbitrary points during training for my future self and any observers:

* Start: usually in the 7-8 range
* Step 2,500: ~6.3
* Step 5,000: ~6
* Step 45,000: ~5
* Step 100,000: ~4.8
* Step 500,000: ~4.6
* Step 1,000,000: ~4.56

While the improvement from 300k to 500k in loss was quite minimal, whether it's the fallacy of man or something else, I do feel like the results tended to be significantly better as it kept nudging down a hundredth or two.

#### 3. run_model.py

* Inputs: `trained_model/*` and `aitextgen.tokenizer.json`
* Outputs: to console

Runs finetuned model - quickly producing memetastic results. Can also be prompted if you uncomment that line because I am lazy.

## Results

Biggest improvement right now is almost certainly the data itself (needs more & longer data than just tweets), grouping similar topics, understanding how context windows really work, and tuning the learning rate. I don't see a reason to move to a bigger model at this time unless that is actually a big barrier to cogence beyond a sentence (which often makes a world of difference in how funny the results are), so... I'll find that out as well.
