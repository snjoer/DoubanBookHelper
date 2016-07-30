## DoubanBookHelper


### What does it do?
Sorting books based on marks from https://book.douban.com

Example:

![](https://raw.githubusercontent.com/Rafael-Cheng/doubanBooks/master/resources/4.png)

----

### How to build?
1. Install libraries yourself, which are requests, bs4 and wxPython.

2. Use command: 
```Bash
$ pip install -r requirements.txt 
```
to install libraries needed.
But I don't recommend it because it's my first time to distribute a python
project and I don't know exactly whether it works.

3. Use command: 
```Bash
python setup.py install 
```
I don't recommend it, same reason of method 2.

----

### How to use?
After installed libraries needed.
*
```Bash
python ui_doubanbookhelper.py 2
```
to start version 2
for version 1, use
```Bash
python ui_doubanbookhelper.py 1
```

Example will use version 2

Input keyword, 'Python' for example

![](https://raw.githubusercontent.com/Rafael-Cheng/doubanBooks/master/resources/1.png)

* Press Start! button to begin searching

![](https://raw.githubusercontent.com/Rafael-Cheng/doubanBooks/master/resources/2.png)

* Done

![](https://raw.githubusercontent.com/Rafael-Cheng/doubanBooks/master/resources/3.png)

* Find file 'booklist of XXX' in folder export_files
what you get is:
![](https://raw.githubusercontent.com/Rafael-Cheng/doubanBooks/master/resources/4.png)

----

### Feature
For now, two versions with UI are available, with command line argument 1 and
2 to invoke.
The 1st version only fetches data from 10 pages, which means 150 books 
realting the key word given, and output a txt file which has a sorted list 
of books based on mark in website book.douban.com.

The other one however, fetches data from 10 * 3 pages, which means 450 books. 
I think it's enough for us to choose a good book. But it's possible to 
search more books.

So if you need more data to help you make a decision. Tell me.

----

### Contact
e-mail: rafaelcheng13@gmail.com

----

## ENJOY!
