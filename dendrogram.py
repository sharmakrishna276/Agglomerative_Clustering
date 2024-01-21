def input_reading():
    f = open("inp.txt", "rt")
    content = f.readlines()
    n = int(content[0].strip().split(",")[-1]) + 1
    inp_matrix = [[0 for j in range(n)] for i in range(n)]
    for i in range(n):
        row = content[i + 1].strip().split(",")[1:]
        for j in range(n):
            inp_matrix[i][j] = round(float(row[j]), 3)
    f.close()
    return inp_matrix


def hierarchical_distance(label, matrix, num):
    p = len(label)
    ans = [[0 for j in range(p)] for i in range(p)]
    for i in range(p):
        for j in range(p):
            l1 = len(label[i])
            l2 = len(label[j])
            temp = num
            for a in range(l1):
                for b in range(l2):
                    temp = min(temp, matrix[label[i][a]][label[j][b]])
            ans[i][j] = temp
    return ans


def find_label(old_labels, new_matrix, num):
    label = []
    ans = [num, 0, 0]
    n = len(new_matrix)
    for i in range(n):
        for j in range(n):
            if new_matrix[i][j] < ans[0] and new_matrix[i][j] > 0:
                ans[0] = new_matrix[i][j]
                ans[1] = i
                ans[2] = j
    if ans[1] > ans[2]:
        ans[1], ans[2] = ans[2], ans[1]

    concatenated_list = old_labels[ans[1]] + old_labels[ans[2]]
    concatenated_list.sort()
    label.append(concatenated_list)

    for i in range(len(old_labels)):
        if i != ans[1] and i != ans[2]:
            label.append(old_labels[i])
    label.sort()
    return label


def output_writing(list_of_clusters, n):
    output = open("dendrogram.txt", "w")
    output.write("(")
    for i in range(n - 1):
        output.write(str(i) + ",")
    output.write(str(n - 1) + ")" + "\n")
    for cluster in list_of_clusters:
        for item in cluster:
            if len(item) == 1:
                output.write(str(item[0]) + " ")
            elif len(item) == 0:
                continue
            else:
                output.write("(")
                for k in range(len(item) - 1):
                    output.write(str(item[k]) + ",")
                output.write(str(item[-1]) + ")" + " ")
        output.write("\n")
    output.close()
    return


inp_matrix = input_reading()
inp_label = []
list_of_labels = []
list_of_matrices = []
n = len(inp_matrix)
max_num = 0

for i in range(n):
    for j in range(n):
        max_num = max(max_num, inp_matrix[i][j])

for i in range(len(inp_matrix)):
    inp_label.append([i])

list_of_labels.append(inp_label)
list_of_matrices.append(inp_matrix)
number_of_matrices = len(inp_matrix) - 1

for i in range(number_of_matrices):
    label = find_label(list_of_labels[-1], list_of_matrices[-1], max_num)
    matrix = hierarchical_distance(label, inp_matrix, max_num)
    list_of_matrices.append(matrix)
    list_of_labels.append(label)

list_of_labels.reverse()
idx = []
list_of_clusters = []

for i in range(len(list_of_labels)):
    dendrogram = []
    label1 = list_of_labels[i]

    for cluster in label1:

        for j in range(i + 1, len(list_of_labels)):
            label2 = list_of_labels[j]
            llabel = len(label2)
            for k in range(llabel):
                for l in range(k + 1, llabel):
                    temp_list = label2[k] + label2[l]
                    temp_list.sort()
                    if temp_list == cluster:
                        if label2[k] not in dendrogram:
                            if len(label2[k]) == 1:
                                if label2[k] not in idx:
                                    dendrogram.append(label2[k])
                                    idx.append(label2[k])
                            else:
                                dendrogram.append(label2[k])
                        if label2[l] not in dendrogram:
                            if len(label2[l]) == 1:
                                if label2[l] not in idx:
                                    dendrogram.append(label2[l])
                                    idx.append(label2[l])
                            else:
                                dendrogram.append(label2[l])

                        break
                else:
                    continue
                break
    dendrogram.sort()
    list_of_clusters.append(dendrogram)

new_list_of_clusters = []

for i in range(len(list_of_clusters)):
    if list_of_clusters[i] != []:
        new_list_of_clusters.append(list_of_clusters[i])

output_writing(new_list_of_clusters, len(inp_matrix))