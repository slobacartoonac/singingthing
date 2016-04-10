import wx

class MyFrame(wx.Frame):

    def __init__(self,parent,id,title='Settings Window'):
        wx.Frame.__init__(self, None, wx.ID_ANY)

        # Add a panel so it looks correct on all platforms
        self.panel = wx.Panel(self, wx.ID_ANY)

        bmp = wx.ArtProvider.GetBitmap(wx.ART_INFORMATION, wx.ART_OTHER, (16, 16))
        titleIco = wx.StaticBitmap(self.panel, wx.ID_ANY, bmp)
        title = wx.StaticText(self.panel, wx.ID_ANY, 'Settings Window')

        bmp = wx.ArtProvider.GetBitmap(wx.ART_TIP, wx.ART_OTHER, (16, 16))
        inputOneIco = wx.StaticBitmap(self.panel, wx.ID_ANY, bmp)
        labelOne = wx.StaticText(self.panel, wx.ID_ANY, 'Field of view x        ')
        self.inputTxtOne = wx.TextCtrl(self.panel, wx.ID_ANY, '')

        inputTwoIco = wx.StaticBitmap(self.panel, wx.ID_ANY, bmp)
        labelTwo = wx.StaticText(self.panel, wx.ID_ANY, 'Field of view y        ')
        self.inputTxtTwo = wx.TextCtrl(self.panel, wx.ID_ANY,'')

        inputThreeIco = wx.StaticBitmap(self.panel, wx.ID_ANY, bmp)
        labelThree = wx.StaticText(self.panel, wx.ID_ANY, 'Height of camera   ')
        self.inputTxtThree = wx.TextCtrl(self.panel, wx.ID_ANY, '')

        inputFourIco = wx.StaticBitmap(self.panel, wx.ID_ANY, bmp)
        labelFour = wx.StaticText(self.panel, wx.ID_ANY, 'Distance of camera')
        self.inputTxtFour = wx.TextCtrl(self.panel, wx.ID_ANY, '')

        saveBtn = wx.Button(self.panel, wx.ID_ANY, 'Save')
        cancelBtn = wx.Button(self.panel, wx.ID_ANY, 'Cancel')
        self.Bind(wx.EVT_BUTTON, self.onSave, saveBtn)
        self.Bind(wx.EVT_BUTTON, self.onCancel, cancelBtn)

        topSizer        = wx.BoxSizer(wx.VERTICAL)
        titleSizer      = wx.BoxSizer(wx.HORIZONTAL)
        inputOneSizer   = wx.BoxSizer(wx.HORIZONTAL)
        inputTwoSizer   = wx.BoxSizer(wx.HORIZONTAL)
        inputThreeSizer = wx.BoxSizer(wx.HORIZONTAL)
        inputFourSizer  = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer        = wx.BoxSizer(wx.HORIZONTAL)

        titleSizer.Add(titleIco, 0, wx.ALL, 5)
        titleSizer.Add(title, 0, wx.ALL, 5)

        inputOneSizer.Add(inputOneIco, 0, wx.ALL, 5)
        inputOneSizer.Add(labelOne, 0, wx.ALL, 5)

        inputOneSizer.Add(self.inputTxtOne, 1, wx.ALL|wx.EXPAND, 5)

        inputTwoSizer.Add(inputTwoIco, 0, wx.ALL, 5)
        inputTwoSizer.Add(labelTwo, 0, wx.ALL, 5)
        inputTwoSizer.Add(self.inputTxtTwo, 1, wx.ALL|wx.EXPAND, 5)

        inputThreeSizer.Add(inputThreeIco, 0, wx.ALL, 5)
        inputThreeSizer.Add(labelThree, 0, wx.ALL, 5)
        inputThreeSizer.Add(self.inputTxtThree, 1, wx.ALL|wx.EXPAND, 5)

        inputFourSizer.Add(inputFourIco, 0, wx.ALL, 5)
        inputFourSizer.Add(labelFour, 0, wx.ALL, 5)
        inputFourSizer.Add(self.inputTxtFour, 1, wx.ALL|wx.EXPAND, 5)

        btnSizer.Add(saveBtn, 0, wx.ALL, 5)
        btnSizer.Add(cancelBtn, 0, wx.ALL, 5)

        topSizer.Add(titleSizer, 0, wx.CENTER)
        topSizer.Add(wx.StaticLine(self.panel,), 0, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(inputOneSizer, 0, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(inputTwoSizer, 0, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(inputThreeSizer, 0, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(inputFourSizer, 0, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(wx.StaticLine(self.panel), 0, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(btnSizer, 0, wx.ALL|wx.CENTER, 5)

        self.panel.SetSizer(topSizer)
        topSizer.Fit(self)
        try:
                f=open("settings.txt")
                print 'file opened'
                var=f.readlines()
                print 'lines read'
                self.inputTxtOne.SetValue(var[0][:-1])
                print 'var added'
                self.inputTxtTwo.SetValue(var[1][:-1])
                self.inputTxtThree.SetValue(var[2][:-1])
                self.inputTxtFour.SetValue(var[3][:-1])
                print 'close'
                f.close()
        except:
                print 'Problem opening file.'
                self.inputTxtOne.SetValue('0')
                self.inputTxtTwo.SetValue('0')
                self.inputTxtThree.SetValue('0')
                self.inputTxtFour.SetValue('0')

    def onSave(self, event):
        try:
            f = open("settings.txt")
            var = f.readlines()
            f.close()
            var[0]=self.inputTxtOne.GetValue()+'\n'
            var[1]=self.inputTxtTwo.GetValue()+'\n'
            var[2]=self.inputTxtThree.GetValue()+'\n'
            var[3]=self.inputTxtFour.GetValue()+'\n'
            f = open("settings.txt", "w")
            f.writelines(var)
        except:
            f = open("settings.txt", "w")
            f.write(self.inputTxtOne.GetValue()+'\n'+self.inputTxtTwo.GetValue()
                    +'\n'+self.inputTxtThree.GetValue()+'\n'+self.inputTxtFour.GetValue()+'\n')
            
            f.close()
            x=float(self.inputTxtOne.GetValue())*math.pi/180
            y=float(self.inputTxtTwo.GetValue())*math.pi/180
            hc=float(self.inputTxtThree.GetValue())
            dc=float(self.inputTxtFour.GetValue())
        
            
            print 'close ', x, y, hc, dc
            f.close()      
        self.Destroy()

    def onOK(self, event):
        # Do something
        print 'onOK handler'

    def onCancel(self, event):
        self.closeProgram()

    def closeProgram(self):
        self.Close()
        
def settingsWindow():
    app = wx.App()
    frame = MyFrame(None, -1, 'Settings Window')
    frame.Show()
    
    app.MainLoop()

# Run the program
if __name__ == '__main__':
    
    app = wx.App()
    frame = MyFrame(None, -1, 'Settings Window')
    frame.Show()
    
    app.MainLoop()
