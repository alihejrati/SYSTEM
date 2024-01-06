import cv2
import multiprocessing as mp
from .basic import load, save, imshow
from KERNEL.SCRIPT.python.classes.basic import PYBASE 

class CallBack(PYBASE):
	CallbackEvents = dict(
		setMouseCallback = [
			'EVENT_LBUTTONDOWN', 
			'EVENT_RBUTTONDOWN'
		],
	)

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.__start()
	
	def __start(self):
		self.state = mp.Manager().list() # proxy list can be accessed across multi proccess.
		self.radius, self.color, self.thickness = 5, (0, 255, 255), 2

	def setMouseCallback(self, event, x, y, flags, params): 
		for event_name in self.__class__.CallbackEvents['setMouseCallback']:
			if event == getattr(cv2, event_name):
				cb = getattr(self, f'CB_{event_name}', None)
				if cb != None:
					cb(event=event, x=x, y=y, flags=flags, params=params, event_name=event_name)

	def sethook(self, winname, handler, img):
		self.winname = winname
		self.handler = handler
		self.img = img
		for cbe_k in self.__class__.CallbackEvents:
			getattr(cv2, cbe_k)(self.winname, getattr(self, cbe_k))

	def winclose(self):
		assert self.winname != None and self.handler != None
		cv2.destroyWindow(self.winname)
		self.winname = None
		self.handler()
		self.handler = None

	def winupdate(self, center):
		"""manipulating img doesnt addect on real img in dip module"""
		cv2.circle(self.img, center, self.radius, self.color, thickness=self.thickness, lineType=8, shift=0)
		cv2.imshow(self.winname, self.img)

	def dip_state_handler(self, state): # NOTE: overwite this function in each child class.
		dip_state_dict = dict() # NOTE: compute this dictionary givven `state` input and variable names in `DIP subclass`. 
		return dip_state_dict
	
	def CB_EVENT_LBUTTONDOWN(self, **kwargs):
		pass
	
	def CB_EVENT_RBUTTONDOWN(self, **kwargs):
		pass

if __name__ == '__main__':
	class CB(CallBack):
		def CB_EVENT_LBUTTONDOWN(self, **kwargs):
			print('left click', kwargs['x'], kwargs['y'])
	
		def CB_EVENT_RBUTTONDOWN(self, **kwargs):
			print('right click', kwargs['x'], kwargs['y'])
	# TEST 0
	imshow(load('*lena.jpg'), callback=CB()) # close image with press any key, while displayer is in focus.
	imshow(load('*lena.jpg', 'gray'), callback=CB()) # BUG: signal pause in imshow function.