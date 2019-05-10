import jieba.analyse
path = 'E:/python/python_test/result.txt' #第一步爬虫结果存储的路径
file_in = open(path,'r',encoding='utf-8')
content = file_in.read()
try:
 tags = jieba.analyse.extract_tags(content, topK=100, withWeight=True)
 for v, n in tags:#权重是小数，为了凑整，乘了一万
  print(v + '\t' + str(int(n * 10000)))
finally:
 file_in.close()