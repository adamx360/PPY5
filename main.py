import smtplib
from email.mime.text import MIMEText

dict_list = []

filepath = "./students.txt"


def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ','.join(recipients)
    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.login(sender, password)
    smtp_server.sendmail(sender, recipients, msg.as_string())
    smtp_server.quit()


def save():
    res = ""
    for element in dict_list:
        res += element["imie"] + " " + element["nazwisko"] + " " + element["email"] + " " + str(
            element["punkty"]) + " " + str(element["ocena"]) + " " + element["status"] + "\n"
    with open(filepath, "w") as file_object:
        file_object.write(res)


def give_grade(points):
    points = int(points)
    if 50 < points <= 60:
        grade = 3
    elif 60 < points <= 70:
        grade = 3.5
    elif 70 < points <= 80:
        grade = 4
    elif 80 < points <= 90:
        grade = 4.5
    elif points > 90:
        grade = 5
    else:
        grade = 2

    return grade


with open(filepath) as file_object:
    for x in file_object:
        line = x.rstrip().split(" ")
        student = {"imie": line[0], "nazwisko": line[1], "email": line[2], "punkty": line[3]}
        if len(line) == 4:
            student["ocena"] = ""
            student["status"] = ""
        if len(line) == 5:
            if line[4] == "2" or line[4] == "3" or line[4] == "3.5" or line[4] == "4" or line[4] == "4.5" or line[4] == "5":
                student["ocena"] = line[4]
                student["status"] = ""
            else:
                student["ocena"] = ""
                student["status"] = line[4]
        if len(line) == 6:
            student["ocena"] = line[4]
            student["status"] = line[5]
        dict_list.append(student)

opt = ""
while True:
    index = 0
    for x in dict_list:
        print(str(index) + ". " + str(x))
        index += 1
    print("==============================")
    print("0. Zakończ")
    print("1. Dodaj studenta")
    print("2. Usuń studenta")
    print("3. Wyślij maile")
    print("4. Oceń uczniów automatycznie")
    opt = input("Wybierz opcje: ")
    match opt:
        case "1":
            isUnique = True
            student = {"imie": input("Podaj imie: "), "nazwisko": input("Podaj nazwisko: ")}
            email = input("Podaj email: ")
            for x in dict_list:
                if x["email"] == email:
                    isUnique = False
            while not isUnique:
                isUnique = True
                print("Email zajety")
                email = input("Podaj email: ")
                for x in dict_list:
                    if x["email"] == email:
                        isUnique = False
            student["email"] = email
            student["punkty"] = input("Podaj punkty: ")
            student["ocena"] = input("Podaj ocenę: ")
            student["status"] = input("Podaj status: ")
            dict_list.append(student)
            save()
        case "2":
            index = input("Podaj indeks studenta którego chcesz usunąć: ")
            if len(dict_list) - 1 >= int(index) >= 0:
                dict_list.pop(int(index))
            save()
        case "3":
            for x in dict_list:
                if x["status"] != "MAILED":
                    subject = "Ocena z PPY"
                    body = "Otrzymujesz ocenę : " + str(x["ocena"])
                    sender = "testmail@gmail.com"
                    recipients = x["email"]
                    password = "password1"
                    send_email(subject, body, sender, recipients, password)
                    x["status"] = "MAILED"
            save()
        case "4":
            for x in dict_list:
                if x["status"] != "GRADED" or x["status"] != "MAILED":
                    x["ocena"] = give_grade(int(x["punkty"]))
                    x["status"] = "GRADED"
            save()
        case "0":
            save()
            break
