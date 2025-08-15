import random
import math

# Sigmoid activation and its derivative #
def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def sigmoid_derivative(x):
    return x * (1 - x)

# Initialize a neural network with given structure #
class NeuralNetwork:
    def __init__(self, layers):
        self.layers = layers  # e.g., [2, 3, 1]
        self.weights = []
        self.biases = []

        # Randomly initialize weights and biases #
        for i in range(len(layers) - 1):
            weight_matrix = [[random.uniform(-1, 1) for _ in range(layers[i])] for _ in range(layers[i+1])]
            bias_vector = [random.uniform(-1, 1) for _ in range(layers[i+1])]
            self.weights.append(weight_matrix)
            self.biases.append(bias_vector)

    # Forward pass #
    def forward(self, input_data):
        activations = [input_data]
        for i in range(len(self.weights)):
            layer_input = []
            for j in range(len(self.weights[i])):
                weighted_sum = sum(w * a for w, a in zip(self.weights[i][j], activations[-1])) + self.biases[i][j]
                layer_input.append(sigmoid(weighted_sum))
            activations.append(layer_input)
        return activations

    # Backward pass (training) #
    def train(self, input_data, target_output, epochs=1000, learning_rate=0.1):
        for epoch in range(epochs):
            for x, y in zip(input_data, target_output):
                # Forward pass #
                activations = self.forward(x)

                # Calculate output error #
                error = [y[i] - activations[-1][i] for i in range(len(y))]
                deltas = [error[i] * sigmoid_derivative(activations[-1][i]) for i in range(len(error))]

                # Backpropagate errors #
                for i in reversed(range(len(self.weights))):
                    new_deltas = []
                    for j in range(len(self.weights[i])):
                        for k in range(len(self.weights[i][j])):
                            self.weights[i][j][k] += learning_rate * deltas[j] * activations[i][k]
                        self.biases[i][j] += learning_rate * deltas[j]

                    if i != 0:
                        for k in range(len(self.weights[i][0])):
                            error_k = sum(self.weights[i][j][k] * deltas[j] for j in range(len(deltas)))
                            new_deltas.append(error_k * sigmoid_derivative(activations[i][k]))
                        deltas = new_deltas

    # Predict #
    def predict(self, input_data):
        return self.forward(input_data)[-1]

#------ Example usage------#
if __name__ == "__main__":
    # XOR problem #
    training_inputs = [[0, 0], [0, 1], [1, 0], [1, 1]]
    training_outputs = [[0], [1], [1], [0]]

    # Create a network with 2 input neurons, 3 hidden neurons, and 1 output neuron #
    nn = NeuralNetwork([2, 3, 1])
    nn.train(training_inputs, training_outputs, epochs=10000, learning_rate=0.1)

    # Test predictions #
    for input_vector in training_inputs:
        output = nn.predict(input_vector)
        print(f"Input: {input_vector} → Output: {output}")