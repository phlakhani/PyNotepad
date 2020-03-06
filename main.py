import tkinter as tk
#import sys
from tkinter import filedialog
from tkinter import messagebox


class Menubar:     # child class of Pytext class by class compositions
    def __init__(self,parent):
        font_specifications = ('Consolas', 11)

        menubar=tk.Menu(parent.notepad,font=('Calibri',12))   # font doesn't changing in menubar
        parent.notepad.configure(menu=menubar)

        dropdown_menu= tk.Menu(menubar,font=font_specifications,tearoff=0)
        about_dropdown= tk.Menu(menubar,font=font_specifications,tearoff=0)

        dropdown_menu.add_command(label='New file', accelerator="Ctrl+N", command=parent.new_file)
        dropdown_menu.add_command(label='Open file', accelerator="Ctrl+O", command=parent.open_file)
        dropdown_menu.add_command(label='Save', accelerator="Ctrl+S", command=parent.save)
        dropdown_menu.add_command(label='Save As', accelerator="Ctrl+Shift+S", command=parent.save_as)
        dropdown_menu.add_separator()
        dropdown_menu.add_command(label='Exit', command=parent.notepad.destroy)  #command=parent.exit_app

        about_dropdown.add_command(label='About',  command=parent.about_message)
        about_dropdown.add_separator()
        about_dropdown.add_command(label='Release Note', command=parent.releaseNote_message)

        menubar.add_cascade(label="File",menu=dropdown_menu)
        menubar.add_cascade(label="About", menu=about_dropdown)

class Statusbar:
    def __init__(self,parent):
        font_specification = ("calibri",12)
        self.status = tk.StringVar()
        self.status.set("PyNotepad - developed by Piyush Lakhani")

        label= tk.Label(parent.textarea, textvariable=self.status, fg="black", bg="lightgrey", anchor="sw", font=font_specification)
        label.pack(side=tk.BOTTOM, fill=tk.BOTH)

    def  update_statusbar(self,*args):   #to update status bar during new changes for that we use *args in new func, u understood well
        if isinstance(args[0],bool):    # if 1st arg===bool then update status bar bcoz we pass bool in particular fun save(),save_as()
            self.status.set("The file has been Saved")
        else:
            self.status.set("PyNotepad - developed by Piyush Lakhani")






class Pytext:
    def __init__(self,notepad):
        self.notepad=notepad
        self.notepad.title("untitle-PyNotepad")
        self.notepad.geometry("900x500")


        font_specifications=('Times New Roman',18)
        self.textarea =tk.Text(notepad,font=font_specifications)
        self.scrollbar=tk.Scrollbar(notepad,command=self.textarea.yview)
        self.textarea.configure(yscrollcommand=self.scrollbar.set)
        self.textarea.pack(side=tk.LEFT,fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.menubar=Menubar(self)    ## class Menubar is child of parent class Pytext
        self.statusbar=Statusbar(self)

        self.bind_shortcut() # it should be called in init method bcoz we want it to be active on starting of app
        self.filename=None

    def set_window_title(self, name=None):
        if name:
            self.notepad.title(name + " -PyNotepad")
        else:
            self.notepad.title("untitle-PyNotepad")
    def new_file(self, *args):   ## *args bcoz shortcut key function sending some argument
        self.textarea.delete(1.0, tk.END)
        self.filename = None
        self.set_window_title()
    def open_file(self, *args):
        self.filename=filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[("all files","*.*"),
                       ("text file", ".txt"),
                       ("python file", ".py"),
                       ("html file", ".html"),
                       ("css file", ".css"),
                       ("javascript file", ".js"),
                       ]

        )
        if self.filename:
            self.textarea.delete(1.0, tk.END)
            #print(self.filename)
            filetext=open(self.filename, "r")
            self.textarea.insert(1.0,filetext.read())
            self.set_window_title(self.filename)



    def save(self, *args):
        if self.filename:
            try:
                textarea_content=self.textarea.get(0.0, tk.END)
                file = open(self.filename, "w")
                file.write(textarea_content)
                self.statusbar.update_statusbar(True)  # update status bar after file is saved
            except Exception as e:
                print(e)
        else:
            self.save_as()


    def save_as(self, *args):
        try:
            new_file=filedialog.asksaveasfilename(
                initialfile="Untitle.txt",
                defaultextension=".txt",
                filetypes=[("all files", "*.*"),
                           ("text file", ".txt"),
                           ("python file", ".py"),
                           ("html file", ".html"),
                           ("css file", ".css"),
                           ("javascript file", ".js"),
                           ]

            )
            textarea_content=self.textarea.get(0.0, tk.END)
            file=open(new_file,"w")
            file.write(textarea_content)
            self.filename=new_file
            self.set_window_title(self.filename)
            self.statusbar.update_statusbar(True)  # update status bar after file is saved
        except Exception as e:
            print(e)

    def about_message(self):
        box_title="About-PyNotepad"
        box_msg="This Fully Functional PyNotepad is Developed by Piyush Lakhani" \
                "   For more Info. Contact: piyushlakhani.net@gmail.com"
        messagebox.showinfo(box_title, box_msg)
    def releaseNote_message(self):
        box_title="Release Note-PyNotepad"
        box_msg="Version 1.01 , Released: Jan,2020"
        messagebox.showinfo(box_title,box_msg)
    def bind_shortcut(self):
        self.textarea.bind('<Control-n>', self.new_file)
        self.textarea.bind('<Control-o>', self.open_file)
        self.textarea.bind('<Control-s>', self.save)
        self.textarea.bind('<Control-S>', self.save_as)
        self.textarea.bind('<Key>', self.statusbar.update_statusbar) #generic bind to get back original text to status bar when
                                                                     # any new key is pressed after saved file





if __name__=="__main__":
    app=tk.Tk()
    notepad=Pytext(app)
    app.mainloop()

