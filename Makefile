setup:
	python -m pip install pygithub
	python -m pip install pywin32

scout:
	python main.py --verbose

launch_script:
	python main.py --launch --n-msgs 5 --verbose