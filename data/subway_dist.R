library("jsonlite")    # To retrieve the JSON data.
library("geosphere")   # To calculate distances.

setwd("~/Work/kdd-comp/")

# Retrieve subway stations. Thank you, amap. ----------------------

amap_url <- "http://map.amap.com/service/subway?_1558231165055&srhdata=1100_drw_beijing.json"
bj_subway_list <- fromJSON(amap_url, simplifyVector = FALSE)

bj_st_df <- lapply(bj_subway_list$l, FUN = function(xline) {
  return(data.frame(
    id = sapply(xline$st, "[[", "sid"),
    name = sapply(xline$st, "[[", "n"),
    line = xline$ln,
    coordinates = sapply(xline$st, "[[", "sl"),
    stringsAsFactors = FALSE
  ))
})
bj_st_df <- do.call(rbind, bj_st_df)
write.csv(bj_st_df, file = "data/bj_subway_stations.csv",
          row.names = FALSE)

# Read in sample --------------------------------------------------

train_set <- read.csv("data/train_queries.csv",
                      stringsAsFactors = FALSE)
test_set <- read.csv("data/test_queries.csv",
                     stringsAsFactors = FALSE)


# Helper functions to deal with coordinates. ----------------------

godlikey_dist <- function(x, y) {
  x_list <- strsplit(x, ",")
  x_longitude <- as.numeric(sapply(x_list, "[", 1))
  x_latitude <- as.numeric(sapply(x_list, "[", 2))
  
  if (missing(y)) {
    return(distm(
      cbind(x_longitude, x_latitude),
      fun = distHaversine
    ))
  } else {
    y_list <- strsplit(y, ",")
    y_longitude <- as.numeric(sapply(y_list, "[", 1))
    y_latitude <- as.numeric(sapply(y_list, "[", 2))
    return(distm(
      cbind(x_longitude, x_latitude),
      cbind(y_longitude, y_latitude),
      fun = distHaversine
    )/1000)
  }
}


# Compute distances -----------------------------------------------

pb <- txtProgressBar(style = 3)
train_dist <- lapply(1:nrow(train_set), FUN = function(ir) {
  setTxtProgressBar(pb, ir/nrow(train_set))
  return(data.frame(
    o2d = godlikey_dist(train_set$o[ir], train_set$d[ir]),
    o2st = min(godlikey_dist(train_set$o[ir],
                             bj_st_df$coordinates)),
    d2st = min(godlikey_dist(train_set$d[ir],
                             bj_st_df$coordinates)),
    stringsAsFactors = FALSE
  ))
})
train_df <- do.call(rbind, train_dist)
train_df$sid <- train_set$sid
write.csv(train_df[, c("sid", "o2d", "o2st", "d2st")],
          "data/train_distance.csv",
          row.names = FALSE)
remove(train_dist)

pb <- txtProgressBar(style = 3)
test_dist <- lapply(1:nrow(test_set), FUN = function(ir) {
  setTxtProgressBar(pb, ir/nrow(test_set))
  return(data.frame(
    o2d = godlikey_dist(test_set$o[ir], test_set$d[ir]),
    o2st = min(godlikey_dist(test_set$o[ir],
                             bj_st_df$coordinates)),
    d2st = min(godlikey_dist(test_set$d[ir],
                             bj_st_df$coordinates)),
    stringsAsFactors = FALSE
  ))
})
test_df <- do.call(rbind, test_dist)
test_df$sid <- test_set$sid
write.csv(test_df[, c("sid", "o2d", "o2st", "d2st")],
          "data/test_distance.csv",
          row.names = FALSE)
remove(test_dist)
