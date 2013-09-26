import winsound,sys
import os
def play_sound(sound):
	winsound.PlaySound('%s.wav' % sound, winsound.SND_FILENAME)

if __name__ == '__main__':
	config = sys.argv[1].split('$')
	if config[1] == '1':
		play_sound(config[0])
	else:
		sys.exit(1)