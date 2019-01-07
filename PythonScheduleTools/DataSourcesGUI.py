import json
import os
import tkinter as tk
import tkinter.messagebox as msg
from tkinter import filedialog


class DataSourcesGUI(tk.Tk):

    def __init__(self, data_sources=None):
        super().__init__()

        if not data_sources:
            self.data_sources = []
            self.data_sources_dic = {}
        else:
            self.data_sources = data_sources

        self.data_sources_canvas = tk.Canvas(self)

        self.data_sources_frame = tk.Frame(self.data_sources_canvas)
        self.entry_frame = tk.Frame(self)
        self.entry_frame.configure(height=10)
        self.chooser_frame = tk.Frame(self)
        self.chooser_frame.configure(height=10)

        self.scrollbar = tk.Scrollbar(
            self.data_sources_canvas,
            orient="vertical",
            command=self.data_sources_canvas.yview)

        self.data_sources_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.title = "Edit Data Sources"
        self.geometry("300x600")
        self.entries = []
        self.entries_dic = {}

        self.data_types = ['Excel File', 'CSV Log File',
                           'Files', 'Folder', 'File Name']

        def add_button_click(*args):
            self.add_data_source()

        def choice_callback(*args):
            for widget in self.entry_frame.winfo_children():
                widget.destroy()
            chosen = self.choice.get()
            options = self.get_choices()
            self.entries.clear()

            for i in range(len(options)):
                row = tk.Frame(self.entry_frame)
                lab = tk.Label(row, width=15, text=options[i], anchor='w')
                ent = tk.Entry(row)
                ent.delete(0, tk.END)
                #ent.insert(0, options[i-1])
                row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
                lab.pack(side=tk.LEFT)
                ent.pack(side=tk.RIGHT, expand=1, fill=tk.X)
                self.entries.append((options[i], ent))
                self.entries_dic[options[i]] = ent
            # print(self.entries_dic)

            self.add_button = tk.Button(
                self.entry_frame, text="ADD", command=add_button_click)
            self.add_button.pack(side=tk.BOTTOM)

        self.choice = tk.StringVar(self.entry_frame)
        self.choice.set('Excel File')
        self.choice.trace('w', choice_callback)
        choice_callback()

        self.data_source_create = tk.OptionMenu(
            self.chooser_frame, self.choice, *self.data_types)

        self.data_sources_canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas_frame = self.data_sources_canvas.create_window(
            (0, 0),
            window=self.data_sources_frame, anchor="n")
        self.data_source_create.pack(side=tk.BOTTOM, fill=tk.X)
        self.entry_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.chooser_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.data_source_create.focus_set()

        self.get_data_sources()

        # data_source1 = tk.Label(self.data_sources_frame,
        #                        text="--- Add Data Sources Here ---", bg="lightgrey",
        #                        fg="black", pady=10)
        #data_source1.bind("<Button-1>", self.remove_data_source)

        # self.data_sources.append(data_source1)

        # for data_source in self.data_sources:
        #    data_source.pack(side=tk.TOP, fill=tk.X)

        self.bind("<Return>", self.add_data_source)
        self.bind("<Configure>", self.on_frame_configure)
        self.bind_all("<MouseWheel>", self.mouse_scroll)
        self.bind_all("<Button-4>", self.mouse_scroll)
        self.bind_all("<Button-5>", self.mouse_scroll)
        self.data_sources_canvas.bind("<Configure>", self.data_sources_width)

        self.colour_schemes = [
            {"bg": "lightgrey", "fg": "black"},
            {"bg": "grey", "fg": "white"}]

    def get_choices(self):
        chosen = self.choice.get()
        if chosen == 'Excel File':
            options = ["Source Name", "Path", "Id Column", "Status Column", "Status"]
        elif chosen == 'CSV Log File':
            options = ["Source Name", "Path", "Id Column", "Status"]
        elif chosen == 'Files':
            options = ["Source Name", "Path", "Sub Path", "Status"]
        elif chosen == 'Folder':
            options = ["Source Name", "Path", "Sub Path", "Folder", "Status"]
        else:
            options = ['Source Name', 'Path', "Status"]
        return options

    def get_data_sources(self):
        if os.stat("DataSources.json").st_size != 0:
            with open('DataSources.json') as json_file:                
                data_sources = json.load(json_file)
                if data_sources:
                    self.data_sources_dic = data_sources
                    for data_source in self.data_sources_dic:
                        
                        data_source_text = data_source
                        new_data_source = tk.Label(
                            self.data_sources_frame,
                            text=data_source_text,
                            pady=10)
                        new_data_source.bind(
                            "<Button-1>", self.remove_data_source)
                        new_data_source.pack(side=tk.TOP, fill=tk.X)

    def add_data_source(self, event=None):
        data_source_text = self.data_source_create.grab_release()
        new_data_source_dic = {}
        new_data_source_dic['Data Type'] = self.choice.get()

        for entry in self.entries:
            new_data_source_dic[entry[0]] = entry[1].get()

        if new_data_source_dic:
            new_data_source = tk.Label(
                self.data_sources_frame, text=new_data_source_dic, pady=10)
            self.set_data_source_colour(
                len(self.data_sources), new_data_source)
            new_data_source.bind("<Button-1>", self.remove_data_source)
            new_data_source.pack(side=tk.TOP, fill=tk.X)

            source_name = new_data_source_dic['Source Name']
            del new_data_source_dic['Source Name']
            self.data_sources_dic[source_name] = new_data_source_dic

            DataSourcesGUI.saveToJSON(self.data_sources_dic)
            self.data_sources.append(new_data_source)

    @staticmethod
    def saveToJSON(sources):
        with open('DataSources.json', mode='w') as json_file:
            json.dump(sources, json_file)

    @staticmethod
    def firstTimeJSON():
        file = open('DataSources.json', mode='w')
        file.close()

    def remove_data_source(self, event):
        data_source = event.widget
        if msg.askyesno("Really Delete?", "Delete " + data_source.cget("text") + "?"):
            self.data_sources.remove(data_source.widget)
            data_source.widget.destroy()
            self.recolour_data_sources()

    def recolour_data_sources(self):
        for index, data_source in enumerate(self.data_sources):
            self.set_data_source_colour(index, data_source)

    def set_data_source_colour(self, position, data_source):
        _, data_source_style_choice = divmod(position, 2)
        my_scheme_choice = self.colour_schemes[data_source_style_choice]

        data_source.configure(bg=my_scheme_choice["bg"])
        data_source.configure(fg=my_scheme_choice["fg"])

    def on_frame_configure(self, event=None):
        self.data_sources_canvas.configure(
            scrollregion=self.data_sources_canvas.bbox("all"))

    def data_sources_width(self, event):
        canvas_width = event.width
        self.data_sources_canvas.itemconfig(
            self.canvas_frame, width=canvas_width)

    def mouse_scroll(self, event):
        if event.delta:
            self.data_sources_canvas.yview_scroll(
                int(-1 * (event.delta / 120)), "units")
        else:
            if event.num == 5:
                move = 1
            else:
                move = -1

            self.data_sources_canvas.yview_scroll(move, "units")


if __name__ == "__main__":
    if not os.path.isfile("DataSources.json"):
        DataSourcesGUI.firstTimeJSON()
    data_sources_gui = DataSourcesGUI()
    data_sources_gui.mainloop()
