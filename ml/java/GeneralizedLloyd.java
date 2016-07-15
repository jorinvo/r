package me.jorin.r;

import java.util.stream.IntStream;

import org.jblas.FloatMatrix;
import org.jblas.MatrixFunctions;

public class GeneralizedLloyd {

  // This implementation uses a very simple splitting mechanism:
  // We just leave the old cluster and create new one that only changes
  // by `SPLIT_VALUE` in the dimension with the highest distortion
  private static final float SPLIT_VALUE = 0.1f;
  private FloatMatrix clusters;


  public void fit(int K, FloatMatrix data) {
    this.clusters = data.columnMeans();

    if (K == 1) {
      return;
    }

    FloatMatrix predictions = FloatMatrix.zeros(data.rows);

    for (int k = 1; k < K; k++) {
      // Find cluster with highest distortion
      int iClusterMax = 0;
      FloatMatrix distortionsMax = getDistortions(iClusterMax, data, predictions);
      float distortionSumMax = distortionsMax.sum();
      for (int c = 1; c < this.clusters.rows; c++) {
        FloatMatrix distortionsC = getDistortions(c, data, predictions);
        float distortionSumC = distortionsC.sum();
        if (distortionSumC > distortionSumMax) {
          iClusterMax =c;
          distortionsMax = distortionsC;
          distortionSumMax = distortionSumC;
        }
      }
      FloatMatrix clusterMax = this.clusters.getRow(iClusterMax);
      // Find dimension with with highest distortion
      int iDimensionMax = distortionsMax.argmax();
      // Split cluster
      clusterMax.put(iDimensionMax, clusterMax.get(iDimensionMax) + SPLIT_VALUE);
      this.clusters = FloatMatrix.concatVertically(this.clusters, clusterMax);
      // Update predictions
      predictions = predict(data);
      // Update cluster centers
      for (int c = 0; c < this.clusters.rows; c++) {
        FloatMatrix clusterData = getClusterData(c, data, predictions);
        this.clusters.putRow(c, clusterData.columnMeans());
      }
    }
  }

  public FloatMatrix getClusters() {
    return this.clusters;
  }

  public FloatMatrix predict(FloatMatrix data) {
    FloatMatrix predictions = new FloatMatrix(data.rows, 1);
    for (int r = 0; r < data.rows; r++) {
      predictions.put(r, MatrixFunctions.pow(this.clusters.subRowVector(data.getRow(r)), 2).rowSums().argmin());
    }
    return predictions;
  }

  private FloatMatrix getDistortions(int c, FloatMatrix data, FloatMatrix predictions) {
    FloatMatrix cluster = this.clusters.getRow(c);
    FloatMatrix clusterData = getClusterData(c, data, predictions);
    return MatrixFunctions.pow(clusterData.subRowVector(cluster), 2).columnSums();
  }

  private FloatMatrix getClusterData(int c, FloatMatrix data, FloatMatrix predictions) {
    int[] clusterDataIndices = IntStream.range(0, data.rows).filter((i) -> predictions.get(i) == c).toArray();
    return data.getRows(clusterDataIndices);
  }

}
