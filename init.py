import subprocess

result1 = subprocess.run(["python", "parser2.py"], capture_output=True, text=True)
if result1.returncode == 0:
    print("First file executed successfully!")
    
    result2 = subprocess.run(["python", "clarifai.py"], capture_output=True, text=True)
    result3 = subprocess.run(["python", "graph.py"], capture_output=True, text=True)
    if result2.returncode == 0:
        print("Second file executed successfully!")
        result2 = subprocess.run(["python", "dashboard.py"], capture_output=True, text=True)
    else:
        print("Error running the second file:", result2.stderr)
else:
    print("Error running the first file:", result1.stderr)
