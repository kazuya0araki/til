# -*- coding:utf-8 -*-
import pandas as pd
import csv
import config
from janome.tokenizer import Tokenizer


def main():
    # reader = pd.read_csv(config.TWITTER_CSV)
    # print(reader)
    with open(config.TWITTER_CSV, encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            t = Tokenizer()
            tokens = t.tokenize(row[2])
            for token in tokens:
                print(token.surface)


if __name__ == '__main__':
    main()