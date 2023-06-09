import sys
sys.path.append('..')
import numpy as np
from common.util import preprocess, create_co_matrix, cos_similarity

def most_similar(query, word_to_id, id_to_word, word_matrix, top=5):
    if query not in word_to_id:
        print('%s (을)를 찾을 수 없습니다.'%query)
    
    print('\n[query] ' + query)
    
    query_id = word_to_id[query]
    query_vec = word_matrix[query_id]

    # 코사인 유사도 계산
    vocab_size = len(id_to_word)
    similarity = np.zeros(vocab_size)
    for i in range(vocab_size):
        similarity[i] = cos_similarity(word_matrix[i], query_vec)
    
    count = 0
    for i in (-1 * similarity).argsort():
        if id_to_word[i] == query:
            continue
        print(' %s: %s'%(id_to_word[i], similarity[i]))
        count += 1
        if count >= top:
            return

def ppmi(C, verbose=False, eps=1e-8):
    M = np.zeros_like(C, dtype=np.float32)
    N = np.sum(C)
    S = np.sum(C, axis=0)
    total = C.shape[0] * C.shape[1]
    cnt = 0

    for i in range(C.shape[0]):
        for j in range(C.shape[1]):
            pmi = np.log2(C[i, j] * N / (S[j] *S[i]) + eps)
            M[i, j] = max(0, pmi)

            if verbose:
                cnt += 1
                if cnt % (total//100) == 0:
                    print('%.1f%% 완료' % (100*cnt/total))
    return M

def ch_2_3():
    text = "You say goodbye and I say hello."
    corpus, word_to_id, id_to_word = preprocess(text)
    vocab_size = len(word_to_id)

    co_mat = create_co_matrix(corpus, vocab_size, window_size=1)

    print(corpus)
    print(id_to_word)
        
    most_similar('you', word_to_id, id_to_word, co_mat)

def ch_2_4():
    return


if __name__ == "__main__":
    exec_list = [ch_2_3, ch_2_4]

    exec_list[0]()