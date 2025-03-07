class MatrixonRings:
    def __init__(self, matrix, add_op=lambda a,b: a+b, mul_op=lambda a,b: a*b):
        self.matrix = matrix
        self.add_op = add_op
        self.mul_op = mul_op
        self.rows = len(matrix)
        self.cols = len(matrix[0])

    def __add__(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Miss dimention")
        result_matrix = [[self.add_op(self.matrix[i][j], other.matrix[i][j]) for j in range(self.cols)] for i in range(self.rows)]

        return MatrixonRings(result_matrix, self.add_op, self.mul_op)

    # можно сделать за O(n^log7)
    def matmul(self, other):
        if self.cols != other.rows:
            raise ValueError("Miss dimention")

        result_matrix = [[0 for r in range(other.cols)] for c in range(self.rows)]
        for i in range(self.rows):
            for j in range(other.rows):
                for k in range(self.cols):
                    result_matrix[i][j] = self.add_op(result_matrix[i][j], self.mul_op(self.matrix[i][k],  other.matrix[k][j]))

        return MatrixonRings(result_matrix, self.add_op, self.mul_op)

    # Hadamar mult
    def __mul__(self,other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Miss dimention")
        result_matrix = [[self.matrix[i][j] * other.matrix[i][j] for j in range(self.cols)] for i in range(self.rows)]

        return MatrixonRings(result_matrix, self.add_op, self.mul_op)

    # метод для корректного вывода
    def __repr__(self):
        return f"{self.matrix}"


