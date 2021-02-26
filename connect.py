from huskylib import HuskyLensLibrary
husky = HuskyLensLibrary("SERIAL", "/dev/ttyUSB0", 3000000)

class Object:
    def learn(self, id): #KeonWoo PARK; Learn Object(number) from Camera.
        return husky.learn(id)
    
    def getall(self): #KeonWoo PARK; Get all Object information from huskylens.
        return husky.requestAll()
    
    def get(self,id): #KeonWoo PARK; Get specific Object information
        return husky.getObjectByID(id)