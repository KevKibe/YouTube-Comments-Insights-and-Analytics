import streamlit as st
import subprocess

st.title("YT Dashboard")
def main():
    if st.button("Authenticate"):
        try:
            # Execute main.py as a subprocess
            subprocess.run(["python", "dashboard.py"], check=True)
            st.success("authentication executed successfully!")
        except subprocess.CalledProcessError:
            st.error("Error executing main.py")

if __name__ == "__main__":
    main()

