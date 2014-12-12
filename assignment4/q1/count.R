########################################################################
## Title: Sum the counts in file.
## Date: 2014-08-05
########################################################################

sum_count = function(file){
    tmp = scan(file = file, what = c("character", "integer"), sep = "\t",
        quote = "")
    sum(as.numeric(tmp[c(FALSE, TRUE)]))
}
sum_count("./results/part-r-00000")

files = dir("./results", full.names = TRUE)
count = 0
for(file in seq_along(files)){
    count = count + sum_count(files[file])
}

