# What is this?

So there is this really cool place online called PolyMarket where people bet on arbitrary stuff. For this project we tried to see how well standard LLMs would behave to the task of predicting these arbitrary binary challenges based solely on the text of the question being asked.
The project was also an opportunity to flex the prompt engineering muscles. ( even though I was never really very fond of the task myself)


# Getting Running
## Collecting Data
This repo already contains a curated dataset with about 3.5K entries of binary questions from Polymarket inside `market.csv`. If you want you can re-run the `polymarketscraper.py` script and it will fetch again the newest 4.5K markets from the website, but only those 4.5K. If you want to build a larger dataset you will have to keep running the scrapper daily and collating the results, as the server denies access over the 45 requests limit.
When you are satisfied with your `market.csv` you will want to run `data_look.py` which fixes a bit of the format of `market.csv`, then you will want to run `data_convert.py` which prepares the prompt for ingestion in the format of 4 txts.

## Setup Ollama

You will then want to download some version of [ollama](https://ollama.ai/).
Ollama is an easy-to-use framework that enables you to load LLMs for most common chat and generation tasks. It runs primarily as its own separate application, but you can also access it through the [ollama-python](https://github.com/ollama/ollama-python) library (and indeed you will need to for this project!)
You can do so by running

    pip install ollama

## Prompt Selection
Finally, you will want to select what prompt formats you are interested in running. The folder "prompts" already contains some made available as ollama [ModelFiles](https://github.com/ollama/ollama/blob/main/docs/modelfile.md). The reason we chose to create prompts like this is to facilitate project organization since this way we have every prompt template compartimentalized instead of hapdashly in the middle of code.
Here are the current features we investigated in the example experiments:

 1. Two slightly different starting prompts. More importantly, one uses the instruction token "guess" while the other uses the token "predict". The models with the "guess" template are always appended with odd numbers, while the "predict" templates are appended with even numbers.
 2. Models with structure tagging are available in prompt lines 3, 4, 7 and 8. These are used in conjunction with the "tagged" txts that were created by the `data_convert.py` script.
 3. 4 types of modelfile are available each one in their own subdirectory. These are `llama2` and its non-fine-tuned `llama2:text variant`; and `mistral` and its instruction finetuned `mistral:instruct` variant.
 4. Finally, llama2 models have the option to include further prompt constraints in model files ending from 5 to 8.
 
 Once you've chosen which models you want to run, you must run the following command-line to instruct ollama to build the model files:
 

    ollama create <modelname> -f ./prompts/<basemodel>/<desiredmodelfile>

Once done, it is **very important** to edit lines 10 to 15 of `zeroshot.py` to contain only the models you want to test:

    input_files  = {'simplequestions.txt': [ 'llama2form1', 'llama2form2', 'llama2textform1', 'llama2textform2', 'mistralform1', 'mistralform2', 'mistralinstructform1', 'mistralinstructform2', 'llama2form5', 'llama2form6', 'llama2textform5', 'llama2textform6'],
    taggedsimplequestions.txt': ['llama2form3', 'llama2form4', 'llama2textform3', 'llama2textform4', 'mistralform3', 'mistralform4', 'mistralinstructform3', 'mistralinstructform4', 'llama2form7', 'llama2form8', 'llama2textform7', 'llama2textform8'],
    'extendedquestions.txt': [ 'llama2form1', 'llama2form2', 'llama2textform1', 'llama2textform2', 'mistralform1', 'mistralform2', 'mistralinstructform1', 'mistralinstructform2', 'llama2form5', 'llama2form6', 'llama2textform5', 'llama2textform6'],
    'taggedextendedquestions.txt': ['llama2form3', 'llama2form4', 'llama2textform3', 'llama2textform4', 'mistralform3', 'mistralform4', 'mistralinstructform3', 'mistralinstructform4', 'llama2form7', 'llama2form8', 'llama2textform7', 'llama2textform8'],}

 And etc.
 Eventually, maybe I will make a .sh file to simplify this proccess.
## Post-Processing and Evaluation
Once you are done with the generations, move all files created to either the `zero_shot_results` folder or the `few_shot_results` folder depending on the kind of tests you ran, and then run `results_cleaner.py` . This script will resolve any weird generations and augment the responses created for the following evaluation steps.
Finally, when you are ready just run `evaluation.py` and enjoy the show. There are currently 6 graphs being generated and more to come.
