import csv


def specialitees(filename):
    """
    :param filename: Fichier csv qui répertorie les spécialistes accrédités par la Haute Autorité de Santé
    :return: renvoie un dictionnaire avec le nombre de médecins  accrédités par spécialité
    """
    file = open(filename, "r", encoding="utf8")
    nombre = dict()
    csvreader = csv.DictReader(file)
    for row in csvreader:  # compte le nombre de medecins par spécialités
        try:
            nombre[row['Spécialité']] += 1 #compte un nouveau médecin dans cette spécialité
        except:
            nombre[row['Spécialité']] = 1 #ajoute une nouvelle spécialité dans le dictionnaire
    print(nombre)
    return nombre


def dict2csv(dico, file, header):
    """
    :param dico:dictionnaire généré par la fonction
    :param file: Fichier Csv tampon qui classera les Spécialités medecales avec leurs pourcentages
    :param header: paramètre qui inscrit l'en-tête dans le fichier Csv Tampon
    :return:Il inscrit dans le fichier Spécialités-HAS.csv la spécialité et son pourcentage
    """
    csvfile = open(file, "w") # ouverture du fichier tampon en mode écriture
    writer = csv.DictWriter(csvfile, fieldnames=header)
    writer.writeheader() #écriture des en-têtes
    for k, v in dico.items():  # boucle qui prend comme valeur k la spécialité et v comme nombre de spécialistes
        aux_d = dict()
        aux_d[header[0]] = k  # inscrit dans la colonne Spécialité son nom
        aux_d[header[1]] = round(int(v) / 10006 * 100, 2)  # formule utilisé pour effectuer un pourcentage
        writer.writerow(aux_d)  # inscrit le contenue dans le fichier CSV


dict2csv(specialitees("medecin-accredites-has.csv"), "Spécialités-HAS.csv", ["Spécialités", "Pourcentage (%)"])


def splitbyspe(filename):
    """
    :param filename:Fichier csv qui répertorie les spécialistes en médecine accrédités par la Haute Autorité de Santé
    :return:il va générer un fichier csv par spécialité avec les noms des différents praticiens
    """
    file = open(filename, 'r', encoding="utf8") # ouverture du fichier tampon en mode lecture
    csvreader = csv.DictReader(file)
    header = next(csvreader) #écriture de l'en-tête
    openfiles = dict()
    for row in csvreader:
        spee = row['Spécialité']
        if spee in openfiles.keys():
            openfiles[row['Spécialité']].writerow(row) #ajout d'une nouvelle ligne
        else:
            outfile = open(spee + ".csv", "w") #Génération du fichier csv contenant les informations sur les spécialites
            writer = csv.DictWriter(outfile, fieldnames=header) #ouverture du fichier .csv
            writer.writeheader() #écriture des en-têtes
            writer.writerow(row) #écriture de la  première ligne
            openfiles[spee] = writer


splitbyspe("medecin-accredites-has.csv")


def htmlpage1():
    """
    :return:Génération de la page HTML/le tableau qui présente le pourcentage d'acréditations par spécialité
    """
    htmlout = open("tableau_principal.html", "w") # ouverture du fichier index en mode écriture
    htmlout.write("<!DOCTYPE html><html> <head><link rel='stylesheet' type='text/css' href='style.css'></head><body> <h1>Proportion "
                  "de medecin accrédité en fonction de la spécialité</h1>")  #écriture du début de la page HTML
    htmlout.write("<table><thead></thead><th>Spécialités Médicales</th> <th>Pourcentage d'accréditations (%)</th>") #écriture de l'en-tête du tableau
    file = open("Spécialités-HAS.csv", "r")
    csvreader = csv.DictReader(file)
    html = ""
    for row in csvreader: #boucle qui inscrit dans le fichier Index.html les informations contenues dans le fichier Spécialités-HAS.csv
        html += "<tr><td><a href='" + row['''Spécialités'''] + ".html'>" + row['Spécialités'] + "</a></td> <td class = 'nombre'>" + row["Pourcentage (%)"] + "</td></tr>"
    htmlout.write(html) #écriture dans le fichier le contenu de la variable "html"
    htmlout.write("</tbody></table></body></html>") #fin d'écriture du fichier html
    htmlout.close()#fermeture du fichier


htmlpage1()


def listespecialistes():
    """
    :return:Génération d'une page HTML par spécialité qui donne des informations sur les praticiens
    """
    file = open("Spécialités-HAS.csv", "r") # ouverture du fichier Spécialités-HAS.csv en mode lecture
    csvreader = csv.DictReader(file)
    for row in csvreader:
        filep = open(row["Spécialités"] + ".csv", "r") # ouverture du fichier csv en mode lecture
        csvreader = csv.DictReader(filep)
        htmloutp = open(row["Spécialités"] + ".html", "w")  # création d'un fichier html avec comme titre la spécialité
        htmloutp.write("<!DOCTYPE html><html><head><link rel='stylesheet' type='text/css' href='style.css'></head><body><h1>" + row["Spécialités"] + "</h1>")#écriture du début de la page HTML

        htmloutp.write("<table><thead></thead><th>Nom</th><th>Prénom</th><th>Date d'accréditation</th><th>Département</th><th>Statut</th>") #écriture de l'en-tête du tableau
        html = ""
        for rew in csvreader:#boucle qui inscrit dans le fichier Index.html les informations contenues dans le fichier Spécialités-HAS.csv
            html += "<tr><td class = 'valeur'>" + rew['Nom'] + "</td><td class = 'valeur'>" + rew[
                "Prénom"] + "</td> <td class = 'valeur'>" + rew["Date accréditation"] + "</td><td class = 'valeur'>" + \
                    rew["Département"] + "</td><td class = 'valeur'>" + rew["Statut"] + "</td></tr>"
        htmloutp.write(html)
        htmloutp.write("</tbody></table></body></html>")
        htmloutp.close()


listespecialistes()


def csstab():
    """

    :return: Fonction qui génére un fichier de CSS pour les tableaux
    """
    fcss = open("style.css", "w")  # ouverture du fichier css en mode écriture
    fcss.write("""
    table {
    table-layout: fixed;
    width: 100%;
    border-collapse: collapse;
    border: 3px solid black;
    background: linear-gradient(45deg, #F6FDFF 0%, #F8FDFF 100%);
    }

    thead th:nth-child(1) {
    width: 30%;
    
    }

    thead th:nth-child(2) {
    width: 20%;
    }

    thead th:nth-child(3) {
    width: 15%;
    }

    thead th:nth-child(4) {
    width: 35%;
    }

    td {
     padding: 20px;
     font-size:25px;
     padding-right: 3em;
     border: 0.5px solid black;
    }
    th{
     padding: 20px;
     font-size:28px;
     padding-right: 3em;
     border: 0.5px solid black;
    }

    .nombre{
    font-size: 25px;
    padding-left: 20%;
    }

    .valeur{
    font-size: 20px;
     padding-left: 7%;
    }""")
    fcss.close()


csstab()