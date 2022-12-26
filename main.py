import csv


def specialitees(filename):
    file = open(filename, "r", encoding="utf8")
    res = dict()
    csvreader = csv.DictReader(file)
    for row in csvreader:
        try:
            res[row['Sp']] += 1
        except:
            res[row['Sp']] = 1
    print(res)
    return res


def dict2csv(d, filename, header):
    csvfile = open(filename, "w")
    writer = csv.DictWriter(csvfile, fieldnames=header)
    writer.writeheader()
    for k, v in d.items():
        aux_d = dict()
        aux_d[header[0]] = k
        aux_d[header[1]] = v
        writer.writerow(aux_d)


dict2csv(specialitees("medecin-accredites-has.csv"), "Spécialitées-HAS.csv", ["Spécialitées", "nombre"])


def spe(filename):
    file = open(filename, "r")
    csvreader = csv.DictReader(file)
    calcul = 0
    c = dict()
    for row in csvreader:
        c = row
        calcul = int(row['nombre']) / 10006 * 100

        print(c, calcul)
    return c, calcul


spe("Spécialitées-HAS.csv")


def splitbyspe(filename):
    file = open(filename, 'r', encoding="utf8")
    csvreader = csv.DictReader(file)
    header = next(csvreader)
    openFiles = dict()
    for row in csvreader:
        spee = row['Sp']
        if spee in openFiles.keys():
            openFiles[row['Sp']].writerow(row)
        else:
            outfile = open(spee + "medecin.csv", "w")
            writer = csv.DictWriter(outfile, fieldnames=header)
            writer.writeheader()
            writer.writerow(row)
            openFiles[spe] = writer


splitbyspe("medecin-accredites-has.csv")
