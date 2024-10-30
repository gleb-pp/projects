s = input("Введите ник учителя в Zoom:\n").split()
def TeacherTalk(line):
    b = 0
    for i in range(len(s)):
        if line[i] != s[i]:
            b = 1
            break
    if b == 0:
        return(True)
    else:
        return(False)

with open('chat.txt') as f:
    d = []
    for line in f:
        t = line.split()
        if len(t) >= 3:
            del t[0]
            del t[0]
            d.append(t)
    l = 0
    for line in d:
        if TeacherTalk(line):
            l = 3
            if line[-1].lower() == 'тест' or line[-1].lower() == 'test':
                l = 1
                break
    if len(d) == 0:
      print("\nОШИБКА!\nВы не скопировали чат в поле для чата.\nСделайте это и перезапустите программу.")
    elif l == 0:
        print('\nОШИБКА!\nВы неправильно ввели свой ник в Zoom.\nПерезапустите программу и введите его правильно.')
    elif l == 3:
        print('\nОШИБКА!\nВы не ввели слово "ТЕСТ" в начале теста.')
    else:
        rez = dict()
        #статусы
        #0 — cвободное общение
        #1 — прием ответов
        status = 0
        for line in d:
            if status == 0:              
                if TeacherTalk(line) and line[-2] == "Вопрос" and line[-1].isnumeric():
                    ans = dict()
                    status = 1
                    t = int(line[-1])
                elif TeacherTalk(line) and line[-2].lower() == "конец" and line[-1].lower() == 'теста':
                    break
            else:                             
                if "ответ" in (''.join(line)).lower() and TeacherTalk(line):
                    status = 0
                    cor = []
                    a = -1
                    while line[a].lower() != "ответ":
                            cor.append(line[a])
                            a -= 1
                    correct = []
                    for elem in cor:
                        correct.append(int(''.join(x for x in elem if x.isdigit())))
                    #correct = список правильных ответов
                    #ans = словарь ответов, где название элемента - ник в zoom, а значение - ответы ученика
                    for elem in ans:
                        #q - ответы ученика, но мы удаляем повторяющиеся ответы
                        name = elem
                        q = list(set(ans[elem]))
                        kl = 0
                        for elem in q:
                            if elem in correct:
                                kl += 1
                        while len(q) < len(correct):
                            q.append(0)
                        if name not in rez:
                            rez[name] = []
                            for i in range(t - 1):
                                rez[name].append('н')
                        if (kl / len(q)) >= 0.75:
                            rez[name].append('+')
                        else:
                            rez[name].append('-')
                    for elem in rez:
                        if len(rez[elem]) < t:
                            rez[elem].append('н')
                else:
                    if "кому" in line or "до" in line:
                        nam = []
                        for elem in line:
                            if elem == "кому" or elem == "до":
                                break
                            else:
                                nam.append(elem)
                        name = nam[0]
                        f = 1
                        for i in range(len(nam) - 1):
                            name += ' ' + nam[f]
                            f += 1
                        a = -1
                        otvety = []
                        while line[a] != ":":
                            otvety.append(line[a])
                            a -= 1
                        otv = []
                        for elem in otvety:
                            tes = (''.join(x for x in elem if x.isdigit()))
                            if len(tes) != 0:
                                otv.append(int(tes))
                        ans[name] = otv
if l == 1:
    print('\nРЕЗУЛЬТАТЫ:')
    for elem in rez:
        cor = 0
        for k in rez[elem]:
            if k == '+':
                cor += 1
        ball = cor / len(rez[elem])
        if ball == 1.0:
            print(elem, " — 5/5 (", *rez[elem], ") ", sep = '')
        elif (round(ball * 5, 2)) == int(ball * 5):
            print(elem, " — ", int(ball * 5), "/5", " (", *rez[elem], ") ", sep = '')
        else:
            print(elem, " — ", (round(ball * 5, 2)), "/5", " (", *rez[elem], ") ", sep = '')