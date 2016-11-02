from sunfish import *

def main():	
	count = 1
	y_log_counter = 1
	x_log_counter = 0
	end = False

	pos_Y = Position(initial, 0, (True,True), (True,True), 0, 0)

	while count < 101 and not end:
		pos_Y, end, y_log_counter, x_log_counter = play(pos_Y, False, y_log_counter, x_log_counter)
		count += 1
	
if __name__ == "__main__":
	main()