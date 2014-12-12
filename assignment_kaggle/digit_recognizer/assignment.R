library(data.table)
library(randomForest)
library(e1071)
library(nnet)
library(neuralnet)

trainFull = read.csv("train.csv", header=TRUE)
trainFull$label = as.factor(trainFull$label)
test = read.csv("test.csv", header=TRUE)

labels = as.factor(trainFull[,1])
train = trainFull[,-1]

rf.train = randomForest(train, labels, xtest=train, ntree = 100)
predictions = levels(labels)[rf.train$test$predicted]

missclassified = which(!predictions == labels)

vectorToImage = function(vector, dim, ...){
    mat = matrix(vector, nrow = dim[1], ncol = dim[2], byrow = TRUE)
    image(t(mat)[, ncol(mat):1], ...)
}

pdf(file = "trainMissClassified.pdf")
for(i in seq_along(missclassified)){
    vectorToImage(unlist(train[missclassified[i], ]),
                  dim = c(28, 28),
                  main = paste0("should be ", labels[missclassified[i]],
                      " classified as ", predictions[missclassified[i]]))
}
graphics.off()


rf.test = randomForest(train, labels, xtest=test, ntree = 100)
predictions = levels(labels)[rf.test$test$predicted]

pdf(file = "testClassified.pdf")
for(i in sample(1:NROW(test), 100)){
    vectorToImage(unlist(test[i, ]), dim = c(28, 28),
                  main = paste0("classified as ", predictions[i]))
}
graphics.off()


## The confusion matrix
rf.test$confusion


trainSplits = sample(1:NROW(trainFull), NROW(trainFull) * 0.5)
train1 = trainFull[trainSplits, ]
train2 = trainFull[-trainSplits, ]


rf.fit = randomForest(train1[, -1], train1[, 1], xtest=train2[, -1],
    ntree = 100)
rf.predictions = levels(train2$label)[rf.fit$test$predicted]
sum(train2$label == rf.predictions)/length(rf.predictions)
missclassified = which(!rf.predictions == labels)

## add in new feature
trainMoreFeature = trainFull


newFeatures = data.frame()
for(i in 1:NROW(trainMoreFeature)){
    obs.mat = matrix(unlist(trainMoreFeature[i, -1]), nrow = 28,
        byrow = TRUE)
    rowsums = rowSums(obs.mat)
    colsums = colSums(obs.mat)
    center =  which.max(rowsums)/which.max(colsums)
    newFeatures = rbind(newFeatures, c(rowsums, colsums, center))
}
colnames(newFeatures) =
    c(paste0("rowsums", 1:28), paste0("colsums", 1:28), "center")

trainFullFeature = cbind(trainMoreFeature, newFeatures)

ggplot(trainFullFeature, aes(x = label, y = center)) + geom_point()


trainSplits =
    sample(1:NROW(trainFullFeature), NROW(trainFullFeature) * 0.5)
trainFeature1 = trainFullFeature[trainSplits, ]
trainFeature2 = trainFullFeature[-trainSplits, ]


rff.fit = randomForest(trainFeature1[, -1], trainFeature1[, 1],
    xtest = trainFeature2[, -1], ntree = 100)
rff.predictions = levels(trainFeature2$label)[rff.fit$test$predicted]
sum(trainFeature2$label == rff.predictions)/length(rff.predictions)
missclassified = which(!rff.predictions == labels)




## There is something wrong with svm for sure.
svm.train = svm(formula = label ~., data = train1)
svm.predictions = predict(svm.train, newdata = train2)
sum(train2$label == svm.predictions)/length(svm.predictions)

## Neural network
nnFormula = as.formula(paste0("label ~ ",
    paste0(colnames(train1)[-1], collapse = " + ")))
train1$label = as.numeric(as.character(train1$label))
nnet.fit = neuralnet(formula = nnFormula, data = train1,
    hidden = 10, threshold = 0.01)
nnet.predictions = predict(nnet.train, newdata = train2)
sum(train2$label == nnet.predictions)/length(nnet.predictions)








write(predictions, file="rf_benchmark.csv", ncolumns=1) 






## Plot the average digits
train.dt = data.table(trainFull)

aggregatedTrain.dt =
    train.dt[, eval(parse(text = paste0("list(",
                              paste0(colnames(train.dt)[-1],
                                     " = mean(",
                                     colnames(train.dt)[-1], ")",
                                     collapse = ", "), ")"))),
             by = "label"]
setkeyv(aggregatedTrain.dt, "label")

pdf(file = "averageDigit.pdf")
for(i in 1:NROW(aggregatedTrain.dt)){
    vectorToImage(unlist(aggregatedTrain.dt[i, -1, with = FALSE]),
                  dim = c(28, 28))
}
graphics.off()
                      
