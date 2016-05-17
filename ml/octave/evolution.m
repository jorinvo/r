clear;



% 1. "cylinders"
% 2. "displacement"
% 3. "horsepower"
% 4. "weight"
% 5. "acceleration"
% 6. "model year"
% 7. "mpg"
cars = dlmread("cars.csv", ",", 1, 1);


% - first 6 columns as input - predict 7th column
records = cars(:, 1:6);
mpg = cars(:, 7);



% Evolution Strategy
function y = es(c, p, records, y, sigma, rounds)
  cols = columns(records);

  % Start with random models as parents
  parents = rand(p, cols) - 0.5;

  for i = 1:rounds
    % Randomly pick children from parents.
    % Mutate with random values from normal distribution.
    % sigma is standard deviation.
    children = parents(randi(p, 1, c),:) .* randn(c, cols) * sigma;

    % Pick new parents from children + parents
    parents = bestmodels([children; parents], p, records, y);
  end

  % Return best parent
  y = bestmodels(parents, 1, records, y);
end



function y = hypothesis(thetas, x, y)
  y = denormalize(sum(normalize(x) .* thetas, 2), y);
end


function y = bestmodels(models, num, records, y)
  rs = cellfun(@(x) rmse(y, hypothesis(x, records, y)), num2cell(models, 2));
  [_, indices] = sort(rs);
  y = models(indices(1:num),:);
end


function y = normalize(A)
  minA = min(A);
  y = (A - minA) ./ (max(A) - minA);
end

function y = denormalize(A, B)
  minB = min(B);
  y = A .* (max(B) - minB) + minB;
end


function y = rmse(y, r)
  y = sqrt(sum((y .- r) .^ 2) / length(y));
end




% standard deviation
sigma = 1.8


parents = 1
children = 3


model = es(children, parents, records, mpg, sigma, 300)
approxmpg = hypothesis(model, records, mpg);
RMSE = rmse(mpg, approxmpg)


% Output
arrayfun(@(l) disp(['Line ', num2str(l), ' : mpg is ', num2str(mpg(l)), ', prediction was ', num2str(approxmpg(l))]), [4, 57, 117, 219]);



% Possible output:
%
%
% model =
%
%   -0.0514460  -0.0091029  -0.0492578  -0.1183851   0.5328305   0.3874412
%
% RMSE =  5.5775
% Line 4 : mpg is 16, prediction was 8.2832
% Line 57 : mpg is 24, prediction was 18.613
% Line 117 : mpg is 29, prediction was 25.618
% Line 219 : mpg is 33.5, prediction was 26.93

