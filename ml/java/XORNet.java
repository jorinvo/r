package me.jorin.r;

import java.io.IOException;
import java.util.Arrays;

import org.jblas.DoubleMatrix;
import org.jblas.FloatMatrix;

public class XORNet {

  public static void main(String[] args) throws IOException {
    FloatMatrix x = new FloatMatrix(new float[][]{
      {0f, 0f},
        {1f, 0f},
        {0f, 1f},
        {1f, 1f},
    });

    FloatMatrix y = new FloatMatrix(new float[][]{
      {0f},
        {1f},
        {1f},
        {0f},
    });

    NeuralNetwork model = new NeuralNetwork(new int[]{2, 2, 1}, 10f);

    model.train(x, y, 10000);

    System.out.println("Prediction: " + model.predict(x));
    System.out.println("With weights:");
    for (int w = 0; w < model.weights.length; w++) {
      System.out.println("theta " + w + ": " + model.weights[w]);
    }
  }
}

