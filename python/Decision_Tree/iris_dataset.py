#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sklearn import datasets
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import LeaveOneOut
from sklearn.metrics import accuracy_score


def main():
    # アイリスデータセットを読み込む
    dataset = datasets.load_iris()

    # 教師データとラベルデータを取り出す
    features = dataset.data
    targets = dataset.target

    # 判定したラベルデータを入れるリスト
    predicted_labels = []
    # LOO 法で汎化性能を調べる
    loo = LeaveOneOut()
    for train, test in loo.split(features):
        # 学習に使うデータ
        train_data = features[train]
        target_data = targets[train]

        # モデルを学習させる
        clf = DecisionTreeClassifier()
        clf.fit(train_data, target_data)

        # テストに使うデータを正しく判定できるか
        predicted_label = clf.predict(features[test])
        predicted_labels.append(predicted_label)

    # テストデータでの正解率 (汎化性能) を出力する
    score = accuracy_score(targets, predicted_labels)
    print(score)


if __name__ == '__main__':
    main()
