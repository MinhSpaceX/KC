def sbreadfile(filename):
    '''
    read file
    return format :
    [ ['EU', 'B-ORG'], ['rejects', 'O'], ['German', 'B-MISC'], ['call', 'O'], ['to', 'O'], ['boycott', 'O'], ['British', 'B-MISC'], ['lamb', 'O'], ['.', 'O'] ]
    '''
    print("prepare data for ",filename)
    f = open(filename,encoding='utf8')
    data = []
    imgs = []
    auxlabels = []
    sentence = []
    label = []
    auxlabel = []
    imgid = ''
    a = 0
    for line in f:
        if line.startswith('IMGID:'):
            imgid = line.strip().split('IMGID:')[1]
            continue

        if line[0] == "\n":
            if len(sentence) > 0:
                data.append((sentence, label))
                imgs.append(imgid)
                auxlabels.append(auxlabel)
                sentence = []
                label = []
                imgid = ''
                auxlabel = []
            continue
        splits = line.split('\t')
        
        # if splits[0] == '' or splits[0].isspace() or splits[0] in SPECIAL_TOKENS or splits[0].startswith(URL_PREFIX):
        #     splits[0] = "<unk>"
        
        sentence.append(splits[0])
        cur_label = splits[-1][:-1]
        if cur_label == 'B-OTHER':
            cur_label = 'B-MISC'
        elif cur_label == 'I-OTHER':
            cur_label = 'I-MISC'
        label.append(cur_label)
        auxlabel.append(cur_label[0])

    if len(sentence) > 0:
        data.append((sentence, label))
        imgs.append(imgid)
        auxlabels.append(auxlabel)
        sentence = []
        label = []
        auxlabel = []

    print("The number of samples: " + str(len(data)))
    print("The number of images: " + str(len(imgs)))
    return data, imgs, auxlabels