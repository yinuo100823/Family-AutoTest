# !/usr/bin/env python
# -*- coding:utf-8 -*-
from common.FileUtils import read_file_to_list

#searchDuplicateData查找一个数组中是否有重复的数据并打印重复数据及其数量
def search_duplicate_data(source,data_type="file"):
    if data_type=="file":
        source = read_file_to_list(source)
    result_map={data :source.count(data) for data in source if source.count(data)>1}
    for k,v in result_map.items():
        print(k, ":", v)
    return result_map

#checkAllItemInCollection查找一个容器内的元素是否都在另外一个容器内
def check_all_item_in_other_collection(source,target,data_type="file"):
    if data_type=="file":
        source = read_file_to_list(source)
        target = read_file_to_list(target)
    result=set(source).difference(set(target))
    # result=list(x for x in source if x not in target)
    for data in result:print(data)
    return result
if __name__ == '__main__':
    search_duplicate_data("source")

    # check_all_item_in_other_collection("target","source")
