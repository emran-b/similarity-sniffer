mkdir -p ~/.streamlit/

echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enablCORS = false\n\
\n\
" > ~/.streamlit/config.toml
