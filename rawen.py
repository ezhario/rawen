"""Rawen is a simple app to remove unnecessary RAWs."""
import os
from pathlib import Path
import wx

class MyFrame(wx.Frame):
    """Main class with all the magic"""

    def __init__(self):
        super().__init__(parent=None, title='RAWEN')

        self.dcim_path = ''

        self.panel = wx.Panel(self)

        my_sizer = wx.BoxSizer(wx.VERTICAL)

        my_sizer.AddSpacer(10)

        open_btn = wx.Button(self.panel, label='Open SD Card Root', pos=(5, 55))
        open_btn.Bind(wx.EVT_BUTTON, self.on_open_folder)
        my_sizer.Add(open_btn, 0, wx.ALL | wx.CENTER, 5)

        self.result = wx.StaticText(self.panel, label="Please select a SD Card Root.",
                                    style=wx.ALIGN_CENTER| wx.ST_NO_AUTORESIZE)
        my_sizer.Add(self.result, 0, wx.ALL | wx.EXPAND, 5)

        self.do_btn = wx.Button(self.panel, label='Do it.', pos=(5, 55))
        self.do_btn.Bind(wx.EVT_BUTTON, self.delete_raws)
        my_sizer.Add(self.do_btn, 0, wx.ALL | wx.CENTER, 5)
        my_sizer.AddSpacer(10)
        font = wx.Font(10, family = wx.FONTFAMILY_MODERN,
                       style = 0, weight = 90, underline = False,
                       faceName ="", encoding = wx.FONTENCODING_DEFAULT)
        self.creds = wx.StaticText(self.panel, label="© ezhario, 2023. Inspired by ixtaccihuatl",
                                   style=wx.ALIGN_CENTER| wx.ST_NO_AUTORESIZE)
        self.creds.SetFont(font)
        my_sizer.Add(self.creds, 0, wx.ALL | wx.EXPAND, 5)
        self.do_btn.Disable()
        self.panel.SetSizer(my_sizer)
        self.create_menu()
        self.Centre()
        self.Show()

    def create_menu(self):
        """This function creates a menu bar with one item."""
        menu_bar = wx.MenuBar()
        file_menu = wx.Menu()
        open_folder_menu_item = file_menu.Append(
            wx.ID_ANY, 'Open SD Card',
            'Open a root of SD Card'
        )
        menu_bar.Append(file_menu, '&File')
        self.Bind(
            event=wx.EVT_MENU,
            handler=self.on_open_folder,
            source=open_folder_menu_item,
        )
        self.SetMenuBar(menu_bar)

    def count_files(self, folder_path):
        """Function for counting folders."""
        print(folder_path)
        path = folder_path + '/DCIM'
        if os.path.exists(path):
            self.result.SetLabel("Counting...")
            self.dcim_path = path
            jpg_pos = len(list(Path(path).rglob("*.[jJ][pP][gG]")))
            raw_pos = len(list(Path(path).rglob("*.[aA][rR][wW]")))
            label = f"JPGs: {jpg_pos}, RAWs: {raw_pos}"
            self.result.SetLabel(label)
            self.do_btn.Enable()
        else:
            self.result.SetLabel("That's not an SD Card: no DCIM folder on it's root.")


    def on_open_folder(self, event):
        """Dialog function."""
        print(event)
        title = "Choose a SD Card Root:"
        dlg = wx.DirDialog(self, title,
                           style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.count_files(dlg.GetPath())
        dlg.Destroy()

    def get_file_list(self, input_list):
        """This function forms the file list"""
        result_list = []
        for path in input_list:
            result_list.append(path.as_posix())
        return result_list

    def get_folder_list(self, input_list):
        """This function forms the folder list"""
        output_list = []
        list_of_paths = self.get_file_list(input_list)
        for path in list_of_paths:
            fpath = path.rsplit('/',1)[0]
            folder_name = fpath.rsplit('/',1)[1]
            if folder_name not in output_list:
                output_list.append(folder_name)
        return output_list

    def provide_folder_dict(self, jpg, raw):
        """This function provides folders as a dict"""
        folder_dict = {}
        for item in self.get_folder_list(jpg):
            folder_dict[item] = {}
            folder_dict[item]['jpg'] = {}
            jpg_lst = []
            for list_str in self.get_file_list(jpg):
                if item in list_str:
                    if not "/." in list_str:
                        jpg_lst.append(list_str)
            folder_dict[item]['jpg'] = jpg_lst
            raw_lst = []
            for list_str in self.get_file_list(raw):
                if item in list_str:
                    if not "/." in list_str:
                        raw_lst.append(list_str)
            folder_dict[item]['raw'] = raw_lst
        return folder_dict

    def form_deletion_list(self, folder_dict):
        """This funtion forms list of files to be deleted"""
        deletion_list = []
        for folder, item in folder_dict.items():
            print('### FOLDER ###')
            print(folder, item)
            print(type(folder), type(item))

            for raw_path in item['raw']:
                flag = False
                raw_file = raw_path[:-4].lower()
                print('### RAW FILE ###')
                print(raw_file)

                for jpg_path in item['jpg']:
                    jpg_file = jpg_path[:-4].lower()
                    print('raw: '+raw_file)
                    print('jpg: '+jpg_file)
                    if raw_file == jpg_file:
                        print('!!! MATCH, file survived !!!')
                        flag = True
                if not flag:
                    print('oh no, it goes to bin: '+raw_path)
                    deletion_list.append(raw_path)
        return deletion_list

    def delete_raws(self, event):
        """This function deletes the files"""
        print(event)
        self.result.SetLabel("Executing...")
        cwd = self.dcim_path
        jpg_pos = list(Path(cwd).rglob("*.[jJ][pP][gG]"))
        raw_pos = list(Path(cwd).rglob("*.[aA][rR][wW]"))

        folder_dict = self.provide_folder_dict(jpg_pos, raw_pos)

        deletion_list = self.form_deletion_list(folder_dict)
        errors = False
        for item in deletion_list:
            if os.path.isfile(item):
                os.remove(item)
            else:
                msg = f"Error: {item} file not found"
                print(msg)
                errors = True
        if errors:
            self.result.SetLabel("There were some errors. You can try again.")
            self.do_btn.Disable()
        else:
            self.result.SetLabel("Done.")
            self.do_btn.Disable()

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()
