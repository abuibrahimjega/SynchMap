import pyttsx3

def init_engine():
    engine = pyttsx3.init()
    return engine

def say(text):
    engine = init_engine()
    
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1.0)
    print(f"Speaking at rate {engine.getProperty('rate')}")
    print(f"Volume is set to {engine.getProperty('volume')}")
    
    engine.say(text)
    
    engine.runAndWait()
    
    engine.stop()

if __name__ == "__main__":
    say("Hello World am not sure if you can recognise him, because the last time we met you were so young, just a child of 5 years old")
    print(say)
