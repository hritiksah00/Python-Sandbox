import datetime
import platform

system = platform.system()
release = platform.release()

print(f"System: {system}, Release: {release}, Current Time: {datetime.datetime.now()}")
