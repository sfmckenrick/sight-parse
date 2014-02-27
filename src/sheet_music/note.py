# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

class Note:
    global value
    value = 'c'
    
    global octave
    octave = 4
    
    global duration
    duration = .25
    
    global dotted
    dotted = 1
    
    def to_string(self):
        print "Note value is: " + value + str(octave)
        
        toPrint = "Duration is: "
        
        if(duration == 1):
            toPrint += "whole"
        elif(duration == .5):
            toPrint += "half"
        elif(duration == .25):
            toPrint += "quarter"
        elif(duration == .125):
            toPrint += "eighth"
        elif(duration == .0625):
            toPrint += "sixteenth"
        elif(duration == .03125):
            toPrint += "thirty-second"
        else:
            toPrint += "undefined"
            
        if(dotted == 1):
            toPrint += " dotted"            
            
        print toPrint
        

n = Note()
n.to_string()


