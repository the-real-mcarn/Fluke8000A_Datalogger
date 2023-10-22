class F8000A_Display:
    def __init__(self, canvas):
        self.canvas = canvas
        self.canvas.configure(bg="#280000")
        self.canvas.update()
        
        self.digits()

        self.decimalPos = 0
        self.showPolarity = True

    def setPolarity(self, polarity):
        self.showPolarity = polarity

    def setDecimalPos(self, pos):
        self.decimalPos = pos
        
    def digits(self):
        # Draw the 'off' digits
        self.canvas.create_text(
            self.canvas.winfo_width() / 2,
            self.canvas.winfo_height() / 2,
            anchor="c",
            text="-8.8.8.8.",
            fill="#450000",
            font=("DSEG7 Classic-Regular", 48),
        )

    def update(self, data, polarity, overload):
        self.canvas.delete("all")

        if overload:
            result = "!0VER"
        else:
            # Remove first digit if it's zero
            if data[0] == 0:
                data[0] = "!"

            if self.decimalPos > 0:
                data.insert(self.decimalPos, ".")

            if self.showPolarity:
                if polarity == 1:
                    data = ["!"] + data
                else:
                    data = ["-"] + data
                
            result = ""
            for digit in data:
                result = result + str(digit)

        self.digits()

        # Draw the 'on' digits
        self.canvas.create_text(
            self.canvas.winfo_width() / 2,
            self.canvas.winfo_height() / 2,
            anchor="c",
            text=result,
            fill="Red",
            font=("DSEG7 Classic-Regular", 48),
        )
