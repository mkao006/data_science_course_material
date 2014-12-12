files = dir(patter = "part*")

foo = function(file){
    tmp = scan(file, what = c("double", "double"), sep = "\t",
        quote = "")
    matrix(as.numeric(tmp), byrow = TRUE, ncol = 2)
}

hist = matrix(ncol = 2, nrow = 0)
for(file in seq_along(files)){
    hist = rbind(hist, foo(files[file]))
}

