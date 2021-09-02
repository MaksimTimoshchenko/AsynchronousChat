import subprocess


print('Задание 1')
words = ['разработка', 'сокет', 'декоратор']
words_utf8 = [
    b'\xd1\x80\xd0\xb0\xd0\xb7\xd1\x80\xd0\xb0\xd0\xb1\xd0\xbe\xd1\x82\xd0\xba\xd0\xb0', 
    b'\xd1\x81\xd0\xbe\xd0\xba\xd0\xb5\xd1\x82', 
    b'\xd0\xb4\xd0\xb5\xd0\xba\xd0\xbe\xd1\x80\xd0\xb0\xd1\x82\xd0\xbe\xd1\x80'
]

for index, word in enumerate(words):
    print(len(word), type(word))
    encoded_word = word.encode('UTF-8')
    print(len(encoded_word), type(encoded_word), words_utf8[index] == encoded_word)


print('Задание 2')    
words = ['class', 'function', 'method']

for word in words:
    encoded_word = bytes(word, 'UTF-8')
    print(type(encoded_word), encoded_word, len(encoded_word))  


print('Задание 3')
words = ['класс', 'функция', 'attribute', 'type']

for word in words:
    encoded_word = bytes(word, 'UTF-8')
    print(encoded_word, type(encoded_word))
    
    
print('Задание 4')
words = ['разработка', 'администрирование', 'protocol', 'standard']

for word in words:
    encoded_word = word.encode('UTF-8')
    decoded_word = encoded_word.decode('UTF-8')
    print(decoded_word)
    
    
print('Задание 5')
args = ['ping', 'youtube.com']
subprocess_ping = subprocess.Popen(args, stdout=subprocess.PIPE)

for line in subprocess_ping.stdout:
    line = line.decode('cp866').encode('utf-8')
    print(line.decode('utf-8'))


print('Задание 6')
f = open('test_file.txt', 'r')
print(f.encoding)
f.close()

with open('test_file.txt', 'r', encoding='UTF-8') as f:
    for line in f:
        print(line)
