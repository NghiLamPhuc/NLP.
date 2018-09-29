def load_sentences(file_name):
    sentences = []
    with open(file_name, encoding='utf8') as file:
        for line in file:
            line = line.split()
            sentences.append(line)
    return sentences


def check(my_output_file, output_file):
    mine = load_sentences(my_output_file)
    output = load_sentences(output_file)
    if len(mine) != len(output):
        print('Number of sentences not match.')
        return None

    num_correct = 0
    total = 0
    for i in range(len(mine)):
        for j in range(len(mine[i])):
            total += 1
            if mine[i][j] == output[i][j]:
                num_correct += 1

    print('correct = %d\ntotal = %d\naccuracy = %.4f' % (num_correct, total, num_correct/total * 100)+'%')


check('test_da2_lower.txt', 'output.txt')
