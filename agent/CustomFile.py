from maa.agent.agent_server import AgentServer
from agent.custom.action.Count import Count
from agent.custom.action.OverridePipe import OverridePipe
from agent.custom.action.IDFRole import RecognitionRole

from agent.custom.action.Notice import Notice
from agent.custom.action.LaunchGameExe import LaunchGameExe
from agent.custom.action.ElysiaDoorNavigator import ElysiaDoorNavigator
from agent.custom.action.ElysiaImprintSelector import ElysiaImprintSelector
from agent.custom.action.ElysiaWeeklyReductionSetup import ElysiaWeeklyReductionSetup

from agent.custom.action.Role.FieryWishingStar import FieryWishingStar
from agent.custom.action.Role.SpinaAstera import SpinaAstera
from agent.custom.action.Role.HerrscherOfTruth import HerrscherOfTruth
from agent.custom.action.Role.LoveElf import LoveElf
from agent.custom.action.Role.FengHuangOfVicissitude import FengHuangOfVicissitude
from agent.custom.action.Role.GeneralFight import GeneralFight
from agent.custom.action.Role.Meibiwusi import Meibiwusi
from agent.custom.action.Role.AstralRingFight import AstralRingFight


from agent.custom.recongition.CheckResolution import CheckResolution


@AgentServer.custom_action("Notice")
class Notice_Cls(Notice):
    def __init__(self):
        super().__init__()
        print(f"{self.__class__.__name__} 初始化")


@AgentServer.custom_action("LaunchGameExe")
class LaunchGameExe_Cls(LaunchGameExe):
    def __init__(self):
        super().__init__()
        print(f"{self.__class__.__name__} 初始化")


@AgentServer.custom_action("GeneralFight")
class GeneralFight_Cls(GeneralFight):
    def __init__(self):
        super().__init__()
        print(f"{self.__class__.__name__} 初始化")


@AgentServer.custom_action("IDFRole")
class IDFRole_Cls(RecognitionRole):
    def __init__(self):
        super().__init__()
        print(f"{self.__class__.__name__} 初始化")


@AgentServer.custom_action("Count")
class Count_Cls(Count):
    def __init__(self):
        super().__init__()
        print(f"{self.__class__.__name__} 初始化")


@AgentServer.custom_action("OverridePipe")
class OverridePipe_Cls(OverridePipe):
    def __init__(self):
        super().__init__()
        print(f"{self.__class__.__name__} 初始化")


@AgentServer.custom_recognition("CheckResolution")
class CheckResolution_Cls(CheckResolution):
    def __init__(self):
        super().__init__()
        print(f"{self.__class__.__name__} 初始化")


@AgentServer.custom_action("FieryWishingStar")
class FieryWishingStar_Cls(FieryWishingStar):
    def __init__(self):
        super().__init__()
        print(f"{self.__class__.__name__} 初始化")


@AgentServer.custom_action("SpinaAstera")
class SpinaAstera_Cls(SpinaAstera):
    def __init__(self):
        super().__init__()
        print(f"{self.__class__.__name__} 初始化")


@AgentServer.custom_action("HerrscherOfTruth")
class HerrscherOfTruth_Cls(HerrscherOfTruth):
    def __init__(self):
        super().__init__()
        print(f"{self.__class__.__name__} 初始化")


@AgentServer.custom_action("LoveElf")
class LoveElf_Cls(LoveElf):
    def __init__(self):
        super().__init__()
        print(f"{self.__class__.__name__} 初始化")


@AgentServer.custom_action("FengHuangOfVicissitude")
class FengHuangOfVicissitude_Cls(FengHuangOfVicissitude):
    def __init__(self):
        super().__init__()
        print(f"{self.__class__.__name__} 初始化")


@AgentServer.custom_action("Meibiwusi")
class Meibiwusi_Cls(Meibiwusi):
    def __init__(self):
        super().__init__()
        print(f"{self.__class__.__name__} 初始化")


@AgentServer.custom_action("AstralRingFight")
class AstralRingFight_Cls(AstralRingFight):
    def __init__(self):
        super().__init__()
        print(f"{self.__class__.__name__} 初始化")


@AgentServer.custom_action("ElysiaDoorNavigator")
class ElysiaDoorNavigator_Cls(ElysiaDoorNavigator):
    def __init__(self):
        super().__init__()
        print(f"{self.__class__.__name__} 初始化")


@AgentServer.custom_action("ElysiaImprintSelector")
class ElysiaImprintSelector_Cls(ElysiaImprintSelector):
    def __init__(self):
        super().__init__()
        print(f"{self.__class__.__name__} 初始化")


@AgentServer.custom_action("ElysiaWeeklyReductionSetup")
class ElysiaWeeklyReductionSetup_Cls(ElysiaWeeklyReductionSetup):
    def __init__(self):
        super().__init__()
        print(f"{self.__class__.__name__} 初始化")
