from pymongo import MongoClient
from internal import load_gene
from internal import query_gene
# from internal import query_patient
# from internal import query_norder
import tkinter as tk

client = MongoClient()

class Interaction:

    def __init__(self, master):
        self.db = client.GeneInformation
        #collection: genes
        self.genes = self.db.genes
        self.master = master
        self.master.title("AD Knowledge Base")
        self.master.minsize(width=1024, height=750)
        self.master.maxsize(width=1024, height=750)
        self.master.tk_setPalette(background='#ffffff')

        #frame to hold all elements. destroy to clear screen
        self.container_frame = tk.Frame(self.master)
        self.container_frame.pack()

    def load(self):
        obj = load_gene.LoadGene()
        if obj.loaded == False:
            obj.load_files()

    #clears all elements off screen and repacks container screen
    def clear(self):
        self.container_frame.destroy()
        self.container_frame = tk.Frame(self.master)
        self.container_frame.pack()

    def open_menu(self):
        self.clear()
        menu = tk.Frame(self.container_frame)
        menu.pack()

        v = tk.IntVar()
        intro = """
        intro text
        """

        tk.Label(menu, text=intro).pack(pady=(253,0),anchor="center")
        tk.Radiobutton(menu, text="Given an entrez id, find all of its n-order interacting genes", variable=v, value=1).pack(anchor="w")
        tk.Radiobutton(menu, text="Given an entrez id, find mean and std of gene expression values for AD/MCI/NCI", variable=v, value=2).pack(anchor="w")
        tk.Radiobutton(menu, text="Given an entrez id, find all other information associated with this gene", variable=v, value=3).pack(anchor="w")
        tk.Radiobutton(menu, text="Given a patient id, find all patient information", variable=v, value=4).pack(anchor="w")
        tk.Radiobutton(menu, text="Advanced gene queries", variable=v, value=5).pack(anchor="w")
        tk.Button(menu, text="Submit", command=lambda: self.enter_info(v) ).pack()
        tk.Button(self.container_frame, text="Quit", command = self.end).pack

    def enter_info(self, op):
        self.clear()

        option = op.get()

        #entrez ID queries
        if option <=3:
            tk.Label(self.container_frame, text="Entrez ID: ").pack(pady=(253,0),anchor="w")
            e = tk.Entry(self.container_frame)
            e.pack()
            if option == 1:
                tk.Button(self.container_frame, text="Submit", command=lambda: self.get_norder(e.get()) ).pack()
            elif option == 2:
                tk.Button(self.container_frame, text="Submit", command=lambda: self.get_stats(e.get()) ).pack()
            elif option == 3:
                tk.Button(self.container_frame, text="Submit", command=lambda: self.get_all(e.get()) ).pack()

        #patient info query
        elif option == 4:
            tk.Label(self.container_frame, text="Patient ID: ").pack(pady=(253,0),anchor="w")
            e = tk.Entry(self.container_frame)
            e.pack()
            tk.Button(self.container_frame, text="Submit", command=lambda: self.get_patient(e.get()) ).pack()

        #advanced gene queries
        elif option == 5:
            tk.Button(self.container_frame, text="Submit", command= self.advanced).pack()

    def get_norder(self, entrez_id):
        self.clear()
        dummy = 0

    def get_stats(self, entrez_id):
        self.clear()

        stats = tk.Frame(self.container_frame)
        stats.pack()

        query_obj = query_gene.QueryGene()
        arr = query_obj.get_stats(entrez_id)

        if len(arr) == 0:
            tk.Label(stats, text="No matches found.").pack(pady=(253,0), anchor="w")
        else:
            tk.Label(stats, text = "Mean of NCI: {}".format(arr[0])).pack(pady=(253,0),anchor="w")
            tk.Label(stats, text = "STD of NCI: {}".format(arr[1])).pack(anchor="w")
            tk.Label(stats, text = "Mean of MCI: {}".format(arr[2])).pack(anchor="w")
            tk.Label(stats, text = "STD of MCI: {}".format(arr[3])).pack(anchor="w")
            tk.Label(stats, text = "Mean of AD: {}".format(arr[4])).pack(anchor="w")
            tk.Label(stats, text = "STD of AD: {}".format(arr[5])).pack(anchor="w")

        tk.Button(stats, text="Back to Menu", command = self.open_menu).pack()
        tk.Button(stats, text="Quit", command = self.end).pack()


    def get_all(self, entrez_id):
        self.clear()
        print(entrez_id)
        info = tk.Frame(self.container_frame)
        info.pack()

        query_obj = query_gene.QueryGene()
        genes = query_obj.get_all_information(entrez_id)

        if len(genes) == 0:
            tk.Label(info, text="No matches found.").pack(pady=(253,0), anchor="w")

        for doc in genes:
            tk.Label(info, text="{").pack(anchor="w")
            for key, value in doc.items():
                if key != "_id":
                    tk.Label(info, text="{} : {}".format(key, value)).pack(anchor="w")
            tk.Label(info, text="}").pack(anchor="w")
            tk.Label(info, text="").pack(anchor="w")

        tk.Button(self.container_frame, text="Back to Menu", command = self.open_menu).pack()
        tk.Button(self.container_frame, text="Quit", command = self.end).pack()

    def get_patient(self, entrez_id):
        self.clear()

        tk.Button(self.container_frame, text="Back to Menu", command = self.open_menu).pack()
        tk.Button(self.container_frame, text="Quit", command = self.end).pack()

    def advanced(self):
        self.clear()

        tk.Label(self.container_frame, text="Advanced Query Mode").pack(pady=(253,0),anchor="w")
        tk.Label(self.container_frame, text="Enter your query in mongoDB syntax to search information about genes.").pack(anchor="w")
        tk.Label(self.container_frame, text="Ex. find({\"gene_symbol\" : \"TNN\"})").pack(anchor="w")
        e = tk.Entry(self.container_frame, width = 52)
        e.pack()

        tk.Button(self.container_frame, text = "Submit", command = lambda: self.advanced_2(e.get())).pack()

        tk.Button(self.container_frame, text = "Back to Menu", command = self.open_menu).pack()

    def advanced_2(self, entry):
        
        
        if "drop" in entry:
            tk.Label(self.container_frame, text="Please don't delete anything from the database.").pack()

        else:
            self.clear()

            info = tk.Frame(self.container_frame)
            info.pack()

            entry = "self.genes." + entry
            genes = eval(entry)

            if len(genes) == 0:
                tk.Label(info, text="No matches found.").pack(pady=(253,0), anchor="w")

            for doc in genes:
                tk.Label(info, text="{").pack(anchor="w")
                for key, value in doc.items():
                    if key != "_id":
                        tk.Label(info, text="{} : {}".format(key, value)).pack(anchor="w")
                tk.Label(info, text="}").pack(anchor="w")
                tk.Label(info, text="").pack(anchor="w")

        tk.Button(self.container_frame, text="Back to Menu", command = self.open_menu).pack()
        tk.Button(self.container_frame, text="Quit", command = self.end).pack()

    def end(self):
        self.master.destroy()

def main():

    root = tk.Tk()

    obj = Interaction(root)

    obj.load()

    obj.open_menu()

    root.mainloop()


if __name__ == "__main__":
    main()