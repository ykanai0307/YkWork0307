# ユーザエージェントコントローラ
class UserAgentClass:
    
    # コンストラクタ
    def __init__(self):
        self._agent = "";
        self._mobile = False;
        self._pc = False;
        pass;

    # agent select
    def MobileOrPc(self):
        try:
            if self._agent != "":
                if ( self._agent.find("Mobile") != -1 ):
                    self._mobile = True;
                else:
                    self._pc = True;
        except Exception as e:
            raise;
    
    # agent set
    def SetAgent(self, agent):
        self._agent = agent;
    # auth get
    def GetAgent(self):
        return self._agent;
        
    # moblie get
    def GetMoblie(self):
        return self._mobile;
    # pc get
    def GetPc(self):
        return self._pc;