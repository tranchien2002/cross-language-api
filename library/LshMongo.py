# -*- coding: utf-8 -*-
from datasketch import MinHashLSHForest, MinHash, MinHashLSH
import library.Mongodb as mongo
from bson.objectid import ObjectId
from library.document2json import pickle_json, lsh_json
import _pickle as cPickle
import os
import string

docs_col = mongo.get_colection("documents")

def get_topn_similarity_documents_lsh(keywords, topn = 3):
    lsh = load_lsh()
    min = MinHash(num_perm=128)
    keywords = keywords.split(",")
    for k in keywords:
        print(k)
        min.update(k.encode("utf-8"))
    result = lsh.query(min, topn)
    list_docs = []
    if result:
        for item in result:
            doc = docs_col.find_one({"_id": ObjectId(str(item))})
            doc.pop('_id', None)
            list_docs.append(doc)
    return list_docs

def store_lsh():
    forest = MinHashLSHForest(num_perm=128)
    documents_en = docs_col.find({"lang": 'english'})
    documents_en = [lsh_json(str(item["_id"]), item["keyword"]) for item in documents_en]
    for item in documents_en:
        minhash = MinHash(num_perm=128)
        list_keyword = item["keyword"].split(",")
        for k in list_keyword:
            minhash.update(k.encode("utf-8"))
        forest.add(str(item["id"]), minhash)
    forest.index()
    ouf = open('pickle_lsh.txt', 'wb')
    cPickle.dump(forest, ouf)
    ouf.close()
    return forest

def load_lsh():
    if(os.path.isfile('pickle_lsh.txt')):
        inf = open('pickle_lsh.txt', 'rb')
        forest = cPickle.load(inf)
    else:
        forest = store_lsh()
    return forest