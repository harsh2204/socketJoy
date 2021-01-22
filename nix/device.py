import logging
from abc import ABC, abstractmethod
from evdev import UInput, AbsInfo, ecodes as e


logger = logging.getLogger('socketJoy.Linux')


class Device(ABC):

	@abstractmethod
	def __init__(self, device, addr):
		self.device = device
		self.address = addr

	def close(self):
		self._ui.close()
		logger.debug(
			f'Destroyed virtual {self.type} device for {self.device} \
				at {self.address}')

	@abstractmethod
	def send(self, key, value):
		pass


class GamepadDevice(Device):

	capabilities = {
		e.EV_KEY: [
			e.BTN_Y,
			e.BTN_X,
			e.BTN_A,
			e.BTN_B,
			e.BTN_THUMBL,
			e.BTN_THUMBR,
			e.BTN_SELECT,
			e.BTN_START,
			e.BTN_MODE,
			e.BTN_TRIGGER_HAPPY1,
			e.BTN_TRIGGER_HAPPY2,
			e.BTN_TRIGGER_HAPPY3,
			e.BTN_TRIGGER_HAPPY4,
			e.BTN_TL,
			e.BTN_TR,
		],
		e.EV_ABS: [
			(e.ABS_X, AbsInfo(value=0, min=0, max=255, fuzz=0, flat=0, resolution=0)),
			(e.ABS_Y, AbsInfo(value=0, min=0, max=255, fuzz=0, flat=0, resolution=0)),
			(e.ABS_Z, AbsInfo(value=0, min=0, max=511, fuzz=0, flat=0, resolution=0)), # Left Trigger
			(e.ABS_RZ, AbsInfo(value=0, min=0, max=511, fuzz=0, flat=0, resolution=0)), # Right Trigger
			(e.ABS_RX, AbsInfo(value=0, min=0, max=255, fuzz=0, flat=0, resolution=0)),
			(e.ABS_RY, AbsInfo(value=0, min=0, max=255, fuzz=0, flat=0, resolution=0)),
			(e.ABS_HAT0X, AbsInfo(value=0, min=-1, max=1, fuzz=0, flat=0, resolution=0)), # DPAD X
			(e.ABS_HAT0Y, AbsInfo(value=0, min=-1, max=1, fuzz=0, flat=0, resolution=0)), # DPAD Y
		],
	}
	buttons = {
		'main-button': e.BTN_MODE,
		'back-button': e.BTN_SELECT,
		'start-button': e.BTN_START,
		'left-stick-press': e.BTN_THUMBL,
		'right-stick-press': e.BTN_THUMBR,
		'left-bumper': e.BTN_TL,
		'right-bumper': e.BTN_TR,
		'y-button': e.BTN_Y,
		'x-button': e.BTN_X,
		'a-button': e.BTN_A,
		'b-button': e.BTN_B,
	}
	axes = {
		'left-stick-X': e.ABS_X,
		'left-stick-Y': e.ABS_Y,
		'right-stick-X': e.ABS_RX,
		'right-stick-Y': e.ABS_RY,
		'left-trigger': e.ABS_Z,
		'right-trigger': e.ABS_RZ,
	}
	dpad = {
		'up-button': e.ABS_HAT0Y,
		'right-button': e.ABS_HAT0X,
		'down-button': e.ABS_HAT0Y,
		'left-button': e.ABS_HAT0X,
	}

	def __init__(self, device, addr):
		super().__init__(device, addr)
		self.type = "sockectJoy Gamepad"
		self._ui = UInput(
			events=self.capabilities,
			name=self.type,
			vendor=0x045e, 
			product=0x2020, # 0x2020 is a random product id
			version=0x0110,
			bustype=e.BUS_USB,
		)

	def send(self, key, value):
		if key in self.buttons:
			logger.debug(f'Sending button event::{e.keys[self.buttons[key]]}: {value}')
			self._ui.write(e.EV_KEY, self.buttons[key], value)
			self._ui.syn()
		elif key in self.dpad:
			if key in {'up-button', 'left-button'}:
				value = -1 if value else 0
			else:
				value = 1 if value else 0
			logger.debug(f'Sending axis event::{e.ABS[self.dpad[key]]}: {value}')
			self._ui.write(e.EV_ABS, self.dpad[key], value)
			self._ui.syn()
                        
		elif 'trigger' in key:
			coord = round(value * 511)
			logger.debug(f'Sending axis event::{e.ABS[self.axes[key]]}: {coord}')
			self._ui.write(e.EV_ABS, self.axes[key], coord)
			self._ui.syn()
		elif key in self.axes:
			coord = round(127 * value) + 127
			logger.debug(f'Sending axis event::{e.ABS[self.axes[key]]}: {coord}')
			self._ui.write(e.EV_ABS, self.axes[key], coord)
			self._ui.syn()
