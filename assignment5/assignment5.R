library(caret)
library(rpart)
library(tree)
library(randomForest)
library(e1071)
library(ggplot2)

## Read the data
seaflow.df = read.csv(file = "seaflow_21min.csv",
    stringsAsFactors = TRUE)

## Split the data
splitIndex = sample(x = NROW(seaflow.df), size = NROW(seaflow.df) * 0.5)
test.df = seaflow.df[splitIndex, ]
training.df = seaflow.df[-splitIndex, ]


## Question 3
mean(training.df$time)

## Question 4
ggplot(test.df, aes(x = pe, y = chl_small, col = pop)) + geom_point()


## Build the model
formula = pop ~ fsc_small + fsc_perp + fsc_big + pe + chl_big + chl_small
tree.fit = rpart(formula, method = "class", data = training.df)

## Predict
prediction = predict(tree.fit, test.df)
test.df$treePrediction =
    attr(prediction, "dimnames")[[2]][apply(prediction, 1, which.max)]

## Question 8
sum(with(test.df, pop == treePrediction))/NROW(test.df)


forest.fit = randomForest(formula, data = training.df)

test.df$forestPrediction = predict(forest.fit, test.df)

## Question 8
sum(with(test.df, pop == forestPrediction))/NROW(test.df)


svm.fit = svm(formula, data = training.df)

test.df$svmPrediction = predict(svm.fit, test.df)
sum(with(test.df, pop == svmPrediction))/NROW(test.df)


with(test.df, table(pred = treePrediction, true = pop))
with(test.df, table(pred = forestPrediction, true = pop))
with(test.df, table(pred = svmPrediction, true = pop))

lapply(seaflow.df, function(x) length(unique(x)))


ggplot(data = seaflow.df, aes(x = time, y = chl_big, col = pop)) +
    geom_point()
ggplot(data = seaflow.df[seaflow.df$file_id != 208, ],
       aes(x = time, y = chl_big, col = pop)) +
    geom_point()


## svm without corrupted data
## cleanTraining.df = training.df[training.df$file_id != 208, ]
## ggplot(data = cleanTraining.df, aes(x = time, y = chl_big, col = pop)) +
##     geom_point()
## ggplot(data = cleanTraining.df, aes(x = pe, y = chl_small, col = pop)) +
##     geom_point()
## ggplot(data = training.df, aes(x = pe, y = chl_small, col = file_id == 208)) +
##     geom_point(alpha = 0.2)

cleanSeaflow.df = seaflow.df[seaflow.df$file_id != 208, ]
splitIndex = sample(x = NROW(cleanSeaflow.df),
    size = NROW(cleanSeaflow.df) * 0.5)
cleanTest.df = cleanSeaflow.df[splitIndex, ]
cleanTraining.df = cleanSeaflow.df[-splitIndex, ]

svmClean.fit = svm(formula, data = cleanTraining.df)

cleanTest.df$svmCleanPrediction = predict(svmClean.fit, cleanTest.df)
sum(with(cleanTest.df, pop == svmCleanPrediction))/NROW(cleanTest.df)

sum(with(cleanTest.df, pop == svmCleanPrediction))/NROW(cleanTest.df) -
    sum(with(test.df, pop == svmPrediction))/NROW(test.df)
