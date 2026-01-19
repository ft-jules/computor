"""
Classe Matrix : Gère les opérations matricielles.
"""
from .complex import Complex
from src.utils.errors import MathError

class Matrix:
    def __init__(self, data):
        if not isinstance(data, list) or not data:
            raise MathError("Matrix cannot be empty")
        self.rows = len(data)
        self.cols = len(data[0])

        self.data = []

        for row in data:
            if not isinstance(row, list):
                raise MathError("Matrix must be a list of lists")
            if len(row) != self.cols:
                raise MathError("Matrix must be rectangular (all rows must have same lenght)")
            new_row = []
            for item in row:
                if not isinstance(item, Complex):
                    item = Complex(item)
                neww_row.append(item)
            self.data.append(new_row)

    def __repr__(self):
        row_str = []
        for row in self.data:
            row_content = ", ",join(str(item) for item in row)
            row_str.append(f"[{row_content}]")
        return f"[{', '.join(row_str)}]"

    def __eq__(self, other):
        if not isistance(other, Matrix):
            return False
        if self.rows != other.rows or self.cols != other.cols:
            return False
        for i in range(self.rows):
            for j in range(self.cols):
                if self.data[i][j] != other.data[i][j]:
                    return False
        return True

    # -------------------OPERATIONS MATRICIELLES------------------- #

    def __add__(self, other):
        if not isisntance(other, Matrix):
            raise MathError("Cannot add matrix and Scalar")
        if self.rows != other.rows or self.cols != other.cols:
            raise MathError(f"Dimension mismatch for addition: ({self.rows},{self.cols}) vs ({other.rows},{other.cols})")
        
        new_data = []
        for i in range(self.rows):
            new_row = []
            for j in range(self.cols):
                new_row.append(self.data[i][j] + other.data[i][j])
            new_data.append(new_row)

        return Matrix(new_data)