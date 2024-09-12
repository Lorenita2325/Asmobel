python3 -m venv venv
.\venv\Scripts\Activate

pip3 install -r requirements.txt
streamlit run app.py 
deactivate
  rm -rf venv 