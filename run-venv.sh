python3 -m venv myenv
source myenv/bin/activate
python3 -m pip install --upgrade pip
export SYSTEM_VERSION_COMPAT=1
pip3 install -r requirements.txt
# streamlit run ./prompt_generator/prompt_generator_streamlit.py
streamlit run few.py
# deactivate
# rm -rf myenv