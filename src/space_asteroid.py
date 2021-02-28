from engine import Engine, TrainingEngine

def main():
    #engine = Engine(use_AIPlayer=False)
    engine = TrainingEngine()
    engine.run_loop()

main()