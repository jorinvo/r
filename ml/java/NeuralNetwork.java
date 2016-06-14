package me.jorin.r;

import java.util.stream.IntStream;

import org.jblas.FloatMatrix;
import org.jblas.MatrixFunctions;

public class NeuralNetwork {

	public FloatMatrix[] weights;
	public int bias = 1;
	public float learnRate = 1;

	public NeuralNetwork() {
	}

	public NeuralNetwork(int[] size, float alpha) {
		learnRate = alpha;

		weights = new FloatMatrix[size.length - 1];
		for (int w = 0; w < weights.length; w++) {
			weights[w] = FloatMatrix.rand(size[w] + 1, size[w + 1]).sub(0.5f);
		}
	}

	public FloatMatrix predict(FloatMatrix x) {
		FloatMatrix layer = x;
		for (int w = 0; w < weights.length; w++) {
			layer = nonlin(addBias(layer).mmul(weights[w]));
		}
		return layer;
	}

	public void train(FloatMatrix x, FloatMatrix y, int iterations) {
		int m = x.rows;
		for (int i = 0; i < iterations; i++) {
			FloatMatrix[] layers = forwardPass(x);
			FloatMatrix error = layers[layers.length - 1].sub(y);
			FloatMatrix[] changes = backpropagation(layers, error);
			for (int w = 0; w < weights.length; w++) {
				weights[w] = weights[w].sub(changes[w].mul(learnRate / m));
			}
		}
	}

	private FloatMatrix[] forwardPass(FloatMatrix x) {
		FloatMatrix layer = x;
		FloatMatrix[] layers = new FloatMatrix[weights.length + 1];
		layers[0] = layer;
		for (int w = 0; w < weights.length; w++) {
			layer = nonlin(addBias(layer).mmul(weights[w]));
			layers[w + 1] = layer;
		}
		return layers;
	}

	private FloatMatrix[] backpropagation(FloatMatrix[] layers, FloatMatrix error) {
		FloatMatrix prediction = layers[layers.length - 1];
		FloatMatrix delta = error.mul(prediction.mul(prediction.rsub(1)));
		FloatMatrix[] deltas = new FloatMatrix[weights.length];
		deltas[deltas.length - 1] = delta;
		for (int d = deltas.length - 2; d >= 0; d--) {
			FloatMatrix weightNoBias = weights[d + 1].getRows(IntStream.range(1, weights[d + 1].rows).toArray());
			FloatMatrix o = layers[d + 1].mul(layers[d + 1].rsub(1));
			delta = delta.mmul(weightNoBias.transpose()).mul(o);
			deltas[d] = delta;
		}
		FloatMatrix[] changes = new FloatMatrix[weights.length];
		for (int c = 0; c < changes.length; c++) {
			changes[c] = addBias(layers[c]).transpose().mmul(deltas[c]);
		}
		return changes;
	}

	private FloatMatrix nonlin(FloatMatrix x) {
		return sigmuid(x);
	}

	private FloatMatrix sigmuid(FloatMatrix x) {
		return MatrixFunctions.pow((float) Math.E, x.mul(-1)).add(1).rdivi(1);
	}

	private FloatMatrix tanh(FloatMatrix x) {
		return MatrixFunctions.tanh(x);
	}

	private FloatMatrix addBias(FloatMatrix x) {
		return FloatMatrix.concatHorizontally(FloatMatrix.ones(x.rows, 1).mul(bias), x);
	}
}
