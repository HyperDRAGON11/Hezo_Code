class SimpleANN:
    def __init__(self, input_size, hidden_size, output_size, learning_rate=0.1):
        self.learning_rate = learning_rate
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.W1 = [[(i+j)/100 for j in range(hidden_size)] for i in range(input_size)]
        self.b1 = [0 for _ in range(hidden_size)]
        self.W2 = [[(i+j)/100 for j in range(output_size)] for i in range(hidden_size)]
        self.b2 = [0 for _ in range(output_size)]

    def sigmoid(self, x):
        return 1 / (1 + pow(2.71828, -x))

    def sigmoid_deriv(self, x):
        return x * (1 - x)

    def forward(self, X):
        self.Z1 = []
        self.A1 = []
        for i in range(len(X)):
            z1 = [sum([X[i][k] * self.W1[k][j] for k in range(self.input_size)]) + self.b1[j] for j in range(self.hidden_size)]
            a1 = [self.sigmoid(z1[j]) for j in range(self.hidden_size)]
            self.Z1.append(z1)
            self.A1.append(a1)
        self.Z2 = []
        self.A2 = []
        for i in range(len(X)):
            z2 = [sum([self.A1[i][k] * self.W2[k][j] for k in range(self.hidden_size)]) + self.b2[j] for j in range(self.output_size)]
            a2 = [self.sigmoid(z2[j]) for j in range(self.output_size)]
            self.Z2.append(z2)
            self.A2.append(a2)
        return self.A2

    def backward(self, X, y, output):
        for i in range(len(X)):
            error = [y[i][j] - output[i][j] for j in range(self.output_size)]
            d_output = [error[j] * self.sigmoid_deriv(output[i][j]) for j in range(self.output_size)]
            error_hidden = [sum([d_output[k] * self.W2[j][k] for k in range(self.output_size)]) for j in range(self.hidden_size)]
            d_hidden = [error_hidden[j] * self.sigmoid_deriv(self.A1[i][j]) for j in range(self.hidden_size)]
            for j in range(self.hidden_size):
                for k in range(self.output_size):
                    self.W2[j][k] += self.learning_rate * self.A1[i][j] * d_output[k]
            for k in range(self.output_size):
                self.b2[k] += self.learning_rate * d_output[k]
            for j in range(self.input_size):
                for k in range(self.hidden_size):
                    self.W1[j][k] += self.learning_rate * X[i][j] * d_hidden[k]
            for k in range(self.hidden_size):
                self.b1[k] += self.learning_rate * d_hidden[k]

    def train(self, X, y, epochs=1000):
        for i in range(epochs):
            output = self.forward(X)
            self.backward(X, y, output)
            if i % 100 == 0:
                loss = sum([(y[m][0] - output[m][0]) ** 2 for m in range(len(X))]) / len(X)
                print("Epoch", i, "Loss:", round(loss, 4))

    def predict(self, X):
        output = self.forward(X)
        return [[1 if o[0] > 0.5 else 0] for o in output]

if __name__ == "__main__":
    X = [[0,0],[0,1],[1,0],[1,1]]
    y = [[0],[1],[1],[0]]
    ann = SimpleANN(2,4,1,0.1)
    ann.train(X,y,2000)
    pred = ann.predict(X)
    print("Predictions:")
    for p in pred:
        print(p)