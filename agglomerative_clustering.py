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

def output_writing(label, matrix):
    n = len(matrix)
    output.write("#")
    for i in range(n):
        if len(label[i]) == 1:
            output.write("," + str(label[i][0]))
        else:
            output.write("," + "(")
            p = len(label[i])
            for j in range(p - 1):
                output.write(str(label[i][j]) + ",")
            output.write(str(label[i][p - 1]) + ")")
    output.write("\n")
    for i in range(n):
        if len(label[i]) == 1:
            output.write(str(label[i][0]))
        else:
            output.write("(")
            p = len(label[i])
            for j in range(p - 1):
                output.write(str(label[i][j]) + ",")
            output.write(str(label[i][p - 1]) + ")")
        for j in range(n):
            output.write("," + str(matrix[i][j]))
        output.write("\n")
    return

inp_matrix = input_reading()
n = len(inp_matrix)
max_num = 0

for i in range(n):
    for j in range(n):
        max_num = max(max_num, inp_matrix[i][j])

output = open("intermediateDistMats.txt", "w")

if n == 1:  # Handling the edge-case of N=1 separately
    output.write("#,0\n")
    output.write("0,0.000")

else:
    inp_label = []
    list_of_labels = []
    list_of_matrices = []

    for i in range(len(inp_matrix)):
        inp_label.append([i])

    output_writing(inp_label, inp_matrix)
    list_of_labels.append(inp_label)
    list_of_matrices.append(inp_matrix)
    number_of_matrices = len(inp_matrix) - 1

    for i in range(number_of_matrices):
        label = find_label(list_of_labels[-1], list_of_matrices[-1], max_num)
        matrix = hierarchical_distance(label, inp_matrix, max_num)
        output_writing(label, matrix)
        list_of_matrices.append(matrix)
        list_of_labels.append(label)

output.close()