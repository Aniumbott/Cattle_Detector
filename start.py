import os
import subprocess

def main():
    if os.path.isdir("venv"):
        print("venv exists")
    else:
        print("venv does not exist")
        subprocess.run("python -m venv venv", shell=True)
        print("venv created")

    # Source to venv
    activate_script = os.path.join("venv", "Scripts", "activate")
    subprocess.run(f"cmd /k {activate_script} | pip install -r requirements.txt | streamlit run app.py", shell=True)
    
if __name__ == "__main__":
    main()
