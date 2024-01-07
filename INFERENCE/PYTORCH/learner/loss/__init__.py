import torch
from .. import Lerner

class Loss(Lerner):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__start()

    def __start(self):
        pass

    def normp(self, p=1, tag=''):
        """Geometry loss"""
        loss, log = None, None
        return loss, log
    
    def nll(self, p, inverse=False, mean=False, eps=1e-5, tag=''):
        """negative_log_likelihood, 0<=p<=1"""
        if mean:
            p = p.mean()
        
        if inverse:
            p = 1 - p
        
        if p >= 0.5:
            if inverse:
                TN = 1
                TP, FP, FN = 0, 0, 0
            else:
                TP = 1
                TN, FP, FN = 0, 0, 0
        else:
            if inverse:
                FP = 1
                FN, TP, TN = 0, 0, 0
            else:
                FN = 1
                FP, TP, TN = 0, 0, 0

        p = self.Grad.safe(p, torch.clamp, min=eps)
        
        loss = -1 * p.log()
        log = {
            '{}/TP:reduction_ignore'.format(tag): TP,
            '{}/TN:reduction_ignore'.format(tag): TN,
            '{}/FP:reduction_ignore'.format(tag): FP,
            '{}/FN:reduction_ignore'.format(tag): FN,
            '{}/ACC:reduction_accuracy'.format(tag): None,
            '{}/loss'.format(tag): loss.clone().detach().mean().item(),
        }
        return loss, log