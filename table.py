from tkinter import *
import tkinter.font as tkfont
from tkinter import filedialog
import webbrowser, os, db


class Table(object):
    def __init__(self, measurements, canvas, table_contents):
        self.rows = measurements["rows"]
        self.cols = measurements["columns"]
        self.cell_height = measurements["cell_height"]
        self.cell_width = measurements["cell_width"]
        self.canvas = canvas
        self.contents = table_contents
        self.header_font = tkfont.Font(family='Open Sans', weight='bold', size=13)
        self.data_font = tkfont.Font(family='Open Sans', size=10)
        self.images = []
        self.selectedCheckbox = []
        self.selectedRadio = ""

    def setScrollbars(self, frame):
        self.vertical_scroll = Scrollbar(frame, orient=VERTICAL)
        self.vertical_scroll.pack(side=RIGHT, fill=Y)
        self.vertical_scroll.config(command=self.canvas.yview)
        self.horizontal_scroll = Scrollbar(frame, orient=HORIZONTAL)
        self.horizontal_scroll.pack(side=BOTTOM, fill=X)
        self.horizontal_scroll.config(command=self.canvas.xview)

        self.canvas.configure(xscrollcommand=self.horizontal_scroll.set, yscrollcommand=self.vertical_scroll.set)
        self.canvas.pack(expand=True, side=LEFT, fill=BOTH)

    def createTable(self):
        self.images = []
        col_image = -1

        for row in range(self.rows):
            y = row * self.cell_height
            for column in range(self.cols):
                x = column * self.cell_width
                self.canvas.create_rectangle(x, y, x + self.cell_width, y + self.cell_height, fill="#EAEAEA")

                x_text = x + (self.cell_width / 2)
                y_text = y + (self.cell_height / 2)

                if row == 0:
                    self.canvas.create_text((x_text, y_text), text=self.contents[row][column], font=self.header_font)
                    if str(self.contents[row][column]) == "Photo":
                        col_image = column
                else:
                    if column == col_image:
                        self.images.append(self.contents[row][column])
                        self.canvas.create_image(x + 50, y + 13, image=self.contents[row][column], anchor=NW)
                    else:
                        self.canvas.create_text((x_text, y_text), text=self.contents[row][column], font=self.data_font)

    def optionsTable(self, num, option):
        self.images = []
        self.checkboxes = {}
        col_image = -1

        for row in range(self.rows):
            y = row * self.cell_height
            for column in range(self.cols):
                x = column * self.cell_width
                self.canvas.create_rectangle(x, y, x + self.cell_width, y + self.cell_height, fill="#EAEAEA")

                x_text = x + (self.cell_width / 2)
                y_text = y + (self.cell_height / 2)

                if row == 0:
                    self.canvas.create_text((x_text, y_text), text=self.contents[row][column], font=self.header_font)
                    if str(self.contents[row][column]) == "Photo":
                        col_image = column
                else:
                    if column == col_image:
                        self.images.append(self.contents[row][column])
                        self.canvas.create_image(x + 50, y + 13, image=self.contents[row][column], anchor=NW)
                    elif column == 0:
                        if option == "checkbox":
                            self.canvas.create_rectangle(x_text - 9, y_text - 9, x_text + 9, y_text + 9, fill="#191919")
                            self.checkboxes[row] = self.canvas.create_rectangle(x_text - 8, y_text - 8, x_text + 8, y_text + 8, fill="#E8E8E8")
                            self.canvas.tag_bind(self.checkboxes[row], "<Button-1>", lambda e: self.optionClicked(num,option))

                            if self.contents[row][0] in self.selectedCheckbox:
                                self.canvas.itemconfig(self.checkboxes[row], fill="#666666")
                        elif option == "radio":
                            self.canvas.create_oval(x_text - 9, y_text - 9, x_text + 9, y_text + 9, fill="#191919")
                            self.checkboxes[row] = self.canvas.create_oval(x_text - 8, y_text - 8, x_text + 8, y_text + 8, fill="#E8E8E8")
                            self.canvas.tag_bind(self.checkboxes[row], "<Button-1>", lambda e: self.optionClicked(num, option))

                            if self.contents[row][0] == self.selectedRadio:
                                self.canvas.itemconfig(self.checkboxes[row], fill="#666666")
                    else:
                        self.canvas.create_text((x_text, y_text), text=self.contents[row][column], font=self.data_font)

    def optionClicked(self, num, option):
        curr_clicked = self.canvas.find_withtag("current")[0] - num
        curr_clicked /= (num - 2)
        curr_clicked = int(curr_clicked)

        try:
            if option == "checkbox":
                if self.contents[int(curr_clicked + 1)][0] in self.selectedCheckbox:
                    self.canvas.itemconfig(self.checkboxes[int(curr_clicked + 1)], fill="#E8E8E8")
                    self.selectedCheckbox.remove(self.contents[int(curr_clicked + 1)][0])
                else:
                    self.canvas.itemconfig(self.checkboxes[int(curr_clicked + 1)], fill="#666666")
                    self.selectedCheckbox.append(self.contents[int(curr_clicked + 1)][0])
            else:
                for radio in range(len(self.checkboxes)):
                    self.canvas.itemconfig(self.checkboxes[int(radio + 1)], fill="#E8E8E8")

                if self.contents[int(curr_clicked + 1)][0] == self.selectedRadio:
                    self.selectedRadio = ""
                else:
                    self.canvas.itemconfig(self.checkboxes[int(curr_clicked + 1)], fill="#666666")
                    self.selectedRadio = self.contents[int(curr_clicked + 1)][0]
        except:
            pass

    def getSelectedCheckbox(self):
        return self.selectedCheckbox

    def getSelectedRadio(self):
        return self.selectedRadio


class ImportExport():
    def __init__(self):
        self.database = db.Database()
        self.import_operations = ""
        self.import_assets = ""

    def displayImport(self, import_bg, sub):
        self.choose_header = Label(import_bg, text="Choose Files to Import", bg="#DDDDDD", fg="#6A6A6A", font=sub)
        self.choose_header.place(relx=.5, rely=0.275, anchor="center")

        self.chosen_operations_header = Label(import_bg, text="No Operations File Chosen", width=25, bg="#EAEAEA", fg="#191919", font=sub)
        self.chosen_operations_header.place(relx=.5, rely=0.350, anchor="center")

        btn_font = tkfont.Font(family='Open Sans', weight="bold", size=13)
        self.choose_ops_btn = Button(import_bg, text="Choose File", width=15, command=lambda: self.uploadOperationsFile(),
                                     bg="#667275", fg="#FFFFFF", bd=0, font=btn_font)
        self.choose_ops_btn.place(relx=.5, rely=0.425, anchor="center")

        self.chosen_assets_header = Label(import_bg, text="No Assets File Chosen", width=25, bg="#EAEAEA", fg="#191919", font=sub)
        self.chosen_assets_header.place(relx=.5, rely=0.560, anchor="center")

        btn_font = tkfont.Font(family='Open Sans', weight="bold", size=13)
        self.choose_asset_btn = Button(import_bg, text="Choose File", width=15, command=lambda: self.uploadAssetsFile(),
                                     bg="#667275", fg="#FFFFFF", bd=0, font=btn_font)
        self.choose_asset_btn.place(relx=.5, rely=0.635, anchor="center")

    def uploadOperationsFile(self):
        fileTypes = [('Excel Workbook', '*.xlsx'),
                     ('Excel 97-2003 Workbook', '*.xls')]
        self.import_operations = filedialog.askopenfilename(filetypes=fileTypes)
        if len(self.import_operations) > 0:
            display_name = self.import_operations.split('/')[len(self.import_operations.split('/')) - 1]
            self.chosen_operations_header.configure(text=display_name)

    def uploadAssetsFile(self):
        fileTypes = [('Excel Workbook', '*.xlsx'),
                     ('Excel 97-2003 Workbook', '*.xls')]
        self.import_assets = filedialog.askopenfilename(filetypes=fileTypes)
        if len(self.import_assets) > 0:
            display_name = self.import_assets.split('/')[len(self.import_assets.split('/')) - 1]
            self.chosen_assets_header.configure(text=display_name)

    def importFile(self, username):
        if len(self.import_operations) > 0 and len(self.import_assets) > 0:
            try:
                self.database.importToExcel(self.import_assets, self.import_operations, username)
                return True
            except:
                return False
        return False

    def exportFile(self):
        self.database.exportToExcel()
        return True

    def openExport(self):
        webbrowser.open(os.getcwd())
