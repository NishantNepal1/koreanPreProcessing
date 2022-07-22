from .utils import Refine
from tqdm import tqdm
from konlpy.tag import Mecab
from os.path import normpath, basename
import sentencepiece as spm
import pandas as pd
import csv

class Tokenizer(Refine):
    def __init__(self, args):
        super().__init__()

        if args.mecab:
            self.cls = self.mecab
            self.args = [normpath(args.input), normpath(args.output), args.encoding]
            if args.morphs + args.nouns + args.pos != 1:
                print("Please select ONE method in [morphs, nouns, pos]")
                raise ValueError
            if args.morphs:
                self.method = Mecab().morphs
            elif args.nouns:
                self.method = Mecab().nouns
            elif args.pos:
                self.method = Mecab().pos
            else:
                print("found no method in [morphs, nouns, pos]")
                raise ValueError
        elif args.bpe:
            self.cls = self.bpe
            self.args = [normpath(args.input), normpath(args.output), \
                        args.model, args.train, args.vocab, args.encoding]
        else:
            print("Tokenizer class indicate error: {} not available"\
                .format())
            raise ValueError

    def apply(self):
        self.cls(*self.args)

    def mecab(self, inp_path, out_path, encoding='utf8'):
        desc_list = []
        with open(inp_path, 'r', encoding="utf-8") as file:
            my_reader = csv.reader(file, delimiter=',')
            for index, row in enumerate(my_reader):
                if index == 0: continue
                desc_list.append([row[1], row[2], row[3]])
                #desc_list.append(row)
                #print(row)
                #print(row[1], row[2],row[2])

        num_lines = sum(1 for line in open(inp_path, "r", encoding=encoding))
        #df = pd.read_csv(inp_path)

        print(desc_list[0])
        """
        lines = super().readline(inp_path, encoding)
        for index, rows in enumerate(lines):
            if index == 0 or index == 1: continue
            print(rows[1], rows[3])
            break
        """

        with open(out_path, "w", encoding=encoding) as out:
            write = csv.writer(out)
            #write.writerow(["English Name",)
            for index, line in enumerate(desc_list):
                #skip first line if column title is ser
                if index ==0 : continue

                if not line:
                    break
                else:
                    #here the data Struct is [Korean Name, English Name, Descp]
                    applied = self.method(line[2])
                    #here the data Struct is ["Review"]
                    #applied = self.method(line[1])
                    #print(line[1])
                    print(applied)
                    if not applied:
                        continue

                    if type(applied[0]) == tuple:# pos
                        list = []
                        for tup in applied[:-1]:
                            list.append((tup[0], tup[1]))
                        list.append((applied[-1][0],applied[-1][1]))
                        print(type(list))
                        write.writerow([line[0],line[1],line[2],list])

                        #write.writerow([line[1],list])
                    else:
                        for token in applied[:-1]: # morphs & nouns
                            out.write(token + ' '+"1-error")
                        out.write(applied[-1] + '\n'+'3-error')
                        
        print("process done, saved at {}".format(out_path))

    def bpe(self, inp_path, out_path, model: str, train: bool, \
                                    vocab: int, encoding='utf8'):
        if train:
            templates = '--input={} --model_prefix={} --vocab_size={}'
            vocab_size = vocab
            prefix = basename(out_path)
            cmd = templates.format(inp_path, prefix, vocab_size)

            spm.SentencePieceTrainer.Train(cmd)

        else:
            assert model and "BPE model path: None"

            sp = spm.SentencePieceProcessor()
            sp.Load(normpath(model))
            num_lines = sum(1 for line in open(inp_path, "r", encoding=encoding))
            lines = super().readline(inp_path, encoding)
            with open(out_path, "w", encoding=encoding) as out:
                for line in tqdm(lines, total=num_lines):
                    if not line:
                        break
                    bpe = sp.EncodeAsPieces(line)
                    for x in bpe[:-1]:
                        out.write(x+' ')
                    try:
                        out.write(bpe[-1]+'\n')
                    except IndexError:
                        out.write('\n')
                            
            print("process done, saved at {}".format(out_path))