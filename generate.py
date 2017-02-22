# import forwardIndex
# import invertIndex
# import json
# import time
# import threading

# dirname = "WEBPAGES_RAW/"
# f = open(dirname + "bookkeeping.json").read()
# bookkeeping = json.loads(f)

# def ForwardIndexThread(id):
#     global bookkeeping
#     for name in bookkeeping:
#         fid = int(name.split("/")[0])*500 + int(name.split("/")[1])
#         if fid % 8 == id:
#             forwardIndex.ProcessForwardIndex(dirname + name)

# t1 = time.time()
# print "ProcessForwardIndex"
# # thread_list = []
# # for i in range(0,8):
# #     t = threading.Thread(target=ForwardIndexThread,args=(i,))
# #     thread_list.append(t)
# #     t.start()
# # for t in thread_list:
# #     t.join()

# for name in bookkeeping:
#     forwardIndex.ProcessForwardIndex(dirname + name)
# t2 = time.time()
# print "Time: " + str(t2-t1)

# print "Middle"
# forwardIndex.middle("ForwardIndex", "ForwardIndexMiddle")
# forwardIndex.middle("BoldForwardIndex", "BoldForwardIndexMiddle")
# forwardIndex.middle("TitleForwardIndex", "TitleForwardIndexMiddle")
# forwardIndex.middle("H1ForwardIndex", "H1ForwardIndexMiddle")
# forwardIndex.middle("H2ForwardIndex", "H2ForwardIndexMiddle")
# forwardIndex.middle("H3ForwardIndex", "H3ForwardIndexMiddle")
# forwardIndex.middle("HeaderForwardIndex", "HeaderForwardIndexMiddle")
# # th1 = threading.Thread(target=forwardIndex.middle, args=("ForwardIndex", "ForwardIndexMiddle",))
# # th2 = threading.Thread(target=forwardIndex.middle, args=("BoldForwardIndex", "BoldForwardIndexMiddle",))
# # th3 = threading.Thread(target=forwardIndex.middle, args=("TitleForwardIndex", "TitleForwardIndexMiddle",))
# # th4 = threading.Thread(target=forwardIndex.middle, args=("H1ForwardIndex", "H1ForwardIndexMiddle",))
# # th5 = threading.Thread(target=forwardIndex.middle, args=("H2ForwardIndex", "H2ForwardIndexMiddle",))
# # th6 = threading.Thread(target=forwardIndex.middle, args=("H3ForwardIndex", "H3ForwardIndexMiddle",))
# # th7 = threading.Thread(target=forwardIndex.middle, args=("HeaderForwardIndex", "HeaderForwardIndexMiddle",))
# # th1.start()
# # th2.start()
# # th3.start()
# # th4.start()
# # th5.start()
# # th6.start()
# # th7.start()
# # th1.join()
# # th2.join()
# # th3.join()
# # th4.join()
# # th5.join()
# # th6.join()
# # th7.join()
# t3 = time.time()
# print "Time: " + str(t3-t2)

# print "invertIndex"
# invertIndex.invertedIndex("ForwardIndexMiddle", "InvertedIndex")
# invertIndex.invertedIndex("BoldForwardIndexMiddle", "BoldInvertedIndex")
# invertIndex.invertedIndex("TitleForwardIndexMiddle", "TitleInvertedIndex")
# invertIndex.invertedIndex("H1ForwardIndexMiddle", "H1InvertedIndex")
# invertIndex.invertedIndex("H2ForwardIndexMiddle", "H2InvertedIndex")
# invertIndex.invertedIndex("H3ForwardIndexMiddle", "H3InvertedIndex")
# invertIndex.invertedIndex("HeaderForwardIndexMiddle", "HeaderInvertedIndex")
# # th1 = threading.Thread(target=invertIndex.invertedIndex, args=("ForwardIndexMiddle", "InvertedIndex",))
# # th2 = threading.Thread(target=invertIndex.invertedIndex, args=("BoldForwardIndexMiddle", "BoldInvertedIndex",))
# # th3 = threading.Thread(target=invertIndex.invertedIndex, args=("TitleForwardIndexMiddle", "TitleInvertedIndex",))
# # th4 = threading.Thread(target=invertIndex.invertedIndex, args=("H1ForwardIndexMiddle", "H1InvertedIndex",))
# # th5 = threading.Thread(target=invertIndex.invertedIndex, args=("H2ForwardIndexMiddle", "H2InvertedIndex",))
# # th6 = threading.Thread(target=invertIndex.invertedIndex, args=("H3ForwardIndexMiddle", "H3InvertedIndex",))
# # th7 = threading.Thread(target=invertIndex.invertedIndex, args=("HeaderForwardIndexMiddle", "HeaderInvertedIndex",))
# # th1.start()
# # th2.start()
# # th3.start()
# # th4.start()
# # th5.start()
# # th6.start()
# # th7.start()
# # th1.join()
# # th2.join()
# # th3.join()
# # th4.join()
# # th5.join()
# # th6.join()
# # th7.join()
# t4 = time.time()
# print "Time: " + str(t4-t3)

maps = {
    '1': 'haha'
}
print maps.has_key('1')