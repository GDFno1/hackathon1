import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import random
import json
import os
from datetime import datetime


QUESTIONS_JSON = "questions.json"
RESULTS_TXT = "results.txt"
QUIZ_DURATION_SECONDS = 300 


EMBEDDED_QUESTIONS = [
    {
        "question": "Galvenie OOP principi:",
        "type": "checkbox",
        "options": ["Inkapulācija", "Mantojums", "Abstrakcija", "Formatēšana"],
        "correct": ["Inkapulācija", "Mantojums", "Abstrakcija"],
        "explanation": "OOP galvenie principi ir inkapsulācija (datu slēpšana), mantojums (klases īpašību nodošana) un abstrakcija (vērtīgo īpašību izcelšana)."
    },
    {
        "question": "Kas ir klase?",
        "type": "radio",
        "options": ["Objekta instances", "Šablons objektu izveidei", "Mainīgo tips"],
        "correct": "Šablons objektu izveidei",
        "explanation": "Klase ir definīcija vai šablons, pēc kura tiek veidoti objekti (instances)."
    },
    {
        "question": "Kā sauc procesu, kad tiek izveidots objekts?",
        "type": "entry",
        "correct": "instanciēšana",
        "explanation": "Objekta izveidi parasti sauc par instanciēšanu (instantiation)."
    },
    {
        "question": "Kurš variants apraksta inkapsulāciju?",
        "type": "radio",
        "options": ["Iekšējo datu slēpšana", "Mantojuma izmantošana", "Jaunu objektu izveide"],
        "correct": "Iekšējo datu slēpšana",
        "explanation": "Inkapsulācija nozīmē slēpt objekta iekšējo stāvokli un piekļūt tam caur publiskām metodēm."
    },
    {
        "question": "Izvēlies polimorfisma piemērus:",
        "type": "checkbox",
        "options": ["Metodes pārslodze", "Metodes pārrakstīšana", "Objekta izveide", "Mainīgā izmantošana"],
        "correct": ["Metodes pārslodze", "Metodes pārrakstīšana"],
        "explanation": "Polimorfisms ļauj metodēm uzvesties atšķirīgi kontekstā — pārslodze un pārrakstīšana ir polimorfisma veidi."
    },
    {
        "question": "Kas ir objekts?",
        "type": "radio",
        "options": ["Instances klase", "Klases nosaukums", "Klases instances"],
        "correct": "Klases instances",
        "explanation": "Objekts ir klases instances (konkrēta klases izpausme ar stāvokli un uzvedību)."
    },
    {
        "question": "Ievadi terminu: spēja objektiem būt dažādās formās — tas ir...",
        "type": "entry",
        "correct": "polimorfisms",
        "explanation": "Polimorfisms nozīmē, ka vienam interfeisam var būt vairākas realizācijas."
    },
    {
        "question": "Izvēlies klases sastāvdaļas:",
        "type": "checkbox",
        "options": ["Metodes", "Lauki (atribūti)", "Mapes", "Faili"],
        "correct": ["Metodes", "Lauki (atribūti)"],
        "explanation": "Klase parasti satur laukus (atribūtus) un metodes; mapes un faili nav klases daļas."
    },
    {
        "question": "Kā sauc mehānismu, kad īpašības tiek nodotas no vienas klases citai?",
        "type": "radio",
        "options": ["Inkapsulācija", "Polimorfisms", "Mantojums"],
        "correct": "Mantojums",
        "explanation": "Mantojums ļauj vienai klasei (apakšklasei) iegūt citu klasi (superklasi) īpašības."
    },
    {
        "question": "Ko dara konstruktors?",
        "type": "entry",
        "correct": "inicializē objektu",
        "explanation": "Konstruktors parasti inicializē objektu — piešķir sākotnējos atribūtus."
    },
    {
        "question": "Abstrakcija nozīmē:",
        "type": "radio",
        "options": ["Datu slēpšana", "Svarīgo īpašību izcelšana", "Īpašību nodošana"],
        "correct": "Svarīgo īpašību izcelšana",
        "explanation": "Abstrakcija nozīmē koncentrēšanos uz būtisko, ignorējot detaļas."
    },
    {
        "question": "Izvēlies pareizus mantojuma piemērus:",
        "type": "checkbox",
        "options": ["Klase Dog manto no Animal", "Klase Car manto no Engine", "Klase Window manto no Container", "Klase Math manto no Number"],
        "correct": ["Klase Dog manto no Animal", "Klase Window manto no Container"],
        "explanation": "Mantojums bieži izmanto 'is-a' attiecības (piem., Dog is an Animal). Car no Engine nav loģiska 'is-a' attiecība."
    },
    {
        "question": "Kāds ir konstruktora nosaukums biežāk programmēšanas valodās?",
        "type": "entry",
        "correct": "__init__",
        "explanation": "Python konstruktors parasti ir __init__; citās valodās var būt atšķirīgi nosaukumi."
    },
    {
        "question": "Ko nozīmē private?",
        "type": "radio",
        "options": ["Pieejams tikai klasē", "Pieejams visur", "Pieejams tikai apakšklasēs"],
        "correct": "Pieejams tikai klasē",
        "explanation": "Private nozīmē ierobežotu piekļuvi — parasti tikai pašā klasē."
    },
    {
        "question": "Izvēlies piekļuves modifikatorus:",
        "type": "checkbox",
        "options": ["public", "private", "protected", "system"],
        "correct": ["public", "private", "protected"],
        "explanation": "Standarta modifikatori ir public, private un protected; 'system' nav tipisks OOP modifikators."
    },
    {
        "question": "Kas ir lauks (field) objektā?",
        "type": "radio",
        "options": ["Funkcija", "Globāla mainīgā", "Mainīgais klasē/objektā"],
        "correct": "Mainīgais klasē/objektā",
        "explanation": "Lauks vai atribūts ir mainīgais, kas pieder klasei vai objektam."
    },
    {
        "question": "Ievadi terminu: objekta raksturojoša īpašība — tas ir...",
        "type": "entry",
        "correct": "atribūts",
        "explanation": "Atribūts (attribute) apraksta objekta stāvokli."
    },
    {
        "question": "Statiskie metodes pieder:",
        "type": "radio",
        "options": ["Objektam (instance)", "Klasei", "Modulim"],
        "correct": "Klasei",
        "explanation": "Statiskas metodes tiek sauktas no klases līmeņa un nav saistītas ar konkrētu instanci."
    },
    {
        "question": "Izvēlies pareizus objektu piemērus:",
        "type": "checkbox",
        "options": ["Galda objekts", "Lietotāja logs", "Klase Animal", "Cilvēks kā objekts"],
        "correct": ["Galda objekts", "Lietotāja logs", "Cilvēks kā objekts"],
        "explanation": "Objekti ir konkrētas instances; klase Animal nav objekts, tā ir definīcija."
    },
    {
        "question": "Kā sauc spēju slēpt iekšējo realizāciju?",
        "type": "entry",
        "correct": "inkapsulācija",
        "explanation": "Inkapsulācija slēpj detaļas un nodrošina skaidru interfeisu."
    },
    {
        "question": "Kas ir metode?",
        "type": "radio",
        "options": ["Klase", "Funkcija klasē", "Objekts"],
        "correct": "Funkcija klasē",
        "explanation": "Metode ir funkcija, kas definēta klasē un darbojas uz objektiem."
    },
    {
        "question": "Izvēlies pareizas īpašības par objektiem:",
        "type": "checkbox",
        "options": ["Objektiem ir stāvoklis", "Objektiem ir uzvedība", "Objekti = klases", "Objektus nevar mainīt"],
        "correct": ["Objektiem ir stāvoklis", "Objektiem ir uzvedība"],
        "explanation": "Objektiem ir stāvoklis (atribūti) un uzvedība (metodes). Objekti nav klases un parasti var tikt mainīti."
    },
    {
        "question": "Ievadi terminu: attiecība starp objektiem un to īpašībām.",
        "type": "entry",
        "correct": "asociācija",
        "explanation": "Asociācija apraksta saikni starp objektiem (piem., viens objekts izmanto citu)."
    },
    {
        "question": "Abstraktā klase ir:",
        "type": "radio",
        "options": ["Klase, ko nevar instancēt", "Parasta klase", "Globāla klase"],
        "correct": "Klase, ko nevar instancēt",
        "explanation": "Abstraktā klase parasti satur abstraktas metodes un netiek tieši instancēta."
    },
    {
        "question": "Izvēlies abstrakcijas piemērus:",
        "type": "checkbox",
        "options": ["Interfeiss", "Abstraktā klase", "Privāts lauks", "Superklase"],
        "correct": ["Interfeiss", "Abstraktā klase"],
        "explanation": "Interfeiss un abstraktā klase nodrošina abstrakciju; privāts lauks nav abstrakcijas piemērs."
    },
    {
        "question": "Ievadi terminu: mehānisms, kas ļauj vienam metodam uzvesties dažādi — tas ir...",
        "type": "entry",
        "correct": "polimorfisms",
        "explanation": "Polimorfisms ļauj vienam interfeisam realizēt vairākas uzvedības."
    },
    {
        "question": "Kas ir superklase (klase no kuras manto)?",
        "type": "entry",
        "correct": "vecāku klase",
        "explanation": "Superklase ir vecāku klase (parent class), no kuras citas klases manto īpašības."
    },
    {
        "question": "Kā sauc metodi ar tādu pašu nosaukumu apakšklasē?",
        "type": "radio",
        "options": ["Pārslodze", "Pārrakstīšana", "Inicializācija"],
        "correct": "Pārrakstīšana",
        "explanation": "Pārrakstīšana (overriding) ir metodes definēšana apakšklasē ar tādu pašu nosaukumu kā superklasē."
    }
]


def ensure_questions_json():
    if not os.path.exists(QUESTIONS_JSON):
        try:
            with open(QUESTIONS_JSON, "w", encoding="utf-8") as f:
                json.dump(EMBEDDED_QUESTIONS, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print("Kļūda saglabājot questions.json:", e)

def load_questions_from_json(path=QUESTIONS_JSON):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OOP viktorīna — AI Quiz Generator (Latviešu)")
        self.root.geometry("700x520")
        self.root.resizable(False, False)

       
        self.style = ttk.Style()
        try:
            self.style.theme_use("clam")
        except:
            pass
        self.style.configure("TLabel", font=("Segoe UI", 11))
        self.style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"))
        self.style.configure("TButton", font=("Segoe UI", 10))
        self.style.configure("Question.TLabel", font=("Segoe UI", 12))

     
        ensure_questions_json()
        self.questions = load_questions_from_json()
        self.total_questions_in_quiz = 5

       
        self.selected_questions = []
        self.current_idx = 0
        self.user_answers = []
        self.start_time = None
        self.remaining_seconds = QUIZ_DURATION_SECONDS
        self.timer_id = None

       
        self.create_menu()
        self.create_start_screen()

 
    def create_menu(self):
        menubar = tk.Menu(self.root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Saglabāt rezultātu", command=self.manual_save_results)
        filemenu.add_command(label="Ielādēt jautājumus (JSON)", command=self.menu_load_questions)
        filemenu.add_separator()
        filemenu.add_command(label="Iziet", command=self.root.quit)
        menubar.add_cascade(label="Fails", menu=filemenu)
        self.root.config(menu=menubar)

   
    def create_start_screen(self):
        for w in self.root.winfo_children():
            w.destroy()

        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="OOP viktorīna", style="Header.TLabel").pack(pady=(10,5))
        ttk.Label(frame, text="Laiks: 5 minūtes. Tiks izvēlēti 5 nejauši jautājumi.", wraplength=640).pack(pady=5)

        start_btn = ttk.Button(frame, text="Sākt viktorīnu", command=self.start_quiz)
        start_btn.pack(pady=15)

        ttk.Label(frame, text="Opcijas", style="Header.TLabel").pack(pady=(20,5))
        opts = ttk.Frame(frame)
        opts.pack(pady=5)

        ttk.Label(opts, text="Kopā jautājumi pieejami: {}".format(len(self.questions))).grid(row=0, column=0, sticky="w")
        ttk.Label(opts, text="Jautājumu skaits viktorīnā: {}".format(self.total_questions_in_quiz)).grid(row=1, column=0, sticky="w")

        ttk.Label(frame, text="Rezultāti tiks saglabāti failā: {}".format(RESULTS_TXT), wraplength=640).pack(pady=(30,0))

    
    def start_quiz(self):
        # reset
        if len(self.questions) < self.total_questions_in_quiz:
            messagebox.showwarning("Brīdinājums", "Nedrīkst būt mazāk jautājumu par nepieciešamo.")
            return

        self.selected_questions = random.sample(self.questions, self.total_questions_in_quiz)
        self.current_idx = 0
        self.user_answers = [None] * self.total_questions_in_quiz
        self.start_time = datetime.now()
        self.remaining_seconds = QUIZ_DURATION_SECONDS

        self.show_question()
        self.update_timer()

   
    def update_timer(self):
        mins = self.remaining_seconds // 60
        secs = self.remaining_seconds % 60
        time_str = f"{mins:02d}:{secs:02d}"
        self.root.title(f"OOP viktorīna — Atlikušais laiks: {time_str}")

        if self.remaining_seconds <= 0:
            messagebox.showinfo("Laiks beidzies", "Laiks beidzies! Tiks rādīts rezultāts.")
            self.finish_quiz(timeout=True)
            return
        self.remaining_seconds -= 1
        self.timer_id = self.root.after(1000, self.update_timer)

 
    def show_question(self):
        for w in self.root.winfo_children():
            if isinstance(w, tk.Menu):
                continue
            w.destroy()

        q = self.selected_questions[self.current_idx]

        container = ttk.Frame(self.root, padding=12)
        container.pack(fill="both", expand=True)

        top = ttk.Frame(container)
        top.pack(fill="x")
        ttk.Label(top, text=f"Jautājums {self.current_idx+1}/{self.total_questions_in_quiz}", style="Header.TLabel").pack(side="left")
    
        mins = self.remaining_seconds // 60
        secs = self.remaining_seconds % 60
        ttk.Label(top, text=f"Atlikušais laiks: {mins:02d}:{secs:02d}").pack(side="right")

        ttk.Separator(container).pack(fill="x", pady=8)

        ttk.Label(container, text=q["question"], style="Question.TLabel", wraplength=660).pack(anchor="w", pady=(6,10))

        self.answer_vars = None

        if q["type"] == "checkbox":
            self.answer_vars = []
            for opt in q["options"]:
                var = tk.BooleanVar()
                chk = ttk.Checkbutton(container, text=opt, variable=var)
                chk.pack(anchor="w", padx=8, pady=2)
                self.answer_vars.append((var, opt))

        elif q["type"] == "radio":
            self.answer_vars = tk.StringVar()
            for opt in q["options"]:
                rb = ttk.Radiobutton(container, text=opt, variable=self.answer_vars, value=opt)
                rb.pack(anchor="w", padx=8, pady=2)

        elif q["type"] == "entry":
            self.answer_vars = tk.StringVar()
            entry = ttk.Entry(container, textvariable=self.answer_vars, width=40)
            entry.pack(anchor="w", padx=8, pady=6)

     
        btn_frame = ttk.Frame(container)
        btn_frame.pack(fill="x", pady=12)
        if self.current_idx > 0:
            ttk.Button(btn_frame, text="Iepriekšējais", command=self.prev_question).pack(side="left", padx=6)
        ttk.Button(btn_frame, text="Pārbaudīt atbildi", command=self.check_answer).pack(side="left", padx=6)
        ttk.Button(btn_frame, text="Tālāk", command=self.next_question).pack(side="right", padx=6)

    
        self.expl_label = ttk.Label(container, text="", wraplength=660)
        self.expl_label.pack(anchor="w", pady=(10,0))

   
    def check_answer(self):
        q = self.selected_questions[self.current_idx]
        user_ans = None

        if q["type"] == "checkbox":
            selected = [opt for var, opt in self.answer_vars if var.get()]
            user_ans = selected
        elif q["type"] == "radio":
            user_ans = self.answer_vars.get()
        elif q["type"] == "entry":
            user_ans = self.answer_vars.get().strip().lower()

      
        self.user_answers[self.current_idx] = user_ans

    
        correct = q["correct"]
        is_correct = False
        if q["type"] == "checkbox":
          
            is_correct = set([s for s in user_ans]) == set(correct)
        elif q["type"] == "entry":
           
            is_correct = str(user_ans).strip().lower() == str(correct).strip().lower()
        else:
            is_correct = str(user_ans).strip() == str(correct).strip()

      
        prefix = "Pareizi! " if is_correct else "Nepareizi. "
        explanation = q.get("explanation", "")
        self.expl_label.config(text=prefix + explanation)

  
    def next_question(self):
      
        if self.user_answers[self.current_idx] is None:
            q = self.selected_questions[self.current_idx]
            if q["type"] == "checkbox":
                selected = [opt for var, opt in self.answer_vars if var.get()]
                self.user_answers[self.current_idx] = selected
            elif q["type"] == "radio":
                self.user_answers[self.current_idx] = self.answer_vars.get()
            elif q["type"] == "entry":
                self.user_answers[self.current_idx] = self.answer_vars.get().strip().lower()

        if self.current_idx < self.total_questions_in_quiz - 1:
            self.current_idx += 1
            self.show_question()
        else:
            self.finish_quiz()

    def prev_question(self):
        if self.current_idx > 0:
            self.current_idx -= 1
            self.show_question()

   
    def finish_quiz(self, timeout=False):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

        
        for i, q in enumerate(self.selected_questions):
            if self.user_answers[i] is None:
                if i == self.current_idx:
                    if q["type"] == "checkbox":
                        self.user_answers[i] = [opt for var, opt in self.answer_vars if var.get()]
                    elif q["type"] == "radio":
                        self.user_answers[i] = self.answer_vars.get()
                    elif q["type"] == "entry":
                        self.user_answers[i] = self.answer_vars.get().strip().lower()
                else:
                    self.user_answers[i] = []

        
        score = 0
        details = []
        for ua, q in zip(self.user_answers, self.selected_questions):
            correct = q["correct"]
            correct_display = correct
            is_correct = False
            if q["type"] == "checkbox":
                is_correct = set(ua) == set(correct)
                correct_display = ", ".join(correct)
                user_display = ", ".join(ua) if ua else "(nav atbildes)"
            elif q["type"] == "entry":
                is_correct = str(ua).strip().lower() == str(correct).strip().lower()
                user_display = ua if ua else "(nav atbildes)"
            else:
                is_correct = str(ua).strip() == str(correct).strip()
                user_display = ua if ua else "(nav atbildes)"

            if is_correct:
                score += 1
            details.append({
                "question": q["question"],
                "user_answer": user_display,
                "correct_answer": correct_display,
                "is_correct": is_correct,
                "explanation": q.get("explanation", "")
            })

      
        summary = f"Jūsu rezultāts: {score}/{self.total_questions_in_quiz}"
        if timeout:
            summary += " (laiks beidzies)"
        messagebox.showinfo("Rezultāts", summary)

   
        try:
            self.save_results_to_txt(score, details)
            messagebox.showinfo("Saglabāts", f"Rezultāts saglabāts: {RESULTS_TXT}")
        except Exception as e:
            messagebox.showwarning("Kļūda", f"Neizdevās saglabāt rezultātu: {e}")

     
        self.create_start_screen()


    def save_results_to_txt(self, score, details):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(RESULTS_TXT, "a", encoding="utf-8") as f:
            f.write(f"--- Rezultāts: {now} ---\n")
            f.write(f"Score: {score}/{self.total_questions_in_quiz}\n")
            for i, d in enumerate(details, start=1):
                f.write(f"{i}. Jautājums: {d['question']}\n")
                f.write(f"   Jūsu atbilde: {d['user_answer']}\n")
                f.write(f"   Pareizā atbilde: {d['correct_answer']}\n")
                f.write(f"   Vai pareizi: {'Jā' if d['is_correct'] else 'Nē'}\n")
                f.write(f"   Paskaidrojums: {d['explanation']}\n")
            f.write("\n")

   
    def manual_save_results(self):
       
        save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if not save_path:
            return
      
        if os.path.exists(RESULTS_TXT):
            with open(RESULTS_TXT, "r", encoding="utf-8") as src, open(save_path, "w", encoding="utf-8") as dst:
                dst.write(src.read())
            messagebox.showinfo("Saglabāts", f"Rezultāti saglabāti: {save_path}")
        else:
            messagebox.showinfo("Nav datu", "Neuzrādīti iepriekšēji rezultāti, nav ko saglabāt.")

  
    def menu_load_questions(self):
        path = filedialog.askopenfilename(title="Izvēlies JSON ar jautājumiem", filetypes=[("JSON files", "*.json")])
        if not path:
            return
        try:
            loaded = load_questions_from_json(path)
           
            if not isinstance(loaded, list) or len(loaded) < self.total_questions_in_quiz:
                messagebox.showwarning("Kļūda", "JSON nav derīgs vai satur par maz jautājumu.")
                return
            self.questions = loaded
           
            with open(QUESTIONS_JSON, "w", encoding="utf-8") as f:
                json.dump(self.questions, f, ensure_ascii=False, indent=2)
            messagebox.showinfo("Ielādēts", f"Jautājumi ielādēti no: {path}")
            self.create_start_screen()
        except Exception as e:
            messagebox.showerror("Kļūda", f"Neizdevās ielādēt JSON: {e}")


def main():
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
