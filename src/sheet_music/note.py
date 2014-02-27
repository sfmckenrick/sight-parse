class Note:
    def __init__(self, value, octave, duration, dotted):
        self.value = value
        self.octave = octave
        self.duration = duration
        self.dotted = dotted
    
    def to_string(self):
        output = "Note value is: " + self.value + " [" + self.octave
        output += "] of duration: "

        if self.dotted:
            output += "dotted "

        duration_string = {
            1: 'whole',
            .5: 'half',
            .25: 'quarter',
            .125: 'eighth',
            .0625: 'sixteenth',
            .03125: 'thirty-second',
        }[self.duration]

        output += "undefined" if duration_string == None else duration_string
        output += "."

        return output

if __name__=="__main__":
    n = Note("C4", "A8", 1, True)
    print(n.to_string())