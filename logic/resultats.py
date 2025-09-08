import os
from PyPDF2 import PdfReader
from logic.eleve import Eleve
from logic.exercice import Exercice
from logic.question import Question
from logic.correction import Correction
from database import models_eleves

class Resultats:
    """
        Classe permettant de générer les fiches de résultats
        des élèves, indiquant :
            - leur note ;
            - le commentaire général sur leur copie ;
            - le barème et les points obtenus à chaque question ;
            - la qualité de l'auto-correction.
    """
    def __init__(self):
        self.evaluation = None
        self.classe = None
        self.outpath = None
        self.inpath = None
        
        self.eleves = []
        self.doublons = []
        
        self.note = 0
        
        self.eleve = Eleve()
        self.exercice = Exercice()
        self.question = Question()
        self.correction = Correction()
    
    def set_evaluation(self, evaluation, classe):
        self.evaluation = evaluation
        self.classe = classe
        self.path = f"{classe.nom}_{evaluation.titre}"
    
    def generer(self):
        """
            Génére le fichier de résultats au format .tex.
        """
        self.lister_eleves()
        
        if not os.path.exists(f"input/{self.path}"):
            os.makedirs(f"input/{self.path}")
        if not os.path.exists(f"output/{self.path}"):
            os.makedirs(f"output/{self.path}")
        
        resultats_path = os.path.join("output", self.path, "resultats")
        if not os.path.exists(resultats_path):
            os.makedirs(resultats_path)
        
        auto_correction_path = os.path.join("output", self.path, "auto_correction")
        if not os.path.exists(auto_correction_path):
            os.makedirs(auto_correction_path)
            
        for eleve in self.eleves:
            self.eleve.set(self.classe.id, eleve)
            self.note = 0
            self.generer_auto_correction()
            self.generer_resultats_eleve()
            self.generer_document()
        
    def lister_eleves(self):
        """
            Liste les élèves pour lesquels il existe un fichier
            d'auto-correction et identifie les doublons et les
            absents.
        """
        self.eleves.clear()
        self.doublons.clear()
                
        for nom in os.listdir(f"input/{self.path}"):
            if nom.lower().endswith(".pdf"):
                fichier = os.path.join("input", self.path, nom)
                lecteur = PdfReader(fichier)
                champs = lecteur.get_fields()
                nom = champs['nomselectionne'].get('/V')
                if nom in self.doublons:
                    continue
                elif nom in self.eleves:
                    self.doublons.append(nom)
                    self.eleves.remove(nom)
                else:
                    self.eleves.append(nom)
        
        absents = []
        for eleve in self.classe.lister_eleves():
            if eleve not in self.eleves:
                if eleve not in self.doublons:
                    absents.append(eleve)
        
        print(f"{len(self.eleves)} élève(s) trouvé(s) : {self.eleves}")
        print(f"{len(self.doublons)} élève(s) en double : {self.doublons}")
        print(f"{len(absents)} élève(s) absent(s) : {absents}")
                
    def generer_auto_correction(self):
        """
            Écrit les exercices avec le corrigé et les erreurs.
        """
        counter_quest = 0
        
        fichier = os.path.join(
            "input",
            self.path,
            f"{self.path}-{self.eleve.nom}.pdf"
        )
        lecteur = PdfReader(fichier)
        champs = lecteur.get_fields()
        
        self.note = 0
        total = 0
        n_erreurs = 0
        n_erreurs_cochees = 0
        n_erreurs_communes = 0
        
        with open(
            f"output/{self.path}/auto_correction/{self.eleve.nom}.tex",
            "w",
            encoding="utf-8"
        ) as f:        
            f.write("\\begin{center}\n")
            f.write("\\begin{longtable}{|C{1cm}|m{0.6\\linewidth}C{1cm}C{1cm}|C{2cm}|}\n")
            f.write("\t\\multicolumn{1}{c}{} & & Prof. & \\multicolumn{1}{c}{\\'Elève} & \\multicolumn{1}{c}{}\\\\\n")
            f.write("\\hline\n")
        
            for exercice in self.evaluation.lister_exercices():
                self.exercice.set_exercice(exercice)

                for question in self.exercice.get_questions():
                    counter_quest += 1
                    self.question.set(self.exercice.id, question[0])
                    self.correction.set(self.eleve.id, self.evaluation.id, self.question.id)
                                
                    counter_err = 0
                    # liste contenant les erreurs cochées
                    # par le professeur ou l'élève
                    erreurs = []
                    for erreur in self.question.lister_erreurs():
                        counter_err += 1
                        erreur_prof = self.correction.chercher_erreur(erreur)
                        erreur_eleve = champs[f'erreur-{counter_quest}-{counter_err}'].get('/V') == "/Yes"
                        if erreur_prof or erreur_eleve:
                            erreurs.append((erreur, erreur_prof, erreur_eleve))
                        
                        # décompte des erreurs
                        if erreur_prof:
                            n_erreurs += 1
                        if erreur_eleve:
                            n_erreurs_cochees += 1
                        if erreur_prof and erreur_eleve:
                            n_erreurs_communes += 1

                
                    # calcul des points
                    bareme = self.question.bareme
                    points = bareme * self.correction.note
                
                    self.note += points
                    total += bareme
                
                    longueur = len(erreurs)
                    commentaire = self.correction.commentaire
                    if commentaire != "":
                        longueur += 1
                    longueur = max(longueur, 1)

                    if len(erreurs) > 0:
                        for i, err in enumerate(erreurs):
                            if i == 0:
                                f.write(f"\t\\multirow{{{longueur}}}{{*}}{{\\textbf{{Q{counter_quest}.}}}}\n")
                            f.write(f"\t& {err[0]}\n")
                            if err[1]:
                                f.write("\t& \\raisebox{0.2ex}{\\color{darkgreen}\\ding{51}}\n")
                            else:
                                f.write("\t& \\raisebox{0.2ex}{\\color{red}\\ding{55}}\n")
                            if err[2]:
                                f.write("\t& \\raisebox{0.2ex}{\\color{darkgreen}\\ding{51}}\n")
                            else:
                                f.write("\t& \\raisebox{0.2ex}{\\color{red}\\ding{55}}\n")
                            f.write("\t&\n")
                            if i == 0:
                                f.write(f" \\multirow{{{longueur}}}{{*}}{{{f'{points:.2f}'.replace('.', ',')}/{f'{bareme:.2f}'.replace('.', ',')}}}\n")
                            f.write("\t\\\\\n")
                        if commentaire != "":
                            f.write(f"\t& \\textit{{{self.correction.commentaire}}} & & & \\\\\n")
                    else:
                        f.write(f"\t\\textbf{{Q{counter_quest}.}}\n")
                        f.write(f"\t& \\textit{{{self.correction.commentaire}}} & & \n")
                        f.write(f"\t& {f'{points:.2f}'.replace('.', ',')}/{f'{bareme:.2f}'.replace('.', ',')}\n")
                        f.write("\t\\\\\n")
                    
                    f.write("\\hline\n")
    
            f.write("\\end{longtable}\n")
            f.write("\\end{center}\n\n\n")
        
            self.note = self.note/total * 20
        
            # évaluation de l'auto-correction
            precision = 0
            if n_erreurs_cochees !=0:
                precision = n_erreurs_communes/n_erreurs_cochees
            rappel = 0
            if n_erreurs != 0:
                rappel = n_erreurs_communes/n_erreurs
            bonus = 0
            if precision != 0 or rappel != 0:
                bonus = round(2 * 2 * precision * rappel / (precision + rappel), 1)
        
            f.write("\\begin{center}\n")
            f.write("\\begin{tabular}{|p{7cm}c|}\n")
            f.write("\\hline\n")
            f.write("\t\\multicolumn{2}{|c|}{Auto-correction}\\\\\n")
            f.write("\\hline\n")
            f.write(f"\tErreurs réelles & {n_erreurs}\\\\\n")
            f.write(f"\tErreurs cochées & {n_erreurs_cochees}\\\\\n")
            f.write(f"\tErreurs cochées réelles & {n_erreurs_communes}\\\\\n")
            f.write(f"\tPrécision & {precision*100:.0f}\\%\\\\\n")
            f.write(f"\tRappel & {rappel*100:.0f}\\%\\\\\n")
            f.write("\\hline\n")
            f.write(f"\tBonus & {f'{bonus}'.replace('.', ',')}\\\\\n")
            f.write("\\hline\n")        
            f.write("\\end{tabular}\n")
            f.write("\\end{center}\n")
    
    def generer_resultats_eleve(self):
        """
            Écrit la note de l'élève et le commentaire sur la copie.
        """
        with open(
            f"output/{self.path}/resultats/{self.eleve.nom}.tex",
            "w",
            encoding="utf-8"
        ) as f:
            f.write("\\begin{center}\n")
            f.write("\\begin{tabular}{|C{3cm}|p{0.96\\linewidth-3cm}|}\n")
            f.write("\\hline\n")
            f.write(f"{{\\huge {f'{self.note:.2f}'.replace('.', ',')}/20}} & \\\\\n")
            f.write("\\hline\n")
            f.write("\\end{tabular}\n")
            f.write("\\end{center}\n\n")
    
    def generer_document(self):
        """
            Génère le document .tex qui rassemble les fiches
            de résultats de chaque élève.
        """
        with open(
            f"output/{self.path}/resultats.tex",
            "w",
            encoding="utf-8"
        ) as f:
            f.write("\\documentclass{ds}\n")
            f.write("\\usepackage{packages}\n")
            f.write("\\usepackage{commandes}\n")
            f.write("\\usepackage{pifont}\n")
            f.write("\n\\begin{document}\n\n")
            
            for i, eleve in enumerate(self.eleves):
                if i != 0:
                    f.write("\\newpage\n\n")
                f.write("\\begin{center}\n")
                f.write("\t\\huge\\bfseries\\sffamily{}")
                f.write(f"{self.evaluation.titre}~---~Résultats\n")
                f.write("\\end{center}\n\n")            
                f.write(f"{{\\sffamily\\Large{{}}\\textbf{{NOM: {eleve}}}}}\n\n")
                f.write(f"\\input{{resultats/{eleve}}}\n")
                f.write(f"\\input{{auto_correction/{eleve}}}\n\n")
            
            f.write("\n\\end{document}")