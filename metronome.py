import asyncio, dialogs, sound, time, ui
from bisect import  bisect_left

class MyMetronome(ui.View):
	def __init__(self):
		self.presets = [40,42,44,46,48,50,52,54,56,58,60,63,66,69,72,76,80,84,88,92,96,100,104,108,112,116,120,126,132,138,144,152,160,168,176,184,192,200,208]
		self.sli_bpm_min = self.presets[0]
		self.sli_bpm_max = self.presets[-1]
		
		self.bpm = 100.0
		self.delay = 60.0/self.bpm
		
		self.name = 'Metronome'
		self.background_color = 'white'
		
		self.sli = ui.Slider('Beats per Minute')
		self.sli.action = self.sli_action
		self.add_subview(self.sli)
		
		self.box = ui.Label()
		self.box.text = '{:d}'.format(int(self.bpm))
		
		self.add_subview(self.box)
		
		#self.seg = ui.SegmentedControl()
		#self.seg.segments = list( map(str,self.presets) )
		#self.add_subview(self.seg)
		
		sound_list = ['8ve:8ve-tap-crisp',
			'8ve:8ve-tap-percussive',
			'8ve:8ve-tap-simple']
		#self.sound_effect_file = dialogs.list_dialog(items=sound_list)
		self.sound_effect_file = sound_list[1]
		
		self.sli_set()
		
		#sound.set_volume(1.0)
		sound.set_honors_silent_switch(False)
		self.init_loop()
		
	@ui.in_background
	def init_loop(self):
		self.event_loop = asyncio.get_event_loop_policy().new_event_loop()
		self.event_loop.call_soon(self.click)
		self.event_loop.run_forever()
		
	def layout(self):
		self.box.font = ('<system-bold>',144)
		self.box.width = 300
		self.box.x = self.width / 2 - 150
		self.box.y = (self.height)/2 - 144
		self.box.height = 144
		self.box.alignment = ui.ALIGN_CENTER
		self.sli.width = self.width - 100
		self.sli.x = (self.width - self.sli.width)/2
		self.sli.y = self.box.y + 150
		#self.seg.width = self.width
		
	def will_close(self):
		sound.stop_all_effects()
		self.event_loop.stop()
		
	def closest_bpm(self, raw_bpm):
		pos = bisect_left(self.presets, raw_bpm)
		if pos == 0:
			return self.presets[0]
		if pos == len(self.presets):
			return self.presets[-1]
		before = self.presets[pos-1]
		after = self.presets[pos]
		if after - raw_bpm < raw_bpm - before:
			return after
		else:
			return before
		
	def sli_set(self):
		self.sli.value = (self.bpm-self.sli_bpm_min)/(self.sli_bpm_max-self.sli_bpm_min)
		
	def sli_action(self, sender):
		val = sender.value
		raw_bpm = (self.sli_bpm_max-self.sli_bpm_min)*val + self.sli_bpm_min
		self.bpm = float(self.closest_bpm(raw_bpm))
		self.delay = 60.0/self.bpm
		#print('{:f}'.format(self.bpm))
		#self.bpm = raw_bpm
		self.box.text = '{:d}'.format(int(self.bpm))
		
	#@ui.in_background	
	def click(self):
		self.event_loop.call_later(self.delay, self.click)
		#print('click')
		#self.box.text_color = 'red'
		sound.play_effect(self.sound_effect_file)
		#time.sleep(0.02)
		#self.box.text_color = 'black'

if __name__ == '__main__':
	sound.stop_all_effects()
	view = MyMetronome()
	view.present('sheet')

