def export(rankList, key_word):
    sortedList = sorted(rankList, key = lambda k: k['rate'], reverse = True)
    lst = open('../export_files/booklist of ' + key_word, 'w+')
    for item in sortedList:
        lst.write('book title: <<' + item['title'] + '>>' + '\n')
        lst.write('pub info: ' + item['pub']+ '\n')
        lst.write('rate: ' + str(item['rate']) + ' ')
        lst.write(item['read'])
        lst.write('\n\n')
