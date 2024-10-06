from tqdm import tqdm
from get_top_10 import get_paragraphs_from_sentence, Notop10found
from mylog import logging
from extractVLSP import sbreadfile
from file_handler import write_to_json

datasets = ['VLSP2016', 'VLSP2018', 'VLSP2021']
filenames = ['dev', 'test', 'train']

def create_document(position, _sentence,_data, _imgs, _auxlabels, _dataset, _filename):
    _paragraphs = []
    try:
        _paragraphs = get_paragraphs_from_sentence(_sentence)
    except Notop10found:
        logging.error(f"No top 10 found with sentence: {_sentence}, IMGID: {_imgs[position]} at record number {position+1} , file: {_dataset}/{_filename}")
    except Exception as e:
        print(e)
    _document = {
        "IMGID" : _imgs[position],
        "data" : _data[position],
        "external": _paragraphs,
        "auxlabels" : _auxlabels[position]
    }
    return _document

if __name__ == '__main__':
    for dataset in datasets:
        for filename in filenames:
            current_file = f'./{dataset}/{filename}'
            data, imgs, auxlabels = sbreadfile(f'{current_file}.txt')
            list_documents = []
            list_documents_token = []
            for i in tqdm(range(0, len(data)), desc=f'Processing {current_file}', bar_format='{l_bar}{bar:20}| {n_fmt}/{total_fmt} | {rate_fmt} | Elapsed: {elapsed} | Est: {remaining}'):
                sentence = ' '.join(data[i][0])
                document = create_document(i, sentence,data, imgs, auxlabels, dataset, filename)
                list_documents.append(document)
            path_to_file_json = f'{current_file}.json'
            write_to_json(path_to_file_json, list_documents)
