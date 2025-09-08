from logic.exercice import Exercice
from logic.question import Question

class CorrigeEvaluation:
    """
        Classe pour générer le corrigé d'une évaluation.
    """
    def __init__(self, evaluation, classe):
        self.evaluation = evaluation
        self.classe = classe
        self.exercice = Exercice()
        self.question = Question()
    
    def generer_corrige(self):
        """
            Corrige l'évaluation
        """    
        with open(
            f"output/{self.classe.nom}_{self.evaluation.titre}/corrige/corrige.tex",
            "w",
            encoding="utf-8"
        ) as f:
            self.start(f)            
            self.exercices(f)            
            self.end(f)

    def liste_eleves(self, f):
        """
            Crée un menu déroulant avec la liste des élèves
            de la classe.
        """
        for nom in self.classe.lister_eleves():
            f.write(f"\t{nom}={nom},\n")
    
    def exercices(self, f):
        """
            Écrit les exercices avec le corrigé et les erreurs.
        """
        counter_quest = 0
        
        # boucle sur l'ensemble des exercices de l'évaluation
        for exercice in self.evaluation.lister_exercices():
            self.exercice.set_exercice(exercice)
            f.write(f"\\section{{{exercice}}}\n\n")
            
            # crée un tableau pour chaque exercice
            f.write("\\begin{center}\n")
            f.write("\\begin{longtable}{|p{0.46\\linewidth}|p{0.46\\linewidth}|}\n")
            f.write("\\hline\n")

            # crée une ligne pour chaque question
            for question in self.exercice.get_questions():
                counter_quest += 1
                counter_err = 0
                self.question.set(self.exercice.id, question[0])
                f.write(f"\\textbf{{Q{counter_quest}.}} {self.question.reponseA} &\n")
                f.write("\\vspace{0.1cm}\n\n")
                f.write("\\begin{Form}")
                
                # crée un item pour chaque erreur, avec une case à cocher
                for erreur in self.question.lister_erreurs():
                    counter_err += 1
                    f.write("\\CheckBox[")
                    f.write(f"\tname=erreur-{counter_quest}-{counter_err},")
                    f.write("\tbackgroundcolor=1 1 1,")
                    f.write("\tbordercolor=0 0 0,")
                    f.write("\twidth=1.3em")
                    f.write(f"]{erreur}\n")
                    f.write("\\vspace{0.2cm}\n\n")
                    
                f.write("\\end{Form}")
                f.write("\\\\\n")
                f.write("\\hline\n")

            f.write("\\end{longtable}\n")
            f.write("\\end{center}\n")

    def start(self, f):
        """
            Écrit le début du document.
        """
        f.write("\\documentclass{ds}\n")
        f.write("\\usepackage{packages}\n")
        f.write("\\usepackage{commandes}\n\n")
        f.write("\\def\\LayoutCheckField#1#2{#2 #1}\n\n")
        f.write("\\hypersetup{\n")
        f.write("\tpdfborderstyle={/S/S},\n")
        f.write("\tpdfborder=0 0 0,\n")
        f.write("}\n")
        f.write("\n\\begin{document}\n\n")
        
        f.write("\\begin{center}\n")
        f.write("\t\\huge\\bfseries\\sffamily{}")
        f.write(f"{self.evaluation.titre}~---~Corrigé\n")
        f.write("\\end{center}\n")
            
        f.write("\n\\ChoiceMenu[combo, name=nom_selectionne, width=8cm, backgroundcolor=1 1 1, bordercolor=0 0 0]{\\textbf{Sélectionner votre nom :}}{\n")
        self.liste_eleves(f)
        f.write("}\n\n")

    def end(self, f):
        """
            Écrit la fin du document.
        """
        f.write("\n\\end{document}")