from typing import Any
from pytorch_lightning.utilities.types import STEP_OUTPUT, OptimizerLRScheduler
from . import Module
import pytorch_lightning as pl

class Module(Module, pl.LightningModule):
    """pytorch lightning module"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__start()

    def __start(self):
        pass

    def training_step(self, *args: Any, **kwargs: Any) -> STEP_OUTPUT:
        return super().training_step(*args, **kwargs)
    
    def validation_step(self, *args: Any, **kwargs: Any) -> STEP_OUTPUT:
        return super().validation_step(*args, **kwargs)
    
    def test_step(self, *args: Any, **kwargs: Any) -> STEP_OUTPUT:
        return super().test_step(*args, **kwargs)
    
    def forward(self, *args: Any, **kwargs: Any) -> Any:
        return super().forward(*args, **kwargs)
    
    def on_train_epoch_end(self) -> None:
        return super().on_train_epoch_end()
    
    def on_validation_end(self) -> None:
        return super().on_validation_end()
    
    def on_test_epoch_end(self) -> None:
        return super().on_test_epoch_end()
    
    def configure_optimizers(self) -> OptimizerLRScheduler:
        return super().configure_optimizers()