clear;



% 1. "cylinders" = Anzahl der Zylinder
% 2. "displacement" = Hubraum
% 3. "horsepower" = Pferdestärke (PS)
% 4. "weight" = Gewicht in Pfund
% 5. "acceleration" = Zeit von 0 auf 60 Meilen pro Stunde
% 6. "model year" = Erscheinungsdatum
% 7. "mpg" = Meilen pro Gallone
cars = dlmread("cars.csv", ",", 1, 1);


% - first 6 columns as input - predict 7th column
global records = cars(:, 1:6);
global mpg = cars(:, 7);



% Linear Regression using Gradient Decent
%
% Returns:
% - Last (and hopefully best) theta values
% - List of RMSE values from each round
function [thetas, rmses] = lr(x, y, a, n, t)
  xn = normalize(x);
  yn = normalize(y);
  thetas = t;
  rmses = [];
  for i = 1:n
    yh = hypothesis(thetas, xn);
    rmses(i) = rmse(y, denormalize(yh, y));
    thetas = thetas - a * mean((yh - yn) .* xn);
  end
  rmses(end + 1) = rmse(y, denormalize(yh, y));
end


function prediction = hypothesis(thetas, x)
  prediction = sum(x .* thetas, 2);
end


function N = normalize(A)
  minA = min(A);
  N = (A - minA) ./ (max(A) - minA);
end

function D = denormalize(A, B)
  minB = min(B);
  D = A .* (max(B) - minB) + minB;
end;


function err = rmse(y, r)
  err = sqrt(sum((y .- r) .^ 2) / length(y));
end




global rounds = 100;
global startthetas = rand(1, columns(records)) - 0.5;


% Output for each graph
function [] = output(a, style)
  global records mpg rounds startthetas;
  [thetas, rmses] = lr(records, mpg, a, rounds, startthetas);
  plot(1:(rounds + 1), rmses, style);
  disp(['Best RMSE for alpha ' num2str(a) ' is: ' num2str(rmses(end))]);
  disp(['with thetas: ' num2str(thetas)]);
end


% Execution and drawing
figure('units', 'normalized', 'outerposition', [0.1 0.1 0.8 0.8]);
hold on;
axis([1 rounds 0 50]);
ylabel("RMSE");
xlabel("Iteration");

alphas = [0.01, 0.10, 1.00, 2.00];
output(alphas(1), '-b');
output(alphas(2), '-g');
output(alphas(3), '-r');
output(alphas(4), '-m');

legend(num2str(alphas(:)));



% Possible output:
%
%
% Best RMSE for alpha 0.01 is: 12.367
% with thetas: 0.39491      0.13328     -0.10268     0.013045      0.16364     0.057524
% Best RMSE for alpha 0.1 is: 5.9332
% with thetas: 0.18072    -0.056223      -0.1635     -0.13575      0.41948       0.3885
% Best RMSE for alpha 1 is: 4.8499
% with thetas: 0.083948     -0.12786      0.26448     -0.41415      0.57737      0.36746
% Best RMSE for alpha 2 is: 35136020214373.66
% with thetas: 614305368303.618       420405370557.17      381840624246.089      472268538872.599      431758983484.921      500929892890.513
