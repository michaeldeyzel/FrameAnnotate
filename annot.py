import numpy as np
import cv2
import pandas as pd
import sys


def display_frame(current_frame):
	ret, frame = cap.read()
	current_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
	#print(f'trying frame {current_frame}')
	if annot_sheet.iloc[int(current_frame)]['entering'] == 1:
		cv2.putText( frame,  'ENTERING',  (70, 70),  font, 1,  (0, 255, 255),  4,  cv2.LINE_4 )
		print('ENTERING here')
	if annot_sheet.iloc[int(current_frame)]['ordering'] == 1:
		cv2.putText( frame,  'ORDERING',  (270, 70),  font, 1,  (255, 0, 255),  4,  cv2.LINE_4 )
		print('ORDERING here')
	if annot_sheet.iloc[int(current_frame)]['collecting'] == 1:
		cv2.putText( frame,  'COLLECTING',  (470, 70),  font, 1,  (255, 255, 0),  4,  cv2.LINE_4 )
		print('COLLECTING here')

	#gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
	print(int(current_frame))
	cv2.putText( frame,  str(int(current_frame)),  (1632-70, 70),  font, 1,  (0, 255, 255),  2,  cv2.LINE_4 )
	frame1 = cv2.resize(frame, (int(1632/2), int(1232/2))) #half vid size
	cv2.imshow(f'Frame annotation',frame1)
	return current_frame

def put_entering(current_frame):
	print(f"Adding ENTERING on frame {current_frame}")
	annot_sheet.at[int(current_frame), 'entering'] = 1


def put_ordering(current_frame):
	print(f"Adding ORDERING on frame {current_frame}")
	annot_sheet.at[int(current_frame), 'ordering'] = 1


def put_collecting(current_frame):
	print(f"Adding COLLECTING on frame {current_frame}")
	annot_sheet.at[int(current_frame), 'collecting'] = 1




def seek_mode():
	global current_frame
	#cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
	#current_frame = start_frame
	mode = 'seek'

	print('Start seek mode in position ', int(cap.get(cv2.CAP_PROP_POS_FRAMES)))
	while(cap.isOpened() and mode == 'seek'):
		key = cv2.waitKey(0)
		#print(current_frame)
		if (key == ord('a')):

			if (current_frame != 0):
					print(f'current frame is not 0 it is {current_frame}')
					current_frame = current_frame - 2
					print(f'Ive changed it to {current_frame}')
					cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame)
					print(f'Ive set it to {current_frame}')
					current_frame = display_frame(current_frame)
					print(f'After display it is {current_frame}')
			else:
				print('Can\'t go back. First frame.')

		if (key == ord('d')):

			#current_frame = current_frame + 1
			cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame)
			current_frame = display_frame(current_frame)

		if (key == ord('q')):
			mode = 'exit'
			break

		if key == ord('e'):
			put_entering(current_frame)
			current_frame = current_frame - 1
			cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame)
			current_frame = display_frame(current_frame)

		if key == ord('b'): # go 20 frames back
			put_entering(current_frame)
			current_frame = current_frame - 20
			cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame)
			current_frame = display_frame(current_frame)

		if key == ord('o'):
			put_ordering(current_frame)
			current_frame = current_frame - 1
			cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame)
			current_frame = display_frame(current_frame)

		if key == ord('c'):
			put_collecting(current_frame)
			current_frame = current_frame - 1
			cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame)
			current_frame = display_frame(current_frame)

		if key == ord('r'):
			annot_sheet.at[int(current_frame)] = 0,0,0
			current_frame = current_frame - 1
			cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame)
			current_frame = display_frame(current_frame)

		if key == ord('j'):
			print(f'Jump to any frame < {int(cap.get(cv2.CAP_PROP_FRAME_COUNT))}:')
			fr = input('Enter frame:')
			print(f'Jumping to frame {fr}')

			cap.set(cv2.CAP_PROP_POS_FRAMES, int(fr)-1)
			current_frame = display_frame(current_frame-1)

		if (key == ord('s')):
			mode = 'play'

	return mode

def play_mode():
	global current_frame

	#cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
	#current_frame = start_frame
	mode = 'play'
	while(cap.isOpened() and mode == 'play'):

		# next_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
		# current_frame = next_frame - 1
		# previous_frame = current_frame - 1

		# if previous_frame >= 0:
		#     cap.set(cv2.CAP_PROP_POS_FRAMES, previous_frame)
		#     ret, frame = cap.read()
		current_frame = display_frame(current_frame)
		# if cv2.waitKey(700) & 0xFF == ord('q'):
		#     break
		# if 0xFF == ord('p'):
		#     cv2.waitKey(-1) #wait until any key is pressed

		tf = 0.8 # speed factor, 1 = real time speed, < 1 slow motion
		key = cv2.waitKey(int(143*tf))
		if key == ord('q'):
			mode = 'exit'
			break
		if key == ord('p'):
			cv2.waitKey(-1) #wait until any key is pressed
		if key == ord('s'):
			mode = 'seek'

		if key == ord('e'):
			put_entering(current_frame)
		if key == ord('o'):
			put_ordering(current_frame)
		if key == ord('c'):
			put_collecting(current_frame)
		if key == ord('r'):
			annot_sheet.at[int(current_frame)] = 0,0,0
		if key == ord('j'):
			print(f'Jump to any frame < {int(cap.get(cv2.CAP_PROP_FRAME_COUNT))}:')
			fr = input()
			print(f'Jumping to frame {fr}')
			cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame-1)
			current_frame = display_frame(current_frame-1)

			
	return mode


if __name__ == "__main__":
	print(f"Doing on video: {sys.argv[1]}")
	font = cv2.FONT_HERSHEY_SIMPLEX
	cap = cv2.VideoCapture(sys.argv[1])
	frame_total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
	actions = ['entering', 'ordering', 'collecting']
	file = f'{sys.argv[1]}_annotated.csv'
	try:
		annot_sheet = pd.read_csv(file, index_col=0)
		action_areas = annot_sheet.loc[(annot_sheet.loc[:, annot_sheet.dtypes != object] != 0).any(1)]
		print(action_areas)

	except FileNotFoundError: 
		annot_sheet = pd.DataFrame(0, index=np.arange(frame_total), columns=actions)

	
	print(f"The total frames in this file is {frame_total}")
	current_frame = 0
	mode = 'play' #start in play mode
	while (mode != 'exit' and current_frame < frame_total-1):
		if mode == 'play':
			mode = play_mode()
		elif mode == 'seek':
			mode = seek_mode()
		elif mode=='exit':
			break
annot_sheet.to_csv(file, index=True)
cap.release()
cv2.destroyAllWindows()



















