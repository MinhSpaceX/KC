from elasticsearch import Elasticsearch
from mylog import logging

minimum_sentence_length = 3

class Notop10found(Exception):
    pass

def get_top_10_sentence(query):
    # Initialize the Elasticsearch client
    es = Elasticsearch(['http://118.70.52.237:5556'])
    #es = Elasticsearch(['http://localhost:5556'])

    # Define the string to search
    search_string = query

    # Step 1: Search in index1 for the string using BM25
    search_response_index1 = es.search(
        index='sentence',
        body={
            "query": {
                "match": {
                    "value": search_string  # Use 'match' for BM25 scoring,
                }
            },
            "size": 10
        }
    )
    page = {}
    for hit in search_response_index1['hits']['hits']:
        score = hit['_score']
        source = hit['_source']
        page_id = int(source["page_id"])
        paragraph_id = int(source["paragraph_id"])
        value = source['value']
        sentence_length = len(value.split())
        if sentence_length < minimum_sentence_length:
            msg = f'Sentence length below minimum({sentence_length} < {minimum_sentence_length}) - query: {query} - result leads to: {page_id}_{paragraph_id}'
            logging.log(logging.INFO, msg)
            continue

        if page_id in page and paragraph_id not in page[page_id]:
            page[page_id].append(paragraph_id)
        else:
            page[page_id] = [paragraph_id]
    return page

def get_document_by_id(id, index):
    document = None
    es = Elasticsearch(['http://118.70.52.237:5556'])
    try:
        # Fetch the document
        response = es.get(index=index, id=id)
        # Access the document data
        document = response['_source']
    except Exception as e:
        print(f"Error retrieving document: {e}")
    return document

def get_paragraph(page={}):
    paragraph_list = []
    for page_id, paragraph_ids in page.items():
        for paragraph_id in paragraph_ids:
            document_id = f'{page_id}_{paragraph_id}'
            document = get_document_by_id(document_id, 'paragraph')
            if (document is None):
                print(f"Error fetching at page_id: {page_id} and para_id: {paragraph_id}")
                continue
            paragraph_list.append(document['value'])
    return paragraph_list

def get_paragraphs_from_sentence(sentence):
    detoken = sentence.replace('_', ' ')
    page = get_top_10_sentence(detoken)
    if (len(page) == 0):
        raise Notop10found
    return get_paragraph(page)
