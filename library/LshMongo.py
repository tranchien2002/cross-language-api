# -*- coding: utf-8 -*-
from datasketch import MinHashLSHForest, MinHash, MinHashLSH
import library.Mongodb as mongo
from bson.objectid import ObjectId
from library.document2json import pickle_json, lsh_json

docs_col = mongo.get_colection("documents")

def get_topn_similarity_documents_lsh(keywords, n = 3):
    lsh = MinHashLSH(threshold=0.15, num_perm=128)
    documents_en = docs_col.find({"lang": 'english'})
    documents_min = [lsh_json(str(item["_id"]), item["keyword"]) for item in documents_en]
    for item in documents_min:
        minhash = MinHash(num_perm=128)
        list_keyword = item["keyword"].split(",")
        for k in list_keyword:
            minhash.update(k.encode("utf-8"))
        lsh.insert(str(item["id"]), minhash)

    min = MinHash(num_perm=128)
    keywords = keywords.split(",")
    for k in keywords:
        print(k)
        min.update(k.encode("utf-8"))
    result = lsh.query(min)
    list_docs = []
    if result:
        for item in result:
            doc = docs_col.find_one({"_id": ObjectId(str(item))})
            doc.pop('_id', None)
            list_docs.append(doc)
    return list_docs
