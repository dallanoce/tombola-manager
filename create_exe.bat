pyinstaller --onefile ^
            --noconsole ^
            --icon=src/tombola_manager/icon/icon.ico ^
            --windowed ^
            --name="Tombola Manager" ^
            --add-data "src/tombola_manager/icon/icon.ico;src/tombola_manager/icon" ^
            main.py
