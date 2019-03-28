import wx
from datetime import datetime


class MyFrame(wx.Frame):

    def __init__(self, symbol_options, time_options):
        wx.Frame.__init__(self, None, title="Cryptocurrency data downloader", size=(450, 220))
        self.symbol_options = symbol_options
        self.time_options = time_options

        input_panel = wx.Panel(self, style=wx.ALIGN_RIGHT)
        input_panel.SetBackgroundColour(wx.LIGHT_GREY)
        input_sizer = wx.BoxSizer(wx.VERTICAL)
        label_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # =================INPUT CONTROLS=======================
        self.crypto_combo = wx.ComboBox(input_panel, choices=self.symbol_options, style=wx.ALIGN_RIGHT)
        input_sizer.Add(self.crypto_combo, 0, wx.ALL | wx.ALIGN_RIGHT, 5)

        self.time_choice = wx.Choice(input_panel, choices=self.time_options, style=wx.ALIGN_RIGHT)
        input_sizer.Add(self.time_choice, 0, wx.ALL | wx.ALIGN_RIGHT, 5)

        self.quantity_entry = wx.TextCtrl(input_panel)
        input_sizer.Add(self.quantity_entry, 0, wx.ALL | wx.ALIGN_RIGHT, 5)

        self.filepath_entry = wx.TextCtrl(input_panel)
        input_sizer.Add(self.filepath_entry, 0, wx.ALL | wx.ALIGN_RIGHT, 5)

        self.prepare_data_cb = wx.CheckBox(input_panel, label="Prepare data for ML", pos=(160, 140))

        self.submit_button = wx.Button(input_panel, -1, "Submit", pos=(180, 170))
        self.submit_button.Bind(wx.EVT_BUTTON, self.on_submit)

        # =====================LABELS============================
        self.crypto_label = wx.StaticText(input_panel, label="Crypto symbol: ")
        label_sizer.Add(self.crypto_label, 0, wx.ALL, 8)

        self.time_label = wx.StaticText(input_panel, label="Time type: ")
        label_sizer.Add(self.time_label, 0, wx.ALL, 8)

        self.quantity_label = wx.StaticText(input_panel, label="How many records: ")
        label_sizer.Add(self.quantity_label, 0, wx.ALL, 8)

        self.filepath_label = wx.StaticText(input_panel, label="Path to save file: ")
        label_sizer.Add(self.filepath_label, 0, wx.ALL, 8)
        # ========================================================
        main_sizer.Add(label_sizer, -1, wx.ALIGN_LEFT)
        main_sizer.Add(input_sizer, -1, wx.ALIGN_RIGHT)

        input_panel.SetSizer(main_sizer)
        self.Show()

    def on_submit(self, event):
        import data_manager as dm  # if import is on top of file, app  window don't display

        time_type = self.time_choice.GetString(self.time_choice.GetCurrentSelection())
        symbol = self.crypto_combo.GetValue()
        quantity = int(self.quantity_entry.GetValue())
        path = self.filepath_entry.GetValue()

        data = dm.get_historical_data(time_type, symbol, limit=quantity)
        dm.create_plot(data, "plot.png", True)

        data_info = "Printed: " + str(datetime.now()) + " | time_type: " + time_type + " | cryptocurrency_symbol: " + \
                    symbol + " | records: " + str(quantity)

        dm.save_data_to_file(data, path, data_info)

        if self.prepare_data_cb.GetValue():
            from data_preparer import CryptoDataPreparer as dp

            dp.prepare_data_file_for_ML(path, False)


if __name__ == "__main__":
    options = ["BTC", "LTC", "ETH", "DOGE"]
    time_options = ["histoday", "histohour", "histominute"]
    app = wx.App(True)
    frame = MyFrame(options, time_options)
    app.MainLoop()

