# imports
import sys
sys.path.append('../..')
from minbpe import Tokenizer
from minbpe import BasicTokenizer



def encode_text(text_data_file):
    with open(text_data_file, "r", encoding="utf-8") as f:
        text_sequence = f.read()


    tokenizer = BasicTokenizer()
    tokenizer.train(text_sequence, vocab_size=1024, verbose=True)
    vocab = tokenizer.vocab
    print(vocab)

    encoded_text = tokenizer.encode("Ekkada unnavu ra")
    print(encoded_text)
    
    decoded_text = tokenizer.decode(encoded_text)
    print(decoded_text)


    max_vocab_id = list(tokenizer.vocab.keys())[-1]
    tokenizer.special_tokens = {"<|startoftext|>": max_vocab_id + 1,
    "<|separator|>": max_vocab_id + 2,
    "<|endoftext|>": max_vocab_id + 3,
    "<|unk|>": max_vocab_id + 4,
    "<|padding|>": max_vocab_id + 5,}



    print(len(tokenizer.encode(text_sequence)))

    tokenizer.save(file_prefix="../../data/tokenizer/custom_tokenizer.model")
    

encode_text("../../data/whatsapp_text.txt")