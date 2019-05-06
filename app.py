from flask import Flask, jsonify, request, abort, make_response
import pdb
import pandas as pd
from flask_cors import CORS
import json
from library.KeywordMongo import trans_keyword, extract_topn_new_vi_doc
from library.LshMongo import get_topn_similarity_documents_lsh
from library.MatrixVector import get_topn_similarity_documents, get_json_docs

app = Flask(__name__)
CORS(app)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
    
@app.route('/cross_languages/plagiarism_matrix', methods=['POST'])
def vector_words():
    content = request.json['document']
    keyword = trans_keyword(extract_topn_new_vi_doc(content))
    list_ids = get_topn_similarity_documents(keyword, int(request.json['top']))
    list_docs = get_json_docs(list_ids)
    # pdb.set_trace()
    pd.Series(list_docs).to_json(orient='values')
    # jsonList = json.dumps(list_docs)
    return jsonify(docs= list_docs), 201

@app.route('/cross_languages/plagiarism_lsh', methods=['POST'])
def lsh_words():
    content = request.json['document']
    keyword = trans_keyword(extract_topn_new_vi_doc(content))
    # list_ids = get_topn_similarity_documents(keyword, 5)
    list_docs = get_topn_similarity_documents_lsh(keyword, int(request.json['top']))
    # jsonList = json.dumps(list_docs)
    pd.Series(list_docs).to_json(orient='values')
    return jsonify(docs= list_docs), 201



if __name__ == '__main__':
    app.run(debug=True)