#-------------------------------------------------------------------------------
# Name:        Python Cards System
# Purpose:     Making things look cool and visualize data with tkinter GUI
# Github:      https://github.com/STocidlowski/tkinterCards
#
# Author:      Shawn
#
# Created:     8/3/22
# Copyright:   (c) Shawn 2022
# Licence:     Unlicence
#-------------------------------------------------------------------------------

from tkinter import *

class TKCardDeck(Canvas):
    """Create a "Card" type visualizaion of objeccts. Right now starting text based only. WIP"""
    Cards = []

    def __init__(self, *args, bg = "Blue", fg = "SteelBlue3" , height = 600, width=400, CardSpacing = 10, **kwargs):

        def _on_mousewheel(event):
           self.yview_scroll(int(-1*(event.delta/120)), "units")                   # https://gist.github.com/JackTheEngineer/81df334f3dcff09fd19e4169dd560c59
        def _bind_to_mousewheel(event):
            self.bind_all("<MouseWheel>", _on_mousewheel)
        def _unbind_from_mousewheel(event):
            self.unbind_all("<MouseWheel>")

        kwargs['bg'] = bg
        self.CardColor = fg
        self.CardSpacing = CardSpacing

        kwargs['width'] = width
        kwargs['height'] = height
        kwargs['scrollregion'] = kwargs.get('scrollregion') or (0, 0, width, height * 2)

        super().__init__(*args, **kwargs)

        # Scrolling when mouse over object
        self.bind('<Enter>', _bind_to_mousewheel)
        self.bind('<Leave>', _unbind_from_mousewheel)

        v = Scrollbar(root, orient=VERTICAL)
        v['command'] = self.yview
        v.grid(column=1, row=0, sticky=(N,S,E))
        self['yscrollcommand'] = v.set

    def GetCardColor(self):
        return self.CardColor

    def RemoveCard(self, CardObject):
        MoveDistance = (CardObject.CardCanvas.winfo_height() + self.CardSpacing) * -1
        print(MoveDistance)
        StartShifting = False
        for Card in self.Cards:
            if (Card == CardObject):
                StartShifting = True
            if (StartShifting):
                self.move(Card.CardCanvasID, 0, MoveDistance)

        CardObject.CardCanvas.destroy()
        self.Cards.remove(CardObject)
        print(f"Removed from list")
        #self.canvas.update()

    def AddCard(self, TitleString, BodyString):
        StartHeight = 10
        for card in self.Cards:
            card.CardCanvas.update()
            StartHeight += card.CardCanvas.winfo_height() + self.CardSpacing

        NewCard = self.PyCard(self, 10, StartHeight, TitleString, BodyString)
        self.Cards.append(NewCard)

    class PyCard:
        """Nested Inner Class of TKCardDeck"""
        title = ""
        bodytext = ""

        CardColor = ""
        DeckBackground = ""

        CardHeight = 100
        CardWidth = 0

        CharacterWidth = 25

        CardCanvas = object()

        TitleLabel = object()
        BodyLabel = object()

        BtnDelete = object()
        BtnOK = object()
        #def CardColor(self):
        #    return self.TKCardDeck().GetCardColor()
        ParentCanvas = object()
        def __init__(self, ParentCanvas, XPos, YPos, title, bodytext):

            self.title = title
            self.bodytext = bodytext
            self.ParentCanvas =  ParentCanvas

            #CardColor = self.CardColor()


            ParentCanvas.update()
            self.CardWidth = ParentCanvas.winfo_width() - 40
            self.DeckBackground = ParentCanvas["bg"]
            self.CardColor = ParentCanvas.GetCardColor()

            # Embed another widget in the main canvas
            self.CardCanvas = Canvas(ParentCanvas, height=self.CardHeight, width=self.CardWidth, bd=0, highlightthickness=0, bg=self.DeckBackground)
            self.CardCanvasID = ParentCanvas.create_window(XPos, YPos, anchor='nw', window=self.CardCanvas)

            #self.CardCanvasID = self.CardCanvas.index()

            # Rounded corners:
            CornerDiameter = 40

            NW_coord = 0, 0, CornerDiameter, CornerDiameter
            NE_coord = (self.CardWidth - CornerDiameter) , 0, self.CardWidth, CornerDiameter
            SW_coord = 0, (self.CardHeight - CornerDiameter), CornerDiameter, self.CardHeight
            SE_coord = (self.CardWidth - CornerDiameter), (self.CardHeight - CornerDiameter), self.CardWidth, self.CardHeight

            NW_arc = self.CardCanvas.create_arc(NW_coord, start=90, extent=90, fill=self.CardColor, outline="")
            NE_arc = self.CardCanvas.create_arc(NE_coord, start=0, extent=90, fill=self.CardColor, outline="")
            SW_arc = self.CardCanvas.create_arc(SW_coord, start=180, extent=90, fill=self.CardColor, outline="")
            SE_arc = self.CardCanvas.create_arc(SE_coord, start=270, extent=90, fill=self.CardColor, outline="")

            #Surrounding Bars
            N_coord = CornerDiameter/2, 0, (self.CardWidth - (CornerDiameter/2)), CornerDiameter/2
            S_coord = CornerDiameter/2, (self.CardHeight - (CornerDiameter * 0.5)), (self.CardWidth - (CornerDiameter * 0.5)), self.CardHeight
            W_coord = 0, CornerDiameter * 0.5, CornerDiameter * 0.5, self.CardHeight - (CornerDiameter * 0.5)
            E_coord = self.CardWidth - (CornerDiameter * 0.5), CornerDiameter * 0.5, self.CardWidth, self.CardHeight - (CornerDiameter * 0.5)
            Center_coord = CornerDiameter* 0.5, CornerDiameter * 0.5, self.CardWidth- (CornerDiameter * 0.5), self.CardHeight - (CornerDiameter * 0.5)

            N_Rect = self.CardCanvas.create_rectangle(N_coord, fill=self.CardColor, outline="")
            S_Rect = self.CardCanvas.create_rectangle(S_coord, fill=self.CardColor, outline="")
            W_Rect = self.CardCanvas.create_rectangle(W_coord, fill=self.CardColor, outline="")
            E_Rect = self.CardCanvas.create_rectangle(E_coord, fill=self.CardColor, outline="")
            Center_Rect = self.CardCanvas.create_rectangle(Center_coord, fill=self.CardColor, outline="")

            # Content:

            self.TitleLabel = Label(text=self.title,
                                    width=self.CharacterWidth,
                                    foreground="white",
                                    background="SteelBlue4"

                                    )
            self.CardCanvas.create_window(self.CardWidth * 0.5, 2, anchor='n', window=self.TitleLabel)

            self.BodyLabel = Label(text=self.bodytext,
                                    width=self.CharacterWidth,
                                    #foreground="white",
                                    background="SteelBlue3"

                                    )
            self.CardCanvas.create_window(self.CardWidth * 0.5, 22, anchor='n', window=self.BodyLabel)



            self.BtnOK =  Button(self.CardCanvas, bg="green", height=1, width=3, command=self.button_event)
            self.CardCanvas.create_window(self.CardWidth - 35, 15, anchor='nw', window=self.BtnOK)
            self.BtnDelete =  Button(self.CardCanvas,  bg="red", height=1, width=3, command=self.button_delete)
            self.CardCanvas.create_window(self.CardWidth - 35, 42, anchor='nw', window=self.BtnDelete)


        def button_event(self):
            print("Other button clicked")
            #self.ParentCanvas.move(self.CardCanvasID, 0, 50)

        def button_delete(self):
            TKCardDeck.RemoveCard(self.ParentCanvas, self)

class App:
    WIDTH = 780
    HEIGHT = 520
    CardDeck = object()

    def __init__(self, master):
        master.title("Python Tkinter Cards System")
        master.geometry(f"{App.WIDTH}x{App.HEIGHT}")

        frameLeft = Frame(master, width=self.WIDTH * 0.5, height=self.HEIGHT)
        frameRight = Frame(master, width=self.WIDTH * 0.5, height=self.HEIGHT)
        frameLeft.grid(row=0, column=0)
        frameRight.grid(row=0, column=1)

        self.CardDeck = TKCardDeck(frameRight, height=self.HEIGHT, width=(self.WIDTH * 0.5) - 10)
        self.CardDeck.pack()

        self.CardDeck.AddCard("title1", "bodytext1\n level2")
        self.CardDeck.AddCard("title2", "bodytext2\n level2")
        self.CardDeck.AddCard("title3", "bodytext3\n level2")
        self.CardDeck.AddCard("title4", "bodytext4\n level2")
        self.CardDeck.AddCard("title5", "bodytext5\n level2")

if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()
    #root.destroy()  #Finally called when event loop terminated
    print("fin")






