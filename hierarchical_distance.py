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


def updated_distance(cluster1, cluster2, matrix, num):
    ans = num
    sz1 = len(cluster1)
    sz2 = len(cluster2)
    for i in range(sz1):
        for j in range(sz2):
            ans = min(ans, matrix[cluster1[i]][cluster2[j]])
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


def LCA(x, y, list):

    list_x = []
    list_y = []
    sz = len(list)
    flag = 0
    for i in range(sz):
        cluster = list[i]
        for item in cluster:
            if x in item and y in item:

                if i == sz - 1:
                    list_x = [x]
                    list_y = [y]

                lst = list[i + 1]

                for it in lst:
                    if x in it:
                        list_x = it
                    if y in it:
                        list_y = it

                flag = 1

    if flag == 0:
        list_x = list[0][0]
        list_y = list[0][1]

    return list_x, list_y


def output_writing(matrix):
    n = len(matrix)
    output = open("hDist.txt", "w")
    output.write("#")
    for i in range(n):
        output.write("," + str(i))
    output.write("\n")
    for i in range(n - 1):
        output.write(str(i))
        for j in range(n):
            output.write("," + str(matrix[i][j]))
        output.write("\n")
    output.write(str(n - 1))
    for i in range(n):
        output.write("," + str(matrix[n - 1][i]))
    output.close()
    return


inp_matrix = input_reading()
n = len(inp_matrix)
max_num = 0.0

for i in range(n):
    for j in range(n):
        max_num = max(max_num, inp_matrix[i][j])
inp_label = []
list_of_labels = []
list_of_matrices = []

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

hierarchical_matrix = [[0.0 for j in range(n)] for i in range(n)]

for i in range(n):
    for j in range(i + 1, n):
        cluster1, cluster2 = LCA(i, j, new_list_of_clusters)
        hierarchical_matrix[i][j] = updated_distance(cluster1, cluster2, inp_matrix, max_num)
        hierarchical_matrix[j][i] = hierarchical_matrix[i][j]

output_writing(hierarchical_matrix)