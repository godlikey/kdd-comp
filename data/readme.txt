在当前目录下放置数据文件

## Distances to nearest subway stations.

- External data source: coordinates of BJ subway stations, obtained from
  Amap.
- Script: `subway_dist.R`
- Data files:
  - bj_subway_stations.csv  
    Lines, names and coordinates of BJ subway stations.
  - train_distance.csv  
    test_distance.csv  
    Derived variables for each sid.
- Variables:
  - sid: session id
  - o2d: straight line distance from origin to destination
  - o2st: the distance from origin to the nearest subway station
  - d2st: the distance from destination to the nearest subway station
