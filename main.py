from SUPERMARIO.source import tools,setup
from SUPERMARIO.source.state import main_menu as m
from SUPERMARIO.source.state import load_screen as lo
from SUPERMARIO.source.state import level as le
def main():
    state_dict = {'main_menu':m.Window(),'load_screen':lo.Load_screen(),'level':le.Level(),'game_over':lo.GameOver()}
    game = tools.Game('超级玛丽',state_dict,'main_menu')
    game.run()
if __name__ == '__main__':
    main()



#sprint冲刺shoot发射