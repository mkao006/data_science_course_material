# makes the random forest submission

library(randomForest)

train = read.csv("train.csv", header=TRUE)
test = read.csv("test.csv", header=TRUE)

labels = as.factor(train[,1])
train = train[,-1]

rf = randomForest(train, labels, xtest=test, ntree = 100)
predictions = levels(labels)[rf$test$predicted]


rf = randomForest(train, labels, xtest=test, ntree = 100)

write(predictions, file="rf_benchmark.csv", ncolumns=1) 
