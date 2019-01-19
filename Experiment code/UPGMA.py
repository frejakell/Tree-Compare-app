
from ete3 import Tree

def UPGMA(matrix, labels):
    
    while len(labels) > 1:

        min_c = float("inf")
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] < min_c:
                    min_c = matrix[i][j]
                    a, b = i, j
        if b < a:
            a, b = b, a

        row = []  
        for i in range(0, a):
            row.append((matrix[a][i] + matrix[b][i])/2)
        matrix[a] = row
        
        for i in range(a+1, b):
            matrix[i][a] = (matrix[i][a]+matrix[b][i])/2

        for i in range(b+1, len(matrix)):
            matrix[i][a] = (matrix[i][a]+matrix[i][b])/2
            del matrix[i][b]
        del matrix[b]

        labels[a] = "(" + labels[a] + "," + labels[b] + ")"

        del labels[b]

        
    return labels[0]


def main(D, labels):
    tree_1=UPGMA(D, labels)
    print(tree_1+';')
    