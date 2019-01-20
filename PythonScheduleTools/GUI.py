import tkinter

#from tkinter import filedialog
import CheckStatusByFiles
import CheckStatusByLog
import FileLogger
PFFILE = '/Users/MicaFunston/Downloads/Printflow-ToDo.xls'

class ScheduleToolsGUI(tkinter.Frame):
    """Gui class for checking Files In and Proof Out"""

    def __init__(self, ROOT):

        tkinter.Frame.__init__(self, ROOT)

        # options for buttons
        button_opt = {'fill': tkinter.constants.BOTH, 'padx': 10, 'pady': 10}

        # define GUI
        tkinter.Button(self, text='Check Files In', command=self.check_files_in).pack(**button_opt)
        tkinter.Button(
            self,
            text='Check Proofs Out',
            command=self.check_proofs_out).pack(**button_opt)
        tkinter.Button(self, text='Check Proofs In', command=self.check_proofs_in).pack(**button_opt)
        self.results_box = tkinter.Text(self)
        self.results_box.insert(tkinter.END, "Results will go here")
        #self.results_box.config(state="disabled")
        self.results_box.pack(fill="both", expand=1)

        # define options for opening or saving a file
        self.file_opt = options = {}
        options['defaultextension'] = '.txt'
        options['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
        options['initialdir'] = 'C:\\'
        options['initialfile'] = 'myfile.txt'
        options['parent'] = ROOT
        options['title'] = 'This is a title'

        # This is only available on the Macintosh, and only when Navigation Services are installed.
        #options['message'] = 'message'

        # if you use the multiple file version of the module functions
        # this option is set automatically.
        #options['multiple'] = 1

        # defining options for opening a directory
        self.dir_opt = options = {}
        options['initialdir'] = 'C:\\'
        options['mustexist'] = False
        options['parent'] = ROOT
        options['title'] = 'This is a title'

    def check_files_in(self):
        """Display Files In jobs in text box"""
        files_in = list()
        files_in.clear()
        dockets_files = CheckStatusByFiles.check_status_by_files(
            PFFILE,
            2,
            3,
            'Files In',
            '/Volumes/Dockets',
            '/Production/Print')
        if dockets_files:
            for dockets_file in dockets_files:
                files_in.append(dockets_file)
        insite_files = CheckStatusByFiles.check_status_by_files(
            PFFILE,
            2,
            3,
            'Files In',
            '/Volumes/AraxiVolume_PRINERGYEPM_J/Jobs',
            '/System/SubPages')
        if insite_files != None:
            for insite_file in insite_files:
                files_in.append(insite_file)
        self.results_box.config(state="normal")
        self.results_box.delete(1.0, tkinter.END)
        for file_in in files_in:
            if file_in:
                self.results_box.insert(tkinter.END, file_in)
                self.results_box.insert(tkinter.END, '\n\n')
        self.results_box.config(state="disabled")

    def check_proofs_out(self):
        """Display Proofs Out jobs in text box"""
        proofs_out = list()
        proofs_out.clear()
        proofs_out = CheckStatusByLog.check_status_by_csv(
            PFFILE,
            2,
            3,
            'Proof Out',
            'ProofLog.csv')
        csr_proofs_out = CheckStatusByFiles.check_status_by_files(
            PFFILE,
            2,
            3,
            'Proof Out',
            '/Volumes/Dockets',
            '/Prepress/PDF Proof'
        )
        if csr_proofs_out:
            for csr_proof in csr_proofs_out:
                proofs_out.append(csr_proof)
        
        self.results_box.config(state="normal")
        self.results_box.delete(1.0, tkinter.END)
        #self.results_box.insert(tkinter.END, self.results_shaper(proofs_out, "proof out"))
        for proof in proofs_out:
            self.results_box.insert(tkinter.END, proof)
            self.results_box.insert(tkinter.END, '\n\n')
        self.results_box.config(state="disabled")
        #return list(set(shaped_results))

    def check_proofs_in(self):
        """Display Proofs In jobs in text box"""
        proofs_in = list()
        dollco = list()
        huntclub = list()
        proofs_in.clear
        FileLogger.folder_watcher("/Volumes/Prepress-2/Plates","/Users/MicaFunston/Downloads/dcplates.csv")

        dollco = CheckStatusByLog.check_status_by_csv(
            PFFILE,
            2,
            3,
            'Proof In',
            '/Users/MicaFunston/Downloads/dcplates.csv')
        huntclub = CheckStatusByLog.check_status_by_csv(
            PFFILE,
            2,
            3,
            'Proof In',
            '/Users/MicaFunston/Downloads/hcplates.csv')
        proofs_in = dollco + huntclub
        self.results_box.config(state="normal")
        self.results_box.delete(1.0, tkinter.END)
        for plate in proofs_in:
            if plate:
                self.results_box.insert(tkinter.END, plate)
                self.results_box.insert(tkinter.END, '\n\n')
        self.results_box.config(state="disabled")

if __name__ == '__main__':
    ROOT = tkinter.Tk()
    ScheduleToolsGUI(ROOT).pack(fill="both", expand=1)
    ROOT.mainloop()
