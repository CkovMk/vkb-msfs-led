from .base import VENDOR_ID
from .gladiatork import GladiatorK, GladiatorKLH
from .gladiator_nxt_thq import Gladiator_NXT_THQ
from .nxt_sem_thq_fsmga import NXT_SEM_THQ_FSMGA

VKB_DEVICES = {
    0x0132: GladiatorK, 0x0133: GladiatorKLH,
    0x0200: Gladiator_NXT_THQ,
    0x2234: NXT_SEM_THQ_FSMGA,
}
