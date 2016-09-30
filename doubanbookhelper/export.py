def export(rankList, filepath):
    sortedList = sorted(rankList, key = lambda k: k['rate'], reverse = True)
    lst = open(filepath, 'w+')
    for item in sortedList:
        lst.write('book title: <<' + item['title'] + '>>' + '\n')
        lst.write('pub info: ' + item['pub']+ '\n')
        lst.write('rate: ' + str(item['rate']) + ' ')
        lst.write(item['read'])
        lst.write('\n\n')
    lst.close()
